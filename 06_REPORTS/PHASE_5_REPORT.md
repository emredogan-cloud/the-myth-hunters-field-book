# FAZ 5 RAPORU — üretim hattı kuruldu, ve dokuz sessiz çelişki bulundu

> **The Myth Hunter's Field Book** · Faz 5 · 14 Ağustos 2026
> Dal `faz/5-yakinsama` → `main` · Kapı **`phase1`'de KALDI** · Etiket `v0.5.0`
>
> Faz 4'ün sorusu *"kitap kapanabiliyor mu"* idi. Bu fazınki başkaydı:
>
> **Kitap ÜRETİLEBİLİR mi — ve üretilirken hangi şartname kendi
> levhasıyla çelişiyor?**
>
> Cevap: **evet, üretilebilir.** Ve çelişen çok şey bulundu: altı görsel
> şartnamesi, iki ön madde sızıntısı, bir sayfa modeli — ve bağımsız
> editoryal inceleme **on üç bloklayıcı** daha buldu. Hepsi bulunması
> gereken yerde bulundu: **görsel üretilmeden önce.**
>
> İkisi kitabı gerçekten bozardı. Dokuz levha yanlış bir yıldız numarası
> basıyordu ve `monsoon` bölgesinin mühür sözcüğü **kurulamıyordu** —
> **üç kapının arasından geçmiş bir kusurdu.**

---

## ⚠ ÇOCUK DOĞRULAMASI: YAPILMADI

Bu satır bu raporun ilk satırıdır ve faz sonunda da değişmedi.

```
FAZ 5 YETKİSİ         ✅ VERİLDİ     kurucu · K34
A12 SAYFA HEDEFİ      ✅ KAPANDI     144 · kurucu · K33
A10 ÇOCUK OTURUMU     ❌ YAPILMADI   0 oturum
DIŞ DOĞRULAMA         ⏳ BEKLİYOR    externalValidation = pending
.gate                     phase1     YÜKSELTİLMEDİ
```

**Kurucu aşması bir üretim yetkisidir, bir test kanıtı değildir.**
Aşma üç kez uzadı (K27 · K30 · **K34**) ve tavan **bir kez bile
kalkmadı**. Aşağıdaki her *"doğrulandı"* sözcüğü **İÇ / TEKNİK
DOĞRULAMA** anlamındadır.

---

## 0 · Tek bakışta

| | Hedef | Ölçülen | Durum |
|---|---:|---:|---|
| **A12 · sayfa hedefi** | kurucu kararı | **144** | ✅ **kapandı → K33** |
| Sayfa modeli | 144 | **144** · sapma **%0,0** | ✅ |
| Model kaynağı | ölçüm | **manuscript** (tahmin değil) | ✅ |
| Ciltsiz baskı · telif | — | **3,45 $ · 5,55 $** | ✅ |
| Başabaş ACOS | — | **%37,0** | ✅ |
| Ön madde | 8 sayfa | **9 sayfa · 8 bölüm** | ✅ *bkz. P1* |
| Kelime | 22.000 ±%15 | **21.615** (%-1,8) | ✅ |
| Ön madde okunabilirliği | ≤ field note +0,5 | **FK 4,22 < 5,40** | ✅ |
| Ticari dil | %100 İngilizce | **1.488 dize** (Faz 4: 814) | ✅ |
| **Varlık envanteri** | ~150 | **158** · hesaplandı | ✅ |
| Zorunlu etiket | — | **732** (Faz 4: 700) | ✅ |
| **Üretilmiş görsel varlık** | kurucuya ait | **0** | ⏳ *bilerek* |
| Görsel hattı | kurulsun | **kuruldu · dosya katmanında sınandı** | ✅ |
| Ölçüme dayanan sayfa | kısıtlı olsun | **43 / 43** | ✅ *23'ü Faz 5'te* |
| **Görsel şartnamesi çelişkisi** | — | **6 bulundu · 6 düzeltildi** | ⚠ *bulundu* |
| Ön madde sızıntısı | — | **2 bulundu · 2 düzeltildi** | ⚠ *bulundu* |
| Sayfa modeli çelişkisi | — | **1 bulundu · düzeltildi** | ⚠ *bulundu* |
| Kültürel kısıt erişilebilirliği | — | **235 satır · 0 çevrilmemiş** | ✅ |
| Kapı sayısı | — | **16** (yeni: `qa_assets`) | ✅ |
| Kapı öz-testi | yeşil | **237 denetim** (Faz 4: 178) | ✅ |
| **Editoryal inceleme** | koşsun | **66 bulgu · 13 bloklayıcı** | ⚠ *bulundu* |
| Bloklayıcı bulgu karşılığı | hepsi | **13 / 13 düzeltildi** | ✅ |
| **Mühür yıldız numarası** | doğru | **9 yanlıştı · 37/37 düzeltildi** | ⚠ *bulundu* |
| Basılı mühür kuralı | doğru | **27/37'de yanlıştı · düzeltildi** | ⚠ *bulundu* |
| Kusurlu kurgu sınıfı (§ 30) | 18 | **18 / 18** | ✅ |
| CI | yeşil | **2 kırmızı · bulundu, düzeltildi** | ⚠ *§ 24.0* |
| **Çocuk saha oturumu** | — | **0 oturum** | ⏳ **BEKLİYOR** |

```
FAZ 5 ÜRETİMİ           ✅ TAMAM       ön madde · görsel hattı · editoryal yakınsama
A12 ÇELİŞKİSİ           ✅ KAPANDI     K33 · 144 · ve DAYANAĞI da kayıtlı
KURUCU AŞMASI           ✅ GENİŞLEDİ   K34 · tavan DEĞİŞMEDİ
HAM GÖRSEL ÜRETİMİ      ⏳ KURUCUYA AİT  0 / 158 · hat HAZIR
DIŞ ÇOCUK DOĞRULAMASI   ⏳ BEKLİYOR    0 oturum · A10 AÇIK

Bunlar TOPLANMAZ. BİR HATTIN KURULMASI, BİR VARLIĞIN ÜRETİLMESİ DEĞİLDİR.
```

---

## 1 · Faz 5 kapsamı

```
① A12'yi kaydet — 144 sayfa üretim modeli        ✅ K33
② A10 kurucu aşmasını kaydet                     ✅ K34
③ nihai ön maddeyi yaz                           ✅ 9 sayfa · 8 bölüm
④ kelime modelini kapat                          ✅ 21.283
⑤ görsel varlık üretim hattını kur               ✅ K35 · dört katman
⑥ ~150 nihai görseli hazırla                     ✅ 158 ŞARTNAME · 0 varlık
⑦ her görseli şartnamesine karşı doğrula         ✅ qa_assets · 33 denetim
⑧ editoryal yakınsamayı koştur                   ✅ bağımsız alt-ajan
⑨ Faz 6 için nihai üretim kaynağını hazırla      ✅ § 26
```

**Yapılmayan:** ham görsel üretimi (kurucuya ait), fizikî prova, KDP
paketi, tarayıcı/KDP paneli işi. Dördü de faz sınırının dışındadır ve
sınır aşılmadı.

---

## 2 · A12 — sayfa hedefi **144** · kurucu kararı **K33**

Kurucu kararı tek cümleydi: **FINAL PAGE TARGET = 144 PAGES.**

| | **ESKİ** | **YENİ** |
|---|---:|---:|
| `scope.pageTarget` | 148 | **144** |
| Ciltsiz baskı | 3,52 $ | **3,45 $** |
| Ciltsiz telif | 5,48 $ | **5,55 $** |
| Başabaş ACOS | %36,5 | **%37,0** |
| Model ↔ hedef sapması | −%2,7 | **%0,0** |

İki yasak da uygulandı: 148'e ulaşmak için **dolgu eklenmedi**, 144'ün
altına inmek için **içerik çıkarılmadı**.

### 2.1 · Aynı sayı iki kez, iki farklı şey

| # | Değer | Karar | Dayanak |
|---|---:|---|---|
| ① | 144 | bootstrap | **hiçbir bölge ölçülmemişti** |
| ② | 148 | K19 (A8) | Faz 1 modeli · 0/6 bölge gerçek |
| ③ | **144** | **K33** (A12) | **6/6 bölge ÖLÇÜLDÜ** (K32) |

① ile ③ aynı sayıdır ve **aynı şey değildir**.

> ### Bir hedefin DEĞERİ bir şey söyler; DAYANAĞI başka bir şey.

Kayıt biçimi bu yüzden değişti: `scope.pageTargetHistory` üçünü de
dayanağıyla taşıyor ve tekil `pageTargetBootstrapHypothesis` alanı
**kaldırıldı** — aynı sayı iki yerde durursa er geç iki farklı şey söyler.

