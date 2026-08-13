#!/usr/bin/env python3
"""
BÖLGE ZORLUK ÖLÇÜMÜ — The Myth Hunter's Field Book
================================================================================
Yol haritası Faz 2 için tek bir talimat verir:

    "Hangi bölge? EN ZOR OLANI — kültürel kısıt taraması en yoğun,
     şifre sistemi en yabancı olan."

Bu betik o cümleyi bir ÖLÇÜME çevirir. Gerekçe projenin kendi disiplinidir:
`safetyClass` HESAPLANIR, beyan edilmez (K14). Pilot bölgesi de öyle.

⚠ BU BİR KAPI DEĞİLDİR. Hiçbir şeyi reddetmez, bir SEÇİM ÜRETİR ve o
seçimin gerekçesini denetlenebilir kılar. `qa_all.sh` onu çağırmaz; Faz 2
raporu onun çıktısını taşır.

Yedi eksen — hepsi projenin kendi verisinden, hiçbiri elle yazılmadan:

  ① KADEME AĞIRLIĞI   — Kademe B/C bir kültürde kutsal katman CEVAP OLAMAZ
  ② YASAK BİÇİM       — culture_index § forbiddenForms sayısı
  ③ YAŞAYAN GELENEK   — yaşayan bir topluluk daha sert bir eşik ister
  ④ YAZI YABANCILIĞI  — dizge Latin harfli mi, alfabetik mi, diakritik mi
  ⑤ HİKÂYE ARZI       — aktivite/hikâye oranı: düşük arz TEKRAR üretir
  ⑥ MÜHÜR YÜKÜ        — kaç yuvanın belirlenimci cevap üretmesi gerekiyor
  ⑦ KAYNAK RİSKİ      — kaç aday yaş incelemesi kapanmamış hikâyeye dayanıyor

④ NEDEN EN AĞIR EKSEN: yol haritası "şifre sistemi en yabancı" der ve bu
bir üslup meselesi değildir. Latin harfli bir imlâ dizgesinde çocuk
harfleri zaten tanır; alfabetik olmayan bir sayı dizgesinde (çubuk-nokta,
düğüm, glif) TANIDIK HİÇBİR ŞEY YOKTUR. Şablon orada kırılır.

⭑ İKİ SKOR, ÇÜNKÜ TEK SKOR YANILTIYORDU ⭑

İlk koşu yalnızca TOPLAM taşıyordu ve `monsoon`'u birinci gösterdi. Ama
`monsoon`'un beş kültürü var: toplanan her eksen (yasak biçim, yaşayan
gelenek, yazı yabancılığı) kültür sayısıyla birlikte MEKANİK OLARAK
büyüyor. Yani skor zorluğu değil BÜYÜKLÜĞÜ ölçüyordu.

Bu yüzden iki ayrı skor üretilir ve ikisi ayrı sorulara cevap verir:

    burden    = toplam üretim yükü      → "bu bölge kaç birim iş"
    intensity = kültür başına yoğunluk  → "bu bölge birim içerikte ne kadar sert"

PİLOT SEÇİMİ `intensity` İLE YAPILIR. Gerekçe yol haritasının kendi
cümlesidir: "kısıt taraması EN YOĞUN, şifre sistemi EN YABANCI olan."
Yoğunluk bir oran sorusudur, bir toplam sorusu değil.

`burden` atılmaz: en yüksek yükü taşıyan bölge, üretim planlamasında
sona bırakılamaz. İki sayı iki ayrı kararı besler.

TASARIM: yalnızca Python standart kütüphanesi (karar K7).

Çıkış kodları:  0 = ölçüldü   2 = veri yok
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ACTIVITY_INDEX = os.path.join(ROOT, "01_SOURCE", "activity_index.json")
REGION_INDEX = os.path.join(ROOT, "01_SOURCE", "region_index.json")
CULTURE_INDEX = os.path.join(ROOT, "01_SOURCE", "culture_index.json")
MANIFEST = os.path.join(ROOT, "01_SOURCE", "inherited", "IMPORT_MANIFEST.json")

# ── ④ YAZI DİZGESİ YABANCILIĞI ─────────────────────────────────────────────
# Bir dizge üç sorudan kaç tanesine "hayır" derse o kadar yabancıdır:
#   (a) Latin harfleriyle mi yazılır      → hayır: +2
#   (b) alfabetik/hecesel mi (ses→işaret) → hayır: +2   (sayı/glif dizgesi)
#   (c) çocuk günlük hayatta görür mü     → hayır: +1
#
# Değerler culture_index § writingSystem alanının TANIMINDAN türer ve
# burada kültür kültür kaydedilir; alan metninden tahmin EDİLMEZ, çünkü
# bir tahmin sessizce yanlış olur ve kimse denetlemez.
WRITING_FOREIGNNESS = {
    # Latin harfli imlâ ve adlandırma dizgeleri — harfler tanıdık
    "akan":       {"latin": True,  "alphabetic": True,  "everyday": True},
    "yoruba":     {"latin": True,  "alphabetic": True,  "everyday": False},
    "zulu":       {"latin": True,  "alphabetic": True,  "everyday": True},
    "maori":      {"latin": True,  "alphabetic": True,  "everyday": False},
    "hawaiian":   {"latin": True,  "alphabetic": True,  "everyday": False},
    "vietnamese": {"latin": True,  "alphabetic": True,  "everyday": False},
    "irish":      {"latin": False, "alphabetic": True,  "everyday": False},
    "norse":      {"latin": False, "alphabetic": True,  "everyday": False},
    "turkic":     {"latin": False, "alphabetic": True,  "everyday": False},
    "greek":      {"latin": False, "alphabetic": True,  "everyday": True},
    "korean":     {"latin": False, "alphabetic": True,  "everyday": False},
    "japanese":   {"latin": False, "alphabetic": True,  "everyday": False},
    "hindu":      {"latin": False, "alphabetic": True,  "everyday": False},
    "inuit":      {"latin": False, "alphabetic": True,  "everyday": False},
    "finnish":    {"latin": True,  "alphabetic": True,  "everyday": True},
    "egyptian":   {"latin": False, "alphabetic": False, "everyday": False},
    "mesopotamian": {"latin": False, "alphabetic": False, "everyday": False},
    "chinese":    {"latin": False, "alphabetic": False, "everyday": False},
    "persian":    {"latin": False, "alphabetic": True,  "everyday": False},
    # Alfabetik OLMAYAN sayı ve yer adı dizgeleri — tanıdık hiçbir şey yok
    "maya":       {"latin": False, "alphabetic": False, "everyday": False},
    "aztec":      {"latin": False, "alphabetic": False, "everyday": False},
    "andean":     {"latin": False, "alphabetic": False, "everyday": False},
}

TIER_WEIGHT = {"A": 0, "B": 2, "C": 3}


def load(path):
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def foreignness(cid: str) -> int:
    w = WRITING_FOREIGNNESS.get(cid)
    if w is None:
        return 5           # bilinmiyorsa EN YABANCI sayılır (kapalı arıza)
    score = 0
    if not w["latin"]:
        score += 2
    if not w["alphabetic"]:
        score += 2
    if not w["everyday"]:
        score += 1
    return score


def measure(acts, regions, cultures, records):
    cmap = {c["id"]: c for c in cultures}
    rows = []
    for r in regions:
        rid = r["id"]
        cids = r.get("cultures", [])
        pool = [a for a in acts if a.get("region") == rid
                and a.get("status") != "dropped"]

        tier = sum(TIER_WEIGHT.get(cmap[c].get("eligibilityTier"), 0) for c in cids)
        forbidden = sum(len(cmap[c].get("forbiddenForms") or []) for c in cids)
        living = sum(1 for c in cids if cmap[c].get("livingTradition"))
        foreign = sum(foreignness(c) for c in cids)

        stories = sum(len(cmap[c].get("usableStories") or []) for c in cids)
        quota = r.get("activityQuota", 0)
        # Arz baskısı: kotayı kaç hikâyeden çıkarmak gerekiyor. Yüksek = zor.
        supply = round(quota / stories, 2) if stories else 99.0

        seals = r.get("sealLetterCount", 0)

        # Kaynak riski: kaç aday, upstream yaş incelemesi kapanmamış
        # (answer-source yetkisi VERİLMEMİŞ) bir hikâyeye dayanıyor.
        risky = 0
        for a in pool:
            s = a.get("sourceStory")
            if not s:
                continue
            rec = records.get(s, {})
            if "answer-source" not in (rec.get("fieldbookUsage") or []):
                risky += 1

        # ── AĞIRLIKLAR ────────────────────────────────────────────────────
        # ④ en ağır eksendir: yol haritasının kendi ölçütü "şifre sistemi
        # en yabancı olan". ① ve ② onu takip eder: "kısıt taraması en
        # yoğun". Kalanlar üretim riskidir ve daha hafif tartılır.
        n = max(1, len(cids))

        # BURDEN — toplam üretim yükü. Kültür sayısıyla büyür ve BÜYÜMELİDİR:
        # beş kültürlük bir bölge gerçekten daha çok iştir.
        burden = (foreign * 3.0 + tier * 2.5 + forbidden * 1.5
                  + living * 1.0 + supply * 1.0 + seals * 0.5 + risky * 1.0)

        # INTENSITY — kültür başına sertlik. Toplanan eksenler kültür
        # sayısına bölünür; bölgeye ait olan eksenler (arz, mühür) bölünmez
        # çünkü onlar zaten bölge düzeyinde tanımlıdır.
        intensity = ((foreign / n) * 3.0 + (tier / n) * 2.5
                     + (forbidden / n) * 1.5 + (living / n) * 1.0
                     + supply * 1.0 + seals * 0.5 + (risky / n) * 1.0)

        rows.append({
            "region": rid,
            "en": r.get("en"),
            "order": r.get("order"),
            "cultures": cids,
            "candidates": len(pool),
            "quota": quota,
            "tierWeight": tier,
            "forbiddenForms": forbidden,
            "livingTraditions": living,
            "writingForeignness": foreign,
            "usableStories": stories,
            "supplyPressure": supply,
            "sealLetters": seals,
            "unauthorisedStoryCandidates": risky,
            "burdenScore": round(burden, 2),
            "intensityScore": round(intensity, 2),
        })
    rows.sort(key=lambda x: -x["intensityScore"])
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    print("=" * 74)
    print("  BÖLGE ZORLUK ÖLÇÜMÜ — pilot bölgesi HESAPLANIR")
    print("=" * 74)

    acts_doc = load(ACTIVITY_INDEX)
    reg_doc = load(REGION_INDEX)
    cul_doc = load(CULTURE_INDEX)
    man = load(MANIFEST)
    if not (acts_doc and reg_doc and cul_doc and man):
        print("  ⊘ dizinler yok — ölçüm yapılamıyor")
        return 2

    acts = acts_doc.get("activities", acts_doc)
    regions = reg_doc.get("regions", reg_doc)
    cultures = cul_doc.get("cultures", cul_doc)
    records = {r["recordId"]: r for r in man.get("records", [])}

    rows = measure(acts, regions, cultures, records)

    print("\n  %-15s %3s %5s %5s %5s %5s %5s %5s %5s %8s %9s"
          % ("bölge", "kül", "yazı", "kdm", "yasak", "canlı", "arz", "mühür",
             "risk", "YÜK", "YOĞUNLUK"))
    for x in rows:
        print("  %-15s %3d %5d %5d %5d %5d %5.2f %5d %5d %8.2f %9.2f"
              % (x["region"], len(x["cultures"]), x["writingForeignness"],
                 x["tierWeight"], x["forbiddenForms"], x["livingTraditions"],
                 x["supplyPressure"], x["sealLetters"],
                 x["unauthorisedStoryCandidates"],
                 x["burdenScore"], x["intensityScore"]))

    win = rows[0]
    runner = rows[1]
    heaviest = max(rows, key=lambda x: x["burdenScore"])

    print("\n  ▸ PİLOT BÖLGESİ (en yoğun): %s (%s) — yoğunluk %.2f"
          % (win["region"], win["en"], win["intensityScore"]))
    print("    ikinci: %s (%.2f) · fark %.2f"
          % (runner["region"], runner["intensityScore"],
             win["intensityScore"] - runner["intensityScore"]))
    if heaviest["region"] != win["region"]:
        print("\n  ! EN YÜKSEK TOPLAM YÜK BAŞKA BİR BÖLGEDE: %s (%.2f)"
              % (heaviest["region"], heaviest["burdenScore"]))
        print("    %d kültür taşıyor. Pilot değil ama üretim planlamasında"
              % len(heaviest["cultures"]))
        print("    SONA BIRAKILAMAZ — yük kültür sayısıyla birlikte gelir.")

    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": "measured",
                       "selectionRule": "highest intensityScore",
                       "pilotRegion": win["region"],
                       "runnerUp": runner["region"],
                       "intensityMargin": round(
                           win["intensityScore"] - runner["intensityScore"], 2),
                       "heaviestBurden": heaviest["region"],
                       "rows": rows}, fh, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
