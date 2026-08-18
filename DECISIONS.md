# DECISIONS — karar kaydı

> İki şey taşır: **alınmış kararlar** (`K##`) ve **AÇIK KARARLAR** (`A#`).
> Bir varsayım sessizce proje gerekliliğine dönüşemez.

---

## AÇIK KARARLAR — kurucudan yanıt bekleyen

Durum tablosu · **14 Ağustos 2026 · Faz 5**

> ⚠ **A10 ERTELENDİ, KAPANMADI.** Kurucu Faz 3'ü A10 beklenmeden
> başlattı (**K27**), Faz 4'ü aynı aşmayla açtı (**K30**) ve Faz 5'i de
> aynı aşmayla açtı (**K34**).
> Bu, testin yapıldığı anlamına **gelmez**.
> `externalValidation` hâlâ `pending`, `.gate` hâlâ `phase1`.

| # | Soru | Aciliyet | Ne zaman kapanmalı | Durum |
|---|---|---|---|---|
| ~~A1~~ | ~~Manuscript public depoda mı duracak?~~ | — | — | ✅ **KAPANDI → K11** |
| ~~A2~~ | ~~Devralma politikası onayı~~ | — | — | ✅ **KAPANDI → K12** |
| ~~A3~~ | ~~6 bölge ve mühür mimarisi onayı~~ | — | — | ✅ **KAPANDI → K18** |
| ~~A8~~ | ~~148 sayfa kabul edilecek mi~~ | — | — | ✅ **KAPANDI → K19** · *sonra **K33** ile aşıldı* |
| ~~A7~~ | ~~≥2 çocuk testçi~~ | — | — | ✅ **KAPANDI → K26** · testçi bulundu |
| ~~A11~~ | ~~`gates.requirements.phase3` 80 mi 60 mı~~ | — | — | ✅ **KAPANDI → K29** · kurucu **60** dedi |
| ~~A4~~ | ~~168 adaydan 120'sinin nihai seçimi~~ | — | — | ✅ **KAPANDI → K31** · Faz 4 kalan 60'ı seçti |
| ~~A12~~ | ~~148 mi 144 mü · dayanak gözden geçirmesi~~ | — | — | ✅ **KAPANDI → K33** · kurucu **144** dedi |
| ~~A10~~ | ~~gerçek oturumun koşturulması~~ | — | — | ⚠ **KAPANDI → K40** · **KURUCU AŞMASI · SIFIR OTURUM** |
| **A9** | fizikî prova siparişi ve değerlendirmesi | ORTA | Faz 5–6 | AÇIK · **KURUCUYA AİT** |
| **A5** | Ciltli hediye sürümü v1.0'a girecek mi | DÜŞÜK | Faz 4 | AÇIK (varsayım: hayır) |
| ~~A6~~ | ~~Yazar biyografisi metni~~ | — | — | ✅ **KAPANDI → K36** · kurucu metni |
| ~~A13~~ | ~~dizilmiş sayfa 160, hedef 144~~ | — | — | ✅ **KAPANDI → K38** · kurucu **160** dedi |
| ~~A14~~ | ~~156 ham görsel hedefin altında~~ | — | — | ✅ **KAPANDI → K39** · kurucu **150 dpi** dedi |
| — | İki ebeveyn okuması | ORTA | Faz 5 | AÇIK · **KURUCUYA AİT** |
| — | ~150 görselin RAW üretimi | ORTA | Faz 5 | AÇIK · **KURUCUYA AİT** · hat hazır (K35) |
| **A15** | **Sayfa mobilyası çiftlemesi — hangi taraf bırakacak** | **YÜKSEK** | **Aşama 2 · dizgiden ÖNCE** | **AÇIK · KURUCU KARARI** |
| **A16** | **156 levha 300 dpi'da yeniden üretilecek mi** | **YÜKSEK** | **Aşama 2 · A15 ile BİRLİKTE** | **AÇIK · KURUCU KARARI** |
| **A17** | Kapak sanatı · A+ · iki eksik levha **RAW üretimi** | **YÜKSEK** | Aşama 2 öncesi | AÇIK · **KURUCUYA AİT** · sözleşme yazıldı |

---

### A15 · Sayfa mobilyası iki kez basılıyor — **hangi taraf bırakacak**

**Ölçüm:** yıldızlı kutu **37/37** mühür sayfasında, yazma alanı
**75/120** sayfada **iki kez** basılıyor — bir kez levhanın içinde
(sanata çizilmiş), bir kez `interior.py` tarafından. Çiftlemesiz sayfa
**21/120**.

Kök neden: `pagePrints` iki ayrı muhataba yazılmış tek bir liste ve
**ayrım hiçbir yerde yazılı değil**:

```
LEVHANIN çizeceği   anahtar paneli · kart · harita · nesne
DİZGİNİN çizeceği   yazma satırı · yıldızlı kutu · numara kutusu
```

Faz 6 promptu doldururken listenin **tamamını** üretece verdi.

> ### 37 mühür sayfasının 37'sinde çocuk İKİ yıldız kutusu görüyor.

**Kurucudan istenen karar — iki yol var ve ikisi de bedelli:**

| Yol | Ne yapılır | Bedel |
|---|---|---|
| ① **Dizgi bırakır** | `pagePrints` maddelerine rol eklenir; `interior.py` levhanın çizdiğini çizmez | levhalar yeniden üretilmez · **ucuz** · levhalardaki gömülü metin kalır |
| ② **Levha bırakır** | 156 levha mobilya olmadan **yeniden üretilir**; dizgi tek yetkili olur | **pahalı** · ama tipografi politikası (§ 4) geri gelir |

⚠ **Seçim sayfa sayısını değiştirebilir** — ve sayfa sayısı değişirse
**sırt değişir**, kapak yeniden dizilir.

⚠ **A16 ile birlikte verilmelidir.** ② seçilirse levhalar zaten yeniden
üretiliyor demektir ve 300 dpi'ı aynı koşuda almak neredeyse bedavadır.

Ölçüm ve kanıt: [`06_REPORTS/KDP_PREFLIGHT_AUDIT.md § D`](06_REPORTS/KDP_PREFLIGHT_AUDIT.md)
Mekanik takip: `qa_design § ⑨` (şimdilik **uyarı**; ② veya ① uygulanınca **hataya** yükseltilir)

---

### A16 · 300 dpi — **158 varlığın 158'i ölçütün altında**

**K39 SİLİNMEDİ ve değiştirilmedi.** `production.minDpiHistory` hem
300'ü hem 150'yi, gerekçesiyle birlikte taşıyor. Bu madde o kararı
**iptal etmiyor**; onun **sonucunu ölçüyor**.

| | |
|---|---:|
| Ölçülen varlık | **158 / 158** |
| Etkin çözünürlük **≥ 300 dpi** | **0** |
| Mevcut piksel · gereken piksel | 120,4 MP · **481,5 MP** |
| Gereken çarpan | **× 4,00** |

> ### 150 dpi bir PROJE İÇİ İNDİRİLMİŞ EŞİKTİR — KDP asgarisine uygunluk KANITI DEĞİLDİR.
>
> `qa_assets` yeşil yanıyor çünkü **ölçüt 150'ye indirildi**. Kapı kendi
> ölçütünü doğruluyor, KDP'ninkini değil.

**Kurucudan istenen karar:**

| # | Seçenek | Bedel |
|---|---|---|
| ① | 156 levhayı yeniden üret (4× piksel) | zaman + üretim |
| ② | 150 dpi'da kal · istisnayı nihai raporda **açıkça** yaz | baskı yumuşaklığı |
| ③ | Yalnızca çizgi yoğunluğu yüksek sayfaları yeniden üret | karma · ölçümle seçilir |

⛔ **Dördüncü bir seçenek yok:** piksel eklemeden DPI etiketini 300
yapmak bir düzeltme değil, bir **yanlış beyandır**. Hat bunu yapmaz.

⚠ **Kapak ve A+ bu maddenin DIŞINDADIR:** ikisi de yeni üretiliyor ve
**gerçek 300 dpi**'da üretilecek. İki eksik levha da 300 dpi'da
üretilebilir.

---

### A17 · Kurucu varlık teslimi — 16 dosya

Kapak (2 seçenek) · A+ (12 görsel) · iki eksik iç blok levhası.
Tam sözleşme, dosya adları, ölçüler ve hedefler:
[`07_ASSETS/FOUNDER_ASSET_DELIVERY.md`](07_ASSETS/FOUNDER_ASSET_DELIVERY.md)
Promptlar: `07_ASSETS/IMAGE_PROMPT_LIBRARY.html § 9`

**Ajan bekliyor.** Kurucu dosyaları koyup **DEVAM** diyene kadar Aşama 2
başlamaz.

---

### A10 · Gerçek oturum — **AÇIK · KURUCU TARAFINDAN ERTELENDİ (K27 · K30)**

A7 kapandı (testçi bulundu, K26) ve Türkçe materyal üretildi. Kalan tek
şey **oturumun kendisidir** ve onu ajan yapamaz.

**Faz 3, A10 beklenmeden başlatıldı** — kurucu talimatı. Ertelemenin
kaydı **K27**'dir. Erteleme A10'u **kapatmaz**: aşağıdaki tablo Faz 2'de
ne diyorsa bugün de aynısını diyor.

| | |
|---|---|
| Testçi | ✅ **2** (kurucu beyanı) |
| Test paketi | ✅ hazır |
| Türkçe materyal | ✅ **üretildi** · 16 sayfa |
| **Yapılan oturum** | ❌ **0** |
| `CHILD_TEST_LOG.md` | ✅ var · **0 oturum** |
| `externalValidation` | ⏳ **`pending`** |

> ### PAKET ÜRETMEK, TEST YAPMAK DEĞİLDİR.

`externalValidation` yalnızca **gerçek bir oturum**
`CHILD_TEST_LOG.md`'ye kaydedildiğinde değişir. `qa_language § ⑤` artık
bunu ayrıca **uyarıyla** hatırlatıyor: testçi onaylı ve materyal üretilmiş
ama oturum yoksa, kapı bunu her koşuda söylüyor.

Kimlikler anonimdir (`tester-01`) ve gerçek ad depoya **hiçbir koşulda**
girmez — `validate_structure.py § check_child_privacy` denetler.

### A11 · Faz 3 kapı eşiği — ✅ **KAPANDI → K29**

Kurucu **60**'ı onayladı ve 80'i *"tutarsız bir artık gereklilik"*
olarak nitelendirdi. Ayrıntı ve kök neden: **K29**.

### A12 · 148 mi 144 mü — ✅ **KAPANDI → K33**

Kurucu **144**'ü onayladı. Ayrıntı, ekonomik sonuç ve kayıt disiplini:
**K33**.

### A13 · Dizilmiş sayfa **160**, onaylı hedef **144** — **YENİ · AÇIK**

Faz 6 gerçek dizgi motorunu (`interior.py`) kurdu ve sayfa sayısını beş
fazda ilk kez **ölçtü**. Sonuç modeli yalanlıyor:

```
MODEL   (page_budget · pageWeight toplamı)   144
ÖLÇÜM   (interior · dizilmiş PDF)            160     ← +16
HEDEF   (K33 · kurucu)                       144
```

**Kök neden ölçüldü.** `pageWeight` Faz 1'de **tipe göre** atanmıştı:
`cipher`/`sort` → 0,75 · `map`/`observe`/`make` → 1,0. 0,75 ağırlık
*"iki hafif sayfa bir sayfayı paylaşır"* demektir. Ölçüm bunu yalanlıyor:

