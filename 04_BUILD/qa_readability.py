#!/usr/bin/env python3
"""
OKUNABİLİRLİK KAPISI — The Myth Hunter's Field Book
================================================================================
Bu kitapta okunabilirlik bir üslup tercihi değil bir İŞLEV meselesidir:
çocuk metni okumaz, KULLANIR. Anlamadığı bir talimat onu sayfada durdurur
ve durduğu yerde kitabı bırakır.

    Çocuk takılıyorsa suç çocukta değil TALİMATTADIR.

⭑ SAYFADA ÜÇ AYRI REGİSTER VARDIR VE TEK BANTLA ÖLÇÜLEMEZ ⭑

Bu kapının ilk hâli tek bir bant taşıyordu (9–14 kelime · 3.–5. sınıf) ve
o bant World Myths'in ANLATI prozasından devralınmıştı. Faz 1 pilotu
bandın bu kitapta YANLIŞ olduğunu ölçtü: harman 8,28 kelime / FK 2,95,
yani "bandın altında" — ama kusur metinde değil ÖLÇÜMDEYDİ.

    talimat    6,96 kelime/cümle · FK 2,03
    field note 10,36 kelime/cümle · FK 4,70
    ipucu       9,38 kelime/cümle · FK 2,86

Bir TALİMAT bir anlatı cümlesi değildir. "Read the age printed beside each
island." yedi kelimedir ve sekiz yaşındaki için DOĞRU uzunluktur.

Ne ölçer:

  ① TALİMAT REGİSTERİ  — ortalama 5–11 kelime · FK ≤ 4,0 · azami 18 kelime
  ② FIELD NOTE         — ortalama 9–14 kelime · FK 3,0–5,9
  ③ DEĞİŞMEZ           — fk(talimat) < fk(field note)
  ④ İPUCU              — FK ≤ 4,5; ipucu görevden zor olamaz
  ⑤ UZUN SÖZCÜK        — üç heceden uzun sözcük oranı ≤ %20
  ⑥ FIELD NOTE BOYU    — 15–35 kelime
  ⑦ YASAK KALIP        — STYLE.md § 4 kalıpları
  ⑧ KÜÇÜMSEYEN TON     — "little explorer" ve akrabaları
  ⑨ ÖN MADDE           — Faz 5'te doğdu · KİTABIN İLK OKUNAN METNİ

⑨ NEDEN AYRI BİR REGİSTER:

Ön madde, çocuğun kitapta okuduğu İLK metindir ve bir aktivite sayfası
değildir: bir talimat da değil, bir field note da değil. Kendi bandı yoksa
hiç ölçülmez — ve ölçülmeyen bir metin, kitabın en zor metni olabilir.

    Bir çocuk kitabın nasıl çalıştığını anlamadan
    ilk sayfayı çeviremez. Ön maddenin zorluğu bir
    ÜSLUP meselesi değil, bir ERİŞİM meselesidir.

Ve değişmez bir kat yukarı taşınır: ön madde, tanıttığı içerikten daha
zor olamaz. Kurucu talimatı Faz 5 § 8 bunu adıyla şart koşuyor —
*"Do NOT allow front matter to become harder than the activity content
without editorial reason."*

③ bu kapının en özgün denetimidir: bir talimat, tanıttığı içerikten
DAHA ZOR OLAMAZ. Olursa çocuk görevi değil cümleyi çözmeye çalışır.

⚠ MANUSCRIPT DEPODA DEĞİLDİR. Dosya yoksa kapı BOŞ KOŞAR ve yeşil yanar;
körlüğü `05_TESTS/selftest.py` kapatır. Bu, projenin kabul edilmiş
düzenidir (bkz. validate.yml § text).

Flesch–Kincaid hece sayımı bir SEZGİSELDİR ve ±0,5 sınıf sapabilir.
Bu yüzden bant geniş tutuldu ve gerçek ölçüt Faz 2'nin ÇOCUK TESTİDİR.

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
SOURCES = [
    os.path.join(ROOT, "02_MANUSCRIPT", "book.json"),
    os.path.join(ROOT, "02_MANUSCRIPT", "pilot", "pilot.json"),
]

FIELD_NOTE_TARGET = (15, 35)      # ~25 kelime bandı
PATRONISING = [
    r"\blittle\s+(?:explorer|reader|friend|one)\b",
    r"\byoung\s+(?:reader|explorer|friend)\b",
    r"\bboys\s+and\s+girls\b",
    r"\bdo\s+your\s+best\b",
    r"\btry\s+your\s+best\b",
]
VOWELS = "aeiouy"


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


def syllables(word: str) -> int:
    """Hece sezgiseli. Kesin değildir ve kesin olduğunu iddia etmez."""
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    count, prev_vowel = 0, False
    for ch in w:
        is_vowel = ch in VOWELS
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if w.endswith("e") and count > 1 and not w.endswith(("le", "ee", "ye")):
        count -= 1
    return max(1, count)


def sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?:])\s+", text) if s.strip()]


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-zʻ'’À-ɏḀ-ỿ-]+", text)


def fk_grade(n_words: int, n_sent: int, n_syll: int) -> float:
    if not n_words or not n_sent:
        return 0.0
    return 0.39 * (n_words / n_sent) + 11.8 * (n_syll / n_words) - 15.59


def child_text(a: dict) -> str:
    parts = [a.get("prompt", ""), a.get("fieldNote", "")]
    parts += list(a.get("steps") or [])
    parts += list(a.get("hints") or [])
    return " ".join(p for p in parts if p)


def load_activities(rep):
    found = []
    for path in SOURCES:
        if not os.path.isfile(path):
            continue
        try:
            with open(path, encoding="utf-8") as fh:
                doc = json.load(fh)
        except json.JSONDecodeError as exc:
            rep.check(False, "JSON bozuk: %s — %s" % (os.path.relpath(path, ROOT), exc))
            continue
        acts = doc.get("activities", [])
        if acts:
            found.append((os.path.relpath(path, ROOT), acts))
    return found


def _block(texts: list[str]) -> dict:
    w = s = sy = 0
    longest = 0
    for t in texts:
        ws = words(t)
        ss = sentences(t)
        w += len(ws)
        s += len(ss)
        sy += sum(syllables(x) for x in ws)
        for sent in ss:
            longest = max(longest, len(words(sent)))
    return {
        "words": w, "sentences": s,
        "avgSentenceWords": round(w / s, 2) if s else 0.0,
        "fkGrade": round(fk_grade(w, s, sy), 2),
        "maxSentenceWords": longest,
    }


def measure_registers(acts: list[dict]) -> dict:
    """Sayfadaki üç registeri AYRI ölçer.

    Harmanlanmış bir ortalama, kısa talimatları uzun field note'ların
    içinde gizler ve ikisini birden yanlış gösterir. Faz 1 pilotu tam
    olarak bunu ortaya çıkardı."""
    instruction, note, hint = [], [], []
    for a in acts:
        if a.get("prompt"):
            instruction.append(a["prompt"])
        instruction.extend(a.get("steps") or [])
        if a.get("fieldNote"):
            note.append(a["fieldNote"])
        hint.extend(a.get("hints") or [])
    return {"instruction": _block(instruction),
            "fieldNote": _block(note),
            "hint": _block(hint)}


def load_front_matter(rep):
    """Ön madde gövde metnini toplar.

    Yalnızca ÇOCUĞUN GÖRDÜĞÜ proza ölçülür: `bodyText`. `purpose` bir
    tasarım notudur ve sayfaya basılmaz; `prints` levha mobilyasıdır ve
    cümle değil ADDIR — ikisini de ölçüme katmak registeri kirletir."""
    for path in SOURCES:
        if not os.path.isfile(path):
            continue
        try:
            with open(path, encoding="utf-8") as fh:
                doc = json.load(fh)
        except json.JSONDecodeError:
            continue
        fm = doc.get("frontMatter")
        if not fm:
            continue
        secs = fm.get("sections", [])
        # ⚠ YALNIZCA ÖĞRETİM SAYFALARI ÖLÇÜLÜR.
        #
        # Başlık ve künye sayfaları çocuğa okutulmak için yazılmaz: bir
        # telif uyarısı hukukî bir cümledir ve uzundur. Onu çocuk
        # registerine katmak iki şeyi birden bozar — bandı yalancı biçimde
        # yukarı çeker VE düzeltmek için hukukî metni kısaltmaya iter.
        #
        #     Bir ölçüm, ölçmemesi gereken şeyi ölçerse,
        #     düzeltilecek şey metin değil ÖLÇÜMDÜR.
        return [(s.get("id"), s.get("bodyText") or "") for s in secs
                if (s.get("bodyText") or "").strip()
                and s.get("role", "teaching") == "teaching"]
    return []


def measure(acts):
    total_w = total_s = total_syll = 0
    long_words = 0
    per_activity = []
    for a in acts:
        t = child_text(a)
        ws = words(t)
        ss = sentences(t)
        sy = sum(syllables(w) for w in ws)
        lw = sum(1 for w in ws if syllables(w) >= 3)
        total_w += len(ws)
        total_s += len(ss)
        total_syll += sy
        long_words += lw
        per_activity.append({
            "activityId": a.get("activityId"),
            "words": len(ws),
            "sentences": len(ss),
            "avgSentenceWords": round(len(ws) / len(ss), 2) if ss else 0,
            "fkGrade": round(fk_grade(len(ws), len(ss), sy), 2),
            "longWordRatio": round(lw / len(ws), 3) if ws else 0,
            "fieldNoteWords": len(words(a.get("fieldNote", ""))),
            "steps": len(a.get("steps") or []),
        })
    return {
        "words": total_w, "sentences": total_s,
        "avgSentenceWords": round(total_w / total_s, 2) if total_s else 0,
        "fkGrade": round(fk_grade(total_w, total_s, total_syll), 2),
        "longWordRatio": round(long_words / total_w, 3) if total_w else 0,
        "perActivity": per_activity,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    print("=" * 74)
    print("  OKUNABİLİRLİK")
    print("=" * 74)

    rep = Report(args.verbose)
    with open(CONFIG, encoding="utf-8") as fh:
        cfg = json.load(fh)
    saf = cfg.get("safety", {})
    lo_avg = saf.get("sentenceAvgWordsMin", 9.0)
    hi_avg = saf.get("sentenceAvgWordsMax", 14.0)
    g_lo, g_hi = saf.get("readabilityTargetGrade", [3, 5])

    found = load_activities(rep)
    if not found:
        print("\n  ⊘ ölçülecek metin yok (manuscript depoda durmaz) — BOŞ KOŞTU")
        print("=" * 74)
        if args.json:
            os.makedirs(os.path.dirname(args.json), exist_ok=True)
            with open(args.json, "w", encoding="utf-8") as fh:
                json.dump({"status": "empty", "checks": 0, "errors": [],
                           "warnings": [], "facts": {}}, fh,
                          ensure_ascii=False, indent=2)
        return 0

    all_acts = []
    for rel, acts in found:
        print("\n  · %s → %d aktivite" % (rel, len(acts)))
        all_acts.extend(acts)

    m = measure(all_acts)
    rep.facts.update(m)

    # ── REGİSTER AYRIMI ────────────────────────────────────────────────────
    # Bir TALİMAT bir anlatı cümlesi değildir ve aynı bantla ölçülemez.
    # Faz 1 pilot ölçümü bunu gösterdi: harmanlanmış ortalama iki registeri
    # birbirinin içinde gizliyordu. Ayrıntı: project_config § readabilityRegisters
    reg = saf.get("readabilityRegisters", {})
    regs = measure_registers(all_acts)
    rep.facts["registers"] = regs

    print("\n── ölçüm · register ──")
    print("  %-12s %6s %6s %8s %7s" % ("register", "kelime", "cümle", "ort", "FK"))
    for name in ("instruction", "fieldNote", "hint"):
        r = regs[name]
        print("  %-12s %6d %6d %8.2f %7.2f"
              % (name, r["words"], r["sentences"], r["avgSentenceWords"], r["fkGrade"]))
    print("  %-12s %6d %6d %8.2f %7.2f"
          % ("HARMAN", m["words"], m["sentences"], m["avgSentenceWords"], m["fkGrade"]))
    print("  uzun sözcük oranı %5.1f%%" % (m["longWordRatio"] * 100))

    print("\n── ① talimat registeri ──")
    ri = reg.get("instruction", {})
    ins = regs["instruction"]
    if ins["sentences"]:
        rep.check(ri.get("avgWordsMin", 5.0) <= ins["avgSentenceWords"]
                  <= ri.get("avgWordsMax", 11.0),
                  "talimat ortalaması bantta (%.2f ∈ [%.1f, %.1f])"
                  % (ins["avgSentenceWords"], ri.get("avgWordsMin", 5.0),
                     ri.get("avgWordsMax", 11.0)))
        rep.check(ins["fkGrade"] <= ri.get("fkGradeMax", 4.0),
                  "talimat okuma seviyesi tavanın altında (%.2f ≤ %.1f)"
                  % (ins["fkGrade"], ri.get("fkGradeMax", 4.0)))
        rep.check(ins["maxSentenceWords"] <= ri.get("maxSentenceWords", 18),
                  "en uzun talimat cümlesi sınırda (%d ≤ %d kelime)"
                  % (ins["maxSentenceWords"], ri.get("maxSentenceWords", 18)))

    print("\n── ② field note registeri ──")
    rf = reg.get("fieldNote", {})
    fnr = regs["fieldNote"]
    if fnr["sentences"]:
        rep.check(rf.get("avgWordsMin", lo_avg) <= fnr["avgSentenceWords"]
                  <= rf.get("avgWordsMax", hi_avg),
                  "field note ortalaması bantta (%.2f ∈ [%.1f, %.1f])"
                  % (fnr["avgSentenceWords"], rf.get("avgWordsMin", lo_avg),
                     rf.get("avgWordsMax", hi_avg)))
        rep.check(rf.get("fkGradeMin", float(g_lo)) <= fnr["fkGrade"]
                  <= rf.get("fkGradeMax", g_hi + 0.9),
                  "field note okuma seviyesi 3.–5. sınıf bandında (%.2f)"
                  % fnr["fkGrade"])

    print("\n── ③ DEĞİŞMEZ: talimat içerikten kolay olmalı ──")
    if ins["sentences"] and fnr["sentences"]:
        rep.check(ins["fkGrade"] < fnr["fkGrade"],
                  "talimat, tanıttığı içerikten DAHA KOLAY (%.2f < %.2f)"
                  % (ins["fkGrade"], fnr["fkGrade"]))

    print("\n── ④ ipucu registeri ──")
    rh = reg.get("hint", {})
    h = regs["hint"]
    if h["sentences"]:
        rep.check(h["fkGrade"] <= rh.get("fkGradeMax", 4.5),
                  "ipuçları tavanın altında (%.2f ≤ %.1f)"
                  % (h["fkGrade"], rh.get("fkGradeMax", 4.5)))

    print("\n── ⑤ uzun sözcük ──")
    rep.check(m["longWordRatio"] <= 0.20,
              "üç heceli ve üstü sözcük oranı sınırda (%.1f%% ≤ 20%%)"
              % (m["longWordRatio"] * 100))

    print("\n── ⑥ field note uzunluğu ──")
    lo_fn = rf.get("wordsMin", FIELD_NOTE_TARGET[0])
    hi_fn = rf.get("wordsMax", FIELD_NOTE_TARGET[1])
    off = ["%s (%d kelime)" % (p["activityId"], p["fieldNoteWords"])
           for p in m["perActivity"]
           if p["fieldNoteWords"] and not (lo_fn <= p["fieldNoteWords"] <= hi_fn)]
    rep.check(not off, "kültürel bilgi kutuları %d–%d kelime bandında" % (lo_fn, hi_fn)
              + ("" if not off else " — BANT DIŞI: %s" % off))

    print("\n── ⑦ yasak kalıp ──")
    blob = " ".join(child_text(a) for a in all_acts)
    hits = [p for p in cfg.get("style", {}).get("forbiddenPatterns", [])
            if p.lower().replace(" … ", " ") in blob.lower()]
    rep.check(not hits, "yasak kalıp yok"
              + ("" if not hits else " — KALIP: %s" % hits))

    print("\n── ⑧ küçümseyen ton ──")
    pat = [p for p in PATRONISING if re.search(p, blob, re.IGNORECASE)]
    rep.check(not pat, "küçümseyen hitap yok"
              + ("" if not pat else " — TON: %s" % pat))

    # ── ⑨ ÖN MADDE REGİSTERİ ───────────────────────────────────────────────
    print("\n── ⑨ ön madde registeri ──")
    front = load_front_matter(rep)
    if not front:
        print("  ⊘ ön madde henüz yazılmadı — BOŞ KOŞTU")
        rep.facts["frontMatterSections"] = 0
    else:
        fb = _block([t for _, t in front])
        rep.facts["frontMatter"] = fb
        rep.facts["frontMatterSections"] = len(front)
        rf9 = reg.get("frontMatter", {})
        print("  %d bölüm · %d kelime · ort %.2f kelime/cümle · FK %.2f"
              % (len(front), fb["words"], fb["avgSentenceWords"], fb["fkGrade"]))

        rep.check(rf9.get("avgWordsMin", 9.0) <= fb["avgSentenceWords"]
                  <= rf9.get("avgWordsMax", 16.0),
                  "ön madde ortalaması bantta (%.2f ∈ [%.1f, %.1f])"
                  % (fb["avgSentenceWords"], rf9.get("avgWordsMin", 9.0),
                     rf9.get("avgWordsMax", 16.0)))
        rep.check(fb["fkGrade"] <= rf9.get("fkGradeMax", 6.5),
                  "ön madde okuma seviyesi tavanın altında (%.2f ≤ %.1f)"
                  % (fb["fkGrade"], rf9.get("fkGradeMax", 6.5)))
        rep.check(fb["maxSentenceWords"] <= rf9.get("maxSentenceWords", 28),
                  "en uzun ön madde cümlesi sınırda (%d ≤ %d kelime)"
                  % (fb["maxSentenceWords"], rf9.get("maxSentenceWords", 28)))

        # ⭑ DEĞİŞMEZ, BİR KAT YUKARIDA ⭑
        # Ön madde kitabın İLK okunan metnidir. Aktivite içeriğinden zorsa
        # çocuk daha ilk sayfada durur ve durduğu yer bir aktivite bile
        # değildir. Kurucu talimatı Faz 5 § 8 bunu adıyla şart koşuyor.
        if fnr["sentences"]:
            rep.check(fb["fkGrade"] <= fnr["fkGrade"] + 0.5,
                      "ön madde, tanıttığı içerikten DAHA ZOR DEĞİL "
                      "(%.2f ≤ %.2f + 0,5)" % (fb["fkGrade"], fnr["fkGrade"]))

        # Ön madde de yasak kalıptan ve küçümseyen tondan muaf değildir.
        fblob = " ".join(t for _, t in front)
        fhits = [p for p in cfg.get("style", {}).get("forbiddenPatterns", [])
                 if p.lower().replace(" … ", " ") in fblob.lower()]
        rep.check(not fhits, "ön maddede yasak kalıp yok"
                  + ("" if not fhits else " — KALIP: %s" % fhits))
        fpat = [p for p in PATRONISING if re.search(p, fblob, re.IGNORECASE)]
        rep.check(not fpat, "ön maddede küçümseyen hitap yok"
                  + ("" if not fpat else " — TON: %s" % fpat))

        # Jenerik AI açılışları: kurucu talimatı § 7 dördünü adıyla yasaklıyor.
        openers = [r"^\s*welcome\s+to\b", r"^\s*get\s+ready\s+to\b",
                   r"^\s*embark\s+on\b", r"^\s*discover\b",
                   r"^\s*let'?s\s+(?:go|begin|start)\b"]
        bad_open = []
        for sid, text in front:
            first = text.strip().split("\n")[0]
            for o in openers:
                if re.search(o, first, re.IGNORECASE):
                    bad_open.append(sid)
                    break
        rep.check(not bad_open, "ön madde jenerik açılış kalıbı kullanmıyor"
                  + ("" if not bad_open else " — AÇILIŞ: %s" % bad_open))

    print("\n" + "=" * 74)
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · %d aktivite · ort %.2f kelime/cümle · FK %.2f"
              % (rep.checks, len(all_acts), m["avgSentenceWords"], m["fkGrade"]))
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
