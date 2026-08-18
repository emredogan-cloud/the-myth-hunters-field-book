#!/usr/bin/env python3
"""
KDP KENAR BOŞLUĞU ADLİ DENETİMİ — The Myth Hunter's Field Book
================================================================================
Basılı sayfanın GERÇEK mürekkep sınırlarını ölçer ve KDP'nin ciltsiz
kenar boşluğu kurallarıyla karşılaştırır.

⭑ NEDEN BU KAPI DOĞDU ⭑

Yerel CI yeşilken **gerçek KDP Print Previewer** iki hata bildirdi:

    "Insufficient gutter. Books with 156 pages require at least 0.5\"
     for the gutter / inside margin…"
    "This text is outside the margins."  (sayfa 47)

Kök neden bir sabitti ve yazıldığı gün DOĞRUYDU:

    GUTTER = 9,5 mm = 0,374 in     ← 110–150 sayfa kademesi

Kitap 144 → 160 → 156 sayfaya taşındı ve **sabit taşınmadı**. 156 sayfa
151–300 kademesindedir ve 0,5 inç ister.

    Sayfa sayısından TÜREMESİ gereken bir ölçü elle yazıldığında,
    sayfa sayısı değiştiği gün sessizce yanlış olur.

Bu, `metadata § açıklama` ile birebir aynı sınıftır (K41) ve bu kapı
onu ölçüme bağlar.

⭑ NE ÖLÇER ⭑

Sayfa raster'a çevrilir ve BEYAZ OLMAYAN piksellerin kutusu bulunur:
bu, sayfanın gerçekten bastığı mürekkeptir — şartnamenin ne dediği
değil.

    Bir kenar boşluğu, hesaplandığı yerde değil BASILDIĞI yerde ölçülür.

Karşıt sayfa mimarisi korunur: tek sayfa (sağ/recto) cildi SOLDA,
çift sayfa (sol/verso) cildi SAĞDA taşır.

  ./04_BUILD/qa_margins.py            ölç ve raporla
  ./04_BUILD/qa_margins.py --dpi 200  daha ince ölçüm
  ./04_BUILD/qa_margins.py --pages 47 tek sayfa adli inceleme

Çıkış kodları:  0 = geçti   1 = İHLAL VAR   2 = bağımlılık yok
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

PDF = os.path.join(ROOT, "08_OUTPUT", "PAPERBACK", "interior.pdf")
CONFIG = os.path.join(ROOT, "project_config.json")
REPORT_JSON = os.path.join(ROOT, "06_REPORTS", "margins.json")
REPORT_MD = os.path.join(ROOT, "08_OUTPUT", "KDP_MARGIN_FORENSIC_REPORT.md")

# ⭑ KDP CİLTSİZ İÇ KENAR KADEMELERİ — sayfa sayısından TÜRETİLİR ⭑
# Kaynak: KDP baskı şartnamesi. Kademe elle seçilmez, sayfa sayısı seçer.
GUTTER_TIERS = [
    (24, 150, 0.375),
    (151, 300, 0.500),
    (301, 500, 0.625),
    (501, 700, 0.750),
    (701, 828, 0.875),
]
OUTSIDE_NO_BLEED = 0.25
OUTSIDE_WITH_BLEED = 0.375


def required_gutter(pages):
    """Sayfa sayısının KDP kademesi. Aralık dışıysa en yakın uç."""
    for lo, hi, val in GUTTER_TIERS:
        if lo <= pages <= hi:
            return val
    return GUTTER_TIERS[-1][2] if pages > 828 else GUTTER_TIERS[0][2]


def required_outside(bleed):
    return OUTSIDE_WITH_BLEED if bleed else OUTSIDE_NO_BLEED


def jload(p, default=None):
    if not os.path.isfile(p):
        return default
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


# ⭑ EŞİK KALİBRE EDİLDİ — İLK HÂLİ KENDİ ARTEFAKTINI ÖLÇÜYORDU ⭑
#
# İlk eşik 246'ydı: neredeyse beyaz pikselleri de "mürekkep" sayıyordu.
# Sonuç, 0,5 inçe TAM oturan bir metnin 0,4933 inçte görünmesiydi —
# yani kenar yumuşatma (antialiasing) halesi.
#
# Ölçüm (sayfa 3, üç çözünürlük, üç eşik):
#
#     eşik 246 → 0,4933 · 0,4967 · 0,4983   ← çözünürlükle 0,5'e yakınsıyor
#     eşik 200 → 0,5000 · 0,5000 · 0,4983   ← GERÇEK mürekkep
#     eşik 128 → 0,5000 · 0,5000 · 0,5000
#
#     Bir ölçüm aracı kendi artefaktını ölçüyorsa,
#     düzeltilmesi gereken ölçülen şey değil ARAÇTIR.
#
# Ayrıca raster ölçüm hiçbir zaman bir pikselden hassas olamaz; bu
# yüzden bir piksellik tolerans AÇIKÇA tanınır ve raporlanır.
INK_THRESHOLD = 200


def ink_box(png, thr=INK_THRESHOLD):
    """Sayfanın GERÇEK mürekkep kutusu — beyaz olmayan pikseller."""
    from PIL import Image
    im = Image.open(png).convert("L")
    w, h = im.size
    bw = im.point(lambda v: 0 if v < thr else 255)
    box = bw.point(lambda v: 255 if v == 0 else 0).getbbox()
    return box, (w, h)


def measure(pdf, dpi, only=None):
    rows = []
    with tempfile.TemporaryDirectory() as td:
        cmd = ["pdftoppm", "-r", str(dpi), "-gray", "-png", pdf,
               os.path.join(td, "p")]
        if only:
            cmd[1:1] = ["-f", str(only), "-l", str(only)]
        if subprocess.run(cmd, capture_output=True).returncode != 0:
            return None
        files = sorted(os.listdir(td))
        for i, f in enumerate(files):
            n = only if only else i + 1
            box, (w, h) = ink_box(os.path.join(td, f))
            rows.append({"page": n, "box": box, "px": [w, h]})
    return rows


# ⭑ ADLİ RAPOR — HER SAYFA, DÖRT MESAFE, TEK HÜKÜM ⭑
#
# Previewer bir sayfa numarası söyler ve susar. Bu rapor 156 satırın
# hepsini yazar: kutunun nerede olduğunu, dört mesafeyi, gerekeni ve
# hükmü. Böylece "sayfa 47" bir bilmece değil, bir SATIR olur.
MD_HEAD = """# KDP KENAR BOŞLUĞU ADLİ RAPORU

