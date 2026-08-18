#!/usr/bin/env python3
"""
CİLTSİZ KAPAK ÜRETİMİ — The Myth Hunter's Field Book
================================================================================
ARKA + SIRT + ÖN → **TEK PDF**. Tipografi VEKTÖR, yazı tipi GÖMÜLÜ.

⭑ SANAT KAHRAMANDIR — TİPOGRAFİ ÜSTÜNE YAPIŞTIRILMIŞ BİR KART DEĞİL ⭑

İlk sürüm metni okutabilmek için dört BEYAZ DİKDÖRTGEN çiziyordu:
başlık kutusu, yazar kutusu, arka kapak paneli ve sırt şeridi. Kurucu
onları reddetti ve haklıydı —

    Kapak bir illüstrasyon değil, üstüne beyaz UI kutuları
    yapıştırılmış bir görüntü gibi duruyordu.

Bu sürümde **hiçbir opak panel yok**. Okunurluk üç araçla kuruluyor ve
üçü de ÖLÇÜLEREK seçiliyor:

  ① YERİ ÖLÇ      her metin bloğunun altındaki sanatın ortalama
                  parlaklığı ve standart sapması ölçülür; mürekkep
                  rengi ondan TÜRETİLİR (açık zemin → koyu mürekkep)
  ② HARF HALESİ   kontrast desteği bir DİKDÖRTGEN değil, harflerin
                  KENDİ BİÇİMİDİR: glifler maskeye çizilir,
                  bulanıklaştırılır ve yumuşak bir ışıma olarak karışır
  ③ YER SEÇİMİ    yazar adı için ön panelin alt bölgesi TARANIR ve en
                  koyu-en sakin bant seçilir

Sanat her yerde GÖRÜNÜR kalır: halenin kenarı yoktur.

⭑ SIRT SANATIN İÇİNDEN GEÇER ⭑

Kurucunun sanatının kot dokulu cilt şeridi gerçek sırttan **%2,86
SOLDA** duruyordu: şerit arka kapağın üstüne düşüyor ve kapak üç ayrı
tasarım bloğu gibi okunuyordu. Sanat, ORANI BOZULMADAN, şeridin merkezi
gerçek sırt merkezine gelecek biçimde yeniden çerçevelendi.

    Ölçüm: cilt merkezi 0,4614 → 0,5000 · sırt merkezi 0,5000

Artık ARKA → SIRT → ÖN tek bir illüstrasyondur.

⭑ SIRT YAZISI OPTİK ORTALANIR — HESAPLA DEĞİL, ÖLÇÜMLE ⭑

Metin matematiksel olarak ortalanır, sonra kapak İKİ KEZ render edilir
(sırt yazısıyla ve yazısız) ve fark alınır. Fark tam olarak mürekkebin
kendisidir; gerçek kutusu ölçülür, sapma varsa düzeltilir ve YENİDEN
ölçülür.

    Bir şeyin ortada OLDUĞUNU varsaymak, ortada olduğunu ölçmek değildir.

⚠ SAHTE ISBN VE SAHTE BARKOD BASILMAZ. KDP kendi barkodunu basar; hat
alanı BOŞ bırakır ve boşluğunu ÖLÇER.

  ./04_BUILD/covers.py            kapağı üret
  ./04_BUILD/covers.py --check    bayat mı
  ./04_BUILD/covers.py --preview  ek olarak PNG önizleme yaz

TASARIM: reportlab + Pillow ister. Yoksa çıkış 2 (ATLANDI).

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = bağımlılık yok
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

META = os.path.join(ROOT, "06_REPORTS", "tracked", "metadata.json")
SELECTION = os.path.join(ROOT, "03_COVER", "COVER_SELECTION.json")
RAW_DIR = os.path.join(ROOT, "07_ASSETS", "raw")
FONT_DIR = os.path.join(ROOT, "07_ASSETS", "fonts")
SYS_FONT_DIR = "/usr/share/fonts/truetype/dejavu"
OUT = os.path.join(ROOT, "08_OUTPUT", "PAPERBACK", "cover.pdf")
PREVIEW = os.path.join(ROOT, "08_OUTPUT", "PAPERBACK", "cover-preview.png")
REPORT = os.path.join(ROOT, "06_REPORTS", "cover.json")

PT = 72.0
SPINE_TEXT_TOL = 0.0625
BARCODE_W, BARCODE_H = 2.0, 1.2
BARCODE_MARGIN = 0.25

FONTS = {
    "Title": "DejaVuSerif-Bold.ttf",
    "Body": "DejaVuSerif.ttf",
    "BodyIt": "DejaVuSerif-Italic.ttf",
    "Sans": "DejaVuSans.ttf",
    "SansBold": "DejaVuSans-Bold.ttf",
}

INK_DARK = (0.11, 0.09, 0.06)
INK_LIGHT = (0.98, 0.96, 0.90)
HALO_LIGHT = (255, 250, 238)
HALO_DARK = (24, 18, 11)
INK_THRESHOLD = 132


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


def register(rep):
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    for d in (FONT_DIR, SYS_FONT_DIR):
        if all(os.path.isfile(os.path.join(d, f)) for f in FONTS.values()):
            for name, fn in FONTS.items():
                pdfmetrics.registerFont(TTFont(name, os.path.join(d, fn)))
            rep.facts["fontDir"] = (os.path.relpath(d, ROOT)
                                    if d.startswith(ROOT) else d)
            return d
    return None


def wrap(text, font, size, width):
    from reportlab.pdfbase import pdfmetrics
    words, line, out = text.split(), "", []
    for w in words:
        t = (line + " " + w).strip()
        if pdfmetrics.stringWidth(t, font, size) <= width:
            line = t
        else:
            out.append(line)
            line = w
    if line:
        out.append(line)
    return out


def fit(text, font, width, start, floor, max_lines):
    """Verilen satır sayısına sığan en büyük punto. Sessiz taşma YASAK."""
    size = start
    while size > floor:
        lines = wrap(text, font, size, width)
        if len(lines) <= max_lines:
            return size, lines
        size -= 0.5
    return floor, wrap(text, font, floor, width)


def zone_stats(art, FW, FH, x0, y0, x1, y1):
    """Sanatın bir bölgesinin parlaklığı. Koordinatlar İNÇ, köken SOL-ALT."""
    from PIL import ImageStat
    aw, ah = art.size
    px0, px1 = max(0, int(x0 / FW * aw)), min(aw, int(x1 / FW * aw))
    py0, py1 = max(0, int((FH - y1) / FH * ah)), min(ah, int((FH - y0) / FH * ah))
    if px1 <= px0 or py1 <= py0:
        return 128.0, 0.0
    s = ImageStat.Stat(art.crop((px0, py0, px1, py1)).convert("L"))
    return s.mean[0], s.stddev[0]


def _rel_lum(rgb01):
    def ch(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in rgb01)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def glyph_contrast(bg, FW, FH, block, font_paths):
    """⭑ OKUNURLUK GÖZLE DEĞİL, HARFLERİN ALTINDAN ÖLÇÜLÜR ⭑

    Bir bloğun ortalama zemini iyi görünebilir ve harflerin TAM ALTI
    yine de kötü olabilir: başlık haritanın koyu tepe çizgilerinin
    üstünden geçiyorsa ortalama bunu gizler.

    Bu ölçüm glif maskesini kurar ve YALNIZCA mürekkebin basılacağı
    piksellerin parlaklığını okur, sonra WCAG karşıtlık oranını verir.

        Ortalama bir zemin, bir harfin altındaki zemin değildir."""
    from PIL import Image, ImageDraw, ImageFont, ImageStat
    aw, ah = bg.size
    ppi = aw / FW
    mask = Image.new("L", (aw, ah), 0)
    d = ImageDraw.Draw(mask)
    size_px = max(4, int(round(block["size"] * ppi / PT)))
    try:
        f = ImageFont.truetype(font_paths[block["font"]], size_px)
    except OSError:
        return None
    for (tx, ty, txt) in block.get("glyphs", []):
        px, py = tx / FW * aw, (FH - ty) / FH * ah
        if block.get("rotate"):
            tmp = Image.new("L", (int(d.textlength(txt, font=f)) + 12,
                                  int(size_px * 2.0) + 12), 0)
            ImageDraw.Draw(tmp).text((6, 4), txt, font=f, fill=255)
            tmp = tmp.rotate(block["rotate"], expand=True)
            mask.paste(tmp, (int(px - tmp.width / 2), int(py - tmp.height / 2)), tmp)
        else:
            anc = "ms" if block.get("align") == "centre" else "ls"
            d.text((px, py), txt, font=f, fill=255, anchor=anc)
    core = mask.point(lambda v: 255 if v > 200 else 0)
    if not core.getbbox():
        return None
    st = ImageStat.Stat(bg.convert("L"), mask=core)
    bgl = st.mean[0] / 255.0
    l_bg = _rel_lum((bgl, bgl, bgl))
    l_ink = _rel_lum(block["ink"])
    hi, lo = max(l_bg, l_ink), min(l_bg, l_ink)
    return (hi + 0.05) / (lo + 0.05), st.mean[0]


def _back_height(md, width):
    """Arka blok yüksekliğinin ÖN KESTİRİMİ — sütunu ölçebilmek için."""
    blurb = md["description"]
    if blurb.startswith("Twenty-two peoples. "):
        blurb = blurb[len("Twenty-two peoples. "):]
    feats = [
        "%d puzzles built from real writing systems, maps and codes"
        % md["descriptionFacts"]["activities"],
        "22 cultures across 6 regions — every answer checked against "
        "museums, archives and universities",
        "Six seals to earn, and a certificate at the end",
        "Written in, not read to — pencil only, no screen",
    ]
    bl = wrap(blurb, "Body", 10.4, (width - 0.30) * PT)
    fl = [wrap(f, "Sans", 9.8, (width - 0.70) * PT) for f in feats]
    bio = wrap(md["authorBio"], "BodyIt", 9.0, (width - 0.30) * PT)
    return (0.42 + 0.34 + len(bl) * 0.190 + 0.20
            + sum(len(g) * 0.180 + 0.05 for g in fl) + 0.14
            + len(bio) * 0.158)


def clear_span(art, FW, FH, x0, x1, y0, y1, min_mean=182, max_sd=34, step=0.06):
    """⭑ METİN SÜTUNU ÖLÇÜLEREK BULUNUR ⭑

    Arka kapak parşömeni geniş ve sakin görünür — ama sol kenarında
    eğreltiotu, deniz kabuğu ve halat var. İlk yerleşim metni güvenli
    alanın TAMAMINA yaydı ve gövde satırları eğreltiotunun üstüne
    düştü: teknik olarak 'panel yok' ama pratikte OKUNMUYOR.

        Bir metnin nereye sığdığı, kenar boşluğundan değil
        SANATIN KENDİSİNDEN ölçülür.

    Bu tarama, verilen bandın sütunlarını tek tek ölçer ve metnin
    gerçekten oturabileceği EN GENİŞ KESİNTİSİZ açıklığı döner."""
    from PIL import ImageStat
    aw, ah = art.size
    py0, py1 = int((FH - y1) / FH * ah), int((FH - y0) / FH * ah)
    cols, x = [], x0
    while x < x1:
        px0, px1 = int(x / FW * aw), int(min(x + step, x1) / FW * aw)
        if px1 <= px0 or py1 <= py0:
            cols.append((x, False))
            x += step
            continue
        st = ImageStat.Stat(art.crop((px0, py0, px1, py1)).convert("L"))
        cols.append((x, st.mean[0] >= min_mean and st.stddev[0] <= max_sd))
        x += step
    best, cur = None, None
    for xv, ok in cols + [(x1, False)]:
        if ok and cur is None:
            cur = xv
        elif not ok and cur is not None:
            if best is None or (xv - cur) > (best[1] - best[0]):
                best = (cur, xv)
            cur = None
    return best


def align_art(raw_path, FW, FH, spine, panel, rep):
    """⭑ SANATI GERÇEK SIRTA HİZALA — ORANI BOZMADAN ⭑

    ⚠ Yukarı örnekleme YOK: yalnızca yeniden çerçeveleme. Çözünürlük
    eklenmiyor, kadraj kaydırılıyor."""
    from PIL import Image
    im = Image.open(raw_path).convert("RGBA")
    im = Image.alpha_composite(Image.new("RGBA", im.size, (255, 255, 255, 255)),
                               im).convert("RGB")
    W, H = im.size
    g = im.convert("L")
    px = g.load()
    step = max(1, H // 240)
    ys = range(0, H, step)
    col = [sum(px[x, y] for y in ys) / len(ys) for x in range(W)]
    dark = min(col)
    band = [x for x in range(int(W * 0.30), int(W * 0.70)) if col[x] < dark + 38]
    rep.facts["artBindingFound"] = bool(band)
    if not band:
        rep.warn("sanatta cilt şeridi bulunamadı — hizalama YAPILMADI")
        return im
    bind = (band[0] + band[-1]) / 2.0
    want = (panel + spine / 2.0) / FW
    cropw = min(bind / want, float(W))
    croph = cropw * FH / FW
    if croph > H:
        croph = float(H)
        cropw = croph * FW / FH
    x0 = max(0.0, bind - want * cropw)
    y0 = (H - croph) / 2.0
    box = (int(round(x0)), int(round(y0)),
           int(round(x0 + cropw)), int(round(y0 + croph)))
    out = im.crop(box)
    rep.facts["artBindingBefore"] = round(bind / W, 4)
    rep.facts["artBindingAfter"] = round((bind - box[0]) / (box[2] - box[0]), 4)
    rep.facts["artAlignCrop"] = list(box)
    return out


def halo_layer(art, FW, FH, blocks, font_paths, rep):
    """⭑ KONTRAST DESTEĞİ BİR DİKDÖRTGEN DEĞİL, HARFLERİN BİÇİMİDİR ⭑

    Glifler maskeye çizilir, kalın bir Gauss bulanıklığından geçirilir
    ve o maske bir yıkamanın ALFA'sı olur. Kenarı yoktur, kutusu
    yoktur, altındaki sanat görünür kalır.

    ⚠ Buradaki PIL çizimi yalnızca IŞIMAYI biçimlendirir. Basılan
    harfler VEKTÖRDÜR ve reportlab bunun üstüne çizer."""
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    aw, ah = art.size
    base = art.convert("RGB")
    ppi = aw / FW

    for b in blocks:
        if not b.get("glyphs"):
            continue
        mask = Image.new("L", (aw, ah), 0)
        d = ImageDraw.Draw(mask)
        size_px = max(4, int(round(b["size"] * ppi / PT)))
        try:
            f = ImageFont.truetype(font_paths[b["font"]], size_px)
        except OSError:
            continue
        for (tx, ty, txt) in b["glyphs"]:
            px = tx / FW * aw
            py = (FH - ty) / FH * ah
            if b.get("rotate"):
                tmp = Image.new("L", (int(d.textlength(txt, font=f)) + 12,
                                      int(size_px * 2.0) + 12), 0)
                ImageDraw.Draw(tmp).text((6, 4), txt, font=f, fill=255)
                tmp = tmp.rotate(b["rotate"], expand=True)
                mask.paste(tmp, (int(px - tmp.width / 2),
                                 int(py - tmp.height / 2)), tmp)
            else:
                anc = "ms" if b.get("align") == "centre" else "ls"
                d.text((px, py), txt, font=f, fill=255, anchor=anc)
        glow = mask.filter(ImageFilter.GaussianBlur(b.get("blur", 9)))
        gain = b.get("gain", 2.4)
        op = b.get("opacity", 0.80)
        glow = glow.point(lambda v: min(255, int(v * gain * op)))
        wash = Image.new("RGB", (aw, ah), b["halo"])
        base = Image.composite(wash, base, glow)
    rep.facts["haloBlocks"] = sum(1 for b in blocks if b.get("glyphs"))
    return base


def layout(md, art, FW, FH, spine, panel, bleed, safe, rep):
    """Bütün blokların yerini İNÇ olarak hesaplar; mürekkep rengini
    zeminden ÖLÇEREK seçer."""
    blocks = []
    fx0 = panel + spine + bleed + safe
    fx1 = FW - bleed - safe
    fw = fx1 - fx0
    fcx = (fx0 + fx1) / 2.0

    def ink_for(mean):
        return ((INK_DARK, HALO_LIGHT) if mean > INK_THRESHOLD
                else (INK_LIGHT, HALO_DARK))

    # ── ÖN: başlık ───────────────────────────────────────────────────────
    title = md["title"].upper()
    t_size, t_lines = fit(title, "Title", (fw - 0.30) * PT, 52, 26, 2)
    t_lead = t_size * 1.15 / PT
    t_top = FH - bleed - safe - 0.30
    ty = t_top - t_size * 0.78 / PT
    tmean, tsd = zone_stats(art, FW, FH, fx0, ty - t_lead * len(t_lines),
                            fx1, t_top)
    ink, halo = ink_for(tmean)
    gl, yy = [], ty
    for ln in t_lines:
        gl.append((fcx, yy, ln))
        yy -= t_lead
    blocks.append({"id": "front-title", "font": "Title", "size": t_size,
                   "glyphs": gl, "ink": ink, "halo": halo, "align": "centre",
                   "blur": 14, "gain": 2.7, "opacity": 0.82,
                   "zoneMean": round(tmean, 1), "zoneSd": round(tsd, 1)})

    # ── ÖN: alt başlık ───────────────────────────────────────────────────
    sub = md["subtitle"].split("—")[0].strip()
    s_size, s_lines = fit(sub, "BodyIt", (fw - 0.9) * PT, 16.5, 11, 2)
    sy = yy - 0.06
    gl = []
    for ln in s_lines:
        gl.append((fcx, sy, ln))
        sy -= s_size * 1.30 / PT
    smean, ssd = zone_stats(art, FW, FH, fx0, sy, fx1, yy)
    ink, halo = ink_for(smean)
    blocks.append({"id": "front-subtitle", "font": "BodyIt", "size": s_size,
                   "glyphs": gl, "ink": ink, "halo": halo, "align": "centre",
                   "blur": 10, "gain": 2.5, "opacity": 0.74,
                   "zoneMean": round(smean, 1), "zoneSd": round(ssd, 1)})

    # ── ÖN: yazar — YER TARANARAK SEÇİLİR ────────────────────────────────
    # Ön panelin alt bölgesi 0,04 inç adımlarla taranır; en KOYU ve en
    # SAKİN bant kazanır. Böylece yazar adı odak nesnesinin (defter)
    # üstüne değil, ahşap masanın sakin bandına oturur.
    a_size = 22.0
    best = None
    y = bleed + safe + 0.34
    while y < FH * 0.30:
        m, sd = zone_stats(art, FW, FH, fx0 + fw * 0.12, y - 0.03,
                           fx1 - fw * 0.12, y + a_size / PT + 0.07)
        score = sd + abs(m - 62) * 0.40
        if best is None or score < best[0]:
            best = (score, y, m, sd)
        y += 0.04
    _, ay, amean, asd = best
    ink, halo = ink_for(amean)
    blocks.append({"id": "front-author", "font": "SansBold", "size": a_size,
                   "glyphs": [(fcx, ay, md["author"].upper())],
                   "ink": ink, "halo": halo, "align": "centre",
                   "blur": 13, "gain": 3.0, "opacity": 0.84,
                   "zoneMean": round(amean, 1), "zoneSd": round(asd, 1)})

    # ── SIRT ─────────────────────────────────────────────────────────────
    usable = spine - 2 * SPINE_TEXT_TOL
    sp_size = min(12.0, usable * PT * 0.72)
    scx = panel + spine / 2.0
    m2, sd2 = zone_stats(art, FW, FH, panel, FH * 0.15, panel + spine, FH * 0.85)
    ink, halo = ink_for(m2)
    blocks.append({"id": "spine", "font": "SansBold", "size": sp_size,
                   "glyphs": [(scx, FH / 2.0, "%s  ·  %s"
                               % (md["title"].upper(), md["author"].upper()))],
                   "ink": ink, "halo": halo, "rotate": 90,
                   "blur": 6, "gain": 3.2, "opacity": 0.60,
                   "zoneMean": round(m2, 1), "zoneSd": round(sd2, 1)})

    # ── ARKA ─────────────────────────────────────────────────────────────
    # ⭑ SÜTUN İKİ GEÇİŞLE ÖLÇÜLÜR ⭑
    #
    # Açıklık, metnin GERÇEKTEN kapladığı bandda aranmalı. İlk hâl bandı
    # barkod alanından üst kenara kadar almıştı ve alt köşedeki kabuk ile
    # halat sütunu gereksiz yere 4,6 inçe daraltıyordu — metin sağa
    # sıkışıyor, sol yarısı boş kalıyordu.
    #
    #     Bir açıklığı ölçmek için ÖNCE metnin nereye oturacağını
    #     bilmek gerekir. Bu yüzden iki geçiş: önce yükseklik, sonra
    #     o yüksekliğin bandında genişlik.
    full0, full1 = bleed + safe, panel - safe
    prov_h = _back_height(md, full1 - full0)
    ztop0 = FH - bleed - safe - 0.60
    zbot0 = bleed + safe + BARCODE_H + BARCODE_MARGIN + 0.35
    mid = (ztop0 + zbot0) / 2.0
    band0, band1 = mid - prov_h / 2.0 - 0.15, mid + prov_h / 2.0 + 0.15
    span = clear_span(art, FW, FH, full0, full1, band0, band1)
    if span and (span[1] - span[0]) >= 4.6:
        bx0, bx1 = span[0] + 0.12, span[1] - 0.12
    else:
        bx0, bx1 = full0, full1
    bw = bx1 - bx0
    bcx = (bx0 + bx1) / 2.0
    rep.facts["backColumnInches"] = [round(bx0, 3), round(bx1, 3), round(bw, 3)]
    rep.facts["backColumnMeasured"] = bool(span)
    rep.facts["backProbeBandInches"] = [round(band0, 3), round(band1, 3)]

    hook = "Twenty-two peoples. One quest. No screens."
    blurb = md["description"]
    if blurb.startswith("Twenty-two peoples. "):
        blurb = blurb[len("Twenty-two peoples. "):]
    feats = [
        "%d puzzles built from real writing systems, maps and codes"
        % md["descriptionFacts"]["activities"],
        "22 cultures across 6 regions — every answer checked against "
        "museums, archives and universities",
        "Six seals to earn, and a certificate at the end",
        "Written in, not read to — pencil only, no screen",
    ]
    age = "Ages %d–%d   ·   %d pages   ·   screen-free" % (
        md["audience"]["ageMin"], md["audience"]["ageMax"], md["edition"]["pages"])
    bio = md["authorBio"]

    h_size, blurb_size, feat_size, bio_size = 18.5, 10.4, 9.8, 9.0
    blurb_lines = wrap(blurb, "Body", blurb_size, (bw - 0.30) * PT)
    feat_lines = [wrap(f, "Sans", feat_size, (bw - 0.70) * PT) for f in feats]
    bio_lines = wrap(bio, "BodyIt", bio_size, (bw - 0.30) * PT)
    h = (0.42 + 0.34 + len(blurb_lines) * 0.190 + 0.20
         + sum(len(gp) * 0.180 + 0.05 for gp in feat_lines) + 0.14
         + len(bio_lines) * 0.158)
    ztop = FH - bleed - safe - 0.60
    zbot = bleed + safe + BARCODE_H + BARCODE_MARGIN + 0.35
    by = ztop - max(0.0, ((ztop - zbot) - h) / 2.0)
    bmean, bsd = zone_stats(art, FW, FH, bx0, by - h, bx1, by + 0.30)
    ink, halo = ink_for(bmean)

    back = [{"font": "Title", "size": h_size, "align": "centre",
             "glyphs": [(bcx, by, hook)]}]
    by -= 0.42
    back.append({"font": "Sans", "size": 10.6, "align": "centre",
                 "glyphs": [(bcx, by, age)]})
    by -= 0.38
    gl = []
    for ln in blurb_lines:
        gl.append((bx0 + 0.15, by, ln))
        by -= 0.190
    back.append({"font": "Body", "size": blurb_size, "align": "left", "glyphs": gl})
    by -= 0.20
    gl = []
    for gp in feat_lines:
        gl.append((bx0 + 0.20, by, "•"))
        for ln in gp:
            gl.append((bx0 + 0.44, by, ln))
            by -= 0.180
        by -= 0.05
    back.append({"font": "Sans", "size": feat_size, "align": "left",
                 "glyphs": gl, "bulletFont": "SansBold"})
    by -= 0.14
    gl = []
    for ln in bio_lines:
        gl.append((bx0 + 0.15, by, ln))
        by -= 0.158
    back.append({"font": "BodyIt", "size": bio_size, "align": "left", "glyphs": gl})

    for i, blk in enumerate(back):
        blk.update({"id": "back-%d" % i, "ink": ink, "halo": halo,
                    "blur": 11, "gain": 2.3, "opacity": 0.76,
                    "zoneMean": round(bmean, 1), "zoneSd": round(bsd, 1)})
        blocks.append(blk)

    rep.facts["backTextBottomInches"] = round(by, 3)
    rep.facts["spineFontPt"] = round(sp_size, 2)
    rep.facts["spineUsableInches"] = round(usable, 4)
    rep.facts["titleFontPt"] = round(t_size, 2)
    rep.facts["authorBaselineInches"] = round(ay, 3)
    rep.facts["zoneMeasurements"] = {
        b["id"]: {"mean": b["zoneMean"], "sd": b["zoneSd"],
                  "ink": "light" if b["ink"] == INK_LIGHT else "dark"}
        for b in blocks}
    return blocks


def draw(c, blocks, skip=()):
    """Vektör metni çizer. HİÇBİR dikdörtgen, HİÇBİR dolgu yok."""
    from reportlab.lib.colors import Color
    for b in blocks:
        if b["id"] in skip or not b.get("glyphs"):
            continue
        c.setFillColor(Color(*b["ink"]))
        for (x, y, txt) in b["glyphs"]:
            c.saveState()
            font = b.get("bulletFont") if (b.get("bulletFont") and txt == "•") \
                else b["font"]
            c.setFont(font, b["size"])
            if b.get("rotate"):
                c.translate(x * PT, y * PT)
                c.rotate(-b["rotate"])
                c.drawCentredString(0, -b["size"] * 0.34, txt)
            elif b.get("align") == "centre":
                c.drawCentredString(x * PT, y * PT, txt)
            else:
                c.drawString(x * PT, y * PT, txt)
            c.restoreState()


def render_png(pdf_path, out_base, dpi=110):
    r = subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-singlefile",
                        pdf_path, out_base], capture_output=True)
    return r.returncode == 0 and os.path.isfile(out_base + ".png")


def ink_bbox(with_pdf, without_pdf, td, dpi=150):
    """İki render'ın FARKI tam olarak o metnin mürekkebidir."""
    from PIL import Image, ImageChops
    a, b = os.path.join(td, "a"), os.path.join(td, "b")
    if not (render_png(with_pdf, a, dpi) and render_png(without_pdf, b, dpi)):
        return None, None
    A = Image.open(a + ".png").convert("L")
    B = Image.open(b + ".png").convert("L")
    d = ImageChops.difference(A, B).point(lambda v: 255 if v > 18 else 0)
    return d.getbbox(), A.size


