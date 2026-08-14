# CHANGELOG — The Myth Hunter's Field Book

Bu dosya **ne zaman ne değişti ve neden** sorusunu yanıtlar.
Her faz kendi girdisini ekler. Format: ters kronolojik.

---

## [Yayımlanmamış] — 2026-08-14 · Faz 4 · A11 kapandı, eşikler TÜRETİLİYOR

**Kurucu A11'i yanıtladı: Faz 3 eşiği 60'tır, 80 değil.**

### Kararlar

- **K29** · **A11 KAPANDI.** `gates.requirements.phase3` **80 → 60**
  (kurucu onayı). Ve kök neden kapatıldı: eşikler artık elle yazılmıyor,
  `gates.productionPlan × scope.regionsHypothesis[].activityQuota`
  formülünden **türetiliyor**. `validate_spec § ⑥` her koşuda yeniden
  hesaplıyor.
- **K30** · Kurucu aşması **Faz 4'e genişletildi**. `authorisedPhase`
  `phase3` → `phase4`; `gateCeiling` **`phase1`'de kaldı**,
  `externalValidation` **`pending`'de kaldı**, A10 **açık kaldı**.
- **K31** · **A4 KAPANDI** — 120 aktivitenin nihai listesi tamam.

### Değişti — eşik merdiveni

| Kapı | ESKİ | YENİ | Not |
|---|---:|---:|---|
| `phase2` | 20 | **16** | türetme sonucu · `jaguar-condor` kotası |
| `phase3` | **80** | **60** | ⭑ **kurucu onayı** · 16 + 24 + 20 |
| `phase4` | 120 | 120 | değişmedi · 60 + 24 + 20 + 16 |

**80 bir hata değil bir ARTIKTI.** Merdivenin tamamı bootstrap'ın
*"6 bölge × 20"* varsayımından geliyordu (`20 · 40 · 60 · 80 · 100 · 120`);
Faz 1 kotaları **eşitsiz** kurdu (K18 · `16 · 20 · 24 · 24 · 20 · 16`) ve
merdiven o gün sessizce yalanlandı. İki basamağı yanlıştı.

`phase2`'nin 20'si kurucunun sorusunda **adı geçmedi** ve türetme onu
kaçınılmaz olarak yakaladı. Değişiklik `founderApproved` /
`derivedConsequence` alanlarıyla **ayrı** kaydedildi ve geri alınabilir.

> **Eski değerler SİLİNMEDİ.** `gates.requirementsHistory` onları makine
> okunur biçimde taşıyor ve `validate_spec § ⑥(g)` kaydın silinmesini
> kırmızı yakıyor.

### Eklendi

- **`validate_spec § ⑥`** — kapı eşiklerinin türetilmesi · 8 alt denetim
- **`gates.productionPlan`** — hangi faz hangi bölgeyi üretir · türetmenin
  tek kaynağı
- **`gates.requirementsHistory`** — eşik değişikliklerinin tarihî kaydı
- **`selftest § ⑰`** — 8 kusurlu kurgu · **eski 80 geri yazılırsa KIRMIZI**

### Düzeltildi

- `selftest` § ⑯ kendini ekrana **⑰** diye yazıyordu — gerçek bir ⑰
  doğduğu gün çakışacaktı
- `selftest § ③` phase2 eşiğini **elle yazıyordu** (20); artık config'ten
  okuyor ve eşiğin **tam yerini** sınıyor (bir altı kırmızı, tam üstü yeşil)

---

## [0.3.0] — 2026-08-13 · Faz 3 · iki bölge, iki kapı, bir tasarım dizgesi

**Faz 3, A10 çocuk oturumu yapılmadan kurucu talimatıyla başlatıldı.**
Aşma gizlenmedi: kayda geçti (**K27**) ve mekanik bir kilide çevrildi.

```
FAZ 3 YETKİSİ       ✅ VERİLDİ     (kurucu)
A10 ÇOCUK OTURUMU   ❌ YAPILMADI   (0 oturum · değişmedi)
.gate                   phase1     (YÜKSELTİLMEDİ)
```

