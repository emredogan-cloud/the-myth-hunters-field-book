# CHANGELOG — The Myth Hunter's Field Book

Bu dosya **ne zaman ne değişti ve neden** sorusunu yanıtlar.
Her faz kendi girdisini ekler. Format: ters kronolojik.

---

## [0.0.1] — 2026-08-12 · Bootstrap

Proje altyapısı kuruldu. **Hiçbir kitap içeriği üretilmedi.**

### Eklendi

- **Dizin mimarisi** — 24 dizin, `00_CONTEXT` … `09_ARCHIVE` şemasına uygun,
  bu projeye özgü eklerle: `01_SOURCE/inherited`, `01_SOURCE/activities`,
  `03_EDITORIAL`
- **`project_config.json`** — makine okunur tek doğruluk kaynağı. Pazar
  raporunun sayıları `scope.locked: false` ile **hipotez** olarak işaretlendi
- **`THE_MYTH_HUNTERS_FIELD_BOOK_IMPLEMENTATION_ROADMAP.md`** — altı faz,
  her fazda 19 alan: amaç, kapsam, teslimatlar, yazım hedefi, kelime/sayfa
  hedefi, araştırma, test altyapısı, QA kapıları, DoD, PASS, FAIL, ajan
  notları, kurucu bağımlılıkları, git kilometre taşı, CI, çıktılar, riskler,
  faz devri
- **`00_CONTEXT/INHERITANCE_ARCHITECTURE.md`** — bu projenin en özgün yapısal
  parçası: World Myths'ten devralma bir *kopyalama + köken kaydı*dır, canlı
  bağımlılık değil. Üç durum ve tek kural: `inherited-provisional` LOCKED olamaz
- **`00_CONTEXT/AGE_POLICY.md`** — World Myths'ten **kopyalanmadı, yeniden
  yazıldı**: orada risk okunan şiddet, burada **yapılan görev**. Altı yasak çerçeve
- **`00_CONTEXT/SOURCING_STANDARD.md`** — doğrulama eşiği **kullanıma göre**
  değişir: anlatı arka planı 1 kaynak, bir aktivitenin **cevabını** üreten
  iddia ≥2 bağımsız kaynak veya `inherited-verified`
- **`00_CONTEXT/STYLE.md`** v1.0 — sayfa dili sabit kalıpları, küçümsemeyen
  ses, "bulmaca içerikten türer" kuralı
- **`00_CONTEXT/LESSONS_FROM_CODEX.md`** — iki referans projeden taşınan
  yedi mekanizma ve altı ders; **kod taşınmadı, disiplin taşındı**
- **`01_SOURCE/activity.schema.json`** — aktivite kaydı şeması;
  `inheritanceStatus` alanı `locked` için belirleyici; `childTests.tester`
  anonim kimlik biçimini şemada zorunlu kılar
- **Test altyapısı** — `validate_spec.py` (veri + kapsam + **6×5 matris** + kapı),
  **`validate_inheritance.py`** (manifest bütünlüğü + devralma kilidi),
  `validate_structure.py` (dosya + gömülü değer + sızıntı + sır +
  **cevap anahtarı** + **çocuk mahremiyeti**),
  `selftest.py` (**kapıların kendi testi**, dokuz kusurlu kurgu)
- **`04_BUILD/qa_all.sh`** — CI'ın birebir aynısı; Faz 1–5'te doğacak
  kapılar için satırlar şimdiden yazıldı (K18 dersi: ölü betik olmasın)
- **`.github/workflows/validate.yml`** — altı iş; `data` işi
  **devralma bütünlüğünü** de koşturur
- **`.gitignore`** — iki hatlı manuscript koruması

### Kararlar

K1 (ortak kütüphane yok) · K2 (`.gate`) · K3 (tek format: ciltsiz) ·
K4 (bulmaca içerikten türer) · K5 (yaş politikası yeniden yazıldı) ·
K6 (devralma canlı bağımlılık değil) · K7 (kapılar üçüncü taraf paket
kullanmaz) · K8 (kapsam hipotez) · **K9 (doğrulanmamış devralma LOCKED
olamaz)** · K10 (cevap anahtarı ve çocuk kimliği public depoya giremez)

### Açık kararlar

A1 (manuscript politikası) · **A2 (devralma politikası · Faz 1 başlamadan)** ·
A3 (bölge ve mühür mimarisi) · A4 (120 aktivite listesi) · A5 (ciltli sürüm) ·
A6 (yazar biyografisi) · A7 (**çocuk testçiler · Faz 2 bloklayıcısı**)

### Durum

`.gate` = `phase0` · **Faz 1 BAŞLAMADI** · kurucu onayı bekleniyor
