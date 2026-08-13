# FAZ 2 RAPORU — pilot, çocuk okunabilirliği ve ilerleme sistemi

> **The Myth Hunter's Field Book** · Faz 2 · 13 Ağustos 2026
> Dal `faz/2-pilot` · Kapı **`phase1`'de KALDI** · Etiket `v0.2.0`
>
> Faz 1 mimarinin tuttuğunu kanıtladı. Bu fazın işi tek bir soruydu:
> **mimari gerçek içerik taşıyabiliyor mu — ve çocuk onu kullanabilir mi?**
>
> Birincisinin cevabı **evet**. İkincisinin cevabı **hâlâ bilinmiyor**,
> ve bu rapor onu bilinmiş gibi göstermiyor.

---

## 0 · Tek bakışta

| | Hedef | Ölçülen | Durum |
|---|---:|---:|---|
| Pilot bölgesi | en zor olan | **jaguar-condor** (hesaplandı) | ✅ |
| Yazılan sayfa | 5–8 + kontrollü genişleme | **16** (6+5+5) | ✅ |
| Aktivite tipi kapsamı | 5 tip | **5/5** | ✅ |
| Yeniden doğrulanan iddia | cevap üreten hepsi | **13** | ✅ |
| Bulunan iddia hatası | — | **3 düzeltme** | ⚠ *bulundu ve düzeltildi* |
| `safe` oranı (pilot) | ≥%90 | **%93,8** | ✅ |
| `do-not-use` | 0 | **0** | ✅ |
| Talimat registeri | 5–11 kel · FK ≤4,0 | **6,64 · 1,28** | ✅ |
| Field note registeri | 9–14 kel · FK 3,0–5,9 | **10,94 · 3,87** | ✅ |
| Okunabilirlik değişmezi | fk(talimat) < fk(note) | **1,28 < 3,87** | ✅ |
| Cevap belirlenimi | çift cevap yok | **16/16** | ✅ |
| Mühür harfi türevi | mekanik | **6/6 hesaplandı** | ✅ |
| Hasar yarıçapı | 1 | **1** | ✅ |
| Zincirleme bağımlılık | 0 | **0** | ✅ |
| Dil ayrımı | ticari %100 İngilizce | **127/127 dize** | ✅ |
| Sayfa modeli | 148 ±%6 | **144** (1/6 bölge gerçek) | ✅ |
| Kapı öz-testi | yeşil | **111 denetim** | ✅ |
| **İç editoryal inceleme** | koşsun | **61 bulgu · 14 bloklayıcı** | ⚠ *bulundu ve düzeltildi* |
| **Çocuk saha testi** | ≥2 testçi · ≥%80 | **0 testçi** | ⏳ **BEKLİYOR** |

```
TEKNİK PİLOT            ✅ GEÇTİ
DIŞ ÇOCUK DOĞRULAMASI   ⏳ BEKLİYOR

Bu ikisi TOPLANMAZ ve biri diğerinin yerine geçmez.
```

---

## 1 · Faz 2 kapsamı

Yol haritası Faz 2'yi bir **üretim** fazı değil bir **doğrulama** fazı
olarak tanımlıyor. Bu fazda yapılan iş:

```
① kurucu kararlarını kaydet          A3 · A8 · A9 · A7
② en zor bölgeyi HESAPLA             region_difficulty.py
③ cevap üreten her iddiayı doğrula   13 iddia · 29 kaynak künyesi
④ üç kontrollü partide 16 sayfa yaz  6 + 5 + 5
⑤ dört yeni kapı doğur               solvable · instruction · language · progression
⑥ mühürü uçtan uca sına              yuva → harf → sözcük → çentik → final
⑦ "felâket kapısı yok"u KANITLA      hasar yarıçapı · zincir taraması
⑧ çocuk test paketini hazırla        koştur ma — testçi yok
⑨ sayfa modelini GERÇEK içerikle ölç 148 → 144
```

**Yazılmayan:** kalan beş bölge, final görev, arka madde, görsel üretimi.
Yol haritası bunları Faz 3–5'e veriyor ve bu faz sınırı aşmadı.

---

## 2 · A3 onayı — altı bölge ve 37 mühür yuvası KİLİTLİ

**Kurucu onayladı → `DECISIONS.md § K18`.**

| # | Bölge | Kültür | Aktivite | Mühür |
|---|---|---:|---:|---:|
| 1 | The Northern Ice | 4 | 24 | 5 harf |
| 2 | The Middle Sea | 3 | 20 | 6 harf |
| 3 | Sun and Savanna | 3 | 16 | 7 harf |
| 4 | Mountain and Monsoon | 5 | 24 | 7 harf |
| 5 | The Great Ocean | 4 | 20 | 6 harf |
| 6 | Jaguar and Condor | 3 | 16 | 6 harf |
| | | **22** | **120** | **37** |

Bootstrap'ın bölge modeline dönülmedi. Mühür mekaniği Faz 1 biçiminde
kaldı ve `qa_matrix § ④` ile `qa_progression` her koşuda denetliyor.

---

## 3 · A8 onayı — 148 sayfa, telif düşüşü bilinerek üstlenildi

**Kurucu (a) şıkkını seçti → `DECISIONS.md § K19`.**

| | Bootstrap | Kabul edilen |
|---|---:|---:|
| Sayfa | 144 | **148** |
| Baskı | 3,45 $ | **3,52 $** |
| Ciltsiz telif | 5,55 $ | **5,48 $** |
| Başabaş ACOS | %37,0 | **%36,5** |

`project_config § scope.pageTarget` **148**'e çekildi, `BRIEF § 7`
güncellendi ve `page_budget.py`'nin Faz 1'den beri yanan uyarısı **sustu**.

> **Uyarının susması bir kazançtır.** Kalıcı bir uyarı bir süre sonra
> görülmez olur ve kapı körleşir. Karar kapandıysa uyarı da kapanmalıdır.

Ayrıca telif dayanağı (`5.48`) betikten çıkarılıp `project_config §
production.royaltyBaseline` içine alındı: Faz 1'de o sayı `page_budget.py`
içine **gömülüydü** ve karar kapandığında iki yerde birden değiştirilmesi
gerekiyordu. **İki yerde duran bir sayı er geç iki farklı şey söyler.**

---

## 4 · A9 — fizikî prova KURUCUYA AİTTİR

Yeni açık karar olarak kaydedildi (`DECISIONS.md § A9`) ve
`project_config § founder.physicalProof` içine yazıldı.

| | |
|---|---|
| Sahiplik | **kurucu** |
| Durum | **KURUCU EYLEMİ / BEKLİYOR** |
| Ajan ne yaptı | prova gerektirmeyen bütün teknik işi sürdürdü |
| Ajan ne yapmadı | **prova sipariş etmedi · yapıldığını iddia etmedi · geri bildirim veya POD doğrulaması uydurmadı** |

Bu satır kurucu tamamlandığını bildirene kadar değişmez.

---

## 5 · A7 — çocuk testçi durumu

| | |
|---|---|
| Gereken | ≥2 |
| **Mevcut** | **0** |
| Test paketi | ✅ **hazır** |
| Yapılan oturum | **0** |
| Dış doğrulama | ⏳ **BEKLİYOR** |

`03_EDITORIAL/CHILD_TEST_LOG.md` **boştur** ve boş olması bir **beyandır**:
o satırların altında uydurulmuş bir oturum yok.

Ve bu, disipline değil **mekanizmaya** bağlandı — § 12'ye bakınız.

---

## 6 · Pilot bölgesi HESAPLANDI, seçilmedi

Faz 1 raporu iki aday önermişti: `sun-savanna` **veya** `jaguar-condor`.
Faz 2 bunu bir sezgi olarak bırakmadı. `04_BUILD/region_difficulty.py`
yedi ekseni ölçtü:

yazı dizgesi yabancılığı · kademe ağırlığı · yasak biçim sayısı ·
yaşayan gelenek · hikâye arzı · mühür yükü · yetkisiz kaynak riski

