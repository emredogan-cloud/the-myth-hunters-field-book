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


def check_star_arrow(acts, rep):
    """⑧ YILDIZ SAYISI ile YUVA SAYISI — İKİ AYRI BÜYÜKLÜK (Faz 5 · A1 · A2).

    ⭑ BU DENETİM İKİ GERÇEK KUSURDAN DOĞDU VE İKİSİ DE KAPILARIN
      DIŞINDAYDI ⭑

    Levha şu kalıbı basar:

        "star box drawn as N letter squares, square k outlined,
         marked ★s → seal slot m"

    Dört sayı var ve üçü AYNI olmak zorunda: `k = s = sealStarIndex`.
    Dördüncüsü (`m = sealSlot`) BAŞKA bir büyüklüktür.

    A1 — dokuz sayfada `s`, `sealStarIndex` yerine `sealSlot` basılmıştı.
    İkisi aritmetik olarak imkânsızdı: altı harfli bir sözcükte ★7,
    dört harfli bir sözcükte ★5. `monsoon` bölgesinin yedi mühür
    sayfasının altısı bu listedeydi — o bölgenin mühür sözcüğü
    KURULAMAZDI.

    A2 — ön madde ve altı bölge açılışı şu kuralı basıyordu:
    *"Copy that letter into the seal slot with the same number."*
    Ölçüm: `sealStarIndex != sealSlot` → 37 sayfanın **27'sinde**.

        Levha doğruydu, KURAL yanlıştı. Ve bir kuralı okuyup levhaya
        bakmayan bir okur harfleri yanlış yuvalara yazardı.

    Neden hiçbir kapı görmedi: `qa_solvable § ⑦` HARFİ yeniden hesaplıyor
    (37/37 doğru) ve `qa_design § ②` kutunun VARLIĞINI denetliyor. İkisi de
    doğruydu. Kimse **basılı sayının** doğru sayı olduğunu sormamıştı.
    """
    print("\n── ⑧ yıldız sayısı ↔ yuva sayısı (A1 · A2) ──")
    # ⚠ KARE SAYISI SÖZCÜKLE YAZILIR ("six letter squares"), rakamla değil.
    # İlk hâl `\d+` arıyordu ve 37 sayfanın 37'sini "kutusuz" sanmıştı —
    # yani kapı doğru sayfaları kusurlu ilan ediyordu. Bir kapının ilk
    # koşusunda yanlış yönde arızalanması bu projede üçüncü kez oldu.
    WORDNUM = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
               "seven": 7, "eight": 8, "nine": 9, "ten": 10}
    pat = re.compile(r"star box drawn as (\w+) letter squares?, "
                     r"square (\d+) outlined, marked ★(\d+)\s*→\s*seal slot (\d+)")
    # ⚠ Bu denetim BASILI levhayı okur. Manuscript depoda yoksa (K10)
    # `pagePrints` hiç yoktur ve o hâlde denetlenecek bir levha da yoktur.
    # Kapı burada BOŞ KOŞAR — kusurlu ilan etmez.
    seal_pages = [a for a in acts if a.get("sealSlot")]
    with_prints = [a for a in seal_pages if a.get("pagePrints")]
    if not with_prints:
        print("  ⊘ levha metni yok (manuscript depoda durmaz) — BOŞ KOŞTU")
        return sum(1 for a in seal_pages
                   if a.get("sealStarIndex") != a.get("sealSlot"))

    seen = 0
    no_print, wrong_sq, wrong_star, wrong_slot, impossible, wrong_len = \
        [], [], [], [], [], []
    for a in with_prints:
        seen += 1
        aid = a["activityId"]
        blob = " ".join(a.get("pagePrints") or [])
        m = pat.search(blob)
        if not m:
            no_print.append(aid)
            continue
        sq_raw = m.group(1)
        squares = (int(sq_raw) if sq_raw.isdigit()
                   else WORDNUM.get(sq_raw.lower(), -1))
        outlined, star, slot = (int(x) for x in m.groups()[1:])
        si = a.get("sealStarIndex")
        word = a.get("sealStarWord") or ""
        if squares != len(word):
            wrong_len.append("%s (%d kare · %d harf)" % (aid, squares, len(word)))
        if outlined != si:
            wrong_sq.append("%s (çerçeve %d · index %s)" % (aid, outlined, si))
        # ⭑ A1'İN KENDİSİ ⭑
        if star != si:
            wrong_star.append("%s (★%d · index %s)" % (aid, star, si))
        if slot != a["sealSlot"]:
            wrong_slot.append("%s (yuva %d · kayıt %s)" % (aid, slot, a["sealSlot"]))
        # Aritmetik imkânsızlık: sözcükte o harf YOK.
        if star > len(word):
            impossible.append("%s (★%d · sözcük %d harf)" % (aid, star, len(word)))

    rep.facts["sealPagesWithPrintedBox"] = seen - len(no_print)
    rep.check(not no_print, "her mühür sayfası yıldız kutusunu levhaya basıyor"
              + ("" if not no_print else " — BASMAYAN: %s" % no_print[:5]))
    rep.check(not wrong_len, "yıldız kutusu kare sayısı sözcük uzunluğuyla aynı"
              + ("" if not wrong_len else " — AYRIK: %s" % wrong_len[:5]))
    rep.check(not wrong_sq, "çerçeveli kare harf sırasıyla aynı"
              + ("" if not wrong_sq else " — AYRIK: %s" % wrong_sq[:5]))
    rep.check(not wrong_star,
              "⭑ BASILI ★ SAYISI HARF SIRASIDIR, yuva numarası DEĞİL"
              + ("" if not wrong_star else " — AYRIK: %s" % wrong_star[:9]))
    rep.check(not impossible,
              "⭑ hiçbir ★ sözcüğün dışına düşmüyor"
              + ("" if not impossible else " — İMKÂNSIZ: %s" % impossible))
    rep.check(not wrong_slot, "basılı yuva numarası kayıtla aynı"
              + ("" if not wrong_slot else " — AYRIK: %s" % wrong_slot[:5]))

    # ⭑ A2 · BASILI KURAL, İKİ SAYIYI AYNI SAYI İLAN EDEMEZ ⭑
    #
    # Ölçüm bunu bir kez ve toplu olarak yapar: eğer bir tek sayfada bile
    # index ≠ slot ise, "aynı numaralı yuva" diyen bir kural YANLIŞTIR.
    diff = sum(1 for a in acts
               if a.get("sealSlot") and a.get("sealStarIndex") != a["sealSlot"])
    rep.facts["starIndexDiffersFromSlot"] = diff
    print("  ★ ile yuva farklı olan sayfa: %d / %d" % (diff, seen))
    return diff