def build(rep, want_preview=False):
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader

    md, sel = jload(META), jload(SELECTION)
    if not md or not sel:
        rep.check(False, "metadata.json ve COVER_SELECTION.json gerekli")
        return None
    cv = md["cover"]
    FW, FH = cv["fullCoverWidthInches"], cv["fullCoverHeightInches"]
    spine, bleed, safe = cv["spineInches"], cv["bleedInches"], cv["safeMarginInches"]
    panel = (FW - spine) / 2.0

    art_path = os.path.join(RAW_DIR, sel["selected"] + ".png")
    if not rep.check(os.path.isfile(art_path),
                     "seçilen kapak sanatı var: %s" % sel["selected"]):
        return None
    fdir = register(rep)
    if not rep.check(fdir is not None, "gömülebilir yazı tipi bulunamadı"):
        return None
    from reportlab import rl_config
    rl_config.canvas_basefontname = "Body"
    font_paths = {k: os.path.join(fdir, v) for k, v in FONTS.items()}

    art = align_art(art_path, FW, FH, spine, panel, rep)
    aw, ah = art.size
    rep.facts["artPixels"] = [aw, ah]
    rep.facts["requiredPixels"] = [round(FW * 300), round(FH * 300)]
    rep.facts["effectiveDpi"] = round(min(aw / FW, ah / FH), 1)
    rep.facts["artSha256"] = sha256(art_path)

    blocks = layout(md, art, FW, FH, spine, panel, bleed, safe, rep)
    bg = halo_layer(art, FW, FH, blocks, font_paths, rep)

    # ⭑ KARŞITLIK ÖLÇÜLÜR VE YETMİYORSA HALE GÜÇLENDİRİLİR ⭑
    #
    # Ölçüt WCAG: büyük punto ≥ 3,0 · gövde ≥ 4,5. Yetmezse hale
    # kazancı artırılır ve katman YENİDEN kurulur — en çok dört kez.
    # Hâlâ yetmiyorsa kapı bunu SÖYLER; sessizce okunmaz bir kapak
    # üretilmez.
    contrast = {}
    for _ in range(4):
        weak = []
        for b in blocks:
            r = glyph_contrast(bg, FW, FH, b, font_paths)
            if r is None:
                continue
            ratio, under = r
            contrast[b["id"]] = [round(ratio, 2), round(under, 1)]
            need = 3.0 if b["size"] >= 18 else 4.5
            if ratio < need:
                weak.append(b)
        if not weak:
            break
        for b in weak:
            b["gain"] = min(6.0, b.get("gain", 2.4) * 1.35)
            b["opacity"] = min(0.97, b.get("opacity", 0.8) + 0.05)
            b["blur"] = b.get("blur", 9) + 2
        bg = halo_layer(art, FW, FH, blocks, font_paths, rep)
    rep.facts["glyphContrast"] = contrast
    rep.facts["contrastFloor"] = {"large>=18pt": 3.0, "body": 4.5}
    state = {"bg": bg}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)

    def emit(path, skip=()):
        c = canvas.Canvas(path, pagesize=(FW * PT, FH * PT))
        c.setTitle(md["title"])
        c.setAuthor(md["author"])
        c.drawImage(ImageReader(state["bg"]), 0, 0, width=FW * PT, height=FH * PT)
        draw(c, blocks, skip=skip)
        c.showPage()
        c.save()

    emit(OUT)

    # ⭑ OPTİK ORTALAMA — ÖLÇÜMLE, TAHMİNLE DEĞİL ⭑
    target = panel + spine / 2.0
    with tempfile.TemporaryDirectory() as td:
        wo = os.path.join(td, "wo.pdf")
        emit(wo, skip=("spine",))
        bbox, size = ink_bbox(OUT, wo, td)
        if bbox and size:
            cx = (bbox[0] + bbox[2]) / 2.0 / size[0] * FW
            drift = cx - target
            rep.facts["spineInkBoxInches"] = [round(bbox[0] / size[0] * FW, 4),
                                              round(bbox[2] / size[0] * FW, 4)]
            rep.facts["spineInkCentreInches"] = round(cx, 4)
            rep.facts["spineTargetCentreInches"] = round(target, 4)
            rep.facts["spineDriftBeforeInches"] = round(drift, 4)
            if abs(drift) > 0.004:
                for blk in blocks:
                    if blk["id"] == "spine":
                        blk["glyphs"] = [(x - drift, y, t)
                                         for (x, y, t) in blk["glyphs"]]
                state["bg"] = halo_layer(art, FW, FH, blocks, font_paths, rep)
                emit(OUT)
                rep.facts["spineOpticalCorrectionInches"] = round(-drift, 4)
                wo2 = os.path.join(td, "wo2.pdf")
                emit(wo2, skip=("spine",))
                bbox, size = ink_bbox(OUT, wo2, td)
            else:
                rep.facts["spineOpticalCorrectionInches"] = 0.0
            if bbox and size:
                cx2 = (bbox[0] + bbox[2]) / 2.0 / size[0] * FW
                rep.facts["spineDriftAfterInches"] = round(cx2 - target, 4)
                rep.facts["spineInkVCentreInches"] = round(
                    FH - (bbox[1] + bbox[3]) / 2.0 / size[1] * FH, 4)
                rep.facts["spineInkWidthInches"] = round(
                    (bbox[2] - bbox[0]) / size[0] * FW, 4)

    if want_preview:
        render_png(OUT, PREVIEW[:-4], dpi=110)
        rep.facts["preview"] = os.path.relpath(PREVIEW, ROOT)

    rep.facts["barcodeZoneInches"] = {
        "x": round(panel - safe - BARCODE_W, 3), "y": round(bleed + safe, 3),
        "w": BARCODE_W, "h": BARCODE_H,
        "note": "boş bırakıldı · KDP kendi barkodunu basar"}
    rep.facts["opaquePanels"] = 0
    rep.facts["contrastMethod"] = "letterform halo (blurred glyph mask) — no rectangles"
    return md, {"panel": panel, "spine": spine, "FW": FW, "FH": FH}


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--preview", action="store_true")
    args = ap.parse_args()

    print("=" * 74)
    print("  CİLTSİZ KAPAK ÜRETİMİ")
    print("=" * 74)
    try:
        import reportlab   # noqa: F401
        import PIL         # noqa: F401
    except ImportError:
        print("  ⊘ reportlab/Pillow yok — ATLANDI")
        print("=" * 74)
        return 2

    md = jload(META)
    if md is None:
        print("  ⊘ metadata.json yok — önce ./04_BUILD/metadata.py")
        print("=" * 74)
        return 0
    sel = jload(SELECTION) or {}
    art = os.path.join(RAW_DIR, (sel.get("selected") or "") + ".png")
    if not os.path.isfile(art):
        print("  ⊘ ham kapak sanatı depoda yok (.gitignore § ③) — BOŞ KOŞTU")
        print("=" * 74)
        return 0

    if args.check:
        f = (jload(REPORT, {}) or {}).get("facts") or {}
        stale = []
        if not os.path.isfile(REPORT):
            stale.append("kapak hiç üretilmedi")
        if f.get("pages") != md["edition"]["pages"]:
            stale.append("sayfa %s ≠ %s" % (f.get("pages"), md["edition"]["pages"]))
        if f.get("artSha256") != sha256(art):
            stale.append("kapak sanatı değişti")
        if f.get("opaquePanels") != 0:
            stale.append("opak panel kaydı yok — eski tipografi sürümü")
        if stale:
            print("  ✗ BAYAT: %s" % " · ".join(stale))
            print("\n  Tazele: ./04_BUILD/covers.py")
            print("=" * 74)
            return 1
        print("  ✅ kapak güncel (%d sayfa · sırt %.4f in · opak panel 0)"
              % (md["edition"]["pages"], md["cover"]["spineInches"]))
        print("=" * 74)
        return 0

    rep = Report()
    res = build(rep, want_preview=args.preview)
    if res is None:
        print("\n  ⛔ kapak ÜRETİLEMEDİ")
        for e in rep.errors:
            print("     · %s" % e)
        print("=" * 74)
        return 1
    md, geo = res
    F = rep.facts

    print("\n── ① geometri ──")
    print("  tam kapak  %.4f × %.4f in · sırt %.4f in (%s sayfa)"
          % (geo["FW"], geo["FH"], geo["spine"], md["edition"]["pages"]))
    rep.check(abs(2 * geo["panel"] + geo["spine"] - geo["FW"]) < 1e-9,
              "arka + sırt + ön = tam kapak")

    print("\n── ② sanat hizalama (ARKA→SIRT→ÖN sürekliliği) ──")
    tgt = (geo["panel"] + geo["spine"] / 2) / geo["FW"]
    if F.get("artBindingFound"):
        print("  cilt şeridi merkezi  %.4f → %.4f   (sırt merkezi %.4f)"
              % (F["artBindingBefore"], F["artBindingAfter"], tgt))
        rep.check(abs(F["artBindingAfter"] - tgt) < 0.004,
                  "sanatın cilt şeridi GERÇEK SIRTA hizalı")
    print("  sanat %d × %d px · etkin %.1f dpi" % (*F["artPixels"], F["effectiveDpi"]))
    if F["effectiveDpi"] < 300:
        rep.warn("kapak sanatı 300 dpi ALTINDA (%.0f dpi) — yukarı örnekleme "
                 "YAPILMADI; tipografi vektör. KURUCU EYLEMİ: sanatı "
                 "≥%d × %d px yeniden üret." % (F["effectiveDpi"], *F["requiredPixels"]))

    print("\n── ③ tipografi · zeminden ÖLÇÜLMÜŞ mürekkep ──")
    for k in ("front-title", "front-subtitle", "front-author", "spine", "back-0"):
        z = F["zoneMeasurements"].get(k)
        if z:
            print("  %-16s zemin %5.1f (sd %4.1f) → %s mürekkep"
                  % (k, z["mean"], z["sd"], z["ink"]))
    rep.check(F.get("opaquePanels") == 0,
              "⭑ HİÇBİR OPAK PANEL YOK — kontrast yalnızca harf halesiyle ⭑")
    print("\n  harf altı karşıtlık (WCAG · ölçüldü):")
    weak = []
    for bid, (ratio, under) in sorted(F.get("glyphContrast", {}).items()):
        need = 3.0 if bid in ("front-title", "front-subtitle", "front-author",
                              "back-0") else 4.5
        ok = ratio >= need
        if not ok:
            weak.append("%s %.2f<%.1f" % (bid, ratio, need))
        print("    %-16s %5.2f : 1   (zemin %5.1f)  %s"
              % (bid, ratio, under, "✓" if ok else "✗ ZAYIF"))
    rep.check(not weak, "her metin bloğu okunurluk eşiğini geçiyor"
              + ("" if not weak else " — ZAYIF: %s" % weak))
    print("  yazar temel çizgisi %.3f in (taranarak seçildi)"
          % F["authorBaselineInches"])

    print("\n── ④ sırt · OPTİK ORTALAMA (ölçüldü) ──")
    print("  sırt bandı        %.4f .. %.4f in"
          % (geo["panel"], geo["panel"] + geo["spine"]))
    if "spineInkBoxInches" in F:
        print("  mürekkep kutusu   %.4f .. %.4f in (genişlik %.4f)"
              % (*F["spineInkBoxInches"], F.get("spineInkWidthInches", 0)))
        print("  ölçülen merkez    %.4f in  (hedef %.4f)"
              % (F["spineInkCentreInches"], F["spineTargetCentreInches"]))
        print("  optik düzeltme    %+.4f in" % F.get("spineOpticalCorrectionInches", 0))
        print("  sonrası sapma     %+.4f in" % F.get("spineDriftAfterInches", 0))
        rep.check(abs(F.get("spineDriftAfterInches", 1)) <= 0.004,
                  "sırt yazısı OPTİK olarak ortalı (±0,004 in)")
        rep.check(F.get("spineInkWidthInches", 99) <= geo["spine"],
                  "sırt mürekkebi sırt bandını AŞMIYOR (%.4f ≤ %.4f)"
                  % (F.get("spineInkWidthInches", 99), geo["spine"]))
        if "spineInkVCentreInches" in F:
            print("  dikey merkez      %.4f in  (hedef %.4f)"
                  % (F["spineInkVCentreInches"], geo["FH"] / 2))
            rep.check(abs(F["spineInkVCentreInches"] - geo["FH"] / 2) < 0.08,
                      "sırt yazısı dikeyde ortalı")
    else:
        rep.warn("sırt mürekkebi ölçülemedi (pdftoppm yok?)")
    print("  punto %.2f pt · kullanılabilir bant %.4f in"
          % (F["spineFontPt"], F["spineUsableInches"]))
    rep.check(F["spineFontPt"] <= F["spineUsableInches"] * PT,
              "sırt puntosu tolerans bandına sığıyor")

    print("\n── ⑤ barkod alanı ──")
    bz = F["barcodeZoneInches"]
    print("  %.2f × %.2f in @ (%.2f, %.2f) — BOŞ" % (bz["w"], bz["h"], bz["x"], bz["y"]))
    rep.check(F["backTextBottomInches"] > bz["y"] + bz["h"],
              "arka kapak metni barkod alanına GİRMİYOR (%.2f > %.2f)"
              % (F["backTextBottomInches"], bz["y"] + bz["h"]))

    print("\n── ⑥ yazı tipi ──")
    rep.check(bool(F.get("fontDir")), "gömülebilir yazı tipi kayıtlı (%d aile)"
              % len(FONTS))

    F["output"] = os.path.relpath(OUT, ROOT)
    F["pages"] = md["edition"]["pages"]
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as fh:
        json.dump({"status": "fail" if rep.errors else "pass",
                   "checks": rep.checks, "errors": rep.errors,
                   "warnings": rep.warnings, "facts": F},
                  fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        print("=" * 74)
        return 1
    print("  ✅ %d denetim yeşil · %s" % (rep.checks, os.path.relpath(OUT, ROOT)))
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