| Bölge | Kültür | Yazı | Kademe | Yasak | Arz | **YÜK** | **YOĞUNLUK** |
|---|---:|---:|---:|---:|---:|---:|---:|
| **jaguar-condor** | 3 | **15** | **6** | 9 | 2,67 | 82,17 | **31,17** |
| great-ocean | 4 | 8 | 8 | 13 | 2,00 | 75,50 | 22,62 |
| monsoon | 5 | 15 | 3 | 13 | 2,18 | **87,68** | 22,08 |
| middle-sea | 3 | 12 | 0 | 7 | 2,50 | 52,00 | 21,00 |
| north-ice | 4 | 9 | 3 | 9 | 2,00 | 58,50 | 18,00 |
| sun-savanna | 3 | **1** | 2 | 8 | 3,20 | 29,70 | **14,37** |

### Ölçüm iki şeyi düzeltti

**① Tek skor büyüklüğü zorluk sanıyordu.** İlk koşu `monsoon`'u birinci
gösterdi — ama `monsoon`'un beş kültürü var ve toplanan her eksen kültür
sayısıyla **mekanik olarak** büyüyor. İki skor ayrıldı: `burden` toplam
üretim yükünü, `intensity` kültür başına sertliği ölçüyor. Pilot
**yoğunlukla** seçilir, çünkü yol haritasının ölçütü *"kısıt taraması en
YOĞUN, şifre sistemi en YABANCI"* ve yoğunluk bir orandır.

**② `sun-savanna` en zor değil, EN KOLAY bölge.** Yoğunluk 14,37 ile
sonuncu. Sebep ölçülebilir: üç yazı dizgesinin **üçü de Latin harflidir**
(Akan gün-adları · Yoruba imlâsı · isiZulu şıklamaları), yani yabancılık
15 üzerinden **1**. Faz 1 *"üç yaşayan gelenek"* ile *"yabancı şifre
dizgesi"*ni aynı şey sanmıştı. Değiller.

**Seçilen: `jaguar-condor`** — üç kültürün üçü de Kademe B (kutsal katman
cevap olamaz) ve üç yazı dizgesinin **üçü de alfabetik değil**: Maya
çubuk-nokta, Nahuatl yer adı glifleri, khipu düğümü. Çocuğun tanıdığı
hiçbir işaret yok.

> ⚠ `monsoon` pilot değil ama **sona bırakılamaz**: en yüksek toplam yükü
> o taşıyor. Faz 3 planlaması bunu dikkate almalı.

---

## 7 · Pilot envanteri

**16 sayfa · üç parti · bölgenin tamamı.**

| # | Sayfa | Kültür | Tip | ★ | Mühür | Parti |
|---:|---|---|---|---|---|---:|
| 1 | maya-bar-dot-numbers | maya | cipher | ★ | **1** | 1 |
| 2 | maya-ballcourt-plate | maya | observe | ★ | — | 2 |
| 3 | maya-number-make | maya | make | ★ | — *(açık uçlu)* | 2 |
| 4 | aztec-chinampa-plate | aztec | observe | ★ | **2** | 1 |
| 5 | aztec-town-sign-make | aztec | make | ★ | — *(açık uçlu)* | 2 |
| 6 | maya-number-add | maya | cipher | ★★ | — | 2 |
| 7 | maya-ballcourt-sort | maya | sort | ★★ | — | 2 |
| 8 | aztec-place-glyphs | aztec | cipher | ★★ | **3** | 1 |
| 9 | aztec-lake-city-map | aztec | map | ★★ | — | 3 |
| 10 | andean-khipu-knots | andean | cipher | ★★ | — | 3 |
| 11 | maya-maize-stages-sort | maya | sort | ★★ | **4** | 1 |
| 12 | andean-altitude-map | andean | map | ★★ | **5** | 1 |
| 13 | andean-flood-warning-sort | andean | sort | ★★★ | — | 3 |
| 14 | aztec-maize-journey-sort | aztec | sort | ★★★ | **6** | 1 |
| 15 | maya-place-glyphs | maya | cipher | ★★★ | — | 3 |
| 16 | aztec-number-signs | aztec | cipher | ★★★ | — | 3 |

**Parti düzeni bilinçli:** Parti 1 **mühür besleyen altı sayfadır**. En
riskli olanlar önce yazıldı, çünkü yanlış bir mühür harfi tek bir sayfayı
değil **bütün bölgeyi** çözülemez yapar.

### Dağılım

| Eksen | Ölçülen | Şart |
|---|---|---|
| Tip | cipher 6 · sort 4 · observe 2 · map 2 · make 2 | asgari 3/4/2/2/2 ✅ |
| Zorluk | ★5 · ★★7 · ★★★4 | profil {5,7,4} ✅ **tam** |
| Kültür | maya 7 · aztec 6 · andean 3 | kota {7,6,3} ✅ **tam** |
| Güvenlik | safe 15 · safe-with-adult 1 | ≥%90 · ≤%10 ✅ |
| Açık uçlu | 2 (%12,5) | yalnızca `make` ✅ |
| Süre | 214 dk toplam · ort 13,4 dk | ≤45 dk/sayfa ✅ |

**Havuzda kalan altı yedek:** `andean-condor-plate` · `aztec-codex-plate` ·
`aztec-five-suns-sort` · `maya-glyph-make` · `maya-lowland-map` ·
`maya-storm-signs-plate`. Bir pilot sayfası çocuk testinde düşerse yerine
aynı bölge × aynı tipten biri geçer ve mühür yuvası taşınır.

---

## 8 · Araştırma yeniden doğrulaması

**13 iddia · 29 kaynak künyesi · 7 devralma kaydı doğrulandı.**

Kayıt: `01_SOURCE/research/jaguar-condor-revalidation.json` — **depoda
durur** ve içinde **cevap yoktur**; iddia ve iddianın kaynağı vardır.

| Verdict | Adet |
|---|---:|
| `confirmed` | **10** |
| `corrected` | **3** |
| `rejected` | 0 |

### 8.1 · Yeni bir sözleşme: KAYIT değil İDDİA doğrulanır

Faz 1'in kuralı `inheritanceStatus` üzerineydi ve **kayıt** düzeyindeydi.
Faz 2 bunun yetersiz olduğunu gösterdi:

> Bir kültür kaydının otuz alanı vardır ve bir aktivite onun ikisini
> kullanır. *"culture-maya doğrulandı"* cümlesi **hangi alanın**
> doğrulandığını söylemez.
>
> **Kaydı `inherited-verified` yapmak bir BEYANDIR.
> İddiayı bir kaynağa bağlamak bir KANITTIR.**

Çözüm: şema **v2.1** `claimRefs` alanını aldı ve
`validate_research § ⑩` doğdu. Kapı artık şunları denetliyor:

- kilitli her sayfa `claimRefs` taşımalı
- her `claimRef` bir doğrulama kaydında **bulunmalı**
- **cevap veya mühür besleyen** her iddia **≥2 bağımsız kaynak** taşımalı
- `rejected` bir iddia hiçbir sayfada kullanılamaz
- iddianın dayandığı devralma kaydı doğrulanmış olmalı
- mühür besleyen her sayfa **mühür yetkili** bir iddiaya dayanmalı

### 8.2 · Üç düzeltme — bu fazın en yararlı çıktısı

Üçü de Faz 1'de **anlatı için yeterli**, **aktivite için yanlış** olan
cümlelerdi. Devralma mimarisinin (`INHERITANCE_ARCHITECTURE § 2`) tarif
ettiği kusurun tam örneği.

#### ① Amblem glifi bir kent etiketi sanılıyordu

> **Faz 1:** *"Maya cities signed their monuments with a glyph for the
> city itself."*

Yanlış. Amblem glifi bir **unvandır** — `k'uhul` + ana işaret + `ajaw`,
yani *"kutsal [X] efendisi"* — ve ana işaret bir **krallığı** adlandırır,
harabelerin bugünkü adını değil. Aynı amblem birden çok yerde görünebilir
(Mutal hem Tikal'de hem Dos Pilas/Aguateca'da), çünkü taşınan şey
**hanedandır**, yer değil.

