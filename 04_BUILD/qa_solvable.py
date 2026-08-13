#!/usr/bin/env python3
"""
TEK CEVAPLILIK KAPISI — The Myth Hunter's Field Book
================================================================================
Bu kapının tek bir gerekçesi var ve o gerekçe pedagojiktir:

    Çift cevaplı bir bulmaca, çocuğa "BEN yanlış yaptım" dedirtir.

Çocuk cevabını arka maddeyle karşılaştırır, tutmadığını görür ve suçu
kendinde arar. Oysa kusur tasarımdadır. Bu, kitabın vaadini — çocuk
kendi kendini doğrulayabilsin — doğrudan kırar.

Sekiz denetim:

  ① CEVAP VARLIĞI   — açık uçlu olmayan her yazılmış aktivitenin cevabı var mı
  ② AÇIK UÇLULUK    — openEnded yalnızca 'make' tipinde mi (kaçış kapısı değil)
  ③ ÖLÇÜT           — openEnded bir aktivite ÖLÇÜLEBİLİR bir başarı ölçütü taşıyor mu
  ④ BELİRSİZ DİL    — cevap "ya da / olabilir / yaklaşık" taşıyor mu
  ⑤ İPUCU SIZINTISI — ipucu cevabın kendisini söylüyor mu
  ⑥ ÇOKLU CEVAP     — bir cevap alanı birden çok kabul edilebilir sonuç mu sayıyor
  ⑦ MÜHÜR BELİRLENİMİ — mühür harfi cevaptan MEKANİK olarak çıkıyor mu
  ⑧ FIELD NOTE       — kültürel bilgi kutusu cevabı SÖYLÜYOR mu  ⭑

③ NEDEN VAR: `openEnded: true` bir kaçış kapısı DEĞİLDİR. "Cevabı zor
buldum, açık uçlu yapayım" demek kitabın ölçülebilirliğini yer. Açık uçlu
bir aktivite bile bir KISIT taşır: tek yollu labirent, dört noktadan
sonra bir çubuk, iki tepe. Kısıt yaratıcılığı öldürmez, MÜMKÜN KILAR.

⑤ NEDEN VAR: ipucu yardım eder, çözmez. Cevabı içeren bir ipucu
aktiviteyi ortadan kaldırır ve çocuk bunu bir kez öğrenirse bir daha
denemez — doğrudan ipucuna gider.

⑦ NEDEN VAR: mühür harfi bir insanın seçtiği bir harf DEĞİLDİR. Sayfada
basılı bir sözcüğün belirli bir harfidir ve bu kapı hesabı YENİDEN YAPAR.
Elle yazılmış bir `sealContribution` ile hesaplanan harf ayrılırsa
çocuk bölgeyi çözemez.

⚠ MANUSCRIPT DEPODA DEĞİLDİR. Dosya yoksa kapı BOŞ KOŞAR ve yeşil yanar;
körlüğü `05_TESTS/selftest.py` kapatır.

TASARIM: yalnızca Python standart kütüphanesi (karar K7).

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CONFIG = os.path.join(ROOT, "project_config.json")
ACTIVITY_INDEX = os.path.join(ROOT, "01_SOURCE", "activity_index.json")
BOOK = os.path.join(ROOT, "02_MANUSCRIPT", "book.json")

# ④ Cevabı belirsizleştiren kalıplar. Bir cevap alanında geçerlerse
# aktivitenin TEK bir doğrusu yoktur.
HEDGE = [
    (r"\bor\b(?!\s*(?:more|fewer|less)\b)", "'or' — iki cevap"),
    (r"\bany\s+of\b", "'any of'"),
    (r"\beither\b", "'either'"),
    (r"\bmight\b|\bmaybe\b|\bperhaps\b|\bpossibly\b", "olasılık kipi"),
    (r"\babout\s+\d", "'about N' — yaklaşık sayı"),
    (r"\bapprox\w*", "'approx'"),
    (r"\bacceptable\s+answers?\b", "'acceptable answers'"),
    (r"\bpossible\s+answers?\b", "'possible answers'"),
    (r"\banswers?\s+(?:may|can)\s+vary\b", "'answers may vary'"),
    (r"\betc\.?\b", "'etc'"),
    (r"\.\.\.", "üç nokta — liste açık bırakılmış"),
]

# Cevap alanında birden çok sonucu AYIRAN meşru işaretler. Bunlar bir
# aktivitenin BİRDEN ÇOK KUTUSU olduğunu söyler, birden çok DOĞRUSU değil.
FIELD_SEP = re.compile(r"\s·\s")


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
    """Tasarım katmanı + proza katmanı. Kapı ikisini BİRLİKTE görmeli:
    `type` tasarımda, `answer` prozada durur."""
    design = {a["activityId"]: a
              for a in (index_doc or {}).get("activities", [])}
    out = []
    for p in (book_doc or {}).get("activities", []):
        base = dict(design.get(p.get("activityId"), {}))
        base.update(p)
        out.append(base)
    return out


def norm_words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9ʻ'’]+", (text or "").lower())


def check_answer_present(acts, rep):
    print("\n── ① cevap varlığı ──")
    missing = [a["activityId"] for a in acts
               if not a.get("openEnded") and not (a.get("answer") or "").strip()]
    rep.check(not missing, "açık uçlu olmayan her sayfanın cevabı var"
              + ("" if not missing else " — CEVAPSIZ: %s" % missing[:5]))


def check_open_ended(cfg, acts, rep):
    print("\n── ② açık uçluluk · ③ ölçülebilir ölçüt ──")
    exempt = set(cfg.get("solvability", {}).get("openEndedTypeExempt", []))
    wrong_type = ["%s (%s)" % (a["activityId"], a.get("type"))
                  for a in acts if a.get("openEnded") and a.get("type") not in exempt]
    rep.check(not wrong_type, "openEnded yalnızca %s tipinde" % sorted(exempt)
              + ("" if not wrong_type else " — KAÇIŞ KAPISI: %s" % wrong_type))

    # Açık uçlu OLMAK ölçüsüz olmak demek değildir.
    no_crit = [a["activityId"] for a in acts
               if a.get("openEnded") and not (a.get("expectedResult") or "").strip()]
    rep.check(not no_crit, "her açık uçlu sayfa ölçülebilir bir ölçüt taşıyor"
              + ("" if not no_crit else " — ÖLÇÜTSÜZ: %s" % no_crit[:5]))

    # Ölçüt bir KISIT söylemeli. "Be creative" bir ölçüt değildir.
    vague = [a["activityId"] for a in acts
             if a.get("openEnded")
             and len(norm_words(a.get("expectedResult"))) < 8]
    rep.check(not vague, "açık uçlu ölçütler somut (≥8 kelime)"
              + ("" if not vague else " — MUĞLAK: %s" % vague[:5]))

    n = sum(1 for a in acts if a.get("openEnded"))
    rep.facts["openEnded"] = n
    rep.facts["openEndedRatio"] = round(n / len(acts), 3) if acts else 0


def check_hedging(acts, rep):
    print("\n── ④ belirsiz cevap dili ──")
    hits = []
    for a in acts:
        ans = a.get("answer") or ""
        if not ans:
            continue
        for pat, name in HEDGE:
            if re.search(pat, ans, re.IGNORECASE):
                hits.append("%s → %s" % (a["activityId"], name))
                break
    rep.check(not hits, "hiçbir cevap belirsiz dil taşımıyor"
              + ("" if not hits else " — BELİRSİZ: %s" % hits[:5]))


def check_hint_leak(acts, rep):
    print("\n── ⑤ ipucu sızıntısı ──")
    leaked = []
    for a in acts:
        ans = a.get("answer") or a.get("expectedResult") or ""
        if not ans:
            continue
        # Cevabın AYIRT EDİCİ parçaları: ayraçla bölünmüş her alan.
        fields = [f.strip() for f in FIELD_SEP.split(ans) if f.strip()]
        for h in (a.get("hints") or []):
            hw = set(norm_words(h))
            for f in fields:
                fw = [w for w in norm_words(f) if len(w) > 3]
                # ⚠ EN AZ İKİ anlamlı sözcük aranır ve bu bir kalibrasyondur.
                # İlk hâli tek sözcükle de eşleşiyordu ve "cord C 8" cevabını
                # "One cord has nothing in its lowest place." ipucunun
                # SIZDIRDIĞINI sandı. Oysa 'cord' sayfanın her yerinde geçen
                # sıradan bir addır; bir alanı ele vermez.
                #
                # Tek sözcüklük bir alanı ele veren şey ipucu değil, o
                # sözcüğün kendisidir — ve o zaten cevabın parçasıdır.
                if len(set(fw)) < 2:
                    continue
                # Bir ipucu, bir cevap alanının BÜTÜN anlamlı sözcüklerini
                # taşıyorsa o alanı söylemiş demektir.
                if set(fw) <= hw:
                    leaked.append("%s → ipucu '%s…' cevabı söylüyor"
                                  % (a["activityId"], h[:32]))
                    break
    rep.check(not leaked, "hiçbir ipucu cevabı içermiyor"
              + ("" if not leaked else " — SIZINTI: %s" % leaked[:5]))


def check_seal_determinism(acts, rep):
    """⑦ Mühür harfi ELLE YAZILMAZ, HESAPLANIR.

    Sayfada yıldızlı bir kutu vardır; yıldızın içindeki sayı, o kutuya
    yazılan basılı sözcüğün kaçıncı harfinin mühre gideceğini söyler.
    Bu kapı hesabı yeniden yapar ve beyanla karşılaştırır."""
    print("\n── ⑦ mühür harfi belirlenimi ──")
    sealed = [a for a in acts if a.get("sealSlot")]
    rep.facts["sealedPages"] = len(sealed)
    if not sealed:
        print("  ⊘ mühür taşıyan sayfa yok")
        return

    problems = []
    for a in sealed:
        aid = a["activityId"]
        word = (a.get("sealStarWord") or "").strip()
        idx = a.get("sealStarIndex")
        declared = (a.get("sealContribution") or "").strip()

        if a.get("openEnded"):
            problems.append("%s açık uçlu ama mühür besliyor" % aid)
            continue
        if not word or not isinstance(idx, int):
            problems.append("%s yıldızlı sözcük veya sayı taşımıyor" % aid)
            continue
        if not (1 <= idx <= len(word)):
            problems.append("%s yıldız sayısı sözcüğün dışında (%d/%d)"
                            % (aid, idx, len(word)))
            continue

        computed = word[idx - 1].upper()
        if declared and computed != declared.upper():
            problems.append("%s hesap=%s beyan=%s" % (aid, computed, declared))

        # Yıldızlı sözcük sayfada BASILI olmalı: çocuk kopyalar, üretmez.
        # Basılı olduğunun kanıtı, sözcüğün cevapta geçmesidir.
        ans = (a.get("answer") or "").lower()
        if word.lower() not in ans:
            problems.append("%s yıldızlı sözcük '%s' cevapta geçmiyor "
                            "— sayfada basılı olduğu kanıtlanamıyor" % (aid, word))

    rep.check(not problems, "mühür harfi cevaptan mekanik olarak çıkıyor"
              + ("" if not problems else " — İHLAL: %s" % problems[:5]))


def check_fieldnote_gives_answer(acts, rep):
    """⑧ FIELD NOTE CEVABI SÖYLÜYOR MU.

    ⭑ BU DENETİM DE İÇ EDİTORYAL İNCELEMEDEN DOĞDU ⭑

    İnceleme pilotun BEŞ sayfasında aynı kusuru buldu: kültürel bilgi
    kutusu, görevin cevabını dört saniye önce söylüyordu.

        field note : "Maize keeps to the lower quechua band, potatoes
                      climb into the suni, and llamas graze the puna."
        görev      : "Draw a line from each card to its band."

    Çocuk düşünmüyor, KOPYALIYOR. Ve `ACTIVITY_TAXONOMY § 2.4` her gözlem
    sayfasının bir ÇIKARIM istemesini şart koşuyor.

    Field note'un işi görevi kurmaktır, bitirmek değil:

        ✓ "These lake gardens do not float, though people often say
           they do."                                    (bir soru açar)
        ✗ "…and their roots reach down and hold the plot."  (soruyu kapatır)

    ÖLÇÜM: cevap alanları ile field note karşılaştırılır. Bir cevap
    alanının bütün anlamlı sözcükleri field note'ta geçiyorsa, o alan
    zaten söylenmiştir.
    """
    print("\n── ⑧ field note cevabı söylüyor mu ──")
    told = []
    for a in acts:
        note = set(norm_words(a.get("fieldNote")))
        if not note:
            continue
        ans = a.get("answer") or ""
        if not ans:
            continue
        fields = [f.strip() for f in FIELD_SEP.split(ans) if f.strip()]
        given = 0
        worst = ""
        for f in fields:
            fw = [w for w in norm_words(f) if len(w) > 3]
            if len(set(fw)) < 2:
                continue
            if set(fw) <= note:
                given += 1
                worst = f[:40]
        # Bir alan tesadüf olabilir; İKİ alan bir kalıptır.
        if given >= 2:
            told.append("%s (%d alan · '%s…')" % (a["activityId"], given, worst))
    rep.check(not told,
              "hiçbir field note cevabın çoğunu vermiyor"
              + ("" if not told else " — SÖYLÜYOR: %s" % told[:5]))


def check_multi_answer(acts, rep):
    print("\n── ⑥ çoklu cevap alanı ──")
    # Bir cevap alanı 8'den çok kutu taşıyorsa sayfa bir aktivite değil bir
    # sınavdır ve çocuk yarıda bırakır. Bu bir UYARIDIR, ret değil.
    heavy = []
    for a in acts:
        ans = a.get("answer") or ""
        if not ans:
            continue
        n = len([f for f in FIELD_SEP.split(ans) if f.strip()])
        if n > 8:
            heavy.append("%s (%d alan)" % (a["activityId"], n))
    if heavy:
        rep.warn("cevap alanı kalabalık: %s — sayfa tasarımı Faz 5'te ölçülecek"
                 % heavy[:5])
    rep.check(True, "cevap alanı sayısı ölçüldü")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    print("=" * 74)
    print("  TEK CEVAPLILIK")
    print("=" * 74)

    rep = Report(args.verbose)
    cfg = load(CONFIG, rep)
    if cfg is None:
        return 1
    index_doc = load(ACTIVITY_INDEX, rep, required=False)
    book_doc = load(BOOK, rep, required=False)

    if not book_doc:
        print("\n  ⊘ manuscript depoda yok — BOŞ KOŞTU")
        print("=" * 74)
        if args.json:
            os.makedirs(os.path.dirname(args.json), exist_ok=True)
            with open(args.json, "w", encoding="utf-8") as fh:
                json.dump({"status": "empty", "checks": 0, "errors": [],
                           "warnings": [], "facts": {}}, fh,
                          ensure_ascii=False, indent=2)
        return 0

    acts = merged(index_doc, book_doc)
    rep.facts["activities"] = len(acts)
    print("\n  · %d sayfa ölçülüyor" % len(acts))

    check_answer_present(acts, rep)
    check_open_ended(cfg, acts, rep)
    check_hedging(acts, rep)
    check_hint_leak(acts, rep)
    check_fieldnote_gives_answer(acts, rep)
    check_multi_answer(acts, rep)
    check_seal_determinism(acts, rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · %d sayfa · %d açık uçlu · %d mühür"
              % (rep.checks, len(acts), rep.facts.get("openEnded", 0),
                 rep.facts.get("sealedPages", 0)))
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