### 2.2 · Yeni kapı — `validate_spec § ⑦`

Sayfa hedefi masum bir sayı değildir: **14,99 $ fiyat noktasının
kendisidir.** Kapı dört şeyi denetliyor: geçmiş duruyor mu · her kayıt
DOLU bir dayanak taşıyor mu · zincir kesintisiz mi · yürürlükteki hedef ve
telif dayanağı son kayıtla aynı mı.

`validate_spec`: 61 → **86 denetim**.

### 2.3 · Kapı ilk koşusunda KENDİ iki deliğini buldu

| Kurgu | İlk hâl | Neden kaçırdı |
|---|---|---|
| `basis: ""` | ❌ yeşil | `is not None` — alan VARDI ama BOŞTU |
| **aradan 148 kaydı düşürülür** | ❌ yeşil | yalnızca SON kayıt denetleniyordu |

İkincisi kapının varlık sebebiydi ve tam da onu kaçırıyordu: aradan bir
kaydı düşürmek, **bir supersession'ın izini silmenin en sinsi biçimidir**
— 148 hiç var olmamış gibi görünür ve iki 144 tek bir karara çöker.
Düzeltme örneği değil **sınıfı** kapattı: zincir kuralı aradan da baştan
da sondan da kayıt düşürmeyi imkânsız kılıyor.

---

## 3 · A10 — kurucu aşması Faz 5'e genişledi · **K34**

| Yetkilenen faz | Karar | Tavan |
|---|---|---|
| `phase3` | K27 | `phase1` |
| `phase4` | K30 | `phase1` |
| **`phase5`** | **K34** | **`phase1`** |

Üçüncü sütun bu tablonun asıl işidir: **aşma üç kez uzadı ve tavan bir
kez bile kalkmadı.**

`phaseOverride.extensionHistory` doğdu: tekil `extendedTo` alanı üçüncü
genişletmede **K30'u ezecekti** — aşmanın ne kadar uzadığı, tam da
uzadıkça görünmez olacaktı.

`doesNotImply` beşinci maddeyi aldı:
**"Faz 5 görsel üretiminin bitmesi A10'u kapatmaz."**

### 3.1 · Uydurulmayan şeyler

```
çocuk oturumu          0   uydurulmadı
çocuk geri bildirimi   0   uydurulmadı
tamamlanma oranı       —   uydurulmadı
ebeveyn onayı          0   uydurulmadı
testçi kaydı           0   uydurulmadı
fizikî prova           0   uydurulmadı
```

`externalValidation` **`pending`** kaldı. A10 **kapatılmadı**.
`qa_language § ⑤` bunu her koşuda uyarıyla hatırlatıyor.

---

## 4 · Ön madde — 9 sayfa · 8 bölüm

| Bölüm | Sayfa | Rol | Gövde |
|---|---:|---|---:|
| `title-page` | 1 | production | 22 |
| `copyright-page` | 1 | production | 90 |
| `mission-order` | 1 | teaching | 330 |
| `how-a-page-works` | **2** | teaching | 320 |
| `star-box-and-seal` | 1 | teaching | 272 |
| `the-route` | 1 | teaching | 208 |
| `when-you-are-stuck` | 1 | teaching | 190 |
| `before-you-start` | 1 | teaching | 227 |
| **toplam** | **9** | | **1.659** |

Yol haritasının adıyla istediği dört parça da var: **görev emri ·
araçlar · mühür sayfası · ipucu kuralı.**

### 4.1 · Ton — jenerik açılış yok

Kurucu talimatı § 7 dört kalıbı adıyla yasakladı (*Welcome to · Get
ready to · Embark on · Discover*). Hiçbiri kullanılmadı ve
`qa_readability § ⑨` bunu mekanik olarak denetliyor. Kitap kendi sesiyle
açılıyor:

> *"This book is a job, and the job is yours."*

### 4.2 · ⭑ BULGU E1 — kullanım kılavuzu KULLANIMDAN SONRA geliyordu

Faz 4 arka maddeye `how-to-use` ve `hint-rule` koymuştu ve ikisi de
**çocuğa** sesleniyordu. Ama bir çocuk kitabın nasıl çalıştığını
**131. sayfada** öğrenemez: oraya vardığında kitap bitmiştir.

> ### Bir kullanım kılavuzu, kullanımdan SONRA gelirse bir kılavuz değil bir ÖZETTİR.

Düzeltme **sayfa sayısına dokunmadı**. Üç sayfanın **okuru** değişti:

```
ÖN MADDE (9 s.)   → çocuk · başlamadan önce · İŞLETİM
ARKA MADDE (3 s.) → yetişkin · takılınca · DESTEK
```

Aynı bilgi iki kez basılmıyor; **iki ayrı okur iki ayrı şey okuyor.**

Ve ayrım bir beyandan ibaret bırakılmadı — **ölçüldü**:

| Ölçüm | Değer | Eşik |
|---|---:|---:|
| ön madde ↔ arka madde en yüksek örtüşme | **0,238** | 0,55 |
| ön madde iç örtüşmesi | **0,197** | 0,55 |

En yüksek çift tam olarak E1'in ayırdığı çifttir
(`when-you-are-stuck` ↔ `hint-rule`) ve **0,238**'dedir: ayrım gerçekten
yazılmış. `qa_echo § ⑦` bunu kilitliyor.

### 4.3 · ⭑ BULGU E2 — örnek sözcük bir MÜHÜR SÖZCÜĞÜYDÜ

Mühür kuralını anlatan sayfa bir örnek kullanıyordu ve örnek sözcük
`CONDOR`du. **CONDOR `jaguar-condor` bölgesinin mühür sözcüğüdür.**

Ön madde o hâliyle bir bölgenin cevabını **kitabın beşinci sayfasında**
basardı — ve sızıntının yönü en kötü yöndü: çocuk henüz tek bir sayfa
çözmeden, kitabın **tek kendi kendini doğrulama aygıtı** ölürdü.

`LANTERN` seçildi: ne mühür sözcüğü, ne yıldız sözcüğü, ne bölge adı.

### 4.4 · ⭑ BULGU E3 — görev emri bir mühür sözcüğü taşıyordu

Görev emri cümlesi `sun-savanna` bölgesinin mühür sözcüğünü **sıradan
bir sözcük olarak** taşıyordu. Sızıntı olarak okunma riski düşüktü ama
ön madde mühür kelime dağarcığının **en yoğun olduğu yerdir**: aynı
sayfalarda *seal*, *star box* ve *letter* geçer ve bir çocuk bağlantıyı
orada kurabilir.

Cümle yeniden yazıldı ve **kapı daraltılmadı**. Yeni hâli bölgenin kendi
`terrainLine`'ıyla da uyumlu.

### 4.5 · Yeni kapı — `qa_answerkey § ⑩`

E2 ve E3'ü **bu kapı buldu**, bir insan değil. Altı denetim: yol
haritasının istediği parçalar · sayfa bütçesi · gerekçe · gövde · mühür
sessizliği · örnek sözcüğün gerçek bir yıldız sözcüğü olmaması.

`qa_answerkey`: 25 → **35 denetim**.

---

## 5 · Kelime modeli — **kapandı**

| Katman | Kelime |
|---|---:|
| Proza (talimat · field note · ipucu · ölçüt · ebeveyn notu) | 9.000 |
| Levha mobilyası (`pagePrints`) | 7.889 |
| Bölge açılışları | 1.031 |
| Final görev | 786 |
| Arka madde iskeleti | 643 |
| **Ön madde** | **2.266** |
| **TOPLAM** | **21.615** |

Hedef **22.000 ± %15** = 18.700–25.300 → **bantta**, sapma **%-1,8**.

### 5.1 · Yol haritasının ~4.000 tahmini tutmadı — ve doldurulmadı

Yol haritası ön madde için ~4.000 kelime tahmin ediyordu; ölçülen
**2.266**. Fark **doldurulmadı** ve doldurulmaması bilinçlidir:

> **Kurucu talimatı § 6:** *"Do NOT add meaningless prose merely to hit
> 22.000. CONTENT QUALITY > WORD COUNT."*

Sekiz sayfalık bir ön maddeye 4.000 kelime, sayfa başına 500 kelime
demektir — 8,5×11 formatında bir çocuk kitabı için **okunamaz bir
yoğunluk**. Model bantta ve tahmin yanlıştı; düzeltilecek şey metin
değil tahmindi.

### 5.2 · Okunabilirlik — ön madde içerikten KOLAY