Bir anlatı cildinde *"Tikal'in glifi"* zararsız bir kısaltmadır. Burada
aynı cümle bir **eşleştirme görevinin cevabı** olur ve çocuk yanlış bir
şeyi deftere yazar.

**Düzeltme:** sayfa artık glifin **üç parçasını** okutuyor ve field note
*"bu bir krallığın adıdır"* diyor. Aynı adın iki yerde çıkması bir kusur
değil, **dersin kendisi**. Yalnızca en iyi belgelenmiş iki okuma
(Mutal · Kaanul) kullanıldı; tartışmalı okumalar sayfaya girmedi.

#### ② 400 işareti "tüy" deniyordu

> **Faz 1:** *"A flag is twenty, a feather four hundred, a bag eight
> thousand."* — ve başlık: *"Flag, Feather, Bag"*.

Nahuatl sözcük **tzontli** ve anlamı **saç**. Kaynaklar işareti *"tüy ya
da saç"* diye tarif ediyor ve gerekçeyi de veriyor: *"saçlar ya da bir
tüyün lifleri kadar çok"*.

Çocuğa *"bu bir tüydür"* demek iddiayı sadeleştirmiyor, **yanlışlıyor** —
ve sözcüğün kendisini görünmez kılıyor.

**Düzeltme:** başlık *"Banner, Tzontli, Bag"* oldu, işaret kendi adıyla
anılıyor ve field note belirsizliği **çocuk diliyle söylüyor**
(`STYLE.md § 6`: belirsizlik gizlenmez). Cevap belirlenimi etkilenmiyor:
çocuk işareti **sayıya** çeviriyor, resmi adlandırmıyor.

#### ③ Top oyununun kuralları "bilinmiyor" sayılıyordu

Faz 1 tasarımı bunu **bilinmeyen** tarafına koyuyordu. Fazla kaba ve
**yanlış tarafa** düşüyor: 16. yüzyılda Diego Durán **Aztek** oyununu
gözüyle görüp yazdı — sayı nasıl alınır, top nereye değerse faul olur.

Doğru ayrım **zamandadır**:

```
BİLİNİYOR    → Aztek oyununun kuralları (görgü tanığı kaydı)
BİLİNİYOR    → sahanın biçimi, topun maddesi, kalçayla vuruş
BİLİNMİYOR   → yedi yüz yıl ÖNCEKİ Klasik Maya oyununun aynı olup olmadığı
```

Bu düzeltme aktiviteyi **zayıflatmadı, keskinleştirdi**: çocuk artık
*"bilinmiyor"* ile *"başka bir yerden ve başka bir yüzyıldan biliniyor"*
arasındaki farkı öğreniyor — `ACTIVITY_TAXONOMY § 2.3`'ün *"bilginin
sınırı da bilgidir"* alt biçiminin tam karşılığı.

### 8.3 · Doğrulama oranı neden %100 değil

| Durum | Kayıt |
|---|---:|
| `inherited-provisional` | **69** |
| `inherited-verified` | **7** |
| `new-researched` | 0 |

Doğrulama **kullanıma göre** ilerler: bir kayıt, ondan **cevap üreten**
bir sayfa yazıldığında doğrulanır. 16 sayfa yazıldı, 7 kayıt doğrulandı.
Kalan 69 kayıt hâlâ `revalidationPlan` taşıyor ve **cevap üretemiyor**.

---

## 9 · Aktivite tipi dağılımı

Pilot beş tipin **hepsini** kapsıyor ve bölge asgarilerinin hepsini
karşılıyor. Ama daha önemlisi: kapsam **kanıtlandı**, iddia edilmedi —
§ 15'teki seçilebilirlik kusuru tam da bu yüzden bulundu.

---

## 10 · Yaş ve güvenlik sonuçları

Ayrıntı: `03_EDITORIAL/AGE_REVIEW_LOG.md`

| Sınıf | Sayfa | Oran | Hedef |
|---|---:|---:|---:|
| `safe` | **15** | %93,8 | ≥%90 ✅ |
| `safe-with-adult` | **1** | %6,3 | ≤%10 ✅ |
| `do-not-use` | **0** | %0 | 0 ✅ |

**Tek `safe-with-adult`:** `andean-khipu-knots` (`string` · T1). İp bir süs
değil — çocuk okuduğu düğümü **kendi eliyle atıyor**. Ebeveyn notu ipin
yetişkin tarafından kesilmesini, verilmesini ve **sonra kaldırılmasını**
şart koşuyor.

**Betimleme taraması:** 16/16 temiz. İki sayfa kenardan dolaştı:
`andean-flood-warning-sort` *"the sea will rise"* diyor (boğulma
betimlenmiyor; anlatı zaten bir **kurtuluş** anlatısı) ve
`maya-ballcourt-sort` yalnızca mimarîye bakıyor (kurban tartışması
**hiç açılmıyor**).

**Kapalı katman:** `story-maya-hero-twins` Xibalba işkence sahnelerini
`forbiddenLayer` olarak taşıyor. Katman **açılmadı**; ikizler yalnızca bir
bağlam cümlesi ve `answer-source` **değil**.

---

## 11 · Kültürel kısıtlar — bir daralma uygulandı

### `aztec-maize-journey-sort` · yasak çerçeve 2

*Leyenda de los Soles*'in tam dizisinde **Oxomoco ile Cipactonal'ın fala
bakarak** ne yapılacağını bulduğu bir adım var.

Bu adım `AGE_POLICY § 2` çerçeve 2 (*kapalı bilginin çözülmesi*),
`CULTURE_POLICY § 4` ve Kademe B kuralı (*kutsal/kehanet katmanı cevap
olamaz*) kapsamına giriyor ve `qa_age § ⑥` `divination` desenini
tetikliyor.

**Karar: adım çocuğa görünen sıralamadan ÇIKARILDI.** Dördüncü kart artık
*"diğer tanrılar dağı açtı"* diyor; fal **anılmıyor**.

Anlatı bozulmuyor: karınca → dağ → tanenin taşınması kendi başına tam ve
nedensel bir dizidir. Çıkarılan adım bir **köprüydü**, omurga değil.

Bu bir sansür değil bir **biçim daralmasıdır** (`K13 § ①`). Daralma
sırasının **ilk basamağı** kullanıldı; kültür, hikâye veya kota **hiç**
düşürülmedi.

---

## 12 · Dil ayrımı — ve testçi kapısı

`04_BUILD/qa_language.py` doğdu. Beş denetim:

| # | Denetim | Sonuç |
|---|---|---|
| ① | Ticari katmanın her alanı İngilizce mi | **127/127** ✅ |
| ② | Türkçeye özgü harf/sözcük imzası | temiz ✅ |
| ③ | Karışık cümle | yok ✅ |
| ④ | TEST-ONLY materyal izolasyonu | temiz ✅ |
| ⑤ | **Testçi yokken test materyali üretilmiş mi** | **yok** ✅ |

### 12.1 · `ç ö ü` bilerek taranmıyor

Türkçe altı harf taşır ki İngilizcede hiç bulunmaz: `ı ğ ş İ Ğ Ş`.
Paylaşılan harfler (`ç ö ü`) ölçüte **katılmıyor**, çünkü bu kitap
kültürel adlar taşıyor: **Tenochtitlán · Huarochirí · Tonacatépetl ·
Kauaʻi**. Genel bir diakritik avı onları Türkçe sanardı ve kültürel imlâyı
korumak bu projenin bir **kuralıdır** (`validate_research § ⑧`).

`selftest § ⑫(d)` bunu ters yönden de kanıtlıyor: kültürel diakritik
taşıyan bir field note kapıdan **geçmelidir** ve geçiyor.

### 12.2 · Sahte test materyali mekanik olarak imkânsız

`04_BUILD/child_test_pack.py` testçi paketini üretir — ama
`founder.childTesters.founderConfirmed` **false** iken `--lang tr`
çağrısını **çıkış kodu 3 ile reddeder**.

```
⛔ REDDEDİLDİ — TESTÇİ ONAYI YOK

   Dosyada duran bir test sayfası, bir testin YAPILDIĞINI ima eder.
   Yapılmadı.

   Sahte test materyali, sahte test kaydının bir adım öncesidir.
   Bu betik o adımı atmaz.
```

