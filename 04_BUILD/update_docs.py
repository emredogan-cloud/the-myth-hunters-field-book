#!/usr/bin/env python3
"""
ÜRETİLEN BELGELER — The Myth Hunter's Field Book
================================================================================
`BOOK_STATS.md` ve `ROADMAP_PROGRESS.md` **elle yazılmaz**. İkisi de bu
betikten üretilir ve `--check` bayrağıyla BAYAT olup olmadıkları denetlenir.

Gerekçe: iki belge de bootstrap'ta *"buradaki her sayı ölçülecektir; hiçbiri
elle yazılmayacaktır"* diye söz verdi. Elle yazılan bir sayı bir süre sonra
sessizce yanlış olur ve kimse fark etmez — çünkü onu kimse denetlemez.

  ./04_BUILD/update_docs.py            belgeleri tazele
  ./04_BUILD/update_docs.py --check    bayatsa KIRMIZI (qa_all.sh bunu koşar)

TASARIM: yalnızca Python standart kütüphanesi (karar K7).

Çıkış kodları:  0 = güncel/yazıldı   1 = BAYAT   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CONFIG = os.path.join(ROOT, "project_config.json")
ACTS = os.path.join(ROOT, "01_SOURCE", "activity_index.json")
REGIONS = os.path.join(ROOT, "01_SOURCE", "region_index.json")
CULTURES = os.path.join(ROOT, "01_SOURCE", "culture_index.json")
BOOK = os.path.join(ROOT, "02_MANUSCRIPT", "book.json")
MANIFEST = os.path.join(ROOT, "01_SOURCE", "inherited", "IMPORT_MANIFEST.json")
PAGE_REPORT = os.path.join(ROOT, "06_REPORTS", "page-budget.json")

BOOK_STATS = os.path.join(ROOT, "BOOK_STATS.md")
ROADMAP_PROGRESS = os.path.join(ROOT, "ROADMAP_PROGRESS.md")

BANNER = "<!-- ÜRETİLMİŞTİR — 04_BUILD/update_docs.py · ELLE DÜZENLEMEYİN -->"

PHASES = [
    ("0", "Bootstrap", "phase0", "main", "—"),
    ("1", "Devralma mimarisi, taksonomi, yaş çerçevesi", "phase1", "faz/1-devralma", "v0.1.0"),
    ("2", "Pilot: bir bölge + çocuk saha testi", "phase2", "faz/2-pilot", "v0.2.0"),
    ("3", "Bölge bloğu I — üç bölge", "phase3", "faz/3-blok-1", "v0.3.0"),
    ("4", "Bölge bloğu II + final görev", "phase4", "faz/4-blok-2", "v0.4.0"),
    ("5", "Editoryal yakınsama + sayfa tasarımı", "phase5", "faz/5-yakinsama", "v0.5.0"),
    ("6", "Nihai üretim + KDP paketi", "release", "faz/6-uretim", "v1.0.0"),
]
ORDER = [p[2] for p in PHASES]


def jload(path, default=None):
    if not os.path.isfile(path):
        return default
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def gate() -> str:
    p = os.path.join(ROOT, ".gate")
    if not os.path.isfile(p):
        return "phase0"
    with open(p, encoding="utf-8") as fh:
        return fh.read().strip()


def collect() -> dict:
    cfg = jload(CONFIG, {})
    acts_doc = jload(ACTS, {"activities": []})
    acts = acts_doc.get("activities", [])
    live = [a for a in acts if a.get("status") != "dropped"]
    regions = (jload(REGIONS, {}) or {}).get("regions", [])
    cultures = (jload(CULTURES, {}) or {}).get("cultures", [])
    man = jload(MANIFEST, {"records": []})
    recs = man.get("records", [])
    page = jload(PAGE_REPORT, {}) or {}
    facts = page.get("facts", {})

    # Kelime sayısı ÖLÇÜLÜR. Manuscript depoda durmaz; yoksa 0 kalır ve
    # bu bir kusur değil, kabul edilmiş düzendir (K11).
    book = jload(BOOK, {"activities": []}) or {"activities": []}
    words = 0
    for a in book.get("activities", []):
        blob = " ".join([a.get("prompt", ""), a.get("fieldNote", ""),
                         a.get("expectedResult", "")]
                        + list(a.get("steps") or [])
                        + list(a.get("hints") or []))
        words += len(re.findall(r"[A-Za-z'\u02bb\u2019-]+", blob))
    # \u26a0 FAZ 3'TE D\u00dcZELT\u0130LD\u0130 \u2014 bu sat\u0131r iki kez yanl\u0131\u015ft\u0131 ve ikisi de sessizdi.
    #
    #   \u2460 Alan ad\u0131 `text` diye okunuyordu; manuscript'te ad\u0131 `openingText`.
    #      Yani b\u00f6lge a\u00e7\u0131l\u0131\u015f\u0131n\u0131n 146 kelimesi H\u0130\u00c7 SAYILMADI ve Faz 2'nin
    #      "1.015 kelime" \u00f6l\u00e7\u00fcm\u00fc ger\u00e7ekte 1.161 idi.
    #   \u2461 Alan TEK\u0130LD\u0130. Faz 3 iki b\u00f6lge daha yaz\u0131yor; tekil bir alan
    #      ikinci a\u00e7\u0131l\u0131\u015f\u0131 sessizce yutard\u0131.
    #
    # Bir \u00f6l\u00e7\u00fcm beti\u011finin en tehlikeli kusuru, \u00f6l\u00e7t\u00fc\u011f\u00fcn\u00fc SANMASIDIR:
    # bo\u015f d\u00f6nen bir alan s\u0131f\u0131r ekler ve hi\u00e7bir kap\u0131 k\u0131rm\u0131z\u0131 yanmaz.
    openings = book.get("regionOpenings")
    if openings is None:
        legacy = book.get("regionOpening")
        openings = [legacy] if legacy else []
    for op in openings:
        blob = " ".join([(op or {}).get("openingText", ""),
                         (op or {}).get("terrainLine", "")])
        words += len(re.findall(r"[A-Za-z'\u02bb\u2019-]+", blob))

    # G\u00f6rsel \u015eARTNAMES\u0130 \u2260 g\u00f6rsel VARLI\u011eI. \u0130kisi ayr\u0131 say\u0131l\u0131r ve ayr\u0131
    # raporlan\u0131r: \u015fartname Faz 3'te do\u011far, varl\u0131k Faz 5'te \u00fcretilir.
    # Birini di\u011ferinin yerine saymak, olmayan bir varl\u0131\u011f\u0131 var g\u00f6stermek olur.
    visual_specs = sum(1 for a in book.get("activities", []) if a.get("visualSpec"))
    page_prints = sum(len(a.get("pagePrints") or [])
                      for a in book.get("activities", []))

    status = collections.Counter(a.get("status") for a in acts)
    inh = collections.Counter(r.get("status") for r in recs)
    verified = inh["inherited-verified"] + inh["new-researched"]

    return {
        "cfg": cfg, "acts": acts, "live": live, "regions": regions,
        "cultures": cultures, "records": recs, "facts": facts,
        "status": status, "inh": inh,
        "verifiedRatio": (verified / len(recs)) if recs else 0.0,
        "words": words,
        "visualSpecs": visual_specs,
        "pagePrints": page_prints,
        "regionsWritten": len({a.get("region") for a in live
                               if a.get("status") == "written" and a.get("region")}),
        "cultureCount": len({a.get("culture") for a in live if a.get("culture")}),
        "typeByRegion": {
            r["id"]: collections.Counter(a["type"] for a in live
                                         if a["region"] == r["id"])
            for r in regions
        },
        "safety": collections.Counter(a.get("safetyClass") for a in live),
        "gate": gate(),
    }


def render_book_stats(d: dict) -> str:
    cfg, facts = d["cfg"], d["facts"]
    scope = cfg.get("scope", {})
    types = [t["id"] for t in scope.get("activityTypes", [])]
    tmin = {t["id"]: t.get("perRegionMin", 0) for t in scope.get("activityTypes", [])}

    L = ["# BOOK STATS — The Myth Hunter's Field Book", "", BANNER, "",
         "> Kapı: `%s` · Bu dosya **ölçümden üretilir**; hiçbir sayı elle yazılmaz."
         % d["gate"], "",
         "## 1. Tek bakışta", "",
         "| | Ölçülen | Hedef |", "|---|---:|---:|"]
    L += [
        "| Aday aktivite | **%d** | ≥%d |" % (len(d["live"]), scope.get("activityCandidateMin", 160)),
        "| Kilitli aktivite | **%d** | %d |" % (d["status"]["locked"] + d["status"]["written"], scope.get("activities", 120)),
        "| Yazılmış aktivite | **%d** | %d |" % (d["status"]["written"], scope.get("activities", 120)),
        "| Düşürülmüş aday | **%d** | — |" % d["status"]["dropped"],
        "| Kültür | **%d** | %d |" % (d["cultureCount"], scope.get("cultures", 22)),
        "| Bölge | **%d** | %d |" % (len(d["regions"]), scope.get("regions", 6)),
        "| Matris deliği (6×5) | **%d** | 0 |" % _holes(d, tmin),
        "| Kısıt taraması | **%d/%d** | muafiyetsiz |"
        % (sum(1 for a in d["live"] if a.get("restrictionStatus")), len(d["live"])),
        "| Görsel öğe | **0** | ~150 |",
        "",
        "## 2. Güvenlik sınıfı", "",
        "| Sınıf | Aday | Oran | Hedef |", "|---|---:|---:|---:|",
    ]
    n = max(1, len(d["live"]))
    for cls, target in (("safe", "≥%90"), ("safe-with-adult", "≤%10"), ("do-not-use", "0")):
        c = d["safety"].get(cls, 0)
        L.append("| `%s` | %d | %%%.1f | %s |" % (cls, c, 100 * c / n, target))

    L += ["", "## 3. Devralma durumu", "",
          "| Durum | Kayıt |", "|---|---:|"]
    for s in ("inherited-provisional", "inherited-verified", "new-researched"):
        L.append("| `%s` | %d |" % (s, d["inh"].get(s, 0)))
    L += ["| **Toplam** | **%d** |" % len(d["records"]),
          "| **Doğrulanmış oran** | **%%%.1f** (Faz 1 ölçütü: doğrulanmış VEYA planlı) |"
          % (100 * d["verifiedRatio"]),
          "",
          "> Doğrulama KAYIT düzeyinde değil KULLANIM düzeyinde ilerler:",
          "> bir kayıt, ondan CEVAP ÜRETEN bir sayfa yazıldığında",
          "> doğrulanır. Bu yüzden oran aktivite üretimiyle birlikte",
          "> yükselir ve Faz 2 sonunda %100 OLMASI BEKLENMEZ.",
          "> Alan düzeyindeki kanıt: `01_SOURCE/research/*-revalidation.json`",
          ""]

    L += ["## 4. Sayfa ve fiyat modeli", ""]
    if facts:
        L += ["| | |", "|---|---:|",
              "| Aktivite sayfası (ölçülen ağırlıktan) | %s |" % facts.get("activityPages", "—"),
              "| Ön madde | %s |" % facts.get("frontMatter", "—"),
              "| Bölge başına yapı sayfası | %s |" % facts.get("structuralPerRegion", "—"),
              "| Final görev | %s |" % facts.get("finalQuest", "—"),
              "| Arka madde | %s |" % facts.get("backMatter", "—"),
              "| **Model (forma hizalı)** | **%s** |" % facts.get("modelPagesSignatureAligned", "—"),
              "| Yol haritası hedefi | %s |" % scope.get("pageTarget", "—"),
              "| Sapma | %%%+.1f |" % facts.get("pageDeltaPct", 0),
              "| Ciltsiz baskı maliyeti | %s $ |" % facts.get("printCost_paperback", "—"),
              "| **Ciltsiz telif** | **%s $** |" % facts.get("royalty_paperback", "—"),
              "| Başabaş ACOS | %%%s |" % facts.get("breakevenAcos_paperback", "—"),
              ""]
    else:
        L += ["> Ölçüm yok — `04_BUILD/page_budget.py --json 06_REPORTS/page-budget.json`", ""]

    L += ["## 5. Bölge × tip matrisi", "",
          "| Bölge | " + " | ".join(types) + " | kota |",
          "|---" * (len(types) + 2) + "|"]
    for r in d["regions"]:
        c = d["typeByRegion"].get(r["id"], {})
        L.append("| %s | %s | %d |" % (r["id"],
                                       " | ".join(str(c.get(t, 0)) for t in types),
                                       r.get("activityQuota", 0)))
    L.append("| **minimum** | " + " | ".join(str(tmin[t]) for t in types) + " | — |")
    L.append("")
    return "\n".join(L) + "\n"


def _holes(d: dict, tmin: dict) -> int:
    holes = 0
    for r in d["regions"]:
        c = d["typeByRegion"].get(r["id"], {})
        for t, m in tmin.items():
            if c.get(t, 0) < m:
                holes += 1
    return holes


def render_progress(d: dict) -> str:
    cur = ORDER.index(d["gate"]) if d["gate"] in ORDER else 0
    scope = d["cfg"].get("scope", {})

    ov = d["cfg"].get("founder", {}).get("phaseOverride") or {}
    active = bool(ov.get("active"))
    auth = ov.get("authorisedPhase")
    auth_i = ORDER.index(auth) if auth in ORDER else -1

    L = ["# ROADMAP PROGRESS — The Myth Hunter's Field Book", "", BANNER, "",
         "> Kapı: `%s`" % d["gate"], ""]

    # ⭑ AŞMA GİZLENMEZ ⭑ Kapı ile yetkilendirilen faz AYRIŞTIĞINDA bu blok
    # basılır. Basılmaması, aşmanın unutulması demektir (K27).
    if active:
        L += ["> ### ⚠ KURUCU FAZ AŞMASI ETKİN — `%s`" % ov.get("decision", "?"),
              ">",
              "> Yetkilendirilen faz: **%s** · kapı tavanı: **`%s`**"
              % (auth, ov.get("gateCeiling")),
              ">",
              "> Ertelenen blokaj: **%s** — %s"
              % (ov.get("deferredBlocker"), ov.get("deferredBlockerStatus")),
              ">",
              "> Bu aşma bir SIRAYI değiştirir, bir SONUCU üretmez:",
              "> **%s hâlâ açıktır ve çocuk oturumu YAPILMAMIŞTIR.**"
              % ov.get("deferredBlocker"),
              "> `.gate` bu yüzden `%s`'de tutulur." % ov.get("gateCeiling"),
              ""]

    L += ["---", "", "## Faz durumu", "",
          "| Faz | Ad | Durum | Kapı | Dal | Etiket |", "|---|---|---|---|---|---|"]
    for i, (num, name, g, branch, tag) in enumerate(PHASES):
        if i < cur:
            st = "✅ **TAMAM**"
        elif i == cur:
            st = "✅ **TAMAM**" if g == d["gate"] else "▶ sürüyor"
        elif active and i == auth_i:
            # Aşmayla yetkilendirilen faz "beklemede" GÖRÜNEMEZ; ama
            # "TAMAM" da değildir. Üçüncü bir durum gerekiyordu.
            st = "▶ **AŞMAYLA SÜRÜYOR (%s)**" % ov.get("decision", "aşma")
        elif active and cur < i < auth_i:
            st = "⏸ **AŞILDI — kapanmadı (%s)**" % ov.get("deferredBlocker", "")
        elif i == cur + 1:
            st = "⏸ **SIRADA**"
        else:
            st = "⏸ beklemede"
        L.append("| **%s** | %s | %s | `%s` | `%s` | %s |"
                 % (num, name, st, g, branch, tag))

    L += ["", "---", "", "## Ölçülen ilerleme", "",
          "| | Ölçülen | Hedef |", "|---|---:|---:|",
          "| Aday aktivite | **%d** | ≥%d |" % (len(d["live"]), scope.get("activityCandidateMin", 160)),
          "| Kilitli aktivite | **%d** | %d |" % (d["status"]["locked"] + d["status"]["written"], scope.get("activities", 120)),
          "| Yazılmış aktivite | **%d** | %d |" % (d["status"]["written"], scope.get("activities", 120)),
          "| Devralınan kayıt | **%d** | — |" % len(d["records"]),
          "| Kültür | **%d** | %d |" % (d["cultureCount"], scope.get("cultures", 22)),
          "| Bölge (tanımlı) | **%d** | %d |" % (len(d["regions"]), scope.get("regions", 6)),
          "| **Bölge (yazılmış)** | **%d** | %d |" % (d["regionsWritten"], scope.get("regions", 6)),
          "| Sayfa basım maddesi (`pagePrints`) | **%d** | — |" % d["pagePrints"],
          "| Görsel şartnamesi | **%d** | ~150 |" % d["visualSpecs"],
          "| Görsel varlık (üretilmiş) | **0** | ~150 |",
          "| Kelime | **%s** | ~%s |"
          % (f"{d['words']:,}".replace(",", "."),
             f"{scope.get('manuscriptWordTarget', 22000):,}".replace(",", ".")),
          "", "---", "", "## Sonraki izinli eylem", ""]

    if active and auth_i > cur:
        nxt = PHASES[auth_i]
        L += ["> **Faz %s — %s** · kurucu aşmasıyla YETKİLİ (%s)"
              % (nxt[0], nxt[1], ov.get("decision", "")), ">",
              "> Dal: `%s` · Etiket: %s" % (nxt[3], nxt[4]), ">",
              "> ⚠ Kapı `%s`'de kalır. **%s kapanmadı.**"
              % (ov.get("gateCeiling"), ov.get("deferredBlocker")), ">",
              "> Bir sonraki fazı kurucu talimatı olmadan **BAŞLATMA**."]
    elif cur + 1 < len(PHASES):
        nxt = PHASES[cur + 1]
        L += ["> **Faz %s — %s**" % (nxt[0], nxt[1]), ">",
              "> Dal: `%s` · Kapı: `%s` · Etiket: %s" % (nxt[3], nxt[2], nxt[4]), ">",
              "> ⛔ **KURUCU ONAYI OLMADAN BAŞLAMAZ.**"]
    else:
        L += ["> Proje burada biter. **AJAN DURUR.**"]
    L.append("")
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="bayatsa kırmızı yan")
    args = ap.parse_args()

    d = collect()
    targets = [(BOOK_STATS, render_book_stats(d)),
               (ROADMAP_PROGRESS, render_progress(d))]

    if args.check:
        stale = []
        for path, want in targets:
            cur = ""
            if os.path.isfile(path):
                with open(path, encoding="utf-8") as fh:
                    cur = fh.read()
            if cur != want:
                stale.append(os.path.relpath(path, ROOT))
        print("=" * 74)
        print("  ÜRETİLEN BELGELER")
        print("=" * 74)
        if stale:
            print("  ✗ BAYAT: %s" % ", ".join(stale))
            print("\n  Tazele: ./04_BUILD/update_docs.py")
            print("=" * 74)
            return 1
        print("  ✅ üretilen belgeler güncel (%d dosya)" % len(targets))
        print("=" * 74)
        return 0

    for path, want in targets:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(want)
        print("yazıldı: %s" % os.path.relpath(path, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
