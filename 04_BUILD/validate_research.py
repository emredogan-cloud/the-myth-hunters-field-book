#!/usr/bin/env python3
"""
ARAŞTIRMA ZİNCİRİ KAPISI — The Myth Hunter's Field Book
================================================================================
Bu kapı tek bir cümleyi mekanikleştirir:

    Hiçbir aktivite "bu eğlenceli görünüyor"dan doğamaz.

Her aktivite şu zinciri sonuna kadar çözebilmelidir:

    aktivite → hikâye → kültür → devralma kaydı → kaynak → gerekçe

Zincirin bir halkası kopuksa aktivite bir tasarım değil bir TAHMİNDİR.

Dokuz denetim:

  ① KÜLTÜR ZİNCİRİ   — her aktivitenin kültürü dizinde ve manifestte var mı
  ② HİKÂYE ZİNCİRİ   — sourceStory manifestte var mı, aktivite dışı mı
  ③ KAYIT ZİNCİRİ    — inheritedRecords'un her üyesi manifestte var mı
  ④ DOĞRULAMA PLANI  — inherited-provisional bir aday plansız duramaz
  ⑤ KADEME TUTARLILIĞI — culture_index ile manifest aynı kademeyi söylüyor mu
  ⑥ CEVAP YETKİSİ    — mühür besleyen aday, cevap üretebilen bir kayda mı dayanıyor
  ⑦ GEREKÇE          — her adayın öğrenme gerekçesi ve boyutu var mı
  ⑧ DİAKRİTİK        — kültür adları ve yazı dizgeleri bozulmuş mu (mojibake)
  ⑨ HİKÂYE ENVANTERİ — culture_index'in usableStories listesi manifestle uyuşuyor mu

⑥ NEDEN VAR: bir mühür harfi yanlışsa çocuk BÜTÜN BÖLGEYİ çözemez ve
kitabı bırakır. Mühür besleyen bir aday, kaynakta yaş incelemesi kapanmamış
bir hikâyeye dayanamaz. Bu kapı Faz 1'de tam olarak iki böyle aday buldu
ve yuvalar taşındı.

⑧ NEDEN VAR: çocuk ā, ʻ, ẹ ve ş'yi DEFTERE YAZACAK. Bir kodlama kazası
sessizce yanlış imlâ öğretir ve bu düzeltilemez.

TASARIM: yalnızca Python standart kütüphanesi (karar K7).

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CONFIG = os.path.join(ROOT, "project_config.json")
ACTIVITY_INDEX = os.path.join(ROOT, "01_SOURCE", "activity_index.json")
CULTURE_INDEX = os.path.join(ROOT, "01_SOURCE", "culture_index.json")
MANIFEST = os.path.join(ROOT, "01_SOURCE", "inherited", "IMPORT_MANIFEST.json")

# Bu kültürlerin kimliğini diakritik taşır. Kaybolursa imlâ yanlış öğretilir.
DIACRITIC_WITNESS = {
    "maori":    ["ā"],           # makron — ünlü uzunluğu
    "hawaiian": ["ʻ", "ā"],      # ʻokina bir HARFTİR
    "yoruba":   ["ẹ", "ọ", "ṣ"],  # alt nokta ayrı harf yapar
    "vietnamese": ["ữ", "ố", "ộ", "ơ", "ư", "ạ"],
}
MOJIBAKE = re.compile(r"Ã[\x80-\xbf]|â€|Ä±|Å\x9f|Ã¼|Ã¶|Ã§|�")


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


def check_culture_chain(acts, cultures, records, rep):
    print("\n── ① kültür zinciri ──")
    cmap = {c["id"]: c for c in cultures}
    orphan = sorted({a.get("culture") for a in acts if a.get("culture") not in cmap})
    rep.check(not orphan, "her aktivitenin kültürü dizinde"
              + ("" if not orphan else " — DİZİNSİZ: %s" % orphan))

    missing = [c["id"] for c in cultures if "culture-%s" % c["id"] not in records]
    rep.check(not missing, "her kültürün bir devralma kaydı var"
              + ("" if not missing else " — KAYITSIZ: %s" % missing))


def check_story_chain(acts, records, rep):
    print("\n── ② hikâye zinciri ──")
    unknown, excluded = [], []
    for a in acts:
        s = a.get("sourceStory")
        if not s:
            continue
        rec = records.get(s)
        if rec is None:
            unknown.append("%s → %s" % (a["activityId"], s))
        elif rec.get("activityExcludedReason"):
            excluded.append("%s → %s" % (a["activityId"], s))
    rep.check(not unknown, "her sourceStory manifestte var"
              + ("" if not unknown else " — MANİFESTSİZ: %s" % unknown[:5]))
    rep.check(not excluded, "aktivite dışı hikâyeden aday türetilmemiş"
              + ("" if not excluded else " — İHLAL: %s" % excluded[:5]))

    with_story = sum(1 for a in acts if a.get("sourceStory"))
    rep.facts["activitiesWithStory"] = with_story
    rep.facts["activitiesCultureOnly"] = len(acts) - with_story


def check_record_chain(acts, records, rep):
    print("\n── ③ kayıt zinciri ──")
    dangling, empty = [], []
    for a in acts:
        refs = a.get("inheritedRecords") or []
        if not refs:
            empty.append(a["activityId"])
            continue
        for r in refs:
            if r not in records:
                dangling.append("%s → %s" % (a["activityId"], r))
    rep.check(not empty, "her aday en az bir devralma kaydına bağlı"
              + ("" if not empty else " — BAĞSIZ: %s" % empty[:5]))
    rep.check(not dangling, "hiçbir kayıt referansı boşa düşmüyor"
              + ("" if not dangling else " — BOŞTA: %s" % dangling[:5]))


def check_revalidation(cfg, acts, rep):
    print("\n── ④ yeniden doğrulama planı ──")
    lock_ok = set(cfg["inheritance"]["lockRequiresStatus"])
    noplan = [a["activityId"] for a in acts
              if a.get("inheritanceStatus") == "inherited-provisional"
              and not (a.get("revalidationPlan") or "").strip()]
    rep.check(not noplan, "her doğrulanmamış aday bir doğrulama planı taşıyor"
              + ("" if not noplan else " — PLANSIZ: %s" % noplan[:5]))

    # Bel kemiği kuralının bu kapıdaki üçüncü kopyası.
    locked_bad = [a["activityId"] for a in acts
                  if a.get("status") in ("locked", "written")
                  and a.get("inheritanceStatus") not in lock_ok]
    rep.check(not locked_bad,
              "doğrulanmamış devralmaya dayanan locked aday yok"
              + ("" if not locked_bad else " — İHLAL: %s" % locked_bad[:5]))

    # "Sonra bakarız" bir plan değildir.
    weak = [a["activityId"] for a in acts
            if a.get("revalidationPlan")
            and len(a["revalidationPlan"].split()) < 8]
    rep.check(not weak, "doğrulama planları somut (≥8 kelime)"
              + ("" if not weak else " — ZAYIF: %s" % weak[:5]))

    counts = {}
    for a in acts:
        counts[a.get("inheritanceStatus")] = counts.get(a.get("inheritanceStatus"), 0) + 1
    rep.facts["inheritanceStatus"] = counts


def check_tier_consistency(cultures, records, rep):
    print("\n── ⑤ kademe tutarlılığı ──")
    mismatch, restr = [], []
    for c in cultures:
        rec = records.get("culture-%s" % c["id"])
        if rec is None:
            continue
        if rec.get("eligibilityTier") != c.get("eligibilityTier"):
            mismatch.append("%s: dizin=%s manifest=%s"
                            % (c["id"], c.get("eligibilityTier"),
                               rec.get("eligibilityTier")))
        if rec.get("restrictionStatus") != c.get("restrictionStatus"):
            restr.append("%s: dizin=%s manifest=%s"
                         % (c["id"], c.get("restrictionStatus"),
                            rec.get("restrictionStatus")))
    rep.check(not mismatch, "kademe dizin ile manifestte aynı"
              + ("" if not mismatch else " — ÇELİŞKİ: %s" % mismatch))
    rep.check(not restr, "kısıt durumu dizin ile manifestte aynı"
              + ("" if not restr else " — ÇELİŞKİ: %s" % restr))

    # Kademe C bir gevşetmeyle A'ya çekilemez.
    loosened = [c["id"] for c in cultures
                if c.get("eligibilityTier") == "A"
                and records.get("culture-%s" % c["id"], {}).get("restrictionRiskHigh")]
    rep.check(not loosened, "hiçbir yüksek riskli kültür A kademesine çekilmemiş"
              + ("" if not loosened else " — GEVŞETME: %s" % loosened))


def check_answer_authority(acts, records, rep):
    print("\n── ⑥ cevap yetkisi ──")
    bad = []
    for a in acts:
        if not a.get("sealSlot"):
            continue
        s = a.get("sourceStory")
        if not s:
            continue          # kültür kaydından türeyen mühür adayı — serbest
        rec = records.get(s, {})
        if "answer-source" not in (rec.get("fieldbookUsage") or []):
            bad.append("%s → %s (%s)"
                       % (a["activityId"], s, rec.get("upstreamAgeReview")))
    rep.check(not bad,
              "mühür besleyen her aday cevap üretebilen bir kayda dayanıyor"
              + ("" if not bad else " — YETKİSİZ: %s" % bad[:5]))

    eligible = sum(1 for r in records.values()
                   if "answer-source" in (r.get("fieldbookUsage") or []))
    rep.facts["answerSourceEligibleRecords"] = eligible


def check_rationale(acts, rep):
    print("\n── ⑦ editoryal gerekçe ──")
    nodim = [a["activityId"] for a in acts if not a.get("learningDimensions")]
    rep.check(not nodim, "her adayın en az bir öğrenme boyutu var"
              + ("" if not nodim else " — BOYUTSUZ: %s" % nodim[:5]))

    nolearn = [a["activityId"] for a in acts
               if not (a.get("learningObjective") or "").strip()]
    rep.check(not nolearn, "her adayın öğrenme gerekçesi yazılı"
              + ("" if not nolearn else " — GEREKÇESİZ: %s" % nolearn[:5]))

    noobj = [a["activityId"] for a in acts if not (a.get("objective") or "").strip()]
    rep.check(not noobj, "her adayın amacı yazılı"
              + ("" if not noobj else " — AMAÇSIZ: %s" % noobj[:5]))

    # Atıf zorunluysa kültürel çerçeve de zorunludur (şema R8).
    noctx = [a["activityId"] for a in acts
             if a.get("attributionRequired") and not (a.get("culturalContext") or "").strip()]
    rep.check(not noctx, "atıf gereken her adayda kültürel çerçeve var"
              + ("" if not noctx else " — ÇERÇEVESİZ: %s" % noctx[:5]))


def check_diacritics(cultures, acts, rep):
    print("\n── ⑧ diakritik bütünlüğü ──")
    blob = json.dumps(cultures, ensure_ascii=False) + json.dumps(acts, ensure_ascii=False)
    m = MOJIBAKE.search(blob)
    rep.check(m is None, "kodlama bozulması yok"
              + ("" if m is None else " — MOJIBAKE: '%s'" % m.group(0)))

    cmap = {c["id"]: c for c in cultures}
    missing = []
    for cid, marks in DIACRITIC_WITNESS.items():
        c = cmap.get(cid)
        if c is None:
            continue
        text = json.dumps(c, ensure_ascii=False)
        for ch in marks:
            if ch not in text:
                missing.append("%s → '%s'" % (cid, ch))
    rep.check(not missing,
              "diakritik tanıkları yerinde (%d kültür)" % len(DIACRITIC_WITNESS)
              + ("" if not missing else " — KAYIP: %s" % missing))


def check_story_inventory(cultures, records, rep):
    print("\n── ⑨ hikâye envanteri ──")
    problems = []
    for c in cultures:
        for s in c.get("usableStories", []):
            rec = records.get(s)
            if rec is None:
                problems.append("%s → %s manifestte yok" % (c["id"], s))
            elif rec.get("activityExcludedReason"):
                problems.append("%s → %s aktivite dışı" % (c["id"], s))
            elif rec.get("culture") != c["id"]:
                problems.append("%s → %s başka kültüre ait (%s)"
                                % (c["id"], s, rec.get("culture")))
    rep.check(not problems, "usableStories listesi manifestle uyuşuyor"
              + ("" if not problems else " — ÇELİŞKİ: %s" % problems[:5]))

    # Manifestte kullanılabilir olup dizinde anılmayan hikâye = kayıp kaynak.
    listed = {s for c in cultures for s in c.get("usableStories", [])}
    usable = {r["recordId"] for r in records.values()
              if r.get("kind") == "story" and not r.get("activityExcludedReason")}
    unlisted = sorted(usable - listed)
    if unlisted:
        rep.warn("%d kullanılabilir hikâye kültür dizininde anılmıyor: %s"
                 % (len(unlisted), unlisted[:5]))
    rep.facts["usableStoriesListed"] = len(listed)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    print("=" * 74)
    print("  ARAŞTIRMA ZİNCİRİ")
    print("=" * 74)

    rep = Report(args.verbose)
    cfg = load(CONFIG, rep)
    if cfg is None:
        return 1

    acts_doc = load(ACTIVITY_INDEX, rep, required=False)
    cul_doc = load(CULTURE_INDEX, rep, required=False)
    man = load(MANIFEST, rep, required=False)

    if acts_doc is None or cul_doc is None or man is None:
        rep.warn("envanter, kültür dizini veya manifest yok — Faz 1 teslimatı; "
                 "araştırma kapısı boş koşuyor")
        print("\n" + "=" * 74)
        print("  ⊘ boş koştu")
        print("=" * 74)
        if args.json:
            os.makedirs(os.path.dirname(args.json), exist_ok=True)
            with open(args.json, "w", encoding="utf-8") as fh:
                json.dump({"status": "empty", "checks": 0, "errors": [],
                           "warnings": rep.warnings, "facts": {}},
                          fh, ensure_ascii=False, indent=2)
        return 0

    acts = [a for a in acts_doc.get("activities", acts_doc)
            if a.get("status") != "dropped"]
    cultures = cul_doc.get("cultures", cul_doc)
    records = {r["recordId"]: r for r in man.get("records", [])}
    rep.facts["records"] = len(records)
    rep.facts["activities"] = len(acts)

    check_culture_chain(acts, cultures, records, rep)
    check_story_chain(acts, records, rep)
    check_record_chain(acts, records, rep)
    check_revalidation(cfg, acts, rep)
    check_tier_consistency(cultures, records, rep)
    check_answer_authority(acts, records, rep)
    check_rationale(acts, rep)
    check_diacritics(cultures, acts, rep)
    check_story_inventory(cultures, records, rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · %d aday · %d devralma kaydı"
              % (rep.checks, len(acts), len(records)))
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
