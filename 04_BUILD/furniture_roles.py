#!/usr/bin/env python3
"""
SAYFA MOBİLYASI ROL AYRIMI — The Myth Hunter's Field Book
================================================================================
`pagePrints` **iki ayrı muhataba** yazılmış tek bir listedir ve ayrım
hiçbir yerde yazılı değildi. Bu betik ayrımı ÖLÇER ve manuscript'e
kalıcı bir alan olarak YAZAR.

⭑ KUSUR NEYDİ ⭑

    LEVHANIN çizeceği   anahtar paneli · kart · harita · nesne
    DİZGİNİN çizeceği   yazma satırı · yıldızlı kutu · numara kutusu

Faz 6 promptu doldururken listenin TAMAMINI üretece verdi; üreteç sayfa
mobilyasını da sanatın içine çizdi. `interior.py` ise aynı mobilyayı
kendi işi saymaya devam etti. Ölçüm:

    yıldızlı kutu iki kez basılıyor   37 / 37 mühür sayfası
    yazma alanı iki kez basılıyor     75 / 120 sayfa
    çiftlemesiz                       21 / 120 sayfa

> 37 mühür sayfasının 37'sinde çocuk İKİ yıldız kutusu görüyor ve
> hangisini dolduracağını bilmiyor.

Faz 5 `A1` yıldızlı kutunun **basılı sayısını** düzeltmişti; kimse
kutunun **kaç kez basıldığını** sormamıştı. Doğru bir sayı, iki kez
basılınca doğru kalmıyor.

⭑ HANGİ TARAF BIRAKIR — VE NEDEN ⭑

156 levha ÜRETİLMİŞ durumda ve mobilya onların içine çizilmiş. Levhaları
yeniden üretmek ajanın elinde değildir (ham üretim kurucuya aittir).
Geriye tek uygulanabilir kök düzeltme kalır:

    Levha bir mobilyayı zaten basıyorsa, DİZGİ onu basmaz.

Ve bu yalnızca uygulanabilir olan değil, DOĞRU olandır: levhanın
satırları ANLAMLI konumdadır ("her sepetin yanında bir satır", "her
runenin yanında iki satır"). Dizginin sayfa altına attığı genel blok
ise konumsuzdur. Anlamlı olan kalır.

⭑ ROL TAHMİN EDİLMEZ, ÖLÇÜLÜR VE DONDURULUR ⭑

Rol her koşuda düzenli ifadeyle yeniden çıkarılsaydı, `pagePrints`
metni bir gün değiştiğinde rol de sessizce değişirdi. Bu yüzden rol bir
kez ölçülür ve manuscript'e `furniture` alanı olarak YAZILIR; dizgi
artık prozayı değil, BEYAN EDİLMİŞ ROLÜ okur.

  ./04_BUILD/furniture_roles.py            rolleri ölç ve manuscript'e yaz
  ./04_BUILD/furniture_roles.py --check    beyan ölçümle uyuşuyor mu
  ./04_BUILD/furniture_roles.py --report   dağılım tablosu

Betik İDEMPOTENTTİR: ikinci koşu hiçbir şeyi değiştirmez.

Çıkış kodları:  0 = tamam   1 = KIRMIZI   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BOOK = os.path.join(ROOT, "02_MANUSCRIPT", "book.json")

# Ölçüm kalıpları. `qa_design § ⑨` AYNI kalıpları kullanır — iki yerde
# iki farklı kalıp, iki farklı gerçek demektir.
WRITING_LINE_RE = re.compile(
    r"\b([a-z]+|\d+)\s+(?:empty\s+|ruled\s+|blank\s+)*writing\s+lines?\b", re.I)
PLATE_STAR_BOX_RE = re.compile(r"\bstar box\b", re.I)
NUMWORD = {"no": 0, "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
           "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
           "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
           "a": 1, "an": 1}


def jload(p, default=None):
    if not os.path.isfile(p):
        return default
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def measure(act):
    """Bir sayfanın mobilyasını ÖLÇER. Beyan değil, prozadan ölçüm."""
    blob = " | ".join(act.get("pagePrints") or [])
    lines = 0
    for m in WRITING_LINE_RE.finditer(blob):
        w = m.group(1).lower()
        lines += int(w) if w.isdigit() else NUMWORD.get(w, 1)
    return {
        "plateStarBox": bool(PLATE_STAR_BOX_RE.search(blob)),
        "plateWritingLines": lines,
    }


def roles_for(act):
    """Ölçümden ROL türetir.

    Kural tek cümledir: **levha basıyorsa dizgi basmaz.**"""
    m = measure(act)
    has_seal = bool(act.get("sealSlot"))
    return {
        "starBox": ("plate" if m["plateStarBox"] else
                    ("typeset" if has_seal else "none")),
        "writingLines": ("plate" if m["plateWritingLines"] else
                         ("typeset" if (act.get("writingSpaceLines") or 0)
                          else "none")),
        "plateWritingLines": m["plateWritingLines"],
        "$measuredBy": "04_BUILD/furniture_roles.py",
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()

    print("=" * 74)
    print("  SAYFA MOBİLYASI ROL AYRIMI")
    print("=" * 74)

    book = jload(BOOK)
    if book is None:
        # ⚠ Manuscript depoda durmaz (K10). Yokluğu bir kusur DEĞİLDİR.
        print("  ⊘ manuscript depoda yok (K10) — BOŞ KOŞTU")
        print("=" * 74)
        return 0

    acts = book.get("activities", [])
    stale, changed = [], 0
    from collections import Counter
    dist = Counter()

    for a in acts:
        want = roles_for(a)
        dist[(want["starBox"], want["writingLines"])] += 1
        cur = a.get("furniture")
        if cur != want:
            stale.append(a["activityId"])
            if not (args.check or args.report):
                a["furniture"] = want
                changed += 1

    print("  sayfa: %d" % len(acts))
    print("\n── rol dağılımı (yıldız kutusu · yazma satırı) ──")
    for (sb, wl), n in sorted(dist.items(), key=lambda kv: -kv[1]):
        print("  %-8s · %-8s  %3d sayfa" % (sb, wl, n))

    if args.report:
        print("\n── dizginin ARTIK ÇİZMEYECEĞİ ──")
        print("  yıldızlı kutu : %d sayfa (levha basıyor)"
              % sum(n for (sb, _), n in dist.items() if sb == "plate"))
        print("  yazma satırı  : %d sayfa (levha basıyor)"
              % sum(n for (_, wl), n in dist.items() if wl == "plate"))
        print("=" * 74)
        return 0

    if args.check:
        if stale:
            print("\n  ✗ %d sayfanın `furniture` beyanı ÖLÇÜMLE UYUŞMUYOR" % len(stale))
            print("     ilk beşi: %s" % stale[:5])
            print("\n  Tazele: ./04_BUILD/furniture_roles.py")
            print("=" * 74)
            return 1
        print("\n  ✅ bütün roller ölçümle aynı")
        print("=" * 74)
        return 0

    if changed:
        with open(BOOK, "w", encoding="utf-8") as fh:
            json.dump(book, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print("\n  yazıldı: %s (%d sayfa güncellendi)"
              % (os.path.relpath(BOOK, ROOT), changed))
    else:
        print("\n  değişiklik yok — roller zaten güncel")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
