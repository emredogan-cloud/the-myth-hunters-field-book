#!/usr/bin/env python3
"""
MÜHÜR, İLERLEME VE KURTARMA KAPISI — The Myth Hunter's Field Book
================================================================================
Mühür sistemi kitabın TAMAMLANMA GÜDÜSÜDÜR. Bir çocuk mührü çözemezse
kitabı bitiremez ve ebeveyn bunu yoruma yazar. Bu yüzden mühür bir süs
değil, mekanik olarak denetlenmesi gereken bir YAPIDIR.

Ama bu kapının asıl işi başka bir şey ve adı yol haritasında geçmiyordu:

    ⭑ BİR YANLIŞ CEVAP ÇOCUĞU KİTABIN GERİ KALANINDAN KİLİTLEYEMEZ ⭑

Bir bulmaca kitabı zincirleme kurulursa (7. sayfanın cevabı 8. sayfanın
girdisidir) tek bir hata çocuğu durdurur ve çocuk PES EDER. Bu, ürünün
en büyük yapısal riskidir ve ölçülmeden bilinmez.

Yedi denetim:

  ① YUVA BÜTÜNLÜĞÜ  — yuvalar 1…N bitişik ve her biri TAM BİR kez dolu mu
  ② HARF TÜREVİ     — yıldızlı sözcüğün harfi bölge sözcüğünü kuruyor mu
  ③ ÇENTİK          — çentik harfi sözcükten doğru konumda mı çıkıyor
  ④ FİNAL           — altı çentik harfi final sözcüğü kuruyor mu
  ⑤ BAĞIMSIZLIK     — bir sayfanın çözümü BAŞKA bir sayfanın cevabına mı bağlı
  ⑥ HASAR YARIÇAPI  — tek bir yanlış cevap kaç harfi bozuyor  (1 OLMALI)
  ⑦ GERİ BİLDİRİM   — çocuk cevap anahtarına bakmadan hatasını görebiliyor mu

⑤ ve ⑥ BİRLİKTE "felâket kapısı yok" ölçütünü kurar:

    Bir hata GERİ BİLDİRİM olmalıdır, TOPLAM BAŞARISIZLIK değil.

⑥ neden 1 olmalı: bir yuvayı TAM BİR aktivite besler. İki aktivite aynı
yuvayı beslerse ya da bir aktivite iki yuva beslerse, tek bir hata iki
harfi birden bozar ve çocuk hangi sayfaya döneceğini BULAMAZ.

⑦ neden var: mühür sözcüğü ANLAMLIDIR. Beş harfi doğru, biri yanlış olan
bir sözcük çocuğa "burada bir şey yanlış" der ve hangi yuvanın bozuk
olduğunu gösterir. Anlamsız bir harf dizisi bunu YAPAMAZ — çocuk hatasını
ancak cevap anahtarından öğrenir ve o an oyun biter.

⭑ AYRICA ÖLÇÜLEN: 37 mühür harfinin yalnızca 6'sı final göreve taşınır.
Yani bir bölgede yapılan hata final cevabı çoğu zaman HİÇ etkilemez.
Bu bir tasarım kazasıdır ve raporlanmaya değer.

⚠ CEVAP ANAHTARI DEPODA DEĞİLDİR (K10). Dosya yoksa kapı ATLAR ve yeşil
yanar — tıpkı manuscript yokken metin kapılarının boş koşması gibi.
Kapı hiçbir koşulda bir mühür sözcüğünü EKRANA BASMAZ.

TASARIM: yalnızca Python standart kütüphanesi (karar K7).

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ACTIVITY_INDEX = os.path.join(ROOT, "01_SOURCE", "activity_index.json")
REGION_INDEX = os.path.join(ROOT, "01_SOURCE", "region_index.json")
BOOK = os.path.join(ROOT, "02_MANUSCRIPT", "book.json")
SEAL_KEY = os.path.join(ROOT, "01_SOURCE", "answers", "seal_key.json")

# ⑤ Bir sayfanın başka bir sayfaya BAĞIMLI olduğunu gösteren kalıplar.
CHAIN = re.compile(
    r"\b(?:your answer (?:from|to) page|the answer from page|"
    r"from the previous page|as you found on page|"
    r"using page \d|from page \d)\b", re.IGNORECASE)

MIN_RECOVERABLE_LETTERS = 4


class Report:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks = 0
        self.facts: dict = {}

    def check(self, cond: bool, label: str) -> bool:
        self.checks += 1
        if cond:
            if self.verbose:
                print("  ✓ %s" % label)
        else:
            self.errors.append(label)
            print("  ✗ %s" % label)
        return cond

    def warn(self, label: str) -> None:
        self.warnings.append(label)
        print("  ! %s" % label)


def load(path, rep, required=True):
    if not os.path.exists(path):
        if required:
            rep.check(False, "dosya yok: %s" % os.path.relpath(path, ROOT))
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        rep.check(False, "JSON bozuk: %s — %s" % (os.path.relpath(path, ROOT), exc))
        return None


def merged(index_doc, book_doc):
    design = {a["activityId"]: a for a in (index_doc or {}).get("activities", [])}
    out = []
    for p in (book_doc or {}).get("activities", []):
        base = dict(design.get(p.get("activityId"), {}))
        base.update(p)
        out.append(base)
    return out


# ── ① YUVA BÜTÜNLÜĞÜ ───────────────────────────────────────────────────────
def check_slots(acts_all, regions, rep):
    print("\n── ① yuva bütünlüğü ──")
    problems = []
    total = 0
    for r in regions:
        want = r.get("sealLetterCount", 0)
        total += want
        slots = [a["sealSlot"] for a in acts_all
                 if a.get("region") == r["id"] and a.get("sealSlot")
                 and a.get("status") != "dropped"]
        counts = collections.Counter(slots)
        for i in range(1, want + 1):
            if counts[i] != 1:
                problems.append("%s yuva %d → %d aktivite" % (r["id"], i, counts[i]))
        for s in counts:
            if s > want:
                problems.append("%s yuva %d mühür uzunluğunun dışında" % (r["id"], s))
    rep.facts["sealSlotsTotal"] = total
    rep.check(not problems, "her yuva tam bir aktivite tarafından besleniyor"
              + ("" if not problems else " — İHLAL: %s" % problems[:6]))


# ── ⑥ HASAR YARIÇAPI ───────────────────────────────────────────────────────
def check_damage_radius(acts_all, regions, rep):
    """Tek bir yanlış cevap kaç harfi bozar? Cevap 1 OLMALIDIR."""
    print("\n── ⑥ hasar yarıçapı ──")
    worst = 0
    offenders = []
    for r in regions:
        by_activity = collections.Counter()
        for a in acts_all:
            if a.get("region") == r["id"] and a.get("sealSlot") \
                    and a.get("status") != "dropped":
                by_activity[a["activityId"]] += 1
        for aid, n in by_activity.items():
            if n > 1:
                offenders.append("%s → %d yuva" % (aid, n))
            worst = max(worst, n)
    rep.facts["damageRadius"] = worst
    rep.check(not offenders,
              "bir yanlış cevap tam BİR harfi bozuyor (yarıçap %d)" % worst
              + ("" if not offenders else " — ÇOK YUVALI: %s" % offenders[:5]))


# ── ⑤ BAĞIMSIZLIK ──────────────────────────────────────────────────────────
def check_independence(acts, rep):
    """Zincirleme bir kitap, tek hatada durur. Bu kitap zincirlenmez."""
    print("\n── ⑤ sayfa bağımsızlığı ──")
    chained = []
    ids = {a.get("activityId") for a in acts}
    for a in acts:
        blob = " ".join([a.get("prompt", ""), a.get("setup", "")]
                        + list(a.get("steps") or [])
                        + list(a.get("hints") or []))
        if CHAIN.search(blob):
            chained.append(a["activityId"])
            continue
        # Bir sayfa başka bir sayfanın kimliğini anıyorsa da bağımlıdır.
        for other in ids:
            if other != a.get("activityId") and other in blob:
                chained.append("%s → %s" % (a["activityId"], other))
                break
    rep.check(not chained,
              "hiçbir sayfa başka bir sayfanın cevabına bağlı değil"
              + ("" if not chained else " — ZİNCİR: %s" % chained[:5]))
    rep.facts["chainedPages"] = len(chained)


# ── ②③④⑦ ANAHTARA BAĞLI DENETİMLER ────────────────────────────────────────
def check_with_key(acts, regions, key, rep):
    """⚠ Bu fonksiyon hiçbir mühür sözcüğünü ekrana BASMAZ."""
    print("\n── ② harf türevi · ③ çentik · ④ final · ⑦ geri bildirim ──")
    seals = {s["region"]: s for s in key.get("seals", [])}
    by_region = collections.defaultdict(dict)
    for a in acts:
        if a.get("sealSlot"):
            by_region[a.get("region")][a["sealSlot"]] = a

    derived_bad, notch_bad, short = [], [], []
    covered = 0
    for r in regions:
        rid = r["id"]
        s = seals.get(rid)
        if not s:
            continue
        word = (s.get("word") or "").upper()
        slots = by_region.get(rid, {})
        if not slots:
            continue                      # o bölge henüz yazılmadı
        covered += 1

        # ② her yazılmış yuva, sözcüğün o konumdaki harfini üretmeli
        for slot, a in sorted(slots.items()):
            star = (a.get("sealStarWord") or "")
            idx = a.get("sealStarIndex")
            if not star or not isinstance(idx, int) or not (1 <= idx <= len(star)):
                derived_bad.append("%s yuva %d: yıldız tanımsız" % (rid, slot))
                continue
            got = star[idx - 1].upper()
            if not (1 <= slot <= len(word)):
                derived_bad.append("%s yuva %d sözcük boyunun dışında" % (rid, slot))
            elif got != word[slot - 1]:
                # Harfin KENDİSİ basılmaz; yalnızca UYUŞMADIĞI söylenir.
                derived_bad.append("%s yuva %d: türetilen harf sözcükle uyuşmuyor"
                                   % (rid, slot))

        # ③ çentik
        np = s.get("notchPosition")
        nl = (s.get("notchLetter") or "").upper()
        if not isinstance(np, int) or not (1 <= np <= len(word)):
            notch_bad.append("%s çentik konumu geçersiz" % rid)
        elif word[np - 1] != nl:
            notch_bad.append("%s çentik harfi sözcükle uyuşmuyor" % rid)

        # ⑦ geri bildirim: kısa bir sözcük tek hatada kurtarılamaz
        if len(word) < MIN_RECOVERABLE_LETTERS:
            short.append("%s (%d harf)" % (rid, len(word)))

    rep.facts["regionsWithWrittenSeals"] = covered
    rep.check(not derived_bad,
              "yazılmış her yuva bölge sözcüğünün doğru harfini üretiyor"
              + ("" if not derived_bad else " — UYUŞMUYOR: %s" % derived_bad[:5]))
    rep.check(not notch_bad, "her çentik harfi sözcükten doğru konumda çıkıyor"
              + ("" if not notch_bad else " — ÇENTİK: %s" % notch_bad[:5]))
    rep.check(not short,
              "her mühür sözcüğü tek hatadan kurtarılabilecek uzunlukta (≥%d)"
              % MIN_RECOVERABLE_LETTERS
              + ("" if not short else " — KISA: %s" % short[:5]))

    # ④ final: altı çentik harfi final sözcüğü kurmalı
    fq = key.get("finalQuest", {})
    final_word = (fq.get("word") or "").upper()
    ordered = sorted(regions, key=lambda x: x.get("order", 99))
    built = "".join((seals.get(r["id"], {}).get("notchLetter") or "").upper()
                    for r in ordered)
    rep.check(built == final_word,
              "altı çentik harfi final sözcüğü kuruyor (%d harf)" % len(final_word))

    # ⭑ ÖLÇÜM: 37 harfin kaçı final cevaba taşınıyor
    total_letters = sum(len((seals.get(r["id"], {}).get("word") or ""))
                        for r in regions)
    rep.facts["sealLettersTotal"] = total_letters
    rep.facts["lettersReachingFinal"] = len([r for r in regions if r["id"] in seals])
    if total_letters:
        pct = 100.0 * rep.facts["lettersReachingFinal"] / total_letters
        rep.facts["finalPropagationPct"] = round(pct, 1)
        print("  · %d mühür harfinin %d'i final göreve taşınıyor (%%%.1f) — "
              "bir bölgedeki hata final cevabı çoğu zaman ETKİLEMEZ"
              % (total_letters, rep.facts["lettersReachingFinal"], pct))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    print("=" * 74)
    print("  MÜHÜR, İLERLEME VE KURTARMA")
    print("=" * 74)

    rep = Report(args.verbose)
    index_doc = load(ACTIVITY_INDEX, rep, required=False)
    reg_doc = load(REGION_INDEX, rep, required=False)
    book_doc = load(BOOK, rep, required=False)

    if index_doc is None or reg_doc is None:
        print("\n  ⊘ dizinler yok — BOŞ KOŞTU")
        print("=" * 74)
        return 0

    regions = reg_doc.get("regions", reg_doc)
    acts_all = index_doc.get("activities", [])
    acts = merged(index_doc, book_doc)

    check_slots(acts_all, regions, rep)
    check_damage_radius(acts_all, regions, rep)
    if acts:
        check_independence(acts, rep)
    else:
        print("\n── ⑤ sayfa bağımsızlığı ──")
        print("  ⊘ manuscript depoda yok — boş koştu")

    key = load(SEAL_KEY, rep, required=False)
    if key is None:
        print("\n── ②③④⑦ ──")
        print("  ⊘ cevap anahtarı bu makinede yok (K10) — ATLANDI, kırmızı DEĞİL")
    elif acts:
        check_with_key(acts, regions, key, rep)
    else:
        print("\n── ②③④⑦ ──")
        print("  ⊘ proza yok — anahtar denetimi atlandı")

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · %d yuva · hasar yarıçapı %d"
              % (rep.checks, rep.facts.get("sealSlotsTotal", 0),
                 rep.facts.get("damageRadius", 0)))
        status = "pass"
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": status, "checks": rep.checks,
                       "errors": rep.errors, "warnings": rep.warnings,
                       "facts": rep.facts}, fh, ensure_ascii=False, indent=2)
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
