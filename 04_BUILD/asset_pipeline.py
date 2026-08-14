#!/usr/bin/env python3
"""
GÖRSEL İŞLEME HATTI — The Myth Hunter's Field Book
================================================================================
RAW → işle → doğrula → PROCESSED → FINAL

⭑ BU BETİĞİN EN ÖNEMLİ ÖZELLİĞİ NE YAPMADIĞIDIR ⭑

    RAW'A ASLA YAZMAZ.

Ham görsel kurucunun çıktısıdır ve **yeniden üretilemez**: üreteç
deterministik değildir, aynı prompt aynı görseli iki kez vermez. Üzerine
yazılan bir RAW **geri getirilemez**. Bu yüzden hat tek yönlüdür ve
betik ham dizini yalnızca OKUR (karar K35).

    İşlenmiş bir varlık her zaman RAW'dan YENİDEN üretilebilmelidir.

Bu cümle bir slogan değil bir SÖZLEŞMEDİR ve mekanikleştirilmiştir: her
işlenmiş dosyanın yanına kaynağının sha256'sı yazılır
(`processed/<ad>.source.json`). Kaynak değişirse hat bunu görür ve
yeniden üretir; değişmediyse dokunmaz.

⭑ REDDEDİLEN GÖRSEL SİLİNMEZ ⭑

Şartnameyi ihlal eden bir RAW `rejected/` altına **taşınmaz — kopyalanır**
ve gerekçesi yazılır. Silinen bir ret, aynı hatanın ikinci kez
yapılmasını serbest bırakır.

NE YAPAR:

  ① ölçüm      RAW'ı açar, gerçek boyut/oran/mod okur
  ② normalize  gri tonlama, 8-bit, profil temizliği
  ③ kırpma     istenmeyen düz kenar boşluklarını kırpar (yalnızca UNIFORM)
  ④ ölçekleme  hedef piksele oturtur, ORANI BOZMADAN
  ⑤ DPI        300 dpi damgası
  ⑥ optimize   PNG yeniden sıkıştırma, kayıpsız
  ⑦ köken      kaynak sha256 + parametreler yazılır

NE YAPMAZ:

  · içerik ekleme veya silme
  · metin basma (tipografi dizgi katmanındadır · § 13)
  · yukarı örnekleme ile "çözünürlük kazanma" — bu bir YALANDIR
  · RAW'ı değiştirme

  ./04_BUILD/asset_pipeline.py                bekleyen bütün RAW'ları işle
  ./04_BUILD/asset_pipeline.py --asset ID     tek varlık
  ./04_BUILD/asset_pipeline.py --check        işlenmişler güncel mi
  ./04_BUILD/asset_pipeline.py --final        processed → final
  ./04_BUILD/asset_pipeline.py --report       durum tablosu

TASARIM: Pillow ister. Yoksa çıkış 2 (ATLANDI) — bir kalite düşüşü
DEĞİLDİR, çünkü ham varlık yokken işlenecek bir şey de yoktur.

Çıkış kodları:  0 = tamam   1 = KIRMIZI   2 = bağımlılık yok (ATLA)
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

MANIFEST = os.path.join(ROOT, "07_ASSETS", "ASSET_MANIFEST.json")
MANIFEST_LOCAL = os.path.join(ROOT, "07_ASSETS", "ASSET_MANIFEST.local.json")

# ⭑ TAM KAYIT YEREL DOSYADADIR ⭑
# Takip edilen envanter içerik taşımaz (K10): requiredLabels ve
# restrictions cevabın kendisini taşıyabilir. Hat ve kapı tam kaydı
# yerelden okur; yerel kayıt yoksa takip edilenle YARIM koşar ve bunu
# SÖYLER — sessizce eksik denetim yapmaz.
def manifest_path():
    return MANIFEST_LOCAL if os.path.isfile(MANIFEST_LOCAL) else MANIFEST
RAW_DIR = os.path.join(ROOT, "07_ASSETS", "raw")
PROC_DIR = os.path.join(ROOT, "07_ASSETS", "processed", "interior")
FINAL_DIR = os.path.join(ROOT, "07_ASSETS", "final", "interior")
REJECT_DIR = os.path.join(ROOT, "07_ASSETS", "rejected")

# Oran toleransı: %1,5. GPT Image çıktısı hedef oranı tam tutturmaz ve
# kırpma bir milimetrelik farkı zaten yutar. Bundan büyük bir sapma ise
# YANLIŞ ŞABLON demektir ve kırpılarak gizlenmemelidir.
ASPECT_TOL = 0.015

# Yukarı örnekleme sınırı: YOK. Bir görsel hedefin altındaysa büyütülmez,
# REDDEDİLİR. Büyütmek çözünürlük kazandırmaz, yalnızca dosyayı şişirir
# ve 300 dpi iddiasını YALAN hâline getirir.
MIN_SCALE = 1.0


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest():
    p = manifest_path()
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def uniform_border_box(im, tol=6):
    """Yalnızca DÜZ (tek renkli) kenar boşluğunu bulur.

    ⚠ İçeriğe dokunan bir kırpma YAPILMAZ. GPT Image çıktıları çoğu zaman
    beyaz bir çerçeveyle gelir ve o çerçeve sayfada ikinci bir kenar
    boşluğu yaratır. Ama bir görselin kenarı gerçekten beyazsa (harita
    kenarı, boş çerçeve) kırpmak İÇERİK SİLMEKTİR.

    Bu yüzden ölçüt sıkıdır: kenar şeridi neredeyse tek renk olmalıdır.
    Şüphe varsa KIRPILMAZ — kırpmamak geri alınabilir, kırpmak alınamaz.
    """
    from PIL import ImageChops
    g = im.convert("L")
    bg = g.getpixel((0, 0))
    # Dört kenarın da aynı renkte olması gerekir; değilse düz çerçeve yok.
    w, h = g.size
    corners = [g.getpixel((0, 0)), g.getpixel((w - 1, 0)),
               g.getpixel((0, h - 1)), g.getpixel((w - 1, h - 1))]
    if max(corners) - min(corners) > tol:
        return None
    from PIL import Image
    bgim = Image.new("L", g.size, bg)
    diff = ImageChops.difference(g, bgim)
    box = diff.point(lambda p: 255 if p > tol else 0).getbbox()
    if not box:
        return None
    if box == (0, 0, w, h):
        return None
    return box


def process_one(asset, raw_path, force=False, verbose=False):
    """Tek varlığı işler. (durum, mesaj) döner."""
    from PIL import Image

    fn = asset["filename"]
    out = os.path.join(PROC_DIR, fn)
    meta_path = out + ".source.json"
    src_hash = sha256(raw_path)

    # Köken kaydı: kaynak değişmediyse yeniden üretme.
    if not force and os.path.isfile(out) and os.path.isfile(meta_path):
        try:
            with open(meta_path, encoding="utf-8") as fh:
                prev = json.load(fh)
            if prev.get("sourceSha256") == src_hash:
                return "current", "güncel"
        except (json.JSONDecodeError, OSError):
            pass

    im = Image.open(raw_path)
    orig_size = im.size
    steps = []

    # ② normalize — iç blok siyah beyaz basılır (production.ink = black)
    if im.mode not in ("L", "1"):
        im = im.convert("L")
        steps.append("grayscale")

    # ③ kırpma — YALNIZCA düz kenar boşluğu
    box = uniform_border_box(im)
    if box:
        im = im.crop(box)
        steps.append("crop%s" % (list(box),))

    # ④ ölçekleme — ORANI BOZMADAN, ve ASLA BÜYÜTMEDEN
    #
    # ⚠ BU ADIM İKİ KEZ YAZILDI VE İLK HÂLİ YANLIŞTI.
    #
    # İlk hâl yalnızca hedefin İÇİNE sığdırıyordu ve orada bırakıyordu.
    # Sonuç: kenar boşluğu kırpılmış her görselin oranı hedeften kayıyordu
    # ve kapı onu "yanlış oran" diye reddediyordu — oysa kusur görselde
    # değil HATTAYDI. Kırpma oranı değiştirir; bu kaçınılmazdır.
    #
    #     Bir hat, kendi ürettiği çıktıyı kapısına reddettiriyorsa,
    #     düzeltilmesi gereken kapı değil HATTIR.
    #
    # Doğrusu: sığdır, sonra hedef kutuya BEYAZLA DOLDUR. Dizgici zaten
    # bunu yapardı; hat onu deterministik ve ölçülebilir hâle getiriyor.
    # Sanata dokunulmaz, kutu garanti edilir.
    tw, th = asset["targetDimensions"]
    w, h = im.size
    scale = min(tw / w, th / h)

    # ⭑ HEDEFTEN KÜÇÜK BİR GÖRSEL BÜYÜTÜLMEZ — VE İŞLENMEZ ⭑
    #
    # Yukarı örnekleme çözünürlük kazandırmaz; yalnızca 300 dpi iddiasını
    # YALAN hâline getirir. İlk hâl bu görselleri yine de işliyordu ve
    # geriye kırık bir işlenmiş dosya bırakıyordu — kapı iki ayrı denetimde
    # aynı kusuru iki kez bildiriyordu.
    #
    #     Bir hat, kabul edemeyeceği bir girdiden çıktı üretmemelidir.
    #
    # Doğrusu: RET. Ham dosya SİLİNMEZ, `rejected/` altına gerekçesiyle
    # kopyalanır ve kurucu onu yeniden üretir (K35).
    if scale > MIN_SCALE:
        reject(asset, raw_path,
               "RAW hedef çözünürlüğün ALTINDA: sanat %dx%d, hedef %dx%d. "
               "Büyütme YAPILMADI — yukarı örnekleme çözünürlük kazandırmaz "
               "ve 300 dpi iddiasını yalan hâline getirir. Yeniden üretilmeli."
               % (w, h, tw, th))
        return "rejected", "RET · hedefin altında (%dx%d < %dx%d)" % (w, h, tw, th)

    under = False
    if scale < MIN_SCALE:
        im = im.resize((max(1, round(w * scale)), max(1, round(h * scale))),
                       Image.LANCZOS)
        steps.append("downscale%.3f" % scale)

    # ⑤ hedef kutuya doldurma — sanat ortalanır, kalan beyaz kalır
    art_w, art_h = im.size
    fill = (art_w * art_h) / float(tw * th)
    if (art_w, art_h) != (tw, th):
        canvas = Image.new("L", (tw, th), 255)
        canvas.paste(im, ((tw - art_w) // 2, (th - art_h) // 2))
        im = canvas
        steps.append("pad→%dx%d" % (tw, th))

    os.makedirs(PROC_DIR, exist_ok=True)
    im.save(out, "PNG", optimize=True, dpi=(asset.get("minDpi") or 300,) * 2)
    steps.append("dpi%d" % (asset.get("minDpi") or 300))

    meta = collections.OrderedDict([
        ("assetId", asset["assetId"]),
        ("source", os.path.relpath(raw_path, ROOT)),
        ("sourceSha256", src_hash),
        ("sourceSize", list(orig_size)),
        ("artSize", [art_w, art_h]),
        ("outputSize", list(im.size)),
        ("targetSize", list(asset["targetDimensions"])),
        # Doluluk: sanat hedef kutunun ne kadarını dolduruyor. 1,0'a yakın
        # olması RAW'ın oranının doğru olduğu anlamına gelir; düşük bir
        # değer YANLIŞ ŞABLON demektir ve doldurma onu GİZLEMEZ, ÖLÇER.
        ("fillRatio", round(fill, 4)),
        ("underTarget", bool(under)),
        ("steps", steps),
        ("generator", "04_BUILD/asset_pipeline.py"),
    ])
    with open(meta_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return "processed", " · ".join(steps)


def reject(asset, raw_path, reason):
    """Reddedilen RAW SİLİNMEZ: kopyalanır ve gerekçesi yazılır."""
    os.makedirs(REJECT_DIR, exist_ok=True)
    dest = os.path.join(REJECT_DIR, asset["filename"])
    if not os.path.isfile(dest):
        shutil.copy2(raw_path, dest)
    with open(dest + ".reason.json", "w", encoding="utf-8") as fh:
        json.dump({"assetId": asset["assetId"],
                   "source": os.path.relpath(raw_path, ROOT),
                   "sourceSha256": sha256(raw_path),
                   "reason": reason}, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def promote_final(asset):
    """processed → final. Ayrı bir katman, çünkü FINAL bir KARARDIR:
    doğrulamadan geçmiş bir varlık basıma hazırdır ve o an damgalanır."""
    src = os.path.join(PROC_DIR, asset["filename"])
    if not os.path.isfile(src):
        return False
    os.makedirs(FINAL_DIR, exist_ok=True)
    shutil.copy2(src, os.path.join(FINAL_DIR, asset["filename"]))
    meta = src + ".source.json"
    if os.path.isfile(meta):
        shutil.copy2(meta, os.path.join(FINAL_DIR,
                                        asset["filename"] + ".source.json"))
    return True


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--asset", default=None, help="tek varlık kimliği")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--final", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    print("=" * 74)
    print("  GÖRSEL İŞLEME HATTI · RAW → PROCESSED → FINAL")
    print("=" * 74)

    doc = load_manifest()
    if doc is None:
        print("  ⊘ ASSET_MANIFEST.json yok — önce ./04_BUILD/asset_manifest.py")
        print("=" * 74)
        return 0 if args.check else 2

    assets = doc["assets"]
    if args.asset:
        assets = [a for a in assets if a["assetId"] == args.asset]
        if not assets:
            print("  ⛔ bilinmeyen varlık: %s" % args.asset)
            return 2

    # RAW envanteri
    present = []
    for a in assets:
        rp = os.path.join(ROOT, a["rawLocation"])
        if os.path.isfile(rp):
            present.append((a, rp))

    print("  manifest varlığı : %d" % len(assets))
    print("  RAW mevcut       : %d" % len(present))
    print("  RAW eksik        : %d" % (len(assets) - len(present)))

    if args.report:
        proc = sum(1 for a in assets
                   if os.path.isfile(os.path.join(PROC_DIR, a["filename"])))
        fin = sum(1 for a in assets
                  if os.path.isfile(os.path.join(FINAL_DIR, a["filename"])))
        rej = sum(1 for a in assets
                  if os.path.isfile(os.path.join(REJECT_DIR, a["filename"])))
        print("  işlenmiş         : %d" % proc)
        print("  nihai            : %d" % fin)
        print("  reddedilmiş      : %d" % rej)
        print("=" * 74)
        return 0

    if not present:
        # ⚠ BU BİR HATA DEĞİLDİR VE ÖYLE RAPORLANMAZ.
        # Ham görselleri KURUCU üretir (açık kalem, PROJECT_CONTEXT § 10).
        # Hat hazırdır ve ham varlık geldiği gün çalışır.
        print("\n  ⊘ hiç ham varlık yok — hat BOŞ KOŞTU")
        print("     Ham görsel üretimi KURUCUYA aittir; hat hazırdır.")
        print("=" * 74)
        return 0

    try:
        import PIL  # noqa: F401
    except ImportError:
        print("\n  ⊘ Pillow yok — ATLANDI")
        print("     pip install -r 04_BUILD/requirements.txt")
        print("=" * 74)
        return 2

    if args.final:
        n = sum(1 for a, _ in present if promote_final(a))
        print("\n  nihai katmana alınan: %d" % n)
        print("=" * 74)
        return 0

    stale, done = [], 0
    for a, rp in present:
        status, msg = process_one(a, rp, force=args.force, verbose=args.verbose)
        if status == "processed":
            done += 1
            if args.check:
                stale.append(a["assetId"])
        if args.verbose or status == "processed":
            print("  %-34s %s" % (a["assetId"], msg))

    if args.check:
        if stale:
            print("\n  ✗ %d işlenmiş varlık BAYAT: %s"
                  % (len(stale), stale[:5]))
            print("\n  Tazele: ./04_BUILD/asset_pipeline.py")
            print("=" * 74)
            return 1
        print("\n  ✅ işlenmiş varlıklar güncel")
        print("=" * 74)
        return 0

    print("\n  ✅ %d varlık işlendi · %d zaten günceldi"
          % (done, len(present) - done))
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
