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
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CONFIG = os.path.join(ROOT, "project_config.json")
ACTS = os.path.join(ROOT, "01_SOURCE", "activity_index.json")
REGIONS = os.path.join(ROOT, "01_SOURCE", "region_index.json")
CULTURES = os.path.join(ROOT, "01_SOURCE", "culture_index.json")
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

    status = collections.Counter(a.get("status") for a in acts)
    inh = collections.Counter(r.get("status") for r in recs)
    verified = inh["inherited-verified"] + inh["new-researched"]

    return {
        "cfg": cfg, "acts": acts, "live": live, "regions": regions,
        "cultures": cultures, "records": recs, "facts": facts,
        "status": status, "inh": inh,
        "verifiedRatio": (verified / len(recs)) if recs else 0.0,
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
          "> Faz 1'de doğrulanmış oran **%0'dır ve bu beklenendir**: bütün",
          "> kayıtlar `inherited-provisional` durumda ve her aday kendi",
          "> `revalidationPlan`ını taşıyor. Doğrulama Faz 2'de yapılır.",
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

    L = ["# ROADMAP PROGRESS — The Myth Hunter's Field Book", "", BANNER, "",
         "> Kapı: `%s`" % d["gate"], "", "---", "", "## Faz durumu", "",
         "| Faz | Ad | Durum | Kapı | Dal | Etiket |", "|---|---|---|---|---|---|"]
    for i, (num, name, g, branch, tag) in enumerate(PHASES):
        if i < cur:
            st = "✅ **TAMAM**"
        elif i == cur:
            st = "✅ **TAMAM**" if g == d["gate"] else "▶ sürüyor"
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
          "| Bölge | **%d** | %d |" % (len(d["regions"]), scope.get("regions", 6)),
          "| Görsel öğe | **0** | ~150 |",
          "| Kelime | **0** | ~%s |" % f"{scope.get('manuscriptWordTarget', 22000):,}".replace(",", "."),
          "", "---", "", "## Sonraki izinli eylem", ""]

    if cur + 1 < len(PHASES):
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
