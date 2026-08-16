# NİHAİ SERT DENETİM RAPORU — Aşama 2 · proje kapanışı

> **The Myth Hunter's Field Book** · 16 Ağustos 2026
> Kapı **`release`** · `qa_all` yeşil · ön uçuş **61/61**
>
> Bu denetim nihai ÇIKTILARDAN başladı ve kaynağa doğru gitti.
> Faz 6'nın "KDP paketi hazır" cümlesi **yanlıştı** ve bu rapor neden
> yanlış olduğunu sayıyla söylüyor.

---

## ⚠ ÖNCE BU: ÇOCUK DOĞRULAMASI HÂLÂ YAPILMADI

```
GERÇEK ÇOCUK OTURUMU     0
TEST EDİLEN ÇOCUK        0
externalValidation       overridden-zero-sessions    ← 'passed' DEĞİL
```

Aşama 2 çok şey düzeltti. **Bunu düzeltmedi ve düzeltemez.** Hiçbir
kapak cümlesi, hiçbir A+ satırı ve hiçbir KDP alanı bu kitabın
çocuklarla test edildiğini iddia etmiyor.

---

## 0 · Nihai sayılar

| | |
|---|---:|
| **Sayfa (PDF'ten sayıldı)** | **156** |
| Aktivite | **120** |
| Kültür · bölge | **22 · 6** |
| Mühür yuvası | 37 |
| **Görsel varlık (nihai)** | **158 / 158** |
| Trim | 8,50 × 11,00 in |
| **Sırt** | **0,3513 in** |
| **Tam kapak** | **17,6013 × 11,2500 in** |
| İç blok yazı tipi | **4 / 4 GÖMÜLÜ** |
| Kapak yazı tipi | **4 / 4 GÖMÜLÜ** |
| A+ görseli | 11 |
| Liste · baskı · **telif** | 14,99 $ · 3,65 $ · **5,34 $** |
| Başabaş ACOS | %35,6 |

### Sayfa sayısı DEĞİŞTİ: 160 → 156

Faz 6'nın 160'ı yanlış değildi — **eksikti**. Arka maddenin yedi
sayfası birebir kopyaydı ve basılan şey içerik değil şartnameydi
(§ 3). Düzeltilince dizgi 156 ölçtü ve **sırt, kapak, baskı maliyeti,
telif ve ACOS kendiliğinden yeniden türedi.** Hiçbir sayı elle
taşınmadı. Karar **K44**.

---

## 1 · Aşama 2'nin kapattığı on bir kusur

| # | Kusur | Nasıl bulundu | Karşılık |
|---|---|---|---|
| **1** | İki yer tutucu basıma girecekti | Faz 6 kaydı | ✅ gerçek levha · CLI dizgisi |
| **2** | **Sıfır yazı tipi gömülü** | `pdffonts` | ✅ 4/4 gömülü |
| **3** | **`M■ori`** — imlâ kuralını öğreten sayfada tofu | PDF metni | ✅ Unicode dizgi |
| **4** | Mobilya **iki kez** basılıyordu | ölçüm + s.125 render | ✅ rol ayrımı · kapı |
| **5** | 11 sayfada cevap sızıyordu | kayıt yeniden sayıldı | ✅ 11'i de düzeltildi |
| **6** | İki **olgusal hata** | kaynak denetimi | ✅ ikisi de düzeltildi |
| **7** | Bir ★★★ sayfanın **cevabı yoktu** | `B19` | ✅ cevap yazıldı |
| **8** | **Başlık sayfası bozuktu** | s.1 render | ✅ hiyerarşi kuruldu |
| **9** | Arka madde **kopya + şartname** | s.149–159 render | ✅ gerçek içerik · akış |
| **10** | Sözlük **TÜRKÇE** basılıyordu | s.149 render | ✅ İngilizce · ölçülmüş |
| **11** | Cevap anahtarında **tofu** | s.151 render | ✅ CJK yazı tipi |

> ### Onunun dokuzu ancak ÇIKTIYA BAKARAK bulundu.
>
> Kaynak denetimleri (22 kapı · 230 selftest) Faz 6'da da yeşildi ve
> bu kusurların hiçbirini görmemişti. Bir kapı ancak SORDUĞU soruyu
> ölçer.

---

## 2 · ⭑ EN BÜYÜK BULGU: MOBİLYA İKİ KEZ BASILIYORDU ⭑

Faz 6 raporu şöyle demişti:

> *"`writingSpaceLines` ile `pagePrints` 120 sayfanın 63'ünde uyuşmuyor."*

**Sayı doğruydu, teşhis yanlıştı.** Bu bir "hangi sayı doğru" sorusu
değildi: iki alan **aynı şeyi saymıyordu** ve **ikisi de basılıyordu**.

```
pagePrints "… writing lines"   →  LEVHANIN İÇİNDE  (sanata çizilmiş)
writingSpaceLines              →  DİZGİNİN çizdiği (levhanın ALTINA)
```

Ölçüm:

| Çiftleme | Sayfa |
|---|---:|
| **Yıldızlı kutu iki kez** | **37 / 37** |
| **Yazma alanı iki kez** | **75 / 120** |
| Çiftlemesiz | **21 / 120** |

Sayfa 125 raster'a çevrildi ve göz ile doğrulandı: **iki yıldız kutusu,
iki yazma satırı öbeği.**

> ### 37 mühür sayfasının 37'sinde çocuk İKİ yıldız kutusu görüyordu.
>
> Faz 5 `A1` kutunun **basılı sayısını** düzeltmişti. Kimse kutunun
> **kaç kez basıldığını** sormamıştı. Doğru bir sayı, iki kez basılınca
> doğru kalmıyor.

**Kök neden:** `pagePrints` iki ayrı muhataba yazılmış tek bir listeydi
ve ayrım hiçbir yerde yazılı değildi. Faz 6 promptu doldururken listenin
TAMAMINI üretece verdi.

**Düzeltme — kaynakta, üreteçte, dizgide ve kapıda:**

1. `04_BUILD/furniture_roles.py` rolü **ölçtü** ve `book.json §
   furniture` alanına **dondurdu**
2. `interior.py` artık levhanın bastığını basmıyor
3. `qa_design § ⑨` **uyarıdan kapıya yükseltildi** — her sayfa
   mobilyasını kimin bastığını **beyan etmek zorunda**
4. Serbest kalan dikey alan **levhaya verildi**: çocuğun yazma
   satırları levhanın içinde ve levha artık daha büyük basılıyor

⚠ Bu düzeltme yazma alanını 25 sayfada 7 mm ölçütünün altına
düşürmüştü ve **kapı onu yakaladı**; rezerv hesabı düzeltildi.

---

## 3 · ⭑ İKİNCİ BÜYÜK BULGU: ARKA MADDE İÇERİK DEĞİL ŞARTNAMEYDİ ⭑

On üç arka madde sayfası iki kusuru birden taşıyordu.

**① Aynı sayfa N kez basılıyordu.** `pages: 4` bir **sayfa
bütçesidir**, bir tekrar talimatı değil. Dizgi onu tekrar sanıyordu:

```
glossary     pages: 4  →  dört ÖZDEŞ sayfa
answer-key   pages: 4  →  dört ÖZDEŞ sayfa
how-to-use   pages: 2  →  iki ÖZDEŞ sayfa
sources      pages: 2  →  iki ÖZDEŞ sayfa
```

On üç sayfanın **yedisi birebir kopyaydı.**

**② Basılan şey içerik değil ŞARTNAMEYDİ.** `prints` alanı sayfanın ne
basacağını **tarif eder**:

```
"twenty-two entries, one per culture, in route order"
"one entry per page in page order, numbered as the pages are numbered"
```

Bu bir sözlük değil, bir **sözlüğün tarifidir**. Gerçek yirmi iki
girdi, gerçek yüz yirmi cevap ve gerçek kurum listesi **hiç
dizilmemişti**.

> ### Arka kapak *"the back of the book says which ones"* diye söz veriyordu ve kitabın arkası hangileri olduğunu SÖYLEMİYORDU.

**Düzeltme:** veri zaten ölçülmüş hâlde duruyordu. Arka madde artık
ondan **türetiliyor** ve sayfalara **akıyor** (tekrar etmiyor):

| Bölüm | Kaynak | Sayfa |
|---|---|---:|
| Sözlük | `culture_index` · 22 kültür · bölge · sayfa sayısı · yaşayan mı | 1 |
| Kaynaklar | `research/*-revalidation` · **115 kurum** · bölgeye göre | 1 |
| Cevap anahtarı | `answers/answer_key.json` · **120 girdi** | 4 |

⚠ Mühür sözcükleri **basılmıyor** (`sealWordsPrinted: false`) — kitabın
tek öz-denetimi onlar.

---

## 4 · Editoryal: 11 sızıntı + 2 olgusal hata + 1 eksik cevap

`04_BUILD/editorial_fixes.py` · **23 düzeltme · idempotent · her biri
eski metni birebir eşleştirerek uygulanır.**

### 4.1 · Sızıntılar

| Bulgu | Sayfa | Ne yapıyordu |
|---|---|---|
| B5 | `zulu-two-messengers` | field note dört adımın üçünü cevaplıyordu |
| B6 | `maya-ballcourt-sort` | field note üç sütunun ÜÇÜNÜ de cevaplıyordu |
| B7 | `mesopotamian-plant-quest-steps` | görev satırı + field note |
| B8 | `aztec-maize-journey-sort` | field note kartları sırasıyla anlatıyordu |
| B9 | `inuit-syllabic-signs` | field note görevin TAM cevabını veriyordu |
| B10 | `japanese-eight-of-everything` | field note + ipucu |
| B11 | `maori-macron-length` | adım bir OLGU HATIRLAMAYA bağlıydı |
| B12 | `finnish-alliteration` | adım YANLIŞ ÖNVARSAYIMLA soruyordu |
| B13 | `greek-labyrinth-cipher` | adım 4, adım 3'ün cevabını ilan ediyordu |
| B14 | `greek-constellation-plate` | **ipucu** iki adımı birden cevaplıyordu |
| B15 | `japanese-turtle-time-plate` | **ipucu** cevabı doğrudan veriyordu |

> Faz 6 raporu bu kümeye **dokuz** demişti. Aynı kayıt yeniden okundu:
> aynı kusur **ipucu katmanında iki sayfada daha** duruyordu ve küme
> *"field note"* diye adlandırıldığı için öncelik listesinin dışında
> kalmıştı.
>
> ### Bir sızıntı, hangi kutuda durduğuyla değil NE YAPTIĞIYLA sınıflanır.

### 4.2 · Çözülebilirlik iki sayfada düzeltmeyi DEĞİŞTİRDİ

`mesopotamian-plant-quest-steps` görev satırından *"ends where it
started"* silinince adım 3 **cevapsız** kalıyordu: levha yalnızca
*"Uruk, the king's city"* kartını basıyor, dönüşü basmıyor. Adım
levhanın **gerçekten bastığı** şeye bağlandı.

> ### Bir sızıntıyı kapatmak, sayfayı çözülemez yapmayı haklı çıkarmaz.

### 4.3 · Kapılar üç düzeltmemi reddetti — ve haklıydılar

| Kapı | Ne dedi | Düzeltmenin düzeltmesi |
|---|---|---|
| `validate_research` | `CLM-NI-KALEVALA-METRE` `usedIn: field-note` | field note **korundu**, kusurlu ADIM kaldırıldı |
| `qa_language` | atıf gereken sayfa kültür adını anmalı | *"Maya"* geri kondu, sütun eşlemesi konmadı |
| `qa_echo` | `put a □…` beşinci sayfaya taştı | özgün fiil `order` korundu |

`qa_answerkey` ayrıca cevap anahtarının manuscript'ten sürüklendiğini
yakaladı; senkronizasyon betiğe eklendi.

### 4.4 · Olgusal hatalar — levha sabit, dizgi onardı

**B17 `korean-hangul-place-names`:** levha anahtarı `ㅇ silent` basıyor.
Bu **yanlıştır** — ㅇ hece sonunda /ng/ okunur ve altı addan biri
(Gwangju) tam olarak buna bağlı. Anahtarı harfiyen uygulayan çocuk
`Gwaju` yazıyordu. Anahtar levhanın İÇİNDE ve levha değiştirilemez;
eksik kural **dizgi katmanına** kondu.

**B1 `inuit-sea-creatures-plate`:** adım *"never come out onto the ice"*
diyordu ve cevap halkalı foku o kümeye koyuyordu. Halkalı fok buzda
dinlenir ve yavrusunu buz üstünde doğurur. Adım bir **biyoloji
iddiasından** bir **levha gözlemine** çevrildi.

**B19 `hawaiian-day-length-plate`:** bir ★★★ sayfanın adım 3 cevabı
**kayıtta yoktu**. Bu bir üslup kusuru değil, **eksik bir üründü**.

---

## 5 · Görsel varlıklar

### 5.1 · Teslim ve eşleme

11 dosya teslim edildi; ikisi **kanonik olmayan adla** geldi
(`Pasted image.png`). Eşleme **tahmin edilmedi**: oran ölçüldü ve görsel
içerik denetlendi, sonra `07_ASSETS/DELIVERY_MAP.json` içine
**sha256'ya bağlı** olarak donduruldu.

> Faz 6 sıralı eşlemeyi denemiş ve **ölçülerek yanlışlanmıştı**.
> Aynı hata iki kez yapılmadı.

Yer tutucular **silinmedi**, `rejected/` altına gerekçesiyle arşivlendi.

### 5.2 · İki levhada üreteç metni KULLANILMADI

| Levha | Neden dizgi |
|---|---|
| `fig-yoruba-underdot-letters` | harfin altındaki nokta **içeriğin kendisidir** |
| `fig-korean-river-crossing-sort` | kartların **sırası** cevabın kendisidir |

Üreteç boş mobilyayı çizdi; glifler ve kart metni `plate_typeset.py`
ile gömülü yazı tipinden basıldı. Kart sırası bir **derangement**
olarak donduruldu ve betik bunu doğruluyor.

### 5.3 · Yorùbá levhasında ölçülmüş bir kusur silindi

Teslim edilen levha **altı harf hücresinin ve üç anahtar hücresinin
altına boş daireler** çizmişti. `pagePrints` bunları istemiyor — ve bu
sayfada zararsız değiller: sayfanın bütün görevi *hangi harflerin
ALTINDA nokta var* sorusudur.

> ### Aranan işaretin bulunduğu yere ikinci bir işaret koymak, cevabı bulandırır.

On bir daire beyazla kapatıldı. Sanata dokunulmadı.

### 5.4 · A+ paketinde bir panel DÜŞÜRÜLDÜ

`aplus-05`'in kit fotoğrafı **cetvel** gösteriyordu. Ölçüm: 120
aktivitenin **sıfırı** cetvel kullanıyor ve *"ruler"* çocuğa görünen
metinde **sıfır kez** geçiyor (Faz 5 · `B22`).

> ### Ürün sayfası, ürünün içermediği bir şeyi göstermez.

---

## 6 · Çözünürlük — dürüst tablo

| Katman | Etkin dpi | Durum |
|---|---:|---|
| İç blok · 158 varlık | **150** | kurucu kararı **K39** · KDP tavsiyesi 300 |
| **Kapak sanatı** | **89** | ⚠ **AÇIK · KURUCU EYLEMİ** |
| Kapak **tipografisi** | **vektör** | ✅ çözünürlükten bağımsız |
| A+ görselleri | modül ölçüsünde | ✅ |

Kapak için gereken **5280 × 3375 px**; teslim edilen **1569 × 1003 px**
— **×3,37 eksik**.

> ⛔ **Yukarı örnekleme YAPILMADI.** Piksel eklemeden DPI etiketini 300
> yapmak bir düzeltme değil, bir **yanlış beyandır**. Gerçek dpi
> `06_REPORTS/cover.json` içine sayı olarak yazıldı.

Azaltıcı önlem gerçektir: başlık, yazar, sırt ve arka kapak metni
**vektördür** ve keskin basar. Yumuşak kalan yalnızca arka plan sanatı.

---

## 7 · Tipografi ve dizgi

| Denetim | Sonuç |
|---|---|
| Yazı tipi gömülü | **4/4** iç blok · **4/4** kapak |
| Eksik glif (tofu) | **0** — ölçülerek doğrulandı |
| `Māori` · `Yorùbá` · `Cú Chulainn` | ✅ doğru basılıyor |
| Kana · kanji (cevap anahtarı) | ✅ Droid Sans Fallback |
| Hangul | ⚠ **basılamıyor** — ↓ |
| Metin ↔ çizgi çakışması | 0 (Korece kartlarda ölçülüp düzeltildi) |
| Kaza eseri boş sayfa | **0** — dolgu sayfası *Field Notes* oldu |
| Yazma satırı ≥ 7 mm | **120/120** |

### ⚠ Hangul — kapatılamayan tek tipografi kalemi

Sistemde **gömülebilir (TrueType)** hiçbir yazı tipi hangul kapsamıyor:
Noto CJK PostScript (CFF) dış hatlı ve reportlab onu gömemiyor; Droid
Sans Fallback hangul taşımıyor.

Cevap anahtarı Korece adları **romanizasyonla** veriyor ve sayfa bunu
okura **açıkça söylüyor**: *"Korean place names are given in their
romanised form here; the hangul itself is printed on the activity
page."* Hangul zaten aktivite levhasında basılı.

> Basılamayan bir karakteri yine de basmak, sayfaya **boş kutu**
> koymaktır — ve boş kutu, eksik bilgiden daha kötüdür.

---

## 8 · Sızıntı ve güvenlik

| Tarama | Sonuç |
|---|---|
| Aktivite sayfalarına birebir düşen cevap | **0** |
| Nihai mühür sözcüğü çözülmüş hâlde | **0** |
| Takip edilen 139 dosyada sır | **0** |
| Takip edilen dosyalarda **yerel yol** | **0** ← *bu denetim bir sızıntı yakaladı ve düzeltildi* |
| PDF üstverisinde yerel yol | **0** |
| Türkçe editör metni iç blokta | **0** ← *bu denetim sözlüğü yakaladı* |
| Sahte ISBN · barkod | **0** |

`06_REPORTS/interior.json` build makinesinin **mutlak yolunu** takip
edilen bir dosyaya yazıyordu; yol artık depo göreli.

---

## 9 · Düzeltilmeyen ve NEDEN

| # | Kalem | Neden düzeltilmedi |
|---|---|---|
| 1 | **Kapak 89 dpi** | ham sanat yeniden üretilmeli — **KURUCU** |
| 2 | İç blok 150 dpi (158 varlık) | K39 kurucu kararı · 4× piksel gerekir |
| 3 | `persian-script-direction` `٤٧` | Farsça `۴۷` olmalı; sayı **levhanın içinde** basılı ve levha yeniden üretilmeden düzeltilemez |
| 4 | Arapça/Farsça harf birleşimi (cevap anahtarı) | reportlab bidi/shaping yapmıyor; iki cevap kaydı etkileniyor, aktivite sayfaları etkilenmiyor |
| 5 | Kalan C sınıfı editoryal bulgular | çoğu levha metnine bağlı; levha yeniden üretimi gerektirir |
| 6 | Bölge açılışı sayfalarında boş alan | tasarım tercihi · kusur değil |

> ⭑ **3, 4 ve 5'in ortak kök nedeni tektir:** metin, üretilmiş levhanın
> **içine** çizilmiş durumda. Levha yeniden üretilmeden dizgiden
> düzeltilemiyor. `pagePrints` rol ayrımı (§ 2) bu sınıfı gelecekte
> kapatır: yeni üretilecek her levha metni **dizgiye** bırakacak.

---

## 10 · Kapı durumu

| | Faz 6 | **Aşama 2** |
|---|---:|---:|
| `qa_all.sh` | yeşil | **yeşil** |
| Kapı sayısı | 22 | **26** |
| `selftest` | 230 | **230** |
| `qa_design` | 19 | **21** |
| `metadata` | 11 | **16** |
| **KDP ön uçuş** | **yoktu** | **61** |
| CI ortamı (yalnız takip edilen) | yeşil | **yeşil** |

Yeni kapılar: `furniture_roles --check` · `editorial_fixes --check` ·
`asset_intake --verify` · `plate_typeset --check` · `covers --check` ·
`kdp_preflight`.

Hepsi kaynağı yokken **boş koşar** — CI'da manuscript ve ham görsel
bulunmaz ve *"üretilmemiş bir çıktı, bozuk bir çıktı değildir."*

---

## 11 · Teslim paketi

```
08_OUTPUT/PAPERBACK/
    interior.pdf              156 sayfa · 40,6 MB · 4/4 yazı tipi gömülü
    cover.pdf                 tek PDF · 17,6013 × 11,2500 in · 4/4 gömülü
    metadata.json             KDP alan değerleri
    checksums.txt             sha256

08_OUTPUT/APLUS/
    11 görsel                 1940×600 · 600×600 · hepsi < 3 MB
    APLUS_MODULE_MAP.md       modül → görsel → kopya
    checksums.txt

08_OUTPUT/
    KDP_UPLOAD_HANDBOOK.md    adım adım · KURUCU/AJAN ayrımıyla
    PROOF_HANDOFF.md          fizikî prova denetim listesi
    FINAL_KDP_PREFLIGHT.md    61 denetimin ölçümü
```

---

## 12 · Kurucuya kalan — ve yalnızca kurucuya

| # | İş | Neden ajanda değil |
|---|---|---|
| 1 | **KDP paneli** — bütün adımlar | panel erişimi kurucunundur |
| 2 | **AI beyanı** | bir BEYANDIR · kurucu verir |
| 3 | **Kapak sanatı ≥5280 × 3375** | ham görsel üretimi kurucuya ait |
| 4 | **Fizikî prova (A9)** | sipariş ve değerlendirme |
| 5 | **Gerçek çocuk oturumu (A10)** | araç hazır · **0 oturum** |
| 6 | İki ebeveyn okuması | insan okuması |
| 7 | Fiyat testi | yayından sonra |
| 8 | 150 dpi kararı (A16) | kabul mü, yeniden üretim mi |

---

## 13 · Bu aşama neyi kanıtladı

| Soru | Cevap |
|---|---|
| Yeşil bir CI, iyi bir kitap demek mi | **HAYIR.** 22 kapı yeşilken on bir kusur duruyordu |
| Bir kusur nasıl bulunur | **ÇIKTIYA BAKARAK.** Dokuzu ancak render edilerek görüldü |
| Bir sayfa bütçesi bir tekrar talimatı mıdır | **HAYIR** — ve dizgi beş faz boyunca öyle sandı |
| Bir şartname bir içerik midir | **HAYIR.** Arka madde on üç sayfa boyunca kendini tarif etti |
| Bir düzeltme yeni bir kusur açabilir mi | **EVET — üç kez.** Üçünde de kapı yakaladı |
| Ölçüm modeli yalanlayabilir mi | **EVET, YİNE.** 160 → 156 |
| **Çocuklar talimatları yardımsız anlıyor mu** | **HÂLÂ BİLİNMİYOR** |

---

> ## FİNAL DURUM
>
> ```
> KDP UPLOAD READY          ✅   dosyalar üretildi ve denetlendi
> KDP PUBLISHED             ❌   ajan panele dokunamaz
> ÇOCUK DOĞRULAMASI         ❌   0 oturum
> KAPAK SANATI 300 dpi      ⚠   kurucu kararı
> ```
>
> **KDP paneline dokunulmadı. Previewer çalıştırılmadı. Prova sipariş
> edilmedi. Hiçbir dosya yüklenmedi. Hiçbir şey yayımlanmadı.**
