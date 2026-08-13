#!/usr/bin/env python3
"""
VERİ BÜTÜNLÜĞÜ VE KAPSAM KAPISI — The Myth Hunter's Field Book
================================================================================
Dört soru:

  ① project_config.json kendi içinde tutarlı mı
  ② activity_index.json şemaya uyuyor mu, kimlikler tekil mi
  ③ 6 bölge × 5 aktivite tipi matrisinin her hücresi dolu mu
  ④ .gate seviyesinin GEREKTİRDİĞİ kapsam sağlanmış mı

③ bu projeye özgüdür: "Kuzeyin Buzları bölgesinde 4 tasnif aktivitesi
bulamıyorum" sorununu 90. aktivitede öğrenmek pahalıdır. Matris Faz 1'de
kurulur ve her fazda denetlenir.

TASARIM: yalnızca Python standart kütüphanesi (karar K7).

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
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
REGION_INDEX = os.path.join(ROOT, "01_SOURCE", "region_index.json")

VALID_GATES = ["phase0", "phase1", "phase2", "phase3", "phase4", "phase5", "release"]
VALID_STATUS = ["candidate", "researched", "locked", "written", "dropped"]
VALID_INHERIT = ["inherited-provisional", "inherited-verified", "new-researched"]
VALID_RESTRICTION = ["open", "attributed", "restricted", "excluded"]


class Report:
    def __init__(self, verbose):
        self.verbose = verbose
        self.errors = []
        self.warnings = []
        self.checks = 0
        self.facts = {}

    def ok(self, label):
        self.checks += 1
        if self.verbose:
            print("  ✓ %s" % label)

    def fail(self, label):
        self.checks += 1
        self.errors.append(label)
        print("  ✗ %s" % label)

    def warn(self, label):
        self.warnings.append(label)
        print("  ! %s" % label)

    def check(self, cond, label):
        self.ok(label) if cond else self.fail(label)
        return cond


def load_json(path, rep, required=True):
    if not os.path.exists(path):
        if required:
            rep.fail("dosya yok: %s" % os.path.relpath(path, ROOT))
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        rep.fail("JSON bozuk: %s — %s" % (os.path.relpath(path, ROOT), exc))
        return None


def read_gate():
    path = os.path.join(ROOT, ".gate")
    if not os.path.exists(path):
        return "phase0"
    with open(path, encoding="utf-8") as fh:
        return fh.read().strip()


def check_config(cfg, rep):
    print("\n── yapılandırma bütünlüğü ──")
    for key in ("project", "founder", "audience", "scope", "inheritance",
                "safety", "solvability", "progression", "production", "gates", "style"):
        rep.check(key in cfg, "config bloğu var: %s" % key)

    scope = cfg.get("scope", {})
    types = scope.get("activityTypes", [])
    regions = scope.get("regionsHypothesis", [])
    rep.check(len(types) == scope.get("activityTypesRequired", -1),
              "aktivite tipi sayısı uyuşuyor (%d)" % len(types))
    rep.check(len(regions) == scope.get("regions", -1),
              "bölge sayısı uyuşuyor (%d)" % len(regions))
    rep.check(len({t.get("id") for t in types}) == len(types), "tip kimlikleri tekil")
    rep.check(len({r.get("id") for r in regions}) == len(regions), "bölge kimlikleri tekil")

    # Matris kapasitesi: her bölgede minimum tip sayıları toplamı, bölge
    # başına düşen aktivite sayısını AŞMAMALI — aşarsa matris imkânsızdır.
    per_region_min = sum(t.get("perRegionMin", 0) for t in types)
    per_region_budget = (scope.get("activities", 0) // max(1, scope.get("regions", 1)))
    rep.check(per_region_min <= per_region_budget,
              "matris uygulanabilir: bölge başına min %d ≤ bütçe %d"
              % (per_region_min, per_region_budget))

    # Devralma sözleşmesi
    inh = cfg.get("inheritance", {})
    rep.check(set(inh.get("lockRequiresStatus", [])) <= set(VALID_INHERIT),
              "devralma kilidi geçerli durumlara işaret ediyor")
    rep.check("inherited-provisional" not in inh.get("lockRequiresStatus", []),
              "DOĞRULANMAMIŞ devralma ile locked OLAMAZ")

    # Üretim ekonomisi
    prod = cfg.get("production", {})
    pc = prod.get("kdpPrintCost", {})
    pages = scope.get("pageTarget", 0)
    for ed in prod.get("editionsHypothesis", []):
        if not ed.get("enabled") or ed.get("list") is None:
            continue
        band = pc.get("paperbackLargeTrimBW" if ed["id"] == "paperback"
                      else "hardcoverLargeTrimBW", {})
        if not band:
            continue
        cost = band.get("fixed", 0) + pages * band.get("perPage", 0)
        rate = (pc.get("royaltyRateAtOrAbove999", 0.6) if ed["list"] >= 9.99
                else pc.get("royaltyRateBelow999", 0.5))
        royalty = ed["list"] * rate - cost
        rep.facts["royalty_%s" % ed["id"]] = round(royalty, 2)
        rep.check(royalty > 0, "%s telifi pozitif: %.2f $ (baskı %.2f $ @ %d s.)"
                  % (ed["id"], royalty, cost, pages))

    saf = cfg.get("safety", {})
    rep.check(len(saf.get("forbiddenActivityFrames", [])) >= 5,
              "yasak aktivite çerçeveleri tanımlı (%d)"
              % len(saf.get("forbiddenActivityFrames", [])))
    rep.check(saf.get("parentReadingsRequired", 0) >= 2,
              "en az iki ebeveyn okuması şartı duruyor")


def check_activities(cfg, acts, regions, gate, rep):
    print("\n── aktivite envanteri ──")
    if acts is None:
        if gate == "phase0":
            rep.warn("activity_index.json yok — phase0'da beklenen (Faz 1 üretir)")
            rep.facts["activities_total"] = 0
            return
        rep.fail("activity_index.json yok ama kapı %s" % gate)
        return

    entries = acts.get("activities", []) if isinstance(acts, dict) else acts
    rep.facts["activities_total"] = len(entries)

    ids = [a.get("activityId") for a in entries]
    rep.check(len(ids) == len(set(ids)), "aktivite kimlikleri tekil (%d)" % len(ids))
    rep.check(all(ids), "her aktivitenin activityId'si var")

    type_ids = {t["id"] for t in cfg["scope"]["activityTypes"]}
    region_ids = {r["id"] for r in cfg["scope"]["regionsHypothesis"]}
    if regions:
        rentries = regions.get("regions", []) if isinstance(regions, dict) else regions
        if rentries:
            region_ids = {r.get("id") for r in rentries}

    bad_type = [a["activityId"] for a in entries if a.get("type") not in type_ids]
    rep.check(not bad_type, "her aktivite tanımlı bir tipte" +
              ("" if not bad_type else " — ihlal: %s" % bad_type[:5]))

    bad_region = [a["activityId"] for a in entries if a.get("region") not in region_ids]
    rep.check(not bad_region, "her aktivite tanımlı bir bölgede" +
              ("" if not bad_region else " — ihlal: %s" % bad_region[:5]))

    bad_status = [a["activityId"] for a in entries if a.get("status") not in VALID_STATUS]
    rep.check(not bad_status, "durum alanları geçerli" +
              ("" if not bad_status else " — ihlal: %s" % bad_status[:5]))

    bad_inh = [a["activityId"] for a in entries
               if a.get("inheritanceStatus") not in VALID_INHERIT]
    rep.check(not bad_inh, "devralma durumları geçerli" +
              ("" if not bad_inh else " — EKSİK: %s" % bad_inh[:5]))

    bad_restr = [a["activityId"] for a in entries
                 if a.get("restrictionStatus") not in VALID_RESTRICTION]
    rep.check(not bad_restr, "kısıt taraması yapılmış" +
              ("" if not bad_restr else " — TARANMAMIŞ: %s" % bad_restr[:5]))

    # DEVRALMA KİLİDİ — bu projenin en önemli tek kuralı
    lock_ok = set(cfg["inheritance"]["lockRequiresStatus"])
    violators = [a["activityId"] for a in entries
                 if a.get("status") in ("locked", "written")
                 and a.get("inheritanceStatus") not in lock_ok]
    rep.check(not violators,
              "DOĞRULANMAMIŞ devralmaya dayanan locked aktivite yok" +
              ("" if not violators else " — İHLAL: %s" % violators[:5]))

    cultures = {a.get("culture") for a in entries if a.get("culture")}
    rep.facts["cultures_total"] = len(cultures)
    for st in VALID_STATUS:
        rep.facts["activities_%s" % st] = sum(1 for a in entries if a.get("status") == st)
    for ist in VALID_INHERIT:
        rep.facts["inherit_%s" % ist] = sum(
            1 for a in entries if a.get("inheritanceStatus") == ist)


def check_matrix(cfg, acts, rep):
    print("\n── bölge × tip matrisi ──")
    if acts is None:
        rep.warn("envanter yok — matris denetlenemiyor")
        return
    entries = acts.get("activities", []) if isinstance(acts, dict) else acts
    if not entries:
        return

    types = cfg["scope"]["activityTypes"]
    regions = cfg["scope"]["regionsHypothesis"]
    holes = []
    for r in regions:
        for t in types:
            n = sum(1 for a in entries
                    if a.get("region") == r["id"] and a.get("type") == t["id"])
            if n < t.get("perRegionMin", 0):
                holes.append("%s×%s=%d(<%d)" % (r["id"], t["id"], n,
                                                t.get("perRegionMin", 0)))
    rep.facts["matrix_holes"] = len(holes)
    rep.check(not holes, "matrisin 30 hücresi de dolu" +
              ("" if not holes else " — BOŞ: %s" % holes[:6]))


def check_gate_scope(cfg, gate, rep):
    print("\n── kapı seviyesi kapsam denetimi (%s) ──" % gate)
    req = cfg.get("gates", {}).get("requirements", {}).get(gate)
    if req is None:
        rep.fail("kapı seviyesi config'de tanımsız: %s" % gate)
        return
    total = rep.facts.get("activities_total", 0)
    locked = rep.facts.get("activities_locked", 0) + rep.facts.get("activities_written", 0)
    written = rep.facts.get("activities_written", 0)

    rep.check(total >= req["activitiesCandidate"],
              "aday aktivite ≥ %d (ölçülen %d)" % (req["activitiesCandidate"], total))
    rep.check(locked >= req["activitiesLocked"],
              "kilitli aktivite ≥ %d (ölçülen %d)" % (req["activitiesLocked"], locked))
    rep.check(written >= req["activitiesWritten"],
              "yazılmış aktivite ≥ %d (ölçülen %d)" % (req["activitiesWritten"], written))

    if cfg["scope"].get("locked") and gate in ("phase4", "phase5", "release"):
        rep.check(rep.facts.get("cultures_total", 0) >= cfg["scope"]["cultures"],
                  "kültür sayısı alt başlığı doğruluyor (≥ %d)" % cfg["scope"]["cultures"])


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", default=None)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    gate = args.gate or read_gate()
    if gate not in VALID_GATES:
        print("HATA: geçersiz kapı seviyesi: %s" % gate, file=sys.stderr)
        return 2

    print("=" * 74)
    print("  VERİ BÜTÜNLÜĞÜ VE KAPSAM · kapı: %s" % gate)
    print("=" * 74)

    rep = Report(args.verbose)
    cfg = load_json(CONFIG, rep)
    if cfg is None:
        print("\n⛔ project_config.json okunamadı")
        return 1

    check_config(cfg, rep)
    acts = load_json(ACTIVITY_INDEX, rep, required=(gate != "phase0"))
    regions = load_json(REGION_INDEX, rep, required=False)
    check_activities(cfg, acts, regions, gate, rep)
    check_matrix(cfg, acts, rep)
    check_gate_scope(cfg, gate, rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · kapı: %s" % (rep.checks, gate))
        status = "pass"
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": status, "gate": gate, "checks": rep.checks,
                       "errors": rep.errors, "warnings": rep.warnings,
                       "facts": rep.facts}, fh, ensure_ascii=False, indent=2)
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
