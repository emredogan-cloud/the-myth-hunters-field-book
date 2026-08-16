#!/usr/bin/env python3
"""
TASARIM DİZGESİ VE GÖRSEL ŞARTNAMESİ KAPISI — The Myth Hunter's Field Book
================================================================================
Faz 2 bir bölgenin sayfa dilini kalibre etti. Faz 3 onu kitap geneline
çıkardı ve dondurdu: `00_CONTEXT/DESIGN_SYSTEM.md`.

Bu kapı o belgenin **uygulandığını** denetler — belgenin var olduğunu
değil. İkisi arasındaki fark, World Myths'in K18 dersidir:

    Bir kapının VARLIĞI yetmez, KOŞMASI gerekir.
    Bir belgenin VARLIĞI yetmez, DENETLENMESİ gerekir.

Yedi denetim:

  ① BÖLGE AÇILIŞI    — üç parça tam mı, mühür kuralı BASILI mı, bant tutuyor mu
  ② MÜHÜR MODÜLÜ     — yıldızlı kutu levhada tarif edilmiş mi, sözcük basılı mı
  ③ DÜZEN            — her sayfa kapalı listeden bir düzen taşıyor mu
  ④ DÜZEN × TİP      — düzen aktivite tipine izinli mi
  ⑤ GÖRSEL ŞARTNAMESİ — her sayfa tam bir `visualSpec` taşıyor mu
  ⑥ BÖLGE ÇEŞİTLİLİĞİ — bir bölge tek düzene çökmüş mü
  ⑦ VARLIK KİMLİĞİ   — assetId tekil mi, dosya adı ve hedef sözleşmeye uyuyor mu
  ⑧ EŞLEŞTİRME       — eşleştirmenin İKİ TARAFI da basılı mı  ⭑FAZ 3⭑
  ⑨ MOBİLYA ÇİFTLEMESİ — levha ve dizgi AYNI kutuyu iki kez mi basıyor ⭑YÜKLEME ÖNCESİ⭑

⑥ NEDEN VAR — VE BU KAPININ EN ÖZGÜN DENETİMİDİR:

`qa_matrix` her bölgede beş TİPİN dağılımını denetliyor. Ama tip ile
DÜZEN aynı şey değildir. Bir bölgenin yirmi sayfası da `sort` tipinden
başka bir şey olmayabilir *ve* `qa_matrix` yine de kırmızı yanmayabilir
— çünkü tip asgarileri tipe bakar. Daha kötüsü: beş tipin hepsi dolu
olduğu hâlde bütün sayfalar aynı LEVHA BİÇİMİNİ kullanabilir.

    Altı bölge farklı içerik taşıyıp aynı ŞABLON gibi okunabilir.

Kurucu talimatı § 15 bunu yasaklıyor: *structure consistency without
cultural homogeneity.* Bu denetim her yazılmış bölgede en az üç ayrı
düzen arar.

⑤ NEDEN VAR: karar K25 *"görsel metnin ihtiyacından türer"* diyor ve
Faz 2 `pagePrints`i doğurdu. Faz 3 zinciri kapatıyor: her sayfa,
levhasından TÜREYEN bir görsel şartnamesi taşır.

⚠ ŞARTNAME BİR VARLIK DEĞİLDİR. Bu kapı hiçbir görselin ÜRETİLDİĞİNİ
iddia etmez ve `status: specified-not-produced` alanını ayrıca sayar.
Üretim Faz 5'e aittir.

⚠ MANUSCRIPT DEPODA DEĞİLDİR. Dosya yoksa kapı BOŞ KOŞAR; körlüğü
`05_TESTS/selftest.py § ⑯` kapatır.

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

CONFIG = os.path.join(ROOT, "project_config.json")
ACTIVITY_INDEX = os.path.join(ROOT, "01_SOURCE", "activity_index.json")
BOOK = os.path.join(ROOT, "02_MANUSCRIPT", "book.json")

# ① Bölge açılışı mühür kuralını BASMAK ZORUNDADIR. Faz 2'nin 1 numaralı
#    bloklayıcısı tam olarak buydu: kural `$comment` alanında duruyordu ve
#    çocuk onu HİÇ öğrenmiyordu.
SEAL_RULE_TOKENS = ("star box", "seal slot", "letter")

# ② Yıldızlı kutunun levhada nasıl tarif edildiği de sabittir.
STAR_BOX_RE = re.compile(r"star box.*letter squares.*square\s+(\d+)\s+outlined.*"
                         r"seal slot\s+(\d+)", re.IGNORECASE)

VISUAL_FIELDS = ("assetId", "visualClass", "layout", "purpose", "subject",
                 "requiredLabels", "orientation", "targetPx", "aspect",
                 "safeAreaMm", "restrictions", "format", "filename",
                 "destination", "status")

# Etiketsiz olması MEŞRU olan düzenler. Bir make çerçevesinin basacak
# etiketi yoktur; bir kart dizisi cümle basar, etiket değil. Ve bir
# karşılaştırma levhası özneleri ADLANDIRAMAZ — adlandırırsa cevabı verir.
LABEL_EXEMPT_LAYOUTS = {"make-frame", "sort-cards", "plate-compare"}


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


def check_openings(book, cfg, rep):
    print("\n── ① bölge açılışı ──")
    lo, hi = cfg.get("openingWordsMin", 120), cfg.get("openingWordsMax", 170)
    ops = book.get("regionOpenings")
    if ops is None:
        legacy = book.get("regionOpening")
        ops = [legacy] if legacy else []
    rep.facts["regionOpenings"] = len(ops)
    rep.check(bool(ops), "manuscript en az bir bölge açılışı taşıyor")

    missing_part, no_rule, off_band = [], [], []
    for o in ops:
        rid = (o or {}).get("regionId", "?")
        for f in ("regionId", "heading", "terrainLine", "openingText"):
            if not (o or {}).get(f):
                missing_part.append("%s → %s" % (rid, f))
        text = (o or {}).get("openingText", "")
        low = text.lower()
        absent = [t for t in SEAL_RULE_TOKENS if t not in low]
        if absent:
            no_rule.append("%s → %s" % (rid, absent))
        n = len(re.findall(r"[A-Za-z'ʻ’-]+", text))
        if text and not (lo <= n <= hi):
            off_band.append("%s (%d kelime)" % (rid, n))
    rep.check(not missing_part, "her açılış üç parçasını da taşıyor"
              + ("" if not missing_part else " — EKSİK: %s" % missing_part))
    rep.check(not no_rule,
              "mühür kuralı her bölge açılışında BASILI"
              + ("" if not no_rule else " — BASILMAMIŞ: %s" % no_rule))
    rep.check(not off_band, "açılış metinleri %d–%d kelime bandında" % (lo, hi)
              + ("" if not off_band else " — BANT DIŞI: %s" % off_band))


def check_seal_module(acts, rep):
    print("\n── ② mühür modülü ──")
    sealed = [a for a in acts if a.get("sealSlot")]
    rep.facts["sealedPages"] = len(sealed)
    if not sealed:
        print("  ⊘ mühür taşıyan sayfa yok")
        rep.check(True, "mühür modülü denetlenecek sayfa yok")
        return
    no_box, wrong_slot, word_unprinted = [], [], []
    for a in sealed:
        prints = " ".join(a.get("pagePrints") or [])
        m = STAR_BOX_RE.search(prints)
        if not m:
            no_box.append(a["activityId"])
            continue
        square, slot = int(m.group(1)), int(m.group(2))
        if slot != a["sealSlot"] or square != a.get("sealStarIndex"):
            wrong_slot.append("%s levha=(kare %d, yuva %d) kayıt=(kare %s, yuva %s)"
                              % (a["activityId"], square, slot,
                                 a.get("sealStarIndex"), a["sealSlot"]))
        # Yıldızlı sözcük LEVHADA basılı olmalı. qa_solvable § ⑦ onu
        # CEVAPTA arar; cevap depoda durmayan bir katmandır ve levha
        # ayrı bir kanıttır: çocuğun kopyalayacağı şey basılmalıdır.
        word = (a.get("sealStarWord") or "").lower()
        if word and word not in prints.lower():
            word_unprinted.append("%s → '%s'" % (a["activityId"], word))
    rep.check(not no_box, "her mühür sayfası levhasında yıldızlı kutuyu tarif ediyor"
              + ("" if not no_box else " — KUTUSUZ: %s" % no_box))
    rep.check(not wrong_slot, "levhadaki kare ve yuva numaraları kayıtla aynı"
              + ("" if not wrong_slot else " — ÇELİŞKİ: %s" % wrong_slot))
    rep.check(not word_unprinted,
              "yıldızlı sözcük levhada BASILI"
              + ("" if not word_unprinted else " — BASILMAMIŞ: %s" % word_unprinted))


def check_layouts(acts, cfg, rep):
    print("\n── ③ düzen · ④ düzen × tip ──")
    allowed = cfg.get("layouts", {})
    known = set(allowed)
    missing = [a["activityId"] for a in acts if not a.get("layout")]
    rep.check(not missing, "her sayfa bir düzen taşıyor"
              + ("" if not missing else " — DÜZENSİZ: %s" % missing[:6]))
    unknown = ["%s (%s)" % (a["activityId"], a.get("layout"))
               for a in acts if a.get("layout") and a["layout"] not in known]
    rep.check(not unknown, "her düzen kapalı listede"
              + ("" if not unknown else " — TANIMSIZ: %s" % unknown[:6]))
    bad = ["%s: %s düzeni %s tipine izinli değil"
           % (a["activityId"], a.get("layout"), a.get("type"))
           for a in acts
           if a.get("layout") in known and a.get("type")
           and a.get("type") not in allowed[a["layout"]]]
    rep.check(not bad, "her düzen kendi aktivite tipinde"
              + ("" if not bad else " — İHLAL: %s" % bad[:6]))
    rep.facts["layoutUse"] = dict(collections.Counter(
        a.get("layout") for a in acts if a.get("layout")))


def check_visual_specs(acts, rep):
    print("\n── ⑤ görsel şartnamesi ──")
    missing, incomplete, thin, unlabelled = [], [], [], []
    produced = 0
    for a in acts:
        vs = a.get("visualSpec")
        if not vs:
            missing.append(a["activityId"])
            continue
        gaps = [f for f in VISUAL_FIELDS if not vs.get(f) and vs.get(f) != 0]
        # requiredLabels bilerek boş olabilir; ayrı denetleniyor.
        gaps = [g for g in gaps if g != "requiredLabels"]
        if gaps:
            incomplete.append("%s → %s" % (a["activityId"], gaps))
        if len(vs.get("restrictions") or []) < 2:
            thin.append(a["activityId"])
        if (not vs.get("requiredLabels")) and a.get("layout") not in LABEL_EXEMPT_LAYOUTS:
            unlabelled.append("%s (%s)" % (a["activityId"], a.get("layout")))
        if vs.get("status") == "produced":
            produced += 1
    rep.check(not missing, "her sayfa bir görsel şartnamesi taşıyor"
              + ("" if not missing else " — ŞARTNAMESİZ: %s" % missing[:6]))
    rep.check(not incomplete, "her şartname bütün alanlarını taşıyor"
              + ("" if not incomplete else " — EKSİK: %s" % incomplete[:4]))
    rep.check(not thin, "her şartname en az iki kısıt taşıyor"
              + ("" if not thin else " — KISITSIZ: %s" % thin[:6]))
    rep.check(not unlabelled,
              "etiket gerektiren her düzen basılacak etiketleri sayıyor"
              + ("" if not unlabelled else " — ETİKETSİZ: %s" % unlabelled[:6]))
    rep.facts["visualSpecs"] = sum(1 for a in acts if a.get("visualSpec"))
    rep.facts["visualAssetsProduced"] = produced
    rep.facts["requiredLabelsTotal"] = sum(
        len((a.get("visualSpec") or {}).get("requiredLabels") or []) for a in acts)
    # ⚠ Şartname bir varlık değildir ve bu satır onu her koşuda söyler.
    print("  · %d şartname · %d ÜRETİLMİŞ varlık (üretim Faz 5'e ait)"
          % (rep.facts["visualSpecs"], produced))


def check_region_variety(acts, cfg, rep):
    print("\n── ⑥ bölge içi düzen çeşitliliği ──")
    need = cfg.get("minLayoutsPerRegion", 3)
    by_region = collections.defaultdict(set)
    counts = collections.Counter()
    for a in acts:
        if a.get("region") and a.get("layout"):
            by_region[a["region"]].add(a["layout"])
            counts[a["region"]] += 1
    thin = ["%s: %d düzen (%d sayfa)" % (r, len(l), counts[r])
            for r, l in sorted(by_region.items()) if len(l) < need]
    rep.facts["layoutsPerRegion"] = {r: len(l) for r, l in by_region.items()}
    for r, l in sorted(by_region.items()):
        print("  · %-14s %d sayfa · %d ayrı düzen" % (r, counts[r], len(l)))
    rep.check(not thin,
              "her yazılmış bölge en az %d ayrı düzen kullanıyor" % need
              + ("" if not thin else " — ŞABLONLAŞMA: %s" % thin))


def check_asset_identity(acts, cfg, rep):
    print("\n── ⑦ varlık kimliği ──")
    dest = cfg.get("assetDestination", "07_ASSETS/processed/interior/")
    ids = [(a.get("visualSpec") or {}).get("assetId")
           for a in acts if a.get("visualSpec")]
    dup = [k for k, v in collections.Counter(ids).items() if v > 1]
    rep.check(not dup, "assetId değerleri tekil"
              + ("" if not dup else " — YİNELENEN: %s" % dup[:5]))
    bad_name, bad_dest = [], []
    for a in acts:
        vs = a.get("visualSpec") or {}
        if not vs:
            continue
        want = "%s.%s" % (vs.get("assetId"), vs.get("format"))
        if vs.get("filename") != want:
            bad_name.append("%s → %s (beklenen %s)"
                            % (a["activityId"], vs.get("filename"), want))
        if vs.get("destination") != dest:
            bad_dest.append("%s → %s" % (a["activityId"], vs.get("destination")))
    rep.check(not bad_name, "dosya adı assetId ile aynı"
              + ("" if not bad_name else " — SÖZLEŞME DIŞI: %s" % bad_name[:4]))
    rep.check(not bad_dest, "her varlık aynı hedefe yazılacak (%s)" % dest
              + ("" if not bad_dest else " — HEDEF DIŞI: %s" % bad_dest[:4]))


MATCH_STEP = re.compile(
    r"\b(?:draw a line from|match|join)\b", re.IGNORECASE)

# Cevap alanlarındaki DEFTER TUTMA sözcükleri. Bunlar cevabın kendisi
# değil, cevabı YAZMA biçimidir ve levhada basılı olmaları beklenmez.
BOOKKEEPING = {
    "marked", "traced", "drawn", "written", "circled", "shaded", "numbered",
    "star", "box", "boxes", "card", "cards", "line", "lines", "name", "names",
    "word", "words", "label", "labels", "column", "row", "rows", "side",
    "sides", "first", "last", "order", "page", "into", "from", "with", "each",
    "their", "there", "here", "cent", "per", "degrees", "latitude", "about",
    "river", "rivers", "city", "cities", "country", "countries", "source",
    "sources", "band", "bands", "sign", "signs", "part", "parts", "only",
    "both", "under", "over", "point", "points", "place", "places",
}
TOKEN = re.compile(r"[A-Za-zʻ'\u00c0-\u024f\u1e00-\u1eff]+")


def _sig(text: str) -> list[str]:
    return [w for w in TOKEN.findall((text or "").lower())
            if len(w) > 3 and w not in BOOKKEEPING]


def check_matching_relation(acts, rep):
    """⑧ BİR EŞLEŞTİRMENİN İKİ TARAFI DA BASILI MI.

    ⭑ BU DENETİM BİR İÇ İNCELEMEDEN DOĞDU VE ON BİR SAYFA BULDU ⭑

    `qa_instruction § ⑨` bir adımın işaret ettiği ADI çözüyor: "the key"
    diyen bir adım için levhada bir anahtar var mı. Ama bir EŞLEŞTİRME
    görevinde ad yetmez — İLİŞKİ gerekir:

        levha: beş renk kartı        ✓ basılı
        levha: beş yön kartı         ✓ basılı
        hangisi hangisiyle gider     ✗ HİÇBİR YERDE

    Üç kapı da yeşil yanıyordu ve sayfa çözülemezdi.

    ⚠ BU KAPI İKİYE AYRILDI VE BÖLÜNME BİLİNÇLİDİR.

    İlk hâli tek bir sert denetimdi: "her cevap alanı TEK bir levha
    maddesinde birlikte geçmeli." O hâl üç sayfayı yakaladı ve biri
    YANLIŞ POZİTİFTİ — bir haritada şehirleri işaretlemek bir eşleştirme
    değildir, ve bazı meşru tasarımlarda ilişki bir TABLODA değil bir
    ÇIKARIMDA durur (iki sayı karşılaştırılır).

        Mekanik olarak karara bağlanabilen şey ile
        bir insanın bakması gereken şey aynı kapıda duramaz.

    Bu yüzden:

      SERT  → eşleştirmenin İKİ TARAFI da sayfada basılı mı
              (basılmayan bir şey eşleştirilemez — bu karara bağlanabilir)
      UYARI → iki taraf AYNI maddede mi duruyor
              (durmuyorsa ilişki bir çıkarım olabilir — insan bakar)
    """
    print("\n── ⑧ eşleştirme ilişkisi ──")
    unprinted, uncolocated = [], []
    checked = 0
    for a in acts:
        if a.get("layout") in ("sort-cards", "make-frame"):
            continue
        steps = a.get("steps") or []
        if not any(MATCH_STEP.search(s or "") for s in steps):
            continue
        checked += 1
        prints = a.get("pagePrints") or []
        # Field note da BASILIDIR ve bir anahtar taşıyabilir.
        haystack = [p.lower() for p in prints] + [(a.get("fieldNote") or "").lower()]
        blob = " ".join(haystack)
        for f in [x.strip() for x in re.split(r"\s·\s", a.get("answer") or "") if x.strip()]:
            toks = _sig(f)
            if len(set(toks)) < 2:
                continue
            missing = [t for t in set(toks) if t not in blob]
            if missing:
                unprinted.append("%s → '%s' basılı değil" % (a["activityId"], missing[0]))
                continue
            if not any(all(t in item for t in set(toks)) for item in haystack):
                uncolocated.append("%s → '%s…'" % (a["activityId"], f[:34]))
    rep.facts["matchingPagesChecked"] = checked
    rep.check(not unprinted,
              "eşleştirmenin her iki tarafı da sayfada basılı (%d sayfa)" % checked
              + ("" if not unprinted else " — BASILI DEĞİL: %s" % unprinted[:6]))
    if uncolocated:
        rep.warn("ilişki tek bir maddede durmuyor — bir ÇIKARIM tasarımı olabilir, "
                 "insan bakmalı: %s" % uncolocated[:6])
    rep.facts["uncolocatedPairs"] = len(uncolocated)


WRITING_LINE_RE = re.compile(
    r"\b([a-z]+|\d+)\s+(?:empty\s+|ruled\s+|blank\s+)*writing\s+lines?\b", re.I)
# ⚠ § ②'nin STAR_BOX_RE'si ile AYNI AD KULLANILMAZ: o kalıp kare ve yuva
# numarasını YAKALAR, bu kalıp yalnızca kutunun levhada ANILDIĞINI arar.
# İki ayrı soru, iki ayrı ad — aynı ada iki kalıp koymak § ②'yi sessizce
# bozar ve ilk koşuda bozdu.
PLATE_STAR_BOX_RE = re.compile(r"\bstar box\b", re.I)
NUMWORD = {"no": 0, "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
           "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
           "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
           "a": 1, "an": 1}


def check_furniture_duplication(acts, rep):
    """⑨ SAYFA MOBİLYASI İKİ KEZ BASILIYOR MU — ⭑ YÜKLEME ÖNCESİ GEÇİŞ ⭑

    ⭑ BU DENETİMİN VAR OLMA SEBEBİ ⭑

    `pagePrints` iki AYRI muhatabı olan tek bir liste:

        LEVHANIN çizeceği   anahtar paneli · kart · harita · nesne
        DİZGİNİN çizeceği   yazma satırı · yıldızlı kutu · numara kutusu

    Ayrım hiçbir yerde YAZILI DEĞİL. Faz 6 promptu doldururken listenin
    TAMAMINI üretece verdi; üreteç sayfa mobilyasını da sanatın içine
    çizdi. `interior.py` ise aynı mobilyayı kendi işi saymaya devam etti.

    Sonuç ölçüldü: **37 mühür sayfasının 37'sinde yıldızlı kutu iki kez**,
    **120 sayfanın 75'inde yazma alanı iki kez** basılıyor.

        Doğru bir sayı, iki kez basılınca doğru kalmıyor.

    Faz 5 `A1` yıldızlı kutunun BASILI SAYISINI düzeltmişti. Kimse
    kutunun KAÇ KEZ basıldığını sormamıştı — `qa_design § ②` kutunun
    VAR olduğunu doğruluyor, İKİ TANE olmadığını değil.

    ⚠ NEDEN UYARI, NEDEN HATA DEĞİL — VE BU GEÇİCİDİR

    Kusur 99 sayfada BUGÜN var. Denetimi hata olarak açmak, düzeltme
    kararı verilmeden CI'ı kırmızıya kilitlemek olurdu — ve bu kapıyı
    gevşetme baskısı yaratır. Ölçüm kayda giriyor, sayı raporda duruyor
    ve kusur GÖRÜNÜR hâle geliyor.

        Aşama 2 `pagePrints` maddelerine rol ekleyince
        (`plate` / `typeset`) bu denetim HATAYA yükseltilir.

    Ölçüm hiçbir koşulda gizlenmez: sıfırsa da yazılır.
    """
    dup_star, dup_write, clean = [], [], 0
    for a in acts:
        prints = a.get("pagePrints") or []
        blob = " | ".join(prints)
        plate_star = bool(PLATE_STAR_BOX_RE.search(blob))
        typeset_star = bool(a.get("sealSlot"))
        plate_lines = 0
        for m in WRITING_LINE_RE.finditer(blob):
            w = m.group(1).lower()
            plate_lines += int(w) if w.isdigit() else NUMWORD.get(w, 1)
        typeset_lines = int(a.get("writingSpaceLines") or 0)
        if plate_star and typeset_star:
            dup_star.append(a["activityId"])
        if plate_lines and typeset_lines:
            dup_write.append("%s (levha %d ⇄ dizgi %d)"
                             % (a["activityId"], plate_lines, typeset_lines))
        if not (plate_star and typeset_star) and not (plate_lines and typeset_lines):
            clean += 1

    rep.facts["furnitureDuplicateStarBox"] = len(dup_star)
    rep.facts["furnitureDuplicateWritingBlock"] = len(dup_write)
    rep.facts["furnitureClean"] = clean

    print("\n── ⑨ sayfa mobilyası rol ayrımı ──")
    print("  levha yıldızlı kutu basıyor : %3d / %d sayfa"
          % (len(dup_star), len(acts)))
    print("  levha yazma satırı basıyor  : %3d / %d sayfa"
          % (len(dup_write), len(acts)))

    # ⭑ ARTIK BİR UYARI DEĞİL, BİR KAPI ⭑
    #
    # Aşama 1'de bu bölüm yalnızca ÖLÇÜYORDU: kusur 99 sayfada vardı ve
    # denetimi hata olarak açmak, düzeltme kararı verilmeden CI'ı
    # kırmızıya kilitlemek olurdu. Aşama 2'de kök düzeltme uygulandı
    # (`04_BUILD/furniture_roles.py` → `book.json § furniture` →
    # `interior.py`), bu yüzden ölçüm artık BAĞLAYICI.
    #
    # Denetlenen şey çiftlemenin YOKLUĞU değil, ROLÜN BEYAN EDİLMİŞ
    # olmasıdır: her sayfa, mobilyasını kimin bastığını SÖYLEMEK
    # zorundadır. Beyan yoksa dizgi eski davranışa döner ve çiftleme
    # sessizce geri gelir.
    undeclared, mismatched = [], []
    for a in acts:
        f = a.get("furniture")
        if not f:
            undeclared.append(a["activityId"])
            continue
        prints = " | ".join(a.get("pagePrints") or [])
        plate_star = bool(PLATE_STAR_BOX_RE.search(prints))
        want_star = ("plate" if plate_star
                     else ("typeset" if a.get("sealSlot") else "none"))
        pl = 0
        for m in WRITING_LINE_RE.finditer(prints):
            wd = m.group(1).lower()
            pl += int(wd) if wd.isdigit() else NUMWORD.get(wd, 1)
        want_lines = ("plate" if pl
                      else ("typeset" if (a.get("writingSpaceLines") or 0)
                            else "none"))
        if f.get("starBox") != want_star or f.get("writingLines") != want_lines:
            mismatched.append(a["activityId"])

    rep.check(not undeclared,
              "her sayfa mobilya rolünü BEYAN ediyor (%d/%d)"
              % (len(acts) - len(undeclared), len(acts))
              + ("" if not undeclared else " — BEYANSIZ: %s" % undeclared[:5]))
    rep.check(not mismatched,
              "beyan edilen rol ÖLÇÜMLE aynı"
              + ("" if not mismatched else " — UYUŞMAZ: %s" % mismatched[:5]))
    print("  beyanı ölçümle tutan        : %3d / %d sayfa"
          % (len(acts) - len(undeclared) - len(mismatched), len(acts)))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    print("=" * 74)
    print("  TASARIM DİZGESİ VE GÖRSEL ŞARTNAMESİ")
    print("=" * 74)

    rep = Report(args.verbose)
    conf = load(CONFIG, rep)
    if conf is None:
        return 1
    cfg = conf.get("design", {})
    if not cfg:
        rep.check(False, "project_config.json § design bloğu yok")
        print("=" * 74)
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

    check_openings(book_doc, cfg, rep)
    check_seal_module(acts, rep)
    check_layouts(acts, cfg, rep)
    check_visual_specs(acts, rep)
    check_region_variety(acts, cfg, rep)
    check_asset_identity(acts, cfg, rep)
    check_matching_relation(acts, rep)
    check_furniture_duplication(acts, rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · %d şartname · %d etiket · 0 üretilmiş varlık"
              % (rep.checks, rep.facts.get("visualSpecs", 0),
                 rep.facts.get("requiredLabelsTotal", 0)))
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
