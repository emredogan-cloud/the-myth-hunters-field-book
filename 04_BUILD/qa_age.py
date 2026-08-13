#!/usr/bin/env python3
"""
YAŞ VE GÜVENLİK KAPISI — The Myth Hunter's Field Book
================================================================================
BU BİR ÇOCUK ÜRÜNÜDÜR ve bu kapı otomatik REDDETME yetkisine sahiptir.
World Myths'in dersi (D7): bir yaş kapısı, doğru çalıştığı KANITLANMADAN
kullanılamaz. `05_TESTS/selftest.py § ⑤` her dalın ısırdığını kanıtlar.

World Myths'te risk OKUNAN şiddetti. Burada risk YAPILAN görevdir:
çocuk artık yalnızca okumuyor — yazıyor, çiziyor, çözüyor. Deftere
yazdığı kalıyor.

Dokuz denetim:

  ① GÜVENLİK SINIFI  — safetyClass malzemeden HESAPLANIR ve beyanla karşılaştırılır
  ② KAPALI ARIZA     — tanınmayan malzeme `safe` DEĞİL, `do-not-use`tur
  ③ EBEVEYN NOTU     — safe-with-adult bir not olmadan sayfaya çıkamaz
  ④ DÜŞÜRME          — do-not-use / restricted / excluded kitapta kalamaz
  ⑤ BETİMLEME        — "şiddeti çiz" ile "kahramanı çiz" farkı MEKANİK olarak ayrılır
  ⑥ YASAK ÇERÇEVE    — altı yasak çerçevenin anahtar sözcük taraması
  ⑦ ZORLUK           — ★★★ oranı %30'u aşamaz; ★ iki adımdan uzun olamaz
  ⑧ DENETİM YÜKÜ     — safe-with-adult oranı %10'u aşamaz
  ⑨ ATIF             — atıf zorunluysa kültür adı ÇOCUĞUN GÖRDÜĞÜ metinde mi ⭑

⑧ NEDEN VAR: ebeveyn bu kitapta MEŞGULİYET satın alıyor. Yarısı yetişkin
eşliği isteyen bir aktivite kitabı, ebeveyne iş çıkarır ve vaadi bozar.

TASARIM: yalnızca Python standart kütüphanesi (karar K7).

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
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
ACTIVITY_INDEX = os.path.join(ROOT, "01_SOURCE", "activity_index.json")
REGION_INDEX = os.path.join(ROOT, "01_SOURCE", "region_index.json")
MANIFEST = os.path.join(ROOT, "01_SOURCE", "inherited", "IMPORT_MANIFEST.json")
BOOK = os.path.join(ROOT, "02_MANUSCRIPT", "book.json")

# ── AGE_POLICY § 3.1 · malzeme beyaz listesi ───────────────────────────────
# ⚠ Bu üç küme belgeyle BİREBİR aynı olmalıdır. selftest § ⑤(a) uyumu denetler.
T0 = {"book", "pencil", "coloured-pencils", "eraser",
      "ruler", "paper-strip", "window-view"}
T1 = {"mirror", "string", "coin", "torch", "read-aloud-partner"}
# TX hiçbir yerde TANIMLI DEĞİLDİR — şemadan da geçemez. Burada yalnızca
# raporlamak ve selftest'in kurgusunu beslemek için adlandırılır.
TX = {"scissors", "blade", "needle", "pin", "fire", "match", "candle",
      "food", "liquid", "small-parts", "magnet", "balloon",
      "outdoor-site", "heat-source"}

BLOCKING_RESTRICTION = {"restricted", "excluded"}

# ── AGE_POLICY § 4 · betimleme fiili × işaretli ad ─────────────────────────
DEPICTION_VERBS = r"(?:draw|sketch|paint|colour|color|show|act\s+out|" \
                  r"describe|retell|re-?enact|perform|mime)"
FLAGGED_NOUNS = r"(?:wound|wounds|blood|bleeding|killing|kill|corpse|body|" \
                r"sacrifice|torture|devour|devouring|eating\s+(?:a\s+)?(?:man|person|child)|" \
                r"beheading|behead|drowning|drown|slaughter|mutilat\w*|" \
                r"severed|dismember\w*)"
DEPICTION_RE = re.compile(
    DEPICTION_VERBS + r"[^.!?]{0,60}?" + FLAGGED_NOUNS, re.IGNORECASE)

# ── AGE_POLICY § 2 · altı yasak çerçeve · anahtar sözcük taraması ──────────
# Bir eşleşme kesin ihlal DEĞİLDİR — bir İNCELEME TALEBİDİR. Bu yüzden
# eşleşen aktivite restrictionNote veya parentNote taşımak zorundadır:
# yani biri o çerçeveye BAKMIŞ olmalıdır.
FRAME_PATTERNS = [
    ("1 · kutsal ritüelin taklidi",
     r"\b(?:ritual|ceremony|ceremonial|prayer|chant|incantation|initiation|"
     r"hula|haka|karakia|oli|mele|puja|jesa|gut\b|harae|norito)\b"),
    ("2 · kapalı bilginin çözülmesi",
     r"\b(?:divination|oracle|fortune[- ]tell\w*|ifa\b|i\s?ching|"
     r"tonalpohualli|whakapapa|secret\s+knowledge|sacred\s+secret)\b"),
    ("3 · karikatürleştirme",
     r"\b(?:tribal\s+chief|witch\s?doctor|savage|primitive\s+people|"
     r"native\s+costume|exotic\s+tribe)\b"),
    ("4 · şiddetin sahnelenmesi",
     r"\b(?:battle\s+scene|war\s+scene|execution|massacre|the\s+killing\s+of)\b"),
    ("5 · evden çıkma",
     r"\b(?:go\s+outside|outdoors|in\s+the\s+garden|in\s+the\s+park|"
     r"on\s+your\s+street|leave\s+the\s+house|field\s+trip)\b"),
    # ⚠ 'match' BURADA GEÇMEZ ve geçmemelidir: bu kitabın en yaygın
    # tasarım fiili "matches" (eşleştirir). Kibrit yalnızca kibrit
    # olduğu apaçık olan biçimlerde aranır. Bu düzeltme kapının ilk
    # koşusunda yapıldı: regex 168 adayın 13'ünü yanlışlıkla reddetti.
    ("6 · kesici alet, ateş, yiyecek",
     r"\b(?:scissors|knife|knives|blade|razor|needle|pin\b|candle|"
     r"matchstick|matchsticks|box\s+of\s+matches|(?:strike|light)\s+a\s+match|"
     r"lighter|flame|bonfire|boil|cook|bake|fry|taste\s+it|eat\s+it)\b"),
]
FRAME_RE = [(name, re.compile(pat, re.IGNORECASE)) for name, pat in FRAME_PATTERNS]

INSTRUCTION_MAX_WORDS_DEFAULT = 18


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


# ═══════════════════════════════════════════════════════════════════════════
# AGE_POLICY § 3.2 karar ağacının BİREBİR kodu.
# Bu fonksiyon değişirse belge de değişmelidir; selftest ikisini bağlar.
# ═══════════════════════════════════════════════════════════════════════════
def classify(materials, restriction_status, frame_hit, needs_adult):
    """Güvenlik sınıfını HESAPLAR. 'Bence güvenli' bir girdi değildir."""
    mats = list(materials or [])

    # ① TX malzeme → hemen dışarı
    if any(m in TX for m in mats):
        return "do-not-use"
    # ② yasak çerçeve ihlali
    if frame_hit:
        return "do-not-use"
    # ③ kısıt taraması engelliyor
    if restriction_status in BLOCKING_RESTRICTION:
        return "do-not-use"
    # ④ KAPALI ARIZA: tanınmayan malzeme `safe` DEĞİLDİR
    if not mats or any(m not in (T0 | T1) for m in mats):
        return "do-not-use"
    # ⑤ T1 malzeme → yetişkin
    if any(m in T1 for m in mats):
        return "safe-with-adult"
    # ⑥ açıkça yetişkin isteyen tasarım
    if needs_adult:
        return "safe-with-adult"
    # ⑦ aksi hâlde
    return "safe"


def child_text(a: dict) -> str:
    """Çocuğa görünen ya da görünecek olan metin.

    Faz 1'de yalnızca tasarım katmanı vardır (objective/title). Faz 2'de
    proza gelir (prompt/steps/hints) ve aynı tarama onu da kapsar."""
    parts = [a.get("title", ""), a.get("objective", ""),
             a.get("prompt", ""), a.get("setup", ""),
             a.get("learningObjective", ""), a.get("culturalContext", "")]
    parts += list(a.get("steps") or [])
    parts += list(a.get("hints") or [])
    return " \n".join(p for p in parts if p)


def scan_frames(text: str):
    return [name for name, rx in FRAME_RE if rx.search(text)]


def check_safety(acts, rep):
    print("\n── ① güvenlik sınıfı · ② kapalı arıza ──")
    mismatched, undeclared = [], []
    for a in acts:
        text = child_text(a)
        frames = scan_frames(text)
        # Bir çerçeve eşleşmesi, o çerçeveye BAKILMIŞ olmasını şart koşar.
        unreviewed = bool(frames) and not (a.get("restrictionNote")
                                           or a.get("parentNote")
                                           or a.get("safetyNotes"))
        want = classify(a.get("materials"), a.get("restrictionStatus"),
                        unreviewed, a.get("needsAdult", False))
        got = a.get("safetyClass")
        if got is None:
            undeclared.append(a["activityId"])
        elif got != want:
            mismatched.append("%s: beyan=%s hesap=%s" % (a["activityId"], got, want))

    rep.check(not undeclared, "her aktivite bir güvenlik sınıfı taşıyor"
              + ("" if not undeclared else " — SINIFSIZ: %s" % undeclared[:5]))
    rep.check(not mismatched, "beyan edilen sınıf hesaplanana eşit"
              + ("" if not mismatched else " — ÇELİŞKİ: %s" % mismatched[:5]))

    # Kapalı arıza kanıtı: beyaz liste dışı malzeme taşıyan aktivite yok.
    stray = ["%s → %s" % (a["activityId"],
                          [m for m in (a.get("materials") or [])
                           if m not in (T0 | T1)])
             for a in acts
             if any(m not in (T0 | T1) for m in (a.get("materials") or []))
             or not a.get("materials")]
    rep.check(not stray, "beyaz liste dışı veya malzemesiz aktivite yok"
              + ("" if not stray else " — TANINMAYAN: %s" % stray[:5]))

    dist = collections.Counter(a.get("safetyClass") for a in acts)
    rep.facts["safetyDistribution"] = dict(dist)
    return dist


def check_parent_notes(acts, rep):
    print("\n── ③ ebeveyn notu ──")
    missing = [a["activityId"] for a in acts
               if a.get("safetyClass") == "safe-with-adult" and not a.get("parentNote")]
    rep.check(not missing, "her safe-with-adult aktivitesi ebeveyn notu taşıyor"
              + ("" if not missing else " — NOTSUZ: %s" % missing[:5]))


def check_dropped(acts, rep):
    print("\n── ④ düşürme kuralı ──")
    live_bad = [a["activityId"] for a in acts
                if a.get("safetyClass") == "do-not-use" and a.get("status") != "dropped"]
    rep.check(not live_bad, "do-not-use aktivite kitapta kalmıyor"
              + ("" if not live_bad else " — KİTAPTA: %s" % live_bad[:5]))

    restr = [a["activityId"] for a in acts
             if a.get("restrictionStatus") in BLOCKING_RESTRICTION
             and a.get("status") != "dropped"]
    rep.check(not restr, "restricted/excluded aktivite kitapta kalmıyor"
              + ("" if not restr else " — KİTAPTA: %s" % restr[:5]))

    unscreened = [a["activityId"] for a in acts if not a.get("restrictionStatus")]
    rep.check(not unscreened, "kısıt taraması muafiyetsiz — taranmamış aktivite yok"
              + ("" if not unscreened else " — TARANMAMIŞ: %s" % unscreened[:5]))


def check_depiction(acts, rep):
    print("\n── ⑤ betimleme fiili × işaretli ad ──")
    hits = []
    for a in acts:
        m = DEPICTION_RE.search(child_text(a))
        if m:
            hits.append("%s → '%s'" % (a["activityId"], m.group(0)[:50]))
    rep.check(not hits, "şiddetin betimlenmesini isteyen görev yok"
              + ("" if not hits else " — İHLAL: %s" % hits[:5]))


def check_frames(acts, rep):
    print("\n── ⑥ altı yasak çerçeve ──")
    unreviewed, reviewed = [], []
    for a in acts:
        frames = scan_frames(child_text(a))
        if not frames:
            continue
        if a.get("restrictionNote") or a.get("parentNote") or a.get("safetyNotes"):
            reviewed.append("%s (%s)" % (a["activityId"], frames[0]))
        else:
            unreviewed.append("%s → %s" % (a["activityId"], ", ".join(frames)))
    rep.facts["frameHitsReviewed"] = len(reviewed)
    rep.check(not unreviewed,
              "yasak çerçeveye değen her aktivite incelenmiş ve not taşıyor"
              + ("" if not unreviewed else " — İNCELENMEMİŞ: %s" % unreviewed[:5]))
    if reviewed:
        rep.warn("%d aktivite bir çerçeveye değiyor ve incelenmiş: %s"
                 % (len(reviewed), reviewed[:3]))


def check_difficulty(cfg, acts, regions, rep):
    print("\n── ⑦ zorluk ve talimat uzunluğu ──")
    over = []
    for r in regions:
        in_region = [a for a in acts if a.get("region") == r["id"]]
        if not in_region:
            continue
        hard = sum(1 for a in in_region if a.get("difficulty") == 3)
        ratio = hard / len(in_region)
        if ratio > 0.30:
            over.append("%s %.1f%%" % (r["id"], ratio * 100))
    rep.check(not over, "★★★ oranı hiçbir bölgede sınırı aşmıyor"
              + ("" if not over else " — AŞIM: %s" % over))

    # ★ tek adımlıdır. Adım yoksa (Faz 1) denetim boş koşar.
    long_easy = [a["activityId"] for a in acts
                 if a.get("difficulty") == 1 and len(a.get("steps") or []) > 2]
    rep.check(not long_easy, "★ aktiviteleri iki adımı aşmıyor"
              + ("" if not long_easy else " — UZUN: %s" % long_easy[:5]))

    limit = cfg.get("safety", {}).get("instructionMaxSentenceWords",
                                      INSTRUCTION_MAX_WORDS_DEFAULT)
    too_long = []
    for a in acts:
        for s in (a.get("steps") or []):
            for sent in re.split(r"(?<=[.!?])\s+", s):
                n = len(sent.split())
                if n > limit:
                    too_long.append("%s (%d kelime)" % (a["activityId"], n))
                    break
    rep.check(not too_long, "talimat cümlesi %d kelimeyi aşmıyor" % limit
              + ("" if not too_long else " — UZUN: %s" % too_long[:5]))
    rep.facts["stepsPresent"] = sum(1 for a in acts if a.get("steps"))


def check_supervision_load(acts, dist, rep):
    print("\n── ⑧ denetim yükü ──")
    n = len(acts)
    adult = dist.get("safe-with-adult", 0)
    ratio = adult / n if n else 0
    rep.facts["safeWithAdultRatio"] = round(ratio, 3)
    rep.check(ratio <= 0.10,
              "safe-with-adult oranı sınırın altında (%.1f%% ≤ 10%%)" % (ratio * 100))
    safe_ratio = dist.get("safe", 0) / n if n else 0
    rep.facts["safeRatio"] = round(safe_ratio, 3)
    rep.check(safe_ratio >= 0.90,
              "safe oranı hedefin üstünde (%.1f%% ≥ 90%%)" % (safe_ratio * 100))


# ── AGE_POLICY § 4 · CULTURE_POLICY § 3 · kültür adı eşleyicileri ──────────
# Kademe A/B/C fark etmez: attributionRequired olan her sayfada kültürün
# adı ÇOCUĞUN GÖRDÜĞÜ metinde geçmelidir. Bir kültürün adı birden çok
# meşru biçimde yazılabilir; liste onları taşır.
#
# ⚠ FAZ 3'TE DÜZELTİLDİ — KAPI DOĞRU İMLÂYI CEZALANDIRIYORDU.
#
# Liste yalnızca diakritiksiz biçimleri taşıyordu ve denetim düz alt-dize
# araması yapıyor. Sonuç: doğru yazılmış **Māori** sayfada geçtiği hâlde
# kapı 'atıfsız' diyordu, çünkü "māori" içinde "maori" alt-dizesi YOKTUR.
#
# Bu kusurun tehlikeli tarafı yanlış pozitif olması değil, ÖNERDİĞİ
# ÇÖZÜMDÜR: kapıyı yeşile çevirmenin en kolay yolu sayfada makronu
# düşürüp "Maori" yazmaktı. Yani kapı, kendisini susturmak isteyen bir
# yazarı bir halkın adını YANLIŞ yazmaya iter.
#
#     Bir kapı, doğru olanı yapmayı pahalı hâle getiriyorsa,
#     düzeltilmesi gereken kapıdır.
#
# `validate_research § ⑧` zaten diakritiklerin korunmasını ŞART KOŞUYOR;
# iki kapı birbirine ters çalışıyordu. Liste artık diakritikli biçimi de
# taşıyor ve `selftest § ⑤b` doğru yazılmış bir adın GEÇTİĞİNİ kanıtlıyor.
CULTURE_NAMES = {
    "maya": ["maya", "k'iche", "kiche", "popol vuh"],
    "aztec": ["aztec", "nahuatl", "mexica", "tenochtitlan"],
    "andean": ["andean", "andes", "quechua", "inca", "inka", "huarochiri"],
    "inuit": ["inuit", "inuktitut", "nunavut"],
    "norse": ["norse", "viking", "icelandic"],
    "finnish": ["finnish", "finland", "kalevala"],
    "irish": ["irish", "ireland", "ogham"],
    "greek": ["greek", "greece"],
    "egyptian": ["egyptian", "egypt", "nile"],
    "mesopotamian": ["mesopotamian", "sumerian", "babylonian", "akkadian"],
    "yoruba": ["yoruba"],
    "akan": ["akan", "ashanti", "asante", "ghana"],
    "zulu": ["zulu", "isizulu"],
    "persian": ["persian", "iran", "shahnameh"],
    "turkic": ["turkic", "turkish", "altai", "orkhon", "dede korkut"],
    "hindu": ["hindu", "sanskrit", "india", "devanagari"],
    "vietnamese": ["vietnamese", "vietnam", "việt"],
    "chinese": ["chinese", "china"],
    "japanese": ["japanese", "japan"],
    "korean": ["korean", "korea", "hangul"],
    "maori": ["maori", "māori", "aotearoa", "new zealand"],
    "hawaiian": ["hawaiian", "hawai"],   # "hawai" makronsuz da, Hawaiʻi de yakalar
}


def check_attribution(acts, rep):
    """⑨ ATIF — kültür adı SAYFADA geçiyor mu.

    ⭑ BU DENETİM İÇ EDİTORYAL İNCELEMEDEN DOĞDU ve pilotun 16 sayfasının
    11'inde ihlal buldu. ⭑

    `CULTURE_POLICY § 3` Kademe A, B ve C için de aynı şeyi söylüyor:
    *"Atıf zorunlu; kültürün adı sayfada geçer."* Tasarım katmanında
    `attributionRequired: true` yazıyordu ve 16 sayfanın 16'sı onu
    taşıyordu — ama ÇOCUĞUN GÖRDÜĞÜ metinde kültür adı yalnızca beş
    sayfada geçiyordu.

        "A khipu counts in tens."   → kimin khipusu?
        "In this account a llama…"  → hangi anlatı?

    Adı olmayan bir nesne bir merak nesnesidir; adı olan bir nesne bir
    HALKIN İŞİDİR. Bu kitabın tezi tam olarak ikincisidir.

    ⚠ Faz 1'de `validate_research § ⑦` yalnızca `culturalContext` alanının
    DOLU olmasını denetliyordu. Dolu bir tasarım alanı, sayfada basılı bir
    ad demek DEĞİLDİR."""
    print("\n── ⑨ atıf ──")
    missing = []
    checked = 0
    for a in acts:
        if not a.get("attributionRequired"):
            continue
        # Yalnızca prozası YAZILMIŞ sayfalar denetlenir: tasarım katmanında
        # çocuk-görünür metin henüz yoktur ve yokluğu bir ihlal değildir.
        if not (a.get("prompt") or a.get("fieldNote")):
            continue
        checked += 1
        seen = " ".join([a.get("prompt", ""), a.get("fieldNote", "")]
                        + list(a.get("steps") or [])
                        + list(a.get("hints") or [])).lower()
        names = CULTURE_NAMES.get(a.get("culture"), [a.get("culture", "")])
        if not any(n in seen for n in names if n):
            missing.append("%s (%s)" % (a["activityId"], a.get("culture")))
    rep.facts["attributionChecked"] = checked
    rep.check(not missing,
              "atıf gereken her yazılmış sayfada kültür adı geçiyor (%d sayfa)"
              % checked
              + ("" if not missing else " — ATIFSIZ: %s" % missing[:6]))


def check_content_flags(acts, manifest, rep):
    print("\n── kaynak işaretleri ve kapalı katmanlar ──")
    if manifest is None:
        rep.warn("manifest yok — kaynak işaret denetimi boş koşuyor")
        return
    by_id = {r["recordId"]: r for r in manifest.get("records", [])}

    excluded_used = []
    for a in acts:
        s = a.get("sourceStory")
        if not s:
            continue
        rec = by_id.get(s)
        if rec is None:
            continue
        if rec.get("activityExcludedReason"):
            excluded_used.append("%s → %s" % (a["activityId"], s))
    rep.check(not excluded_used,
              "aktivite dışı bırakılmış hikâyeden aday türetilmemiş"
              + ("" if not excluded_used else " — İHLAL: %s" % excluded_used[:5]))

    # Kapalı katmanlı bir hikâyeye dayanan aday, kapalı katmanı bilmelidir.
    layered = sum(1 for a in acts
                  if a.get("sourceStory") and by_id.get(a["sourceStory"], {}).get("forbiddenLayer"))
    rep.facts["activitiesOnLayeredStories"] = layered
    if layered:
        rep.warn("%d aday kapalı katmanlı bir hikâyeye dayanıyor — proza "
                 "yazılırken o katman AÇILAMAZ (Faz 2)" % layered)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    print("=" * 74)
    print("  YAŞ VE GÜVENLİK KAPISI")
    print("=" * 74)

    rep = Report(args.verbose)
    cfg = load(CONFIG, rep)
    if cfg is None:
        return 1

    acts_doc = load(ACTIVITY_INDEX, rep, required=False)
    reg_doc = load(REGION_INDEX, rep, required=False)
    manifest = load(MANIFEST, rep, required=False)

    if acts_doc is None:
        rep.warn("activity_index.json yok — Faz 1 teslimatı; yaş kapısı boş koşuyor")
        print("\n" + "=" * 74)
        print("  ⊘ boş koştu (envanter henüz yok)")
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
    all_acts = acts_doc.get("activities", acts_doc)
    regions = (reg_doc or {}).get("regions", []) if reg_doc else []

    # Manuscript varsa proza katmanı da taranır (Faz 2+).
    book = load(BOOK, rep, required=False)
    if book:
        prose = {b.get("activityId"): b for b in book.get("activities", [])}
        merged = 0
        for a in acts:
            p = prose.get(a["activityId"])
            if p:
                a = a.update(p) or a
                merged += 1
        rep.facts["proseMerged"] = merged
        print("  · manuscript bulundu — proza katmanı da taranıyor (%d)" % merged)

    rep.facts["activitiesScanned"] = len(acts)
    dist = check_safety(acts, rep)
    check_parent_notes(acts, rep)
    check_dropped(all_acts, rep)
    check_depiction(acts, rep)
    check_frames(acts, rep)
    if regions:
        check_difficulty(cfg, acts, regions, rep)
    check_supervision_load(acts, dist, rep)
    check_attribution(acts, rep)
    check_content_flags(acts, manifest, rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · %d aktivite tarandı · %s"
              % (rep.checks, len(acts), dict(dist)))
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
