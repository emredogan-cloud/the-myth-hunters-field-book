#!/usr/bin/env python3
"""
A+ İÇERİK PAKETİ — The Myth Hunter's Field Book
================================================================================
Teslim edilen ham A+ görsellerinden Amazon modül ölçülerinde nihai
paketi üretir ve `08_OUTPUT/APLUS/` altına yazar.

⭑ İKİ TESLİM BİRLEŞİK GELDİ — REDDEDİLMEDİ, BÖLÜNDÜ ⭑

Şartname `aplus-02` için ÜÇ ayrı kare, `aplus-05` için DÖRT ayrı kare
istiyordu. Kurucu ikisini de TEK dosyada teslim etti: biri yatay
triptik, diğeri 2×2 ızgara.

    Teslim edilmiş bir varlık, biçimi beklenenden farklı diye
    ATILMAZ. Ayrıştırılabiliyorsa ayrıştırılır.

Paneller beyaz oluk aranarak ÖLÇÜLEREK bulunur; sabit koordinat
kullanılmaz.

⭑ BİR PANEL DÜŞÜRÜLDÜ — VE GEREKÇESİ ÖLÇÜMDÜR ⭑

`aplus-05`'in üçüncü paneli bir "kit" fotoğrafı: kalem · silgi ·
**CETVEL** · ip. Ölçüm:

    120 aktivitenin CETVEL kullananı:  0
    'ruler' sözcüğünün çocuğa görünen metinde geçişi:  0

Faz 5 bunu `B22` olarak zaten bulmuş ve ön maddedeki kit sayfasını
düzeltmişti. Aynı iddiayı bir PAZARLAMA görselinde tekrarlamak,
kitabın kendi düzeltmesini yalanlar — ve alıcıya sahip olmadığı bir
gereksinim satar.

    Ürün sayfası, ürünün içermediği bir şeyi göstermez.

Panel düşürüldü ve modül dört kareden ÜÇ kareye çekildi.

⭑ METİN GÖRSELE GİRMEZ ⭑

Amazon *Image & Text Overlay* modüllerinde arka plan görseline metin
eklenmemesini tavsiye ediyor. Kopya `APLUS_MODULE_MAP.md` içinde
AYRI durur ve panele oradan girilir.

  ./04_BUILD/aplus.py            paketi üret
  ./04_BUILD/aplus.py --check    üretilebilir mi

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = bağımlılık yok
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

MAP = os.path.join(ROOT, "07_ASSETS", "DELIVERY_MAP.json")
META = os.path.join(ROOT, "06_REPORTS", "tracked", "metadata.json")
OUT_DIR = os.path.join(ROOT, "08_OUTPUT", "APLUS")
REPORT = os.path.join(ROOT, "06_REPORTS", "aplus.json")

BANNER = (1940, 600)
SQUARE = (600, 600)
MAX_BYTES = 3 * 1024 * 1024

# ⚠ KOPYA ÖLÇÜLMÜŞ SAYILARDAN GELİR. Hiçbir satır ödül, onay,
# 'bestseller' ya da ÇOCUK TESTİ iddia edemez: externalValidation
# `overridden-zero-sessions` — sıfır oturum, sıfır testçi.
MODULES = [
    {"id": "aplus-01-hero", "module": "Standard Image & Text Overlay",
     "shape": "banner", "panels": 1,
     "purpose": "HERO — kitabın ne olduğu tek bakışta",
     "headline": "Not a puzzle book with a mythology theme",
     "body": ("Every puzzle is built out of what a people actually made: a "
              "writing system, a counting system, a map of a real place, a "
              "message that had to travel. {activities} puzzles across "
              "{cultures} cultures.")},
    {"id": "aplus-02-what-children-do", "module": "Standard Three Image & Text",
     "shape": "square", "panels": 3, "composite": "triptych",
     "purpose": "ÇOCUK NE YAPIYOR — çöz · diz · mühürle",
     "headline": "Work it out. Write it down. Earn the seal.",
     "body": ("Children decode, sort and draw their way through the book — "
              "then press a seal at the end of every region."),
     "panelCopy": ["Decode and write", "Sort the evidence", "Earn the seal"]},
    {"id": "aplus-03-six-regions", "module": "Standard Image Header with Text",
     "shape": "banner", "panels": 1,
     "purpose": "KAPSAM — altı bölge, yirmi iki halk",
     "headline": "Six regions. {cultures} peoples. One quest.",
     "body": ("From sea ice to cloud forest, the route crosses six regions "
              "and {cultures} cultures — each named by its own name.")},
    {"id": "aplus-04-real-cultures", "module": "Standard Single Image & Sidebar",
     "shape": "square", "panels": 1,
     "purpose": "GÜVENİLİRLİK — cevaplar kaynaklarla denetlendi",
     "headline": "Checked against museums, archives and universities",
     "body": ("Every cultural claim in the book was revalidated against "
              "primary and institutional sources, and the back of the book "
              "says which ones.")},
    {"id": "aplus-05-screen-free", "module": "Standard Three Image & Text",
     "shape": "square", "panels": 3, "composite": "quad", "dropPanels": [2],
     "purpose": "SATIN ALMA GEREKÇESİ — masa başı, ekransız",
     "headline": "A pencil. That is the whole kit.",
     "body": ("No screen, no app, no batteries. {pages} pages a child writes "
              "in, at a table, with a pencil."),
     "panelCopy": ["Closed and ready", "Open and working", "Finished for today"]},
    {"id": "aplus-06-maps-and-codes", "module": "Standard Single Left Image",
     "shape": "square", "panels": 1,
     "purpose": "AKTİVİTE TÜRLERİ — harita · kod · gözlem · sıralama",
     "headline": "Maps, keys, plates and cards",
     "body": ("Four kinds of work, {activities} times over: trace a real "
              "coast, build a key, label a plate, put an account back in "
              "order.")},
    {"id": "aplus-07-completion", "module": "Standard Image & Text Overlay",
     "shape": "banner", "panels": 1,
     "purpose": "TAMAMLAMA — bu kitap BİTİRİLİR",
     "headline": "Six seals, and a certificate at the end",
     "body": ("The book is a single quest with an ending. Six regions, six "
              "seals, and a final page that only opens when all six are in.")},
]


def jload(p, default=None):
    if not os.path.isfile(p):
        return default
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(65536), b""):
            h.update(c)
    return h.hexdigest()


class Report:
    def __init__(self):
        self.errors, self.warnings, self.checks = [], [], 0
        self.facts = {}

    def check(self, cond, label):
        self.checks += 1
        if not cond:
            self.errors.append(label)
            print("  ✗ %s" % label)
        return bool(cond)

    def warn(self, label):
        self.warnings.append(label)
        print("  ! %s" % label)


def content_box(im, thr=246):
    """Beyaz çerçeveyi atıp gerçek içerik kutusunu bulur."""
    g = im.convert("L")
    w, h = g.size
    px = g.load()
    cols = [x for x in range(w)
            if min(px[x, y] for y in range(0, h, max(1, h // 120))) < thr]
    rows = [y for y in range(h)
            if min(px[x, y] for x in range(0, w, max(1, w // 120))) < thr]
    if not cols or not rows:
        return (0, 0, w, h)
    return (cols[0], rows[0], cols[-1] + 1, rows[-1] + 1)


def gaps(im, box, axis, thr=246, min_run=6):
    """İçerik kutusu içindeki BEYAZ olukları bulur (panel ayırıcıları)."""
    g = im.convert("L")
    px = g.load()
    x0, y0, x1, y1 = box
    runs, cur = [], None
    rng = range(x0, x1) if axis == "x" else range(y0, y1)
    for i in rng:
        if axis == "x":
            blank = min(px[i, y] for y in range(y0, y1, max(1, (y1 - y0) // 90))) >= thr
        else:
            blank = min(px[x, i] for x in range(x0, x1, max(1, (x1 - x0) // 90))) >= thr
        if blank:
            cur = (i, i) if cur is None else (cur[0], i)
        elif cur is not None:
            if cur[1] - cur[0] + 1 >= min_run:
                runs.append(cur)
            cur = None
    if cur is not None and cur[1] - cur[0] + 1 >= min_run:
        runs.append(cur)
    return runs


def split_panels(im, kind, rep, aid):
    """Birleşik teslimi panellere ayırır. Oluklar ÖLÇÜLÜR."""
    box = content_box(im)
    x0, y0, x1, y1 = box
    if kind == "triptych":
        g = [r for r in gaps(im, box, "x") if r[0] > x0 + 40 and r[1] < x1 - 40]
        g.sort(key=lambda r: r[1] - r[0], reverse=True)
        cuts = sorted((r[0] + r[1]) // 2 for r in g[:2])
        if len(cuts) != 2:
            rep.warn("%s: oluk bulunamadı, eşit üçe bölündü" % aid)
            w = (x1 - x0) // 3
            cuts = [x0 + w, x0 + 2 * w]
        bounds = [(x0, cuts[0]), (cuts[0], cuts[1]), (cuts[1], x1)]
        return [im.crop((a, y0, b, y1)) for a, b in bounds]
    if kind == "quad":
        gx = [r for r in gaps(im, box, "x") if r[0] > x0 + 80 and r[1] < x1 - 80]
        gy = [r for r in gaps(im, box, "y") if r[0] > y0 + 80 and r[1] < y1 - 80]
        gx.sort(key=lambda r: r[1] - r[0], reverse=True)
        gy.sort(key=lambda r: r[1] - r[0], reverse=True)
        cx = ((gx[0][0] + gx[0][1]) // 2) if gx else (x0 + x1) // 2
        cy = ((gy[0][0] + gy[0][1]) // 2) if gy else (y0 + y1) // 2
        return [im.crop((x0, y0, cx, cy)), im.crop((cx, y0, x1, cy)),
                im.crop((x0, cy, cx, y1)), im.crop((cx, cy, x1, y1))]
    return [im.crop(box)]


def fit(im, target):
    """Hedef orana KIRPAR (merkezden), sonra hedefe ölçekler."""
    from PIL import Image
    tw, th = target
    w, h = im.size
    want = tw / th
    got = w / h
    if got > want:
        nw = int(h * want)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    elif got < want:
        nh = int(w / want)
        im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    return im.resize(target, Image.LANCZOS)


def save_under(im, path, limit=MAX_BYTES):
    """3 MB sınırının ALTINA indirene kadar JPEG kalitesini düşürür.
    Kalite ÖLÇÜLEREK seçilir, tahmin edilmez."""
    for q in (95, 92, 88, 84, 80, 75, 70):
        im.convert("RGB").save(path, "JPEG", quality=q, optimize=True,
                               progressive=True)
        if os.path.getsize(path) <= limit:
            return q
    return q


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    print("=" * 74)
    print("  A+ İÇERİK PAKETİ")
    print("=" * 74)

    dmap = jload(MAP)
    md = jload(META)
    if not dmap or not md:
        print("  ⊘ DELIVERY_MAP.json / metadata.json yok — BOŞ KOŞTU")
        print("=" * 74)
        return 0
    try:
        from PIL import Image
    except ImportError:
        print("  ⊘ Pillow yok — ATLANDI")
        print("=" * 74)
        return 2

    subs = {"activities": md["descriptionFacts"]["activities"],
            "pages": md["edition"]["pages"],
            "cultures": 22, "regions": 6}
    delivered = {d["assetId"]: d for d in dmap["deliveries"] if d["class"] == "aplus"}
    # Ham A+ sanatı depoda durmaz (.gitignore § ③): CI'da BOŞ KOŞ.
    if not any(os.path.isfile(os.path.join(ROOT, d["delivered"]))
               for d in delivered.values()):
        print("  ⊘ ham A+ sanatı depoda yok (.gitignore § ③) — BOŞ KOŞTU")
        print("=" * 74)
        return 0

    rep = Report()
    if not args.check:
        os.makedirs(OUT_DIR, exist_ok=True)
    produced, rows = [], []

    for m in MODULES:
        d = delivered.get(m["id"])
        if not rep.check(d is not None, "teslim var: %s" % m["id"]):
            continue
        src = os.path.join(ROOT, d["delivered"])
        if not rep.check(os.path.isfile(src), "dosya var: %s" % d["delivered"]):
            continue
        if sha256(src) != d["sha256"]:
            rep.check(False, "%s sha256 haritayla uyuşmuyor" % m["id"])
            continue

        im = Image.open(src).convert("RGBA")
        im = Image.alpha_composite(Image.new("RGBA", im.size, (255, 255, 255, 255)),
                                   im).convert("RGB")
        panels = (split_panels(im, m["composite"], rep, m["id"])
                  if m.get("composite") else [im])
        for i in sorted(m.get("dropPanels", []), reverse=True):
            if i < len(panels):
                panels.pop(i)
        if not rep.check(len(panels) >= m["panels"],
                         "%s: %d panel gerekiyor, %d bulundu"
                         % (m["id"], m["panels"], len(panels))):
            continue
        panels = panels[:m["panels"]]

        target = BANNER if m["shape"] == "banner" else SQUARE
        for n, p in enumerate(panels, 1):
            name = ("%s.jpg" % m["id"] if m["panels"] == 1
                    else "%s-%02d.jpg" % (m["id"], n))
            out = os.path.join(OUT_DIR, name)
            if args.check:
                produced.append(name)
                continue
            q = save_under(fit(p, target), out)
            size = os.path.getsize(out)
            produced.append(name)
            rows.append({
                "module": m["module"], "moduleId": m["id"], "file": name,
                "purpose": m["purpose"],
                "headline": m["headline"].format(**subs),
                "body": m["body"].format(**subs),
                "panelCopy": (m.get("panelCopy") or [None] * m["panels"])[n - 1],
                "dimensions": "%d × %d" % target,
                "bytes": size, "jpegQuality": q,
                "sha256": sha256(out),
            })
            rep.check(size <= MAX_BYTES, "%s < 3 MB (%.2f MB)" % (name, size / 1e6))

    print("\n  modül: %d · üretilen görsel: %d" % (len(MODULES), len(produced)))

    if args.check:
        print("=" * 74)
        return 1 if rep.errors else 0

    # ── modül haritası ────────────────────────────────────────────────────
    lines = [
        "# A+ İÇERİK MODÜL HARİTASI — The Myth Hunter's Field Book",
        "",
        "<!-- ÜRETİLMİŞTİR — 04_BUILD/aplus.py · ELLE DÜZENLEMEYİN -->",
        "",
        "> Kurucu bu tabloyu KDP **Marketing → A+ Content** ekranında "
        "satır satır uygular.",
        "> Görseller `08_OUTPUT/APLUS/` altındadır ve **yüklenmedi**.",
        "",
        "## ⭑ METİN GÖRSELE GÖMÜLÜ DEĞİLDİR ⭑",
        "",
        "Aşağıdaki *başlık* ve *gövde* metinleri Amazon'un kendi modül "
        "alanlarına girilir. Arka plan görselleri **metinsizdir** ve öyle "
        "kalmalıdır: gömülü metin düzeltilemez, mobilde okunmaz ve dil "
        "değişirse yeniden çizim ister.",
        "",
        "## ⚠ BU METİNLERİN İDDİA ETMEDİĞİ ŞEYLER",
        "",
        "- ödül · onay · *bestseller* · eğitim kurumu tavsiyesi",
        "- **çocuk testi** — `externalValidation = overridden-zero-sessions`; "
        "sıfır oturum, sıfır testçi. Hiçbir A+ satırı bunun aksini söylemez.",
        "- bir bulmaca cevabı, çözülmüş bir sayfa veya bir mühür harfi",
        "",
        "## Modüller",
        "",
    ]
    for r in rows:
        lines += [
            "### `%s` — %s" % (r["file"], r["module"]),
            "",
            "| | |", "|---|---|",
            "| **Amaç** | %s |" % r["purpose"],
            "| **Ölçü** | %s px |" % r["dimensions"],
            "| **Dosya boyutu** | %.2f MB (JPEG q%d) |" % (r["bytes"] / 1e6,
                                                           r["jpegQuality"]),
            "| **sha256** | `%s` |" % r["sha256"][:32],
        ]
        if r["panelCopy"]:
            lines.append("| **Panel etiketi** | %s |" % r["panelCopy"])
        lines += [
            "",
            "**Başlık (Amazon alanına girilir):**",
            "",
            "> %s" % r["headline"],
            "",
            "**Gövde (Amazon alanına girilir):**",
            "",
            "> %s" % r["body"],
            "",
        ]
    lines += [
        "---",
        "",
        "## Kurucuya kalan",
        "",
        "1. KDP → kitap → **Marketing** → **A+ Content Manager**",
        "2. **Create A+ Content** · dil: English",
        "3. Yukarıdaki modülleri **sırayla** ekle",
        "4. Her modüle kendi görselini yükle ve metnini yapıştır",
        "5. **Preview** · sonra **Submit for approval**",
        "6. Amazon moderasyonu birkaç iş günü sürer",
        "",
        "> ⚠ **Panel bir A+ belgesindeki modül sayısını sınırlar.** Sınır "
        "bu setten azsa yukarıdan aşağıya seçin: sıra **öncelik "
        "sırasıdır** (01 · 03 · 05 en yüksek ticari sinyali taşır).",
        "",
        "> **AJAN AMAZON'A HİÇBİR ŞEY YÜKLEMEDİ.**",
        "",
    ]
    with open(os.path.join(OUT_DIR, "APLUS_MODULE_MAP.md"), "w",
              encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    with open(os.path.join(OUT_DIR, "checksums.txt"), "w", encoding="utf-8") as fh:
        for r in sorted(rows, key=lambda x: x["file"]):
            fh.write("%s  %s\n" % (r["sha256"], r["file"]))

    rep.facts["modules"] = len(MODULES)
    rep.facts["images"] = len(rows)
    rep.facts["droppedPanels"] = {"aplus-05-screen-free":
                                  "kit paneli — CETVEL gösteriyor, kitapta "
                                  "cetvel kullanan 0 sayfa var (B22)"}
    with open(REPORT, "w", encoding="utf-8") as fh:
        json.dump({"status": "fail" if rep.errors else "pass",
                   "checks": rep.checks, "errors": rep.errors,
                   "warnings": rep.warnings, "facts": rep.facts,
                   "rows": rows}, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        print("=" * 74)
        return 1
    print("  ✅ %d denetim yeşil · %d görsel → 08_OUTPUT/APLUS/"
          % (rep.checks, len(rows)))
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
