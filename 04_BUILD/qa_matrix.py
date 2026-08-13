#!/usr/bin/env python3
"""
BÖLGE × TİP MATRİSİ VE KAPSAM DAĞILIMI — The Myth Hunter's Field Book
================================================================================
Bu kapı tek bir soruyu erken sorar:

    "Kuzeyin Buzları bölgesinde dört tasnif aktivitesi bulamıyorum"
    sorununu 90. aktivitede öğrenmek PAHALIDIR.

Yedi denetim:

  ① MATRİS        — 6 bölge × 5 tip = 30 hücrenin hepsi asgarinin üstünde mi
  ② KÜLTÜR        — 22 kültürün hepsi temsil ediliyor mu, kotalar tutuyor mu
  ③ ZORLUK        — havuz her bölgenin zorluk profilini besleyebiliyor mu
  ④ MÜHÜR         — yuvalar 1…N bitişik mi, her yuva TAM BİR kez dolu mu
  ⑤ TEKRAR        — yinelenen kimlik, başlık veya amaç var mı
  ⑥ AÇIK UÇLULUK  — openEnded yalnızca 'make' tipinde ve mühür beslemiyor mu
  ⑦ TERİMLER      — bölge, kültür ve kayıt kimlikleri dizinlerle uyuşuyor mu

③ NEDEN VAR: 120'lik kitap her bölgede belli sayıda ★, ★★ ve ★★★ ister.
Havuz o profili besleyemiyorsa zorluk merdiveni Faz 3'te çöker ve
"8 yaş da 12 yaş da kullanabilir" vaadi kırılır. Bu kapı Faz 1'de üç
bölgede tam olarak bu açığı buldu.

④ NEDEN VAR: mühür kitabın tamamlanma güdüsüdür. Bir yuva boşsa çocuk
bölgeyi bitiremez; iki aktivite aynı yuvayı beslerse harf çakışır.
⚠ Bu kapı mühür SÖZCÜKLERİNİ görmez ve görmemelidir — cevaplar depoda
durmaz (K10). Yalnızca YAPIYI denetler.

TASARIM: yalnızca Python standart kütüphanesi (karar K7).

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
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
ACTIVITY_INDEX = os.path.join(ROOT, "01_SOURCE", "activity_index.json")
REGION_INDEX = os.path.join(ROOT, "01_SOURCE", "region_index.json")
CULTURE_INDEX = os.path.join(ROOT, "01_SOURCE", "culture_index.json")

LIVE_STATUS = ("candidate", "researched", "locked", "written")


class Report:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks = 0
        self.facts: dict = {}

    def check(self, cond: bool, label: str) -> bool:
        self.checks += 1
        if cond:
            if self.verbose:
                print("  ✓ %s" % label)
        else:
            self.errors.append(label)
            print("  ✗ %s" % label)
        return cond

    def warn(self, label: str) -> None:
        self.warnings.append(label)
        print("  ! %s" % label)


def load(path, rep, required=True):
    if not os.path.exists(path):
        if required:
            rep.check(False, "dosya yok: %s" % os.path.relpath(path, ROOT))
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        rep.check(False, "JSON bozuk: %s — %s" % (os.path.relpath(path, ROOT), exc))
        return None


def live(acts):
    return [a for a in acts if a.get("status") in LIVE_STATUS]


# ── ① MATRİS ───────────────────────────────────────────────────────────────
def check_matrix(cfg, acts, regions, rep):
    print("\n── ① bölge × tip matrisi ──")
    types = cfg["scope"]["activityTypes"]
    holes = []
    for r in regions:
        for t in types:
            n = sum(1 for a in acts
                    if a.get("region") == r["id"] and a.get("type") == t["id"])
            if n < t.get("perRegionMin", 0):
                holes.append("%s×%s=%d(<%d)"
                             % (r["id"], t["id"], n, t.get("perRegionMin", 0)))
    rep.facts["matrixCells"] = len(regions) * len(types)
    rep.facts["matrixHoles"] = len(holes)
    rep.check(not holes, "%d hücrenin hepsi asgarinin üstünde"
              % (len(regions) * len(types))
              + ("" if not holes else " — BOŞ: %s" % holes[:6]))


# ── ② KÜLTÜR ───────────────────────────────────────────────────────────────
def check_cultures(cfg, acts, cultures, rep):
    print("\n── ② kültür temsili ve kota ──")
    declared = {c["id"] for c in cultures}
    present = {a.get("culture") for a in acts}
    target = cfg["scope"]["cultures"]

    rep.facts["culturesDeclared"] = len(declared)
    rep.facts["culturesPresent"] = len(present)
    rep.check(len(declared) == target,
              "kültür dizini alt başlığı doğruluyor (%d/%d)" % (len(declared), target))

    missing = sorted(declared - present)
    rep.check(not missing, "her kültürün en az bir adayı var"
              + ("" if not missing else " — TEMSİLSİZ: %s" % missing))

    unknown = sorted(present - declared)
    rep.check(not unknown, "tanımsız kültür kimliği yok"
              + ("" if not unknown else " — TANIMSIZ: %s" % unknown))

    # Kota, kitaptaki 120'yi bölüştürür; havuz her kültür için kotayı
    # BESLEYEBİLMELİDİR, aksi hâlde o kültür kitapta eksik kalır.
    short = []
    for c in cultures:
        n = sum(1 for a in acts if a.get("culture") == c["id"])
        if n < c.get("activityQuota", 0):
            short.append("%s=%d(<%d)" % (c["id"], n, c["activityQuota"]))
    rep.check(not short, "her kültürün havuzu kotasını besliyor"
              + ("" if not short else " — YETERSİZ: %s" % short[:6]))

    total_quota = sum(c.get("activityQuota", 0) for c in cultures)
    rep.facts["quotaTotal"] = total_quota
    rep.check(total_quota == cfg["scope"]["activities"],
              "kültür kotaları toplamı kitap kapsamına eşit (%d/%d)"
              % (total_quota, cfg["scope"]["activities"]))

    # Bölge kotası da kültür kotalarının toplamı olmalı.
    by_region = collections.Counter()
    for c in cultures:
        by_region[c["region"]] += c.get("activityQuota", 0)
    rep.facts["quotaByRegion"] = dict(by_region)


def check_region_quota(acts, regions, by_region_from_cultures, rep):
    print("\n── ② bölge kotası ──")
    mismatched, thin = [], []
    for r in regions:
        want = r.get("activityQuota", 0)
        got = by_region_from_cultures.get(r["id"], 0)
        if want != got:
            mismatched.append("%s: bölge=%d kültür toplamı=%d" % (r["id"], want, got))
        cand = sum(1 for a in acts if a.get("region") == r["id"])
        if cand < want:
            thin.append("%s: aday=%d < kota=%d" % (r["id"], cand, want))
        if cand < r.get("candidateQuota", 0):
            thin.append("%s: aday=%d < aday kotası=%d"
                        % (r["id"], cand, r["candidateQuota"]))
    rep.check(not mismatched, "bölge kotaları kültür kotalarıyla tutarlı"
              + ("" if not mismatched else " — ÇELİŞKİ: %s" % mismatched))
    rep.check(not thin, "her bölgenin havuzu kotasını besliyor"
              + ("" if not thin else " — YETERSİZ: %s" % thin))


# ── ③ ZORLUK ───────────────────────────────────────────────────────────────
def check_difficulty(acts, regions, rep):
    print("\n── ③ zorluk profili ──")
    short, over = [], []
    for r in regions:
        prof = {int(k): v for k, v in (r.get("difficultyProfile") or {}).items()}
        if not prof:
            continue
        have = collections.Counter(a.get("difficulty")
                                   for a in acts if a.get("region") == r["id"])
        for lvl, need in prof.items():
            if have[lvl] < need:
                short.append("%s ★%d: %d<%d" % (r["id"], lvl, have[lvl], need))
        total = sum(prof.values())
        if total and prof.get(3, 0) / total > 0.30:
            over.append("%s ★★★ %.1f%%" % (r["id"], 100 * prof[3] / total))
    rep.check(not short, "havuz her bölgenin zorluk profilini besliyor"
              + ("" if not short else " — YETERSİZ: %s" % short))
    rep.check(not over, "★★★ oranı hiçbir bölgede %30'u aşmıyor"
              + ("" if not over else " — AŞIM: %s" % over))


# ── ④ MÜHÜR ────────────────────────────────────────────────────────────────
def check_seals(acts, regions, rep):
    print("\n── ④ mühür yuvaları ──")
    problems = []
    for r in regions:
        want = r.get("sealLetterCount", 0)
        if not want:
            continue
        slots = [a["sealSlot"] for a in acts
                 if a.get("region") == r["id"] and a.get("sealSlot")]
        counts = collections.Counter(slots)
        for i in range(1, want + 1):
            if counts[i] == 0:
                problems.append("%s yuva %d BOŞ" % (r["id"], i))
            elif counts[i] > 1:
                problems.append("%s yuva %d %d kez dolu" % (r["id"], i, counts[i]))
        extra = [s for s in counts if s > want]
        if extra:
            problems.append("%s mühür uzunluğu %d ama yuva %s var"
                            % (r["id"], want, sorted(extra)))
    rep.facts["sealSlotsTotal"] = sum(r.get("sealLetterCount", 0) for r in regions)
    rep.check(not problems, "her mühür yuvası tam bir kez dolu"
              + ("" if not problems else " — İHLAL: %s" % problems[:6]))

    # Mührü besleyen aktivite BELİRLENİMCİ olmalıdır.
    bad = [a["activityId"] for a in acts if a.get("sealSlot") and a.get("openEnded")]
    rep.check(not bad, "açık uçlu aktivite mühür beslemiyor"
              + ("" if not bad else " — İHLAL: %s" % bad[:5]))

    dropped = [a["activityId"] for a in acts
               if a.get("sealSlot") and a.get("status") == "dropped"]
    rep.check(not dropped, "düşürülmüş aktivite mühür beslemiyor"
              + ("" if not dropped else " — İHLAL: %s" % dropped[:5]))


# ── ⑤ TEKRAR ───────────────────────────────────────────────────────────────
def check_duplicates(acts, rep):
    print("\n── ⑤ tekrar taraması ──")
    ids = [a.get("activityId") for a in acts]
    dup_id = [k for k, v in collections.Counter(ids).items() if v > 1]
    rep.check(not dup_id, "aktivite kimlikleri tekil"
              + ("" if not dup_id else " — YİNELENEN: %s" % dup_id[:5]))

    # Aynı başlık iki farklı kültürde olabilir; aynı KÜLTÜRDE olamaz.
    seen = collections.Counter((a.get("culture"), (a.get("title") or "").lower())
                               for a in acts)
    dup_title = ["%s/%s" % k for k, v in seen.items() if v > 1]
    rep.check(not dup_title, "aynı kültürde yinelenen başlık yok"
              + ("" if not dup_title else " — YİNELENEN: %s" % dup_title[:5]))

    obj = collections.Counter((a.get("objective") or "").lower()
                              for a in acts if a.get("objective"))
    dup_obj = [k[:50] for k, v in obj.items() if v > 1]
    rep.check(not dup_obj, "yinelenen amaç cümlesi yok"
              + ("" if not dup_obj else " — YİNELENEN: %s" % dup_obj[:3]))

    # Tek hikâyeden çok aktivite → tekrar riski. Eşik: 3.
    per_story = collections.Counter(a.get("sourceStory") for a in acts
                                    if a.get("sourceStory"))
    heavy = ["%s×%d" % (k, v) for k, v in per_story.items() if v > 3]
    if heavy:
        rep.warn("tek hikâyeden 3'ten çok aday: %s — qa_echo (Faz 3) izleyecek"
                 % heavy[:5])


# ── ⑥ AÇIK UÇLULUK ─────────────────────────────────────────────────────────
def check_open_ended(cfg, acts, rep):
    print("\n── ⑥ açık uçluluk ──")
    exempt = set(cfg.get("solvability", {}).get("openEndedTypeExempt", []))
    bad = [a["activityId"] for a in acts
           if a.get("openEnded") and a.get("type") not in exempt]
    rep.check(not bad, "openEnded yalnızca %s tipinde" % sorted(exempt)
              + ("" if not bad else " — İHLAL: %s" % bad[:5]))

    n_open = sum(1 for a in acts if a.get("openEnded"))
    rep.facts["openEnded"] = n_open
    ratio = n_open / len(acts) if acts else 0
    rep.facts["openEndedRatio"] = round(ratio, 3)
    rep.check(ratio <= 0.25,
              "açık uçlu oranı %%25'i aşmıyor (%.1f%%)" % (ratio * 100))


# ── ⑦ TERİMLER ─────────────────────────────────────────────────────────────
def check_terminology(acts, regions, cultures, rep):
    print("\n── ⑦ terim tutarlılığı ──")
    rids = {r["id"] for r in regions}
    cmap = {c["id"]: c for c in cultures}

    bad_region = [a["activityId"] for a in acts if a.get("region") not in rids]
    rep.check(not bad_region, "her aktivite tanımlı bir bölgede"
              + ("" if not bad_region else " — TANIMSIZ: %s" % bad_region[:5]))

    # Aktivitenin bölgesi, kültürünün bölgesiyle AYNI olmalıdır.
    mism = ["%s (%s→%s, kültür→%s)"
            % (a["activityId"], a.get("culture"), a.get("region"),
               cmap[a["culture"]]["region"])
            for a in acts
            if a.get("culture") in cmap and a.get("region") != cmap[a["culture"]]["region"]]
    rep.check(not mism, "aktivite bölgesi kültürün bölgesiyle aynı"
              + ("" if not mism else " — ÇELİŞKİ: %s" % mism[:5]))

    # Kısıt durumu kültür dizininden GEVŞETİLEMEZ.
    order = {"open": 0, "attributed": 1, "restricted": 2, "excluded": 3}
    loosened = ["%s (%s < %s)" % (a["activityId"], a.get("restrictionStatus"),
                                  cmap[a["culture"]]["restrictionStatus"])
                for a in acts
                if a.get("culture") in cmap
                and order.get(a.get("restrictionStatus"), -1)
                < order.get(cmap[a["culture"]]["restrictionStatus"], 0)]
    rep.check(not loosened, "kısıt durumu kültür dizininden gevşetilmemiş"
              + ("" if not loosened else " — GEVŞEK: %s" % loosened[:5]))

    # İzinli tip listesi.
    off = ["%s (%s)" % (a["activityId"], a.get("type"))
           for a in acts
           if a.get("culture") in cmap
           and a.get("type") not in cmap[a["culture"]].get("allowedTypes", [])]
    rep.check(not off, "her aktivite kültürünün izinli tipinde"
              + ("" if not off else " — İZİNSİZ: %s" % off[:5]))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    print("=" * 74)
    print("  BÖLGE × TİP MATRİSİ VE KAPSAM DAĞILIMI")
    print("=" * 74)

    rep = Report(args.verbose)
    cfg = load(CONFIG, rep)
    if cfg is None:
        return 1

    acts_doc = load(ACTIVITY_INDEX, rep, required=False)
    reg_doc = load(REGION_INDEX, rep, required=False)
    cul_doc = load(CULTURE_INDEX, rep, required=False)

    if acts_doc is None or reg_doc is None or cul_doc is None:
        rep.warn("envanter, bölge veya kültür dizini yok — Faz 1 teslimatı; "
                 "matris kapısı boş koşuyor")
        print("\n" + "=" * 74)
        print("  ⊘ boş koştu (dizinler henüz yok)")
        print("=" * 74)
        if args.json:
            os.makedirs(os.path.dirname(args.json), exist_ok=True)
            with open(args.json, "w", encoding="utf-8") as fh:
                json.dump({"status": "empty", "checks": 0, "errors": [],
                           "warnings": rep.warnings, "facts": {}},
                          fh, ensure_ascii=False, indent=2)
        return 0

    acts = live(acts_doc.get("activities", acts_doc))
    regions = reg_doc.get("regions", reg_doc)
    cultures = cul_doc.get("cultures", cul_doc)
    rep.facts["activitiesLive"] = len(acts)

    check_matrix(cfg, acts, regions, rep)
    check_cultures(cfg, acts, cultures, rep)
    by_region = collections.Counter()
    for c in cultures:
        by_region[c["region"]] += c.get("activityQuota", 0)
    check_region_quota(acts, regions, by_region, rep)
    check_difficulty(acts, regions, rep)
    check_seals(acts, regions, rep)
    check_duplicates(acts, rep)
    check_open_ended(cfg, acts, rep)
    check_terminology(acts, regions, cultures, rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · %d aday · %d hücre"
              % (rep.checks, len(acts), rep.facts.get("matrixCells", 0)))
        status = "pass"
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": status, "checks": rep.checks,
                       "errors": rep.errors, "warnings": rep.warnings,
                       "facts": rep.facts}, fh, ensure_ascii=False, indent=2)
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