| Register | Ort. kelime/cümle | FK | Bant |
|---|---:|---:|---|
| Talimat | 7,91 | **2,53** | 5–11 · ≤4,0 ✅ |
| Field note | 12,40 | **5,39** | 9–14 · 3,0–5,9 ✅ |
| İpucu | 9,93 | **3,74** | ≤4,5 ✅ |
| **Ön madde** | **11,09** | **4,22** | 9–16 · ≤6,5 ✅ |

Değişmez: **fk(ön madde) 4,22 ≤ fk(field note) 5,40 + 0,5** ✅

Ön madde kitabın **en zor metni değil**: field note'tan 1,18 sınıf kolay.
Kurucu talimatı § 8 bunu adıyla şart koşuyordu.

`qa_readability`: 11 → **18 denetim** (yeni § ⑨ ön madde registeri).

⚠ **Üretim sayfaları ölçüme KATILMAZ.** Bir telif uyarısı hukukî bir
cümledir (40 kelime) ve çocuğa okutulmaz. İlk hâl onu registere katıyordu
ve bandı yalancı biçimde yukarı çekiyordu.

> **Bir ölçüm, ölçmemesi gereken şeyi ölçerse, düzeltilecek şey metin
> değil ÖLÇÜMDÜR.**

---

## 6 · Varlık envanteri — **158**, hesaplandı

| Sınıf | Adet | Kaynak |
|---|---:|---|
| aktivite görseli | **120** | `book.json § visualSpec` |
| kültür vinyeti | **22** | `culture_index.json` |
| mühür damgası | **6** | `region_index § sealStampMotif` |
| rozet | **6** | `DESIGN_SYSTEM § 1 · § 4 · § 7` |
| ön madde diyagramı | **4** | `book.json § frontMatter § visualNeed` |
| **TOPLAM** | **158** | *yol haritası tahmini 150* |

Kurucu talimatı § 10 bunu adıyla şart koşuyordu: *"Do NOT blindly assume
exactly 150 files. Calculate the actual final asset inventory."*

**158, 150'ye yuvarlanmadı.** Envanter dört kaynaktan **türetilir** ve
`asset_manifest.py --check` bayatlığı her koşuda denetler.

### 6.1 · Envanter İKİ katmandır — ve bu bir kilittir

İlk hâl **tek** dosya yazıyordu ve o dosya takip ediliyordu. İçinde
`requiredLabels` ve `restrictions` vardı — ve Faz 5'te eklenen ölçüm
kısıtları cevabın **kendisini** taşıyor:

> *"Exactly these knot counts must be countable: cord A three in the tens
> and four in the ones; …"*

Bu bir görsel şartnamesidir **ve aynı zamanda cevaptır**. K10 cevabın
public depoda durmasını yasaklar — ve `image_prompts.py` **Faz 2'den beri
tam olarak bu gerekçeyle** şartname metnini kütüphaneye almıyordu.

> ### Bir kural yalnızca onu bilen dosyalarda geçerliyse, bir kural değil bir ALIŞKANLIKTIR.

| Katman | Ne taşır | Depoda |
|---|---|---|
| `ASSET_MANIFEST.json` | kimlik · ölçü · yol · **sayım** · sha256 | ✅ |
| `ASSET_MANIFEST.local.json` | tam kayıt · etiket · kısıt | ❌ |

Public dosya içerik taşımaz ama **sağlamasını** taşır: özel kayıt
sürüklenirse `privateSha256` değişir ve denetlenebilir kalır.

`validate_structure § ⑤b` doğdu: takip edilen **hiçbir** dosya
`requiredLabels` / `restrictions` / `pagePrints` **içeriği** taşıyamaz.

### 6.2 · `.gitignore`'da iki katman eksikti

`final/` ve `rejected/` Faz 5'te doğdu ve ikisi de **görsel taşır**.
`rejected/` özellikle tehlikeliydi:

> **Reddedilen bir ham görsel, kabul edilenden daha az gizli değildir.**

---

## 7 · Ham varlıklar — **0 / 158**

```
ham görsel üretimi   ⏳ KURUCUYA AİT
üretilmiş ham varlık    0
uydurulmuş varlık       0
```

Bu bir **kusur değil bir sıra**dır: `PROJECT_CONTEXT § 10` ham görsel
üretimini açık kalem olarak kurucuya veriyor. Faz 5'in işi hattı kurmak
ve **hattın çalıştığını kanıtlamaktı** — ikisi de yapıldı.

`asset_pipeline.py` ham varlık yokken **bir hata bildirmez**:

> *"⊘ hiç ham varlık yok — hat BOŞ KOŞTU. Ham görsel üretimi KURUCUYA
> aittir; hat hazırdır."*

---

## 8 · İşlenmiş varlıklar — hat · **K35**

```
07_ASSETS/raw/         KURUCUNUN çıktısı · DEĞİŞMEZ · asla üzerine yazılmaz
07_ASSETS/processed/   CLI ÜRETİR · her zaman RAW'dan YENİDEN üretilebilir
07_ASSETS/final/       basıma hazır · processed'dan türer
07_ASSETS/rejected/    şartnameyi ihlal eden RAW · SİLİNMEZ, AYRILIR
```

Hat yedi adım koşar: ölçüm → gri tonlama → **düz kenar kırpma** →
ölçekleme → **hedef kutuya doldurma** → 300 dpi → **köken kaydı**.

### 8.1 · İki kural, ikisi de mekanik

**① RAW'A ASLA YAZILMAZ.** Ham görsel yeniden üretilemez: üreteç
deterministik değildir, aynı prompt aynı görseli iki kez vermez.

**② HEDEFTEN KÜÇÜK RAW BÜYÜTÜLMEZ — REDDEDİLİR.** Yukarı örnekleme
çözünürlük kazandırmaz; yalnızca 300 dpi iddiasını **yalan** hâline
getirir. Ret **silinmez**: `rejected/` altına gerekçesiyle kopyalanır.

> **Silinen bir ret, aynı hatanın ikinci kez yapılmasını serbest bırakır.**

### 8.2 · Hattın kendi kusuru — ilk hâl kendi çıktısını reddettiriyordu

İlk hâl yalnızca hedefin **içine sığdırıyordu**. Sonuç: kenar boşluğu
kırpılmış her görselin oranı hedeften kayıyordu ve kapı onu *"yanlış
oran"* diye reddediyordu — oysa kusur görselde değil **hattaydı**.
Kırpma oranı değiştirir; bu kaçınılmazdır.

> ### Bir hat, kendi ürettiği çıktıyı kapısına reddettiriyorsa, düzeltilmesi gereken kapı değil HATTIR.

Doğrusu: sığdır, sonra hedef kutuya **beyazla doldur**. Sanata
dokunulmaz, kutu garanti edilir — ve **doluluk oranı ölçülür**, yani
doldurma yanlış şablonu **gizlemez, görünür kılar**.

---

## 9 · Nihai varlıklar

`final/` katmanı **bir karardır**: doğrulamadan geçmiş bir varlık basıma
hazırdır ve o an damgalanır. `--final` bayrağı `processed/` → `final/`
taşır ve köken kaydını birlikte götürür.

Bugün **0 nihai varlık** vardır ve olması gereken de budur: ham varlık
yok.

---

## 10 · Görsel prompt kütüphanesi — 158 dolu prompt

Envanterle **aynı iki katman**, aynı gerekçe:

| Dosya | Ne taşır | Depoda |
|---|---|---|
| `IMAGE_PROMPT_LIBRARY.html` | şablon · ölçü · politika · `{PRINT_LIST}` | ✅ |
| `IMAGE_PROMPT_LIBRARY.local.html` | **158 DOLU prompt** | ❌ |

Dolu sürüm kurucunun **gerçek çalışma arayüzüdür**: her varlık için tek
başına yeterli bir kutu — şablon + `PRINT EXACTLY` listesi + zorunlu
etiketler + sayfaya özgü kısıtlar + ortak olumsuzlar + çıktı ölçüsü.
**158 kutu, 158 kopyala düğmesi.**

Dört yeni **sınıf** şablonu doğdu: kültür vinyeti · mühür damgası ·
rozet · ön madde diyagramı. Vinyet bir levha değildir, damga bir
illüstrasyon değildir — şablonu düzenden değil **sınıftan** alırlar.

### 10.1 · ⭑ BULGU V1 — bir kısıt sınıfı GERÇEKTE HİÇ ULAŞMIYORDU

Kültürel güvenlik kısıtları `culture_index`te **Türkçedir** (proje dili)
ve promptlar onları olduğu gibi taşıyordu. Ama bu satırlar görseli
**üreten** tarafa gider ve bir üreteç Türkçe bir emri güvenilir biçimde
uygulamaz.

> ### Uygulanamayan bir kısıt, yazılmamış bir kısıttır.