Ve `qa_language § ⑤` testçi sayısı eşiğin altındayken
`externalValidation: "passed"` yazılmasını **engelliyor** —
`selftest § ⑫(f)` bunu kanıtlıyor.

> **Türkçe pilotun geçmesi İngilizce sürümün geçtiği anlamına GELMEZ.**
> Bu cümle `K21` olarak karara, `qa_language` olarak koda geçti.

---

## 13 · Mühür sistemi — uçtan uca doğrulandı

### 13.1 · Kural: çocuk bunu bir kez öğrenir, altı kez kullanır

```
Mühür taşıyan her sayfada YILDIZLI bir kutu vardır.
Yıldızın içindeki sayı, o kutuya yazılan sözcüğün KAÇINCI
harfinin mühre gideceğini söyler.
```

**Yıldızlı kutuya yazılan sözcük sayfada BASILIDIR** — bir etiket,
sözcük bankası girdisi veya anahtar satırı. Çocuk onu **kopyalar,
üretmez**. Bu üç şeyi birden çözüyor: yanlış yazım · diakritik kazası ·
sayısal cevaptan harf çıkarma.

### 13.2 · Yuvalar taşındı — ve bu mimarî tarafından öngörülmüştü

Faz 1 yuvaları **cevaplar yazılmadan** atamıştı; başka türlü de olamazdı.
Cevaplar yazılınca altı yuvanın **dördü** ihtiyaç duyulan harfi ancak
**yapay bir ek adımla** verebiliyordu.

`PROGRESSION_ARCHITECTURE § 6` bunu açıkça öngörüyor:
*"`sealSlot` bir aktivite özelliği değil bir **bölge özelliğidir**.
Yuva kalıcı, sakini değiştirilebilir."*

| Yuva | Faz 1 | **Faz 2** | Yıldızlı sözcük |
|---:|---|---|---|
| 1 | maya-bar-dot-numbers | **maya-bar-dot-numbers** | basılı etiket, 1. harf |
| 2 | maya-number-add | **aztec-chinampa-plate** | basılı etiket, 6. harf |
| 3 | aztec-place-glyphs | **aztec-place-glyphs** | anahtar satırı, 1. harf |
| 4 | aztec-lake-city-map | **maya-maize-stages-sort** | basılı kart, 1. harf |
| 5 | andean-khipu-knots | **andean-altitude-map** | basılı kart, 2. harf |
| 6 | andean-flood-warning-sort | **aztec-maize-journey-sort** | basılı kart, 2. harf |

Mühür **sözcüğü değişmedi**; mimarî sarsılmadı. Yeni yerleşim üç kültürü
de (maya 2 · aztec 3 · andean 1) ve beş tipin dördünü kapsıyor.

### 13.3 · `qa_progression.py` — yedi denetim

| # | Denetim | Sonuç |
|---|---|---|
| ① | Yuvalar 1…N bitişik, her biri **tam bir** kez dolu | **37/37** ✅ |
| ② | Yıldızlı sözcüğün harfi bölge sözcüğünü kuruyor | **6/6** ✅ |
| ③ | Çentik harfi sözcükten doğru konumda çıkıyor | **6/6** ✅ |
| ④ | Altı çentik harfi final sözcüğü kuruyor | ✅ |
| ⑤ | Zincirleme bağımlılık | **0** ✅ |
| ⑥ | Hasar yarıçapı | **1** ✅ |
| ⑦ | Sözcük tek hatadan kurtarılabilir uzunlukta | **6/6** ✅ |

> ⚠ Kapı hiçbir mühür sözcüğünü **ekrana basmaz** ve anahtar dosyası
> yoksa **atlar** — kırmızı yanmaz (K10).

---

## 14 · İlerleme ve kurtarma — "felâket kapısı yok" KANITLANDI

Yol haritasının söylemediği ama kurucunun istediği ölçüt buydu:

> **Bir yanlış cevap çocuğu kitabın geri kalanından kilitleyemez.
> Bir hata GERİ BİLDİRİM olmalıdır, TOPLAM BAŞARISIZLIK değil.**

Üç bağımsız mekanizma bunu birlikte sağlıyor:

### ① Hasar yarıçapı = 1

Bir yuvayı **tam bir** aktivite besliyor. Tek bir yanlış cevap **tam bir**
harfi bozuyor. İki aktivite aynı yuvayı besleseydi tek bir hata iki harfi
bozardı ve çocuk hangi sayfaya döneceğini **bulamazdı**.
`selftest § ⑬(c)` bu kurguyu koşturuyor ve kapı yakalıyor.

### ② Zincir yok

Hiçbir sayfanın çözümü başka bir sayfanın cevabına bağlı değil.
`qa_progression § ⑤` hem *"use your answer from page N"* kalıplarını hem de
bir sayfanın başka bir sayfanın kimliğini anmasını tarıyor.
`selftest § ⑬(f)` zincirleme bir sayfa kuruyor ve kapı kırmızı yanıyor.

> Zincirleme bir bulmaca kitabında 7. sayfadaki bir hata çocuğu 8. sayfada
> **durdurur** ve çocuk pes eder. Bu kitap zincirlenmiyor.

### ③ Sözcük anlamlı, yani geri bildirim veriyor

Beş harfi doğru, biri yanlış olan bir sözcük çocuğa *"burada bir şey
yanlış"* der ve **hangi yuvanın bozuk olduğunu gösterir**. Çocuk cevap
anahtarına bakmadan düzeltebilir.

### Ve ölçülen bir bonus

**37 mühür harfinin yalnızca 6'sı** (%16,2) final göreve taşınıyor —
her bölgeden bir **çentik** harfi. Yani bir bölgede yapılan hata, o harf
çentik konumunda değilse final cevabı **hiç etkilemiyor**.

> Bu bir tasarım kazasıydı ve ölçülmeseydi bilinmeyecekti. Çocuğun bir
> bölgede yaptığı hata kitabın **sonunu** bozmuyor.

---

## 15 · Kapıların bulduğu kusurlar

Bu bölüm raporun en yararlı kısmı: kapılar **yazıldıkları gün** iş yaptı.

| # | Kusur | Bulan | Düzeltme |
|---|---|---|---|
| 1 | **`jaguar-condor`'dan geçerli hiçbir 16'lık seçim yoktu** | pilot seçimi | iki aday editoryal gerekçeyle taşındı; `qa_matrix § ⑧` doğdu |
| 2 | Amblem glifi kent adı sanılıyordu | yeniden doğrulama | iddia düzeltildi, sayfa yeniden tasarlandı |
| 3 | 400 işareti "tüy" deniyordu | yeniden doğrulama | *tzontli* = saç; belirsizlik sayfada söyleniyor |
| 4 | Top oyunu kuralları "bilinmiyor" sayılıyordu | yeniden doğrulama | ayrım zamana taşındı |
| 5 | Kehanet adımı bir sıralama görevindeydi | `qa_age § ⑥` | adım çıkarıldı |
| 6 | **`qa_instruction § ②` ölü doğmuştu** | `selftest` | edilgen/kişisiz tarayıcıya çevrildi |
| 7 | İpucu sızıntı sezgiseli tek sözcükle eşleşiyordu | `qa_solvable § ⑤` | eşik iki anlamlı sözcüğe çıkarıldı |
| 8 | Yıldızlı sözcük sayfada basılı değildi | `qa_solvable § ⑦` | anahtar cevaba yazıldı |
| 9 | Bir adım talimat değil **beyan**dı | `qa_instruction § ①` | emir kipine çevrildi |
| 10 | Telif dayanağı betiğe **gömülüydü** | A8 kapanışı | `project_config`'e taşındı |
| 11 | Sapma uyarısı **yön duyarsızdı** | sayfa ölçümü | model ucuzlayınca "kıs" demiyor |
| 12 | Bölge açılışı 56 kelimeydi (hedef ~150) | ölçüm | 146 kelimeye yeniden yazıldı |
| 13 | **Mühür kuralı çocuğa HİÇ basılmıyordu** | iç inceleme | açılışa ve her yıldızlı kutunun yanına basıldı |
| 14 | **'Add the three counts' → 4 veriyordu, 8820 değil** | iç inceleme | her adım değeri söylüyor |
| 15 | **Field note beş sayfada cevabı veriyordu** | iç inceleme | beşi yeniden yazıldı · `qa_solvable § ⑧` doğdu |
| 16 | **Atıf 16 sayfanın 11'inde yoktu** | iç inceleme | kültür adı sayfaya girdi · `qa_age § ⑨` doğdu |
| 17 | **'the key' sayfada olmayan anahtarı gösteriyordu** | iç inceleme | `pagePrints` + `qa_instruction § ⑨` doğdu |
| 18 | 'tetl + nochtli' birleştirilemiyordu | iç inceleme | adım eşleştirmeye çevrildi |
| 19 | Üç yıldız talimatı iki farklı sözcüğe uyuyordu | iç inceleme | tekilleştirildi · harf kareleri eklendi |
| 20 | 16 sayfanın hepsinde ipucu vardı (şartname: yalnızca ★★★) | iç inceleme | 4 sayfaya indirildi |
| 21 | `qa_instruction § ⑨` deseni açgözlüydü | `selftest` | belirteç tek tek okunuyor |
| 22 | `qa_instruction § ⑨` samanlığı adımı içeriyordu | `selftest` | adım samanlıktan çıkarıldı |