| Ağırlık | Sayfa | Gerçek dikey ihtiyaç (ort.) |
|---|---:|---:|
| 1,00 | 56 | **8,01"** |
| 0,75 | 64 | **8,57"** ← *daha AĞIR* |

Kullanılabilir yükseklik **10,00"**. İki 0,75 sayfasının paylaşması için
her birinin **≤ 5,00"** olması gerekir: **64 sayfanın 0'ı sığıyor.**

> **`cipher` ve `sort` sayfaları hafif değildir.** Anahtar paneli, kart
> bankası ve daha çok yazma satırı taşırlar. 0,75 ölçülmedi, **atandı**.

Ve `DESIGN_SYSTEM § 1.1` zaten sayfa başına **tek** modül yığını
tanımlıyor — paylaşım, dizgenin kendisiyle de çelişiyordu.

| Seçenek | Sonuç |
|---|---|
| **160 kabul edilir** | telif **5,27 $** (−0,28 $) · başabaş ACOS %35,2 · içerik değişmez |
| 144'e indirilir | **16 sayfa çıkar** = ~16 aktivite → alt başlıktaki **120 vaadi düşer** |
| Düzen sıkılaştırılır | levha yüksekliği ve yazma satırı kısılır → **ürünün işlevi** bozulur |

**Ajan hiçbirini seçmedi.** Sayfa kısılmadı, hedef sessizce değişmedi.

### A14 · 156 ham görsel hedefin **altında** — **YENİ · AÇIK**

Kurucu 158 ham görseli teslim etti. Ölçüm:

```
teslim edilen         156 dosya   (beklenen 158 · 2 EKSİK)
çözünürlük            156/156'sı 1,57 MP — hepsi AYNI
aktivite hedefini karşılayan   0 / 156
```

En küçük aktivite hedefi **2100×1200 = 2,52 MP**. Hiçbir dosya
karşılamıyor. Zorlanırsa efektif çözünürlük **166–202 dpi** olur;
şartname **300 dpi** diyor (`visualSpec.minDpi`).

| Sınıf | Adet | 300 dpi'da üretilebilir mi |
|---|---:|---|
| kültür vinyeti (1350×900) | 22 | ✅ |
| mühür damgası (900×900) | 6 | ✅ |
| rozet (600×600) | 6 | ✅ |
| **aktivite levhası** | **120** | ❌ |
| **ön madde diyagramı** | **4** | ❌ |