**The Myth Hunter's Field Book** · iç blok · `08_OUTPUT/PAPERBACK/interior.pdf`

> Bu rapor `04_BUILD/qa_margins.py` tarafından ÜRETİLİR. Elle düzenlemeyin;
> bir sonraki koşu üzerine yazar. Buradaki her sayı basılı sayfanın
> raster'ından ÖLÇÜLDÜ — hiçbiri şartnameden kopyalanmadı.

---

## ⓵ NEDEN BU RAPOR VAR

Yerel CI yeşilken **gerçek Amazon KDP Print Previewer** iki hata bildirdi:

```
Insufficient gutter. Books with 156 pages require at least 0.5" (12.700mm)
for the gutter / inside margin and at least 0.25" (6.35mm) for the
outside, top and bottom margins.
```
```
This text is outside the margins.        (sayfa 47)
```

İkisi de GERÇEKTİ. Kök neden bir sabitti ve yazıldığı gün doğruydu:

```python
GUTTER = 9.5 * MM          # = 0,3740 in  ← 110–150 sayfa kademesi
```

Kitap 144 → 160 → 156 sayfaya taşındı; sabit taşınmadı. 156 sayfa
151–300 kademesindedir ve **0,5 inç** ister. Açık 0,1260 in (3,20 mm)
ve 156 sayfanın **152'sini** kırıyordu.

> Sayfa sayısından TÜREMESİ gereken bir ölçü elle yazıldığında,
> sayfa sayısı değiştiği gün sessizce yanlış olur.

Sayfa 47 AYRI bir kusurdu: görev satırı sarmalanmıyordu
(`drawString`, `wrap_lines` değil). `egyptian-nile-map` görev cümlesi
7,918 in ölçüyor, sütun 7,626 in — fazlalık dış kenara taşıyordu.

## ⓶ ÖLÇÜM YÖNTEMİ

Her sayfa `pdftoppm` ile gri raster'a çevrilir ve BEYAZ OLMAYAN
piksellerin sınır kutusu bulunur. Ölçülen şey şartnamenin ne dediği
değil, sayfanın gerçekten BASTIĞI mürekkeptir.

Karşıt sayfa mimarisi korunur: **tek sayfa (recto) cildi SOLDA**,
**çift sayfa (verso) cildi SAĞDA** taşır. `inner` sütunu her satırda
o sayfanın kendi cilt tarafıdır.

> ⚠ Bu araç KDP Print Previewer'ı **taklit etmez ve simüle etmez**.
> KDP'nin yayımlanmış ciltsiz kenar boşluğu kurallarını modelleyip
> basılı sayfayı onlara karşı ölçer. Nihai hüküm yalnızca gerçek
> Previewer'a aittir.