### 15.1 · En önemli kusur — ayrı ayrı yeşil, birlikte imkânsız

Pilot bölgesinden 16 aktivite seçmeye çalışırken **geçerli hiçbir seçim
bulunamadı**. Oysa üç kısıt da yeşildi:

```
zorluk profili   ✓ havuz besliyor
kültür kotaları  ✓ havuz besliyor
tip asgarileri   ✓ havuz besliyor
─────────────────────────────────
üçü BİRDEN       ✗ kesişim BOŞ   (8008 kombinasyon · 60'ı profil+kota · 0'ı hepsi)
```

**Sebep:** ★1 havuzunda tam 5 aday vardı ve profil tam 5 istiyordu — beşi
de **zorunluydu**. Üçü `observe` idi. Asgarisi 2 olan bir tip üçe çıkınca
`sort`, `make` ve `map` aç kaldı.

**Düzeltme — iki aday, EDİTORYAL gerekçeyle taşındı:**

| Aday | Değişiklik | Gerekçe |
|---|---|---|
| `andean-condor-plate` | ★→★★ | *"etiketle **ve** ne işe yaradığını söyle"* iki işlemdir ve ikincisi bir **çıkarımdır**. Karşılaştırma: `aztec-chinampa-plate` ★ kalır çünkü *"neyin tuttuğunu **işaretle**"* der ve işaretleme çıkarım değildir |
| `aztec-town-sign-make` | ★★→★ | Kısıt **çocuğa veriliyor** (*"iki tepe"*); tek bir çizim işi kalıyor. `maya-glyph-make` ★★ **kalır** çünkü orada çocuk kısıtı **kendi bulur** |

Değişiklik sayı tutsun diye değil, ikisi de merdivende **yanlış basamakta**
olduğu için yapıldı (`ACTIVITY_TAXONOMY § 5`: *zorluk bir tasarım koludur*).

**Kapı düzeltmesi:** `qa_matrix § ⑧` doğdu ve üç kısıtı artık **birlikte**
denetliyor. Kaba kuvvet değil — kültür kültür DP, tip sayaçları asgaride
doyurulur; 34 adaylı bir bölgede bile 0,06 saniye.

> **Ayrı ayrı sağlanan üç kısıt, birlikte sağlanamayabilir.**
> Kısıtları tek tek denetleyen bir kapı, imkânsız bir kitabı yeşil gösterir.

### 15.2 · Bir kapı ölü doğdu ve `selftest` onu ilk koşuda yakaladı

`qa_instruction § ②` *"metinde 'you' geçiyor mu"* diye soruyordu. Ama
`§ ⑤` her sayfanın **`Your mission:`** ile açılmasını şart koşuyor — yani
`Your` her zaman oradaydı ve denetim **hiçbir koşulda** kırmızı
yanamazdı.

> **Hiçbir koşulda yanmayan bir kapı, bir kapı değildir.**

Gerçek risk `you` yokluğu değil, **edilgen ve kişisiz sürüklenmedir**.
Denetim yeniden yazıldı — ve ilk hâli *"the numbers must be **read**"*
cümlesini de **kaçırdı**, çünkü desen yalnızca `\w+ed` arıyordu ve `read`
düzensizdir. Bu kitabın en sık fiilleri düzensizdir (read · draw · write ·
find · put · take), yani desen tam da en olası cümleyi kaçırıyordu.

---

## 16 · Cevap belirlenimi

`04_BUILD/qa_solvable.py` · sekiz denetim · **16/16 geçti**

| # | Denetim | Sonuç |
|---|---|---|
| ① | Açık uçlu olmayan her sayfanın cevabı var | 14/14 ✅ |
| ② | `openEnded` yalnızca `make` tipinde | 2/2 ✅ |
| ③ | Açık uçlu sayfa **ölçülebilir** ölçüt taşıyor | 2/2 ✅ |
| ④ | Belirsiz dil (*or · may vary · about N · etc*) | **0** ✅ |
| ⑤ | İpucu cevabı içermiyor | 32 ipucu ✅ |
| ⑥ | Cevap alanı kalabalık değil | ✅ |
| ⑦ | **Mühür harfi yeniden hesaplandı** | 6/6 ✅ |

`openEnded` bir kaçış kapısı **değil**: iki açık uçlu sayfa da bir
**kısıt** taşıyor (*"dört noktadan sonra bir çubuk"* · *"iki tepe"*) ve
kapı ölçütün ≥8 kelime olmasını şart koşuyor.

---

## 17 · Okunabilirlik ve İngilizce kalibrasyonu

### 17.1 · Bantlar tutuyor — ve İngilizce üzerinde ölçüldü

| Register | Faz 1 (5 sayfa) | **Faz 2 (16 sayfa)** | Bant |
|---|---:|---:|---|
| Talimat | 6,96 · FK 2,03 | **6,64 · FK 1,28** | 5–11 · ≤4,0 ✅ |
| Field note | 10,36 · FK 4,70 | **10,94 · FK 3,87** | 9–14 · 3,0–5,9 ✅ |
| İpucu | 9,38 · FK 2,86 | **7,50 · FK 3,27** | ≤4,5 ✅ · yalnızca ★★★ |
| **Değişmez** | 2,03 < 4,70 | **1,28 < 3,87** | fk(talimat) < fk(note) ✅ |

| Ölçüt | Faz 2 | Bant |
|---|---:|---|
| En uzun talimat cümlesi | 12 | ≤18 ✅ |
| Adım sayısı | ort 2,81 · azami 4 | ≤4 · ★ için ≤2 ✅ |
| Field note boyu | 20–29 · ort 23,2 | 15–35 ✅ |
| Üç heceli sözcük oranı | **%2,1** | ≤%20 ✅ |
| Bölge açılışı | **146 kelime** | ~150 ✅ |

### 17.2 · Ölçüm **İngilizce metin üzerinde** yapıldı

Kurucu talimatı bunu ayrıca soruyordu: *"Türkçe okunabilirlik varsayımı
İngilizce kitaba uygulanmasın."*

Kalibrasyon **hiçbir noktada** Türkçe metin görmedi:

- `qa_readability.py` Flesch–Kincaid kullanıyor — **İngilizce için**
  tanımlanmış bir formül
- Hece sezgiseli İngilizce ünlü kümelerine göre yazılmış
- Faz 1 bandı **İngilizce pilot prozasından** ölçülmüştü
- Faz 2 ölçümü **16 İngilizce sayfadan** geldi
- Türkçe olan tek şey `$comment` ve `answerNote` alanları — ve
  `child_text()` onları **okumaz**

Yani düzeltilecek bir dil karışıklığı **bulunmadı**; ayrım zaten mimarîdeydi.
`qa_language.py` şimdi onu **mekanik olarak** koruyor.