Ve tam olarak **en önemli** kısıtlar bunlardır: kutsal adın bir şifrenin
cevabı olmaması, ritüelin taklit edilmemesi, yaşayan bir topluluğun
*"yok olmuş"* diye anlatılmaması.

22 kültürün **59 yasak biçiminin** İngilizce karşılığı yazıldı
(`forbiddenFormsEn`). Türkçe alan **authoritative kalır** ve bütün
kapılar onu okumaya devam eder; İngilizce alan **yalnızca prompt katmanı
içindir**.

| | Önce | Sonra |
|---|---:|---:|
| Prompta ulaşan kültürel güvenlik satırı | **0 anlaşılır** | **235** |
| Çevrilmemiş kalan | 59 | **0** |
| Türkçe kalıntı | — | **0** |

### 10.2 · Ve son bir kısıt yine eşleşmedi: **noktasız-ı**

`'CEVABI'.lower()` Python'da `'cevabi'` verir, `'cevabı'` değil. Nokta
Türkçede anlamlıdır ama Unicode küçültmesi onu bilmez.

Faz 4 § 28 ④ aynı kusuru `qa_age`'de **üçüncü kez** görmüş ve örneği
değil **sınıfı** kapatmıştı. Burada da liste büyütülmedi, **katlama**
yapıldı.

`qa_assets § ⑧b` doğdu: iki liste aynı uzunlukta mı, *"İngilizce"* alanda
Türkçe kalıntı var mı.

---

## 11 · Görsel doğrulaması — `qa_assets` · 33 denetim

```
① envanter tamlığı   ② kimlik            ③ katman haritası
④ RAW dokunulmazlığı ⑤ ölçü              ⑥ zorunlu etiket
⑦ cevap gözlemlenebilirliği              ⑧ kültürel güvenlik
⑨ mühür sessizliği   ⑩ ret kaydı
```

Kapı **ikiye bölünmüştür** ve bu bilinçlidir:

```
ŞARTNAME denetimleri  → HER ZAMAN koşar    (①②③⑥⑦⑧⑨)
DOSYA denetimleri     → varlık VARSA koşar (④⑤⑩)
```

Böylece kusurlu bir şartname, **görsel üretilmeden önce** yakalanır.

> **Faz 5'in en pahalı hatası, kusurlu bir şartnameye göre üretilmiş
> kusursuz bir görseldir: görsel doğrudur, sayfa çözülemez.**

### 11.1 · ⭑ ALTI ŞARTNAME KENDİ LEVHASIYLA ÇELİŞİYORDU

Faz 4'ün 120 şartnamesi hiçbir görsele karşı sınanmamıştı — sınanamazdı,
çünkü görsel yoktu. Kapı doğduğunda şartname katmanını sınadı:

| # | Sayfa | Ne çelişiyordu |
|---|---|---|
| **D1** | `andean-altitude-map` | `subject` *"all four bands"* deyip **beş** ad sayıyordu; etiketin biri cümle parçasıydı |
| **D2** | `turkic-yurt-plate` | `uuk` etiketi levhada **basılı değildi** |
| **D3** | `persian-joined-letters` | `مدرسه` hiçbir levhada, adımda ve cevapta **yoktu** |
| **D4** | `vietnamese-red-river-map` | ⭑ **BLOKLAYICI** — etiket *"tinted pale"* istiyordu, levha *"no tinting"* diyor |
| **D5** | `hawaiian-island-chain-map` | ⭑ etiketler **sayısal yaş** istiyordu, levha **göreli sözcük** basıyor; ada adları etikette **hiç yoktu** |
| **D6** | `japanese-turtle-time-plate` | `Meiji` bir **dönem** adı; adım 1 **yıl** okumak istiyor |
| **D7** | `inuit-ice-window-draw` | Kademe C, kısıt `culture_index`e **izlenebilir değildi** |

**D4 ve D5 sayfayı bozardı, süslemezdi:**

- **D4** — boyama **çocuğun görevidir** (adım 2). Tintlenmiş bir harita
  sayfayı **önceden çözerdi** ve *"No answer may be visible"* kısıtını
  ihlal ederdi. Etiket ayrıca var olmayan bir bandı (*ten metres*)
  istiyordu; anahtar **iki** bantlıdır.
- **D5** — sayılar basılsaydı görev bir **sıralama** değil bir
  **aritmetik** olur, cevap uzayı değişirdi. Ve ada adları zorunlu
  etikette hiç yoktu: **adı basılmayan bir ada numaralandırılamaz.**

Yedisi de düzeltildi ve her biri `designCorrection` alanıyla kayda geçti.

### 11.2 · Kapının KENDİ iki hatası — ve ikisi de aynı sınıftan

| Kapı hâli | Sonuç | Kusur |
|---|---|---|
| sabit cümle aradı (*"No answer may be visible"*) | **57 doğru sayfa kırmızı** | Faz 4 kuralı sayfaya ÖZGÜ yazmıştı ve o hâli **daha güçlüdür** |
| evrensel kuralı 158 şartnamede aradı | **55 kırmızı** | kural zaten TEK yerde duruyordu (`image_prompts § NEGATIVE`) |

İkisinde de kapıyı yeşile çevirmenin **en ucuz yolu doğru olanı
bozmaktı**: kesin kısıtları silip yerine kalıp yapıştırmak, ya da
evrensel bir kuralı 158 yere kopyalayarak 158 kez sürüklenebilir hâle
getirmek.

> ### Bir kapı doğru olanı pahalı hâle getiriyorsa, düzeltilmesi gereken KAPIDIR. *(Faz 3 § 21.1 · Faz 4 § 24.1 · ve şimdi bir kez daha)*

Kapı artık **cümleyi değil sınıfı** arıyor, ve evrensel kuralı **tek
kaynakta** denetliyor.

---

## 12 · Cevap gözlemlenebilirliği — **43 / 43**

Faz 4'ün kuralı:

> **Bir cevap ölçülebilir diye yazıldıysa, görsel şartnamesi o ölçümü
> MÜMKÜN KILMAK ZORUNDADIR.**

Ölçüm ölçüldü: cevabı bir **sayıya, sıraya, konuma ya da glife** dayanan
**43** sayfa var. Faz 4 bunların **20'sinde** kısıt yazmıştı.
**23'ünde yoktu.**

> **Üreteç eline bırakılmış bir ölçüm, üretecin değiştirebileceği bir
> cevaptır.**

23 sayfaya **49 kısıt** eklendi ve her biri o sayfanın **kendi
cevabından** türetildi. Örnekler:

- *"The four cards must be printed in an order that is NOT the answer
  order; no card may sit in its own numbered position."* — bir sıralama
  sayfası, kartları cevap sırasında basarsa **önceden çözülmüştür**
- *"Exactly these knot counts must be countable, register by register…"*
- *"The age bands must be printed as WORDS exactly as supplied and never
  as figures: printing numeric ages would turn an ordering task into
  arithmetic."*
- *"The six hangul place names must be reproduced EXACTLY as supplied; no
  letter may be redrawn, simplified or approximated."*

Ve denetim **uyarı olmaktan çıkarıldı**:

> **Yalnızca uyaran bir kural, uyulmayan bir kuraldır.**

Artık kısıtsız bir ölçüm sayfası eklemek kapıyı **kırmızı** yakar.

---

## 13 · Kültür vinyetleri — 22 / 22

Her kültüre **bir** vinyet, **kendi adıyla**. `qa_assets § ②`
yirmi ikisinin de var olduğunu denetliyor: bir kültürün yalnızca
bulmacada görünmesi **K13'e aykırıdır**.

Vinyet **bağlam sanatıdır, cevap değildir** (kurucu talimatı § 18) ve bu
mekanikleştirildi: vinyetin `requiredLabels`'ı **tek** öğe taşır —
kültürün kendi adı. Bir vinyete etiket eklemek onu sessizce bir aktivite
levhasına çevirir ve `qa_assets § ⑥` bunu kırmızı yakar.

Şablon üç şeyi birden şart koşuyor:

- *"documented, everyday objects or landscape features that belong to
  this culture and to no other"* — **jenerik "fantastik egzotik" yok**
- *"It must read as a place people LIVE, not as a ruin, a museum case or
  a costume"* — **yaşayan gelenek yaşayan gösterilir** (16 kültür)
- *"No people, no faces, no ceremony, no sacred object"*

Ve her vinyet, kültürünün **bütün** yasak biçimlerini taşır — vinyet saf
kültürel tasvirdir, orada tam kapsam gerekir.

---

## 14 · Mühür ve rozet varlıkları — 12