**Ve ikinci bir engel:** dosya adları `001.png`–`156.png`; envanterin
beklediği `assetId` adlarıyla **hiçbiri eşleşmiyor** (0/158) ve dosyalar
manifest sırasında **değil** (ölçüldü: `001` Inuktitut hecelemesi,
manifest #1 Maya sayıları; `121` Irish vinyeti, manifest #121 Finnish).

> ### Bir eşleme TAHMİN EDİLEMEZ. Yanlış aktiviteye bağlanmış kusursuz bir görsel, o sayfayı ÇÖZÜLEMEZ yapar.

`asset_pipeline.py` yukarı örneklemeyi **reddeder** (K35) ve bu bilinçli:
büyütmek çözünürlük kazandırmaz, yalnızca 300 dpi iddiasını yalan hâline
getirir.

| Seçenek | Sonuç |
|---|---|
| **124 görsel yeniden üretilir** | hedef ölçüde · hat hazır · envanter deterministik |
| 300 dpi ölçütü düşürülür | **kurucu kararı** · dayanağı kayda geçer (A12 gibi) |
| Yalnızca 34 üretilebilir | vinyet + damga + rozet basılır, aktivite levhaları **boş kalır** |

### A9 · Fizikî prova — KURUCUYA AİT · **YENİ**

Fizikî prova (POD baskı örneği) siparişi, teslim alınması ve
değerlendirilmesi **kurucunun işidir**. Ajan:

- prova **sipariş etmez**
- prova yapıldığını **iddia etmez**
- prova geri bildirimi **uydurmaz**
- POD doğrulaması **uydurmaz**

Ajan prova gerektirmeyen bütün teknik işi sürdürür ve yol haritasının
istediği yerde prova hazır dosyalarını, kontrol listesini ve kurucu devir
bilgisini üretir.

**Durum: KURUCU EYLEMİ / BEKLİYOR.** Kurucu tamamlandığını bildirene
kadar bu satır değişmez.

---

## ALINMIŞ KARARLAR

### K1 · Ortak kütüphane YOK — üç proje tam izole
**12 Ağustos 2026 · bootstrap.** Talimat § 31 bir ajanın tek klasörle
çalışabilmesini şart koşuyor. Paylaşılan bir dosyadaki değişiklik üç projeyi
birden kırar. **Kopyalanan kod biraz fazlalıktır; bağımlılık bir kırılganlıktır.**

### K2 · Faz kapısı `.gate` dosyasından okunur
Kapı tahmin edilmez. `--fix` kapıya dokunmaz (Bestiarium dersi).

### K3 · Tek format: ciltsiz
Aktivite kitabı **üzerine yazılır**. Kindle üretilmez — e-okuyucuda
çalışmaz ve kötü yorum üretir. Bu bir gelir kaybı değil, **itibar korumasıdır**.
Ciltli hediye sürümü A5 kararına bağlıdır.

### K4 · Bulmaca içerikten türer, süslenmez
Dekoratif tema **yasaktır**. Bir aktivite "hangi mitolojik bilgiyi öğretiyor"
sorusuna cevap veremiyorsa kitaba girmez. Bu, kitabın rakiplerinden ayrıldığı
tek yerdir ve bir üslup kuralı değil bir **kapsam kuralıdır**.

### K5 · Yaş politikası World Myths'ten KOPYALANMAZ, yeniden yazılır
Orada risk *okunan şiddetti*; burada risk **yapılan görev**. Çocuk artık
yazıyor, çiziyor, çözüyor. Altı yasak çerçeve
[`00_CONTEXT/AGE_POLICY.md`](00_CONTEXT/AGE_POLICY.md)'de tanımlıdır.

### K6 · Devralma = kopyalama + köken kaydı, canlı bağımlılık DEĞİL
World Myths deposunun kardeş dizinde bulunması **zorunlu değildir**.
Bu proje onsuz build alır, test edilir ve CI'ı yeşil yanar.
`--cross-check` yalnızca depo **varsa** çalışır ve yoksa **atlar**.

### K7 · Kalite kapıları üçüncü taraf paket kullanmaz
`validate.yml` saniyeler içinde biter. Ağır bağımlılıklar yalnızca görsel
ve dizgi işlerine aittir (`run_optional`).

### K8 · Kapsam sayıları Faz 1'e kadar HİPOTEZDİR
`scope.locked: false`. Faz 1 doğrular veya değiştirir.

### K9 · Doğrulanmamış devralma LOCKED OLAMAZ
**Bu projenin bel kemiği.** `inherited-provisional` bir kayda dayanan hiçbir
aktivite `locked` olamaz, dolayısıyla yazılamaz.

İki ayrı kapı denetler (`validate_spec.py` ve `validate_inheritance.py`) ve
`selftest.py` sözleşmenin **gevşetilmesini** de yakalar. Tek bir kapının
unutulması sistemi açmaz.

### K10 · Cevap anahtarı ve çocuk kimliği public depoya giremez
Cevaplar **ürünün kendisidir**; public depoda duran cevap ürünü değersizleştirir.
Çocuk testçi adları hiçbir koşulda depoya girmez.
`validate_structure.py` her ikisini de içerik taramasıyla denetler.

---

## FAZ 1 KARARLARI — 13 Ağustos 2026

### K11 · Manuscript public depoda DURMAZ (A1 kapandı)
**Bootstrap varsayımı onaylandı.** `.gitignore § ①` manuscript prozasını,
cevap anahtarını ve çocuk testçi kayıtlarını dışlar; `validate_structure.py`
ikinci hat olarak takip edilen dosyaların **içeriğine** bakar.

Public kalan: kod · CI · şema · doğrulayıcı · **devralma manifestosu** ·
belgeler · araştırma künyeleri · **ölçüm raporları**.

Sonuç: mühür sözcükleri (`01_SOURCE/answers/`) ve pilot prozası
(`02_MANUSCRIPT/pilot/`) depoda **yoktur**; raporlar yalnızca **sayı** taşır.

### K12 · Devralma politikası (a) — kopyala + sha256 + kullanıma göre doğrula (A2 kapandı)
Kurucunun *"START PHASE 1"* talimatı bootstrap varsayımını onayladı.

Devralma bir **kopyalama + köken kaydıdır**, canlı bağımlılık değil.
World Myths deposu kardeş dizinde bulunmak **zorunda değildir**: bu proje
onsuz build alır, test edilir ve CI'ı yeşil yanar. Depo **varsa**
`--cross-check` sha256'ları karşılaştırır ve sürüklenmeyi bildirir.

Şık (c) — *"devralınanı doğrulanmış say"* — **reddedildi**. Seçilseydi
`selftest § ②(i)` gevşetmeyi yakalayıp CI'ı kırmızı yakacaktı; yani karar
zaten sessizce alınamazdı.

### K13 · Kültür düşürülmez, BİÇİM daralır
`22` alt başlıkta yazan **doğrulanabilir bir vaattir**. Kısıt bulunduğunda
daralma sırası: **yasak biçim → izinli tip → kota → hikâye → (son çare) kültür**.

Faz 1'de ilk dördü kullanıldı, sonuncusu **hiç** kullanılmadı: iki hikâye
aktivite dışı bırakıldı (`egyptian-horus-seth` · `hindu-ganesha-head`),
yirmi hikâyede kapalı katman işaretlendi, dört kültür Kademe C'ye alındı.
**22 kültürün hepsi kitapta.**

Ayrıntı: [`00_CONTEXT/CULTURE_POLICY.md`](00_CONTEXT/CULTURE_POLICY.md)

### K14 · Güvenlik sınıfı HESAPLANIR, beyan edilmez
Bir insan *"bence bu güvenli"* diyemez. `safetyClass` malzemeden,
yasak çerçeveden ve kısıt durumundan **türetilir**
([`AGE_POLICY.md § 3.2`](00_CONTEXT/AGE_POLICY.md)) ve `qa_age.py`
beyan ile hesabı karşılaştırır.

**Kapı kapalı yönde arızalanır:** beyaz listede olmayan bir malzeme
`safe` sayılmaz, `do-not-use` olur. *"Bilmiyorum"* güvenli değildir.

`selftest § ⑤(k)` belgeyi, kodu ve şemayı **birbirine bağlar**: üçü
ayrıldığı an CI kırmızı yanar.

### K15 · Bölgeler kıtaya göre değil ARAZİYE göre kurulur
Bir saha defteri iklimi izler, siyasî sınırları değil — ve bu pedagojik
bir tercihtir: çocuk coğrafyanın hikâyeyi biçimlendirdiğini görür.

Bölge kotaları **eşit değildir** ve bu bilinçlidir: kota, o bölgenin
kullanılabilir hikâye arzıyla orantılıdır. Eşit dağıtım beş hikâyeli bir
bölgeden yirmi aktivite çıkarmayı zorlar ve bu **tekrar üretir**.

### K16 · Okunabilirlik bandı metne değil REGİSTERE bağlanır
Faz 1 pilotu bootstrap'ın tek bandının (9–14 kelime · 3.–5. sınıf)
bu kitapta **yanlış** olduğunu ölçtü. O bant World Myths'in **anlatı**
prozasından geliyordu.

> **Bir talimat bir anlatı cümlesi değildir.**

Üç register ayrı ölçülür (talimat · field note · ipucu) ve bir **değişmez**
eklenir: `fk(talimat) < fk(field note)` — bir talimat, tanıttığı içerikten
daha zor olamaz.

Ölçüm ve bantlar: [`00_CONTEXT/STYLE.md § 3`](00_CONTEXT/STYLE.md)

### K17 · Üretilen belgeler elle yazılmaz — *(K18–K25 için § FAZ 2 KARARLARI)*
`BOOK_STATS.md` ve `ROADMAP_PROGRESS.md` `04_BUILD/update_docs.py`
tarafından **üretilir** ve `--check` bayrağıyla bayatlıkları denetlenir.

Gerekçe: elle yazılan bir sayı bir süre sonra sessizce yanlış olur ve
kimse fark etmez — çünkü onu kimse denetlemez. İki belge de bootstrap'ta
zaten *"hiçbiri elle yazılmayacaktır"* diye söz vermişti.

---

## FAZ 2 KARARLARI — 13 Ağustos 2026

### K18 · Altı bölge ve 37 mühür yuvası KİLİTLİ (A3 kapandı)

**Kurucu onayladı.** Faz 1'in araziye göre kurduğu altı bölge ve 37 yuvalık
mühür mimarisi artık **dondurulmuştur**:

```
1. The Northern Ice      4 kültür · 24 aktivite · 5 harf
2. The Middle Sea        3 kültür · 20 aktivite · 6 harf
3. Sun and Savanna       3 kültür · 16 aktivite · 7 harf
4. Mountain and Monsoon  5 kültür · 24 aktivite · 7 harf
5. The Great Ocean       4 kültür · 20 aktivite · 6 harf
6. Jaguar and Condor     3 kültür · 16 aktivite · 6 harf
                                    ─────────────────────
                                    120 aktivite · 37 yuva
```

Bootstrap'ın bölge modeline **dönülmez**. Mühür mekaniği
(`sealSlot` → tek harf → bölge sözcüğü → çentik → final sözcük) Faz 1
biçiminde kalır.

Değişiklik bundan sonra **yeni bir kurucu kararı** gerektirir ve
`qa_matrix.py § ④` ile `qa_progression.py` mimariyi her koşuda denetler.

### K19 · 148 sayfa kabul edildi, telif düşüşü bilinerek üstlenildi (A8 kapandı)

**Kurucu (a) şıkkını seçti.** Planlama hedefi artık **148 sayfadır**.

| | Bootstrap hipotezi | Kabul edilen model |
|---|---:|---:|
| Sayfa | 144 | **148** |
| Baskı maliyeti | 3,45 $ | **3,52 $** |
| Ciltsiz telif | 5,55 $ | **5,48 $** |
| Başabaş ACOS | %37,0 | **%36,5** |

`project_config.json § scope.pageTarget` **148**'e çekildi ve
`BRIEF.md § 7` güncellendi — böylece iki belge aynı sayıyı söylüyor ve
`page_budget.py`'nin sapma uyarısı **sustu**.

> **Uyarının susması bir kayıp değil bir kazançtır.** Faz 1'de o uyarı
> gerçek bir açık kararı gösteriyordu. Karar kapandı; uyarı da kapanmalı.
> Kalıcı bir uyarı bir süre sonra **görülmez** olur ve kapı körleşir.

Karar **yeniden açılmaz.** 0,07 $ geri kazanmak için içerik kısılmaz.
Sayfa modeli gerçek içerikle **ölçülmeye devam eder**; anlamlı bir sapma
çıkarsa raporlanır, sessizce yutulmaz.

### K20 · Pilot bölgesi HESAPLANIR, seçilmez

Faz 1 raporu en zor bölge için iki aday önerdi: `sun-savanna` **veya**
`jaguar-condor`. Faz 2 bunu bir sezgi olarak bırakmadı ve
`04_BUILD/region_difficulty.py` ile **ölçtü** — çünkü bu projede
`safetyClass` hesaplanıyorsa (K14) pilot bölgesi de hesaplanabilir.

Yedi eksen, ikisi bölgeye ait: yazı dizgesi yabancılığı · kademe ağırlığı ·
yasak biçim sayısı · yaşayan gelenek · hikâye arzı · mühür yükü ·
yetkisiz kaynak riski.

**Ölçüm iki şeyi düzeltti.**

**① Tek skor büyüklüğü zorluk sanıyordu.** İlk koşu `monsoon`'u birinci
gösterdi — ama `monsoon`'un beş kültürü var ve toplanan her eksen kültür
sayısıyla mekanik olarak büyüyor. İki skor ayrıldı:

```
burden    = toplam üretim yükü       →  monsoon 87,68 (en yüksek)
intensity = kültür başına sertlik    →  jaguar-condor 31,17 (en yüksek)
```

Pilot **yoğunlukla** seçilir; yol haritasının ölçütü *"kısıt taraması en
YOĞUN, şifre sistemi en YABANCI"* der ve yoğunluk bir orandır.

**② `sun-savanna` en zor değil, EN KOLAY bölge.** Yoğunluk 14,37 ile
altıncı sırada. Sebep ölçülebilir: üç yazı dizgesinin **üçü de Latin
harflidir** (Akan gün-adları · Yoruba imlâsı · isiZulu şıklamaları), yani
yabancılık 15 üzerinden **1**. Faz 1 "üç yaşayan gelenek" ile "yabancı
şifre dizgesi"ni aynı şey sanmıştı; değiller.

**Seçilen pilot: `jaguar-condor`** — yoğunluk 31,17, ikinciyle fark 8,55.
Üç kültürün üçü de Kademe B (kutsal katman cevap olamaz) ve üç yazı
dizgesinin **üçü de alfabetik değil**: Maya çubuk-nokta, Nahuatl yer adı
glifleri, khipu düğümü. Çocuğun tanıdığı hiçbir işaret yok.

> `monsoon` pilot değildir ama **sona bırakılamaz**: en yüksek toplam yükü
> o taşıyor ve yük kültür sayısıyla birlikte geliyor. Üretim planlaması
> bunu Faz 3'te dikkate alır.

### K21 · Ticari dil İNGİLİZCE; Türkçe yalnızca geçici TEST dilidir

Kurucu talimatı açık: nihai ticari ürünün **tamamı İngilizcedir** —
manuscript, talimatlar, field note'lar, ipuçları, mühür metinleri, arka
madde, kapak, A+ içerik, metadata, KDP paketi.

Türkçe **yalnızca** gerçek Türkçe konuşan çocuk testçiler bulunduğunda,
**geçici tester-facing materyal** için kullanılabilir. O materyal:

- ticari değildir
- kanonik manuscript değildir
- nihai çıktıya **giremez**
- makine çevirisiyle İngilizceye dönüştürülmez

Test bulguları İngilizce ticari sürüme **yeniden yazılarak** taşınır ve
İngilizce sürüm ilgili kapılardan **bağımsız olarak** geçmek zorundadır.

> **Türkçe pilotun geçmesi İngilizce sürümün geçtiği anlamına GELMEZ.**

Bu kural disipline değil **mekanizmaya** bağlandı: `04_BUILD/qa_language.py`
ticari katmanda Türkçe imza arar ve bulursa CI'ı kırmızı yakar.
`04_BUILD/child_test_pack.py` ise `founder.childTesters.founderConfirmed`
`false` iken Türkçe materyal üretmeyi **reddeder** — yani testçi yokken
test materyali de olamaz.

**Proje belgeleri (bu dosya dahil) Türkçedir ve öyle kalır.** Belge dili
ile ürün dili aynı şey değildir; `project_config.json` ikisini ayrı
alanlarda taşır (`language: en` · `documentLanguage: tr`).

### K22 · Doğrulama KAYIT düzeyinde değil İDDİA düzeyinde yapılır

Faz 1'in sözleşmesi `inheritanceStatus` üzerineydi ve **kayıt**
düzeyindeydi. Faz 2 bunun yetersiz olduğunu gösterdi:

> Bir kültür kaydının otuz alanı vardır ve bir aktivite onun ikisini
> kullanır. *"culture-maya doğrulandı"* cümlesi **hangi alanın**
> doğrulandığını söylemez.
>
> **Kaydı `inherited-verified` yapmak bir BEYANDIR.
> İddiayı bir kaynağa bağlamak bir KANITTIR.**

Şema **v2.1** `claimRefs` alanını aldı; `01_SOURCE/research/*-revalidation.json`
her iddiayı tek tek taşıyor (hangi sayfada, nerede kullanılıyor, hangi
kaynakla karşılaştırıldı, sonuç ne); `validate_research § ⑩` zinciri
denetliyor ve **cevap üreten her iddia için ≥2 bağımsız kaynak** şart
koşuyor.

Bu sözleşme Faz 2'de **üç yanlış iddia** buldu — üçü de anlatı için
yeterli, aktivite için yanlış cümlelerdi.

### K23 · `.gate` teknik başarıyla yükselmez

Faz 2'nin teknik pilotu geçti: 16 sayfa, on üç kapı yeşil, mühür uçtan
uca doğrulandı. **`.gate` yine de `phase1`'de bırakıldı.**

Gerekçe: `phase2` kapısının PASS ölçütü *"çocuk testinde ≥%80 yardımsız
anlaşılma"* ve **0 testçi** var.

```
TEKNİK PİLOT            ✅ GEÇTİ
DIŞ ÇOCUK DOĞRULAMASI   ⏳ BEKLİYOR
        bu ikisi TOPLANMAZ
```

> **Kapıyı yükseltmek, yapılmamış bir testi geçmiş saymaktır.**

Kapı yalnızca gerçek bir çocuk oturumundan sonra `phase2` olur. Aynı
gerekçeyle `STYLE.md` **v1.2**'de kaldı: v2.0 numarası yol haritasında
*"çocuk testiyle kalibre"* diye tanımlı ve o numara ilk gerçek oturuma
ayrılmıştır.

### K24 · Bir yanlış cevap çocuğu kitaptan kilitleyemez

Kurucu talimatının § 23'ü: *"Bir hata GERİ BİLDİRİM olmalıdır, TOPLAM
BAŞARISIZLIK değil."* Faz 2 bunu üç bağımsız mekanizmaya bağladı ve
**mekanik olarak kanıtladı**:

| Mekanizma | Ölçülen |
|---|---|
| **Hasar yarıçapı 1** — bir yuvayı tam bir aktivite besler | ✅ `qa_progression § ⑥` |
| **Zincir yok** — hiçbir sayfa başka bir sayfanın cevabına bağlı değil | ✅ `qa_progression § ⑤` |
| **Sözcük anlamlı** — yanlış harf sözcüğü bozar ve çocuk hangi sayfaya döneceğini bilir | ✅ `qa_progression § ⑦` |

Ve ölçülen bir bonus: **37 mühür harfinin yalnızca 6'sı** (%16,2) final
göreve taşınıyor. Bir bölgede yapılan hata, o harf çentik konumunda
değilse final cevabı **hiç etkilemiyor**.

`selftest § ⑬` her üçü için de kusur taşıyan kurgu koşturuyor.

### K25 · Görsel metnin İHTİYACINDAN türer, tersi değil

İç editoryal inceleme şunu gösterdi: on üç kapı yeşilken 16 sayfanın
**11'i çözülemezdi**, ve sebeplerin çoğu görseldeydi.

```
"Colour them the way the key shows."   → sayfada anahtar YOK
"Read the four cards beside the cord." → sayfada ip YOK
"Put each one in the right column."    → sütun başlıkları YOK
```

Dördü de kusursuz İngilizce, dördü de okunabilirlik bandında, dördü de
bir çocuğu durdurur.

> **Bir talimat "the X" derse, levha X'i basmak ZORUNDADIR.**

Manuscript şemasına `pagePrints` alanı eklendi: *sayfanın çözülebilmesi
için levhanın basması gereken her şey*. Pilotun 16 sayfası için **67
madde**. Alan iki iş birden yapıyor — bugün `qa_instruction § ⑨`'un
girdisi, Faz 5'te görsel şartnamesinin kendisi.

⚠ Şartnamelerin **metni** depoya girmez: içerikleri cevabın kendisidir
(K10). `02_MANUSCRIPT/book.json` içinde durur.

### K26 · A7 kapandı — testçi bulundu, Türkçe materyal üretildi

**13 Ağustos 2026 · kurucu beyanı: en az iki Türkçe konuşan çocuk testçi
bulundu.** `founder.childTesters.founderConfirmed` **true**,
`availableTesters` **2**.

Bu onay `child_test_pack.py`'nin reddetme kapısını açtı ve Türkçe
tester-facing materyal üretildi: **16 sayfa**, veli notu ve boş kayıt
formu → `01_SOURCE/pilot_tr/`.

**Onayın AÇMADIĞI şey:** `externalValidation` hâlâ `pending`.

```
TESTÇİ BULUNDU        ✅   → materyal üretilebilir
MATERYAL ÜRETİLDİ     ✅   → oturum koşturulabilir
OTURUM YAPILDI        ❌   → dış doğrulama BEKLİYOR
```

#### Türkçe mühür sözcüğü KATMAN — ve neden CONDOR değil

Ticari bölge mührü **CONDOR**'dur ve öyle kalır. Ama Türkçe sayfalarda
yıldızlı sözcükler Türkçedir (*kakao · ahuejote · nochtli · hamur ·
patates · tane*) ve harfleri CONDOR'u kurmaz.

Zorlamanın iki yolu vardı ve ikisi de kötüydü:

| Şık | Sonuç |
|---|---|
| Türkçe sayfaya İngilizce sözcük koymak | **dilleri karıştırır** — K21 ihlali |
| Mührü anlamsız bir harf dizisi yapmak | **testin kendisini yok eder** |

İkincisi kritiktir: mühür mekaniğinin en önemli özelliği sözcüğün
**anlamlı** olmasıdır — çocuk sözcüğü kurunca doğru çözdüğünü **kendi
anlar**. Anlamsız bir dizi bunu yapamaz, ve tam da bu özellik test
edilmek isteniyor.

Bu yüzden Türkçe pilot kendi mühür sözcüğünü taşır: **KATMAN**. Tematik
olarak da doğru — chinampa katman katman kurulur, And kuşakları da birer
katmandır.

> **Test edilen şey sözcük değil MEKANİKTİR:**
> yıldızlı kutu → sayılan harf → yuva → anlamlı sözcük → kendini doğrulama

Ticari CONDOR mührü etkilenmez: `qa_progression` yalnızca `book.json`'u
okur ve Türkçe kaynağı hiç görmez.

#### İzolasyon — üç hat

| Hat | Ne yapar |
|---|---|
| `.gitignore § ①d` | `01_SOURCE/pilot_tr/` depoya **girmez** |
| `qa_language § ④` | TEST-ONLY etiketli materyal test dizini dışında görülürse **kırmızı** |
| `child_test_pack.py` | onay **veya** kaynak yoksa üretmeyi **reddeder** (çıkış 3) |

Üçüncü hat Faz 2'de bir kusur da düzeltti: betiğin ilk hâli reddetme
kapısını taşıyordu ama kapı **açıldığında** ne olacağı yazılmamıştı —
İngilizce prozayı basıp üstüne `tr` etiketi yapıştıracaktı.

> **Bir dosyanın adında `tr` yazması, içindekini Türkçe yapmaz.**

Türkçe materyal ayrı bir kaynak olarak **yazıldı**
(`01_SOURCE/pilot_tr/source-tr.json`), çevrilmedi. `selftest § ⑪b` üç
yolu da kanıtlıyor: onaysız **ret**, kaynaksız **ret**, ikisi varsa üretim.

---

## FAZ 3 KARARLARI — 13 Ağustos 2026

### K27 · Faz 3, A10 beklenmeden başlatıldı — **AŞMA KAYITLIDIR, GİZLİ DEĞİLDİR**

**Kurucu talimatı:** *"Test aşamasını atlayıp tasarım (Faz 3) aşamasına
geç."*

Bu meşru bir kurucu kararıdır ve uygulandı. Ama iki şey **birbirine
karıştırılamaz** ve bu karar tam olarak o ayrımı korumak için var:

```
FAZ 3 BAŞLATMA YETKİSİ    ✅ VERİLDİ      (kurucu)
A10 ÇOCUK OTURUMU         ❌ YAPILMADI    (0 oturum)

Birincisi ikincisini KAPATMAZ.
```

| | |
|---|---|
| Aşmayı veren | kurucu · 13 Ağustos 2026 |
| Yetkilendirilen | **Faz 3** — tasarım, ölçekleme, üretim |
| Ertelenen blokaj | **A10** — gerçek çocuk oturumu |
| A10 durumu | **AÇIK · YAPILMADI** — değişmedi |
| `externalValidation` | ⏳ **`pending`** — değişmedi |
| `.gate` | **`phase1`** — **YÜKSELTİLMEDİ** |
| `STYLE.md` | **v1.2** — v2.0 hâlâ ilk gerçek oturuma ayrılmış |

#### Neden `.gate` yükseltilmedi

Kurucu talimatı § 4 bunu ayrıca şart koşuyor: kapı **depo temiz görünsün
diye** yükseltilmez. `phase2` kapısının PASS ölçütü *"çocuk testinde
≥%80 yardımsız anlaşılma"* ve **0 oturum** var. K23 bu gerekçeyle
yazıldı ve **hâlâ geçerlidir**.

> **Bir aşma, bir sonucu üretmez. Yalnızca bir SIRAYI değiştirir.**

#### Aşma bir KİLİDE çevrildi

Bir aşmanın gerçek tehlikesi karar değil, kararın **unutulmasıdır**:
altı ay sonra depoyu açan bir ajan Faz 3 içeriğini görür ve Faz 2'nin
kapandığını **sanar**. Bu yüzden aşma yalnızca yazılmadı, **kodlandı**:

`project_config § founder.phaseOverride` + `validate_spec § ⑤`

| Kilit | Ne yapar |
|---|---|
| `.gate ≤ gateCeiling` | kapı aşmayla **yükseltilemez** |
| `externalValidation ≠ passed` | aşma bir testi **geçmiş saydıramaz** |
| `deferredBlockerStatus ≠ closed` | A10 **kapanmış görünemez** |
| `documentedIn` taraması | belgede **anılmayan** aşma kırmızı yanar |

Sonuncusu bir liste denetimi değildir: kapı o dosyaları **açar** ve
içlerinde `K27` ya da `A10` geçtiğini arar. Belgeden düşen bir aşma,
CI'ı kırmızı yakar.

`selftest § ⑭` dört kilidin dördünü de kusurlu kurguyla sınar.

#### Bu kararın ÜRETMEDİĞİ cümleler

- ~~"kitap çocuklarla test edildi"~~
- ~~"Faz 2 kapandı"~~
- ~~"A10 karşılandı"~~
- ~~"dış doğrulama geçti"~~

Kurucu gerçek bir oturum bildirdiğinde A10 normal yoldan kapanır ve
`externalValidation` o zaman değişir — **aşmayla değil, veriyle**.

### K28 · Faz 3 bölgeleri YÜKLE seçilir — `monsoon` + `great-ocean`

Yol haritası Faz 3'ü *"Bölge bloğu I — üç bölge · 60 aktivite (pilot
dâhil)"* diye tanımlıyor. Kurucu talimatı § 11 sırayı **ölçüme**
bağlıyor: *"measurable production burden and research readiness"*, ve
§ 9 `monsoon`'un **erken** planlanmasını şart koşuyor.

