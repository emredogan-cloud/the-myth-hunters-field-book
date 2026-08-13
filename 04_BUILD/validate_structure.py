#!/usr/bin/env python3
"""
DEPO, BELGE VE MANUSCRIPT KORUMASI — The Myth Hunter's Field Book
================================================================================
Beş ayrı denetim, hepsi bir kusurun GERİ GELMESİNİ engellemek için var:

  ① ZORUNLU DOSYALAR       — yol haritasının söz verdiği belgeler gerçekten var mı
  ② GÖMÜLÜ SABİT DEĞER     — yazar/yayıncı adı bir betiğe gömülmüş mü
  ③ MANUSCRIPT SIZINTISI   — kural prozası takip edilen bir dosyaya sızmış mı
  ④ SIR SIZINTISI          — .env veya anahtar benzeri dize depoya girmiş mi
  ⑤ CEVAP ANAHTARI         — çözümler public depoya sızmış mı
  ⑥ ÇOCUK KİMLİĞİ          — test eden çocuğun adı depoya girmiş mi

⑤ ve ⑥ BU PROJEYE ÖZGÜDÜR. Bir aktivite kitabının cevap anahtarı
ticari olarak hassastır: public depoda duran cevaplar ürünü değersizleştirir.
Ve çocuk testçilerinin adları HİÇBİR KOŞULDA depoya girmez — kayıtlar
yalnızca anonim kimlik (tester-01), yaş ve sonuç taşır.

② NEDEN VAR: World Myths Faz 6'da yazar adı ÜÇ betikte ayrı ayrı gömülüydü
(covers.py, epub.py, handoff.py) ve metadata.py yer tutucu basıyordu — aynı
kitabın KAPAĞI ile METADATASI farklı yazar taşıyordu. Kusur Bestiarium D17'de
de vardı. Tek doğruluk kaynağı project_config.json'dur ve bu kapı onu korur.

③ NEDEN VAR: .gitignore YOL kalıplarıyla çalışır ve yeni bir ada konan dosyayı
YAKALAMAZ. Bu yüzden ikinci bir hat gerekir: takip edilen dosyaların İÇERİĞİNE
bakan bir tarayıcı. Politikayı disipline değil MEKANİZMAYA bağlarız.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

REQUIRED_FILES = [
    "README.md",
    "PROJECT_CONTEXT.md",
    "BRIEF.md",
    "DECISIONS.md",
    "CHANGELOG.md",
    "ROADMAP_PROGRESS.md",
    "BOOK_STATS.md",
    "project_config.json",
    ".gate",
    ".gitignore",
    "THE_MYTH_HUNTERS_FIELD_BOOK_IMPLEMENTATION_ROADMAP.md",
    "00_CONTEXT/STYLE.md",
    "00_CONTEXT/SOURCING_STANDARD.md",
    "00_CONTEXT/AGE_POLICY.md",
    "00_CONTEXT/INHERITANCE_ARCHITECTURE.md",
    "00_CONTEXT/LESSONS_FROM_CODEX.md",
    "01_SOURCE/activity.schema.json",
    "04_BUILD/qa_all.sh",
    "04_BUILD/validate_spec.py",
    "04_BUILD/validate_inheritance.py",
    "05_TESTS/selftest.py",
    ".github/workflows/validate.yml",

    # ── FAZ 1 TESLİMATLARI ────────────────────────────────────────────────
    # Bir teslimat üretildikten sonra ZORUNLU olur. Aksi hâlde bir yeniden
    # düzenleme sırasında sessizce kaybolur ve kimse fark etmez.
    "00_CONTEXT/CULTURE_POLICY.md",
    "00_CONTEXT/ACTIVITY_TAXONOMY.md",
    "00_CONTEXT/PROGRESSION_ARCHITECTURE.md",
    "01_SOURCE/activity_index.json",
    "01_SOURCE/culture_index.json",
    "01_SOURCE/region_index.json",
    "01_SOURCE/inherited/IMPORT_MANIFEST.json",
    "04_BUILD/validate_research.py",
    "04_BUILD/qa_matrix.py",
    "04_BUILD/qa_age.py",
    "04_BUILD/qa_readability.py",
    "04_BUILD/page_budget.py",
    "04_BUILD/import_from_world_myths.py",
    "07_ASSETS/IMAGE_PROMPT_LIBRARY.html",
    "06_REPORTS/PHASE_1_REPORT.md",

    # ── FAZ 2 TESLİMATLARI ────────────────────────────────────────────────
    # Aynı gerekçe: üretilen bir teslimat ZORUNLU olur, yoksa bir yeniden
    # düzenlemede sessizce kaybolur ve kimse fark etmez.
    "04_BUILD/qa_solvable.py",
    "04_BUILD/qa_instruction.py",
    "04_BUILD/qa_language.py",
    "04_BUILD/qa_progression.py",
    "04_BUILD/region_difficulty.py",
    "04_BUILD/child_test_pack.py",
    "01_SOURCE/research/jaguar-condor-revalidation.json",
    "03_EDITORIAL/CHILD_TEST_PROTOCOL.md",
    "03_EDITORIAL/CHILD_TEST_LOG.md",
    "03_EDITORIAL/AGE_REVIEW_LOG.md",
    "06_REPORTS/PHASE_2_REPORT.md",
]

REQUIRED_DIRS = [
    "00_CONTEXT", "01_SOURCE", "02_MANUSCRIPT", "03_COVER", "04_BUILD",
    "05_TESTS", "06_REPORTS", "07_ASSETS", "08_OUTPUT", "09_ARCHIVE",
    "01_SOURCE/activities", "01_SOURCE/inherited", "01_SOURCE/research",
    "03_EDITORIAL", "07_ASSETS/raw", "07_ASSETS/processed",
]

# ② Gömülü sabit değer taraması ------------------------------------------------
# Bu dizeler YALNIZCA project_config.json içinde geçebilir.
SINGLE_SOURCE_VALUES = ["Emre Doğan", "Vâliçe Press"]
SCAN_CODE_EXT = (".py", ".sh", ".yml", ".yaml")
# Bu dosyalar muaf: config'in kendisi ve onu ANLATAN belgeler.
EMBED_SCAN_SKIP = {
    "project_config.json",
    "04_BUILD/validate_structure.py",   # tarayıcının kendisi dizeleri taşır
}

# ③ Manuscript sızıntısı -------------------------------------------------------
# Kural prozasının parmak izleri. Bir belge bunlardan BİRDEN ÇOK taşıyorsa
# ve manuscript dizininde değilse, proza sızmış olabilir.
LEAK_MARKERS = [
    r"\bYour mission:\s",
    r"\bWrite your answer\b",
    r"\bDraw the\b",
    r"\bSolve the\b",
    r"\bField note:\s",
]
LEAK_MIN_HITS = 2
LEAK_SCAN_EXT = (".md", ".json", ".txt", ".html")
# Muafiyet = yalnızca bu dosyalar kural dilini ÖRNEK olarak taşıyabilir.
#
# ⚠ HER MUAFİYET selftest § ④ TARAFINDAN İKİ KEZ DENETLENİR:
#   (a) dosya gerçekten var mı        → yoksa ÖLÜ MUAFİYET
#   (b) muafiyet olmasaydı yakalanır mıydı → hayırsa GEREKSİZ MUAFİYET
#
# Bu yüzden listeye "ihtimale karşı" dosya eklenmez. Bir dosya ancak kural
# dilini GERÇEKTEN taşıdığı için buraya girer.
# (World Myths K14 · Bestiarium D28: ölü kural sessizce yanlış güven verir.)
#
# ⚠ `01_SOURCE/activity.schema.json` BURADAN ÇIKARILDI (Faz 1).
# Şema v2 sayfa dili örneklerini artık taşımıyor — kalıplar STYLE.md § 2'ye
# taşındı ve şema onlara ATIF yapıyor. Muafiyet o anda ÖLDÜ ve
# `selftest § ④` onu ilk koşuda yakaladı. Kural işledi: listeye "ihtimale
# karşı" dosya konmaz, gereksiz kalan çıkarılır.
LEAK_SCAN_SKIP = {
    "00_CONTEXT/STYLE.md",
}

# ⑤ CEVAP ANAHTARI KORUMASI — bu projeye özgü -----------------------------
# Bir aktivite kitabının cevapları ÜRÜNÜN KENDİSİDİR. Public depoda duran
# cevap anahtarı ürünü değersizleştirir. Bu tarama, cevap taşıyan alan
# adlarının takip edilen dosyalara sızmasını engeller.
ANSWER_MARKERS = [
    r'"answer"\s*:',
    r'"answerKey"\s*:',
    r'"correctAnswer"\s*:',
    r'"solution"\s*:',
    r"\bANSWER KEY\b",
]
ANSWER_MIN_HITS = 1
# Şema DOSYASI alan adlarını TANIMLAR ama DEĞER taşımaz — muaf.
ANSWER_SCAN_SKIP = {
    "01_SOURCE/activity.schema.json",
    "04_BUILD/validate_structure.py",
}

# ⑥ ÇOCUK KİMLİĞİ — anonim kimlik dışında hiçbir şey depoya girmez.
# Kabul edilen biçim: tester-01, tester-02 …
CHILD_ID_OK = re.compile(r"^tester-\d{2}$")

# ④ Sır taraması ---------------------------------------------------------------
SECRET_PATTERNS = [
    (r"sk-[A-Za-z0-9]{20,}", "OpenAI benzeri anahtar"),
    (r"gh[pousr]_[A-Za-z0-9]{30,}", "GitHub token"),
    (r"AKIA[0-9A-Z]{16}", "AWS anahtar kimliği"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "özel anahtar"),
]

FAKE_ISBN = re.compile(r"\b97[89][- ]?\d{1,5}[- ]?\d{1,7}[- ]?\d{1,7}[- ]?\d\b")


class Report:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks = 0

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


def tracked_files() -> list[str]:
    """git ls-files — TAKİP EDİLEN dosyalar. Sızıntı denetimi yalnızca
    bunlara bakar: takip edilmeyen dosya zaten public değildir."""
    try:
        out = subprocess.run(["git", "ls-files"], cwd=ROOT,
                             capture_output=True, text=True, timeout=30)
        if out.returncode != 0:
            return []
        return [p for p in out.stdout.splitlines() if p.strip()]
    except (OSError, subprocess.SubprocessError):
        return []


def check_files(rep: Report) -> None:
    print("\n── zorunlu dosya ve dizinler ──")
    for rel in REQUIRED_DIRS:
        rep.check(os.path.isdir(os.path.join(ROOT, rel)), "dizin: %s" % rel)
    for rel in REQUIRED_FILES:
        rep.check(os.path.isfile(os.path.join(ROOT, rel)), "dosya: %s" % rel)


def check_gate_file(rep: Report) -> None:
    print("\n── .gate ──")
    path = os.path.join(ROOT, ".gate")
    if not os.path.exists(path):
        rep.check(False, ".gate dosyası var")
        return
    with open(path, encoding="utf-8") as fh:
        lvl = fh.read().strip()
    rep.check(lvl in ("phase0", "phase1", "phase2", "phase3", "phase4",
                      "phase5", "release"),
              ".gate geçerli bir seviye taşıyor: '%s'" % lvl)


def check_embedded(rep: Report, files: list[str]) -> None:
    print("\n── gömülü sabit değer (tek doğruluk kaynağı) ──")
    hits: list[str] = []
    for rel in files:
        if rel in EMBED_SCAN_SKIP or not rel.endswith(SCAN_CODE_EXT):
            continue
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        try:
            with open(p, encoding="utf-8") as fh:
                body = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        for val in SINGLE_SOURCE_VALUES:
            if val in body:
                hits.append("%s → '%s'" % (rel, val))
    rep.check(not hits,
              "kurucu değerleri yalnızca project_config.json'da" +
              ("" if not hits else " — GÖMÜLÜ: %s" % hits[:5]))


def check_manuscript_leak(rep: Report, files: list[str]) -> None:
    print("\n── manuscript sızıntısı ──")
    leaked: list[str] = []
    for rel in files:
        if rel in LEAK_SCAN_SKIP or not rel.endswith(LEAK_SCAN_EXT):
            continue
        if rel.startswith("02_MANUSCRIPT/"):
            # Manuscript dizinindeki TAKİP EDİLEN her dosya zaten ihlaldir.
            if os.path.basename(rel) not in (".gitkeep", "README.md"):
                leaked.append("%s (manuscript dizini takip ediliyor)" % rel)
            continue
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        try:
            with open(p, encoding="utf-8") as fh:
                body = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        hits = sum(1 for pat in LEAK_MARKERS if re.search(pat, body))
        if hits >= LEAK_MIN_HITS:
            leaked.append("%s (%d kural işareti)" % (rel, hits))
    rep.check(not leaked,
              "kural prozası depoya sızmamış" +
              ("" if not leaked else " — SIZINTI: %s" % leaked[:5]))


def check_secrets(rep: Report, files: list[str]) -> None:
    print("\n── sır ve sahte ISBN taraması ──")
    rep.check(".env" not in files, ".env takip edilmiyor")

    found: list[str] = []
    for rel in files:
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p) or os.path.getsize(p) > 2_000_000:
            continue
        try:
            with open(p, encoding="utf-8") as fh:
                body = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        for pat, name in SECRET_PATTERNS:
            if re.search(pat, body):
                found.append("%s → %s" % (rel, name))
    rep.check(not found,
              "sır benzeri dize yok" + ("" if not found else " — %s" % found[:3]))

    # Sahte ISBN: kurucu kararı KDP ücretsiz ISBN. Uydurulmuş numara YASAK.
    cfgp = os.path.join(ROOT, "project_config.json")
    strategy = "kdp-free"
    if os.path.exists(cfgp):
        try:
            with open(cfgp, encoding="utf-8") as fh:
                strategy = json.load(fh).get("founder", {}).get(
                    "isbn", {}).get("strategy", "kdp-free")
        except (OSError, json.JSONDecodeError):
            pass
    if strategy == "kdp-free":
        isbn_hits: list[str] = []
        for rel in files:
            if not rel.endswith((".md", ".json", ".py")):
                continue
            if rel in ("04_BUILD/validate_structure.py",):
                continue
            p = os.path.join(ROOT, rel)
            if not os.path.isfile(p):
                continue
            try:
                with open(p, encoding="utf-8") as fh:
                    body = fh.read()
            except (OSError, UnicodeDecodeError):
                continue
            if FAKE_ISBN.search(body):
                isbn_hits.append(rel)
        rep.check(not isbn_hits,
                  "uydurulmuş ISBN yok (strateji: kdp-free)" +
                  ("" if not isbn_hits else " — %s" % isbn_hits[:3]))


def check_answer_leak(rep: Report, files: list[str]) -> None:
    """⑤ Cevap anahtarı public depoya sızmış mı.

    `.gitignore` cevap dosyalarını YOL ile dışlar; bu ikinci hat İÇERİĞE
    bakar. Bir cevap alanı yeni bir ada konan dosyaya taşınırsa yol kalıbı
    onu yakalamaz — bu tarama yakalar."""
    print("\n── cevap anahtarı koruması ──")
    leaked: list[str] = []
    for rel in files:
        if rel in ANSWER_SCAN_SKIP or not rel.endswith((".json", ".md", ".txt")):
            continue
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        try:
            with open(p, encoding="utf-8") as fh:
                body = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        hits = sum(1 for pat in ANSWER_MARKERS if re.search(pat, body))
        if hits >= ANSWER_MIN_HITS:
            leaked.append("%s (%d cevap işareti)" % (rel, hits))
    rep.check(not leaked, "cevap anahtarı depoya sızmamış" +
              ("" if not leaked else " — SIZINTI: %s" % leaked[:5]))


def check_child_privacy(rep: Report, files: list[str]) -> None:
    """⑥ Çocuk testçi kimlikleri anonim mi.

    Çocuk testçilerinin adları HİÇBİR KOŞULDA depoya girmez. Test kayıtları
    yalnızca `tester-01` biçiminde anonim kimlik, yaş ve sonuç taşır."""
    print("\n── çocuk testçi mahremiyeti ──")
    bad: list[str] = []
    for rel in files:
        if not rel.endswith((".md", ".json")):
            continue
        if "CHILD_TEST" not in rel.upper() and "child_test" not in rel:
            continue
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8") as fh:
            body = fh.read()
        for m in re.finditer(r'"tester"\s*:\s*"([^"]*)"', body):
            if not CHILD_ID_OK.match(m.group(1)):
                bad.append("%s → '%s'" % (rel, m.group(1)))
    rep.check(not bad, "çocuk testçi kimlikleri anonim" +
              ("" if not bad else " — KİMLİK AÇIK: %s" % bad[:5]))


def check_doc_links(rep: Report) -> None:
    """Belge bağları — iki ayrı denetim.

    ① KIRIK BAĞ      — hedef dosya var mı
    ② DEPO SINIRI    — bağ deponun DIŞINA çıkıyor mu

    ② NEDEN AYRI BİR DENETİM: bir bağ yerel makinede çözülüp CI'da
    kırılabilir. `../PAZAR-RAPORU.html` kurucunun çalışma dizininde
    VARDIR ama depoyu klonlayan kimsede YOKTUR — yani yerelde yeşil,
    CI'da kırmızı. Bu tam olarak bootstrap sırasında yaşandı.

    Depo sınırı denetimi bu ayrışmayı ortadan kaldırır: dosyanın var olup
    olmadığına bakmadan, deponun dışına çıkan her bağ REDDEDİLİR. Böylece
    yerel sonuç ile CI sonucu AYNI OLMAK ZORUNDADIR.

    Kural: depo dışındaki bir kaynağa **künyeyle** atıf yapılır, bağ verilmez.
    """
    print("\n── belge bağları ──")
    broken: list[str] = []
    escaped: list[str] = []
    root_abs = os.path.realpath(ROOT)

    scan = list(REQUIRED_FILES)
    for extra in ("02_MANUSCRIPT/README.md", "01_SOURCE/solutions/README.md"):
        if os.path.isfile(os.path.join(ROOT, extra)):
            scan.append(extra)

    for rel in scan:
        if not rel.endswith(".md"):
            continue
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8") as fh:
            body = fh.read()
        for m in re.finditer(r"\]\((?!https?://|#|mailto:)([^)\s]+)\)", body):
            target = m.group(1).split("#")[0]
            if not target:
                continue
            base = os.path.dirname(p)
            resolved = os.path.realpath(os.path.join(base, target))
            # ② depo sınırı — dosyanın varlığından BAĞIMSIZ
            if not (resolved == root_abs or resolved.startswith(root_abs + os.sep)):
                escaped.append("%s → %s" % (rel, target))
                continue
            # ① kırık bağ
            if not os.path.exists(resolved):
                broken.append("%s → %s" % (rel, target))

    rep.check(not escaped,
              "hiçbir bağ deponun dışına çıkmıyor" +
              ("" if not escaped else
               " — SINIR İHLALİ (künyeye çevirin): %s" % escaped[:5]))
    rep.check(not broken,
              "belge içi bağlar çözülüyor" +
              ("" if not broken else " — KIRIK: %s" % broken[:5]))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    print("=" * 74)
    print("  DEPO, BELGE VE MANUSCRIPT KORUMASI")
    print("=" * 74)

    rep = Report(args.verbose)
    files = tracked_files()
    if not files:
        rep.warn("git takip listesi boş — depo henüz init edilmemiş olabilir; "
                 "sızıntı denetimleri boş koşuyor")

    check_files(rep)
    check_gate_file(rep)
    check_embedded(rep, files)
    check_manuscript_leak(rep, files)
    check_secrets(rep, files)
    check_answer_leak(rep, files)
    check_child_privacy(rep, files)
    check_doc_links(rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil" % rep.checks)
        status = "pass"
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": status, "checks": rep.checks,
                       "errors": rep.errors, "warnings": rep.warnings,
                       "trackedFiles": len(files)},
                      fh, ensure_ascii=False, indent=2)

    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