| Sınıf | Adet | Ne |
|---|---:|---|
| mühür damgası | 6 | bölge başına bir damga · motif `region_index`ten |
| rozet | 6 | üç zorluk işareti · yıldız kutusu · mühür sayacı · sertifika damgası |

> ### ⭑ HİÇBİRİ BİR HARF TAŞIMAZ ⭑

Damga bir **kimliktir**: bölge, rota, motif. Mühür sözcüğü **çocuğun
kendi yazdığı şeydir** ve basılı hiçbir yerde durmaz. `requiredLabels`
bu yüzden **boştur** ve `qa_assets § ⑨` bir harf isteyen damgayı kırmızı
yakar.

Şablon bunu ayrıca **prompta** yazıyor:

> *"⭑ THE STAMP CARRIES NO LETTERS AND NO WORDS. The letter slots are
> drawn EMPTY… A letter printed here would destroy the only self-check in
> the book."*

Çentik **çizilir ama numaralandırılmaz**: numara dizgi katmanında basılır.

---

## 15 · Editoryal yakınsama

> ⚠ **İÇ İNCELEME ÇOCUK DOĞRULAMASI DEĞİLDİR.**
>
> İnceleme *"bir yetişkin bu talimatı harfi harfine okuduğunda kusur
> görüyor mu"* sorusunu sorar. Çocuk testi *"sekiz yaşındaki onu
> yardımsız yapabiliyor mu"* sorusunu sorar. İkincisini yalnızca bir
> çocuk cevaplayabilir.
>
> **INTERNAL EDITORIAL VALIDATION — NOT CHILD VALIDATION.**

Bağımsız bir editoryal alt-ajan koşturuldu ve **kitabın tamamını** okudu:
120 aktivitenin 120'si, altı bölge açılışı, final görev, arka madde ve
Faz 5'te yazılan ön madde. **37 mühür kutusunun aritmetiği ilk kez birer
birer yeniden hesaplandı.**

| Sınıf | Bulgu | Karşılık |
|---|---:|---|
| **A · BLOKLAYICI** | **13** | **13 düzeltildi** |
| **B · CİDDİ** | **26** | 4 düzeltildi · 22 kayıtlı |
| **C · KÜÇÜK** | 19 | 19 kayıtlı |
| **D · GÖRSEL KISIT** | 8 | 3 düzeltildi · 5 kayıtlı |
| **Toplam** | **66** | **20 düzeltildi · 46 kayıtlı** |

Ayrıntı: [`06_REPORTS/LINE_EDITOR_REPORT.md`](LINE_EDITOR_REPORT.md)

> Faz 4 on bulgu bulmuştu; bu inceleme altmış altı buluyor. **Bu bir kalite
> düşüşü değildir:** Faz 4 altmış YENİ sayfayı inceledi, bu inceleme
> kitabın TAMAMINI ve daha hiç incelenmemiş ön maddeyi inceledi.

### 15.1 · Raporun kendisi kapıya takıldı

Tam kayıt her bulguyu **sayfadan birebir alıntıyla** kanıtlıyor ve o
alıntılar aktivite prozası ile **cevap** taşıyor. `validate_structure § ④⑤`
raporu bir sızıntı olarak yakaladı.

> ### Bir inceleme raporu, incelediği metni alıntılayarak kanıtlar — ve o alıntı, metnin kendisi kadar korumalıdır.

Rapor, envanterin ve prompt kütüphanesinin izlediği **aynı ayrıma** tabi
tutuldu: takip edilen özet + `.gitignore`'lu tam kayıt. **Faz 5'te bu
ayrım üçüncü kez kuruldu** ve üçünde de aynı kural geçerliydi — kuralın
kendisi yeni değildi, ona uymayan dosyalar yeniydi.

---

## 16 · Line editor bulguları — on üç bloklayıcı

| # | Sayfa / bölüm | Kusur | Karşılık |
|---|---|---|---|
| **A1** | 9 mühür sayfası | Basılı `★` **harf sırası değil yuva numarasıydı**; ikisi aritmetik olarak imkânsız (6 harflik sözcükte ★7, 4 harflikte ★5). `monsoon`'un yedi mühür sayfasının **altısı** — o bölgenin sözcüğü **kurulamazdı** | ✅ |
| **A2** | ön madde + 6 açılış + `DESIGN_SYSTEM § 4` | Basılı kural iki **ayrı** büyüklüğü aynı ilan ediyordu; ölçüm: **27/37 sayfada farklılar** | ✅ |
| **A3** | ön madde + arka madde | *"Hiçbir sayfa başkasının cevabına bağlı değil"* — üç karşı örnek | ✅ |
| **A4** | `akan-story-web-map` | Beş kasaba **dört** bacak verir; cevap 100 mil ve **altı** kasaba ister | ✅ |
| **A5** | `aztec-maize-journey-sort` | **Faz 5'in kendi ölçüm kısıtı** levhanın konum göndermesiyle çelişti | ✅ |
| **A6** | `maori-macron-length` | Sayfa **üç farklı sayfa** olarak tarif edilmişti | ✅ |
| **A7** | `aztec-town-sign-make` | Gri tonlamalı örnekten **renk** kopyalatıyordu | ✅ |
| **A8** | `norse-runestone-read` | *"Tek kişi"* aslında **iki** kişiydi | ✅ |
| **A9** | `persian-joined-letters` | Adım tekil, cevap **iki** şekil; ölçüt levhada basılı değildi | ✅ |
| **A10** | `finnish-vowel-harmony` | Adım 3'ün **üç** geçerli cevabı vardı · test sözcüğü kuralı **bozmuyordu** · field note cevabı veriyordu | ✅ |
| **A11** | `akan-day-name-pairs` | Adım **başka bir sayfanın** levhasını gerektiriyordu | ✅ |
| **A12** | `zulu-click-letters` | `safe-with-adult` sayfanın **zorunlu** ebeveyn notu yoktu | ✅ |
| **A13** | ön madde + 4 sayfa | Ön madde imlâ kuralını **kendi sayfasında** çiğniyordu · 14 ad | ✅ |

### 16.1 · ⭑ A1 ve A2 üç kapının ARASINDAN geçti

| Kapı | Ne denetliyordu | Sonuç |
|---|---|---|
| `qa_solvable § ⑦` | mühür **harfi** yeniden hesaplanıyor mu | ✅ 37/37 |
| `qa_design § ②` | yıldız kutusu **var mı** | ✅ 37/37 |
| `qa_progression § ②` | harf **gerçek bir cevaptan** mı türüyor | ✅ 37/37 |

Üçü de doğruydu. Harf doğruydu, kutu vardı, türetme doğruydu.

> ### Kimse BASILI SAYININ doğru sayı olduğunu sormamıştı.

`qa_progression § ⑧⑨` doğdu ve ikisini birden kapatıyor: basılı `★` harf
sırasıdır · hiçbir `★` sözcüğün dışına düşemez · **ölçüm ayrıkken hiçbir
yer "aynı numaralı yuva" kuralını basamaz.**

`qa_progression`: 7 → **14 denetim**.

### 16.2 · Faz 5'in kendi kusurları — üçü

Bu incelemenin en değerli tarafı, **Faz 5'in kendi işini** denetlemesiydi:

| # | Ne | Nereden geldi |
|---|---|---|
| **A5** | ölçüm kısıtı levhanın konum göndermesini yasakladı | § 12'nin 49 kısıtı |
| **A13** | ön madde imlâ kuralını kendi sayfasında çiğnedi | § 4'ün ön maddesi |
| **B22** | kit sayfası **cetvel** istiyordu; 120 sayfanın **hiçbiri** kullanmıyor | § 4'ün ön maddesi |

B22'nin ölçümü: `coloured-pencils` **38** sayfa · `read-aloud-partner` 2 ·
`mirror` 1 · `string` 1 · **`ruler` 0**. *"Kit'in tamamı bu"* diyen bir
sayfa ölçümle çelişemez.

### 16.3 · Kayıtlı kalan 46 bulgu

| Sınıf | Adet | En büyük küme |
|---|---:|---|
| B · ciddi | 22 | **9 sayfada field note cevabı söylüyor** |
| C · küçük | 19 | sayım, birim ve etiket uyuşmazlıkları |
| D · görsel kısıt | 5 | eksik `requiredLabels` · `pagePrints`'e sızmış tasarım notu |

Dokuz field-note sızıntısı **aynı sınıftan** ve Faz 4 § 27.3 aynı sınıfı
dört sayfada bulmuştu: `qa_solvable § ⑧` anlamlı sözcük örtüşmesiyle
çalışıyor ve **kısa cümleler eşiğin altında kalıyor**.

