#!/usr/bin/env python3
"""
ÇOCUK TEST PAKETİ ÜRETECİ — The Myth Hunter's Field Book
================================================================================
Testçi-görünür sayfaları, veli talimatını ve boş kayıt formunu üretir.

⭑ BU BETİK BİR ŞEYİ ÜRETMEYİ REDDEDER ⭑

    Kurucu gerçek çocuk testçi onaylamadan TÜRKÇE test materyali üretmez.

Gerekçe tek cümledir ve bu projenin en sert kuralına bağlıdır:

    Sahte test materyali, sahte test kaydının bir adım öncesidir.

Dosyada duran Türkçe bir test sayfası, bir testin YAPILDIĞINI ima eder.
Yapılmadıysa o dosya bir yalanın başlangıcıdır. Bu yüzden kapı
`project_config.json § founder.childTesters.founderConfirmed` alanına
bakar ve `false` iken `--lang tr` çağrısını çıkış kodu 3 ile reddeder.

İngilizce paket her zaman üretilebilir: o ticari metnin kendisidir ve
zaten yazılmıştır — üretmek yeni bir iddia doğurmaz.

KULLANIM

    child_test_pack.py                     → İngilizce paket, ekrana
    child_test_pack.py --out DIZIN         → dosyaya yaz
    child_test_pack.py --lang tr           → REDDEDİLİR (testçi yokken)
    child_test_pack.py --activities a,b,c  → yalnızca seçilen sayfalar

⚠ ÜRETİLEN PAKET CEVAP TAŞIMAZ. Testçi sayfayı çözecek; cevabı görmesi
testin kendisini yok eder. Cevaplar `--with-key` ile AYRI bir dosyaya
yazılır ve o dosya `.gitignore` kapsamındaki dizine gider.

TASARIM: yalnızca Python standart kütüphanesi (karar K7).

Çıkış kodları:  0 = üretildi   2 = kullanım hatası   3 = REDDEDİLDİ
"""

from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CONFIG = os.path.join(ROOT, "project_config.json")
ACTIVITY_INDEX = os.path.join(ROOT, "01_SOURCE", "activity_index.json")
BOOK = os.path.join(ROOT, "02_MANUSCRIPT", "book.json")

PARENT_BRIEF_EN = """\
FIELD TEST — NOTE FOR THE ADULT

We are testing the PAGE, not the child. There is no score and no pass mark.

Please:
  · Do not explain the page. If the child asks what it means, say
    "however it looks to you" and wait.
  · Do not give or hint at the answer, and try not to nod or smile
    at the right one.
  · Let the child stop at any time. Where a child gets stuck is the
    most useful thing we can learn.
  · If you did have to help, please write down what you said. It does
    not spoil the record — it is what makes the record usable.

Time: 20-30 minutes, at most four pages.

We do not collect names, schools, addresses, dates of birth, photographs
or recordings. The record holds an anonymous code, an age and a result.
"""

RECORD_FORM = """\
SESSION RECORD  (anonymous)

  tester code ....... tester-__          (never a real name)
  age ............... __
  date .............. ____-__-__

  page .............. ______________________________
  started ........... __:__      ended ... __:__
  understood unaided  yes / no
  result ............ solved / partial / stuck
  hints used ........ 0 / 1 / 2
  difficulty felt ... too easy / about right / too hard
  mood .............. bored / enjoying / tense / neutral

  where the child stopped or read twice:
  ______________________________________________________________

  what the child misread:
  ______________________________________________________________

  anything an adult said (quote it):
  ______________________________________________________________

  the child's own words:
  ______________________________________________________________
"""


def load(path, required=True):
    if not os.path.isfile(path):
        if required:
            print("HATA: dosya yok: %s" % os.path.relpath(path, ROOT),
                  file=sys.stderr)
            sys.exit(2)
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def merged(index_doc, book_doc):
    design = {a["activityId"]: a for a in (index_doc or {}).get("activities", [])}
    out = []
    for p in (book_doc or {}).get("activities", []):
        base = dict(design.get(p.get("activityId"), {}))
        base.update(p)
        out.append(base)
    out.sort(key=lambda a: a.get("pageOrder", 999))
    return out


