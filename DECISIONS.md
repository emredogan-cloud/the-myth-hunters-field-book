# DECISIONS — karar kaydı

> İki şey taşır: **alınmış kararlar** (`K##`) ve **AÇIK KARARLAR** (`A#`).
> Bir varsayım sessizce proje gerekliliğine dönüşemez.

---

## AÇIK KARARLAR — kurucudan yanıt bekleyen

Durum tablosu · **13 Ağustos 2026 · Faz 2**

| # | Soru | Aciliyet | Ne zaman kapanmalı | Durum |
|---|---|---|---|---|
| ~~A1~~ | ~~Manuscript public depoda mı duracak?~~ | — | — | ✅ **KAPANDI → K11** |
| ~~A2~~ | ~~Devralma politikası onayı~~ | — | — | ✅ **KAPANDI → K12** |
| ~~A3~~ | ~~6 bölge ve mühür mimarisi onayı~~ | — | — | ✅ **KAPANDI → K18** |
| ~~A8~~ | ~~148 sayfa kabul edilecek mi~~ | — | — | ✅ **KAPANDI → K19** |
| **A4** | 168 adaydan 120'sinin nihai seçimi | **YÜKSEK** | Faz 3 başlarken | AÇIK · pilot 16'sını seçti |
| **A7** | **≥2 çocuk testçi kim** | **YÜKSEK** | Faz 2 kapanışı | AÇIK · **0 testçi** · **DIŞ DOĞRULAMA BEKLİYOR** |
| **A9** | **YENİ** — fizikî prova siparişi ve değerlendirmesi | ORTA | Faz 5–6 | AÇIK · **KURUCUYA AİT** |
| **A5** | Ciltli hediye sürümü v1.0'a girecek mi | DÜŞÜK | Faz 4 | AÇIK (varsayım: hayır) |
| **A6** | Yazar biyografisi metni | ORTA | Faz 5 | AÇIK |

---

### A4 · 120 aktivitenin nihai listesi — kısmen ilerledi

Faz 2 pilotu `jaguar-condor` bölgesinin **16'sını** 22 adaydan seçti ve
`locked` yaptı. Kalan beş bölgenin seçimi Faz 3–4'e ait.

**Düşürülen altı aday havuzda kalır** ve `status: candidate` durumundadır:
bir pilot aktivitesi çocuk testinde düşerse yerine aynı bölge × aynı
tipten biri geçer (PROGRESSION_ARCHITECTURE § 6).

### A7 · Çocuk testçiler — Faz 2'nin sert bloklayıcısı · **AÇIK**

**13 Ağustos 2026 itibarıyla mevcut testçi sayısı: 0.**

Ajan çocukla test yapamaz. Test paketi Faz 2'de **hazırlandı ve koşmaya
hazırdır** ([`03_EDITORIAL/CHILD_TEST_PROTOCOL.md`](03_EDITORIAL/CHILD_TEST_PROTOCOL.md)),
ama koşturulmadı ve **sahte kayıt üretilmedi**.

| | |
|---|---|
| Test paketi | ✅ hazır |
| Testçi | ❌ 0 |
| `CHILD_TEST_LOG.md` | ✅ var · **0 oturum** |
| Faz 2 çocuk kapısı | ⏳ **DIŞ DOĞRULAMA BEKLİYOR** — PASS **değil** |

Kimlikler anonimdir (`tester-01`) ve gerçek ad depoya **hiçbir koşulda**
girmez — `validate_structure.py § check_child_privacy` denetler.

Kurucu Türkçe konuşan testçi sağlarsa tester-facing materyal geçici
olarak **Türkçe** üretilebilir (K21). O materyal ticari değildir ve
`qa_language.py` onun nihai çıktıya sızmasını mekanik olarak engeller.

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