> **Kapı yanlış değil, ÇÖZÜNÜRLÜĞÜ yetersiz — ve bu bir kapı gevşetme
> gerekçesi değil, bir İNSAN OKUMASI gerekçesidir.**

⚠ Ayrıca ölçüldü ve **Faz 6'ya taşındı:** `writingSpaceLines` alanı ile
`pagePrints`'in saydığı yazma satırı **120 sayfanın 63'ünde** uyuşmuyor.
İki alan da satır sayısı iddia ediyor; dizgiden önce **biri yetkili ilan
edilmelidir**.

---

## 17 · qa_echo — 11 denetim · yeşil

| Ölçüm | Değer | Eşik |
|---|---:|---:|
| En yüksek field note örtüşmesi | 0,33 | 0,55 |
| Ön madde ↔ arka madde | **0,238** | 0,55 |
| Ön madde iç örtüşmesi | **0,197** | 0,55 |

Yeni **§ ⑦** E1 kararını kilitliyor: arka madde ön maddeyi tekrar
etmeye başlarsa kapı yanar, ve her arka madde bölümü **okurunu beyan
etmek zorundadır**.

> **Beyansız bir ayrım, bir sonraki yazarın farkında olmadan geri
> alabileceği bir ayrımdır.**

Kapı hiçbir zorunlu kültürel terimi cezalandırmadı; yanlış-pozitif testi
geçiyor.

---

## 18 · qa_design — 19 denetim · yeşil

Faz 4'ten **değişmedi**. `DESIGN_SYSTEM.md` **v1.0**'da kaldı ve Faz 5
tek bir satırını değiştirmedi: kurucu talimatı § 20 bunu adıyla şart
koşuyordu (*"Phase 5 is ASSET REALIZATION, not DESIGN REINVENTION"*).

Tek belge değişikliği § 9'daki **bayat bir referanstı**: *"Sayfa hedefi
148 (K19)"* satırı K33'e güncellendi. Bir tasarım dizgesi kendisinden
önce alınmış kararları yeniden açmaz — ama **yanlış** de anmamalıdır.

Kapının bir uyarısı duruyor (*"ilişki tek bir maddede durmuyor"* · 6
madde) ve **Faz 4'tekiyle birebir aynı**: meşru bir **çıkarım
tasarımıdır**, Faz 4'te bir insan baktı ve Faz 5'te değişmedi.

---

## 19 · qa_answerkey — 35 denetim · yeşil

25 → **35**. Yeni **§ ⑩** ön maddeyi denetliyor (§ 4.5).

Cevap anahtarı **120/120** kayıt taşımaya devam ediyor: 105 kapalı cevap
+ 15 açık uçlu ölçüt. **Altı mühür sözcüğünün hiçbiri anahtarda yok** ve
olmayacak.

Kapının bir uyarısı duruyor: *"mühür sözcükleriyle aynı yazılan 4 sıradan
sözcük anahtarda geçiyor"* — Faz 4 § 24.1'de incelendi, **yanlış
pozitiftir** ve sözcükler ekrana **basılmadı**.

---

## 20 · Sayfa entegrasyonu — ve **BULGU P1**

### 20.1 · ⭑ İki sayının uyuşması bir doğrulama DEĞİLDİR

Faz 1 sayfa modeli ön maddeyi **8** sayfa sayıyordu ve o 8'in **ikisi**
`title-and-copyright` idi. Manuscript'in ön maddesi de **8** sayfaydı —
ama içinde **ne başlık ne künye sayfası vardı**.

```
page_budget.py  →  title-and-copyright 2 · mission-order 2 · how-to-use 1
                   hint-rule 1 · route-map 1 · seal-page 1        = 8

book.json       →  mission-order 1 · the-kit 1 · how-a-page-works 2
                   star-box 1 · route 1 · stuck 1 · before 1      = 8
```

> ### İki liste TOPLAMDA uyuşuyordu ve BAŞKA BİR KİTABI tarif ediyordu.

Basılı bir kitap **başlık ve künye sayfası olmadan basılamaz**. İkisi de
yoktu ve **hiçbir kapı bunu göremezdi**: ikisi de doğru toplamı
veriyordu.

Bu tam olarak K29'un eşiklerde yakaladığı kusur, bir kat aşağıda: elle
yazılmış iki sayı, mimari kayınca **aynı şeyi söylemeye devam eder**.

### 20.2 · Düzeltme içerik KISMADI

- `the-kit` bölümü `mission-order`ın **ayak paneline katlandı** —
  metnin tamamı duruyor, taşınan şey **bölüm sınırı**
- açılan yere kitabın gerçekten ihtiyaç duyduğu **iki sayfa** kondu
- ön madde **8 → 9** sayfa · ham model **143 → 144**

### 20.3 · Model artık ÖLÇÜYOR

Ön/arka madde ve final görev sayfa sayıları `page_budget.py` içine
**gömülüydü**. Faz 1'de doğruydu — manuscript yoktu. Faz 4 arka maddeyi,
Faz 5 ön maddeyi yazdı; o günden sonra elle yazılmış sayı bir tahmin
değil bir **risk** oldu.

Model artık manuscript'i **okur**. Gömülü tablo yalnızca manuscript
**yokken** (CI · K10) kullanılan bir yedektir ve rapor hangisinin
kullanıldığını **söyler** (`matterSource`). Bildirilen bütçe ile
bölümlerin toplamı da artık **ayrılamaz**.

### 20.4 · İki kapı ROL ayrımı öğrendi

Bir başlık sayfası **22 kelime** taşır ve doğrusu budur; bir telif
uyarısı **hukukî** bir cümledir ve çocuğa okutulmaz.

| Kapı | Ne öğrendi |
|---|---|
| `qa_answerkey § ⑩` | gövde şartı yalnızca `role: teaching` için · *"her bölümü production ilan etmek"* bir **kaçış kapısı değildir** (azami 2) |
| `qa_readability § ⑨` | ön madde registeri yalnızca öğretim sayfalarını ölçer |

Ve `⑩(a)` artık bölüm **adı** değil **işi** arıyor: `the-kit`
katlandığında kapı onu **kayıp sanmıştı** — oysa içerik duruyordu, yeri
değişmişti.

> **Bir kapı bölüm ADINI şart koşarsa, yeniden düzenlemeyi bir KAYIP
> sanar.**

---

## 21 · Nihai sayfa modeli

| Blok | Sayfa | Kaynak |
|---|---:|---|
| Ön madde | **9** | ⭑ ÖLÇÜLDÜ (manuscript) |
| Bölgeler (6) | **116,0** | ÖLÇÜLDÜ (6/6 gerçek içerik) |
| Final görev | **5** | ⭑ ÖLÇÜLDÜ (manuscript) |
| Arka madde | **14** | ⭑ ÖLÇÜLDÜ (manuscript) |
| **ham model** | **144,0** | |
| yuvarlanmış | 144 | |
| **forma hizalı (×4)** | **144** | |

| | Hedef | Ölçülen |
|---|---:|---:|
| **Sayfa** | **144** | **144** · sapma **%0,0** |
| Ciltsiz baskı | — | **3,45 $** |
| **Ciltsiz telif** | 5,55 $ | **5,55 $** · sapma **0,00 $** |
| Başabaş ACOS | — | **%37,0** |

> **Kurucunun onayladığı sayı artık bir tahminle değil bir ÖLÇÜMLE
> tutuyor.** Faz 4'te model 144'tü ve hedef 148 diyordu; Faz 5'te ikisi
> aynı şeyi söylüyor ve **ikisi de ölçümden geliyor**.

### 21.1 · Görsel entegrasyonu sayfa modelini DEĞİŞTİRMEDİ

Kurucu talimatı § 21 bunu ölçmeyi şart koşuyordu. Ölçüldü: **değişmedi.**
Gerekçe yapısaldır — görseller `pageWeight` alanına **zaten dâhildi**
(Faz 1'den beri: bir tam sayfalık gözlem levhası 1,0, iki sığan bir şifre
0,75). Faz 5 görselleri **üretmedi**, şartnamelerini **doğruladı**;
ağırlıklar değişmedi.

⚠ **Bu bir dizgi ölçümü DEĞİLDİR.** Gerçek dizgi (`interior.py`) Faz 6'ya
aittir ve o gün sayfa sayısı **yeniden ölçülmelidir**. Bugünkü 144 bir
**modeldir** ve model olduğunu söyler.

---

## 22 · Araştırma güncellemeleri

| Durum | Faz 4 | **Faz 5** |
|---|---:|---:|
| `inherited-verified` | 54 | **54** |
| `inherited-provisional` | 22 | **22** |
| Doğrulanmış iddia | 108 | **108** |

