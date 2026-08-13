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