### 17.3 · Talimat registerinin tabanı yok — ve olmayacak

Talimat FK'sı 2,03'ten **1,28**'e indi. Bant yalnızca bir tavan taşıyor ve
bir taban **eklenmeyecek**:

> *"Count the dots beside each basket."* yedi kelimedir, hepsi tek
> hecelidir ve sekiz yaşındaki için **doğru cümledir**.

Ölçülmesi gereken şey talimatın kolaylığı değil, talimat ile içerik
**arasındaki mesafedir** — onu da değişmez ölçüyor.

> **Bir metriğe taban koymak, metriği hedefe çevirir.**

`STYLE.md` **v1.2**'ye çıktı. **v2.0 numarası ilk gerçek çocuk oturumuna
ayrıldı** — yol haritası v2.0'ı *"ölçümle kalibre"* diye tanımlıyor ve o
ölçümün adı çocuk testidir.

---

## 18 · İç inceleme — bu fazın en sert dersi

> ⚠ **İÇ İNCELEME ÇOCUK DOĞRULAMASI DEĞİLDİR.**
>
> İç inceleme *"bir yetişkin bu talimatı harfi harfine okuduğunda kusur
> görüyor mu"* sorusunu sorar. Çocuk testi *"sekiz yaşındaki onu
> yardımsız yapabiliyor mu"* sorusunu sorar. İkincisini yalnızca bir
> çocuk cevaplayabilir ve bu ayrım rapor boyunca korunmuştur.

Bağımsız bir editoryal alt-ajan 16 sayfayı, yalnızca basılı metni
okuyarak, sekiz yaşındaki bir çocuk gibi harfi harfine çalıştı.

| Kategori | Bulgu |
|---|---:|
| **A · BLOKLAYICI** (çocuk takılır) | **14** |
| **B · CİDDİ** (çocuk büyük olasılıkla yanlış yapar) | **26** |
| **C · KÜÇÜK** | **16** |
| **F · KÜLTÜREL** | **5** |
| **Toplam** | **61** |
| En az bir bloklayıcı taşıyan sayfa | **11 / 16** |

### 18.1 · Ve işte fazın dersi

> ### Bütün mekanik kapılar 16/16 geçiyordu. Sayfaların çoğu yine de çözülemezdi.

Cümle uzunluğu bantta. Hece oranı bantta. Adım sayısı yasal. Field note
boyu bantta. On üç kapı yeşil.

**Kapılar cümlenin BİÇİMİNİ ölçüyordu. Kusurların hepsi cümlenin
GÖNDERMESİNDEYDİ.**

```
"Colour them the way the key shows."     → sayfada anahtar YOK
"Read the four cards beside the cord."   → sayfada ip YOK
"Put each one in the right column."      → sütun başlıkları YOK
"Write the words on the six lines."      → dört satır tanımlı
"Write where the two of them went."      → istenen ad sayfada basılı DEĞİL
```

Beşi de kusursuz İngilizce. Beşi de banttaydı. Beşi de bir çocuğu durdurur.

### 18.2 · En pahalı bulgu: mühür kuralı hiç basılmıyordu

Mühür kuralı `$comment` ve `meta.sealRule` alanlarında duruyordu — ikisi
de **makine okur, çocuk okumaz**. Çocuğa görünen metinde `seal` sözcüğü
**sıfır kez**, `slot` **sıfır kez** geçiyordu.

Yani çocuk altı kutuya altı sözcük yazar ve **CONDOR'u hiç kurmazdı**.
Bölgenin bütün ödül yapısı — `seal_key.json`'un *"ürünün kendisi"*
dediği şey — sessizce gerçekleşmiyordu.

**Düzeltme:** kural bölge açılışının son paragrafında **basılıyor**, ve
her yıldızlı kutunun yanında `★n → seal slot n` duruyor. Açılış 52
kelimeden **146 kelimeye** çıktı — `STYLE § 3`'ün ~150 hedefine oturdu ve
eksik olan tam da bu paragraftı.

### 18.3 · İkinci en pahalı: aritmetik boşluk

`aztec-number-signs` son adımı *"Add the three counts and write the
total"* diyordu. `1 banner + 2 tzontli + 1 bag` için üç sayım **1, 2, 1**
eder. Çocuk **4** yazardı; doğru cevap **8820**.

Sayfada *"çarp"* sözcüğü **hiç geçmiyordu**. Field note değerleri
veriyordu ama hiçbir adım değeri sayıya bağlamıyordu.

### 18.4 · Üçüncü: field note görevi bitiriyordu

**Beş sayfada** kültürel bilgi kutusu cevabın çoğunu söylüyordu:

> field note: *"Maize keeps to the lower quechua band, potatoes climb
> into the suni, and llamas graze the puna."*
> görev: *"Draw a line from each card to its band."*

Çocuk düşünmüyor, **kopyalıyor**. Beşi de yeniden yazıldı: field note
artık soruyu **açıyor**, kapatmıyor.

### 18.5 · Dördüncü: atıf 16 sayfanın 11'inde yoktu

Tasarım katmanında **16/16** sayfa `attributionRequired: true`
taşıyordu. Çocuğun gördüğü metinde kültür adı yalnızca **beş** sayfada
geçiyordu.

> *"A khipu counts in tens."* — kimin khipusu?
> *"In this account a llama will not eat."* — hangi anlatı?

`validate_research § ⑦` Faz 1'den beri `culturalContext` alanının **dolu**
olmasını denetliyordu. **Dolu bir tasarım alanı, sayfada basılı bir ad
demek değildir.**

Adı olmayan bir nesne bir merak nesnesidir; adı olan bir nesne bir
**halkın işidir** — ve bu kitabın tezi tam olarak ikincisidir.

### 18.6 · Üç yeni denetim doğdu

İnceleme kendi kapanışında doğru kapıyı da söyledi ve üçü yazıldı:

| Kapı | Ne denetler | Yakaladığı sınıf |
|---|---|---|
| `qa_instruction § ⑨` | *"the X"* diyen bir adım için sayfada gerçekten X var mı | A3 · A7 · A9 · A12 · A14 |
| `qa_solvable § ⑧` | field note cevabın çoğunu söylüyor mu | B2 (5 sayfa) |
| `qa_age § ⑨` | atıf zorunluysa kültür adı **sayfada** geçiyor mu | F1 (11 sayfa) |

`qa_instruction § ⑨` yeni bir alan getirdi: **`pagePrints`** — sayfanın
çözülebilmesi için levhanın **basması gereken** her şey. 16 sayfa için
**67 madde**. Bu alan aynı anda iki iş yapıyor:

```
bugün  → kapı girdisi: gönderme çözülüyor mu
Faz 5  → görsel şartnamesi: levha NE TAŞIMALI
```

> **Görsel, metnin ihtiyacından türer — tersi değil.** Faz 5'e "bir şeyler
> çiz" diye değil, sayfa sayfa **şart listesiyle** giriliyor.

### 18.7 · Ve iki kapı kusuru daha

Yeni denetimi yazarken `selftest` **iki kez** onu yakaladı:

1. **Desen açgözlüydü.** *"Copy the colours from the wall chart."*
   cümlesinde `the colours from the` öbeğini yakalıyor, ikinci `the`'yi
   yutuyor ve asıl göndermeyi — `wall chart` — **hiç görmüyordu**.
2. **Samanlık adımların kendisini içeriyordu.** *"the wall chart"* diyen
   bir adım, kendi cümlesinde geçtiği için **çözülmüş sayılıyordu**.
   Denetim her şeyi geçiriyordu.

> Bir kapı yazmak, kapının ısırdığını kanıtlamak değildir. İkisi arasında
> `selftest` durur — ve bu fazda üç kez iş yaptı.

### 18.8 · Düzeltme sonrası ölçüm