def render_page(a: dict) -> str:
    """Testçi sayfası. CEVAP TAŞIMAZ."""
    lines = []
    lines.append("=" * 66)
    lines.append("  PAGE %s   %s" % (a.get("pageOrder", "?"),
                                     "*" * int(a.get("difficulty") or 1)))
    lines.append("=" * 66)
    lines.append("")
    lines.append(a.get("prompt", ""))
    lines.append("")
    if a.get("fieldNote"):
        lines.append("Field note: " + a["fieldNote"])
        lines.append("")
    for i, s in enumerate(a.get("steps") or [], 1):
        lines.append("  %d. %s" % (i, s))
    lines.append("")
    n = int(a.get("writingSpaceLines") or 0)
    if n:
        lines.append("  Write your answer here:")
        for _ in range(n):
            lines.append("  " + "_" * 56)
        lines.append("")
    if a.get("sealSlot"):
        lines.append("  [*%d]  SEAL BOX -- write the word, then carry letter %s"
                     % (a["sealSlot"], a.get("sealStarIndex", "?")))
        lines.append("        " + "_" * 40)
        lines.append("")
    if a.get("hints"):
        lines.append("  Stuck? Turn to the hint page.")
        lines.append("")
    if a.get("parentNote"):
        lines.append("  ADULT: " + a["parentNote"])
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lang", default="en",
                    help="paket dili · 'tr' KURUCU ONAYI gerektirir")
    ap.add_argument("--out", default=None, help="çıktı dizini")
    ap.add_argument("--activities", default=None,
                    help="virgülle ayrılmış activityId listesi")
    ap.add_argument("--with-key", action="store_true",
                    help="cevapları AYRI bir dosyaya yaz (depo dışı dizine)")
    args = ap.parse_args()

    cfg = load(CONFIG)
    ct = cfg.get("founder", {}).get("childTesters", {})
    lang_cfg = cfg.get("language", {})
    commercial = lang_cfg.get("commercial", "en")
    test_langs = lang_cfg.get("testOnly", [])

    print("=" * 74)
    print("  ÇOCUK TEST PAKETİ · dil: %s" % args.lang)
    print("=" * 74)

    # ── REDDETME KAPISI ────────────────────────────────────────────────────
    if args.lang != commercial:
        if args.lang not in test_langs:
            print("\n  ⛔ REDDEDİLDİ: '%s' ne ticari dil ne de tanımlı bir "
                  "test dili." % args.lang)
            print("     Tanımlı test dilleri: %s" % (test_langs or "yok"))
            return 3
        if not ct.get("founderConfirmed"):
            print("\n  ⛔ REDDEDİLDİ — TESTÇİ ONAYI YOK")
            print()
            print("     founder.childTesters.founderConfirmed = false")
            print("     founder.childTesters.availableTesters  = %s"
                  % ct.get("availableTesters", 0))
            print()
            print("     '%s' dilinde test materyali ancak GERÇEK testçiler"
                  % args.lang)
            print("     onaylandıktan sonra üretilir.")
            print()
            print("     Dosyada duran bir test sayfası, bir testin")
            print("     YAPILDIĞINI ima eder. Yapılmadı.")
            print()
            print("     Sahte test materyali, sahte test kaydının bir adım")
            print("     öncesidir. Bu betik o adımı atmaz.")
            print("=" * 74)
            return 3

    index_doc = load(ACTIVITY_INDEX, required=False)
    book_doc = load(BOOK, required=False)
    if not book_doc:
        print("\n  ⊘ manuscript bu makinede yok — üretilecek sayfa yok")
        print("=" * 74)
        return 0

    acts = merged(index_doc, book_doc)
    if args.activities:
        want = {x.strip() for x in args.activities.split(",") if x.strip()}
        acts = [a for a in acts if a.get("activityId") in want]
    if not acts:
        print("\n  ⊘ seçilen sayfa yok")
        return 2

    pages = "\n".join(render_page(a) for a in acts)
    body = (PARENT_BRIEF_EN + "\n" + "=" * 66 + "\n\n"
            + pages + "\n" + "=" * 66 + "\n\n" + RECORD_FORM)

    if args.out:
        os.makedirs(args.out, exist_ok=True)
        pack = os.path.join(args.out, "tester-pack-%s.txt" % args.lang)
        with open(pack, "w", encoding="utf-8") as fh:
            fh.write(body)
        print("\n  ✅ %d sayfa yazıldı → %s" % (len(acts), pack))
        if args.with_key:
            keyp = os.path.join(args.out, "answer-key-%s.txt" % args.lang)
            with open(keyp, "w", encoding="utf-8") as fh:
                for a in acts:
                    fh.write("%s: %s\n" % (a["activityId"],
                                           a.get("answer")
                                           or a.get("expectedResult") or ""))
            print("  ⚠ cevap anahtarı AYRI dosyada → %s" % keyp)
            print("    Bu dosya testçiye VERİLMEZ ve depoya GİRMEZ.")
    else:
        print()
        print(body)

    print("=" * 74)
    print("  Testçi: %d · onay: %s · dış doğrulama: %s"
          % (ct.get("availableTesters", 0), ct.get("founderConfirmed"),
             ct.get("externalValidation")))
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