**Faz 5 yeni araştırma yapmadı ve yapmaması gerekiyordu:** yol haritası
Faz 5 § 7 devralma manifestosunun **dondurulmasını** istiyor.

Kurucu talimatı § 27 bir şart koşuyordu: *"If an unverified record
becomes necessary for an image, a caption, front matter, an activity or a
cultural note, then revalidate it before use."*

**Böyle bir durum oluşmadı ve bu ölçüldü:**

- Ön madde hiçbir yeni kültürel iddia taşımıyor — altı kültürü **adıyla**
  anıyor (`Yorùbá`, `Māori`, `Inuktitut`, `Skíðblaðnir`, `Osun-Osogbo`,
  `cholq'ij`) ve hepsi **zaten doğrulanmış** kayıtlardan geliyor.
- Görsel şartnameleri **yeni olgu üretmedi**: 49 yeni kısıtın hepsi o
  sayfanın **zaten doğrulanmış** cevabından türetildi.
- Vinyet promptları **belgelenmiş** nesne istiyor ve hiçbiri yeni bir
  iddia kurmuyor.

22 provisional kayıt **cevap üretmiyor** ve üretmedikleri için
`validate_inheritance` yeşil.

---

## 23 · Kültürel güvenlik bulguları

| Ölçüm | Değer |
|---|---:|
| Kültüre bağlı varlık | 142 (120 aktivite + 22 vinyet) |
| Kademe C / kısıtlı kültür varlığı | kısıt taşıyan **tümü** |
| Prompta ulaşan kültürel güvenlik satırı | **235** |
| Çevrilmemiş kalan | **0** |
| Vinyet — yaşayan gelenek beyanı | **16 / 16** |

### 23.1 · Bulgu D7 — bir Kademe C sayfası izlenebilir değildi

`inuit-ice-window-draw` avlanma yasağını **özünde** karşılıyordu
(*"No hunting scene and no human figure anywhere on the page"*) ama kısıt
`culture_index`e **izlenebilir değildi**.

> **İllüstratör politikayı okumaz, promptu okur.**

Kısıt künyesiyle yazıldı ve sayfanın kendi kısıtları **korundu**.

### 23.2 · Zorunluluk riske göre ölçeklenir

Kapının ilk hâli **her** kültür varlığından o kültürün **bütün** yasak
biçimlerini istiyordu. Bu yanlıştı ve yanlışlığı ince: bir sayfa rün
taşları hakkındaysa, prompta *"Loki'nin bahis bedeli"* uyarısı koymak o
sayfayı korumaz — yalnızca promptu uzatır.

> ### Okunmayan bir uyarı, olmayan bir uyarıdır. İlgisiz uyarı yığmak, ilgili olanı gizlemenin en kolay yoludur.

Zorunluluk artık riske göre ölçekleniyor: **Kademe C / kısıtlı** kültür
ve **her vinyet** tam kapsam ister; diğer aktivite sayfaları için sayfaya
özgü kısıt yeter — **ama en az bir tane ZORUNLUDUR**.

---

## 24 · Git ve CI

| | |
|---|---|
| Faz 5 dalı | `faz/5-yakinsama` |
| Commit | **10** |
| CI | **2 kırmızı koşu** (§ 24.0 · tek sebep) · düzeltildi · kalan hepsi yeşil |
| Açık PR | 0 |
| `.gate` | **`phase1`** — değişmedi |
| Depoda **olmayan** | `book.json` · `answer_key.json` · `seal_key.json` · `pilot_tr/` · **ham/işlenmiş/nihai/reddedilmiş görseller** · **`*.local.json`** · **`*.local.html`** |
| Depoda **olan** | kod · şema · kapılar · **envanter (içeriksiz)** · **prompt kütüphanesi (yer tutuculu)** · ölçüm raporları |

### 24.0 · ⚠ CI BİR KEZ KIRMIZI YANDI — ve sebebi bir kapı EKLEMEKTİ

Faz 5'in dokuzuncu ve onuncu push'unda CI kırmızı yandı (aynı sebep: ikincisi düzeltme gelmeden önce push edilmişti). Rapor bunu gizlemiyor,
çünkü kırmızının **sebebi** bu fazın en tekrar eden dersidir.

Kırmızıyı yakan adım benim eklediğim adımdı: *"ÜRETİLEN BELGELER bayat
mı"*. `image_prompts` doğru davrandı ve boş koştu; `update_docs`
davranmadı.

`BOOK_STATS` ve `ROADMAP_PROGRESS` manuscript'ten de beslenir (kelime
sayısı, yazılmış aktivite, sayfa modeli). Manuscript depoda **durmaz**
(K10) — yani CI'da üreteç **farklı** bir metin üretiyor ve o fark bir
bayatlık **değildir**: kaynak orada değildir.

> ### Bir bayatlık denetimi, kaynağın YOKLUĞUNU bir sürüklenme sanmamalıdır.

`asset_manifest.py` ve `image_prompts.py` aynı gerekçeyle aynı guard'ı
**zaten taşıyordu**; `update_docs.py` taşımıyordu ve **CI'a eklendiği anda
görünür oldu**. Kural yeniydi denemez: kural vardı, ona uymayan dosya
vardı.

Düzeltme sonrası CI ortamı yeniden ve tam olarak sınandı — takip edilen
dosyalarla, manuscript olmadan:

```
üç üreteç (--check)     → çıkış 0
on altı kapı            → hepsi yeşil
selftest                → yeşil (177 denetim · manuscript'e bağlı bölümler atlandı)
```

Faz 5'in geri kalanında CI kırmızı yanmadı: her batch **yerel
`qa_all.sh` yeşil olduktan sonra** push edildi.

### 24.1 · CI ortamı ayrıca sınandı

Yeni kapılar manuscript **yokken** de doğru davranmalıdır (K10). Depo
takip edilen dosyalarla yeniden kuruldu ve koşturuldu:

```
asset_manifest.py --check  →  ⊘ BOŞ KOŞTU · çıkış 0
qa_assets.py               →  ⊘ BOŞ KOŞTU · çıkış 0
selftest.py                →  ✅ 177 denetim (manuscript'e bağlı bölümler atlandı)
```

---

## 25 · Test altyapısı

| Kapı | Faz 4 | **Faz 5** | Değişim |
|---|---:|---:|---|
| `validate_spec.py` | 61 | **86** | ⭑ **§ ⑦ YENİ** |
| `validate_structure.py` | 74 | **75** | ⭑ **§ ⑤b YENİ** |
| `validate_inheritance.py` | 8 | 8 | — |
| `validate_research.py` | 27 | 27 | — |
| `qa_matrix.py` | 23 | 23 | — |
| `qa_age.py` | 17 | 17 | — |
| `qa_solvable.py` | 9 | 9 | — |
| `qa_instruction.py` | 11 | 11 | — |
| `qa_readability.py` | 11 | **18** | ⭑ **§ ⑨ YENİ** |
| `qa_language.py` | 7 | **8** | ⭑ ticari alan 814 → **1.488** |
| `qa_progression.py` | 7 | **14** | ⭑ **§ ⑧⑨ YENİ** |
| `qa_echo.py` | 7 | **11** | ⭑ **§ ⑦ YENİ** |
| `qa_design.py` | 19 | 19 | — |
| `qa_answerkey.py` | 25 | **35** | ⭑ **§ ⑩ YENİ** |
| **`qa_assets.py`** | — | **33** | ⭑ **YENİ KAPI** |
| `page_budget.py` | 6 | 6 | ⭑ artık ÖLÇÜYOR |

### Kapıların kendi testi: 178 → **237 denetim**

Faz 5'te eklenen dört bölüm:

- **⑲ sayfa hedefi karar zinciri** — geçmiş silinir · hedef sessizce
  değişir · dayanak boşaltılır · **aradan kayıt düşürülür** · kökenden
  düşürülür · sondan düşürülür · aşılmış kayıt yürürlükte gösterilir ·
  zincir yanlış karara işaret eder · telif dayanağı modelden ayrılır
- **⑳ ön madde** — ön madde silinir · mühür sayfası düşer · bütçe
  sürüklenir · gerekçe boşalır · **gövdesiz öğretim bölümü** · *her
  bölümü production ilan etmek* · **basılan mühür sözcüğü (E2)** ·
  **gövdeye sızan mühür sözcüğü (E3)** · örnek sözcük gerçek yıldız
  sözcüğü · **rota sayfasının bölge adları GEÇER**
- **㉑ görsel varlık** — 15 kurgu: envanterden düşen şartname · yanlış
  aktivite/bölge/kültür · vinyetsiz kültür · damgasız bölge · **RAW
  üzerine yazma riski** · levhadan türemeyen etiket · düşen ölçüm kısıtı ·
  harfli damga · **etiket olarak basılan mühür sözcüğü** · Kademe C kısıtı ·
  **çeviri senkronu (3)** · **sayı genişletmesi GEÇER**