def check_printed_rule(book, diff, rep):
    """⑨ BASILI KURAL ÖLÇÜMLE UYUŞUYOR MU (A2).

    Kural metni yalnızca ölçüm onu doğruluyorsa 'aynı numara' diyebilir.
    Bir tek sayfada bile ayrılıyorlarsa o cümle yanlıştır ve okuru yanlış
    yuvaya yollar."""
    print("\n── ⑨ basılı mühür kuralı (A2) ──")
    BAD = re.compile(r"seal slot (?:with|carrying) the same number", re.I)
    hits = []
    for r in book.get("regionOpenings") or []:
        if BAD.search(r.get("openingText") or ""):
            hits.append("regionOpening:" + r.get("regionId", "?"))
    for s in (book.get("frontMatter") or {}).get("sections") or []:
        blob = (s.get("bodyText") or "") + " " + " ".join(s.get("prints") or [])
        if BAD.search(blob):
            hits.append("frontMatter:" + s.get("id", "?"))
    for s in (book.get("backMatter") or {}).get("sections") or []:
        blob = (s.get("purpose") or "") + " " + " ".join(s.get("prints") or [])
        if BAD.search(blob):
            hits.append("backMatter:" + s.get("id", "?"))
    if diff:
        rep.check(not hits,
                  "⭑ hiçbir yer 'aynı numaralı yuva' KURALINI basmıyor "
                  "(ölçüm: %d sayfada farklılar)" % diff
                  + ("" if not hits else " — YANLIŞ KURAL: %s" % hits))
    else:
        rep.check(True, "ölçümde ★ ile yuva hiç ayrılmıyor — kural serbest")


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

    if acts:
        diff = check_star_arrow(acts, rep)
        if book_doc:
            check_printed_rule(book_doc, diff, rep)
    else:
        print("\n── ⑧⑨ ──")
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