### Kararlar

- **K27** · Faz 3 aşması — `project_config § founder.phaseOverride` +
  `validate_spec § ⑤`. Dört kilit: kapı tavanı aşılamaz,
  `externalValidation` 'passed' olamaz, blokaj kapanamaz, aşma
  belgelerden düşemez.
- **K28** · Faz 3 bölgeleri **ölçülmüş yükle** seçildi: `monsoon` (87,68)
  ve `great-ocean` (75,50) — yazılmamış iki en ağır bölge.
- **A11 (yeni)** · `gates.requirements.phase3` **80** diyor, yol haritası
  **60**. Ajan hiçbirini değiştirmedi; kurucu kararı.

### Eklendi

- **`02_MANUSCRIPT/book.json` v3.0** — 16 → **60 sayfa** · üç bölge
  (jaguar-condor 16 · monsoon 24 · great-ocean 20). `regionOpening`
  tekil alanı **çoğula** çevrildi.
- **`01_SOURCE/research/monsoon-revalidation.json`** — 24 iddia
- **`01_SOURCE/research/great-ocean-revalidation.json`** — 18 iddia
- **`04_BUILD/qa_echo.py`** — tekrar ve kültürel düzleşme · 6 denetim
- **`04_BUILD/qa_design.py`** — tasarım dizgesi ve görsel şartnamesi · 7 denetim
- **`04_BUILD/image_prompts.py`** — prompt kütüphanesi **üretilir** (K17)
- **`00_CONTEXT/DESIGN_SYSTEM.md` v1.0** — 10 modül + 10 düzen, donduruldu
- 60 sayfa için **görsel şartnamesi** · 317 zorunlu etiket ·
  **0 üretilmiş varlık**

### Araştırma — 42 yeni iddia, üç düzeltme, bir düşen sayfa

24 devralma kaydı `inherited-provisional` → `inherited-verified`
(7 → **31** / 76). Üç iddia **cevap eşiğini geçemedi** ve sayfalar
yeniden tasarlandı:

| Sayfa | Neydi | Ne oldu |
|---|---|---|
| `hindu-river-names-sort` | *"hepsi buzda başlar"* ve sıradağ eşleştirmesi | Sutlej **gölden** doğar; eşleştirme **çift cevaplıydı** → adlandırılmış kaynak |
| `vietnamese-mountain-water-sort` | *"yarışmanın dört turu"* | iki bağımsız kaynakta **yok** → nedensel omurga |
| `japanese-turtle-time-plate` | anlatının sayıları (3 yıl / 300 yıl) | değişkeye göre **değişiyor** → metin tarihleri 713 · 720 · 759 |
| `korean-sky-rope-plate` | hangi kardeş güneşi aldı | doğrulanamadı → **kitaptan düştü**, yerine `korean-hangul-build` |

### Kapıların kendi kusurları — üçü gerçekti

- **`qa_age § ⑨` doğru imlâyı cezalandırıyordu.** Sayfada **Māori**
  yazılıyken kapı *"atıfsız"* diyordu ve kapıyı susturmanın en kolay
  yolu **makronu düşürmekti**. `validate_research § ⑧` tam tersini şart
  koşuyor: iki kapı birbirine ters çalışıyordu.
- **`selftest` kurgusu elle bakım istiyordu** — tek bir doğrulama dosyası
  adı gömülüydü; dizin artık taranıyor.
- **`update_docs` bölge açılışını kelime sayımından düşürüyordu**
  (alan adı yanlış, alan tekildi): 1.015 → **1.175**.
- Faz 1'den kalan mühür yuvaları seçilmemiş adaylarda duruyordu.
- **`DESIGN_SYSTEM.md` sayfa kalıplarını ikinci kez basıyordu** —
  sızıntı kapısı yakaladı ve haklıydı.

### Ölçüldü