`region_difficulty.py` yükü zaten ölçmüştü (K20). Sıralama:

| Bölge | YÜK | Kota | Durum |
|---|---:|---:|---|
| ~~jaguar-condor~~ | 82,17 | 16 | ✅ Faz 2 pilotu |
| **monsoon** | **87,68** | **24** | ⭑ Faz 3 |
| **great-ocean** | **75,50** | **20** | ⭑ Faz 3 |
| north-ice | 58,50 | 24 | Faz 4 |
| middle-sea | 52,00 | 20 | Faz 4 |
| sun-savanna | 29,70 | 16 | Faz 4 |

**Yazılmamış iki en ağır bölge Faz 3'e alındı.** `monsoon` en yüksek
toplam yükü taşıyor (5 kültür) ve Faz 2 raporu onu açıkça *"sona
bırakılamaz"* diye işaretlemişti.

#### Ve sayı KENDİLİĞİNDEN oturuyor

A3 kotaları (K18) bölgeler arasında eşit değildir, yani "üç bölge"
otomatik olarak 60 etmez. Bu seçimde ediyor:

```
jaguar-condor 16  +  monsoon 24  +  great-ocean 20  =  60   ✅ yol haritası Faz 3
north-ice     24  +  middle-sea 20  +  sun-savanna 16  =  60   ✅ yol haritası Faz 4
                                                        ───
                                                        120
```

Yol haritasının *"Faz 3 → 60 kümülatif"* ve *"Faz 4 → 60 yeni,
kümülatif 120"* cümleleri, **yük sıralamasıyla birebir uyuşuyor**.
Sayı uydurulmadı; iki bağımsız kısıt aynı bölünmeyi verdi.

**Faz 3'te yazılacak yeni sayfa: 44.**

#### Ölçülen bir çelişki — kurucuya not

`project_config § gates.requirements.phase3` **80** kilitli aktivite
istiyor. Yol haritası **60** diyor. İkisi aynı anda doğru olamaz.

Sayı **değiştirilmedi**: yol haritası *"tek doğruluk kaynağıdır"* ve
kapsam sayıları bir **kurucu kararıdır** (K8 · `scope.locked`). 80
büyük olasılıkla bootstrap'ın "6 bölge × 20" varsayımından kalma bir
artıktır ama bunu ajan **varsayamaz**.

Bugün ısırmıyor — `.gate` `phase1` ve orada kalıyor (K27). Kapıyı
`phase3`'e yükseltmek istendiğinde **ısıracak** ve o an bir karar
gerekecek. Açık kalem: **A11**.

> **Sonuç (14 Ağustos 2026):** kurucu **60**'ı onayladı. Çelişki
> kapandı ve bir daha açılamayacak biçimde **mekanikleştirildi** →
> **K29**.

---

### K29 · A11 kapandı — Faz 3 eşiği **60** · ve eşikler artık TÜRETİLİYOR

**14 Ağustos 2026 · Faz 4 · KURUCU KARARI.**

Kurucu talimatı § 2:

> *"The Phase 3 gate requirement must be treated as **60 locked
> activities**, NOT 80. The previous 80-activity requirement was
> identified as an **inconsistent leftover requirement**."*

#### Değişen sayı

| Kapı | Alan | **ESKİ** | **YENİ** | Kaynak |
|---|---|---:|---:|---|
| `phase3` | `activitiesLocked` | **80** | **60** | ⭑ kurucu onayı |
| `phase3` | `activitiesWritten` | **80** | **60** | ⭑ kurucu onayı |
| `phase2` | `activitiesLocked` | 20 | **16** | türetme sonucu |
| `phase2` | `activitiesWritten` | 20 | **16** | türetme sonucu |
| `phase4` | her ikisi | 120 | 120 | değişmedi |