- **㉒ görsel hat · DOSYA katmanı** — kurgu PNG üretir ve hattı koşturur:
  hedef kutu birebir · **hedeften küçük RAW REDDEDİLİR** · ret gerekçesi
  yazılır · köken sha256'sı · **doluluk oranı ölçülür** · RAW değişince
  bayat · **`--force` koşusundan sonra bile RAW'a YAZILMADI**

> **㉑ şartnameyi sınar; ㉒ dosyayı sınar. İkisi ayrı körlüklerdir ve biri
> ötekini kapatmaz: kusursuz bir şartname, hattın hiç çalışmadığı bir
> depoda da kusursuz görünür.**

### 25.1 · Kurucu talimatı § 30 — 18 kusurlu kurgu sınıfının 18'i

| Kurgu | Nerede | |
|---|---|---|
| missing visual | ㉑(b) | ✅ |
| wrong assetId | ㉑ kimlik + `qa_assets § ②` | ✅ |
| wrong activityId | ㉑(c) | ✅ |
| wrong region | ㉑(d) | ✅ |
| wrong culture | ㉑(d2) | ✅ |
| wrong dimensions | ㉒(a) | ✅ |
| wrong aspect ratio | ㉒(d) | ✅ |
| low resolution | ㉒(b) | ✅ |
| missing required label | ㉑(h) | ✅ |
| answer property not observable | ㉑(i) | ✅ |
| Turkish text in final manuscript | ⑫ | ✅ |
| manuscript leak | ④ + `validate_structure § ③` | ✅ |
| protected answer leakage | ④ **§ ⑤b** | ✅ |
| final seal word visible | ⑳(g,h) · ㉑(l) · ⑱ | ✅ |
| image contradicting pagePrint | ㉑(h) | ✅ |
| page count outside tolerance | ⑧ | ✅ |
| missing front matter | ⑳(b,c) | ✅ |
| broken page integration | ⑳(d) + ⑧ | ✅ |

---

## 26 · Kalan blokajlar ve Faz 6 hazırlığı

### Faz 6'ya girmek için gereken

- [x] A12 kapandı — sayfa hedefi **144** · kurucu (K33)
- [x] Ön madde **9 sayfa** · başlık ve künye dâhil
- [x] Kelime modeli **kapandı** — 21.283 · bantta
- [x] Ticari dil **%100 İngilizce** · 1.488 dize
- [x] Varlık envanteri **hesaplandı** — 158
- [x] Görsel hattı **kuruldu ve dosya katmanında sınandı** (K35)
- [x] Prompt kütüphanesi **158 dolu prompt**
- [x] Kültürel güvenlik kısıtları **235 satır · illüstratöre ulaşıyor**
- [x] Cevap gözlemlenebilirliği **43/43**
- [x] Altı şartname çelişkisi **bulundu ve düzeltildi**
- [x] Sayfa modeli **ölçülüyor** · 144 · sapma %0
- [x] `selftest` **237** · CI yeşil · 0 açık PR
- [x] İç editoryal inceleme koşturuldu
- [ ] **Ham görsel üretimi** ⏳ **KURUCUYA AİT** — 0 / 158
- [ ] **İki ebeveyn okuması** ⏳ **KURUCUYA AİT**
- [ ] **A9 · fizikî prova** ⏳ **KURUCUYA AİT**
- [ ] **A6 · yazar biyografisi** ⏳ kurucu (Faz 6 kapısı `authorBio` null iken KIRMIZI)
- [ ] **A10 — gerçek oturum** ⏳ **BEKLİYOR**
- [ ] `.gate` → `phase2` — **A10 kapanmadan yükseltilmez**

### Açık riskler

| Risk | Ölçü | Azaltma |
|---|---|---|
| **Çocuk oturumu yapılmadı** | 0 oturum · 2 testçi hazır | materyal hazır; **sahte kayıt üretilmedi** |
| **Ham görsel üretilmedi** | 0 / 158 | hat kuruldu, sınandı ve **boş koşuyor**; envanter deterministik |
| Gerçek dizgi ölçülmedi | model 144 | `interior.py` Faz 6; sayfa **yeniden ölçülmeli** |
| 22 kayıt hâlâ provisional | 22/76 | **cevap üretmiyorlar**; manifest donduruldu |
| Field note FK bandın üst yarısında | 5,39 / 5,9 | Faz 5 metne dokunmadı; Faz 6'da yeniden ölçülmeli |
| 8 kısıt denetlenebilir yazılmamış | `validate_research` uyarısı | Faz 4'ten devraldı; cevap üretmiyor |

### Faz 6'nın ilk üç işi

1. **Kurucu ham görselleri ürettiğinde** hattı koştur: `asset_pipeline.py`
   → `qa_assets.py` → `--final`. Envanter ve promptlar hazır.
2. **Gerçek dizgi** (`interior.py`) ve **gerçek sayfa sayısı** — bugünkü
   144 bir modeldir.
3. **A6 yazar biyografisi** ve KDP metadata paketi.

---

## 27 · Faz 5 neyi kanıtladı

| Soru | Cevap |
|---|---|
| Envanter deterministik olarak hesaplanabilir mi | **Evet.** 158 · dört kaynaktan türetildi, 150'ye yuvarlanmadı |
| Bir şartname kendi levhasıyla çelişebilir mi | **Evet — altı kez çelişti.** İkisi sayfayı önceden çözerdi |
| Kusurlu bir şartname görsel üretilmeden yakalanabilir mi | **Evet.** ⑦'nin tamamı üretimden ÖNCE koştu |
| Bir kısıt yazılıp da hiç ULAŞMAYABİLİR mi | **Evet.** 59 kültürel güvenlik kısıtı üretecin okuyamadığı dildeydi |
| İki sayının uyuşması bir doğrulama mıdır | **HAYIR.** İki liste 8'de uyuşuyordu ve başka bir kitabı tarif ediyordu |
| Bir hat kendi çıktısını reddettirebilir mi | **Evet — ve reddettirdi.** Düzeltilen kapı değil hattı |
| Bir kapı doğru olanı pahalı hâle getirebilir mi | **Evet — iki kez.** 57 ve 55 doğru sayfa kırmızı yandı |
| Ön madde içerikten kolay mı | **Evet.** FK 4,22 < 5,40 |
| Bir kusur üç kapının ARASINDAN geçebilir mi | **Evet.** A1 ve A2 üç doğru kapının arasından geçti |
| Bir faz kendi işini denetleyebilir mi | **Evet — üç kendi kusurunu buldu** (A5 · A13 · B22) |
| Bir inceleme raporu bir sızıntı olabilir mi | **Evet.** Alıntı, metnin kendisi kadar korumalıdır |
| Bir kapı EKLEMEK CI'ı kırabilir mi | **Evet — kırdı.** Kaynağın yokluğu bir sürüklenme değildir |
| Sayfa hedefi ölçümle tutuyor mu | **Evet.** 144 = 144 · sapma %0,0 |
| **Çocuklar talimatları yardımsız anlıyor mu** | **HÂLÂ BİLİNMİYOR** |

Son satır Faz 2'de, 3'te ve 4'te de aynıydı. Bu bir kusur değil bir **dış
bağımlılıktır**. Faz 5 onu çözmedi, çözdüğünü de iddia etmiyor.

---

> ## FAZ 5 TAMAM. AJAN DURUR.
>
> ```
> FAZ 5 ÜRETİMİ           ✅ TAMAM         ön madde · görsel hattı · yakınsama
> A12 SAYFA HEDEFİ        ✅ KAPANDI       144 · K33 · sapma %0,0
> KURUCU AŞMASI           ✅ GENİŞLEDİ     K34 · tavan phase1'de KALDI
> HAM GÖRSEL ÜRETİMİ      ⏳ KURUCUYA AİT  0 / 158 · hat HAZIR ve SINANMIŞ
> DIŞ ÇOCUK DOĞRULAMASI   ⏳ BEKLİYOR      0 oturum · A10 AÇIK
> ```
>
> ### ÇOCUK DOĞRULAMASI: YAPILMADI.
>
> `.gate` **`phase1`'de bırakıldı** ve aşma kaydı onu oraya
> **kilitliyor**. Kapı yalnızca gerçek bir çocuk oturumundan sonra
> `phase2` olur.
>
> **Faz 6 başlatılmadı** ve kurucu talimatı olmadan başlamaz.
> **Ham görsel üretilmedi** (0 / 158). **Prova sipariş edilmedi.**
> **KDP'ye dokunulmadı.**