| | Faz 2 | **Faz 3** |
|---|---:|---:|
| Yazılmış sayfa | 16 | **60** |
| Ölçülmüş bölge | 1 / 6 | **3 / 6** |
| Sayfa modeli | 144 | **144** (hedef 148 · sapma −%2,7) |
| Ort. sayfa ağırlığı | 0,844 | 0,844 · 0,865 · 0,863 |
| Kapı öz-testi | 114 | **145** |
| Doğrulanmış devralma | 7 / 76 | **31 / 76** |

**Faz 2'nin kelime tahmini DOĞRULANDI.** Faz 2 açığın *"sayfa
mobilyasında"* olduğunu tahmin etmişti; mobilya artık yazıldı ve
prozanın **%75'i kadar**: 3.958 proza + 2.968 mobilya. Kelime hedefi
(22.000) yine de yüksek görünüyor ve **fiyat modelini etkilemiyor** —
sayfa modeli `pageWeight`ten türüyor, kelimeden değil.

### DEĞİŞMEYEN

`.gate` `phase1` · A10 **açık** · `externalValidation` `pending` ·
`STYLE.md` v1.2 · altı bölge · 37 yuva · 148 hedefi · A9 kurucuya ait.

---

## [0.2.1] — 2026-08-13 · A7 onayı · Türkçe testçi paketi

**Kurucu A7'yi onayladı: en az iki Türkçe konuşan çocuk testçi bulundu.**
Türkçe tester-facing materyal üretildi. **Oturum hâlâ yapılmadı.**

### Karar

- **A7 → K26** · `founderConfirmed: true` · `availableTesters: 2`
- **A10 (yeni)** · gerçek oturumun koşturulması — **açık**, kurucuya ait

```
TESTÇİ BULUNDU     ✅   MATERYAL ÜRETİLDİ  ✅
OTURUM YAPILDI     ❌   → externalValidation hâlâ 'pending'
```

### Eklendi

- **`01_SOURCE/pilot_tr/source-tr.json`** — 16 sayfanın Türkçe kaynağı
  (çeviri değil, **ayrı yazılmış** materyal) · **depo dışı**
- **`01_SOURCE/pilot_tr/tester-pack-tr.txt`** — üretilen paket: veli notu,
  16 sayfa, boş kayıt formu · **cevap taşımaz** · **depo dışı**
- `.gitignore § ①d` — `01_SOURCE/pilot_tr/` depodan dışlandı
- `selftest.py` **111 → 114 denetim** — paketin üç yolu da kanıtlandı

### Türkçe mühür sözcüğü: KATMAN

Ticari mühür **CONDOR** kalır. Türkçe yıldızlı sözcüklerin harfleri onu
kurmaz ve zorlamak ya dilleri karıştırır ya da mührü anlamsız bir harf
dizisine indirger. İkincisi **testin kendisini yok ederdi**: mühür
mekaniğinin test edilecek özelliği tam da sözcüğün **anlamlı** olmasıdır.

```
kakao[1]=K · ahuejote[1]=A · nochtli[5]=T
hamur[3]=M · patates[2]=A  · tane[3]=N     →  KATMAN
```

### Düzeltildi

- **`child_test_pack.py` Türkçe basamıyordu.** Reddetme kapısı çalışıyordu
  ama kapı **açıldığında** ne olacağı yazılmamıştı: İngilizce prozayı
  basıp üstüne `tr` etiketi yapıştıracaktı. Artık ayrı kaynak okuyor ve
  kaynak yoksa **reddediyor** (çıkış 3)
- **Türkçe kaynak yanlış yerdeydi** — `02_MANUSCRIPT/` altında, kanonik
  manuscript'in yanında. `qa_language § ④` yakaladı; bütün Türkçe malzeme
  `01_SOURCE/pilot_tr/` altına alındı
- `qa_language § ⑤` artık **onay ≠ oturum** uyarısı basıyor

### Değişmeyen

- `externalValidation: "pending"` · `CHILD_TEST_LOG.md` **0 oturum**
- `.gate` **`phase1`** · `STYLE.md` **v1.2**
- Ticari dil **İngilizce**; CONDOR mührü ve `book.json` **dokunulmadı**

