#!/usr/bin/env python3
"""
TALİMAT NETLİĞİ KAPISI — The Myth Hunter's Field Book
================================================================================
    Çocuk takılıyorsa suç çocukta değil TALİMATTADIR.

`qa_readability.py` talimatın OKUNABİLİRLİĞİNİ ölçer: kaç kelime, kaç
hece, hangi sınıf seviyesi. Bu kapı başka bir şeye bakar — talimatın
BİÇİMİNE. Bir cümle mükemmel okunabilir olup yine de ne yapılacağını
söylemeyebilir.

    "The stones are arranged in an interesting order."

Bu cümle FK 3'tür ve bir TALİMAT DEĞİLDİR. Çocuk okur, anlar, ve hiçbir
şey yapmaz.

Dokuz denetim:

  ① EMİR KİPİ      — her adım bir FİİLLE başlıyor mu
  ② İKİNCİ ŞAHIS   — sayfa çocuğa doğrudan sesleniyor mu ('you' · 'your')
  ③ ADIM SAYISI    — ≤4, ★ için ≤2 (AGE_POLICY § 7)
  ④ CÜMLE UZUNLUĞU — hiçbir talimat cümlesi 18 kelimeyi aşmıyor mu
  ⑤ GÖREV SATIRI   — her sayfa 'Your mission:' kalıbıyla açılıyor mu
  ⑥ ADIM BİRLİĞİ   — bir adım iki iş birden istiyor mu ('and then')
  ⑦ İSİMSİZ REFERANS — 'it' ve 'them' neye işaret ettiği belirsiz mi
  ⑧ YAZMA ALANI    — yazdıran bir sayfa yazacak yer bırakmış mı
  ⑨ GÖNDERME       — 'the key' dediğinde sayfada gerçekten anahtar var mı  ⭑

⑥ NEDEN VAR: "Read the clues and then draw a line and mark the odd one"
bir adım gibi görünür, üç iştir. Çocuk ikincisini unutur ve eksik cevap
verir — sonra kendini suçlar. Adım sayısı sınırı, adımlar GERÇEKTEN tek
işlemse anlamlıdır.

⑧ NEDEN VAR: bir çocuk kitabında "yaz" demek yetmez. Yazacak yer yoksa
çocuk kitabın kenarına yazar veya hiç yazmaz. Faz 5 alanı MİLİMETREYLE
ölçecek; bu kapı ALANIN VARLIĞINI şimdiden şart koşar.

⚠ MANUSCRIPT DEPODA DEĞİLDİR. Dosya yoksa kapı BOŞ KOŞAR.

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

MISSION_LINE = re.compile(r"^Your mission:\s+\S", re.IGNORECASE)

# ① Bir adım bir FİİLLE başlar. Bu kitabın gerçekten kullandığı fiiller —
# liste kapalıdır ve yeni bir fiil eklemek bilinçli bir karardır.
IMPERATIVES = {
    "add", "circle", "colour", "compare", "copy", "count", "cross", "draw",
    "fill", "find", "follow", "join", "label", "look", "mark", "match",
    "measure", "name", "number", "order", "put", "read", "ring", "shade",
    "sort", "start", "tick", "trace", "turn", "use", "walk", "write",
    "check", "choose", "list", "place", "point", "show", "take", "tie",
}

# ⑥ Bir adımı iki işe bölen bağlaçlar.
SPLIT_HINT = re.compile(r"\band\s+then\b|\bafter\s+that\b|\bnext\b\s*,", re.IGNORECASE)

# ⑦ Öncülü belirsiz zamirle BAŞLAYAN adım.
DANGLING = re.compile(r"^(?:it|they|them|these|those|this)\b", re.IGNORECASE)

# ② Edilgen ve kişisiz kuruluşlar. Bir talimat çocuğa DOĞRUDAN seslenir.
#
# ⚠ DÜZENSİZ ORTAÇLAR AYRICA SAYILIR. İlk hâl yalnızca `\w+ed` arıyordu ve
# "the numbers must be READ" cümlesini KAÇIRDI — çünkü 'read' düzensizdir.
# Bu kitabın en sık kullandığı fiillerin çoğu düzensizdir (read · draw ·
# write · find · put · take), yani desen tam da en olası cümleyi kaçırıyordu.
IRREGULAR = (r"read|done|drawn|written|found|seen|made|put|taken|shown|given|"
             r"kept|held|left|told|begun|chosen|drawn|known|thought|brought")
IMPERSONAL = re.compile(
    r"\b(?:must|should|shall|can|may|will)\s+be\s+(?:\w+ed|" + IRREGULAR + r")\b"
    r"|\b(?:is|are|was|were)\s+(?:then\s+)?(?:\w+ed|" + IRREGULAR + r")\s+by\b"
    r"|\bis\s+to\s+be\b|\bare\s+to\s+be\b"
    r"|\bthe\s+(?:reader|child|pupil|student)s?\b"             # üçüncü şahıs
    r"|\bchildren\s+(?:should|must|can|will)\b"
    r"|\bone\s+(?:should|must)\b"
    r"|\bit\s+is\s+(?:necessary|important|possible)\b",
    re.IGNORECASE)

# ⑧ Çocuğun yazmasını/çizmesini isteyen fiiller.
WRITES = re.compile(r"\b(?:write|draw|number|label|fill|list|colour|shade|copy)\b",
                    re.IGNORECASE)


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


def first_word(s: str) -> str:
    m = re.match(r"\s*([A-Za-z]+)", s or "")
    return m.group(1).lower() if m else ""


def check_imperative(acts, rep):
    print("\n── ① emir kipi ──")
    bad = []
    for a in acts:
        for i, s in enumerate(a.get("steps") or [], 1):
            w = first_word(s)
            if w not in IMPERATIVES:
                bad.append("%s adım %d → '%s'" % (a["activityId"], i, w or "?"))
    rep.check(not bad, "her adım tanınmış bir emir fiiliyle başlıyor"
              + ("" if not bad else " — FİİLSİZ: %s" % bad[:5]))


def check_second_person(cfg, acts, rep):
    """② ÇOCUĞA SESLENİYOR MU — ama doğru soruyla.

    ⚠ BU DENETİMİN İLK HÂLİ ÖLÜYDÜ ve `selftest` onu ilk koşuda yakaladı.

    İlk hâli "metinde 'you' geçiyor mu" diye soruyordu. Ama ⑤ her sayfanın
    'Your mission:' ile açılmasını ŞART KOŞUYOR — yani 'Your' her zaman
    oradaydı ve denetim HİÇBİR KOŞULDA kırmızı yanamazdı.

        Hiçbir koşulda yanmayan bir kapı, bir kapı değildir.

    Gerçek risk 'you' yokluğu değil, EDİLGEN ve KİŞİSİZ sürüklenmedir:

        ✗ "The numbers must be read."        (edilgen)
        ✗ "The reader counts the dots."      (üçüncü şahıs)
        ✗ "Children should write the name."  (kişisiz öğüt)
        ✓ "Count the dots beside each basket."

    Denetim artık bunu arıyor ve ADIMLARA bakıyor — çünkü görev satırının
    kalıbı zaten ⑤ tarafından korunuyor."""
    print("\n── ② edilgen ve kişisiz sürüklenme ──")
    if not cfg.get("style", {}).get("secondPersonRequired", True):
        print("  ⊘ config ikinci şahıs şartı taşımıyor")
        return
    bad = []
    for a in acts:
        for i, s in enumerate([a.get("prompt", "")] + list(a.get("steps") or [])):
            where = "görev satırı" if i == 0 else "adım %d" % i
            m = IMPERSONAL.search(s or "")
            if m:
                bad.append("%s %s → '%s'" % (a["activityId"], where, m.group(0)))
    rep.check(not bad, "hiçbir talimat edilgen veya kişisiz kurulmuş"
              + ("" if not bad else " — KİŞİSİZ: %s" % bad[:5]))

    # Sayfanın bütünü yine de çocuğa seslenmeli; bu bir ÖLÇÜMDÜR, kapı değil
    # (kalıbı ⑤ koruyor ve iki kapı aynı şeyi denetlemez).
    addressed = sum(1 for a in acts
                    if re.search(r"\byou\b|\byour\b", a.get("prompt", ""),
                                 re.IGNORECASE))
    rep.facts["pagesAddressingReader"] = addressed


def check_step_count(acts, rep):
    print("\n── ③ adım sayısı ──")
    too_many = ["%s (%d adım)" % (a["activityId"], len(a.get("steps") or []))
                for a in acts if len(a.get("steps") or []) > 4]
    rep.check(not too_many, "hiçbir sayfa dört adımı aşmıyor"
              + ("" if not too_many else " — UZUN: %s" % too_many[:5]))

    easy_long = ["%s (%d adım)" % (a["activityId"], len(a.get("steps") or []))
                 for a in acts
                 if a.get("difficulty") == 1 and len(a.get("steps") or []) > 2]
    rep.check(not easy_long, "★ sayfaları iki adımı aşmıyor"
              + ("" if not easy_long else " — UZUN: %s" % easy_long[:5]))

    none_at_all = [a["activityId"] for a in acts if not (a.get("steps") or [])]
    rep.check(not none_at_all, "her sayfa en az bir adım taşıyor"
              + ("" if not none_at_all else " — ADIMSIZ: %s" % none_at_all[:5]))


def check_sentence_length(cfg, acts, rep):
    print("\n── ④ talimat cümlesi uzunluğu ──")
    limit = cfg.get("safety", {}).get("instructionMaxSentenceWords", 18)
    long_ones = []
    for a in acts:
        for s in [a.get("prompt", "")] + list(a.get("steps") or []):
            for sent in re.split(r"(?<=[.!?])\s+", s or ""):
                n = len(sent.split())
                if n > limit:
                    long_ones.append("%s (%d kelime)" % (a["activityId"], n))
    rep.check(not long_ones, "hiçbir talimat cümlesi %d kelimeyi aşmıyor" % limit
              + ("" if not long_ones else " — UZUN: %s" % long_ones[:5]))
    rep.facts["instructionMaxWords"] = limit


def check_mission_line(acts, rep):
    print("\n── ⑤ görev satırı ──")
    bad = [a["activityId"] for a in acts
           if not MISSION_LINE.match((a.get("prompt") or "").strip())]
    rep.check(not bad, "her sayfa 'Your mission:' kalıbıyla açılıyor"
              + ("" if not bad else " — KALIP DIŞI: %s" % bad[:5]))


def check_step_unity(acts, rep):
    print("\n── ⑥ adım birliği ──")
    split = []
    for a in acts:
        for i, s in enumerate(a.get("steps") or [], 1):
            if SPLIT_HINT.search(s or ""):
                split.append("%s adım %d" % (a["activityId"], i))
    rep.check(not split, "hiçbir adım iki işi tek adıma sıkıştırmıyor"
              + ("" if not split else " — BİRLEŞİK: %s" % split[:5]))


def check_dangling(acts, rep):
    print("\n── ⑦ öncülsüz zamir ──")
    bad = []
    for a in acts:
        for i, s in enumerate(a.get("steps") or [], 1):
            if DANGLING.match((s or "").strip()):
                bad.append("%s adım %d" % (a["activityId"], i))
    rep.check(not bad, "hiçbir adım öncülsüz bir zamirle başlamıyor"
              + ("" if not bad else " — BELİRSİZ: %s" % bad[:5]))


def check_reference(acts, rep):
    """⑨ BELİRTİLİ GÖNDERME SAYFADA BASILI MI.

    ⭑ BU DENETİM BİR İÇ EDİTORYAL İNCELEMEDEN DOĞDU ⭑

    İnceleme 16 sayfayı sekiz yaşındaki bir çocuk gibi harfi harfine okudu
    ve şunu buldu: BÜTÜN mekanik kapılar 16/16 geçiyordu ama sayfaların
    çoğu yine de çözülemezdi.

        Kapılar cümlenin BİÇİMİNİ ölçüyordu.
        Kusurların hepsi cümlenin GÖNDERMESİNDEYDİ.

    Örnekler — hepsi bant içinde, hepsi çözülemez:

        "Colour them the way the key shows."     → sayfada anahtar YOK
        "Read the four cards beside the cord."   → sayfada ip YOK
        "Put each one in the right column."      → sütun başlıkları YOK
        "Write the words on the six lines."      → dört satır var
        "Write where the two of them went."      → cevaptaki ad basılı DEĞİL

    Bir talimat "the X" derse, çocuk sayfada bir X arar. Yoksa yanlış
    sayfada olduğunu düşünür ve bırakır.

    ÇÖZÜM: her sayfa `pagePrints` taşır — levhanın çözülebilirlik için
    BASMASI GEREKEN her şey. Kapı, adımlardaki belirtili adları o listede
    (ve sayfanın kendi metninde) arar.

    Bu alan aynı zamanda Faz 5'in görsel şartnamesidir: görsel, metnin
    ihtiyacından türer — tersi değil.
    """
    print("\n── ⑨ belirtili gönderme çözülüyor mu ──")

    # "the X" ve "your X" kalıplarındaki ad. Kapalı bir sözcük listesi
    # tutulmaz: sayfanın kendi sözcük dağarcığı ölçüt olur.
    #
    # ⚠ İKİ KEZ DÜZELTİLDİ ve iki kez `selftest` yakaladı.
    #
    #   "Copy the colours from the wall chart."
    #
    # ① İlk desen açgözlüydü: "colours from the" öbeğini yakalıyordu.
    # ② İkinci desen öbeği işlev sözcüğünde kesti ama eşleşme YİNE de
    #    ikinci `the`'yi YUTUYORDU — `finditer` bir sonraki aramaya onun
    #    ARDINDAN başlıyor ve "wall chart" hiç görülmüyordu.
    #
    # Yani denetim, tam da yakalaması gereken cümleyi iki farklı sebeple
    # kaçırıyordu. Desen bırakıldı: belirteçler tek tek bulunuyor ve öbek
    # ELLE okunuyor. Hiçbir şey yutulmuyor.
    # YALNIZCA BELİRTİLİ TANIMLIK. "your age" ve "your first name" çocuğun
    # KENDİ şeyleridir ve sayfada basılı olamazlar; "the key" ise sayfanın
    # bir şeyi olduğu SÖZÜNÜ verir. Denetim o sözü tutuyor mu diye bakar.
    DET = re.compile(r"\bthe\b")
    WORD = re.compile(r"[a-z']+")
    STOP = {"the", "your", "a", "an", "and", "or", "of", "from", "in", "on",
            "to", "into", "with", "for", "at", "by", "that", "this", "it",
            "each", "every", "its", "their", "so", "then", "as", "is", "are"}
    # Gönderme SAYILMAYANLAR: soyut ya da sayfadan bağımsız adlar.
    GENERIC = {
        "same", "right", "left", "last", "first", "most", "rest", "top",
        "bottom", "middle", "end", "way", "answer", "box", "star", "star box",
        "page", "book", "order", "number", "numbers", "word", "words", "name",
        "names", "letter", "letters", "total", "totals", "three totals",
        "two counts", "four", "six", "own", "own string", "seal", "seal slot",
        "time", "one", "ones", "other", "others", "pair", "same column",
        "empty basket", "next", "sign", "signs", "part", "parts", "thing",
    }

    missing = []
    for a in acts:
        # ⚠ ADIMLAR SAMANLIĞA GİRMEZ.
        #
        # İlk hâlde adımların kendisi de aranan metnin içindeydi ve bu,
        # denetimi TAMAMEN boşa çıkarıyordu: "the wall chart" diyen bir
        # adım, kendi cümlesinde "wall chart" geçtiği için çözülmüş
        # sayılıyordu. Kapı her şeyi geçiriyordu.
        #
        # Bir gönderme, kendi cümlesi DIŞINDA bir yerde karşılanmalıdır:
        # levhada basılı olan şeyde, field note'ta veya cevapta.
        prints = " ".join(a.get("pagePrints") or []).lower()
        shown = " ".join([a.get("fieldNote", ""),
                          a.get("answer", "") or "",
                          a.get("expectedResult", "") or "",
                          a.get("parentNote", "") or ""]).lower()
        haystack = prints + " " + shown
        if not (a.get("pagePrints") or []):
            missing.append("%s → pagePrints YOK" % a["activityId"])
            continue
        for s in (a.get("steps") or []):
            low = s.lower()
            for m in DET.finditer(low):
                # Belirtecin ARDINDAKİ ad öbeğini elle oku; en çok üç
                # sözcük, ilk işlev sözcüğünde dur.
                parts = []
                pos = m.end()
                for w in WORD.finditer(low, pos):
                    if w.start() > pos + 1:      # araya noktalama girdi
                        break
                    if w.group(0) in STOP or len(parts) == 3:
                        break
                    parts.append(w.group(0))
                    pos = w.end()
                if not parts:
                    continue
                phrase = " ".join(parts)
                # Öbeğin TAMAMI ya da HERHANGİ BİR sözcüğü karşılanıyorsa
                # gönderme çözülmüş sayılır. Gevşek olması bilinçli: amaç
                # imlâ denetlemek değil, SAYFADA OLMAYAN bir şeye yapılan
                # göndermeyi yakalamak. "wall chart" ikisiyle de düşer.
                # Çoğul toleransı: "the dots" bir levhadaki "dot = 1"
                # anahtarını karşılar. Bu bir imlâ denetimi değil.
                def seen(w: str) -> bool:
                    if w in GENERIC or w in haystack:
                        return True
                    if w.endswith("s") and w[:-1] in haystack:
                        return True
                    return (w + "s") in haystack

                if phrase in GENERIC or phrase in haystack:
                    continue
                if any(seen(w) for w in parts):
                    continue
                missing.append("%s → '%s' sayfada basılı değil"
                               % (a["activityId"], phrase))

    rep.check(not missing,
              "adımlardaki her belirtili gönderme sayfada basılı"
              + ("" if not missing else " — ÇÖZÜLMEYEN: %s" % missing[:6]))
    rep.facts["pagesWithPrintSpec"] = sum(1 for a in acts if a.get("pagePrints"))


def check_writing_space(acts, rep):
    print("\n── ⑧ yazma alanı ──")
    missing = []
    for a in acts:
        blob = " ".join([a.get("prompt", "")] + list(a.get("steps") or []))
        if WRITES.search(blob) and not a.get("writingSpaceLines"):
            missing.append(a["activityId"])
    rep.check(not missing,
              "yazdıran her sayfa yazacak yer bırakıyor"
              + ("" if not missing else " — ALANSIZ: %s" % missing[:5]))
    lines = [a.get("writingSpaceLines", 0) for a in acts]
    rep.facts["writingLinesTotal"] = sum(lines)
    rep.facts["writingLinesMax"] = max(lines) if lines else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    print("=" * 74)
    print("  TALİMAT NETLİĞİ")
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

    check_imperative(acts, rep)
    check_second_person(cfg, acts, rep)
    check_step_count(acts, rep)
    check_sentence_length(cfg, acts, rep)
    check_mission_line(acts, rep)
    check_step_unity(acts, rep)
    check_dangling(acts, rep)
    check_writing_space(acts, rep)
    check_reference(acts, rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · %d sayfa" % (rep.checks, len(acts)))
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
