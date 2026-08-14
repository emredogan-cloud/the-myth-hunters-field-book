#!/usr/bin/env bash
# =============================================================================
# THE MYTH HUNTER'S FIELD BOOK — BÜTÜN KALİTE KAPILARI
# =============================================================================
# CI'ın çalıştırdığı komutların BİREBİR AYNISI. Push etmeden önce yerelde
# koşturun; yeşilse CI de yeşil olur.
#
#   ./04_BUILD/qa_all.sh              mevcut kapı seviyesiyle (.gate)
#   ./04_BUILD/qa_all.sh phase1       kapıyı yükselterek dene
#   ./04_BUILD/qa_all.sh --fix        üretilen belgeleri tazeleyerek
#
# Hafif kapıların hiçbiri venv gerektirmez; hepsi Python standart
# kütüphanesiyle koşar. Görsel/dizgi işleri Pillow ve reportlab ister ve
# yoksa ATLANIR (çıkış 2) — bu bir kalite düşüşü DEĞİLDİR.
# =============================================================================
set -uo pipefail

BUILD="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$BUILD")"
TESTS="$ROOT/05_TESTS"
cd "$ROOT"

GATE=""
FIX=0
for arg in "$@"; do
  case "$arg" in
    --fix) FIX=1 ;;
    phase0|phase1|phase2|phase3|phase4|phase5|release) GATE="$arg" ;;
    *) echo "bilinmeyen argüman: $arg" >&2; exit 2 ;;
  esac
done

# Kapı seviyesi .gate dosyasındadır; yalnızca AÇIKÇA verilirse o kazanır.
# (Bestiarium'da --fix kapıyı draft'a düşürüyordu — yani belgeleri tazeleyen
# koşu açılmış kapıları HİÇ denetlemiyordu.)
if [ -z "$GATE" ]; then
  GATE="$( [ -f .gate ] && tr -d '[:space:]' < .gate || echo phase0 )"
fi

PY="${PYTHON:-python3}"
VENV_PY="$PY"
[ -x "$BUILD/.venv/bin/python" ] && VENV_PY="$BUILD/.venv/bin/python"

FAILED=()
SKIPPED=()

run () {
  local name="$1"; shift
  echo
  echo "──────────────────────────────────────────────────────────────────────"
  echo "▸ $name"
  echo "──────────────────────────────────────────────────────────────────────"
  if "$@"; then return 0; else FAILED+=("$name"); return 1; fi
}

run_optional () {
  local name="$1"; shift
  echo
  echo "──────────────────────────────────────────────────────────────────────"
  echo "▸ $name"
  echo "──────────────────────────────────────────────────────────────────────"
  "$@"
  case $? in
    0) ;;
    2) echo "ATLANDI: bağımlılık yok — pip install -r 04_BUILD/requirements.txt"
       SKIPPED+=("$name") ;;
    *) FAILED+=("$name") ;;
  esac
}

echo "════════════════════════════════════════════════════════════════════════"
echo "  THE MYTH HUNTER'S FIELD BOOK · KALİTE KAPILARI · kapı: $GATE"
echo "════════════════════════════════════════════════════════════════════════"

if [ "$FIX" = "1" ]; then
  echo "▸ üretilen belgeler tazeleniyor…"
  [ -f 04_BUILD/update_docs.py ] && $PY 04_BUILD/update_docs.py >/dev/null || true
fi

# ── YAPILANDIRMA VE VERİ ────────────────────────────────────────────────────
run "veri bütünlüğü ve kapsam"  $PY 04_BUILD/validate_spec.py --gate "$GATE" \
                                   --json 06_REPORTS/spec-validation.json
run "depo ve belge bütünlüğü"   $PY 04_BUILD/validate_structure.py \
                                   --json 06_REPORTS/structure.json