**Eski değerler silinmedi**, `project_config § gates.requirementsHistory`
içinde makine okunur biçimde duruyor ve `validate_spec § ⑥(g)` kaydın
silinmesini **kırmızı yakıyor**.

#### Kök neden — 80 bir hata değil, bir ARTIKTI

Merdivenin tamamı bootstrap'ın **"6 bölge × 20 aktivite"** varsayımından
elle türetilmişti: `20 · 40 · 60 · 80 · 100 · 120`. Faz 1 o varsayımı
yıktı ve kotaları **arza göre eşitsiz** kurdu (**K18**):

```
16 · 20 · 24 · 24 · 20 · 16  =  120
```

Eşitsiz kotalarla *"üç bölge"* otomatik olarak 60 etmez. O günden sonra
merdivenin her basamağı bir **tahmindi** ve iki basamağı yanlıştı:
`phase3` 80 yerine 60, `phase2` 20 yerine 16.

> ### Bir düzeltme, düzelttiği kusurun TEKRARINI engellemiyorsa bir düzeltme değil bir ERTELEMEDİR.

80'i elle 60 yapmak bugünkü çelişkiyi kapatırdı ve **yarınkini
kapatmazdı**. Bu yüzden eşik artık okunmuyor, **türetiliyor**:

```
gates.productionPlan[faz]  ×  scope.regionsHypothesis[].activityQuota
        →  kümülatif toplam  ==  gates.requirements[faz].activitiesLocked
```

`project_config`'teki sayılar artık bir **kopyadır**. Kopya sürüklenirse
`validate_spec § ⑥` kırmızı yanar ve **hangi basamağın hangi yönde**
sürüklendiğini söyler.

#### phase2 · 20 → 16 — kurucunun sorusunda ADI GEÇMEDİ

Bu şeffaflık gerektiriyor. Kurucu **phase3**'ü sordu ve **phase3**'ü
yanıtladı. `phase2` aynı artığın bir basamak aşağısıdır ve türetme onu
kaçınılmaz olarak yakaladı: pilot bölgesi `jaguar-condor`'un kotası
**16**'dır (K18) ve Faz 2 gerçekten 16 sayfa yazdı.

Eski 20, Faz 2 tamamlandığı gün kapıyı **yanlış yere** kırmızı
yakardı — yani bir *yanlış-kırmızı*ydı. Yanlış-kırmızı, yanlış-yeşil
kadar zarar verir: kapıya olan güveni bitirir.

Değişiklik **gizlenmiyor**: burada, `requirementsHistory` içinde ve
`PHASE_4_REPORT § 2`'de açıkça duruyor, `founderApproved: ["phase3"]`
ile `derivedConsequence: ["phase2"]` alanları **ayrı** tutuluyor ve bir
kurucu talimatıyla **geri alınabilir**.

#### Kanıt — `selftest § ⑰` sekiz kusurlu kurgu koşturuyor

| Kurgu | Beklenen |
|---|---|
| **eski 80 geri yazılır** | ⭑ **KIRMIZI** |
| eski 20 geri yazılır | ⭑ KIRMIZI |
| bir bölge iki fazda üretilir | KIRMIZI |
| bir bölge hiç planlanmaz | KIRMIZI |
| **kota değişir, eşik değişmez** | ⭑ KIRMIZI |
| eşik geri gider (phase5 < phase4) | KIRMIZI |
| tarihî kayıt silinir / ESKİ değer düşürülür | KIRMIZI |
| üretim planı silinir | KIRMIZI |
| **temiz türetilmiş config** | **YEŞİL** |

Beşincisi denetimin asıl işidir: mimari kayarsa kapı da kayar,
**sessizce ayrılmazlar**.

#### Ne DEĞİŞMEDİ

- `scope.activities` = **120** · `scope.cultures` = **22** — alt başlığın
  vaadi
- Bölge kotaları (**K18** · A3) — bir tanesine bile dokunulmadı
- `.gate` — hâlâ `phase1`, K27/K30 tavanı orada tutuyor
- 37 mühür yuvası mimarisi

---

### K30 · Kurucu aşması Faz 4'e genişletildi — **tavan değişmedi**

**14 Ağustos 2026 · KURUCU KARARI.**

Kurucu talimatı § 3:

> *"CONTINUE PHASE 4 USING THE 60-ACTIVITY PRODUCTION PATH… A10 MUST NOT
> BLOCK PHASE 4."*

K27 aşması `authorisedPhase: "phase3"` taşıyordu. Kurucu Faz 4'ü de aynı
koşullarla açtı, yani aşma **genişledi**:

```
authorisedPhase   phase3  →  phase4     ⭑ GENİŞLEDİ
gateCeiling       phase1  →  phase1     ✋ DEĞİŞMEDİ
deferredBlocker   A10     →  A10        ✋ DEĞİŞMEDİ
externalValidation pending → pending    ✋ DEĞİŞMEDİ
```

**Yalnızca yetki genişledi, kilit genişlemedi.** Aynı talimat bunu
ayrıca şart koşuyor:

> *"A10 MUST NEVER BE MARKED PASS / CLOSED / COMPLETED / VERIFIED unless
> the founder later supplies genuine external test evidence."*

`validate_spec § ⑤` dört kilidi koruyor ve `doesNotImply` listesine
beşinci bir cümle eklendi:

> **"Faz 4 üretiminin bitmesi A10'u kapatır"** — hayır, kapatmaz.

Yüz yirmi sayfanın tamamlanması sıfır çocuk oturumunu bir çocuk
oturumu yapmaz.

---

### K31 · A4 kapandı — 120 aktivitenin nihai listesi tamam

**14 Ağustos 2026 · Faz 4.**

A4 üç fazda kapandı: Faz 2 pilotun **16**'sını, Faz 3 iki bölgenin
**44**'ünü, Faz 4 kalan üç bölgenin **60**'ını seçti.

```
jaguar-condor 16 + monsoon 24 + great-ocean 20 + north-ice 24
              + middle-sea 20 + sun-savanna 16  =  120   ✅
```

**Düşürülen 48 aday havuzda kalır** ve `status: candidate` durumundadır
(**PROGRESSION_ARCHITECTURE § 6**): bir sayfa çocuk testinde düşerse
yerine aynı bölge × aynı tipten biri geçer. Faz 3 bu yedeği bir kez
gerçekten kullandı (`korean-sky-rope-plate` → `korean-hangul-build`).

---

### K32 · Sayfa modeli ALTI bölgeyle ölçüldü — dayanak kararı kurucuya taşındı

**14 Ağustos 2026 · Faz 4.**

Faz 2 bir bölge ölçtü, Faz 3 üç, Faz 4 **altı**:

| Bölge | Ağırlık | Faz |
|---|---:|---|
| jaguar-condor | 0,844 | 2 |
| great-ocean | 0,863 | 3 |
| monsoon | 0,865 | 3 |
| north-ice | 0,865 | **4** |
| sun-savanna | 0,875 | **4** |
| middle-sea | 0,887 | **4** |

Ortalama **0,867** · yayılım **0,043** (en ağır bölge en hafifinden
yalnızca %5 ağır). Faz 3'ün *"kalan üç bölge de 0,857'de gelirse model
yine 144 eder"* tahmini tuttu: **model 144.**

`page_budget.py` uyarısı buna göre değiştirildi ve artık *"bekle"*
demiyor: **"BÜTÜN BÖLGELER ÖLÇÜLDÜ (6/6): dayanağın gözden geçirilmesi
artık bir KURUCU KARARIDIR."**

> **Bir uyarı koşullar değişince aynı şeyi söylemeye devam ederse,
> söylediği şey doğru olsa bile YANLIŞ ZAMANI gösterir.**

Karar kurucuya taşındı: **A12**. 148 hedefi o karara kadar **yerinde
kalır** (K19 yeniden açılmadı).

---

## FAZ 5 KARARLARI — 14 Ağustos 2026

### K33 · A12 kapandı — sayfa hedefi **144** · ve hedefin DAYANAĞI da kayda geçti

**14 Ağustos 2026 · Faz 5 · kurucu talimatı § 3.**

Kurucu kararı tek cümleydi: **FINAL PAGE TARGET = 144 PAGES.**

| | **ESKİ** | **YENİ** | Kaynak |
|---|---:|---:|---|
| `scope.pageTarget` | **148** | **144** | ⭑ kurucu onayı |
| Ciltsiz baskı maliyeti | 3,52 $ | **3,45 $** | ölçüm |
| Ciltsiz telif | 5,48 $ | **5,55 $** | ölçüm |
| Başabaş ACOS | %36,5 | **%37,0** | ölçüm |
| `royaltyBaseline.paperback` | 5,48 | **5,55** | türetme sonucu |

Talimat iki yasağı birlikte koydu ve ikisi de uygulandı:

```
148'e ulaşmak için DOLGU EKLENMEDİ
144'ün altına inmek için İÇERİK ÇIKARILMADI
```

Model zaten **143 ham → 144 forma hizalı** ölçülmüştü (K32). Karar bir
sayıyı değiştirmedi; **bir tahmini bir ölçümle değiştirdi.**

#### 33.1 · Aynı sayı iki kez, iki farklı şey

Hedef bu projede üç kez yazıldı ve **ikisi aynı sayıdır**:

| # | Değer | Karar | Dayanak |
|---|---:|---|---|
| ① | 144 | bootstrap | **hiçbir bölge ölçülmemişti** — tahmin |
| ② | 148 | **K19** (A8) | Faz 1 modeli · 0/6 bölge gerçek içerikle ölçülmüştü |
| ③ | **144** | **K33** (A12) | **6/6 bölge GERÇEK içerikle ölçüldü** (K32) |

① ile ③ aynı sayıdır ve **aynı şey değildir**. Biri hiçbir şey
ölçülmeden yazıldı, öteki altı ölçümün sonucudur.

> ### Bir hedefin DEĞERİ bir şey söyler; DAYANAĞI başka bir şey. Yalnızca değeri saklayan bir kayıt, üçüncü değişiklikte hangi ölçümün hangi sayıyı ürettiğini SÖYLEYEMEZ.

Bu yüzden karar bir sayıyı güncellemekle kalmadı, **kaydın biçimini
değiştirdi**: `scope.pageTargetHistory` üç kaydı da dayanağıyla taşıyor
ve tekil `pageTargetBootstrapHypothesis` alanı **kaldırıldı** — aynı sayı
iki yerde durursa er geç iki farklı şey söyler (D17).

#### 33.2 · Kök neden düzeltmesi — hedef artık SESSİZCE kayamaz

K29'un dersi burada bir kat yukarıda tekrarlandı:

> **Bir düzeltme, düzelttiği kusurun TEKRARINI engellemiyorsa bir
> düzeltme değil bir ERTELEMEDİR.**

148'i 144 yapmak yalnızca bugünkü sayıyı düzeltir. Sayfa hedefi bu
projede masum bir sayı değildir — **14,99 $ fiyat noktasının kendisidir**.
Sessizce kayan bir hedef, sessizce kayan bir marjdır.

`validate_spec § ⑦` doğdu ve dört şeyi birlikte denetliyor:

```
· pageTargetHistory DURUYOR ve her kayıt DOLU bir dayanak taşıyor
· zincir KESİNTİSİZ: her kayıt kendisini aşan kararı gösterir ve
  o karar BİR SONRAKİ kaydın kendisidir
· geçmiş KÖKENİNDEN başlar (ilk kayıt 'bootstrap')
· yürürlükteki hedef ve telif dayanağı geçmişin SON kaydıyla aynı
```

