#!/usr/bin/env python3
"""
LEVHA DİZGİ KATMANI — The Myth Hunter's Field Book
================================================================================
İki levhanın **answer-critical** metnini üreteç yerine DİZGİ basar.

⭑ NEDEN BİR ÜRETEÇ BU İKİ SAYFANIN METNİNİ BASAMAZ ⭑

    yoruba-underdot-letters   Harfin ALTINDAKİ nokta İÇERİĞİN KENDİSİDİR.
                              Uydurulmuş, kaymış veya düşmüş bir nokta
                              levhayı biraz yanlış yapmaz — sayfayı
                              ÇÖZÜLEMEZ ve dilbilimsel iddiayı YANLIŞ yapar.

    korean-river-crossing     Kartların SIRASI cevabın kendisidir. Üretecin
                              yerleştirdiği bir metnin karışık sırada
                              duracağı garanti edilemez; kendi numaralı
                              yerine düşen bir kart cevabı okura VERİR.

Üreteç boş mobilyayı çizdi. Bu betik içine gerçek tipografiyi basar.

⭑ METİN BU DOSYADA YAZILI DEĞİLDİR (K10) ⭑

Yorùbá anahtarı ve Korece kart cümleleri CEVAPTIR ve public depoda
duramazlar. Betik metni `02_MANUSCRIPT/book.json § pagePrints`ten
**türetir**; depoda yalnızca GEOMETRİ durur
(`07_ASSETS/PLATE_GEOMETRY.json`).

    Bir kutunun nerede olduğu bir cevap değildir.
    İçine ne yazılacağı cevaptır.

⭑ RAW'A YAZMAZ ⭑

Çıktı `07_ASSETS/typeset/` altına yazılır ve `asset_pipeline` onu
RAW yerine kaynak alır. Ham dosya kurucunundur ve DEĞİŞMEZ (K35).

  ./04_BUILD/plate_typeset.py            dizilmiş levhaları üret
  ./04_BUILD/plate_typeset.py --check    ham veya geometri değiştiyse KIRMIZI

Çıkış kodları:  0 = tamam   1 = KIRMIZI   2 = bağımlılık yok
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

GEOM = os.path.join(ROOT, "07_ASSETS", "PLATE_GEOMETRY.json")
BOOK = os.path.join(ROOT, "02_MANUSCRIPT", "book.json")
RAW_DIR = os.path.join(ROOT, "07_ASSETS", "raw")
OUT_DIR = os.path.join(ROOT, "07_ASSETS", "typeset")

# Gömülebilir, Latin Genişletilmiş Ek kapsayan yazı tipleri.
# ⚠ Yorùbá `ẹ ọ ṣ` U+1EB9 / U+1ECD / U+1E63 kod noktalarındadır ve
# base-14 PDF yazı tiplerinin WinAnsi kodlamasında YOKTUR. Levha bir
# raster olduğu için burada sorun yaşamayız — ama aynı kusur dizgi
# katmanında yaşandı ve `interior.py` orada düzeltildi.
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def jload(p, default=None):
    if not os.path.isfile(p):
        return default
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def pick_font():
    for p in FONT_CANDIDATES:
        if os.path.isfile(p):
            return p
    return None


def after_colon(s):
    return s.split(":", 1)[1].strip() if ":" in s else s.strip()


def yoruba_content(act):
    """Yorùbá levhasının metnini `pagePrints`ten TÜRETİR.

    Beklenen üç madde:
      'a letter strip printed with six letters side by side: e, ẹ, o, ọ, s, ṣ'
      'a key panel under the strip: ẹ says eh, ọ says aw, ṣ says sh'
      'a rule strip: …'
    Ayrıştırma başarısızsa None döner ve betik SESSİZCE yanlış basmaz."""
    letters, key = None, None
    for p in act.get("pagePrints") or []:
        low = p.lower()
        if "letter strip" in low and "side by side" in low:
            letters = [t.strip() for t in after_colon(p).split(",") if t.strip()]
        elif "key panel" in low:
            pairs = []
            for chunk in after_colon(p).split(","):
                m = re.match(r"\s*(\S+)\s+says\s+(\S+)\s*$", chunk.strip())
                if m:
                    pairs.append((m.group(1), m.group(2)))
            key = pairs
    if not letters or len(letters) != 6 or not key or len(key) != 3:
        return None
    return {"letters": letters, "key": key}


def korean_content(act):
    """Korece kart cümlelerini `pagePrints`ten TÜRETİR.

    Beklenen madde: '… empty number box: A / B / C / D'"""
    for p in act.get("pagePrints") or []:
        if "number box" in p.lower() and "/" in p:
            cards = [c.strip() for c in after_colon(p).split("/") if c.strip()]
            if len(cards) == 4:
                return {"cards": cards}
    return None


def fit_font(draw, text, box, font_path, start, min_size=10):
    """Kutuya sığan en büyük puntoyu bulur. Sığmıyorsa KÜÇÜLTMEZ —
    çağıran sarma yapar. Sessiz taşma YASAK."""
    from PIL import ImageFont
    w = box[2] - box[0]
    size = start
    while size > min_size:
        f = ImageFont.truetype(font_path, size)
        if draw.textlength(text, font=f) <= w:
            return f
        size -= 1
    return ImageFont.truetype(font_path, min_size)


def wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if draw.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def centre(draw, text, font, box, im, fill=0):
    x0, y0, x1, y1 = box
    tw = draw.textlength(text, font=font)
    a = font.getbbox(text)
    th = a[3] - a[1]
    draw.text((x0 + (x1 - x0 - tw) / 2, y0 + (y1 - y0 - th) / 2 - a[1]),
              text, font=font, fill=fill)


def render_plate(asset_id, plate, act, font_path, rep):
    from PIL import Image, ImageDraw

    raw = os.path.join(RAW_DIR, asset_id + ".png")
    if not os.path.isfile(raw):
        rep.append("HAM YOK: %s" % asset_id)
        return None
    got = sha256(raw)
    if got != plate["rawSha256"]:
        rep.append("HAM DEĞİŞTİ: %s — geometri GEÇERSİZ (harita %s, dosya %s)"
                   % (asset_id, plate["rawSha256"][:12], got[:12]))
        return None

    im = Image.open(raw).convert("RGBA")
    im = Image.alpha_composite(Image.new("RGBA", im.size, (255, 255, 255, 255)), im)
    im = im.convert("L")
    if list(im.size) != plate["rawSize"]:
        rep.append("HAM ÖLÇÜSÜ GEOMETRİYLE UYUŞMUYOR: %s" % asset_id)
        return None
    d = ImageDraw.Draw(im)

    # ① ölçülmüş kusurların silinmesi — beyazla kapatma
    for group in plate.get("erase", []):
        for b in group["boxes"]:
            d.rectangle(b, fill=255)

    cells = plate["cells"]
    fonts = plate["fonts"]

    if asset_id == "fig-yoruba-underdot-letters":
        c = yoruba_content(act)
        if not c:
            rep.append("pagePrints AYRIŞTIRILAMADI: %s — dizgi YAPILMADI" % asset_id)
            return None
        from PIL import ImageFont
        f_let = ImageFont.truetype(font_path, fonts["letterStrip"])
        for box, ch in zip(cells["letterStrip"], c["letters"]):
            centre(d, ch, f_let, box, im)
        f_g = ImageFont.truetype(font_path, fonts["keyGlyph"])
        f_s = ImageFont.truetype(font_path, fonts["keySound"])
        for box, (g, _s) in zip(cells["keyGlyph"], c["key"]):
            centre(d, g, f_g, box, im)
        for box, (_g, s) in zip(cells["keySound"], c["key"]):
            centre(d, s, f_s, box, im)
        # Kural şeridi gösterim glifi: anahtarın İLK dotted harfi.
        f_r = ImageFont.truetype(font_path, fonts["ruleDemoGlyph"])
        centre(d, c["key"][0][0], f_r, cells["ruleDemoGlyph"][0], im)
        placed = 6 + 3 + 3 + 1

    elif asset_id == "fig-korean-river-crossing-sort":
        c = korean_content(act)
        if not c:
            rep.append("pagePrints AYRIŞTIRILAMADI: %s — dizgi YAPILMADI" % asset_id)
            return None
        from PIL import ImageFont
        perm = plate["cardOrder"]["permutation"]
        if sorted(perm) != [1, 2, 3, 4]:
            rep.append("permutation geçersiz: %s" % perm)
            return None
        if any(p == i + 1 for i, p in enumerate(perm)):
            rep.append("permutation bir DERANGEMENT DEĞİL: %s — bir kart kendi "
                       "numaralı yerinde duruyor" % perm)
            return None
        # ⭑ ÖNCE TEK SATIR DENENİR — VE BU BİR ÜSLUP TERCİHİ DEĞİL ⭑
        #
        # İlk hâl sabit puntoyla dizip taşarsa SARIYORDU. Uzun kart
        # ("he crosses and goes on to found Goguryeo") iki satıra düştü
        # ve ikinci satır kartın kendi YAZMA ÇİZGİSİNİN üstüne bindi:
        # metin ile çizgi çakıştı. Çakışma sayfada görünür bir kusurdur
        # ve dizgi onu gizleyemez.
        #
        #     Bir kutuya sığmayan metin sarılmadan ÖNCE küçültülür;
        #     küçültme tabanı da sığdırmıyorsa O ZAMAN sarılır.
        #
        # Taban 20 px: nihai 975 px genişlikte 6,5 inçe oturunca
        # ≈ 9,6 pt eder ve 8–12 yaş için okunur kalır.
        CARD_MIN = 20
        for box, story_no in zip(cells["cardText"], perm):
            text = c["cards"][story_no - 1]
            w = box[2] - box[0]
            f = fit_font(d, text, box, font_path, fonts["cardText"], CARD_MIN)
            lines = [text] if d.textlength(text, font=f) <= w else wrap(d, text, f, w)
            lh = f.getbbox("Ag")[3] - f.getbbox("Ag")[1] + 8
            # Tek satır kartın üst yarısına oturur: alt yarıda kartın
            # kendi yazma çizgisi vardır ve metin oraya inemez.
            y = box[1] + ((box[3] - box[1]) - lh * len(lines)) / 2 - lh * 0.15
            for ln in lines:
                d.text((box[0], y), ln, font=f, fill=0)
                y += lh
        placed = 4
    else:
        rep.append("bilinmeyen levha: %s" % asset_id)
        return None

    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, asset_id + ".png")
    im.save(out, "PNG", optimize=True)
    meta = {
        "assetId": asset_id,
        "sourceRaw": os.path.relpath(raw, ROOT),
        "sourceSha256": got,
        "geometrySha256": sha256(GEOM),
        "erasedBoxes": sum(len(g["boxes"]) for g in plate.get("erase", [])),
        "placedCells": placed,
        "font": font_path,
        "generator": "04_BUILD/plate_typeset.py",
        "note": ("Metin `02_MANUSCRIPT/book.json § pagePrints`ten TÜRETİLDİ; "
                 "bu dosyada ve PLATE_GEOMETRY.json'da YAZILI DEĞİLDİR (K10)."),
    }
    with open(out + ".source.json", "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return out, placed, meta["erasedBoxes"]


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    print("=" * 74)
    print("  LEVHA DİZGİ KATMANI")
    print("=" * 74)

    geom = jload(GEOM)
    if geom is None:
        print("  ⊘ PLATE_GEOMETRY.json yok — BOŞ KOŞTU")
        print("=" * 74)
        return 0

    book = jload(BOOK)
    if book is None:
        # ⚠ Manuscript depoda durmaz (K10). Metin ondan türer; yoksa
        # dizgi yapılamaz ve bu bir KUSUR DEĞİLDİR.
        print("  ⊘ manuscript depoda yok (K10) — dizgi yapılamadı, BOŞ KOŞTU")
        print("=" * 74)
        return 0

    try:
        import PIL  # noqa: F401
    except ImportError:
        print("  ⊘ Pillow yok — ATLANDI")
        print("=" * 74)
        return 2

    font_path = pick_font()
    if not font_path:
        print("  ⛔ Latin Genişletilmiş Ek kapsayan yazı tipi bulunamadı")
        print("=" * 74)
        return 1
    print("  yazı tipi: %s" % font_path)

    # Ham levha depoda durmaz: CI'da doğrulanacak bir şey yok.
    if not any(os.path.isfile(os.path.join(RAW_DIR, aid + ".png"))
               for aid in geom["plates"]):
        print("  ⊘ ham levha depoda yok (.gitignore § ③) — BOŞ KOŞTU")
        print("=" * 74)
        return 0

    acts = {a["activityId"]: a for a in book.get("activities", [])}
    byasset = {(a.get("visualSpec") or {}).get("assetId"): a for a in acts.values()}

    errs, done = [], 0
    for asset_id, plate in geom["plates"].items():
        act = byasset.get(asset_id)
        if not act:
            errs.append("aktivite bulunamadı: %s" % asset_id)
            continue
        res = render_plate(asset_id, plate, act, font_path, errs)
        if res:
            out, placed, erased = res
            done += 1
            print("  ✓ %-36s %d hücre dizildi · %d kutu silindi"
                  % (asset_id, placed, erased))

    print("\n" + "=" * 74)
    if errs:
        print("  ⛔ %d HATA" % len(errs))
        for e in errs:
            print("     · %s" % e)
        print("=" * 74)
        return 1
    print("  ✅ %d levha dizildi → 07_ASSETS/typeset/" % done)
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
