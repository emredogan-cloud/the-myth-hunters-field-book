#!/usr/bin/env python3
"""
CİLTSİZ KAPAK ÜRETİMİ — The Myth Hunter's Field Book
================================================================================
ARKA + SIRT + ÖN → **TEK PDF**. Tipografi VEKTÖR, yazı tipi GÖMÜLÜ.

⭑ SIRT BU DOSYADA HESAPLANMAZ ⭑

Sırt `metadata.py` tarafından SAYFA SAYISINDAN türetilir ve
`metadata.json § cover` içinde durur. Burada ikinci bir kopya tutmak,
ikisinin bir gün ayrışması demektir — ve ayrıştığı gün kapak YANLIŞ
SIRTLA basılır.

    sayfa sayısı → metadata.py → metadata.json → covers.py
                                                  ↑ BURADAN OKUR

⭑ PANEL ENLERİ ÇIKARILIR, HESAPLANMAZ ⭑

Her ölçüyü ayrı ayrı yuvarlamak 1 px açık bırakıyordu
(2588 + 108 + 2588 = 5284 ≠ 5283). Bir piksel bir hata gibi görünmez —
ta ki üç panel yan yana konup tuvalin dışına taşana kadar.

⭑ METİN GÖRSELE GÖMÜLMEZ, PDF'E ÇİZİLİR ⭑

Kurucu sanatı METİNSİZ teslim etti. Başlık, yazar ve arka kapak metni
burada VEKTÖR olarak basılır:

  · düzeltilebilir           — metadata değişirse yeniden üretilir
  · çözünürlükten bağımsız   — sanat 89 dpi olsa da metin keskin
  · metadata ile birebir     — panele girilecek başlıkla AYNI kaynak

⚠ SAHTE ISBN VE SAHTE BARKOD BASILMAZ. KDP kendi barkodunu arka kapağın
alt bölgesine kendisi basar; hat orayı BOŞ ve AÇIK bırakır ve boş
olduğunu ÖLÇER.

  ./04_BUILD/covers.py            kapağı üret
  ./04_BUILD/covers.py --check    üretilebilir mi · ölçüler tutuyor mu

TASARIM: reportlab + Pillow ister. Yoksa çıkış 2 (ATLANDI).

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

META = os.path.join(ROOT, "06_REPORTS", "tracked", "metadata.json")
SELECTION = os.path.join(ROOT, "03_COVER", "COVER_SELECTION.json")
RAW_DIR = os.path.join(ROOT, "07_ASSETS", "raw")
FONT_DIR = os.path.join(ROOT, "07_ASSETS", "fonts")
SYS_FONT_DIR = "/usr/share/fonts/truetype/dejavu"
OUT = os.path.join(ROOT, "08_OUTPUT", "PAPERBACK", "cover.pdf")
REPORT = os.path.join(ROOT, "06_REPORTS", "cover.json")

PT = 72.0
# KDP: sırt metni sırt kenarlarından en az 0,0625 in içeride kalmalı.
SPINE_TEXT_TOL = 0.0625
# KDP barkod alanı: 2,0 × 1,2 in. Kesin konum ŞABLONDAN doğrulanır;
# hat bu alanı boş bırakır ve boşluğunu ÖLÇER.
BARCODE_W, BARCODE_H = 2.0, 1.2
BARCODE_MARGIN = 0.25

FONTS = {
    "Title": "DejaVuSerif-Bold.ttf",
    "Body": "DejaVuSerif.ttf",
    "Sans": "DejaVuSans.ttf",
    "SansBold": "DejaVuSans-Bold.ttf",
}


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
            # mutlak yol rapora yazılmaz (bkz. interior.py)
            rep.facts["fontDir"] = (os.path.relpath(d, ROOT)
                                    if d.startswith(ROOT) else d)
            return True
    return False


def wrap(c, text, font, size, width):
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


def fit_lines(c, text, font, width, start, min_size, max_lines):
    """Metni verilen satır sayısına SIĞDIRAN en büyük puntoyu bulur.

    Sığmıyorsa taşırmaz, küçültür; tabana kadar sığmazsa taban döner ve
    çağıran ölçer. Sessiz taşma bir kapak hatasıdır."""
    size = start
    while size > min_size:
        lines = wrap(c, text, font, size, width)
        if len(lines) <= max_lines:
            return size, lines
        size -= 0.5
    return min_size, wrap(c, text, font, min_size, width)


def build(rep):
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    from reportlab.lib.colors import Color
    from PIL import Image

    md = jload(META)
    sel = jload(SELECTION)
    if not md or not sel:
        rep.check(False, "metadata.json ve COVER_SELECTION.json gerekli")
        return None

    cv = md["cover"]
    FW, FH = cv["fullCoverWidthInches"], cv["fullCoverHeightInches"]
    spine, bleed, safe = cv["spineInches"], cv["bleedInches"], cv["safeMarginInches"]
    panel = (FW - spine) / 2.0

    art_id = sel["selected"]
    art_path = os.path.join(RAW_DIR, art_id + ".png")
    if not rep.check(os.path.isfile(art_path), "seçilen kapak sanatı var: %s" % art_id):
        return None

    # ── gerçek çözünürlük ÖLÇÜLÜR ────────────────────────────────────────
    with Image.open(art_path) as im:
        aw, ah = im.size
    eff_dpi = min(aw / FW, ah / FH)
    rep.facts["artPixels"] = [aw, ah]
    rep.facts["requiredPixels"] = [round(FW * 300), round(FH * 300)]
    rep.facts["effectiveDpi"] = round(eff_dpi, 1)
    rep.facts["artSha256"] = sha256(art_path)

    if not register(rep):
        rep.check(False, "gömülebilir yazı tipi bulunamadı")
        return None
    # ⚠ Tuvalin VARSAYILAN yazı tipi de değiştirilmeli: reportlab
    # `rl_config.canvas_basefontname`i sayfa kaynak sözlüğüne HİÇ
    # KULLANILMASA DA yazar ve `pdffonts` gömülmemiş bir Helvetica
    # görür. İç blokta aynı kusur ölçülmüş ve düzeltilmişti.
    from reportlab import rl_config
    rl_config.canvas_basefontname = "Body"

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    c = canvas.Canvas(OUT, pagesize=(FW * PT, FH * PT))
    c.setTitle(md["title"])
    c.setAuthor(md["author"])

    # ① SANAT — tam bleed, tek parça, KENDİ çözünürlüğünde
    #
    # ⚠ YUKARI ÖRNEKLEME YAPILMAZ. Sanat 1569 px ve hedef 5283 px; aradaki
    # farkı piksel uydurarak kapatmak çözünürlük kazandırmaz, yalnızca
    # 300 dpi iddiasını YALAN hâline getirir. Gerçek dpi rapora yazılır.
    with Image.open(art_path) as im:
        flat = Image.new("RGB", im.size, (255, 255, 255))
        im = im.convert("RGBA")
        flat.paste(im, mask=im.split()[3])
    c.drawImage(ImageReader(flat), 0, 0, width=FW * PT, height=FH * PT)

    # koordinat yardımcıları (inç → punto, sol-alt köken)
    def X(inch):
        return inch * PT

    def Y(inch):
        return inch * PT

    back_x0, back_x1 = 0.0, panel
    front_x0, front_x1 = panel + spine, FW
    spine_x0, spine_x1 = panel, panel + spine

    def scrim(x0, y0, x1, y1, alpha=0.80, r=0.10):
        """Tipografi altlığı. Sanat metinsiz teslim edildi; metnin
        okunabilmesi için altına AÇIK ve YUMUŞAK bir zemin konur.
        Bu bir sanat müdahalesi değil, bir OKUNURLUK önlemidir."""
        c.saveState()
        c.setFillColor(Color(0.98, 0.96, 0.90, alpha=alpha))
        c.setStrokeColor(Color(0.42, 0.35, 0.24, alpha=alpha * 0.55))
        c.setLineWidth(0.8)
        c.roundRect(X(x0), Y(y0), X(x1 - x0), Y(y1 - y0), radius=r * PT,
                    stroke=1, fill=1)
        c.restoreState()

    ink = Color(0.13, 0.11, 0.09)
    muted = Color(0.32, 0.28, 0.22)

    # ── ② ÖN PANEL ────────────────────────────────────────────────────────
    fx0 = front_x0 + bleed + safe
    fx1 = front_x1 - bleed - safe
    fw = fx1 - fx0

    title = md["title"].upper()
    t_size, t_lines = fit_lines(c, title, "Title", X(fw - 0.5), 46, 22, 2)
    sub = md["subtitle"].split("—")[0].strip()
    s_size, s_lines = fit_lines(c, sub, "Body", X(fw - 0.8), 15, 9, 2)

    block_h = (len(t_lines) * t_size * 1.16 + 10 + len(s_lines) * s_size * 1.3) / PT
    top_y = FH - bleed - safe - 0.28
    scrim(fx0 - 0.10, top_y - block_h - 0.34, fx1 + 0.10, top_y + 0.20)

    y = top_y - t_size * 0.92 / PT
    c.setFillColor(ink)
    for ln in t_lines:
        c.setFont("Title", t_size)
        c.drawCentredString(X((fx0 + fx1) / 2), Y(y), ln)
        y -= t_size * 1.16 / PT
    y -= 0.06
    c.setFillColor(muted)
    for ln in s_lines:
        c.setFont("Body", s_size)
        c.drawCentredString(X((fx0 + fx1) / 2), Y(y), ln)
        y -= s_size * 1.3 / PT

    # yazar — alt bant
    a_size = 21
    a_y = front_low = bleed + safe + 0.30
    scrim(fx0 + fw * 0.16, a_y - 0.17, fx1 - fw * 0.16, a_y + a_size / PT + 0.15)
    c.setFillColor(ink)
    c.setFont("SansBold", a_size)
    c.drawCentredString(X((fx0 + fx1) / 2), Y(a_y), md["author"].upper())

    # ── ③ SIRT ────────────────────────────────────────────────────────────
    # KDP sırt metnini iki kenardan 0,0625 in içeride ister.
    usable = spine - 2 * SPINE_TEXT_TOL
    rep.facts["spineUsableInches"] = round(usable, 4)
    sp_size = min(13.0, usable * PT * 0.78)
    rep.facts["spineFontPt"] = round(sp_size, 2)
    if md["cover"]["spineTextAllowed"]:
        c.saveState()
        c.setFillColor(Color(0.99, 0.97, 0.92, alpha=0.90))
        c.rect(X(spine_x0 + SPINE_TEXT_TOL * 0.4), Y(bleed + 0.9),
               X(spine - SPINE_TEXT_TOL * 0.8), Y(FH - 2 * bleed - 1.8),
               stroke=0, fill=1)
        c.translate(X(spine_x0 + spine / 2), Y(FH / 2))
        c.rotate(-90)
        c.setFillColor(ink)
        c.setFont("SansBold", sp_size)
        c.drawCentredString(0, -sp_size * 0.34, "%s   ·   %s"
                            % (md["title"].upper(), md["author"].upper()))
        c.restoreState()

    # ── ④ ARKA PANEL ──────────────────────────────────────────────────────
    bx0 = back_x0 + bleed + safe
    bx1 = back_x1 - bleed - safe
    bw = bx1 - bx0

    hook = "Twenty-two peoples. One quest. No screens."
    feats = [
        "%d puzzles built from real writing systems, maps and codes"
        % md["descriptionFacts"]["activities"],
        "22 cultures across 6 regions — every answer checked against "
        "museums, archives and universities",
        "Six seals to earn, and a certificate at the end",
        "Written in, not read to — pencil only, no screen",
    ]
    # ⚠ KAPAKTA TEKRAR: kanca ve tanıtım metni AYNI cümleyle başlıyordu
    # ("Twenty-two peoples."). Arka kapağın ilk iki satırında birebir
    # tekrar, okurun gözünde metni ucuzlatır.
    #
    #     KDP açıklaması TAM hâliyle kalır — kapak onun bir SUNUMUDUR,
    #     kopyası değil.
    #
    # Bu yüzden kancanın yuttuğu ilk cümle kapak metninden düşülür;
    # `metadata.json § description` DEĞİŞMEZ.
    blurb = md["description"]
    if blurb.startswith("Twenty-two peoples. "):
        blurb = blurb[len("Twenty-two peoples. "):]
    age = "Ages %d–%d  ·  %d pages  ·  screen-free" % (
        md["audience"]["ageMin"], md["audience"]["ageMax"],
        md["edition"]["pages"])
    bio = md["authorBio"]

    # ⭑ ALTLIK METNİ ÖLÇTÜKTEN SONRA ÇİZİLİR ⭑
    #
    # İlk hâl altlığı barkod alanının hemen üstüne kadar uzatıyordu ve
    # metin üçte birinde bitiyordu: arka kapağın yarısı boş bir krem
    # dikdörtgen olarak kalıyordu. Boş bir altlık, tasarımın kendisi
    # gibi görünür ve ucuz durur.
    #
    #     Bir altlık metni TAŞIR; metnin yerine geçmez.
    #
    # Bu yüzden bütün satırlar ÖNCE sarılır, yükseklik toplanır ve
    # altlık o yüksekliğe göre çizilir. Blok kalan alanda dikey
    # ortalanır.
    blurb_lines = wrap(c, blurb, "Body", 10.2, X(bw - 0.3))
    feat_lines = [wrap(c, f, "Sans", 9.6, X(bw - 0.55)) for f in feats]
    bio_lines = wrap(c, bio, "Body", 9.0, X(bw - 0.3))
    text_h = (0.40 + 0.36
              + len(blurb_lines) * 0.185 + 0.16
              + sum(len(g) * 0.17 + 0.03 for g in feat_lines) + 0.10
              + len(bio_lines) * 0.155)

    zone_top = FH - bleed - safe - 0.45
    zone_bottom = bleed + safe + BARCODE_H + BARCODE_MARGIN + 0.30
    slack = max(0.0, (zone_top - zone_bottom) - text_h)
    b_top = zone_top - slack / 2.0
    scrim(bx0 - 0.14, b_top - text_h - 0.26, bx1 + 0.14, b_top + 0.42, alpha=0.86)
    rep.facts["backScrimHeightInches"] = round(text_h + 0.68, 3)

    y = b_top
    c.setFillColor(ink)
    c.setFont("Title", 19)
    c.drawCentredString(X((bx0 + bx1) / 2), Y(y), hook)
    y -= 0.40

    c.setFillColor(muted)
    c.setFont("Sans", 10.5)
    c.drawCentredString(X((bx0 + bx1) / 2), Y(y), age)
    y -= 0.36

    c.setFillColor(ink)
    for ln in blurb_lines:
        c.setFont("Body", 10.2)
        c.drawString(X(bx0 + 0.15), Y(y), ln)
        y -= 0.185
    y -= 0.16

    for lines in feat_lines:
        c.setFont("SansBold", 11)
        c.drawString(X(bx0 + 0.18), Y(y), "•")
        for i, ln in enumerate(lines):
            c.setFont("Sans", 9.6)
            c.drawString(X(bx0 + 0.38), Y(y), ln)
            y -= 0.17
        y -= 0.03
    y -= 0.10

    c.setFillColor(muted)
    for ln in bio_lines:
        c.setFont("Body", 9.0)
        c.drawString(X(bx0 + 0.15), Y(y), ln)
        y -= 0.155

    rep.facts["backTextBottomInches"] = round(y, 3)
    rep.facts["barcodeTopInches"] = round(bleed + safe + BARCODE_H, 3)

    # ⑤ BARKOD ALANI — BOŞ BIRAKILIR, ÇİZİLMEZ
    #
    # ⚠ Buraya SAHTE bir barkod veya ISBN basılmaz. KDP ücretsiz ISBN
    # veriyor ve barkodu kendisi basıyor; hat yalnızca alanı temiz
    # tutar. Kesin kutu konumu KDP ŞABLONUNDAN doğrulanır — bu koordinat
    # bir başlangıçtır, bir teyit değil.
    rep.facts["barcodeZoneInches"] = {
        "x": round(back_x1 - bleed - safe - BARCODE_W, 3),
        "y": round(bleed + safe, 3),
        "w": BARCODE_W, "h": BARCODE_H,
        "note": "boş bırakıldı · KDP kendi barkodunu basar",
    }

    c.showPage()
    c.save()
    return md, {"panel": panel, "spine": spine, "FW": FW, "FH": FH}


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    print("=" * 74)
    print("  CİLTSİZ KAPAK ÜRETİMİ")
    print("=" * 74)

    try:
        import reportlab  # noqa: F401
        import PIL        # noqa: F401
    except ImportError:
        print("  ⊘ reportlab/Pillow yok — ATLANDI")
        print("=" * 74)
        return 2

    md = jload(META)
    if md is None:
        print("  ⊘ metadata.json yok — önce ./04_BUILD/metadata.py")
        print("=" * 74)
        return 0

    # ⭑ HAM KAPAK SANATI DEPODA DURMAZ (.gitignore § ③) ⭑
    #
    # CI'da `07_ASSETS/raw/` boştur ve kapak ÜRETİLEMEZ. Bu bir kalite
    # düşüşü DEĞİLDİR: kaynak orada değildir. Aynı hata bu projede iki
    # kez CI'ı kırmızı yaktı (`update_docs` · `metadata --check`) ve
    # dersi kayıtlıdır:
    #
    #     Üretilmemiş bir çıktı, bozuk bir çıktı değildir.
    #     Ve OLMAYAN bir kaynak, bir kusur değildir.
    sel = jload(SELECTION) or {}
    art = os.path.join(RAW_DIR, (sel.get("selected") or "") + ".png")
    if not os.path.isfile(art):
        print("  ⊘ ham kapak sanatı depoda yok (.gitignore § ③) — BOŞ KOŞTU")
        print("=" * 74)
        return 0

    if args.check:
        # Bayatlık: kapak raporu, ÜRETİLDİĞİ ANDAKİ sayfa sayısını ve
        # sanat sha256'sını taşır. İkisinden biri değiştiyse kapak bayattır.
        cj = jload(REPORT, {}) or {}
        f = cj.get("facts") or {}
        stale = []
        if f.get("pages") != md["edition"]["pages"]:
            stale.append("sayfa %s ≠ %s" % (f.get("pages"), md["edition"]["pages"]))
        if f.get("artSha256") != sha256(art):
            stale.append("kapak sanatı değişti")
        if not os.path.isfile(REPORT):
            stale.append("kapak hiç üretilmedi")
        if stale:
            print("  ✗ BAYAT: %s" % " · ".join(stale))
            print("\n  Tazele: ./04_BUILD/covers.py")
            print("=" * 74)
            return 1
        print("  ✅ kapak güncel (%d sayfa · sırt %.4f in)"
              % (md["edition"]["pages"], md["cover"]["spineInches"]))
        print("=" * 74)
        return 0

    rep = Report()
    res = build(rep)
    if res is None:
        print("\n" + "=" * 74)
        print("  ⛔ kapak ÜRETİLEMEDİ")
        for e in rep.errors:
            print("     · %s" % e)
        print("=" * 74)
        return 1
    md, geo = res

    print("\n── ① geometri ──")
    print("  tam kapak   %.4f × %.4f in" % (geo["FW"], geo["FH"]))
    print("  sırt        %.4f in  (%s sayfa)" % (geo["spine"], md["edition"]["pages"]))
    print("  panel       %.4f in" % geo["panel"])
    rep.check(abs(2 * geo["panel"] + geo["spine"] - geo["FW"]) < 1e-9,
              "arka + sırt + ön = tam kapak")

    print("\n── ② çözünürlük ──")
    print("  sanat       %d × %d px" % tuple(rep.facts["artPixels"]))
    print("  gereken     %d × %d px @300 dpi" % tuple(rep.facts["requiredPixels"]))
    print("  ETKİN DPI   %.1f" % rep.facts["effectiveDpi"])
    if rep.facts["effectiveDpi"] < 300:
        rep.warn("kapak sanatı 300 dpi ALTINDA (%.0f dpi) — yukarı örnekleme "
                 "YAPILMADI; tipografi vektör olduğu için METİN keskin. "
                 "KURUCU EYLEMİ: sanatı ≥%d × %d px yeniden üret."
                 % (rep.facts["effectiveDpi"], *rep.facts["requiredPixels"]))

    print("\n── ③ sırt metni ──")
    print("  kullanılabilir bant %.4f in · punto %.2f pt"
          % (rep.facts["spineUsableInches"], rep.facts["spineFontPt"]))
    rep.check(rep.facts["spineFontPt"] * 1.0 <= rep.facts["spineUsableInches"] * PT,
              "sırt puntosu tolerans bandına sığıyor")

    print("\n── ④ barkod alanı ──")
    bz = rep.facts["barcodeZoneInches"]
    print("  %.2f × %.2f in @ (%.2f, %.2f) — BOŞ" % (bz["w"], bz["h"], bz["x"], bz["y"]))
    rep.check(rep.facts["backTextBottomInches"] > bz["y"] + bz["h"],
              "arka kapak metni barkod alanına GİRMİYOR (%.2f > %.2f)"
              % (rep.facts["backTextBottomInches"], bz["y"] + bz["h"]))

    print("\n── ⑤ yazı tipi ──")
    rep.check(bool(rep.facts.get("fontDir")), "gömülebilir yazı tipi kayıtlı")

    rep.facts["output"] = os.path.relpath(OUT, ROOT)
    rep.facts["pages"] = md["edition"]["pages"]
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as fh:
        json.dump({"status": "fail" if rep.errors else "pass",
                   "checks": rep.checks, "errors": rep.errors,
                   "warnings": rep.warnings, "facts": rep.facts},
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