#### 33.3 · Kapı ilk koşusunda KENDİ iki deliğini buldu

`selftest § ⑲` on kurgu koşturuyor ve ilk hâl **ikisini kaçırdı**:

| Kurgu | İlk hâl | Neden kaçırdı |
|---|---|---|
| `basis: ""` | ❌ **yeşil** | `is not None` kullanıyordu — alan VARDI ama BOŞTU |
| **aradan 148 kaydı düşürülür** | ❌ **yeşil** | yalnızca SON kayıt denetleniyordu |

İkincisi kapının varlık sebebiydi ve tam da onu kaçırıyordu: aradan bir
kaydı düşürmek, **bir supersession'ın izini silmenin en sinsi biçimidir**
— 148 hiç var olmamış gibi görünür ve iki 144 tek bir karara çöker.

Düzeltme örneği değil **sınıfı** kapattı: zincir kuralı, aradan da
baştan da sondan da bir kaydın düşürülmesini imkânsız kılıyor.

`selftest`: 178 → **188 denetim**.

---

### K34 · Kurucu aşması Faz 5'e genişletildi — **tavan yine değişmedi**

**14 Ağustos 2026 · Faz 5 · kurucu talimatı § 4.**

Kurucu talimatı açıktı: *"Use the Founder Override and proceed to
Phase 5."*

```
PHASE 5 PRODUCTION      ✅ YETKİLİ      (kurucu · K34)
A10 ÇOCUK OTURUMU       ❌ YAPILMADI    (0 oturum)
DIŞ DOĞRULAMA           ⏳ BEKLİYOR     externalValidation = pending
.gate                       phase1      (YÜKSELTİLMEDİ)
```

Genişleyen yalnızca `authorisedPhase`'tir: **`gateCeiling` `phase1`'de
kalır.** Talimatın kendisi bu ayrımı tek cümlede kuruyor:

> *"The Founder Override means: DO NOT WAIT FOR CHILD TESTING TO BEGIN
> PHASE 5. It does NOT mean: CHILD TESTING PASSED."*

#### 34.1 · Genişletme kaydı artık EZİLMİYOR

K27 ve K30 tekil alanlar kullanıyordu (`extendedTo` · `extensionDecision`)
ve **üçüncü genişletme K30'u ezecekti**. Aşmanın ne kadar uzadığı, tam da
uzadıkça görünmez olacaktı.

`phaseOverride.extensionHistory` doğdu ve üç genişletmeyi de taşıyor:

| Yetkilenen faz | Karar | Tavan |
|---|---|---|
| `phase3` | **K27** | `phase1` |
| `phase4` | **K30** | `phase1` |
| **`phase5`** | **K34** | **`phase1`** |

Üçüncü sütun bu tablonun asıl işidir: **aşma üç kez uzadı ve tavan bir
kez bile kalkmadı.**

#### 34.2 · `doesNotImply` beşinci maddeyi aldı

Faz 4 listeye *"120 sayfanın bitmesi A10'u kapatmaz"* maddesini eklemişti.
Faz 5 aynı sınıfın bir sonrakini ekliyor:

> **"Faz 5 görsel üretiminin bitmesi A10'u kapatmaz."**

Gerekçe aynı ve tekrar etmesi bir kusur değil, kusurun **tekrar eden
biçimi**: her fazda üretim bitince, biten üretimin yapılmamış testi
kapattığı sanılır. Liste bunu her fazda bir kez daha yazarak engelliyor.

---

### K35 · Görsel hattı ÜÇ KATMANDIR ve RAW'a dokunulmaz

**14 Ağustos 2026 · Faz 5 · kurucu talimatı § 14–15.**

Görsel varlıklar üç dizinde durur ve **yalnızca ortadaki üretilebilir**:

```
07_ASSETS/raw/         KURUCUNUN çıktısı · DEĞİŞMEZ · asla üzerine yazılmaz
07_ASSETS/processed/   CLI ÜRETİR · her zaman RAW'dan YENİDEN üretilebilir
07_ASSETS/final/       basıma hazır · processed'dan türer
07_ASSETS/rejected/    şartnameyi ihlal eden RAW · silinmez, AYRILIR
```

Kural tek cümlede: **bir işlenmiş varlık her zaman RAW'dan yeniden
üretilebilmelidir.** Bu yüzden `asset_pipeline.py` RAW'ı okur, asla
yazmaz ve her işlenmiş dosyanın yanına kaynağının sha256'sını koyar.

Reddedilen bir görsel **silinmez**: `rejected/` altına taşınır ve
gerekçesi manifest'e yazılır. Silinen bir ret, aynı hatanın ikinci kez
yapılmasını serbest bırakır.

> **Şartnameyi ihlal eden görsel değiştirilir; şartname değiştirilmez.**
> Şartnamenin kendisi kanıtlanabilir biçimde yanlışsa bu bir **tasarım
> düzeltmesidir** ve kayda geçer (kurucu talimatı § 16).


---

## FAZ 6 KARARLARI — 16 Ağustos 2026

### K36 · A6 kapandı — yazar biyografisi kurucu metnidir

**16 Ağustos 2026 · Faz 6 talimatı § 2.**

> *"Emre is a puzzle designer, mythologist, and game archivist dedicated
> to preserving ancient cultures, codes, and stories for the next
> generation."*

21 kelime. Metin **kurucunun kendi cümlesidir** ve tek kelimesi
değiştirilmedi. `authorBio` null iken Faz 6 kapısı kırmızı yanıyordu —
World Myths'te KDP bir yer tutucu biyografiyi reddetmişti ve o ders bu
projeye bir kapı olarak taşınmıştı.

### K37 · Çocuk testi ARACI üretildi — A10 KAPANMADI

**16 Ağustos 2026 · Faz 6 talimatı § 3.**

Kurucu etkileşimli bir çocuk testi dosyası istedi ve üretildi:
`01_SOURCE/pilot_tr/interactive_child_test.html` — on altı Türkçe pilot
sayfası, sayfa başına gözlemci paneli, oturum kaydı üreteci.

**A10 kapatılmadı ve `.gate` yükseltilmedi.** Gerekçe projenin kendi
kuralıdır ve beş fazdır değişmedi:

> ### PAKET ÜRETMEK, TEST YAPMAK DEĞİLDİR. (DECISIONS § A10 · Faz 2'den beri)

Bir simülasyon bir çocuk değildir. Araç **testi yapmayı mümkün kılar**;
testin **yapıldığını göstermez**. Bugün yapılan oturum sayısı **sıfırdır**
ve `externalValidation` **`pending`** kaldı.

    araç üretildi        ✅
    oturum yapıldı       ❌  0
    çocuk sayısı         ❌  0
    externalValidation   ⏳  pending

**A10 şu üçü birlikte olduğunda kapanır:** gerçek bir çocuk · gerçek bir
oturum · `CHILD_TEST_LOG.md`'ye kaydedilmiş sonuç. Araç o kaydı tek
düğmeyle üretiyor; kurucu iki testçisiyle koşturduğunda A10 **aynı gün**
kapanır.

Ajan bir simülasyonu bir oturum olarak kaydetmedi — çünkü kaydetseydi
proje belgeleri **yanlış bir olguyu** taşırdı ve `validate_spec § ⑤`
zaten bunu kırmızı yakacak biçimde kurulmuştu.


---

### K38 · A13 kapandı — sayfa **160** · ölçüm modeli yendi

**16 Ağustos 2026 · Faz 6 talimatı § 1.**

Kurucu gerçek dizgi ölçümünü kabul etti ve **hiçbir aktiviteyi kesmedi**.

| | ESKİ | YENİ |
|---|---:|---:|
| `scope.pageTarget` | 144 | **160** |
| Ciltsiz baskı | 3,45 $ | **3,72 $** |
| Ciltsiz telif | 5,55 $ | **5,27 $** |
| Başabaş ACOS | %37,0 | **%35,2** |

**Kök neden düzeltildi, sayı değil.** `pageWeight` Faz 1'de **tipe göre**
atanmıştı (`cipher`/`sort` → 0,75) ve bu *"iki hafif sayfa bir sayfayı
paylaşır"* demekti. Ölçüm yalanladı:

```
ağırlık 1,00 (56 sayfa) → ortalama 8,01 inç dikey ihtiyaç
ağırlık 0,75 (64 sayfa) → ortalama 8,57 inç   ← DAHA AĞIR
kullanılabilir yükseklik 10,00 inç · paylaşım için gereken ≤5,00 inç
64 hafif sayfanın SIFIRI sığıyor.
```

> ### `cipher` ve `sort` sayfaları hafif değildir. 0,75 ölçülmedi, ATANDI.

168 adayın `pageWeight`i 1,0'a çekildi ve model artık dizgiyle **birebir**
tutuyor: **160 = 160 · sapma %0,0**.

**Alt başlıktaki 120 vaadi korundu.** Kurucu 16 sayfayı üstlendi.

---

### K39 · A14 kapandı — baskı ölçütü **300 → 150 dpi**

**16 Ağustos 2026 · Faz 6 talimatı § 2.**

Teslim edilen 156 ham görselin **hepsi 1,57 MP**. Aktivite hedeflerinde
efektif çözünürlük 166–202 dpi çıkıyordu. Kurucu görselleri **yeniden
üretmemeyi** ve ölçütü düşürmeyi seçti.

> ### Bir ölçüt düşürülüyorsa, düşürüldüğü SÖYLENMELİDİR.

`production.minDpiHistory` eski değeri, gerekçeyi **ve sonucunu** taşıyor:

> *"İç blok çizgi sanatı 150–200 dpi bandında basılacak. KDP tavsiyesi
> 300 dpi'dır; bu ölçüt düşürülmesi bir kurucu kararıdır ve baskı
> yumuşaklığı KABUL EDİLMİŞTİR."*

Fiziksel boy **değişmedi**; `targetPx` yarılandı (aynı inç, yarı piksel).

#### 39.1 · ⭑ SIRALI EŞLEME UYGULANMADI — VE UYGULANAMAZDI ⭑

Talimat *"001–156'yı manifestin ilk 156 girdisine sırayla eşle"* diyordu.
**Bu eşleme ölçülerek yanlışlandı:**

| Dosya | Gerçekte ne | Manifest sırası ne derdi |
|---|---|---|
| `001.png` | **Inuktitut hecelemesi** levhası | `fig-maya-bar-dot-numbers` |
| `121.png` | **Irish** kültür vinyeti | `vig-finnish` |

> **Yanlış aktiviteye bağlanmış kusursuz bir görsel, o sayfayı ÇÖZÜLEMEZ
> yapar** — ve bir kültürü başka bir kültürün sanatıyla etiketler.

**Doğru eşleme bulundu ve kanıtlandı:** dosyalar **manifest sırasında
değil, PROMPT KÜTÜPHANESİ sırasında** (bölge sırası × sayfa sırası) ve
aradan **iki** girdi eksik.

```
yönelim eşleşmesi   156 / 156   (%100)
görsel çapa         001 → inuit-syllabic-signs   ✅
görsel çapa         119 → vig-finnish            ✅
görsel çapa         121 → vig-irish              ✅
görsel çapa         141 → seal-north-ice         ✅
eksik girdi         yoruba-underdot-letters · korean-river-crossing-sort
```

İki eksik varlık için **dürüst yer tutucu** üretildi: çapraz taramalı,
üzerinde `PLACEHOLDER` ve `art not supplied — do not print` yazan kutular.
Manifest'te `status: placeholder-art-missing`.