| Ölçüt | Düzeltme öncesi | **Sonrası** | Bant |
|---|---:|---:|---|
| Talimat ort · FK | 6,42 · 0,75 | **6,64 · 1,28** | 5–11 · ≤4,0 ✅ |
| Field note ort · FK | 11,45 · 4,02 | **10,94 · 3,87** | 9–14 · 3,0–5,9 ✅ |
| İpucu FK | 1,63 | **3,27** | ≤4,5 ✅ |
| Değişmez | 0,75 < 4,02 | **1,28 < 3,87** | ✅ |
| Field note boyu | 20–27 | **20–29** | 15–35 ✅ |
| Adım ort · azami | 2,69 · 3 | **2,81 · 4** | ≤4 ✅ |
| İpuçlu sayfa | 16 | **4** | yalnızca ★★★ ✅ |
| `pagePrints` maddesi | 0 | **67** | — |

**İpucu politikası da düzeltildi.** `ACTIVITY_TAXONOMY § 5` ★ ve ★★
sayfalarının **ipuçsuz** çözülmesini söylüyor; ilk sürüm 16 sayfaya da
ipucu koymuştu ve şartnameyle çelişiyordu. Artık yalnızca dört ★★★
sayfası kademeli iki ipucu taşıyor.

### 18.9 · Kabul edilmeyen bir bulgu

İnceleme `maya-number-add`'in dört çiftinden **üçünün** sayfanın öğrettiği
çubuk takasını hiç çalıştırmadığını buldu (yalnızca `3+4` beş serbest
nokta üretiyordu) ve *"bunu reçete etmiyorum, işaret ediyorum"* dedi.

**Kabul edildi ve uygulandı:** `6+8` → `7+8` yapıldı; artık iki çift
takas istiyor. Ama bu bir **cevap değişikliğidir** ve raporda ayrıca
duruyor — basılı bir cevabı değiştirmek sessizce yapılacak bir şey değil.

> **Alt-ajan körü körüne kabul edilmez** (yol haritası § 13). 61 bulgunun
> hepsi tek tek okundu; dördü mekanik olarak **yeniden doğrulandı** (mühür
> kuralı sayımı · aritmetik · basılı olmayan ad · atıf) ve o dördü de
> gerçek çıktı.

---

## 19 · Çocuk testçi durumu ve test paketi

| | |
|---|---|
| Testçi | **0** |
| Yapılan oturum | **0** |
| Üretilen sahte kayıt | **0** |
| Test paketi | ✅ **hazır** |
| Dış doğrulama | ⏳ **BEKLİYOR — PASS DEĞİL** |

### Hazırlanan paket

| Dosya | Ne |
|---|---|
| `03_EDITORIAL/CHILD_TEST_PROTOCOL.md` | oturum akışı · veli talimatı · üç soru · kayıt şeması · mahremiyet kuralları · başarı eşiği |
| `03_EDITORIAL/CHILD_TEST_LOG.md` | **boş** kayıt defteri |
| `04_BUILD/child_test_pack.py` | testçi sayfası + veli notu + boş form üreteci · **cevapsız** |
| `03_EDITORIAL/child_tests_raw/` | ham kayıt dizini · **depo dışı** |

Veli talimatının çekirdeği tek cümle: **sayfayı açıklamayın.** Bir
yetişkin *"ne demek istediğini"* açıklarsa test **geçersizdir** — çünkü
ölçtüğümüz şey çocuğun zekâsı değil, **sayfanın netliğidir**.

### Toplanmayan veri

Ad · soyad · okul · adres · doğum tarihi · fotoğraf · ses. Gerekçe basit:
**toplanmayan veri sızmaz.** Kayıtta yalnızca `tester-01` biçiminde anonim
kod, yaş ve sonuç durur ve `validate_structure § check_child_privacy`
bunu mekanik olarak denetliyor.

---

## 20 · Sayfa modeli — gerçek içerikle ölçüldü

`page_budget.py` artık bir bölgenin seçimi kilitlendiğinde **havuz
ortalaması yerine gerçek seçimi** ölçüyor.

| | Faz 1 (havuz) | **Faz 2 (1 bölge gerçek)** |
|---|---:|---:|
| `jaguar-condor` ort. ağırlık | 0,875 | **0,844** |
| Model (forma hizalı) | 148 | **144** |
| Ciltsiz baskı | 3,52 $ | 3,45 $ |
| Ciltsiz telif | 5,48 $ | 5,55 $ |

**Havuz ortalaması fazla tahmin ediyordu.** Kitaba girmeyen adayların
ağırlıkları farklı ve havuz onları da sayıyordu.

### Ve bir uyarı ters yöne çevrildi

`page_budget.py`'nin sapma uyarısı yön duyarsızdı: model **ucuzladığında**
da *"BRIEF güncellenmeli VEYA sayfa kısılmalı"* diyordu. Kısacak bir şey
yok; model zaten küçüldü. **Yanlış eylemi öneren bir uyarı gürültüdür.**
Uyarı artık yönü ve **ölçüm kapsamını** söylüyor.

### Karar açılmadı

> **148 hedefi yerinde kaldı.** Bir bölgeden bütün kitaba genelleme
> yapılmaz — Faz 1'in okunabilirlik bandında yaptığı hatanın aynısı olur.
> 6 bölgenin 5'i hâlâ havuz tahmini kullanıyor. Kalan bölgeler ölçüldükçe
> dayanak gözden geçirilir ve o **kurucu kararıdır**.

### Kelime modeli — açık bir sapma

| | Model | Ölçülen |
|---|---:|---:|
| Kelime / sayfa | ~183 | **~63** |
| 16 sayfa + açılış | ~2.930 | **1.015** |

*(İpucu politikası düzeltildikten sonra — 16 sayfanın 12'sinden ipuçları
kaldırıldı, çünkü `ACTIVITY_TAXONOMY § 5` onları yalnızca ★★★ için
tanımlıyor. Kelime sayısı bu yüzden de düştü.)*

Sapma **büyük** ve raporlanıyor. Sebep büyük olasılıkla eksik ölçüm:
manuscript şu an yalnızca **talimat metnini** taşıyor. Sayfa mobilyası —
sözcük bankaları, levha etiketleri, şifre anahtarı satırları, kartların
üstündeki metin — görsel şartnameyle birlikte Faz 5'te yazılıyor ve
kelime sayısını yükseltecek.

> Bu bir kusur olabilir de olmayabilir de, ve **bugün ayırt edilemez**.
> Faz 3'te iki bölge daha yazıldığında eğim görülür. Sayfa modeli
> `pageWeight`'ten türüyor, kelimeden değil — yani **fiyat modeli
> etkilenmiyor**.

---

## 21 · Test altyapısı

### Kapılar

| Kapı | Yeni | Denetim |
|---|---|---:|
| `validate_spec.py` | — | 33 |
| `validate_structure.py` | — | 74 |
| `validate_inheritance.py` | — | 9 |
| `validate_research.py` | **§ ⑩ yeni** | 26 |
| `qa_matrix.py` | **§ ⑧ yeni** | 23 |
| `qa_age.py` | **§ ⑨ yeni** | 16 |
| **`qa_solvable.py`** | ✅ | 9 |
| **`qa_instruction.py`** | ✅ | 11 |
| `qa_readability.py` | — | 11 |
| **`qa_language.py`** | ✅ | 7 |
| **`qa_progression.py`** | ✅ | 7 |
| `page_budget.py` | — | 6 |
| `update_docs.py` | — | — |
| **`region_difficulty.py`** | ✅ | *ölçüm, kapı değil* |
| **`child_test_pack.py`** | ✅ | *araç, kapı değil* |

### Kapıların kendi testi: 70 → **111 denetim**

`selftest.py` on dört bölüme çıktı. Faz 2'de eklenen ⑤b ve ⑩–⑬, yeni kapıların
**her dalı** için tam bir kusur taşıyan kurgu koşturuyor:

- cevapsız sayfa · çift cevap · *"answers may vary"* · ölçütsüz açık uçlu ·
  muğlak ölçüt · **cevabı sızdıran ipucu** · **elle yazılmış mühür harfi** ·
  sözcük dışı yıldız · basılı olmayan yıldız sözcüğü · **açık uçlu mühür**
- **beyan olan adım** · kalıp dışı görev satırı · **edilgen talimat** ·
  üçüncü şahıs · iki işi tek adıma sıkıştırma · öncülsüz zamir ·
  **yazma alanı yokluğu** · ★ sayfasında üçüncü adım
