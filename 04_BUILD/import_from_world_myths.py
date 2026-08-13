#!/usr/bin/env python3
"""
DEVRALMA İTHALATÇISI — The Myth Hunter's Field Book
================================================================================
`THE-GREAT-BOOK-OF-WORLD-MYTHS`'ten veri devralır ve
`01_SOURCE/inherited/IMPORT_MANIFEST.json`'u üretir.

BU BİR KAPI DEĞİL, BİR TEK SEFERLİK ARAÇTIR. Kapı `validate_inheritance.py`dir
ve manifestin kendisini denetler — bu betik olmadan da koşar.

⚠ ÇALIŞMASI İÇİN KAYNAK DEPO GEREKİR. Yoksa çıkış 2 verir (= ATLANDI) ve bu
bir kusur DEĞİLDİR: devralma bir KOPYALAMA + KÖKEN KAYDIdır, canlı bağımlılık
değil. Manifest üretildikten sonra bu proje kaynak depo olmadan da build alır,
test edilir ve CI'ı yeşil yanar (karar K6).

NE DEVRALINIR
-------------
  · 22 kilitli kültür kaydı        → culture_index.json
  · o kültürlerin 54 hikâye kaydı  → story_index.json + research/*.md

NE DEVRALINMAZ
--------------
  · Manuscript prozası — Field Book kendi metnini yazar
  · Aday (kilitlenmemiş) kültürler — Field Book 22 kültürde kilitlidir
  · Yaş incelemesi 'cleared' olmayan hikâyelerin CEVAP ÜRETEN katmanı
    (kayıt gelir, ama activityUsage kısıtlı gelir)

HER KAYIT DÖRT SORUYA CEVAP VERİR
---------------------------------
  ① nereden geldi        → sourceRepo · sourcePath · sourceSha256
  ② ne devralındı        → inheritedFields
  ③ burada ne yapılabilir → fieldbookUsage · activityUsage · restrictionStatus
  ④ doğrulandı mı        → status · reviewStatus · revalidatedFields

Çıkış kodları:  0 = manifest üretildi   1 = hata   2 = kaynak depo yok (ATLANDI)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

MANIFEST = os.path.join(ROOT, "01_SOURCE", "inherited", "IMPORT_MANIFEST.json")
DEFAULT_SOURCE = os.path.join("..", "THE-GREAT-BOOK-OF-WORLD-MYTHS")

SOURCE_REPO = "emredogan-cloud/the-great-book-of-world-myths"
SOURCE_PROJECT = "THE-GREAT-BOOK-OF-WORLD-MYTHS"

CULTURE_INDEX = os.path.join("01_RESEARCH", "culture_index.json")
STORY_INDEX = os.path.join("01_RESEARCH", "story_index.json")

# Bir kültür kaydından devralınan alanlar. Anlatı prozası DEVRALINMAZ.
CULTURE_FIELDS = ["id", "name", "macroRegion", "region", "livingTradition",
                  "restrictionAssessment", "restrictionRisk", "restrictionNote",
                  "mapPoint", "cardText"]

# Bir hikâye kaydından devralınan alanlar. `plot` ve tam metin DEVRALINMAZ:
# Field Book hikâye anlatmaz, hikâyeye ATIF yapar ve ondan görev türetir.
STORY_FIELDS = ["id", "title", "cultureId", "region", "period", "sources",
                "canonicalVersion", "variants", "variantNote",
                "restrictionScreened", "restrictionNote", "ageReviewStatus",
                "contentFlags", "characters", "pronunciationEntries",
                "culturalNote", "themes", "motifs"]


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_record(obj: dict) -> str:
    """Kaydın kendi parmak izi. Dosya değişip kayıt değişmediğinde
    sürüklenmeyi AYIRT ETMEK için gerekir: dosya sha256'sı bütün kayıtlar
    için ortaktır, bu ise kayda özgüdür."""
    canon = json.dumps(obj, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


# ── FIELD BOOK'UN KENDİ EDİTORYAL KARARLARI ────────────────────────────────
# Bunlar DEVRALINMAZ; devralınanın ÜSTÜNE konur. Kaynak proje bu hikâyeleri
# ANLATI için temizledi — ve o karar orada doğrudur. Burada aynı hikâye bir
# GÖREVE dönüşüyor: çocuk çiziyor, çözüyor, deftere yazıyor. Eşik farklıdır.
#
# ⚠ Kültür DÜŞÜRÜLMEZ, HİKÂYE düşürülür. 22 kültür alt başlıkta yazan bir
# vaattir; her kültürün elinde en az iki kullanılabilir hikâye kalmalıdır.
STORY_ACTIVITY_EXCLUSIONS = {
    "egyptian-horus-seth": (
        "Kaynak anlatı cinsel saldırı içeren bir bölüm taşıyor (contentFlags: "
        "sexuality). Anlatı katmanında ele alınabilir; bir GÖREV çocuğu "
        "kaynağa yönlendirir. Mısır iki hikâyeyle temsil edilir."),
    "hindu-ganesha-head": (
        "Anlatının çekirdeği bir başın kesilmesidir ve kaynakta yaş "
        "incelemesi 'pending'. Bir çocuk aktivite kitabında bu anlatıdan "
        "görev türetmek 'çocuğum için fazla karanlık' yorumunun tam "
        "tarifidir. Hindu iki hikâyeyle temsil edilir."),
}

# Bir hikâyenin İÇİNDE aktiviteye çevrilemeyecek bölümler. Hikâye kalır,
# o katman kapanır. `qa_age.py` bunu aktivite metninde tarar.
STORY_FORBIDDEN_LAYERS = {
    "turkic-basat-tepegoz": "yamyamlık ve öldürme sahnesi; motif katmanı açık",
    "inuit-blind-boy-loon": "çocuğa yönelik kötü muamele bölümü",
    "inuit-sedna": "parmakların kesilmesi; deniz yaratıkları katmanı açık",
    "maya-hero-twins": "yeraltı işkence sınavlarının betimlenmesi",
    "aztec-fifth-sun": "kurban bölümü; beş güneşin sırası katmanı açık",
    "japanese-susanoo-orochi": "canavarın öldürülme sahnesi",
    "irish-cu-chulainn-name": "savaş çılgınlığı ve öldürme sahneleri",
    "persian-kaveh": "isyan ve infaz sahneleri; sancak motifi açık",
    "maori-maui-fish": "kardeşlerin balığı parçalaması",
    "greek-persephone": "kaçırılma anı; mevsim pazarlığı katmanı açık",
    "egyptian-isis-secret-name": "zehirlenme sahnesi; ad ve yazı katmanı açık",
    "yoruba-obatala-land": "kutsal ritüel katmanı — YALNIZCA anlatı ve coğrafya",
    "yoruba-osun-seventeenth": "Ifá kehanet mekaniği aktiviteye ÇEVRİLEMEZ",
    "hawaiian-pele-journey": "mele/oli (ezgi ve dua) metni kullanılamaz",
    "japanese-amaterasu-cave": "Şinto ritüel uygulaması taklit edilemez",
    "hindu-ganga-descent": "tapınma uygulaması aktiviteye çevrilemez",
    "hindu-hanuman-sun": "tapınma uygulaması aktiviteye çevrilemez",
    "maori-rangi-papa": "whakapapa (soy sayımı) bir bulmaca cevabı olamaz",
    "andean-llama-flood": "yaşayan tören takvimi aktiviteye çevrilemez",
    "maya-hurakan-storm": "çağdaş Maya töreni aktiviteye çevrilemez",
}


def activity_usage_for_culture(c: dict) -> tuple[str, str]:
    """Bir kültürün aktivite uygunluk kademesi — MEKANİK KURAL.

    Kaynak proje `restrictionRisk`, `livingTradition` ve
    `restrictionAssessment` alanlarını zaten taşıyor ve o tarama
    MUAFİYETSİZ yapılmıştı. Field Book bu üç alandan kendi kademesini
    TÜRETİR — çünkü buradaki eşik farklıdır:

        Bir geleneği ANLATMAK ile onu YAPTIRMAK aynı şey değildir.

    Kademe A · `eligible` / `eligible-with-attribution`
        Beş aktivite tipinin hepsi açık. Yaşayan gelenekte atıf zorunlu.

    Kademe B · `eligible-with-attribution`
        Beş tip açık, atıf ZORUNLU ve kutsal/ritüel katman bir bulmaca
        CEVABI olamaz.

    Kademe C · `restricted-forms`
        `observe` · `map` · `sort` · `make` açık.
        `cipher` YALNIZCA kamuya açık yazı sistemi ve imlâ üzerinden
        (Inuktitut hecelemesi, makron, ʻokina) — kutsal ad veya ritüel
        sözcük ÜZERİNDEN ASLA.
        Her aktivite atıf ve ebeveyn notu taşır.
    """
    risk = c.get("restrictionRisk", "low")
    living = bool(c.get("livingTradition"))
    assess = c.get("restrictionAssessment", "clear")

    if risk == "high":
        return "restricted-forms", "C"
    if risk == "medium" or (living and assess == "partial"):
        return "eligible-with-attribution", "B"
    if living:
        return "eligible-with-attribution", "A"
    return "eligible", "A"


def restriction_for_culture(c: dict) -> str:
    """Kısıt durumu — SOURCING_STANDARD § 4.

    Yaşayan bir gelenek `open` olamaz: adı anılır, atfı yazılır.
    Şüphe her zaman daha sert olanın lehine çözülür."""
    if c.get("restrictionRisk") in ("high", "medium"):
        return "attributed"
    if c.get("livingTradition"):
        return "attributed"
    return "open"


def build(source_root: str, imported_at: str) -> dict:
    ci_path = os.path.join(source_root, CULTURE_INDEX)
    si_path = os.path.join(source_root, STORY_INDEX)

    with open(ci_path, encoding="utf-8") as fh:
        culture_index = json.load(fh)
    with open(si_path, encoding="utf-8") as fh:
        story_index = json.load(fh)

    ci_sha = sha256_file(ci_path)
    si_sha = sha256_file(si_path)

    locked = [c for c in culture_index["cultures"] if c.get("status") == "locked"]
    locked_ids = {c["id"] for c in locked}

    records: list[dict] = []

    # ── ① KÜLTÜR KAYITLARI ────────────────────────────────────────────────
    for c in sorted(locked, key=lambda x: x["id"]):
        usage, tier = activity_usage_for_culture(c)
        subset = {k: c[k] for k in CULTURE_FIELDS if k in c}
        records.append({
            "recordId": "culture-%s" % c["id"],
            "kind": "culture",
            "sourceProject": SOURCE_PROJECT,
            "sourceRepo": SOURCE_REPO,
            "sourcePath": CULTURE_INDEX,
            "sourceRecordId": c["id"],
            "sourceSha256": ci_sha,
            "recordSha256": sha256_record(subset),
            "importedAt": imported_at,
            "status": "inherited-provisional",
            "reviewStatus": "screened",
            "inheritedFields": [k for k in CULTURE_FIELDS if k in c],
            "revalidatedFields": [],
            "revalidatedAt": None,
            "revalidatedBy": None,
            "adaptationStatus": "not-adapted",
            "restrictionStatus": restriction_for_culture(c),
            "eligibilityTier": tier,
            "activityUsage": usage,
            "fieldbookUsage": ["background", "field-note", "glossary", "map"],
            "note": "Kültür künyesi ve kısıt değerlendirmesi devralındı. "
                    "Ad yazımı ve harita noktası çocuğun deftere yazacağı "
                    "şeye dönüşürse yeniden doğrulama ZORUNLUDUR.",
        })

    # ── ② HİKÂYE KAYITLARI ────────────────────────────────────────────────
    for s in sorted(story_index["stories"], key=lambda x: x["id"]):
        if s["cultureId"] not in locked_ids:
            continue
        culture = next(c for c in locked if c["id"] == s["cultureId"])
        usage, tier = activity_usage_for_culture(culture)

        research_rel = s.get("researchFile") or ""
        research_abs = os.path.join(source_root, research_rel) if research_rel else ""
        if research_rel and os.path.isfile(research_abs):
            path_rel, path_sha = research_rel, sha256_file(research_abs)
        else:
            path_rel, path_sha = STORY_INDEX, si_sha

        subset = {k: s[k] for k in STORY_FIELDS if k in s}

        # Yaş incelemesi kaynakta kapanmamışsa, bu kayıt Field Book'ta
        # CEVAP ÜRETEMEZ. Kayıt gelir; yetkisi gelmez.
        age_cleared = s.get("ageReviewStatus") == "cleared"
        fb_usage = ["background", "field-note", "glossary"]
        if age_cleared:
            fb_usage.append("answer-source")

        # Duygusal risk: kaynağın contentFlags'i BURAYA TAŞINIR ve
        # qa_age.py onu aktivite biçiminde uygular.
        flags = s.get("contentFlags") or []

        # Field Book'un kendi editoryal kararı — devralınanın ÜSTÜNE konur.
        excluded_reason = STORY_ACTIVITY_EXCLUSIONS.get(s["id"])
        if excluded_reason:
            usage = "not-eligible"
            fb_usage = ["background"]

        records.append({
            "recordId": "story-%s" % s["id"],
            "kind": "story",
            "sourceProject": SOURCE_PROJECT,
            "sourceRepo": SOURCE_REPO,
            "sourcePath": path_rel,
            "sourceRecordId": s["id"],
            "sourceSha256": path_sha,
            "recordSha256": sha256_record(subset),
            "indexPath": STORY_INDEX,
            "indexSha256": si_sha,
            "importedAt": imported_at,
            "status": "inherited-provisional",
            "reviewStatus": "screened",
            "inheritedFields": [k for k in STORY_FIELDS if k in s],
            "revalidatedFields": [],
            "revalidatedAt": None,
            "revalidatedBy": None,
            "adaptationStatus": "not-adapted",
            "restrictionStatus": restriction_for_culture(culture),
            "eligibilityTier": tier,
            "activityUsage": usage,
            "fieldbookUsage": fb_usage,
            "culture": s["cultureId"],
            "upstreamAgeReview": s.get("ageReviewStatus"),
            "contentFlags": flags,
            "pronunciationCount": len(s.get("pronunciationEntries") or []),
            "activityExcludedReason": excluded_reason,
            "forbiddenLayer": STORY_FORBIDDEN_LAYERS.get(s["id"]),
            "note": excluded_reason if excluded_reason else
                    (("Yaş incelemesi kaynakta '%s' — CEVAP ÜRETEMEZ, "
                      "yeniden inceleme gerekir." % s.get("ageReviewStatus"))
                     if not age_cleared else
                     "Anlatı katmanı devralındı. Telaffuz ve ad yazımı "
                     "yeniden doğrulanmadan cevap üretemez."),
        })

    return {
        "$comment": [
            "DEVRALMA MANİFESTOSU — kopyalama + köken kaydı, canlı bağımlılık DEĞİL.",
            "Bu dosya KENDİ KENDİNE YETERLİDİR: kaynak depo bu makinede",
            "olmasa da proje build alır, test edilir ve CI'ı yeşil yanar.",
            "",
            "TEK KURAL: 'inherited-provisional' bir kayda dayanan hiçbir",
            "aktivite locked olamaz — dolayısıyla yazılamaz. Bunu iki ayrı",
            "kapı denetler: validate_spec.py ve validate_inheritance.py.",
            "",
            "Sözleşme: 00_CONTEXT/INHERITANCE_ARCHITECTURE.md",
        ],
        "manifestVersion": "1.0",
        "sourceProject": SOURCE_PROJECT,
        "sourceRepo": SOURCE_REPO,
        "sourceRoot": DEFAULT_SOURCE,
        "sourceGate": _read_source_gate(source_root),
        "importedAt": imported_at,
        "generatedBy": "04_BUILD/import_from_world_myths.py",
        "counts": {},          # aşağıda doldurulur
        "records": records,
    }


def _read_source_gate(source_root: str) -> str | None:
    p = os.path.join(source_root, ".gate")
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as fh:
        return fh.read().strip()


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", default=DEFAULT_SOURCE,
                    help="World Myths deposunun yolu (ROOT'a göre)")
    ap.add_argument("--date", required=True, help="ithalat tarihi YYYY-AA-GG")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    source_root = os.path.normpath(os.path.join(ROOT, args.source))
    if not os.path.isdir(source_root):
        print("ATLANDI: kaynak depo bu makinede yok: %s" % source_root)
        print("Bu bir kusur DEĞİLDİR — manifest zaten kendi kendine yeterlidir.")
        return 2

    man = build(source_root, args.date)

    counts: dict[str, int] = {}
    for r in man["records"]:
        counts[r["kind"]] = counts.get(r["kind"], 0) + 1
        counts["status_" + r["status"]] = counts.get("status_" + r["status"], 0) + 1
        counts["tier_" + r["eligibilityTier"]] = \
            counts.get("tier_" + r["eligibilityTier"], 0) + 1
    counts["total"] = len(man["records"])
    counts["answerSourceEligible"] = sum(
        1 for r in man["records"] if "answer-source" in r["fieldbookUsage"])
    counts["activityExcluded"] = sum(
        1 for r in man["records"] if r.get("activityExcludedReason"))
    counts["forbiddenLayerFlagged"] = sum(
        1 for r in man["records"] if r.get("forbiddenLayer"))
    man["counts"] = counts

    print("devralınan kayıt  : %d" % counts["total"])
    print("  kültür          : %d" % counts.get("culture", 0))
    print("  hikâye          : %d" % counts.get("story", 0))
    print("  cevap üretebilir: %d" % counts["answerSourceEligible"])
    print("  aktivite DIŞI   : %d" % counts["activityExcluded"])
    print("  kapalı katmanlı : %d" % counts["forbiddenLayerFlagged"])
    print("kademe A/B/C      : %d / %d / %d"
          % (counts.get("tier_A", 0), counts.get("tier_B", 0),
             counts.get("tier_C", 0)))

    # Bir kültürün elinde kullanılabilir hikâye kalmadıysa 22 vaadi kırılır.
    usable: dict[str, int] = {}
    for r in man["records"]:
        if r["kind"] != "story":
            continue
        if r.get("activityExcludedReason"):
            continue
        usable[r["culture"]] = usable.get(r["culture"], 0) + 1
    thin = sorted(k for k, v in usable.items() if v < 2)
    if thin:
        print("  ⚠ tek hikâyeli kültür: %s" % ", ".join(thin))

    if args.dry_run:
        print("\n--dry-run: manifest YAZILMADI")
        return 0

    os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(man, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("\nyazıldı: %s" % os.path.relpath(MANIFEST, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
