#!/usr/bin/env python3
"""
VARLIK ENVANTERİ ÜRETECİ — The Myth Hunter's Field Book
================================================================================
`07_ASSETS/ASSET_MANIFEST.json` **elle yazılmaz**. Manuscript'ten,
kültür dizininden ve bölge dizininden **TÜRETİLİR** (karar K17 ile aynı
gerekçe, bir kat aşağıda).

    Elle yazılmış bir varlık listesi, bir sayfa değiştiği gün sessizce
    yalan söylemeye başlar — ve görsel hattı yanlış aktiviteye bağlanmış
    kusursuz bir görsel üretir. Faz 5'in en pahalı hatası budur.

⭑ "YAKLAŞIK 150" BİR TAHMİNDİR, BİR ENVANTER DEĞİL ⭑

Yol haritası *"~150 görsel öğe"* diyor ve kurucu talimatı § 10 bunu açıkça
uyarıyor: *"Do NOT blindly assume exactly 150 files. Calculate the actual
final asset inventory."*

Envanter DÖRT kaynaktan türetilir ve toplam **hesaplanır**:

    ① aktivite görselleri     book.json § activities[].visualSpec
    ② kültür vinyetleri       culture_index.json § cultures[]
    ③ mühür / rozet varlığı   region_index.json § sealStampMotif
    ④ ön madde görselleri     book.json § frontMatter § visualNeed

Sayı ne çıkarsa odur. 150'ye YUVARLANMAZ.

⭑ DÖRT KATMANLI DOSYA YOLU (karar K35) ⭑

    raw/        KURUCUNUN çıktısı · DEĞİŞMEZ · asla üzerine yazılmaz
    processed/  CLI ÜRETİR · her zaman RAW'dan YENİDEN üretilebilir
    final/      basıma hazır · processed'dan türer
    rejected/   şartnameyi ihlal eden RAW · SİLİNMEZ, ayrılır

Manifest her varlık için dördünün de yolunu taşır — dosya var olmasa bile.
**Bir yol bir varlık değildir**: `status` alanı ikisini ayırır ve
`BOOK_STATS` şartname ile varlığı iki AYRI satırda sayar.

  ./04_BUILD/asset_manifest.py            envanteri tazele
  ./04_BUILD/asset_manifest.py --check    bayatsa KIRMIZI

TASARIM: yalnızca Python standart kütüphanesi (karar K7).

Çıkış kodları:  0 = güncel/yazıldı   1 = BAYAT   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

BOOK = os.path.join(ROOT, "02_MANUSCRIPT", "book.json")
ACTS = os.path.join(ROOT, "01_SOURCE", "activity_index.json")
CULTURES = os.path.join(ROOT, "01_SOURCE", "culture_index.json")
REGIONS = os.path.join(ROOT, "01_SOURCE", "region_index.json")
CONFIG = os.path.join(ROOT, "project_config.json")
OUT = os.path.join(ROOT, "07_ASSETS", "ASSET_MANIFEST.json")
OUT_LOCAL = os.path.join(ROOT, "07_ASSETS", "ASSET_MANIFEST.local.json")

# ⭑ ENVANTER İKİ KATMANDIR — VE BU BİR KOLAYLIK DEĞİL BİR KİLİTTİR ⭑
#
# İlk hâl TEK bir dosya yazıyordu ve o dosya takip ediliyordu. İçinde
# `requiredLabels` ve `restrictions` vardı — ve Faz 5'te eklenen ölçüm
# kısıtları cevabın KENDİSİNİ taşıyor:
#
#     "Exactly these knot counts must be countable: cord A three in the
#      tens and four in the ones; cord B two and one; ..."
#
# Bu bir görsel şartnamesidir VE AYNI ZAMANDA CEVAPTIR. Public depoda
# duran bir cevap ürünü değersizleştirir (K10) — ve `image_prompts.py`
# tam olarak bu gerekçeyle Faz 2'den beri şartname metnini kütüphaneye
# ALMIYORDU. Envanter o kuralı yeniden keşfetmek yerine ona UYAR:
#
#     TAKİP EDİLEN  → kimlik · sınıf · ölçü · yol · sayım · sha256
#     TAKİP EDİLMEYEN → requiredLabels · restrictions · purpose
#
# Public dosya içeriği taşımaz ama SAĞLAMASINI taşır: özel kayıt
# sürüklenirse sağlama değişir ve denetlenebilir kalır.
PRIVATE_FIELDS = ("requiredLabels", "restrictions", "purpose", "sourceSpec")

RAW = "07_ASSETS/raw/"
PROCESSED = "07_ASSETS/processed/interior/"
FINAL = "07_ASSETS/final/interior/"
REJECTED = "07_ASSETS/rejected/"

# Vinyet ve rozet ölçüleri: iç blok 8,5×11 inç · 300 dpi.
# Vinyet bir bölüm başı süsü değil, kültürün BAĞLAM sanatıdır (§ 18) ve
# sayfanın üçte birinden küçüktür.
VIGNETTE_PX = [1350, 900]
VIGNETTE_ASPECT = "3:2"
SEAL_PX = [900, 900]
SEAL_ASPECT = "1:1"
BADGE_PX = [600, 600]
BADGE_ASPECT = "1:1"
FRONT_PX = [1950, 2550]
FRONT_ASPECT = "13:17"

SAFE_AREA = {"bleed": 3.2, "gutter": 9.5, "outer": 12.7}

BASE_RESTRICTIONS = [
    "No answer may be visible anywhere in the image.",
    "No decorative text: print only the labels listed in requiredLabels.",
    "No photographic or realistic human faces; line drawing only.",
]


def jload(path, default=None):
    if not os.path.isfile(path):
        return default
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def entry(**kw):
    """Manifest kaydı — alan SIRASI sabittir ki diff okunabilir kalsın."""
    e = collections.OrderedDict()
    for k in ("assetId", "assetClass", "activityId", "region", "culture",
              "visualClass", "purpose", "sourceSpec", "requiredLabels",
              "orientation", "aspectRatio", "targetDimensions", "safeArea",
              "minDpi", "format", "colour", "filename",
              "rawLocation", "processedLocation", "finalLocation",
              "rejectedLocation", "promptRef", "restrictions", "status"):
        e[k] = kw.get(k)
    return e


def build() -> dict:
    book = jload(BOOK, {}) or {}
    acts_doc = jload(ACTS, {"activities": []}) or {"activities": []}
    design = {a["activityId"]: a for a in acts_doc.get("activities", [])}
    cultures = (jload(CULTURES, {}) or {}).get("cultures", [])
    regions = (jload(REGIONS, {}) or {}).get("regions", [])
    rorder = {r["id"]: r.get("order", 99) for r in regions}

    assets = []

    # ── ① AKTİVİTE GÖRSELLERİ ──────────────────────────────────────────────
    # Şartname manuscript'te durur; manifest ona İŞARET EDER, kopyalamaz.
    # requiredLabels tek istisnadır: doğrulama hattı onu dosya adı kadar
    # sık okur ve iki dosya arasında gidip gelmek hatayı davet eder.
    for a in book.get("activities", []):
        vs = a.get("visualSpec")
        if not vs:
            continue
        d = design.get(a["activityId"], {})
        assets.append(entry(
            assetId=vs["assetId"],
            assetClass="activity",
            activityId=a["activityId"],
            region=d.get("region"),
            culture=d.get("culture"),
            visualClass=vs.get("visualClass"),
            purpose=vs.get("purpose"),
            sourceSpec="02_MANUSCRIPT/book.json#activities.%s.visualSpec"
                       % a["activityId"],
            requiredLabels=list(vs.get("requiredLabels") or []),
            orientation=vs.get("orientation"),
            aspectRatio=vs.get("aspect"),
            targetDimensions=list(vs.get("targetPx") or []),
            safeArea=vs.get("safeAreaMm"),
            minDpi=vs.get("minDpi"),
            format=vs.get("format"),
            colour=vs.get("colour"),
            filename=vs.get("filename"),
            rawLocation=RAW + vs["filename"],
            processedLocation=PROCESSED + vs["filename"],
            finalLocation=FINAL + vs["filename"],
            rejectedLocation=REJECTED + vs["filename"],
            promptRef=vs.get("promptDependency"),
            restrictions=list(vs.get("restrictions") or []),
            status=vs.get("status", "specified-not-produced"),
        ))

    # ── ② KÜLTÜR VİNYETLERİ ────────────────────────────────────────────────
    # Yol haritası 22 vinyet istiyor: her kültüre BİR tane, kendi adıyla.
    #
    # ⚠ VİNYET CEVAP DEĞİLDİR (kurucu talimatı § 18). Bu yüzden vinyetin
    # requiredLabels'ı TEK bir öğe taşır — kültürün kendi adı — ve
    # başka hiçbir şey basmaz. Bir vinyete etiket eklemek onu sessizce
    # bir aktivite levhasına çevirir.
    for c in sorted(cultures, key=lambda x: (rorder.get(x.get("region"), 99),
                                             x["id"])):
        aid = "vig-%s" % c["id"]
        fn = aid + ".png"
        restr = list(BASE_RESTRICTIONS)
        restr.append("This is CONTEXT art, not a puzzle: it must not carry any "
                     "part of any answer.")
        restr.append("Do not merge this culture's visual language with any "
                     "other culture in the book.")
        if c.get("livingTradition"):
            restr.append("This is a living tradition: depict it as present, "
                         "not as a ruin or a museum case.")
        for f in c.get("forbiddenForms") or []:
            restr.append("culture_index § %s yasak biçim: %s" % (c["id"], f))
        assets.append(entry(
            assetId=aid,
            assetClass="culture-vignette",
            activityId=None,
            region=c.get("region"),
            culture=c["id"],
            visualClass="culture-vignette",
            purpose="Give %s a page presence of its own in the glossary and at "
                    "its first appearance, so the culture is more than a puzzle."
                    % c.get("name", c["id"]),
            sourceSpec="01_SOURCE/culture_index.json#cultures.%s" % c["id"],
            requiredLabels=[c.get("name", c["id"])],
            orientation="landscape",
            aspectRatio=VIGNETTE_ASPECT,
            targetDimensions=list(VIGNETTE_PX),
            safeArea=dict(SAFE_AREA),
            minDpi=300,
            format="png",
            colour="grayscale",
            filename=fn,
            rawLocation=RAW + fn,
            processedLocation=PROCESSED + fn,
            finalLocation=FINAL + fn,
            rejectedLocation=REJECTED + fn,
            promptRef="07_ASSETS/IMAGE_PROMPT_LIBRARY.html#" + aid,
            restrictions=restr,
            status="specified-not-produced",
        ))

    # ── ③ MÜHÜR DAMGALARI ──────────────────────────────────────────────────
    # Her bölge bir damga motifi taşır ve motif `region_index`te ZATEN
    # tanımlıdır — burada icat edilmez.
    #
    # ⚠ DAMGA MÜHÜR SÖZCÜĞÜNÜ TAŞIMAZ (kurucu talimatı § 19). Damga bir
    # KİMLİKTİR: bölge, rota, motif. Sözcük çocuğun kendi yazdığı şeydir ve
    # basılı hiçbir yerde durmaz. `requiredLabels` bu yüzden BOŞTUR.
    for r in sorted(regions, key=lambda x: x.get("order", 99)):
        aid = "seal-%s" % r["id"]
        fn = aid + ".png"
        assets.append(entry(
            assetId=aid,
            assetClass="seal-stamp",
            activityId=None,
            region=r["id"],
            culture=None,
            visualClass="seal-stamp",
            purpose="Mark the end of %s with its own stamp outline, so the "
                    "reader can see which region a filled seal belongs to."
                    % r.get("en", r["id"]),
            sourceSpec="01_SOURCE/region_index.json#regions.%s.sealStampMotif"
                       % r["id"],
            requiredLabels=[],
            orientation="square",
            aspectRatio=SEAL_ASPECT,
            targetDimensions=list(SEAL_PX),
            safeArea=dict(SAFE_AREA),
            minDpi=300,
            format="png",
            colour="grayscale",
            filename=fn,
            rawLocation=RAW + fn,
            processedLocation=PROCESSED + fn,
            finalLocation=FINAL + fn,
            rejectedLocation=REJECTED + fn,
            promptRef="07_ASSETS/IMAGE_PROMPT_LIBRARY.html#" + aid,
            restrictions=BASE_RESTRICTIONS + [
                "⭑ The stamp must carry NO letters and NO words. The seal word "
                "is written by the reader and is printed nowhere.",
                "The letter slots must be drawn EMPTY.",
                "The notch on the stamp edge must be visible and unnumbered in "
                "the artwork; the number is set in type.",
            ],
            status="specified-not-produced",
        ))

    # ── ④ İLERLEME ROZETLERİ ───────────────────────────────────────────────
    # Üç zorluk işareti + rota göstergesi + saha araştırmacısı damgası.
    # Bunlar tasarım dizgesinin ZATEN tanımladığı öğelerdir
    # (DESIGN_SYSTEM § 7): burada yeni bir öğe icat edilmiyor, var olan
    # öğenin varlığı üretiliyor.
    badges = [
        ("badge-star-1", "One-star difficulty mark", "DESIGN_SYSTEM.md § 1 modül ②"),
        ("badge-star-2", "Two-star difficulty mark", "DESIGN_SYSTEM.md § 1 modül ②"),
        ("badge-star-3", "Three-star difficulty mark", "DESIGN_SYSTEM.md § 1 modül ②"),
        ("badge-star-box", "Star box module: letter squares with one outlined",
         "DESIGN_SYSTEM.md § 4"),
        ("badge-seal-counter", "Region seal counter: n of N filled slots",
         "DESIGN_SYSTEM.md § 7"),
        ("badge-field-researcher", "Field researcher certificate stamp",
         "book.json § finalQuest.quest[4]"),
    ]
    for aid, purpose, src in badges:
        fn = aid + ".png"
        assets.append(entry(
            assetId=aid,
            assetClass="badge",
            activityId=None,
            region=None,
            culture=None,
            visualClass="badge",
            purpose=purpose,
            sourceSpec=src,
            requiredLabels=[],
            orientation="square",
            aspectRatio=BADGE_ASPECT,
            targetDimensions=list(BADGE_PX),
            safeArea=dict(SAFE_AREA),
            minDpi=300,
            format="png",
            colour="grayscale",
            filename=fn,
            rawLocation=RAW + fn,
            processedLocation=PROCESSED + fn,
            finalLocation=FINAL + fn,
            rejectedLocation=REJECTED + fn,
            promptRef="07_ASSETS/IMAGE_PROMPT_LIBRARY.html#" + aid,
            restrictions=BASE_RESTRICTIONS + [
                "This is a reusable interface element: it must read at small "
                "size and carry no culture-specific ornament.",
                "⭑ No letters inside the star box squares: they are filled by "
                "the reader.",
            ],
            status="specified-not-produced",
        ))

    # ── ⑤ ÖN MADDE GÖRSELLERİ ──────────────────────────────────────────────
    # Ön madde sayfalarının bir kısmı görsel ister ve `visualNeed` alanı
    # bunu BEYAN eder. Beyan etmeyen bir sayfa için varlık üretilmez:
    # envanter dilekten değil ŞARTNAMEDEN türer.
    fm = book.get("frontMatter") or {}
    for s in fm.get("sections") or []:
        if not s.get("visualNeed"):
            continue
        aid = "front-%s" % s["id"]
        fn = aid + ".png"
        assets.append(entry(
            assetId=aid,
            assetClass="front-matter",
            activityId=None,
            region=None,
            culture=None,
            visualClass="diagram",
            purpose=s.get("purpose"),
            sourceSpec="02_MANUSCRIPT/book.json#frontMatter.%s" % s["id"],
            requiredLabels=list(s.get("prints") or [])[:0] or [],
            orientation="portrait",
            aspectRatio=FRONT_ASPECT,
            targetDimensions=list(FRONT_PX),
            safeArea=dict(SAFE_AREA),
            minDpi=300,
            format="png",
            colour="grayscale",
            filename=fn,
            rawLocation=RAW + fn,
            processedLocation=PROCESSED + fn,
            finalLocation=FINAL + fn,
            rejectedLocation=REJECTED + fn,
            promptRef="07_ASSETS/IMAGE_PROMPT_LIBRARY.html#" + aid,
            restrictions=BASE_RESTRICTIONS + [
                "⭑ This diagram teaches the book's own rules. It must use a "
                "NEUTRAL demonstration subject and must not reproduce any real "
                "activity page from the book.",
                "⭑ It must carry no seal word, no star word and no answer.",
            ],
            status="specified-not-produced",
        ))

    counts = collections.Counter(a["assetClass"] for a in assets)
    doc = collections.OrderedDict()
    doc["$comment"] = [
        "ÜRETİLMİŞTİR — 04_BUILD/asset_manifest.py · ELLE DÜZENLEMEYİN.",
        "",
        "Envanter DÖRT kaynaktan TÜRETİLİR ve toplam HESAPLANIR:",
        "  ① aktivite görselleri   book.json § activities[].visualSpec",
        "  ② kültür vinyetleri     culture_index.json § cultures[]",
        "  ③ mühür damgaları       region_index.json § sealStampMotif",
        "  ④ rozetler              DESIGN_SYSTEM § 1 · § 4 · § 7",
        "  ⑤ ön madde görselleri   book.json § frontMatter § visualNeed",
        "",
        "Yol haritası '~150' diyor. Bu bir TAHMİNDİR; gerçek sayı buradadır",
        "ve 150'ye YUVARLANMAZ (kurucu talimatı § 10).",
        "",
        "⚠ BİR YOL BİR VARLIK DEĞİLDİR. rawLocation dolu olması dosyanın",
        "VAR OLDUĞU anlamına gelmez; onu `status` söyler ve qa_assets.py",
        "diskten DOĞRULAR.",
        "",
        "⚠ MÜHÜR DAMGALARI VE ROZETLER HİÇBİR HARF TAŞIMAZ. Mühür sözcüğü",
        "çocuğun kendi yazdığı şeydir ve basılı hiçbir yerde durmaz (§ 19).",
    ]
    doc["version"] = 1
    doc["generator"] = "04_BUILD/asset_manifest.py"
    doc["layers"] = collections.OrderedDict([
        ("raw", RAW), ("processed", PROCESSED),
        ("final", FINAL), ("rejected", REJECTED)])
    doc["counts"] = collections.OrderedDict(
        [(k, counts[k]) for k in sorted(counts)] + [("total", len(assets))])
    doc["roadmapEstimate"] = 150
    doc["assets"] = assets
    return doc


def redact(doc):
    """Takip edilen sürümü üretir: içerik ÇIKARILIR, sağlama KALIR.

    Bir sayım ile bir içerik aynı şey değildir. `requiredLabels: 9`
    denetlenebilir bir olgudur; `requiredLabels: ['chilli', ...]` bir
    cevaptır. Public dosya birinciyi taşır, ikincisini taşımaz."""
    pub = collections.OrderedDict()
    for k, v in doc.items():
        if k != "assets":
            pub[k] = v
    pub["$comment"] = list(doc["$comment"]) + [
        "",
        "⭑ BU DOSYA İÇERİK TAŞIMAZ — SAYIM VE SAĞLAMA TAŞIR ⭑",
        "requiredLabels · restrictions · purpose · sourceSpec bu dosyada",
        "YOKTUR. Üçü de cevap taşıyabilir (bir ölçüm kısıtı çoğu zaman",
        "cevabın kendisidir) ve K10 cevabın public depoda durmasını",
        "yasaklar.",
        "",
        "Tam kayıt: 07_ASSETS/ASSET_MANIFEST.local.json (.gitignore § ③c)",
        "Sürüklenme denetimi: her varlık privateSha256 taşır.",
    ]
    out = []
    for a in doc["assets"]:
        r = collections.OrderedDict()
        for k, v in a.items():
            if k in PRIVATE_FIELDS:
                continue
            r[k] = v
        r["requiredLabelCount"] = len(a.get("requiredLabels") or [])
        r["restrictionCount"] = len(a.get("restrictions") or [])
        blob = json.dumps({k: a.get(k) for k in PRIVATE_FIELDS},
                          ensure_ascii=False, sort_keys=True)
        r["privateSha256"] = hashlib.sha256(blob.encode("utf-8")).hexdigest()
        out.append(r)
    pub["assets"] = out
    return pub


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    print("=" * 74)
    print("  VARLIK ENVANTERİ")
    print("=" * 74)

    if not os.path.isfile(BOOK):
        print("  ⊘ manuscript depoda yok (K10) — envanter üretilemedi, BOŞ KOŞTU")
        print("=" * 74)
        return 0

    doc = build()
    new_local = json.dumps(doc, ensure_ascii=False, indent=2) + "\n"
    new = json.dumps(redact(doc), ensure_ascii=False, indent=2) + "\n"

    for k in sorted(doc["counts"]):
        if k != "total":
            print("  %-18s %3d" % (k, doc["counts"][k]))
    print("  %-18s %3d   (yol haritası tahmini %d)"
          % ("TOPLAM", doc["counts"]["total"], doc["roadmapEstimate"]))

    if args.check:
        stale = []
        for path, want in ((OUT, new), (OUT_LOCAL, new_local)):
            old = ""
            if os.path.isfile(path):
                with open(path, encoding="utf-8") as fh:
                    old = fh.read()
            if old != want:
                stale.append(os.path.relpath(path, ROOT))
        if stale:
            print("\n  ✗ BAYAT: %s" % ", ".join(stale))
            print("\n  Tazele: ./04_BUILD/asset_manifest.py")
            print("=" * 74)
            return 1
        print("\n  ✅ envanter güncel (takip edilen + yerel)")
        print("=" * 74)
        return 0

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(new)
    with open(OUT_LOCAL, "w", encoding="utf-8") as fh:
        fh.write(new_local)
    print("\n  yazıldı: %s   (takip edilen · içeriksiz)"
          % os.path.relpath(OUT, ROOT))
    print("  yazıldı: %s   (yerel · tam kayıt)"
          % os.path.relpath(OUT_LOCAL, ROOT))
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