- **Türkçe talimat/field note/ipucu ticari katmanda** ·
  **kültürel diakritiğin Türkçe sanılmaması** · **dil gevşetmesi** ·
  **testçi yokken "passed" beyanı**
- **boş mühür yuvası** · **hasar yarıçapı 2** · yanlış türetilen harf ·
  yanlış çentik · **zincirleme bağımlılık** · kurtarılamayacak kısa sözcük
- **cevabı söyleyen field note** · **sayfada basılı olmayan gönderme** ·
  **görsel şartnamesiz sayfa** · **atıfsız sayfa**

Her yeni kapı için **kusur fikstürü + selftest + CI entegrasyonu**
üçlüsü tamamlandı; kurucu talimatı § 27 bunu şart koşuyordu.

---

## 22 · CI

| | |
|---|---|
| İş akışı | `.github/workflows/validate.yml` |
| Eklenen | `qa_language` metin işine dahil edildi |
| Yerel tam koşu | **bütün kapılar yeşil** |
| Üçüncü taraf paket | **yok** (karar K7) |

---

## 23 · Git durumu

| | |
|---|---|
| Faz 1 | `main`'e merge edildi · **v0.1.0** etiketlendi |
| Faz 1 dalı | `faz/1-devralma` **silindi** (yerel + uzak) |
| Faz 2 dalı | `faz/2-pilot` → **`main`'e merge edildi** · **v0.2.0** |
| Faz 2 dalı (silme) | merge sonrası **silindi** (yerel + uzak) |
| Açık PR | **0** |
| CI (`faz/2-pilot`) | ✅ **success** |
| CI (`main`) | ✅ **success** |
| Depoda **olmayan** | `book.json` · `seal_key.json` · ham test kayıtları · Faz 1 mimari pilotu |
| Depoda **olan** | kod · şema · kapılar · **doğrulama künyeleri** · ölçüm raporları |

**Depo sınırı iki kez sınandı ve iki kez tuttu:**

- `pagePrints` şartnameleri cevabın kendisini taşıyor (*"the chilli
  basket drawn empty"*) ve bu yüzden görsel kütüphanesine **metin olarak
  girmedi** — yalnızca sözleşmesi anlatıldı.
- Bir **kaynak künyesindeki ISBN** (Salomon–Urioste çevirisinin) sahte
  ISBN kapısını kırmızı yaktı. Kapı bizim ISBN'imizle bir **alıntının**
  ISBN'ini ayırt edemiyor ve **kapalı yönde arızalanıyor** — bu doğru.
  Künye yayıncı + yıl + sayfa biçimine çevrildi; akademik olarak tamdır.

---

## 24 · Kalan bağımlılıklar

| # | Ne | Kimden | Blokladığı |
|---|---|---|---|
| **A7** | **≥2 çocuk testçi** | kurucu | **Faz 2'nin kapanması** |
| A4 | 120'nin nihai seçimi | kurucu | Faz 3 (pilot 16'sını seçti) |
| A9 | fizikî prova | kurucu | Faz 5–6 |
| A5 | ciltli hediye sürümü | kurucu | Faz 4 |
| A6 | yazar biyografisi | kurucu | Faz 6 (`authorBio` null → kırmızı) |
| — | iki ebeveyn okuması | kurucu | Faz 4–5 |
| — | ~150 görsel | kurucu | Faz 5 |

### Açık riskler

| Risk | Ölçü | Azaltma |
|---|---|---|
| **Çocuk testi yapılmadı** | 0/2 testçi | Paket hazır; **sahte kayıt üretilmedi** |
| Kelime modeli %61 altında | 71 vs 183 /sayfa | Faz 3'te iki bölge daha ölçülünce eğim görülür |
| `monsoon` en yüksek yükü taşıyor | 87,68 | Faz 3 planlamasına not edildi; **sona bırakılamaz** |
| 5 bölge hâlâ havuz tahmininde | 1/6 ölçüldü | Her bölge kilitlendikçe model kendini düzeltiyor |
| 69 kayıt hâlâ provisional | 69/76 | Doğrulama **kullanıma göre** ilerliyor; cevap üretemiyorlar |
| Görsel şartname yazılmadı | — | Faz 5; iç inceleme gereken görsel öğeleri listeledi |

---

## 25 · Faz 3 hazırlığı

### Girmek için gereken

- [x] A3 kaydedildi — altı bölge ve 37 yuva **kilitli**
- [x] A8 kaydedildi — **148 sayfa**, telif düşüşü kabul
- [x] A9 kurucuya ait olarak kaydedildi
- [x] En zor bölge **hesaplandı** ve pilot yazıldı
- [x] Cevap üreten her iddia yeniden doğrulandı
- [x] 16 sayfa yazıldı ve `locked`
- [x] Beş aktivite tipi kapsandı
- [x] Yaş · okunabilirlik · kültürel kısıt · dil kapıları yeşil
- [x] Mühür ve **kurtarma** mekanik olarak kanıtlandı
- [x] Çocuk test paketi hazır
- [x] `selftest` yeşil (106) · CI yeşil
- [ ] **A7 — çocuk saha testi** ⏳ **BEKLİYOR**
- [ ] `.gate` → `phase2` — **A7 kapanmadan yükseltilmez**

### Faz 3'ün ilk üç işi

1. **Çocuk testi koşarsa** bulguları uygula, `STYLE.md`'yi **v2.0** yap,
   `.gate`'i `phase2`'ye yükselt.
2. `monsoon`'u erken planla — en yüksek toplam yükü o taşıyor ve beş
   kültürü var.
3. `qa_echo` kapısını doğur: tek hikâyeli kültürler (Zulu · And) tekrar
   gibi okunuyor mu.

---

## 26 · Faz 2 neyi kanıtladı

| Soru | Cevap |
|---|---|
| Mimari gerçek içerik taşıyabiliyor mu | **Evet.** 16 sayfa on üç kapıdan geçti |
| Devralınan veri aktivite eşiğini geçiyor mu | **Kısmen.** 13 iddianın **3'ü yanlıştı** ve düzeltildi |
| Mühür harfi mekanik olarak türetilebiliyor mu | **Evet.** 6/6 hesaplandı, elle yazılmadı |
| Bir yanlış cevap çocuğu kilitliyor mu | **Hayır** — ve bu artık **kanıtlanmış** bir özellik |
| Kısıtlar ayrı ayrı yeşilken birlikte tutuyor mu | **Tutmuyordu.** Kusur bulundu, kapı doğdu |
| Okunabilirlik bandı İngilizcede tutuyor mu | **Evet**, üç register de bantta |
| Bantta olmak sayfayı çözülebilir yapıyor mu | **HAYIR.** On üç kapı yeşilken 11 sayfa çözülemezdi |
| Türkçe test dili ticari çıktıdan izole mi | **Evet**, ve izolasyon **mekanik** |
| Sayfa modeli gerçek içerikle tutuyor mu | **Evet** — hatta 4 sayfa daha ucuz |
| **Çocuk talimatları yardımsız anlıyor mu** | **HÂLÂ BİLİNMİYOR** |

Son satır bu fazın **cevaplayamadığı** tek soru ve bu bir kusur değil bir
**dış bağımlılıktır**.

---

> ## FAZ 2 · TEKNİK PİLOT TAMAM. AJAN DURUR.
>
> ```
> TEKNİK PİLOT            ✅ GEÇTİ
> DIŞ ÇOCUK DOĞRULAMASI   ⏳ BEKLİYOR
> ```
>
> **Faz 3 başlatılmadı** ve kurucu talimatı olmadan başlamaz.
> `.gate` **`phase1`'de bırakıldı**: `phase2` kapısı geçen bir çocuk
> testi ister ve o test yapılmadı. Kapıyı yükseltmek, yapılmamış bir
> testi geçmiş saymak olurdu.
>
> Bekleyen: **A7** — en az iki çocuk testçi. Paket hazır, defter açık ve
> **boş**. Testçi bulunamazsa boş kalır: **sahte test kaydı üretilmez.**