#### 39.2 · Kutular sanata oturtuldu, sanat kutuya zorlanmadı

46 varlıkta teslim edilen sanat kutudan kısaydı. Boşluk beyazla
doldurulabilirdi (beyaz sayfada görünmez) ama kutu yanlış boy iddia
etmeye devam ederdi. **Kutular daraltıldı**: yukarı örnekleme yok,
kırpma yok, doluluk ≈%100.

Bir varlık (`fig-korean-animal-plate`) hedeften 6×97 px küçüktü ve hat
**büyütmeyi reddetti** — doğru davranış. Kutusu sanata oturtuldu.

---

### K40 · A10 kapandı — ⚠ **KURUCU AŞMASI · SIFIR OTURUM**

**16 Ağustos 2026 · Faz 6 talimatı § 3.**

```
GERÇEK ÇOCUK OTURUMU     0
TEST EDİLEN ÇOCUK        0
externalValidation       overridden-zero-sessions   ← 'passed' DEĞİL
.gate                    release
```

Kurucu, gerçek bir çocuk oturumu **yapılmadan** A10'u kapatmayı ve kapıyı
yükseltmeyi **açıkça** seçti. Karar kayıtlıdır, gizli değildir ve
**'passed' olarak yazılmamıştır**.

> ### Bir kapanış KANITLA da olur KARARLA da. İkisi aynı şey değildir ve kayıt hangisi olduğunu söyler.

`childTesters.closure.whatThisIsNot` beş maddeyi kalıcı olarak reddediyor:

- *bir çocuk bu kitabı test etti*
- *kitap çocuk-doğrulandı*
- *talimatların anlaşıldığı ölçüldü*
- *Faz 2'nin PASS ölçütü sağlandı*
- *externalValidation 'passed' oldu*

**Ne yapıldı:** `interactive_child_test.html` üretildi — on altı Türkçe
pilot sayfası, sayfa başına gözlemci paneli, tek düğmeyle oturum kaydı.
Araç **hazırdır**; kurucu iki testçisiyle koşturursa kayıt
`CHILD_TEST_LOG.md`'ye girer ve alan `passed` olabilir.

**Aşma kaydı silinmedi.** Üç fazlık genişletme geçmişi (K27 · K30 · K34)
ve tavanın üç faz boyunca `phase1`'de kaldığı olduğu gibi duruyor;
`gateCeilingHistory` tavanın **ne zaman ve neden** kalktığını taşıyor.

---

## YÜKLEME ÖNCESİ GEÇİŞ KARARLARI — 16 Ağustos 2026

> Faz 6 kapandıktan **sonra**, yükleme öncesi denetimde alınan kararlar.
> Yeni bir faz değildir: paketi yükleyecek biri gibi bakan bir geçiştir.
> Ölçüm raporu: [`06_REPORTS/KDP_PREFLIGHT_AUDIT.md`](06_REPORTS/KDP_PREFLIGHT_AUDIT.md)

---

### K41 · Metadata açıklamasındaki sayı **ELLE YAZILMAZ** — ölçümden türer

**Ne yanlıştı.** `metadata.json § description` — müşterinin Amazon'da
okuyacağı tek metin — *"Twenty-two peoples. One hundred and twenty
pages."* diye başlıyordu. Kitap **160 sayfa**. Fark **40 sayfa**.

**Kök neden: sayı yanlış değildi — BAĞLI DEĞİLDİ.** Cümle Faz 6'da elle
yazıldı; `pageWeight` düzeltilip dizgi 160 ölçtüğünde (**K38**) açıklama
ölçümle birlikte hareket etmedi, çünkü ölçüme bağlı değildi.

> ### Elle yazılmış bir sayı, kaynağı değiştiği gün sessizce yalan söylemeye başlar.
>
> Bu, `pageWeight = 0,75`'in **birebir aynı** dersidir: o da ölçülmemiş,
> **atanmıştı** ve beş faz yaşadı. Aynı sınıf, ikinci kez — ve bu kez
> **müşteriye bakan yüzde**.

**İki büyüklük AYRIDIR ve karıştırıldı:**

```
120  =  AKTİVİTE (bulmaca) sayısı   ← alt başlığın vaadi
160  =  SAYFA sayısı                ← dizgiden ölçüldü
```

**Karar:** açıklama bir **kalıptır**; iki sayı da ölçümden gelir.
`descriptionFacts` alanı açıklamanın **iddia ettiği** sayıları taşır ve
yeni kapı **`metadata § ⑤`** onları ölçümle karşılaştırır.

| Yeni denetim | Ne yakalar |
|---|---|
| sayfa iddiası = PDF ölçümü | bayat sayfa sayısı |
| aktivite iddiası = manuscript sayımı | bayat aktivite sayısı |
| ölçülen sayfa sayısı metinde geçiyor | sayının düşmesi |
| aktivite sayısı `pages` diye anılmıyor | **120 puzzle ≠ 120 page** |
| rakamlı bayat sayfa iddiası yok | `"120 pages"` biçiminin dönmesi |

`metadata` kapısı **11 → 16 denetim**.

**Yeni açıklama** — pazarlama dili **eklenmedi**, yanlış sözcük
düzeltildi ve eksik gerçek yazıldı:

```
Twenty-two peoples. One hundred and twenty puzzles across one hundred
and sixty pages. Six seals to earn. …
```

---

### K42 · Prompt kütüphanesi **ELLE DEĞİL, ÜRETEÇTEN** genişletilir

Talimat *"`IMAGE_PROMPT_LIBRARY.html` sonuna ekle"* diyordu. Dosya
**üretilmiştir** ve `image_prompts.py --check` bayatlık kapısı her
koşuda dosyayı üreteçle karşılaştırıyor.

> ### Üretilmiş bir dosyaya elle eklenen bir bölüm, bir sonraki üretimde SİLİNİR — ve silinene kadar CI'ı kırmızı yakar.

**Karar:** yeni bölüm (§ 9) **üretece** eklendi. Sonuç talimatın
istediğiyle aynı — bölüm dosyanın sonunda, § 1–8'e dokunulmadan — ama
**yeniden üretimde hayatta kalıyor** ve bayatlık kapısı yeşil kalıyor.

`04_BUILD/image_prompts.py`: `COVER_OPTIONS` · `APLUS_MODULES` ·
`MISSING_ASSETS` · `kdp_final_section()`. Kütüphane **332 → 745 satır**.

**K10 ayrımı korundu ve GENİŞLETİLDİ.** İki eksik levhanın promptu
takip edilen sürümde `{PRINT_LIST}` ve `{REQUIRED_LABELS}` yer
tutucularıyla duruyor: `yoruba-underdot-letters`'ın etiket listesi
*tam olarak* çocuğun yazacağı şeydir.

**Kapak geometrisi hiçbir yerde elle yazılmadı** —
`06_REPORTS/tracked/metadata.json § cover`'dan okunuyor. Panel
enleri **hesaplanmıyor, sarmaldan çıkarılıyor**: ayrı ayrı yuvarlama
1 px açık bırakıyordu (2588+108+2588 = 5284 ≠ 5283) ve bir piksel,
birleştirici üç paneli yan yana koyduğunda tuvalin dışına taşar.

---

### K43 · Yeni varlık sınıfları **iç bloğun kurallarını miras ALMAZ**

Kapak ve A+ yeni üretiliyor. Üçünün ayrı standardı var:

| | KAPAK | A+ | EKSİK İÇ BLOK |
|---|---|---|---|
| Renk | RGB renkli | RGB renkli | gri tonlama |
| Çözünürlük | **gerçek 300 dpi** | 300 dpi kaynak | 150 dpi (K39) |
| Nihai biçim | tek PDF | PNG/JPEG < 3 MB | PNG |

> ### K39 bir İÇ BLOK kararıdır. Yeni üretilen bir varlığın düşürülmüş bir ölçütü miras almasının hiçbir gerekçesi yok.

**Ve üçünün ORTAK kuralı tektir:** görselde metin yok. Kapakta bu bir
üslup tercihi değil bir zorunluluktur — bir üretecin yazdığı başlık
düzeltilemez, KDP metadata'sıyla harfi harfine eşleşmez ve gömülü bir
yazım hatası bütün kapağı yeniden ürettirir.

**İki eksik levhada kural daha da ileri gider:** glifler ve kart metni
üreteçten **hiç gelmez**. Üreteç yalnızca boş mobilyayı çizer.
`yoruba`'da nokta içeriğin kendisidir; `korean`'da kartların sırası
cevabın kendisidir. İkisi de bir üretece bırakılamaz.

---

## AŞAMA 2 KARARLARI — 16 Ağustos 2026

> Kurucu bütün varlıkları teslim etti ve Aşama 2'yi yetkilendirdi.
> Nihai denetim: [`06_REPORTS/FINAL_BRUTAL_AUDIT_REPORT.md`](06_REPORTS/FINAL_BRUTAL_AUDIT_REPORT.md)

---

### K44 · Sayfa **160 → 156** · arka madde yeniden dizildi

**A15 kapandı.** Arka madde iki kusuru birden taşıyordu ve ikisi de
basılı sayfada görülüyordu:

**① `pages: N` bir SAYFA BÜTÇESİDİR, bir TEKRAR TALİMATI DEĞİL.**
Dizgi onu tekrar sanıyordu: `glossary pages: 4` → dört ÖZDEŞ sayfa.
On üç arka madde sayfasının **yedisi birebir kopyaydı**.

**② Basılan şey İÇERİK değil ŞARTNAMEYDİ.** `prints` alanı sayfanın ne
basacağını *tarif eder* — *"twenty-two entries, one per culture"*. Bu
bir sözlük değil, bir sözlüğün tarifidir.

> ### Arka kapak "the back of the book says which ones" diye söz veriyordu ve kitabın arkası hangileri olduğunu SÖYLEMİYORDU.

Veri zaten ölçülmüş hâlde duruyordu; arka madde artık ondan **türetilir
ve akar**: 22 sözlük girdisi · 115 kurum · 120 cevap.

**Sonuç zinciri — hiçbir sayı elle taşınmadı:**

```
sayfa 160 → 156   sırt 0,3603 → 0,3513 in
                  kapak eni 17,6103 → 17,6013 in
                  baskı 3,72 → 3,65 $
                  telif 5,27 → 5,34 $
                  ACOS %35,2 → %35,6
```

`royaltyBaseline` artık `metadata.py` içinde **TÜRETİLİYOR**; config
değeri modelin karşılaştırma dayanağıdır.

---

### K45 · Sayfa mobilyası — **levha basıyorsa dizgi basmaz**

**A15'in ikinci yarısı.** Ölçüm: yıldızlı kutu **37/37**, yazma alanı
**75/120** sayfada **iki kez** basılıyordu.

Kök neden: `pagePrints` iki ayrı muhataba yazılmış tek bir listeydi ve
ayrım hiçbir yerde yazılı değildi.

**Karar:** rol **ölçülür** (`04_BUILD/furniture_roles.py`) ve
`book.json § furniture` alanına **dondurulur**; dizgi prozayı değil
beyanı okur. `qa_design § ⑨` uyarıdan **kapıya** yükseltildi.

156 levha üretilmiş durumda ve yeniden üretilemez; bu yüzden **dizgi
bıraktı**. Ve bu yalnızca uygulanabilir olan değil DOĞRU olandır:
levhanın satırları anlamlı konumdadır, dizginin bloğu konumsuzdur.

**Yan kazanç:** serbest kalan dikey alan levhaya verildi — çocuğun
yazma satırları levhanın içinde ve levha artık **daha büyük** basılıyor.