## [0.2.0] — 2026-08-13 · Faz 2 · Pilot: Jaguar and Condor + kapı seti

**16 sayfa yazıldı ve kilitlendi.** Bir bölgenin tamamı, üç kontrollü
partide. Kapı **`phase1`'de KALDI** — gerekçe § *Değişmeyen* altında.

### Karar — kurucu

- **A3 → K18** · altı bölge ve **37 mühür yuvası KİLİTLENDİ**
- **A8 → K19** · **148 sayfa kabul edildi**, telif 5,55 $ → **5,48 $**.
  `pageTarget` 144 → 148, `BRIEF § 7` aynı sayılara güncellendi ve
  `page_budget.py`'nin kalıcı uyarısı **sustu**
- **A9 (yeni)** · fizikî prova **kurucuya aittir** — ajan sipariş etmez,
  yapıldığını iddia etmez, geri bildirim uydurmaz
- **A7** · **0 çocuk testçi**. Paket hazır, test **koşturulmadı**,
  dış doğrulama **BEKLİYOR** — PASS değil

### Eklendi — kapılar

- **`qa_solvable.py`** — tek cevaplılık · ipucu sızıntısı ·
  **mühür harfinin yeniden hesaplanması**
- **`qa_instruction.py`** — emir kipi · adım birliği · edilgen sürüklenme ·
  yazma alanı
- **`qa_language.py`** — ticari katman İngilizce mi · **testçi yokken
  test materyali üretilmiş mi**
- **`qa_progression.py`** — yuva bütünlüğü · harf türevi · çentik ·
  **hasar yarıçapı** · **zincirleme bağımlılık**
- **`region_difficulty.py`** — pilot bölgesi HESAPLANIR (ölçüm, kapı değil)
- **`child_test_pack.py`** — testçi paketi üreteci; **testçi onayı yokken
  Türkçe materyal üretmeyi REDDEDER** (çıkış 3)
- **`validate_research.py § ⑩`** — **iddia zinciri**: kilitli bir sayfanın
  her iddiası bir kanıt kaydına bağlı mı
- **`qa_matrix.py § ⑧`** — **seçilebilirlik**: zorluk × kota × tip
  BİRLİKTE sağlanabiliyor mu
- `selftest.py` **70 → 111 denetim**; her yeni kapının her dalı için
  kusur taşıyan kurgu

### Eklendi — içerik ve kanıt

- **`02_MANUSCRIPT/book.json`** — 16 sayfa + bölge açılışı · **depo dışı**
- **`01_SOURCE/research/jaguar-condor-revalidation.json`** — **13 iddia**,
  her biri kaynağı ve erişim tarihiyle künyeli · **depoda durur**
- **`03_EDITORIAL/CHILD_TEST_PROTOCOL.md`** · **`CHILD_TEST_LOG.md`**
  (0 oturum) · **`AGE_REVIEW_LOG.md`**
- `activity.schema.json` **v2.0 → v2.1** — `claimRefs` alanı

### Düzeltildi — İÇ EDİTORYAL İNCELEME (61 bulgu · 14 bloklayıcı)

Bağımsız bir alt-ajan 16 sayfayı sekiz yaşındaki bir çocuk gibi harfi
harfine okudu. **On üç kapı yeşilken 16 sayfanın 11'i çözülemezdi.**

- **Mühür kuralı çocuğa HİÇ basılmıyordu** — `$comment` ve `meta` içinde
  duruyordu; çocuk altı kutuya altı sözcük yazıp CONDOR'u hiç kurmazdı.
  Artık bölge açılışında ve her yıldızlı kutunun yanında basılı
- **`aztec-number-signs` çarpmayı hiç söylemiyordu** — "Add the three
  counts" 1+2+1 = **4** veriyordu; doğru cevap 8820
- **Beş field note görevin cevabını veriyordu** — çocuk düşünmüyor,
  kopyalıyordu