# DEVRALMA KİLİDİ — bu projenin bel kemiği. Doğrulanmamış devralmaya
# dayanan bir aktivite LOCKED olamaz.
#
# --cross-check: kaynak depo BU MAKİNEDE varsa sha256'ları karşılaştırır ve
# sürüklenmeyi bildirir; yoksa ATLAR ve kırmızı yanmaz (karar K6). Bayrağı
# burada vermek, sürüklenmeyi kurucu makinesinde her koşuda görünür kılar.
run "DEVRALMA BÜTÜNLÜĞÜ"        $PY 04_BUILD/validate_inheritance.py --cross-check \
                                   --json 06_REPORTS/inheritance.json

# ── KAPILARIN KENDİ TESTİ — en önemlisi ────────────────────────────────────
run "KAPILARIN KENDİ TESTİ"     $PY 05_TESTS/selftest.py

# ── FAZ 1'DE DOĞACAK KAPILAR ───────────────────────────────────────────────
# Bu betikler henüz yok. Var olduklarında bu satırlar canlanır.
# Bir kapının VARLIĞI yetmez, KOŞMASI gerekir (World Myths K18).
[ -f 04_BUILD/validate_research.py ] && \
  run "araştırma kayıtları"     $PY 04_BUILD/validate_research.py \
                                   --json 06_REPORTS/research.json
[ -f 04_BUILD/qa_matrix.py ] && \
  run "bölge × tip matrisi"     $PY 04_BUILD/qa_matrix.py \
                                   --json 06_REPORTS/qa-matrix.json

# ── FAZ 2'DE DOĞACAK KAPILAR ───────────────────────────────────────────────
[ -f 04_BUILD/qa_age.py ] && \
  run "YAŞ POLİTİKASI"          $PY 04_BUILD/qa_age.py \
                                   --json 06_REPORTS/qa-age.json
[ -f 04_BUILD/qa_solvable.py ] && \
  run "TEK CEVAPLILIK"          $PY 04_BUILD/qa_solvable.py \
                                   --json 06_REPORTS/qa-solvable.json
[ -f 04_BUILD/qa_instruction.py ] && \
  run "talimat netliği"         $PY 04_BUILD/qa_instruction.py \
                                   --json 06_REPORTS/qa-instruction.json
[ -f 04_BUILD/qa_readability.py ] && \
  run "okunabilirlik (8–12)"    $PY 04_BUILD/qa_readability.py \
                                   --json 06_REPORTS/qa-readability.json
# DİL AYRIMI — ticari dil İNGİLİZCE, Türkçe yalnızca geçici test dili (K21).
[ -f 04_BUILD/qa_language.py ] && \
  run "DİL AYRIMI"              $PY 04_BUILD/qa_language.py \
                                   --json 06_REPORTS/qa-language.json
[ -f 04_BUILD/qa_length.py ] && \
  run "kelime bandı"            $PY 04_BUILD/qa_length.py \
                                   --json 06_REPORTS/qa-length.json
[ -f 04_BUILD/qa_voice.py ] && \
  run "ses ve yasak kalıp"      $PY 04_BUILD/qa_voice.py \
                                   --json 06_REPORTS/qa-voice.json
[ -f 04_BUILD/qa_echo.py ] && \
  run "tekrar taraması"         $PY 04_BUILD/qa_echo.py \
                                   --json 06_REPORTS/qa-echo.json
[ -f 04_BUILD/qa_design.py ] && \
  run "TASARIM DİZGESİ"          $PY 04_BUILD/qa_design.py \
                                   --json 06_REPORTS/qa-design.json
[ -f 04_BUILD/qa_drift.py ] && \
  run "üslup sürüklenmesi"      $PY 04_BUILD/qa_drift.py \
                                   --json 06_REPORTS/qa-drift.json

# ── FAZ 3+ KAPILARI ────────────────────────────────────────────────────────
[ -f 04_BUILD/qa_crossref.py ] && \
  run "çapraz referans"         $PY 04_BUILD/qa_crossref.py \
                                   --json 06_REPORTS/qa-crossref.json
[ -f 04_BUILD/qa_progression.py ] && \
  run "mühür ve ilerleme"       $PY 04_BUILD/qa_progression.py \
                                   --json 06_REPORTS/qa-progression.json
