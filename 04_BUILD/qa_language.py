#!/usr/bin/env python3
"""
DİL AYRIMI KAPISI — The Myth Hunter's Field Book
================================================================================
    TİCARİ DİL İNGİLİZCEDİR. TÜRKÇE YALNIZCA GEÇİCİ BİR TEST DİLİDİR.

Bu kitap İngilizce satılır. Ama kurucu Türkçe okur, proje belgeleri
Türkçedir, ve gerçek çocuk testçiler bulunursa tester-facing materyal
GEÇİCİ olarak Türkçe olabilir (karar K21).

Üç dil, üç ayrı yer, ve aralarında bir duvar:

    ticari   → İNGİLİZCE  · 02_MANUSCRIPT · 08_OUTPUT · kapak · metadata
    belge    → TÜRKÇE     · 00_CONTEXT · *.md · $comment alanları
    test     → TÜRKÇE     · 03_EDITORIAL/child_tests_raw/ · GEÇİCİ

Duvar bir DİSİPLİN değil bir MEKANİZMA olmalıdır, çünkü disiplin unutulur
ve bu kusurun bedeli çok yüksektir: Türkçe bir talimatın nihai KDP
paketine sızması, kitabın İngilizce rafta reddedilmesi demektir.

Beş denetim:

  ① TİCARİ KATMAN     — çocuk-görünür her alan İngilizce mi
  ② TÜRKÇE İMZASI     — Türkçeye özgü harfler ve ekler ticari alanda var mı
  ③ KARIŞIK CÜMLE     — tek bir alan iki dili birden taşıyor mu
  ④ TEST İZOLASYONU   — Türkçe test materyali ticari dizinlere sızmış mı
  ⑤ TESTÇİ KAPISI     — testçi yokken Türkçe test materyali üretilmiş mi

② NASIL ÇALIŞIR: Türkçe altı harf taşır ki İngilizcede HİÇ bulunmaz
(ı ğ ş İ Ğ Ş) — ve 'ç ö ü' gibi paylaşılan harfler ölçüte KATILMAZ,
çünkü İngilizce metinde de meşru olarak geçebilirler (façade, coöperate)
ve daha önemlisi bu kitap KÜLTÜREL ADLAR taşır: Tenochtitlán, Huarochirí,
Tonacatépetl. Bir diakritik avı bu adları yanlışlıkla suçlardı.

⑤ NEDEN VAR — VE BU KAPININ EN ÖNEMLİ DENETİMİDİR:

Türkçe test materyali ancak GERÇEK Türkçe konuşan çocuk testçiler
varsa üretilebilir. Testçi yokken Türkçe bir test sayfası dosyada
duruyorsa, o sayfa bir testin YAPILDIĞINI ima eder. Yapılmadı.

    Sahte test materyali, sahte test kaydının bir adım öncesidir.

Bu yüzden kapı `founder.childTesters.founderConfirmed` alanına bakar:
false iken test dizininde materyal bulursa KIRMIZI yanar.

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

# ② TÜRKÇEYE ÖZGÜ HARFLER — İngilizcede hiç bulunmazlar.
#
# ⚠ 'ç', 'ö', 'ü' BİLEREK DIŞARIDA BIRAKILDI. Bu kitap kültürel adlar
# taşır (Tenochtitlán · Huarochirí · Tonacatépetl · Kauaʻi) ve genel bir
# diakritik taraması onları Türkçe sanardı. Kapı yanlış yönde
# arızalanmamalı: kültürel imlâyı korumak bu projenin bir KURALIDIR
# (validate_research § ⑧).
TURKISH_LETTERS = re.compile(r"[ıİğĞşŞ]")

# Türkçeye özgü, İngilizcede karşılığı olmayan yüksek frekanslı sözcükler.
# Harf taraması bir adı yanlışlıkla yakalarsa bu ikinci hat ayırt eder.
TURKISH_WORDS = re.compile(
    r"\b(?:ve|bir|bu|için|ile|olarak|değil|çocuk|sayfa|cevap|kutu|"
    r"yazı|göre|olan|daha|kadar|sonra|önce|hangi|nasıl|neden|"
    r"yaz|çiz|bul|eşleştir|sırala|oku|işaretle)\b", re.IGNORECASE)


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


def turkishness(text: str) -> tuple[int, int]:
    """(özgü harf sayısı, özgü sözcük sayısı)"""
    if not text:
        return 0, 0
    return (len(TURKISH_LETTERS.findall(text)),
            len(TURKISH_WORDS.findall(text)))


def walk_commercial(doc, fields, path="", out=None):
    """Ticari alanları BULUR. `$` ile başlayan anahtarlar ve `…Note` biten
    editorial alanlar ATLANIR: onlar sayfaya çıkmaz."""
    if out is None:
        out = []
    if isinstance(doc, dict):
        for k, v in doc.items():
            if k.startswith("$") or k in ("answerNote", "editorialNote",
                                          "batchNote", "note", "comment"):
                continue
            walk_commercial(v, fields, "%s.%s" % (path, k), out)
    elif isinstance(doc, list):
        for i, v in enumerate(doc):
            walk_commercial(v, fields, "%s[%d]" % (path, i), out)
    elif isinstance(doc, str):
        key = path.rsplit(".", 1)[-1].split("[")[0]
        if key in fields:
            out.append((path, doc))
    return out


def check_commercial_layer(cfg, rep):
    print("\n── ① ticari katman · ② Türkçe imzası · ③ karışık cümle ──")
    lang = cfg.get("language", {})
    fields = set(lang.get("commercialFields", []))
    layers = lang.get("commercialLayers", [])
    rep.facts["commercialFields"] = len(fields)

    scanned = 0
    hits = []
    for rel in layers:
        path = os.path.join(ROOT, rel)
        if os.path.isdir(path):
            continue
        if not os.path.isfile(path):
            continue
        doc = load(path, rep, required=False)
        if doc is None:
            continue
        for where, text in walk_commercial(doc, fields):
            scanned += 1
            letters, words = turkishness(text)
            # Tek bir özgü harf bir kültürel addan gelebilir; SÖZCÜK gelmez.
            if words >= 1 or letters >= 2:
                hits.append("%s%s → '%s…' (harf=%d sözcük=%d)"
                            % (rel, where, text[:40], letters, words))
    rep.facts["commercialStringsScanned"] = scanned

    if scanned == 0:
        print("  ⊘ ticari katman depoda yok — BOŞ KOŞTU")
        rep.check(True, "ticari katman taranabilir durumda")
        return

    rep.check(not hits,
              "ticari katmanın %d alanının hepsi İngilizce" % scanned
              + ("" if not hits else " — TÜRKÇE SIZINTISI: %s" % hits[:5]))


def check_test_isolation(cfg, rep):
    print("\n── ④ test materyali izolasyonu ──")
    lang = cfg.get("language", {})
    test_path = lang.get("testOnlyPath", "03_EDITORIAL/child_tests_raw/")
    rep.facts["testOnlyPath"] = test_path

    # Test materyali YALNIZCA kendi dizininde durabilir. Başka bir yerde
    # 'TEST-ONLY' etiketi taşıyan bir dosya, duvarın delindiği anlamına gelir.
    stray = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", ".venv")]
        for fn in files:
            if not fn.endswith((".md", ".json", ".txt", ".html")):
                continue
            full = os.path.join(base, fn)
            rel = os.path.relpath(full, ROOT)
            if rel.replace(os.sep, "/").startswith(test_path.rstrip("/")):
                continue
            try:
                with open(full, encoding="utf-8") as fh:
                    body = fh.read(200000)
            except (OSError, UnicodeDecodeError):
                continue
            if re.search(r"TEST-ONLY\s*/\s*(?:TURKISH|TÜRKÇE)\s*PILOT", body, re.I):
                stray.append(rel)
    rep.check(not stray,
              "TEST-ONLY etiketli materyal yalnızca test dizininde"
              + ("" if not stray else " — DIŞARIDA: %s" % stray[:5]))


def check_tester_gate(cfg, rep):
    print("\n── ⑤ testçi kapısı ──")
    ct = cfg.get("founder", {}).get("childTesters", {})
    confirmed = bool(ct.get("founderConfirmed"))
    available = ct.get("availableTesters", 0)
    rep.facts["childTestersConfirmed"] = confirmed
    rep.facts["childTestersAvailable"] = available

    test_dir = os.path.join(ROOT, cfg.get("language", {}).get(
        "testOnlyPath", "03_EDITORIAL/child_tests_raw/"))
    present = []
    if os.path.isdir(test_dir):
        present = [f for f in os.listdir(test_dir)
                   if not f.startswith(".") and f != "README.md"]
    rep.facts["testMaterialFiles"] = len(present)

    # Testçi yoksa test materyali de olamaz. Bir sayfa varsa, bir test
    # YAPILDIĞINI ima eder — ve yapılmadı.
    rep.check(confirmed or not present,
              "testçi onayı yokken test materyali üretilmemiş "
              "(onay=%s · testçi=%d · dosya=%d)"
              % (confirmed, available, len(present))
              + ("" if not present or confirmed
                 else " — SAHTE MATERYAL: %s" % present[:5]))

    # Ve durum dürüst raporlanmalı: testçi yokken 'passed' yazılamaz.
    ext = ct.get("externalValidation")
    rep.check(not (ext == "passed" and available < ct.get("minTesters", 2)),
              "dış doğrulama durumu testçi sayısıyla tutarlı (%s · %d testçi)"
              % (ext, available))

    if not confirmed:
        rep.warn("çocuk testçi YOK — dış doğrulama BEKLİYOR, PASS DEĞİL "
                 "(karar A7). Bu bir kusur değil, kabul edilmiş bir bloktur.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    print("=" * 74)
    print("  DİL AYRIMI — ticari: İNGİLİZCE · test: geçici TÜRKÇE")
    print("=" * 74)

    rep = Report(args.verbose)
    cfg = load(CONFIG, rep)
    if cfg is None:
        return 1

    lang = cfg.get("language", {})
    if not lang:
        rep.check(False, "project_config.json § language bloğu yok")
    else:
        rep.check(lang.get("commercial") == "en",
                  "ticari dil İngilizce olarak tanımlı (%s)" % lang.get("commercial"))
        rep.check("tr" in (lang.get("testOnly") or []),
                  "Türkçe yalnızca test dili olarak tanımlı")
        rep.check(lang.get("commercial") not in (lang.get("testOnly") or []),
                  "ticari dil ile test dili AYRI")

    check_commercial_layer(cfg, rep)
    check_test_isolation(cfg, rep)
    check_tester_gate(cfg, rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · %d ticari dize tarandı"
              % (rep.checks, rep.facts.get("commercialStringsScanned", 0)))
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
