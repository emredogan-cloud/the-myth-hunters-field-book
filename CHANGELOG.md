# CHANGELOG — The Myth Hunter's Field Book

Bu dosya **ne zaman ne değişti ve neden** sorusunu yanıtlar.
Her faz kendi girdisini ekler. Format: ters kronolojik.

---

## [0.1.0] — 2026-08-13 · Faz 1 · Devralma mimarisi, taksonomi, yaş çerçevesi

**Kitap yazılmadı.** Bu fazın işi, üretim başlamadan önce mimarinin
tuttuğunu kanıtlamaktı. Kapı `phase0` → **`phase1`**.

### Eklendi — veri

- **`01_SOURCE/inherited/IMPORT_MANIFEST.json`** — World Myths'ten **76 kayıt**
  (22 kültür + 54 hikâye), her biri sha256'lı, kökeni ve **yetkisi** yazılı.
  Her kayıt dört soruya cevap veriyor: nereden geldi · ne devralındı ·
  burada ne yapılabilir · doğrulandı mı
- **`01_SOURCE/culture_index.json`** — 22 kültürün **aktiviteye
  çevrilebilirlik** kararı: kademe (A/B/C), izinli tipler, **yasak biçimler**,
  kota ve — kritik — her kültürün **kamuya açık yazı dizgesi**
- **`01_SOURCE/region_index.json`** — 6 bölge, kültür eşlemesi, kotalar,
  **mühür mekaniği** ve final görev yapısı. Mühür *sözcükleri* burada YOK
- **`01_SOURCE/activity_index.json`** — **168 aday** (hedef ≥160).
  Her biri gerçek bir devralma kaydına bağlı, hiçbiri `locked` değil,
  168'i de kendi `revalidationPlan`ını taşıyor
- **`01_SOURCE/activity.schema.json` v2.0** — `objective` · `steps` ·
  `materials` (beyaz liste) · `safetyClass` · `learningDimensions` ·
  `sourceStory` · `revalidationPlan` · `sealSlot` · `pageWeight`.
  **Tasarım katmanı ile proza katmanı şemada ayrıldı**

### Eklendi — belge

- **`00_CONTEXT/CULTURE_POLICY.md`** — hangi kültür hangi biçimde aktiviteye
  girer. Bu projenin **ikinci en özgün parçası**
- **`00_CONTEXT/ACTIVITY_TAXONOMY.md`** — beş tip, alt biçimleri, on öğrenme
  boyutu, tipik kusurları
- **`00_CONTEXT/PROGRESSION_ARCHITECTURE.md`** — kitap neden bitirilir:
  beş hareket, mühür mekaniği, rota
- **`07_ASSETS/IMAGE_PROMPT_LIBRARY.html`** — sekiz görsel sınıfı,
  kopyalanabilir prompt gövdeleri, **kültür güvenliği negatif promptları**.
  Faz 1 iskeleti; nihai 150 varlık Faz 5'te
- **`06_REPORTS/PHASE_1_REPORT.md`** — faz raporu

### Eklendi — kapı

- **`04_BUILD/validate_research.py`** — araştırma zinciri: aktivite → hikâye
  → kültür → kayıt → kaynak. Kademe tutarlılığı, **cevap yetkisi**,
  **diakritik bütünlüğü** (mojibake + tanık karakterler)
- **`04_BUILD/qa_matrix.py`** — 6×5 matris, kültür kotası, zorluk profili,
  **mühür yuvaları**, tekrar, açık uçluluk, terim tutarlılığı
- **`04_BUILD/qa_age.py`** — **güvenlik sınıfı hesaplayıcısı**, altı yasak
  çerçeve, betimleme fiili taraması, denetim yükü
- **`04_BUILD/qa_readability.py`** — **üç register** ayrı ölçülür + değişmez
- **`04_BUILD/page_budget.py`** — sayfa modeli, baskı sınırı, telif
- **`04_BUILD/update_docs.py`** — `BOOK_STATS.md` ve `ROADMAP_PROGRESS.md`
  artık **üretiliyor** ve bayatlıkları denetleniyor
- **`04_BUILD/import_from_world_myths.py`** — devralma ithalatçısı (araç);
  kaynak depo yoksa çıkış 2 = ATLANDI
- **`05_TESTS/selftest.py`** — dört bölümden **dokuz** bölüme, 22'den
  **70 denetime**. ⑤–⑨ her yeni kapı için kusurlu kurgu koşturuyor

### Değişti

- **Altı bölge yeniden kuruldu.** Bootstrap'ın bölgeleri 22 kültüre
  oturmuyordu: Okyanusya'ya iki kültür düşüyor, **Amerikalara hiç bölge
  kalmıyordu**. Bölgeler kıtaya göre değil **araziye** göre kuruldu (K15)
- **`STYLE.md` v1.0 → v1.1** — tek okunabilirlik bandı **üç register
  bandına** ayrıldı. Gerekçe ölçüm, tercih değil (K16)
- **`AGE_POLICY.md` v1.0 → v2.0** — `SAFE` / `SAFE-WITH-ADULT` /
  `DO-NOT-USE` kararı **mekanikleştirildi**: malzeme beyaz listesi,
  karar ağacı, kapalı arıza (K14)
- **`project_config.json`** — `scope.locked: true`; bölgeler, register
  bantları ve kotalar eklendi
- **`.gate`** — `phase0` → `phase1`

### Kaldırıldı

- `activity.schema.json`'ın sızıntı muafiyeti — şema v2 artık sayfa dili
  örneklerini taşımıyor, muafiyet **öldü** ve `selftest § ④` onu yakaladı

### Kapıların Faz 1'de bulduğu kusurlar

Kapılar **yazıldıkları gün** iş yaptı:

1. Üç bölge en kolay bantta (★) havuzsuz kalıyordu → altı aday yeniden kalibre edildi
2. Zulu'ya harita aktivitesi verilmiş ama `allowedTypes`'ta yoktu
3. **İki mühür yuvası**, yaş incelemesi kapanmamış hikâyelere dayanıyordu
4. Vietnam kaydı ton işaretlerini adlandırıyor ama **taşımıyordu**
5. Şema muafiyeti ölmüştü
6. `qa_age` regex'i *"matches"* (eşleştirir) fiilini **kibrit** sanıyordu — 13 yanlış ret

Ayrıca `selftest § ⑤(k)`'nin ilk hâli malzeme adlarının belgede
**geçtiğini** doğruluyordu ama **hangi kademede** olduğunu değil.
`ruler` kodda T0, belgede T1 durduğu hâlde test yeşil yanıyordu.

> Bir kapı *"adı geçiyor mu"* diye sorarsa, o kapı **yoktur**.

### Kapanan kararlar

- **A1** → **K11** · manuscript public depoda durmaz
- **A2** → **K12** · devralma politikası (a): kopyala + sha256 + kullanıma göre doğrula

### Açılan karar

- **A8** · 148 sayfa kabul edilip BRIEF § 7 mi güncellenecek, yoksa
  4 sayfa mı kısılacak (Faz 1 önerisi: kabul et)

### Ölçülen

| | |
|---|---:|
| Aday aktivite | **168** / ≥160 |
| Kültür · bölge | **22** · **6** |
| Matris hücresi | **30/30 dolu** |
| Devralınan kayıt | **76** |
| `safe` oranı | **%96,4** |
| Sayfa modeli | **148** (+%2,8) |
| Ciltsiz telif | **5,48 $** |
| Kapı öz-testi | **70 denetim yeşil** |

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
