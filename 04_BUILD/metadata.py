#!/usr/bin/env python3
"""
KDP METADATA VE KAPAK GEOMETRİSİ — The Myth Hunter's Field Book
================================================================================
Yükleme paketinin **makine okunur** parçasını üretir ve denetler:

  ① METADATA      başlık · alt başlık · yazar · biyografi · BISAC · anahtar
  ② KAPAK GEOMETRİSİ  sırt kalınlığı · tam kapak ölçüsü · güvenli alan
  ③ İÇ BLOK       PDF var mı · sayfa sayısı ölçümle uyuşuyor mu
  ④ BEYAN         yer tutucu metin · sahte ISBN · eksik biyografi

⭑ SIRT KALINLIĞI BİR TAHMİN DEĞİL BİR FORMÜLDÜR ⭑

KDP beyaz kâğıt siyah-beyaz baskı için sırt = sayfa × 0,002252 inç.
160 sayfa → 0,360 inç. Bu sayı **sayfa sayısından türer** ve sayfa
sayısı değiştiğinde sırt da değişir; ikisini ayrı yerlerde tutmak,
kapağın bir gün yanlış sırtla basılması demektir.

    Kapak ölçüsü elle yazılmaz. Sayfa sayısından TÜRETİLİR.

⚠ AJAN KDP PANELİNE DOKUNMAZ. Bu betik yüklenecek DOSYALARI ve
yüklerken girilecek DEĞERLERİ üretir; yüklemeyi kurucu yapar.

  ./04_BUILD/metadata.py            paketi üret
  ./04_BUILD/metadata.py --check    eksik/çelişkili ise KIRMIZI

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
BOOK = os.path.join(ROOT, "02_MANUSCRIPT", "book.json")
ACTIVITY_INDEX = os.path.join(ROOT, "01_SOURCE", "activity_index.json")
INTERIOR = os.path.join(ROOT, "08_OUTPUT", "PAPERBACK", "interior.pdf")
INTERIOR_REPORT = os.path.join(ROOT, "06_REPORTS", "interior.json")
OUT = os.path.join(ROOT, "06_REPORTS", "tracked", "metadata.json")
COVER = os.path.join(ROOT, "03_COVER", "COVER_SPEC.md")

# KDP · beyaz kâğıt · siyah-beyaz · sayfa başına sırt kalınlığı (inç)
SPINE_PER_PAGE = 0.002252
BLEED = 0.125
COVER_SAFE = 0.25          # kapak kenarından güvenli alan
SPINE_TEXT_MIN_PAGES = 79  # bu sayfanın altında sırta yazı basılmaz

PLACEHOLDER = re.compile(r"\b(lorem ipsum|tbd|todo|xxx|placeholder|coming soon)\b",
                         re.I)

# ⭑ AÇIKLAMADAKİ SAYILAR ELLE YAZILMAZ — VE BU BİR ÜSLUP MESELESİ DEĞİL ⭑
#
# Faz 6 açıklaması şu cümleyle üretildi ve cümle ELLE YAZILMIŞTI:
#
#     "Twenty-two peoples. One hundred and twenty pages."
#
# Sayı doğruydu — YAZILDIĞI GÜN. `pageWeight` düzeltilip dizgi 144 yerine
# 160 ölçtüğünde (K38) açıklama ölçümle birlikte HAREKET ETMEDİ, çünkü
# ölçüme bağlı değildi. Sonuç: müşteriye bakan tek metin, kitabın
# fiziksel gerçeğiyle 40 sayfa çelişiyordu.
#
# Ve iki büyüklük gerçekten AYRIDIR:
#     120 = AKTİVİTE (bulmaca) sayısı   ← alt başlığın vaadi
#     160 = SAYFA sayısı (dizgiden ölçüldü)
# İkisini aynı sözcükle anmak bir pazarlama tercihi değil, bir HATADIR.
#
#     Bir açıklama sayı iddia ediyorsa, o sayı ÖLÇÜMDEN gelmelidir.
#
# Aşağıdaki kalıp sayıları `%d` ile taşır ve `§ ⑤` kapısı açıklamanın
# iddia ettiği her sayıyı ölçümle karşılaştırır. Elle yazılmış bir sayı
# artık sessizce bayatlayamaz: CI'ı KIRMIZI yakar.
DESCRIPTION_TEMPLATE = (
    "Twenty-two peoples. {activities_word} puzzles across {pages_word} pages. "
    "Six seals to earn. This is not a puzzle book with a mythology theme — "
    "every puzzle is built out of what a people actually made: a writing "
    "system, a counting system, a map of a real place, a message that had to "
    "travel. Children decode Younger Futhark and Inuktitut syllabics, count "
    "in Maya bars and dots, trace the Red River delta, and sort the Akan day "
    "names. Answers are checked against museums, archives and universities, "
    "and the back of the book says which ones. Screen-free, written in, and "
    "finished with a certificate."
)

# Açıklama sayıyı RAKAMLA değil SÖZCÜKLE anar (pazarlama dili). Kapının
# sayıyı yeniden okuyabilmesi için karşılık tablosu burada durur; tablo
# yoksa kapı rakama düşer ve yine denetler.
NUMBER_WORDS = {
    100: "one hundred", 110: "one hundred and ten", 120: "one hundred and twenty",
    130: "one hundred and thirty", 140: "one hundred and forty",
    144: "one hundred and forty-four", 148: "one hundred and forty-eight",
    150: "one hundred and fifty", 160: "one hundred and sixty",
    168: "one hundred and sixty-eight", 176: "one hundred and seventy-six",
    180: "one hundred and eighty", 192: "one hundred and ninety-two",
    200: "two hundred",
}


def number_word(n):
    """Sayıyı pazarlama diline çevirir; karşılığı yoksa RAKAM basar.

    Uydurma bir sözcük üretmez: tablo dışındaki bir sayı için '160' yazmak,
    yanlış bir 'one hundred and sixty-two' yazmaktan iyidir."""
    return NUMBER_WORDS.get(int(n), str(int(n)))


def description_for(activities, pages):
    return DESCRIPTION_TEMPLATE.format(
        activities_word=number_word(activities).capitalize(),
        pages_word=number_word(pages))


class Report:
    def __init__(self, verbose):
        self.verbose, self.errors, self.warnings, self.checks = verbose, [], [], 0
        self.facts = {}

    def check(self, cond, label):
        self.checks += 1
        if cond:
            if self.verbose:
                print("  ✓ %s" % label)
        else:
            self.errors.append(label)
            print("  ✗ %s" % label)
        return bool(cond)

    def warn(self, label):
        self.warnings.append(label)
        print("  ! %s" % label)


def jload(p, default=None):
    if not os.path.isfile(p):
        return default
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def pdf_pages(path):
    if not os.path.isfile(path):
        return None
    with open(path, "rb") as fh:
        blob = fh.read()
    n = len(re.findall(rb"/Type\s*/Page[^s]", blob))
    return n or None


def _royalty(cfg, pages):
    """liste × oran − baskı maliyeti. KDP formülü, tek yerde."""
    pc = cfg["production"]["kdpPrintCost"]
    ed = next(e for e in cfg["production"]["editionsHypothesis"]
              if e["id"] == "paperback")
    rate = (pc["royaltyRateAtOrAbove999"] if ed["list"] >= 9.99
            else pc["royaltyRateBelow999"])
    cost = pc["paperbackLargeTrimBW"]["fixed"] + pages * pc["paperbackLargeTrimBW"]["perPage"]
    return round(ed["list"] * rate - cost, 2)


def build(cfg, book, pages, rep):
    pr, fo, au = cfg["project"], cfg["founder"], cfg["audience"]
    spine = round(pages * SPINE_PER_PAGE, 4)
    tw, th = cfg["production"]["trimPaperback"]["w"], cfg["production"]["trimPaperback"]["h"]
    # AKTİVİTE sayısı manuscript'ten SAYILIR; SAYFA sayısı PDF'ten ÖLÇÜLÜR.
    # İkisi ayrı büyüklüktür ve açıklama ikisini ayrı sözcükle anmak zorundadır.
    #
    # ⚠ MANUSCRIPT DEPODA DURMAZ (K10) — VE BU BİR SIFIR DEĞİLDİR.
    #
    # CI'da `book.json` yoktur. Naif bir `len(book.activities)` orada 0
    # verir ve açıklama *"0 puzzles"* diye üretilirdi — üstelik kapılar
    # yeşil kalarak, çünkü 0 == 0. Bu, Faz 5/6'da CI'ı iki kez kırmızı
    # yakan hatanın aynası: bir KAYNAĞIN YOKLUĞU bir ÖLÇÜM sanılıyor.
    #
    #     Üretilmemiş bir çıktı bozuk bir çıktı değildir —
    #     ve OLMAYAN bir kaynak SIFIR bir kaynak değildir.
    #
    # Yedek kaynak takip edilen `activity_index.json`: orada `written`
    # durumundaki kayıtlar tam olarak yazılmış sayfalardır.
    activities = len((book or {}).get("activities") or [])
    if not activities:
        idx = jload(ACTIVITY_INDEX, {}) or {}
        activities = sum(1 for a in idx.get("activities", [])
                         if a.get("status") == "written")
        if activities:
            print("  aktivite kaynağı: activity_index (manuscript depoda yok) → %d"
                  % activities)

    md = {
        "$comment": [
            "ÜRETİLMİŞTİR — 04_BUILD/metadata.py · ELLE DÜZENLEMEYİN.",
            "",
            "Bu dosya KDP paneline GİRİLECEK değerleri taşır. Paneli KURUCU",
            "doldurur; ajan panele dokunmaz (yol haritası Faz 6 § 13).",
            "",
            "Sırt kalınlığı sayfa sayısından TÜRETİLİR; elle yazılmaz.",
        ],
        "title": pr["title"],
        "subtitle": pr["subtitleHypothesis"],
        "author": fo["author"],
        "publisher": fo["publisher"],
        "authorBio": fo.get("authorBio"),
        "language": cfg["language"]["commercial"],
        "isbn": {"strategy": fo["isbn"]["strategy"],
                 "paperback": fo["isbn"]["paperback"],
                 "note": "KDP ücretsiz ISBN verir; SAHTE ISBN YAZILMAZ."},
        "audience": {"ageMin": au["readerAgeMin"], "ageMax": au["readerAgeMax"],
                     "gradeRange": au["gradeRange"],
                     "bisacPrimary": au["bisacPrimary"],
                     "bisacSecondary": au["bisacSecondary"]},
        "keywords": [
            "screen free activity book kids 8-12",
            "mythology puzzles for children",
            "world cultures activity book",
            "codes and ciphers for kids",
            "maps and mazes puzzle book",
            "gift for curious kids age 9",
            "homeschool world mythology",
        ],
        "description": description_for(activities, pages),
        "descriptionFacts": {
            "$comment": ("Açıklamanın İDDİA ETTİĞİ sayılar. § ⑤ kapısı bunları "
                         "ölçümle karşılaştırır; elle yazılmış bir sayı "
                         "sessizce bayatlayamaz."),
            "activities": activities,
            "pages": pages,
        },
        "edition": {
            "format": "paperback", "trim": "%.2f x %.2f in" % (tw, th),
            "pages": pages, "ink": cfg["production"]["ink"],
            "paper": cfg["production"]["paper"],
            "interiorPdf": os.path.relpath(INTERIOR, ROOT),
        },
        "pricing": {
            "list": next(e["list"] for e in cfg["production"]["editionsHypothesis"]
                         if e["id"] == "paperback"),
            "printCost": round(cfg["production"]["kdpPrintCost"]
                               ["paperbackLargeTrimBW"]["fixed"]
                               + pages * cfg["production"]["kdpPrintCost"]
                               ["paperbackLargeTrimBW"]["perPage"], 2),
            # ⭑ TELİF ELLE YAZILMAZ, HESAPLANIR ⭑
            # Sayfa sayısı 160 → 156 olunca baskı maliyeti düştü ama
            # `royaltyBaseline` bir CONFIG SABİTİYDİ ve yerinde kaldı:
            # metadata 3,65 $ baskı maliyeti ile 5,27 $ telif iddia
            # ediyordu. İkisi aynı formülün iki ucudur ve ayrı
            # duramazlar.
            "royaltyBaseline": _royalty(cfg, pages),
        },
        "cover": {
            "spineInches": spine,
            "spineTextAllowed": pages >= SPINE_TEXT_MIN_PAGES,
            "fullCoverWidthInches": round(2 * tw + spine + 2 * BLEED, 4),
            "fullCoverHeightInches": round(th + 2 * BLEED, 4),
            "bleedInches": BLEED, "safeMarginInches": COVER_SAFE,
        },
        "aiDisclosure": {
            "founderConfirmed": fo["aiDisclosure"]["founderConfirmed"],
            "note": "KDP panelindeki AI beyanı SEÇİMİNİ kurucu yapar.",
        },
        "measuredFrom": {
            "typesetPages": pages,
            "source": os.path.relpath(INTERIOR, ROOT),
        },
    }
    rep.facts["spineInches"] = spine
    rep.facts["pages"] = pages
    return md


def cover_spec(md):
    c = md["cover"]
    return "\n".join([
        "# KAPAK GEOMETRİSİ — The Myth Hunter's Field Book",
        "",
        "<!-- ÜRETİLMİŞTİR — 04_BUILD/metadata.py · ELLE DÜZENLEMEYİN -->",
        "",
        "> Bütün ölçüler **sayfa sayısından türetilmiştir**. Sayfa sayısı",
        "> değişirse bu dosya yeniden üretilmelidir — sırt onunla birlikte",
        "> değişir.",
        "",
        "| | |",
        "|---|---:|",
        "| Sayfa | **%d** |" % md["edition"]["pages"],
        "| Trim | %s |" % md["edition"]["trim"],
        "| Kâğıt · mürekkep | %s · %s |" % (md["edition"]["paper"], md["edition"]["ink"]),
        "| **Sırt kalınlığı** | **%.4f in** |" % c["spineInches"],
        "| Sırta yazı basılabilir mi | %s |" % ("EVET" if c["spineTextAllowed"] else "HAYIR"),
        "| **Tam kapak (bleed dâhil)** | **%.4f × %.4f in** |"
        % (c["fullCoverWidthInches"], c["fullCoverHeightInches"]),
        "| Bleed | %.3f in |" % c["bleedInches"],
        "| Güvenli kenar | %.2f in |" % c["safeMarginInches"],
        "",
        "## Formül",
        "",
        "```",
        "sırt        = sayfa × 0,002252 in      (KDP · beyaz kâğıt · S/B)",
        "kapak eni   = 2 × trim eni + sırt + 2 × bleed",
        "kapak boyu  = trim boyu + 2 × bleed",
        "```",
        "",
        "## ⚠ Kapak sanatı bu depoda ÜRETİLMEDİ",
        "",
        "Bu dosya kapağın **geometrisini** verir, sanatını değil. Kapak",
        "tasarımı kurucuya aittir ve ön/arka/sırt tek bir düz PDF olarak",
        "yüklenir.",
        "",
        "Arka kapakta bulunması gerekenler:",
        "",
        "- alt başlık (ebeveyne konuşan satır)",
        "- yaş bandı: **%d–%d**" % (md["audience"]["ageMin"], md["audience"]["ageMax"]),
        "- *screen-free* ve *120 puzzles · 22 cultures* sinyalleri",
        "- yazar biyografisi (§ metadata.authorBio)",
        "- barkod alanı **boş bırakılır** — KDP kendi barkodunu basar",
        "",
    ]) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    print("=" * 74)
    print("  KDP METADATA VE KAPAK GEOMETRİSİ")
    print("=" * 74)

    rep = Report(args.verbose)
    cfg = jload(CONFIG)
    book = jload(BOOK)
    if cfg is None:
        print("  ⛔ project_config.json okunamadı")
        return 1

    # Sayfa sayısı ÖLÇÜMDEN gelir: önce gerçek PDF, yoksa dizgi raporu.
    pages = pdf_pages(INTERIOR)
    src = "interior.pdf"
    if pages is None:
        ir = jload(INTERIOR_REPORT, {})
        pages = (ir.get("facts") or {}).get("typesetPagesSignatureAligned")
        src = "interior.json"
    if pages is None:
        pages = cfg["scope"]["pageTarget"]
        src = "scope.pageTarget (DİZGİ YOK)"
    print("  sayfa kaynağı: %s → %s" % (src, pages))

    md = build(cfg, book, pages, rep)

    print("\n── ① metadata ──")
    rep.check(bool(md["authorBio"]),
              "authorBio dolu (A6 · Faz 6 kapısı)")
    rep.check(md["isbn"]["paperback"] is None or
              re.fullmatch(r"[0-9-]{10,17}", str(md["isbn"]["paperback"] or "")) is not None,
              "ISBN ya boş ya geçerli biçimde — SAHTE ISBN yok")
    blob = json.dumps(md, ensure_ascii=False)
    hits = PLACEHOLDER.findall(blob)
    rep.check(not hits, "yer tutucu metin yok" + ("" if not hits else " — %s" % set(hits)))
    rep.check(len(md["keywords"]) >= 5, "en az beş anahtar kelime (%d)" % len(md["keywords"]))
    rep.check(40 <= len(md["description"].split()) <= 400,
              "açıklama uzunluğu bantta (%d kelime)" % len(md["description"].split()))
    rep.check(md["language"] == "en", "ticari dil İngilizce (%s)" % md["language"])

    print("\n── ② kapak geometrisi ──")
    c = md["cover"]
    print("  sırt %.4f in · tam kapak %.4f × %.4f in"
          % (c["spineInches"], c["fullCoverWidthInches"], c["fullCoverHeightInches"]))
    rep.check(c["spineInches"] > 0, "sırt kalınlığı hesaplandı")
    rep.check(c["spineTextAllowed"] == (pages >= SPINE_TEXT_MIN_PAGES),
              "sırt yazısı kuralı sayfa sayısıyla tutarlı")

    print("\n── ③ iç blok ──")
    # ⚠ 08_OUTPUT ÜRETİLMİŞ ÇIKTIDIR VE DEPODA DURMAZ (.gitignore § ⑤).
    #
    # CI'da iç blok PDF'i YOKTUR ve olmaması bir kusur değildir: kaynaktan
    # yeniden üretilebilir. Bir kapı, bir BUILD ÇIKTISININ yokluğunu bir
    # kalite düşüşü sanmamalıdır — bu hata Faz 5'te `update_docs` ile bir
    # kez yapıldı ve CI'ı kırmızı yaktı.
    #
    #     Üretilmemiş bir çıktı, bozuk bir çıktı değildir.
    if os.path.isfile(INTERIOR):
        rep.check(True, "iç blok PDF üretilmiş (%s)"
                  % os.path.relpath(INTERIOR, ROOT))
        ir = jload(INTERIOR_REPORT, {})
        tp = (ir.get("facts") or {}).get("typesetPagesSignatureAligned")
        if tp:
            rep.check(tp == pages,
                      "PDF sayfa sayısı dizgi ölçümüyle aynı (%s == %s)"
                      % (pages, tp))
        tgt = cfg["scope"]["pageTarget"]
        rep.check(pages == tgt,
                  "sayfa sayısı onaylı hedefle aynı (%d == %d)" % (pages, tgt))
    else:
        print("  ⊘ iç blok PDF yok (08_OUTPUT depoda durmaz) — ③ ATLANDI")
        rep.warn("iç blok PDF bu makinede yok — sayfa sayısı "
                 "scope.pageTarget'tan alındı, ÖLÇÜLMEDİ")

    print("\n── ⑤ açıklamanın iddia ettiği sayılar ──")
    # ⭑ MÜŞTERİYE BAKAN TEK METİN, KİTABIN GERÇEĞİYLE ÇELİŞEMEZ ⭑
    #
    # Faz 6 açıklaması "One hundred and twenty pages" diyordu; dizgi 160
    # ölçmüştü. Sayı yanlış DEĞİLDİ — BAĞLI DEĞİLDİ. Bu kapı bağı kurar:
    # açıklamada geçen her büyüklük ölçümle karşılaştırılır ve iki
    # büyüklüğün BİRBİRİNE karışması ayrıca yakalanır.
    desc = md["description"]
    facts = md["descriptionFacts"]
    rep.check(facts["pages"] == pages,
              "açıklamanın sayfa iddiası ölçümle aynı (%d == %d)"
              % (facts["pages"], pages))
    # Kaynak build() ile AYNI olmak zorunda: manuscript varsa o, yoksa
    # takip edilen indeks. İki yerde iki farklı kaynak okumak, CI'da
    # 120 ile 0'ı karşılaştırıp kapıyı kırmızı yakardı.
    counted = len((book or {}).get("activities") or []) or sum(
        1 for a in (jload(ACTIVITY_INDEX, {}) or {}).get("activities", [])
        if a.get("status") == "written")
    rep.check(facts["activities"] == counted,
              "açıklamanın aktivite iddiası kaynakla aynı (%d == %d)"
              % (facts["activities"], counted))
    rep.check(number_word(pages) in desc.lower(),
              "ölçülen sayfa sayısı açıklamada geçiyor (%s)" % number_word(pages))
    # Karışma denetimi: aktivite sayısı 'pages' sözcüğünün yanında geçemez.
    wrong = re.search(r"%s\s+pages" % re.escape(number_word(facts["activities"])),
                      desc, re.I) if facts["activities"] != pages else None
    rep.check(wrong is None,
              "aktivite sayısı SAYFA diye anılmıyor (120 puzzle ≠ 120 page)")
    # Ve rakamla yazılmış bayat bir sayfa iddiası da yakalanır.
    stale = [m for m in re.findall(r"\b(\d{2,4})\s+pages\b", desc, re.I)
             if int(m) != pages]
    rep.check(not stale,
              "açıklamada bayat rakamlı sayfa iddiası yok"
              + ("" if not stale else " — %s" % stale))

    print("\n── ④ beyan ──")
    if not md["aiDisclosure"]["founderConfirmed"]:
        rep.warn("KDP AI beyanı SEÇİMİ kurucuda — panelde doldurulacak")
    if md["isbn"]["paperback"] is None:
        rep.warn("ISBN boş — KDP ücretsiz ISBN verecek (kurucu seçimi)")

    if not args.check:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8") as fh:
            json.dump(md, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        os.makedirs(os.path.dirname(COVER), exist_ok=True)
        with open(COVER, "w", encoding="utf-8") as fh:
            fh.write(cover_spec(md))
        print("\n  yazıldı: %s" % os.path.relpath(OUT, ROOT))
        print("  yazıldı: %s" % os.path.relpath(COVER, ROOT))

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        print("=" * 74)
        return 1
    print("  ✅ %d denetim yeşil · %d sayfa · sırt %.4f in"
          % (rep.checks, pages, rep.facts["spineInches"]))
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