- **Atıf 16 sayfanın 11'inde yoktu** — tasarım katmanı
  `attributionRequired: true` diyordu ama kültür adı sayfada geçmiyordu
- **"the key" sayfada olmayan bir anahtarı gösteriyordu** — beş sayfada
  benzer gönderme kusuru
- `tetl + nochtli` birleştirilemiyordu ("tetlnochtli"); adım eşleştirmeye
  çevrildi
- Üç yıldız talimatı **iki farklı sözcüğe** uyuyordu ve her biri farklı
  bir mühür harfi üretiyordu
- 16 sayfanın hepsinde ipucu vardı; `ACTIVITY_TAXONOMY § 5` yalnızca
  ★★★ için ipucu tanımlıyor → 4 sayfaya indirildi

### Eklendi — incelemeden doğan üç kapı

- **`qa_instruction § ⑨`** — belirtili gönderme sayfada basılı mı;
  yeni **`pagePrints`** alanı (16 sayfa · 67 madde) hem kapı girdisi hem
  **Faz 5 görsel şartnamesi**
- **`qa_solvable § ⑧`** — field note cevabı söylüyor mu
- **`qa_age § ⑨`** — atıf zorunluysa kültür adı **sayfada** geçiyor mu
- `selftest.py` **106 → 111 denetim**

### Düzeltildi — kapıların bulduğu altı kusur

1. **Seçilebilirlik boşluğu** — `jaguar-condor`'un zorluk profili, kültür
   kotaları ve tip asgarileri **ayrı ayrı** sağlanıyordu ama kesişimleri
   **boştu**: geçerli hiçbir 16'lık kitap seçimi yoktu. İki aday
   editoryal gerekçeyle taşındı; `qa_matrix § ⑧` doğdu
2. **Amblem glifi kent adı sanılıyordu** — bir amblem glifi bir
   **krallığı** adlandırır, harabelerin bugünkü adını değil
3. **400 işareti 'tüy' deniyordu** — *tzontli* **saç** demektir; kaynaklar
   işareti "tüy ya da saç" diye tarif ediyor
4. **Top oyununun kuralları 'bilinmiyor' sayılıyordu** — Aztek oyununun
   kuralları 16. yüzyılda **görgü tanığıyla yazıldı**; bilinmeyen şey
   yedi yüz yıl önceki Maya oyununun aynı olup olmadığı
5. **Kehanet adımı bir sıralama görevinin içindeydi** — Oxomoco ve
   Cipactonal'ın fal adımı çocuğa görünen diziden çıkarıldı
6. **`qa_instruction § ②` ölü doğmuştu** — "metinde 'you' var mı" diye
   soruyordu ve `Your mission:` kalıbı yüzünden **hiçbir koşulda**
   yanamıyordu. Edilgen/kişisiz tarayıcıya çevrildi

### Değişti

- `page_budget.py` telif dayanağını artık **config'ten okuyor**, gömmüyor;
  sapma uyarısı **yön duyarlı** (model ucuzladığında "kıs" demiyor)
- `page_budget.py` bir bölgenin seçimi kilitlendiğinde **havuz ortalaması
  yerine gerçek seçimi** ölçüyor
- `STYLE.md` **v1.1 → v1.2** — mühür kuralı ve talimat tabanı eklendi.
  **v2.0 DEĞİL**: o numara ilk gerçek çocuk oturumuna ayrıldı
- Faz 1 mimari pilotu `09_ARCHIVE`'a alındı — Faz 2 ölçümü karışmasın

### Değişmeyen — ve neden

- **`.gate` `phase1`'de KALDI.** `phase2` kapısı 20 yazılmış aktivite ve
  **geçen bir çocuk testi** ister. 16 sayfa yazıldı ve çocuk testi
  yapılamadı. Kapıyı yükseltmek, yapılmamış bir testi geçmiş saymaktır
- Devralınan 69 kayıt hâlâ `inherited-provisional` — doğrulama **kullanıma
  göre** ilerler, toptan değil

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