[ -f 04_BUILD/qa_answerkey.py ] && \
  run "cevap anahtarı"          $PY 04_BUILD/qa_answerkey.py \
                                   --json 06_REPORTS/qa-answerkey.json

# ── FAZ 5 · GÖRSEL VARLIK HATTI ────────────────────────────────────────────
# ⚠ ENVANTER ÖLÇÜMDEN ÖNCE KOŞAR (yol haritası Faz 5 § 8): yanlış aktiviteye
# bağlanmış kusursuz bir görsel, aktiviteyi ÇÖZÜLEMEZ yapar. Bu yüzden
# envanter tazeliği bir görsel kapısı DEĞİL, bir veri kapısıdır.
[ -f 04_BUILD/asset_manifest.py ] && \
  run "varlık envanteri güncel"  $PY 04_BUILD/asset_manifest.py --check
[ -f 04_BUILD/qa_assets.py ] && \
  run "GÖRSEL VARLIKLAR"         $PY 04_BUILD/qa_assets.py \
                                   --json 06_REPORTS/qa-assets.json

# ── ÜRETİM MODELİ ──────────────────────────────────────────────────────────
[ -f 04_BUILD/page_budget.py ] && \
  run "sayfa bütçesi"           $PY 04_BUILD/page_budget.py \
                                   --json 06_REPORTS/page-budget.json
[ -f 04_BUILD/editions.py ] && \
  run "sürüm ve telif modeli"   $PY 04_BUILD/editions.py \
                                   --json 06_REPORTS/editions.json

# ── GÖRSEL VE ÜRETİM HATTI (Pillow / reportlab ister) ──────────────────────
[ -f 04_BUILD/asset_inventory.py ] && \
  run_optional "ham varlık envanteri"   $VENV_PY 04_BUILD/asset_inventory.py --check
[ -f 04_BUILD/interior.py ] && \
  run_optional "iç blok güncel"         $VENV_PY 04_BUILD/interior.py --check
[ -f 04_BUILD/epub.py ] && \
  run_optional "Kindle EPUB güncel"     $VENV_PY 04_BUILD/epub.py --check
[ -f 04_BUILD/covers.py ] && \
  run_optional "kapak üretimi güncel"   $VENV_PY 04_BUILD/covers.py --check
[ -f 04_BUILD/metadata.py ] && \
  run "KDP metadata paketi"     $PY 04_BUILD/metadata.py --check

# ── ÜRETİLEN BELGELER BAYAT MI ─────────────────────────────────────────────
# Görsel prompt kütüphanesi de ÜRETİLİR (K17): elle yazılan bir varlık
# listesi, bir sayfa değişince sessizce yalan söylemeye başlar.
[ -f 04_BUILD/image_prompts.py ] && \
  run "görsel kütüphanesi güncel" $PY 04_BUILD/image_prompts.py --check
[ -f 04_BUILD/update_docs.py ] && \
  run "üretilen belgeler güncel" $PY 04_BUILD/update_docs.py --check

# ── ÖZET ───────────────────────────────────────────────────────────────────
echo
echo "════════════════════════════════════════════════════════════════════════"
if [ ${#SKIPPED[@]} -gt 0 ]; then
  echo "  ⊘ ${#SKIPPED[@]} kapı atlandı (bağımlılık yok):"
  for s in "${SKIPPED[@]}"; do echo "     · $s"; done
fi
if [ ${#FAILED[@]} -eq 0 ]; then
  echo "  ✅ BÜTÜN KAPILAR YEŞİL · kapı seviyesi: $GATE"
  echo "════════════════════════════════════════════════════════════════════════"
  exit 0
fi
echo "  ⛔ ${#FAILED[@]} KAPI KIRMIZI"
for f in "${FAILED[@]}"; do echo "     · $f"; done
echo "════════════════════════════════════════════════════════════════════════"
echo
echo "  Kalite düştü. Düzeltilmeden ilerleme yok."
exit 1