---

### K46 · Yazı tipi **GÖMÜLÜR** — ve bu iki kusuru birden kapattı

Faz 6 iç bloğu base-14 `Helvetica` ile dizdi. `pdffonts`:

```
Helvetica  Type 1  WinAnsi  emb=no      ← sıfır gömülü yazı tipi
```

**① KDP bütün yazı tiplerinin gömülü olmasını ister.**

**② WinAnsi kitabın kendi imlâsını taşıyamıyordu.** Faz 5'in `A13`
düzeltmesi on dört ad geçişine işaret eklemişti ve dizgi onları
DÜŞÜRÜYORDU:

```
basılan:  M■ori     ← ön maddede · imlâ kuralını ÖĞRETEN sayfada
```

> ### Bir kitabın "işaretler önemlidir" diyen sayfası, işareti basamıyordu.

DejaVu Sans (Latin Genişletilmiş Ek + `★`) ve cevap anahtarındaki
kana/kanji için Droid Sans Fallback gömüldü. `interior § ⑥` artık
gömülülüğü **her koşuda** ölçüyor.

⚠ **Hangul kapatılamadı:** sistemde gömülebilir hiçbir yazı tipi hangul
kapsamıyor (Noto CJK CFF dış hatlı). Cevap anahtarı Korece adları
romanizasyonla veriyor ve sayfa bunu **okura açıkça söylüyor**.

---

### K47 · Kapak **Seçenek 1** — ölçülerek seçildi

Talimat *"artistic preference ile seçme"* diyordu. İki seçenek de
metinsiz ve güvenliydi; fark **tipografinin oturacağı alanların
sakinliğiyle** ölçüldü (bölge gri tonlama standart sapması).

| | Seçenek 1 | Seçenek 2 |
|---|---:|---:|
| Arka kapak tanıtım alanı | **20,3** | 43,3 |
| Toplam | **151,7** | 160,6 |

Arka kapak belirleyici oldu: en yoğun metin oradadır ve iki kat fark
doksan kelimelik bir metin için okunurluk farkıdır. Ön panelin altında
zaten **altı mühür izi** basılı — kitabın mekaniği tam olarak altı
mühürdür.

Seçilmeyen sanat **silinmedi**: `07_ASSETS/raw/kdp-cover-option-02.png`
duruyor ve `03_COVER/COVER_SELECTION.json` neden seçilmediğini taşıyor.

---

### K48 · Kapak sanatı **89 dpi** — YUKARI ÖRNEKLENMEDİ

Teslim edilen kapak **1569 × 1003 px**; 300 dpi için **5280 × 3375 px**
gerekiyordu — **×3,37 eksik**.

> ⛔ Piksel eklemeden DPI etiketini 300 yapmak bir düzeltme değil,
> bir **YANLIŞ BEYANDIR**.

**Karar:** sanat kendi çözünürlüğünde yerleştirildi, gerçek dpi
`06_REPORTS/cover.json` içine **sayı olarak** yazıldı ve bütün tipografi
**vektör** yapıldı — başlık, yazar, sırt ve arka kapak metni
çözünürlükten bağımsız olarak keskin basar.

**AÇIK · KURUCU EYLEMİ:** baskı kalitesi için kapak sanatı yeniden
üretilmeli. Tek komut yeter; sırt ve geometri kendiliğinden türer.

---

### K49 · Kapak tipografisi — **SANAT KAHRAMAN, PANEL YOK**

Kurucu ilk kapağı reddetti. Gerekçe tek cümleydi ve doğruydu:

> Kapak bir illüstrasyon değil, üstüne **beyaz UI kutuları** yapıştırılmış
> bir görüntü gibi duruyordu.

Dört opak panel kaldırıldı: başlık kutusu · yazar kutusu · arka kapak
paneli · sırt şeridi. **Şu an opak panel sayısı 0** ve `covers.py` bunu
her koşuda kaydediyor; `--check` panelli eski sürümü BAYAT sayıyor.

Yerine üç ÖLÇÜLEN araç geldi:

| # | Araç | Nasıl ölçülür |
|---|---|---|
| ① | mürekkep rengi | bloğun altındaki sanatın ortalama parlaklığı |
| ② | harf halesi | glif maskesi bulanıklaştırılıp yumuşak bir yıkamanın ALFASI olur |
| ③ | okunurluk | **yalnızca mürekkebin basılacağı piksellerin** parlaklığı → WCAG oranı |

> ### Ortalama bir zemin, bir harfin altındaki zemin değildir.
>
> ② ve ③ birlikte çalışır: eşiğin altında kalan blok için hale
> güçlendirilir ve katman yeniden kurulur (en çok dört kez). Ölçülen en
> düşük oran **8,77 : 1** (eşik 3,0).

Kontrast desteğinin kenarı yoktur: harita, kıyı çizgisi ve pusula gülü
halenin içinden görünmeye devam eder.

---

### K50 · Sanat **gerçek sırta** hizalandı — süreklilik ölçüldü

Kurucunun sanatının kot cilt şeridi gerçek sırttan **%2,86 solda**
duruyordu; şerit arka kapağın üstüne düşüyor ve kapak üç ayrı tasarım
bloğu gibi okunuyordu.

```
cilt şeridi merkezi   0,4614  →  0,5000
sırt merkezi          0,5000
```

Oran bozulmadan yeniden çerçevelendi — **yalnızca kadraj kaydı, yukarı
örnekleme YOK**. Bedeli dürüstçe kayıtlı: etkin dpi **89 → 82**.

> Bir sürekliliği "sağladık" demek, ölçmekten farklıdır.
> `covers.py § ②` hizayı her koşuda ölçer ve sapma 0,004'ü aşarsa
> KIRMIZI yanar.

---

### K51 · Sırt yazısı **optik** ortalandı — hesapla değil ÖLÇÜMLE

Kapak iki kez render edilir (sırt yazısıyla ve yazısız) ve fark alınır.
Fark tam olarak mürekkebin kendisidir; gerçek kutusu ölçülür.

```
sapma (önce)        -0,0100 in
optik düzeltme      -0,0100 in
sapma (sonra)       +0,0033 in     ← ölçüt ±0,004
mürekkep genişliği   0,1600 in     ← sırt bandı 0,3513 in
```

> ### Bir şeyin ortada OLDUĞUNU varsaymak, ortada olduğunu ölçmek değildir.

---

### K52 · A+ modül haritası **MODÜL MERKEZLİ** oldu

*Standard Three Image & Text* modülü Amazon'da TEK bir modül başlığı ve
**üç ayrı yuva metni** verir. Harita görsel merkezliydi ve aynı başlığı
ile aynı gövdeyi üç satıra da yazıyordu — kurucu paneli doldururken
hangi metnin nereye gideceğini bilemezdi.

> ### Bir eşleme belgesi, panelde HANGİ ALANA ne gireceğini tek anlamlı söylemiyorsa eşleme yapmıyor demektir.

Harita artık **MODÜL → GÖRSEL → BAŞLIK → GÖVDE** sırasıyla kuruluyor ve
çok görselli iki modülün her yuvası kendi başlığını ve kendi gövdesini
taşıyor. Onaylı kopya **yeniden yazılmadı**; yalnızca eksik yuva metni
eklendi ve `kdp_preflight` iddia taraması onu da kapsıyor.

---

### K53 · Kapak sanatı **4× super-resolution** sürümüyle değişti — ölçülerek

Kurucu 18 Ağustos 2026'da `kdp-cover-option-01-4x-300dpi.png` teslim etti.

> ### ⭑ DOSYA ADI BİR KANIT DEĞİLDİR ⭑
>
> Ad *"4x-300dpi"* diyor ve gömülü üstveri *299,9994* yazıyor. İkisi de
> **iddiadır**. Kabul kararı ölçümden verildi:
> `etkin dpi = piksel / gerçek fiziksel boy`.

| | eski | **yeni** |
|---|---:|---:|
| piksel | 1569 × 1003 | **6276 × 4012** |
| etkin dpi (17,6013 × 11,2500 in) | 89,1 | **356,6** |
| sırt hizalama kırpması sonrası | — | **329,2** |

Dört ayrı test yapıldı ve dördü de geçti:

| Test | Ölçüm |
|---|---|
| aynı kompozisyon mu | yeni→eski ölçekte **PSNR 32,3 dB** → onaylı sanatın kendisi |
| gerçek detay mı | kenar enerjisi saf bicubic tabana göre **4,66×** → super-resolution |
| kompozisyon uyumu | cilt şeridi 0,4616 ↔ eski 0,4614 → hizalama birebir çalışır |
| kirlilik | metin · filigran · logo · barkod · ISBN **yok**; mühürler BOŞ |

**Eski dosya SİLİNMEDİ**, `rejected/` altına gerekçesiyle arşivlendi ve
`asset_intake --verify` artık aşılmış teslimleri **arşivde** doğruluyor:
kaybolan bir arşiv de bir kusurdur.

**Ve eşik kapıya dönüştü:** `covers.py` etkin dpi < 300 ise KIRMIZI
yanıyor.

> ### Bir eşik, karşılanabilir hâle geldiği gün KAPIYA dönüşür.

---

### K54 · A+ metni görsele GÖMÜLMEZ — kardeş kitaptan bilinçli ayrım

*The Great Book of World Myths*'in A+ uygulaması okundu ve görselleri
açıldı. Ölçülen gerçek:

| Soru | Cevap |
|---|---|
| metin görselin içinde mi | **EVET** — `aplus.py` PIL ile JPEG'e basıyor |
| modül alanı dolduruluyor mu | **HAYIR, kasıtlı** — playbook *"headline/body BOŞ bırakılır"* diyor |
| neden | o projede **üreteç kapakta kitabın adını yanlış yazmıştı**; bütün tipografi görsele deterministik basıldı |

> ### Kardeş kitabın gerekçesi bu kitapta YOKTUR.
>
> Buradaki metin de üreteçten gelmiyor: `metadata.json` ölçümlerinden
> türetiliyor ve Amazon onu kendi alanlarında **duyarlı** basıyor.
> Aynı riski çözmek için aynı bedeli ödemeye gerek yok.

Bedel gerçek: gömülü metin **düzeltilemez** (bu kitabın sayfa sayısı
zaten 160 → 156 değişti), **mobilde ölçeklenmez**, **çevrilemez** ve
Amazon overlay modüllerinde **iki kez** görünür.

**Karar: kopyalanmadı.** Görseller metinsiz kalır, kopya modül
alanlarına girer. Harita bunu açıkça uyarıyor — iki kitabın sözleşmesi
birbirinin tersidir.

---

### K55 · A+ **alt metni** eksikti — ve bu gerçek bir kusurdu

Karşılaştırma bir eksik buldu: kardeş projenin playbook'u her görsel
için alt metni *"erişilebilirlik; zorunlu"* diye işaretliyor; bu
projenin haritasında **hiç yoktu**.

> ### Alt metin bir pazarlama alanı değildir: görmeyen bir okurun gördüğü TEK şeydir.

11 görselin 11'ine betimleyici alt metin yazıldı — görseli TARİF eder,
pazarlama cümlesini tekrarlamaz.

**Ve bir kapı eklendi**, kardeş projenin pahalı dersinden: orada iki
modül **metinsiz** çıkmış ve hiçbir kapı görmemişti çünkü doğrulama
yalnızca ölçü, renk ve dosya boyutuna bakıyordu. Artık başlık · gövde ·
alt metin · yuva başlığı · yuva gövdesi **boş olamaz**.
`aplus` kapısı **32 → 77 denetim**.