### Ölçüm aracının kendi kalibrasyonu

İlk eşik (246) neredeyse beyaz pikselleri de mürekkep sayıyordu ve
0,5 inçe TAM oturan metni 0,4933 inçte gösteriyordu — yani kenar
yumuşatma halesini. Üç çözünürlük × üç eşik ölçüldü:

| eşik | 150 dpi | 300 dpi | 600 dpi | yorum |
|---|---|---|---|---|
| 246 | 0,4933 | 0,4967 | 0,4983 | çözünürlükle 0,5'e yakınsıyor → ARTEFAKT |
| 200 | 0,5000 | 0,5000 | 0,4983 | gerçek mürekkep |
| 128 | 0,5000 | 0,5000 | 0,5000 | gerçek mürekkep |

> Bir ölçüm aracı kendi artefaktını ölçüyorsa,
> düzeltilmesi gereken ölçülen şey değil ARAÇTIR.

Eşik 200'e indirildi ve raster'ın bir pikselden hassas olamayacağı
AÇIKÇA tanındı (tolerans = 1 piksel).

---
"""


def _fmt(v, nd=4):
    """Türkçe ondalık ayracı — belge Türkçe, sayılar da öyle olmalı."""
    return ("%.*f" % (nd, v)).replace(".", ",")


def write_md(facts, rows, viol, gutter_used=None):
    """Sayfa sayfa adli tablo — dört mesafe, gereken ve hüküm."""
    g, o = facts["requiredGutter"], facts["requiredOutside"]
    lines = [MD_HEAD]
    lines.append("## ⓷ ÖLÇÜLEN GEOMETRİ\n")
    lines.append("| ölçü | değer | kaynak |")
    lines.append("|---|---|---|")
    lines.append("| sayfa sayısı | **%d** | `pdfinfo` |" % facts["pages"])
    lines.append("| trim | %s × %s in | `pdfinfo` |"
                 % tuple(_fmt(v, 3) for v in facts["trimInches"]))
    lines.append("| bleed | %s | `project_config.json`" % (
        "VAR" if facts["bleed"] else "YOK") + " § production |")
    lines.append("| KDP kademesi | %s sayfa | sayfa sayısından TÜREDİ |"
                 % facts["tier"])
    lines.append("| **gereken iç/gutter** | **%s in** | kademe tablosu |" % _fmt(g))
    lines.append("| **gereken dış/üst/alt** | **%s in** | bleed durumu |" % _fmt(o))
    if gutter_used is not None:
        lines.append("| dizgide KULLANILAN gutter | %s in | `interior.py` "
                     "(KDP asgarisi + güvenlik payı) |" % _fmt(gutter_used))
    lines.append("| ölçüm çözünürlüğü | %d dpi | `--dpi` |"
                 % facts["measuredAtDpi"])
    lines.append("| mürekkep eşiği | %d/255 | kalibre edildi (§2) |"
                 % facts["inkThreshold"])
    lines.append("| ölçüm toleransı | %s in | 1 piksel |"
                 % _fmt(facts["measurementToleranceInches"], 5))
    lines.append("")
    lines.append("### En dar kenarlar (bütün kitapta)\n")
    lines.append("| kenar | en dar ölçüm | gereken | pay |")
    lines.append("|---|---|---|---|")
    for lab, key, req in (("iç / gutter", "minInner", g),
                          ("dış", "minOuter", o),
                          ("üst", "minTop", o),
                          ("alt", "minBottom", o)):
        v = facts[key]
        lines.append("| %s | %s in | %s in | **+%s in** |"
                     % (lab, _fmt(v), _fmt(req), _fmt(v - req)))
    lines.append("")
    lines.append("## ⓸ HÜKÜM\n")
    if viol:
        lines.append("**⛔ %d SAYFA İHLAL EDİYOR.**\n" % len(viol))
        lines.append("| sayfa | taraf | ihlal |")
        lines.append("|---|---|---|")
        for v in viol:
            lines.append("| %d | %s | %s |"
                         % (v["page"], v["side"], "; ".join(v["why"])))
    else:
        lines.append("**✅ ölçülen %d sayfanın hepsi geçiyor.** "
                     "Hiçbir sayfada iç, dış, üst veya alt kenar "
                     "KDP asgarisinin altına inmiyor.\n" % facts["pagesMeasured"])
    lines.append("")
    lines.append("## ⓹ SAYFA SAYFA ADLİ TABLO\n")
    lines.append("`box` = mürekkep sınır kutusu, raster pikselinde "
                 "(sol, üst, sağ, alt). `inner` sütunu o sayfanın CİLT "
                 "tarafıdır: recto'da sol, verso'da sağ.\n")
    lines.append("| s. | taraf | mürekkep kutusu (px) | iç | dış | üst | alt "
                 "| gereken iç | gereken dış/üst/alt | hüküm |")
    lines.append("|---:|---|---|---:|---:|---:|---:|---:|---:|---|")
    for r in rows:
        if r["verdict"] == "BLANK":
            lines.append("| %d | %s | — (boş sayfa) | — | — | — | — | %s "
                         "| %s | ⊘ BOŞ |"
                         % (r["page"], "recto" if r["page"] % 2 else "verso",
                            _fmt(g), _fmt(o)))
            continue
        bx = r.get("box")
        bxs = ("%d, %d, %d, %d" % tuple(bx)) if bx else "—"
        lines.append("| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s |"
                     % (r["page"], r["side"], bxs,
                        _fmt(r["inner"]), _fmt(r["outer"]),
                        _fmt(r["top"]), _fmt(r["bottom"]), _fmt(g), _fmt(o),
                        "✅ PASS" if r["verdict"] == "PASS" else "⛔ **FAIL**"))
    lines.append("")
    lines.append("---\n")
    lines.append("## ⓺ SAYFA 47 — PREVIEWER'IN ADIYLA ANDIĞI SAYFA\n")
    p47 = next((r for r in rows if r["page"] == 47), None)
    if p47 and p47["verdict"] != "BLANK":
        lines.append("| mesafe | ÖNCE (kusurlu dizgi) | SONRA (bu koşu) "
                     "| gereken |")
        lines.append("|---|---:|---:|---:|")
        lines.append("| iç / gutter | 0,4467 | **%s** | %s |"
                     % (_fmt(p47["inner"]), _fmt(g)))
        lines.append("| dış | **0,2200 ⛔** | **%s** | %s |"
                     % (_fmt(p47["outer"]), _fmt(o)))
        lines.append("| üst | 0,3733 | **%s** | %s |"
                     % (_fmt(p47["top"]), _fmt(o)))
        lines.append("| alt | 0,3333 | **%s** | %s |"
                     % (_fmt(p47["bottom"]), _fmt(o)))
        lines.append("")
        lines.append("Sayfa 47 `egyptian-nile-map`. Görev cümlesi "
                     "sarmalanmadan tek satırda basılıyordu ve sütunu "
                     "0,292 in aşıyordu. Çözüm metni KAYDIRMAK değil, "
                     "görev satırını sarmalamak ve zorluk yıldızlarına "
                     "genişlik ayırmaktı — aynı kusur 8 sayfada daha "
                     "vardı ve geniş gutter'la 13'e çıkacaktı.\n")
        lines.append("> Previewer bir sayfa söyler. Kusur bir SINIFTIR.\n")
    lines.append("---\n")
    lines.append("*Bu belge üretilmiştir · `04_BUILD/qa_margins.py` · "
                 "elle düzenlemeyin.*")
    os.makedirs(os.path.dirname(REPORT_MD), exist_ok=True)
    with open(REPORT_MD, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")



def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--pages", type=int, default=None)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    print("=" * 74)
    print("  KDP KENAR BOŞLUĞU ADLİ DENETİMİ")
    print("=" * 74)

    if not os.path.isfile(PDF):
        # ⚠ 08_OUTPUT üretilmiş çıktıdır ve depoda durmaz.
        print("  ⊘ interior.pdf yok (08_OUTPUT depoda durmaz) — BOŞ KOŞTU")
        print("=" * 74)
        return 0
    for tool in ("pdftoppm", "pdfinfo"):
        if subprocess.run(["which", tool], capture_output=True).returncode != 0:
            print("  ⊘ %s yok — ATLANDI" % tool)
            print("=" * 74)
            return 2
    try:
        import PIL  # noqa: F401
    except ImportError:
        print("  ⊘ Pillow yok — ATLANDI")
        print("=" * 74)
        return 2

    info = subprocess.run(["pdfinfo", PDF], capture_output=True, text=True).stdout
    import re
    pages = int(re.search(r"Pages:\s+(\d+)", info).group(1))
    pw, ph = (float(x) / 72.0 for x in
              re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", info).groups())

    cfg = jload(CONFIG, {}) or {}
    bleed = bool(cfg.get("production", {}).get("interiorBleed", False))
    g_req = required_gutter(pages)
    o_req = required_outside(bleed)

    print("  sayfa            %d" % pages)
    print("  trim             %.3f × %.3f in" % (pw, ph))
    print("  bleed            %s" % ("VAR" if bleed else "YOK"))
    print("  KDP kademesi     %s" % next(
        ("%d–%d sayfa" % (lo, hi) for lo, hi, v in GUTTER_TIERS
         if lo <= pages <= hi), "?"))
    print("  GEREKEN iç/gutter   %.4f in" % g_req)
    print("  GEREKEN dış/üst/alt %.4f in" % o_req)

    rows = measure(PDF, args.dpi, args.pages)
    if rows is None:
        print("  ⛔ render başarısız")
        return 1

    viol, out = [], []
    for r in rows:
        n, box = r["page"], r["box"]
        w, h = r["px"]
        if not box:
            out.append({**r, "verdict": "BLANK"})
            continue
        x0, y0, x1, y1 = box
        left = x0 / w * pw
        right = pw - x1 / w * pw
        top = y0 / h * ph
        bot = ph - y1 / h * ph
        # ⭑ KARŞIT SAYFA: tek sayfa (recto) cildi SOLDA taşır ⭑
        odd = (n % 2 == 1)
        inner_d = left if odd else right
        outer_d = right if odd else left
        # Bir piksellik ölçüm toleransı — raster bundan hassas olamaz.
        tol = 1.0 / args.dpi
        bad = []
        if inner_d < g_req - tol:
            bad.append("GUTTER %.4f < %.4f" % (inner_d, g_req))
        if outer_d < o_req - tol:
            bad.append("OUTER %.4f < %.4f" % (outer_d, o_req))
        if top < o_req - tol:
            bad.append("TOP %.4f < %.4f" % (top, o_req))
        if bot < o_req - tol:
            bad.append("BOTTOM %.4f < %.4f" % (bot, o_req))
        rec = {"page": n, "side": "recto" if odd else "verso",
               "box": [x0, y0, x1, y1], "rasterPx": [w, h],
               "inner": round(inner_d, 4), "outer": round(outer_d, 4),
               "top": round(top, 4), "bottom": round(bot, 4),
               "verdict": "FAIL" if bad else "PASS", "why": bad}
        out.append(rec)
        if bad:
            viol.append(rec)

    print("\n  ölçülen sayfa    %d" % len(out))
    print("  İHLAL            %d" % len(viol))
    if viol and not args.quiet:
        print("\n  ilk 12 ihlal:")
        for v in viol[:12]:
            print("    s.%-4d %-5s iç %.4f dış %.4f üst %.4f alt %.4f  → %s"
                  % (v["page"], v["side"], v["inner"], v["outer"],
                     v["top"], v["bottom"], "; ".join(v["why"])))

    facts = {"pages": pages, "trimInches": [round(pw, 4), round(ph, 4)],
             "bleed": bleed, "requiredGutter": g_req, "requiredOutside": o_req,
             "tier": next(("%d-%d" % (lo, hi) for lo, hi, v in GUTTER_TIERS
                           if lo <= pages <= hi), "?"),
             "measuredAtDpi": args.dpi, "inkThreshold": INK_THRESHOLD,
             "measurementToleranceInches": round(1.0 / args.dpi, 5),
             "pagesMeasured": len(out),
             "violations": len(viol),
             "minInner": round(min((r["inner"] for r in out
                                    if r["verdict"] != "BLANK"), default=0), 4),
             "minOuter": round(min((r["outer"] for r in out
                                    if r["verdict"] != "BLANK"), default=0), 4),
             "minTop": round(min((r["top"] for r in out
                                  if r["verdict"] != "BLANK"), default=0), 4),
             "minBottom": round(min((r["bottom"] for r in out
                                     if r["verdict"] != "BLANK"), default=0), 4)}
    # Dizginin GERÇEKTEN kullandığı gutter — rapor onu da yazsın.
    gutter_used = None
    itr = jload(os.path.join(ROOT, "06_REPORTS", "interior.json"), {}) or {}
    gu = (itr.get("facts") or {}).get("gutterInches")
    if isinstance(gu, (int, float)):
        gutter_used = float(gu)

    write_md(facts, out, viol, gutter_used)
    print("  → %s" % os.path.relpath(REPORT_MD, ROOT))

    os.makedirs(os.path.dirname(REPORT_JSON), exist_ok=True)
    with open(REPORT_JSON, "w", encoding="utf-8") as fh:
        json.dump({"status": "fail" if viol else "pass", "facts": facts,
                   "pages": out}, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    print("\n" + "=" * 74)
    if viol:
        print("  ⛔ %d SAYFA KDP KENAR BOŞLUĞUNU İHLAL EDİYOR" % len(viol))
        print("=" * 74)
        return 1
    print("  ✅ %d sayfanın hepsi KDP kenar boşluklarını geçiyor" % len(out))
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
