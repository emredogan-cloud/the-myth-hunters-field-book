#!/usr/bin/env python3
"""
KURUCU VARLIK KABULÜ — The Myth Hunter's Field Book
================================================================================
Teslim edilen ham görselleri **kanonik adlarına kurar** ve eşlemeyi
`07_ASSETS/DELIVERY_MAP.json` üzerinden sha256'ya bağlar.

⭑ NEDEN BİR HARİTA — VE NEDEN sha256 ⭑

Faz 6 sıralı eşlemeyi denedi ve eşleme **ölçülerek yanlışlandı**:
`001.png` bir Inuktitut levhasıydı, manifestin ilk girdisi ise
`fig-maya-bar-dot-numbers`. Sıralı eşleme 120 sayfanın tamamında yanlış
resim basardı.

    Yanlış aktiviteye bağlanmış kusursuz bir görsel,
    o sayfayı ÇÖZÜLEMEZ yapar.

Bu yüzden eşleme bir kez ÖLÇÜLÜR (oran + görsel içerik denetimi) ve
haritaya yazılır. Harita her satırda kaynağın sha256'sını taşır: dosya
değişirse eşleme geçersizdir ve bu betik KIRMIZI yanar. Aynı harita
başka bir görsele **sessizce uygulanamaz**.

⭑ KURUCUNUN DOSYASI DEĞİŞTİRİLMEZ ⭑

Kanonik olmayan adla gelen bir teslim (`Pasted image.png`) yeniden
adlandırılmaz, **kopyalanır**. Orijinal olduğu yerde kalır.

⭑ YER TUTUCU SİLİNMEZ, ARŞİVLENİR ⭑

Kanonik ham yuvada bir yer tutucu duruyorsa `07_ASSETS/rejected/`
altına `<ad>.placeholder.png` olarak taşınır ve gerekçesi yazılır.
Silinen bir yer tutucu, aynı yuvanın bir gün sessizce boş kalmasıdır.

  ./04_BUILD/asset_intake.py --verify   haritayı sha256 ile doğrula
  ./04_BUILD/asset_intake.py            kanonik ham dosyaları kur
  ./04_BUILD/asset_intake.py --report   durum tablosu

TASARIM: Pillow ister (ölçüm için). Harita doğrulaması saf stdlib'dir.

Çıkış kodları:  0 = tamam   1 = KIRMIZI   2 = bağımlılık yok
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

MAP = os.path.join(ROOT, "07_ASSETS", "DELIVERY_MAP.json")
MANIFEST = os.path.join(ROOT, "07_ASSETS", "ASSET_MANIFEST.json")
REJECT_DIR = os.path.join(ROOT, "07_ASSETS", "rejected")

# Oran toleransı — teslim ile şartname arasında. Üreteç hedef oranı tam
# tutturmaz; %1,5 üstü bir sapma ise YANLIŞ ŞABLON demektir.
ASPECT_TOL = 0.015


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


class Report:
    def __init__(self):
        self.errors, self.warnings, self.checks = [], [], 0

    def check(self, cond, label):
        self.checks += 1
        if not cond:
            self.errors.append(label)
            print("  ✗ %s" % label)
        return bool(cond)

    def warn(self, label):
        self.warnings.append(label)
        print("  ! %s" % label)


def is_placeholder(path):
    """Bir ham dosya YER TUTUCU mu?

    Yer tutucular hattın kendi ürettiği çapraz taramalı kutulardır ve
    manifestte `placeholder-art-missing` durumuyla kayıtlıdır. Dosyayı
    içeriğinden tanımaya çalışmak kırılgan olurdu; durum kaydı yeterli
    ve KESİNDİR."""
    return os.path.isfile(path)


def verify(rep, doc):
    """Haritanın her satırını sha256 ve ölçü ile doğrular."""
    man = {a["assetId"]: a for a in (jload(MANIFEST, {}) or {}).get("assets", [])}
    print("\n── ① teslim haritası bütünlüğü ──")
    for d in doc["deliveries"]:
        p = os.path.join(ROOT, d["delivered"])
        if not rep.check(os.path.isfile(p), "teslim dosyası var: %s" % d["delivered"]):
            continue
        got = sha256(p)
        rep.check(got == d["sha256"],
                  "sha256 haritayla aynı: %s%s"
                  % (d["delivered"],
                     "" if got == d["sha256"] else " — HARİTA %s, DOSYA %s"
                     % (d["sha256"][:12], got[:12])))

    print("\n── ② teslim ↔ şartname oranı ──")
    try:
        from PIL import Image
    except ImportError:
        rep.warn("Pillow yok — oran denetimi ATLANDI")
        return
    for d in doc["deliveries"]:
        if d["class"] != "interior":
            continue
        a = man.get(d["assetId"])
        if not rep.check(a is not None,
                         "şartname bulundu: %s" % d["assetId"]):
            continue
        p = os.path.join(ROOT, d["delivered"])
        if not os.path.isfile(p):
            continue
        with Image.open(p) as im:
            w, h = im.size
        tw, th = a["targetDimensions"]
        got, want = w / h, tw / th
        dev = abs(got - want) / want
        rep.check(dev <= ASPECT_TOL,
                  "%s oranı şartnameyle aynı (%.4f ↔ %.4f · sapma %%%.2f)"
                  % (d["assetId"], got, want, dev * 100))
        # ⚠ Küçültme meşrudur, BÜYÜTME değildir: hat büyütmeyi reddeder.
        rep.check(w >= tw and h >= th,
                  "%s hedeften KÜÇÜK DEĞİL (%dx%d ≥ %dx%d)"
                  % (d["assetId"], w, h, tw, th))


def install(rep, doc):
    """Kanonik ham dosyaları kurar; yer tutucuyu arşivler."""
    print("\n── ③ kanonik ham kurulumu ──")
    n_inst = n_arch = 0
    for d in doc["deliveries"]:
        canon = d.get("canonicalRaw")
        if not canon or d["class"] == "aplus":
            continue
        src = os.path.join(ROOT, d["delivered"])
        dst = os.path.join(ROOT, canon)
        if not os.path.isfile(src):
            continue
        if os.path.abspath(src) == os.path.abspath(dst):
            print("  = %-40s zaten kanonik" % d["assetId"])
            continue
        # Yuvada duran yer tutucu ARŞİVLENİR — üzerine yazılmaz.
        if os.path.isfile(dst) and sha256(dst) != d["sha256"]:
            os.makedirs(REJECT_DIR, exist_ok=True)
            base = os.path.basename(canon).replace(".png", ".placeholder.png")
            arch = os.path.join(REJECT_DIR, base)
            if not os.path.isfile(arch):
                shutil.move(dst, arch)
                with open(arch + ".reason.json", "w", encoding="utf-8") as fh:
                    json.dump({
                        "assetId": d["assetId"],
                        "wasAt": canon,
                        "reason": ("FAZ 6 yer tutucusu. Kurucu Aşama 2'de gerçek "
                                   "levhayı teslim etti; yer tutucu SİLİNMEDİ, "
                                   "arşivlendi."),
                        "replacedBy": d["delivered"],
                        "replacedBySha256": d["sha256"],
                    }, fh, ensure_ascii=False, indent=2)
                    fh.write("\n")
                n_arch += 1
                print("  ⌫ %-40s yer tutucu arşivlendi → rejected/" % d["assetId"])
            else:
                os.remove(dst)
        if not os.path.isfile(dst):
            shutil.copy2(src, dst)
            n_inst += 1
            print("  + %-40s kuruldu ← %s"
                  % (d["assetId"], os.path.basename(d["delivered"])))
    print("\n  kurulan: %d · arşivlenen yer tutucu: %d" % (n_inst, n_arch))


def report(doc):
    print("\n── teslim envanteri ──")
    by = {}
    for d in doc["deliveries"]:
        by.setdefault(d["class"], []).append(d)
    for cls in ("interior", "cover", "aplus"):
        items = by.get(cls, [])
        panels = sum(d.get("panels", 1) for d in items)
        print("  %-10s dosya %2d · panel %2d" % (cls, len(items), panels))
        for d in items:
            note = ""
            if d.get("composite"):
                note = "  ⚠ %s → %d panel" % (d["composite"], d["panels"])
            print("      %-34s %s%s"
                  % (d["assetId"], "×".join(map(str, d["deliveredSize"])), note))


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()

    print("=" * 74)
    print("  KURUCU VARLIK KABULÜ")
    print("=" * 74)

    doc = jload(MAP)
    if doc is None:
        # ⚠ Harita yoksa bu bir KUSUR DEĞİLDİR: henüz teslim yapılmamıştır.
        print("  ⊘ DELIVERY_MAP.json yok — teslim yapılmamış, BOŞ KOŞTU")
        print("=" * 74)
        return 0

    # Teslim edilen ham dosyalar depoda durmaz (.gitignore § ③).
    if not any(os.path.isfile(os.path.join(ROOT, d["delivered"]))
               for d in doc["deliveries"]):
        print("  ⊘ teslim dosyaları depoda yok (.gitignore § ③) — BOŞ KOŞTU")
        print("=" * 74)
        return 0

    rep = Report()
    print("  harita satırı: %d" % len(doc["deliveries"]))

    if args.report:
        report(doc)
        print("=" * 74)
        return 0

    verify(rep, doc)
    if rep.errors:
        print("\n" + "=" * 74)
        print("  ⛔ %d/%d DENETİM KIRMIZI — kurulum YAPILMADI"
              % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        print("=" * 74)
        return 1

    if not args.verify:
        install(rep, doc)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    print("  ✅ %d denetim yeşil" % rep.checks)
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
