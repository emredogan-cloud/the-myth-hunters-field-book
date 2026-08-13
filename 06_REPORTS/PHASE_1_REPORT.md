# FAZ 1 RAPORU — devralma mimarisi, aktivite taksonomisi, yaş çerçevesi

> **The Myth Hunter's Field Book** · Faz 1 · 13 Ağustos 2026
> Dal `faz/1-devralma` · Kapı `phase0` → **`phase1`** · Etiket `v0.1.0`
>
> Bu fazın işi kitabı yazmak değildi. İşi şuydu:
> **üretim başlamadan önce mimarinin tuttuğunu kanıtlamak.**

---

## 0 · Tek bakışta

| | Hedef | Ölçülen | Durum |
|---|---:|---:|---|
| Aktivite adayı | ≥160 | **168** | ✅ |
| Kültür | 22 | **22** | ✅ |
| Bölge | 6 | **6** | ✅ |
| Matris hücresi (6×5) | 30 dolu | **30 dolu** | ✅ |
| Kısıt taraması | muafiyetsiz | **168/168** | ✅ |
| Devralınan kayıt | — | **76** | ✅ |
| Sayfa modeli | 144 ±%6 | **148** (+%2,8) | ✅ |
| Ciltsiz telif | 5,55 $ (hipotez) | **5,48 $** | ⚠ −0,07 $ |
| `safe` oranı | ≥%90 | **%96,4** | ✅ |
| Kilitli aktivite | 0 | **0** | ✅ |
| Kapı öz-testi | yeşil | **70 denetim** | ✅ |
| CI | YEŞİL | *push sonrası* | ⏳ |

---

## 1 · Mimari

Faz 1 altı katman kurdu. Her katman bir öncekinin üstüne oturur ve
her birinin **kendi kapısı** vardır.

```
① DEVRALMA        IMPORT_MANIFEST.json ····· 76 kayıt · sha256'lı
       ↓          validate_inheritance.py
② KÜLTÜR          culture_index.json ······· 22 kültür · A/B/C kademesi
       ↓          validate_research.py
③ BÖLGE + MÜHÜR   region_index.json ········ 6 bölge · 37 mühür yuvası
       ↓          qa_matrix.py
④ AKTİVİTE        activity_index.json ······ 168 aday · 30 hücre dolu
       ↓          validate_spec.py
⑤ GÜVENLİK        AGE_POLICY.md § 3 ········ safetyClass HESAPLANIR
       ↓          qa_age.py
⑥ SAYFA           page-budget.json ········· 148 sayfa · 5,48 $ telif
                  page_budget.py
```

**Hiçbir katman bir insana güvenmiyor.** Her ilişki bir kapı tarafından
denetleniyor ve her kapı `selftest.py` tarafından sınanıyor.

---

## 2 · Devralınan araştırma

### 2.1 · Ne devralındı

| Kayıt tipi | Adet | Kaynak |
|---|---:|---|
| Kültür künyesi | 22 | `01_RESEARCH/culture_index.json` |
| Hikâye kaydı | 54 | `01_RESEARCH/story_index.json` + `research/*.md` |
| **Toplam** | **76** | — |

Her kayıt dört soruya cevap veriyor: **nereden geldi** (`sourceRepo` ·
`sourcePath` · `sourceSha256`), **ne devralındı** (`inheritedFields`),
**burada ne yapılabilir** (`activityUsage` · `fieldbookUsage` ·
`restrictionStatus`), **doğrulandı mı** (`status` · `reviewStatus` ·
`revalidatedFields`).

Ayrıca her kayıt **kendi parmak izini** taşıyor (`recordSha256`): dosya
sha256'sı bütün kayıtlar için ortaktır ve tek başına "hangi kayıt
değişti" sorusunu cevaplayamaz.

### 2.2 · Doğrulama durumu — %0 ve bu beklenendir

| Durum | Kayıt |
|---|---:|
| `inherited-provisional` | **76** |
| `inherited-verified` | 0 |
| `new-researched` | 0 |

**Bu bir eksiklik değil, sözleşmenin kendisidir.** Faz 1'in PASS ölçütü
*"devralınan kayıtların ≥%80'i doğrulanmış **veya doğrulama planı var**"*
der. 168 adayın **168'i** kendi `revalidationPlan` alanını taşıyor ve
`validate_research.py § ④` planı olmayan bir adayı reddediyor —
"sonra bakarız" dahil (8 kelimeden kısa plan kırmızı yanar).

Ve `lockRequiresStatus` sözleşmesi gereği:

> `inherited-provisional` → **LOCKED OLAMAZ** → **YAZILAMAZ**

Bu kural **üç ayrı kapıda** denetleniyor (`validate_spec` ·
`validate_inheritance` · `validate_research`) ve `selftest § ②(i)`
sözleşmenin **gevşetilmesini** de yakalıyor.

### 2.3 · Devralınan yetki ≠ devralınan veri

Kaynak projede yaş incelemesi kapanmamış **14 hikâye** var
(9 `pending` · 5 `needs-review`). Bu kayıtlar Field Book'a **geldi** ama
**cevap üretme yetkisi gelmedi**: `fieldbookUsage` listelerinde
`answer-source` yok.

| Kayıt | Cevap üretebilir |
|---|---:|
| Toplam hikâye | 54 |
| `answer-source` yetkili | **39** |
| Yetkisiz (yaş incelemesi açık veya aktivite dışı) | 15 |

---

## 3 · Field Book'un kendi editoryal kararları

Devralınanın **üstüne** konan katman. Kaynak proje bu hikâyeleri *anlatı*
için temizledi ve o karar orada doğrudur. Burada aynı hikâye bir **göreve**
dönüşüyor ve eşik farklı.

### 3.1 · İki hikâye aktivite dışı

| Hikâye | Gerekçe |
|---|---|
| `story-egyptian-horus-seth` | Kaynak anlatı cinsel saldırı içeren bir bölüm taşıyor. Anlatıda ele alınabilir; bir **görev** çocuğu kaynağa yönlendirir. |
| `story-hindu-ganesha-head` | Çekirdeği bir başın kesilmesi, kaynakta yaş incelemesi `pending`. Bir çocuk aktivite kitabında bu, *"çocuğum için fazla karanlık"* yorumunun tarifidir. |

**Her iki kültür de iki kullanılabilir hikâyeyle temsil edilmeye devam
ediyor.** 22 vaadi kırılmadı — kültür değil **hikâye** düşürüldü.

### 3.2 · Yirmi hikâyede kapalı katman

Hikâye kalır, belirli bir bölümü aktiviteye çevrilemez
(`IMPORT_MANIFEST.json § forbiddenLayer`). Örnekler: Tepegöz'ün yamyamlık
bölümü, Sedna'nın parmakları, Xibalba işkence sınavları, Ifá kehanet
mekaniği, mele/oli metinleri, whakapapa.

### 3.3 · Kültür kademeleri

Kademe, kaynak projenin üç alanından **mekanik olarak türetiliyor** ve
`validate_research.py § ⑤` dizin ile manifestin aynı kademeyi söylediğini
denetliyor — elle gevşetme kapıyı kırmızı yakar.

| Kademe | Kültür | Aktivite | Kural |
|---|---:|---:|---|
| **A** | 13 | 92 | Beş tip açık; yaşayan gelenekte atıf zorunlu |
| **B** | 5 | 27 | Beş tip açık; kutsal katman **cevap olamaz** |
| **C** | 4 | 14 | Biçim kısıtlı; şifre yalnızca **kamuya açık yazı ve imlâ** üzerinden |

**Kademe C bir dışlama değildir.** İnuit, Māori, Hawaii ve Hindu kitapta
var, adıyla anılıyor ve toplam 14 aktivite taşıyor. Kısıtlanan kültür
değil, ondan türetilebilecek **görev biçimi**.

---

## 4 · Aktivite mimarisi

### 4.1 · Havuz

**168 aday** (hedefin %5 üstü). Dağılım:

| Bölge | Kültür | Hikâye | Aday | Kitap kotası | Mühür |
|---|---:|---:|---:|---:|---:|
| The Northern Ice | 4 | 12 | 34 | 24 | 5 harf |
| The Middle Sea | 3 | 8 | 28 | 20 | 6 harf |
| Sun and Savanna | 3 | 5 | 24 | 16 | 7 harf |
| Mountain and Monsoon | 5 | 11 | 34 | 24 | 7 harf |
| The Great Ocean | 4 | 10 | 26 | 20 | 6 harf |
| Jaguar and Condor | 3 | 6 | 22 | 16 | 6 harf |

**Bölge kotaları eşit değil ve bu bilinçli.** Kota, o bölgenin
kullanılabilir hikâye arzıyla orantılı. Eşit dağıtım (6×20) beş hikâyeli
bir bölgeden yirmi aktivite çıkarmayı zorlar ve bu **tekrar üretir** —
`qa_echo`'nun Faz 3'te yakalayacağı kusurun ta kendisi.

### 4.2 · Matris — 30 hücrenin hepsi dolu

| Tip | Aday | Bölge başına asgari | En dar hücre |
|---|---:|---:|---:|
| `sort` | 43 | 4 | 5 |
| `cipher` | 41 | 3 | 5 |
| `observe` | 35 | 2 | 5 |
| `make` | 25 | 2 | 3 |
| `map` | 24 | 2 | 3 |

### 4.3 · Bölgeler neden yeniden kuruldu

Bootstrap'ın altı bölgesi 22 kültüre **oturmuyordu**: Okyanusya'ya iki
kültür düşüyor, Amerikalara **hiç bölge kalmıyordu**. Bölgeler kıtaya
göre değil **araziye** göre yeniden kuruldu — bir saha defteri iklimi
izler, siyasî sınırları değil.

### 4.4 · Şifreler süs değil

22 kültürün **hepsinin** kamuya açık bir yazı veya notasyon dizgesi var
ve bu, kültür seçiminin ölçütlerinden biriydi: Ogham · Genç Futhark ·
Orhun runik · hiyeroglif · çivi yazısı · Yunan alfabesi · Hangul · kana ·
Çince karakter · Devanagari · Inuktitut hecelemesi · Maya çubuk-nokta ·
Aztek bayrak-tüy · khipu düğümü · Akan gün-adları · ton ve imlâ işaretleri.

> **Kutsal ad veya ritüel sözcük üzerinden şifre kurulmaz.**

---

## 5 · Çocuk güvenliği

### 5.1 · Güvenlik sınıfı hesaplanır, tahmin edilmez

`AGE_POLICY § 3.2` bir karar ağacı tanımlıyor ve `qa_age.py § classify()`
onu **birebir** kodluyor. Sınıf malzemeden türüyor; bir insan
"bence güvenli" diyemiyor.

| Sınıf | Aday | Oran | Hedef |
|---|---:|---:|---:|
| `safe` | **162** | %96,4 | ≥%90 |
| `safe-with-adult` | **6** | %3,6 | ≤%10 |
| `do-not-use` | **0** | %0 | 0 |

**Kapı kapalı yönde arızalanıyor:** beyaz listede olmayan bir malzeme
`safe` sayılmıyor, `do-not-use` oluyor. "Bilmiyorum" cevabı güvenli
değildir.

Altı `safe-with-adult` aktivitenin hepsi gerçek bir gerekçe taşıyor:
ayna (cam), ip (dolanma), yüksek sesle okuma ortağı (tanım gereği ikinci
kişi). Her biri ebeveyn notu taşıyor ve not olmadan kapı kırmızı yanıyor.

### 5.2 · "Şiddeti çiz" ile "kahramanı çiz" arasındaki fark

`qa_age.py § ⑤` betimleme fiili ile işaretli adın **eşleşmesini** arıyor:

```
(draw · sketch · colour · show · act out · describe · retell)
        ×
(wound · blood · killing · corpse · sacrifice · torture · devour · beheading · drowning)
```

Eşleşme = kırmızı. Bu, bir insanın yargısını bir **kapıya** bağlıyor.

### 5.3 · Altı yasak çerçeve

Anahtar sözcük taraması. Bir eşleşme kesin ihlal değil bir **inceleme
talebi**: eşleşen aktivite `restrictionNote`, `parentNote` veya
`safetyNotes` taşımak zorunda — yani **biri o çerçeveye bakmış olmalı**.
Bakılmamışsa aktivite `do-not-use` oluyor.

### 5.4 · Denetim yükü bir üründür

`safe-with-adult` oranı **%10'u aşamaz**. Gerekçe ticari: ebeveyn bu
kitapta **meşguliyet** satın alıyor. Yarısı yetişkin eşliği isteyen bir
aktivite kitabı ebeveyne **iş çıkarır** ve vaadi bozar.

---

## 6 · İlerleme mimarisi

```
① Bölge içindeki bazı aktiviteler bir MÜHÜR YUVASI taşır (sealSlot)
② O aktivitenin cevabından TEK BİR HARF yuvaya gider
③ Bölgenin son sayfasında yuvalar sırayla bir SÖZCÜK kurar
④ Mührün kenarındaki ÇENTİK bir sayı gösterir
⑤ O harf FİNAL GÖREVE taşınır — altı harf tek bir sözcük kurar
```

**37 mühür yuvası** tanımlandı; `qa_matrix.py § ④` her yuvanın **tam bir
kez** dolu olduğunu, yuvaların bitişik (1…N) olduğunu ve **açık uçlu bir
aktivitenin mühür besleyemediğini** denetliyor.

En önemli özellik: mühür sözcüğü **anlamlıdır**. Çocuk sözcüğü kurunca
doğru çözdüğünü **kendi anlar** ve yanlış harfi hangi aktiviteden
alacağını bilir. Bu, cevap anahtarına bakmadan düzeltme imkânı verir —
*"çocuk pes etmez"* vaadinin (BRIEF § 6.3) mekanik karşılığı.

> **Mühür sözcükleri ve final cevap bu depoda YOKTUR** (karar K10).
> `01_SOURCE/answers/seal_key.json` içindeler ve o dizin `.gitignore § ①b`
> ile dışlanmış.

### Kapının bulduğu bir kusur

İlk yerleşimde **iki mühür yuvası**, kaynakta yaş incelemesi kapanmamış
hikâyelere dayanıyordu (`persian-kaveh` · `maya-hurakan-storm`).
`validate_research.py § ⑥` bunu yakaladı ve yuvalar hikâyeden bağımsız,
belirlenimci aktivitelere taşındı.

**Bu tam olarak Faz 1'in işi:** yanlış bir mühür harfi çocuğun bütün
bölgeyi çözememesine yol açar.

---

## 7 · Pilot ve okunabilirlik kalibrasyonu

Yol haritası Faz 1'de *"tek bir aktivite yazılmaz"* der. Yazılan kitap
değil, **mimarinin sınandığı beş örnektir**: beş tip, dört bölge, iki
kademe, bir açık uçlu, iki mühür besleyici.

> Pilot prozası `02_MANUSCRIPT/pilot/pilot.json` içindedir ve **depoya
> girmez** (`.gitignore § ①`). Bu rapor yalnızca **ölçümü** taşır.

### 7.1 · Kalibrasyonun bulduğu şey

İlk ölçüm bandın **altında** çıktı: harman 8,28 kelime/cümle, FK 2,95
(hedef 9–14 kelime, 3.–5. sınıf). **Ama kusur metinde değil ölçümdeydi.**

Ayrıştırınca sebep göründü — sayfada **üç ayrı register** var:

| Register | Ölçülen | Kalibre edilen bant |
|---|---:|---|
| **Talimat** | 6,96 kelime · FK 2,03 | 5–11 kelime · FK ≤ 4,0 |
| **Field note** | 10,36 kelime · FK 4,70 | 9–14 kelime · FK 3,0–5,9 |
| **İpucu** | 9,38 kelime · FK 2,86 | FK ≤ 4,5 |

> ### Bir talimat bir anlatı cümlesi değildir.
> *"Read the age printed beside each island."* yedi kelimedir ve sekiz
> yaşındaki için **doğru uzunluktur**. Onu dokuz kelimeye uzatmak metni
> **kötüleştirirdi**.

Bootstrap'ın tek bandı World Myths'in **anlatı** prozasından devralınmıştı
ve bu kitapta yanlıştı. `STYLE.md` v1.1'e çıktı.

### 7.2 · Ve bir değişmez

```
fk(talimat)  <  fk(field note)
```

**Bir talimat, tanıttığı içerikten daha zor olamaz.** Olursa çocuk görevi
değil cümleyi çözmeye çalışır. Pilotta 2,03 < 4,70 — geçti.

### 7.3 · Diğer ölçümler

| Ölçüt | Ölçülen | Bant |
|---|---:|---|
| En uzun talimat cümlesi | 11 kelime | ≤18 |
| Üç heceli ve üstü sözcük oranı | %3,9 | ≤%20 |
| Field note boyu | 21–24 kelime | 15–35 |
| Adım sayısı | 2–3 | ≤4 (★ için ≤2) |

---

## 8 · Sayfa ve fiyat modeli

| Blok | Sayfa |
|---|---:|
| Ön madde | 8 |
| Bölgeler (aktivite 105 + yapı 12) | 117 |
| Final görev | 5 |
| Arka madde | 14 |
| **Ham model** | **144** |
| **Forma hizalı (×4)** | **148** |

Aktivite sayfası **veriden** türüyor: her adayın `pageWeight` alanı
toplanıyor (`cipher`/`sort` 0,75 · `map`/`observe`/`make` 1,0).

| | Hipotez (BRIEF § 7) | Model | Fark |
|---|---:|---:|---:|
| Sayfa | 144 | **148** | +%2,8 |
| Baskı maliyeti | 3,45 $ | **3,52 $** | +0,07 $ |
| **Ciltsiz telif** | **5,55 $** | **5,48 $** | **−0,07 $** |
| Başabaş ACOS | %37,0 | %36,5 | −0,5 puan |

⚠ **Sessiz sapma yasak.** `page_budget.py` sapma 0,05 $'ı aştığında
uyarı basıyor. Karar kurucunundur → **A8** (§ 11).

---

## 9 · Test altyapısı

### 9.1 · Kapılar

| Kapı | Yeni | Ne denetler |
|---|---|---|
| `validate_spec.py` | — | Şema, kimlik tekilliği, matris, kapı kapsamı |
| `validate_structure.py` | — | Depo, belge, gömülü değer, **cevap sızıntısı**, çocuk mahremiyeti |
| `validate_inheritance.py` | — | Manifest bütünlüğü, sha256, **devralma kilidi**, çapraz denetim |
| **`validate_research.py`** | ✅ | Araştırma zinciri, kademe tutarlılığı, **cevap yetkisi**, **diakritik** |
| **`qa_matrix.py`** | ✅ | 6×5 matris, kültür kotası, **mühür yuvaları**, tekrar |
| **`qa_age.py`** | ✅ | **Güvenlik sınıfı**, yasak çerçeve, betimleme, denetim yükü |
| **`qa_readability.py`** | ✅ | **Üç register**, değişmez, yasak kalıp, ton |
| **`page_budget.py`** | ✅ | Sayfa bandı, baskı sınırı, **telif modeli** |
| **`update_docs.py`** | ✅ | Üretilen belgeler bayat mı |
| **`import_from_world_myths.py`** | ✅ | Devralma ithalatı (araç, kapı değil) |

### 9.2 · Kapıların kendi testi — 70 denetim

`selftest.py` dokuz bölüme çıktı. Faz 1'de eklenen ⑤–⑨, her yeni kapı
için **tam bir kusur taşıyan kurgu** koşturuyor ve kapının o kusuru
yakaladığını kanıtlıyor.

Gerekçe World Myths'in **D7** dersi:

> Bir yaş kapısı, doğru çalıştığı **kanıtlanmadan** kullanılamaz.

Kanıtlanan bazı dallar:

- Yasak malzeme · tanınmayan malzeme (**kapalı arıza**) · malzemesizlik
- Şiddetin betimlenmesini isteyen görev
- İncelenmemiş yasak çerçeve · kutsal ritüel taklidi
- Matris deliği · boş mühür yuvası · çakışan yuva · açık uçlu mühür
- Temsilsiz kültür · izinsiz tip · **kısıt gevşetmesi** · **kademe gevşetmesi**
- Manifestsiz hikâye · aktivite dışı hikâye · plansız provisional
- **Yetkisiz kayda dayanan mühür** · **diakritik kaybı** · mojibake
- Sayfa bandı aşımı · negatif telif
- **Talimatın içerikten zor olması** (okunabilirlik değişmezi)

### 9.3 · Belge ↔ kod bağı

`selftest § ⑤(k)` üç yönlü bir bağ kuruyor:

```
AGE_POLICY.md § 3.1  ==  qa_age.py T0/T1/TX  ==  activity.schema.json enum
```

Ayrıldıkları an kapı kırmızı yanıyor — çünkü ayrıldıkları an **belge
yalan söylemeye başlıyor**.

---

## 10 · Kapıların Faz 1'de bulduğu altı kusur

Bu bölüm raporun en yararlı kısmı: kapılar **yazıldıkları gün** iş yaptı.

| # | Kusur | Bulan | Düzeltme |
|---|---|---|---|
| 1 | Üç bölge en kolay bantta (★) havuzsuz kalıyordu | `qa_matrix § ③` | Altı aday ★★'dan ★'a indirildi |
| 2 | Zulu'ya harita aktivitesi verilmiş ama `allowedTypes`'ta yok | `qa_matrix § ⑦` | `map` izinli tipe eklendi |
| 3 | İki mühür yuvası, yaş incelemesi kapanmamış hikâyelere dayanıyordu | `validate_research § ⑥` | Yuvalar belirlenimci aktivitelere taşındı |
| 4 | Vietnam kaydı ton işaretlerini **adlandırıyor** ama taşımıyordu | `validate_research § ⑧` | Altı ton kaydın içine yazıldı |
| 5 | Şema v2'nin sızıntı muafiyeti **ölmüştü** | `selftest § ④` | Muafiyet kaldırıldı |
| 6 | `qa_age` regex'i *"matches"* (eşleştirir) fiilini **kibrit** sanıyordu | ilk koşu | 13 yanlış ret; desen daraltıldı |

Ayrıca `selftest § ⑤(k)`'nin ilk hâli yetersizdi: malzeme adlarının
belgede **geçtiğini** doğruluyordu ama **hangi kademede** olduğunu değil.
`ruler` kodda T0, belgede T1 durduğu hâlde test yeşil yandı. Denetim
kademe kademe karşılaştırmaya çevrildi.

> Bir kapı *"adı geçiyor mu"* diye sorarsa, o kapı **yoktur**.

---

## 11 · Çözülmemiş kararlar

| # | Soru | Aciliyet | Ne zaman |
|---|---|---|---|
| **A3** | 6 bölge ve mühür mimarisi onayı | **YÜKSEK** | **şimdi** |
| **A4** | 168 adaydan 120'sinin nihai seçimi | **YÜKSEK** | Faz 2 başlarken |
| **A8** | **YENİ** — 148 sayfa kabul edilip BRIEF § 7 mi güncellenecek, yoksa 4 sayfa mı kısılacak | ORTA | Faz 2 |
| **A7** | ≥2 çocuk testçi | **YÜKSEK** | **Faz 2 SERT BLOKLAYICI** |
| A5 | Ciltli hediye sürümü | DÜŞÜK | Faz 4 |
| A6 | Yazar biyografisi | ORTA | Faz 5 |

**A1** (manuscript public depoda durmayacak) ve **A2** (devralma
politikası (a) — kopyala + sha256 + kullanıma göre yeniden doğrula)
kurucunun *"START PHASE 1"* talimatıyla **bootstrap varsayımları üzerinden
kapandı** ve `DECISIONS.md § K11–K12` olarak kayda geçti.

### Açık riskler

| Risk | Ölçü | Azaltma |
|---|---|---|
| Zulu ve And **tek hikâyeli** | 4 ve 3 aktivite | Aktiviteler ağırlıklı olarak **kültür kaydından** türüyor; `qa_echo` (Faz 3) izleyecek |
| Bazı zorluk hücrelerinde **slack sıfır** | ★★★: 3 bölgede 0 · ★: 3 bölgede 0 | Zorluk sabit değil bir **tasarım kolu**: ★★ sadeleşip ★ olur |
| Akan `ananse-stories`'ten **3 aday** | eşik 3 | `qa_matrix § ⑤` uyarısı açık |
| 20 aday **kapalı katmanlı** hikâyeye dayanıyor | 20/168 | Proza yazılırken katman açılamaz; `qa_age` uyarısı Faz 2'de kalır |
| 14 hikâyede yaş incelemesi **kapanmamış** | 14/54 | `answer-source` yetkisi verilmedi; Faz 2'de yeniden incelenecek |

---

## 12 · Faz 2 hazırlığı

### Girmek için gereken

- [x] `.gate` = `phase1`
- [x] `IMPORT_MANIFEST.json` üretildi, her kayıt sha256'lı
- [x] Devralma politikası yazılı ve onaylı (K11)
- [x] ≥160 aday, şemayı geçiyor (168)
- [x] 6×5 matrisin her hücresi asgarinin üstünde
- [x] `AGE_POLICY` onaylı — 6 yasak çerçeve + **deterministik sınıflandırma**
- [x] Kısıt taraması 168/168 muafiyetsiz
- [x] Mühür sistemi mimarisi tanımlı ve mekanik olarak denetleniyor
- [x] Sayfa modeli üretildi (148, bantta)
- [x] `selftest.py` yeşil (70 denetim)
- [ ] **CI YEŞİL** — push sonrası
- [ ] **A3 onayı** — kurucu
- [ ] **A7: ≥2 çocuk testçi** — Faz 2'nin SERT BLOKLAYICISI

### Faz 2'nin ilk üç işi

1. En zor bölgeyi seç — kısıt taraması en yoğun, şifre dizgesi en yabancı
   olan. Aday: **Sun and Savanna** (üç yaşayan gelenek, tek hikâyeli Zulu)
   veya **Jaguar and Condor** (üç Kademe B kültürü, üç ayrı sayı dizgesi).
2. O bölgenin 20 aktivitesinin dayandığı **her kültürel iddiayı yeniden
   doğrula** — `inherited-provisional` kalan hiçbir iddia pilotta
   kullanılamaz.
3. Proza yaz, `qa_solvable` ve `qa_instruction` kapılarını doğur,
   **gerçek çocuklarla test et**.

---

## 13 · Faz 1 neyi kanıtladı

| Soru | Cevap |
|---|---|
| Devralınan verinin ne kadarı yeniden doğrulama gerektiriyor | **Cevap üreten her iddia.** 76 kayıttan 39'u yetkili, 168 adayın 168'i planlı |
| 6×5 matrisin her hücresi dolabiliyor mu | **Evet** — 30/30, en dar hücre 3 |
| 22 kültür 6 bölgeye oturuyor mu | **Bootstrap'ın bölgeleriyle hayır.** Araziye göre yeniden kuruldu |
| Yaş politikası aktiviteye uyuyor mu | **Uyarlandı ve mekanikleştirildi** — sınıf hesaplanıyor, tahmin edilmiyor |
| 120 aktivite 144 sayfaya sığıyor mu | **148'e sığıyor** — bantta, telif −0,07 $ |
| Çocuk talimatları yardımsız anlıyor mu | **Bilinmiyor** — Faz 2'nin işi ve bu fazın kanıtlayamayacağı tek şey |

---

> ## FAZ 1 TAMAM. AJAN DURUR.
>
> Faz 2 **başlatılmadı** ve kurucu onayı olmadan başlamaz.
> Bekleyen: **A3** onayı ve **A7** (çocuk testçiler) — ikincisi Faz 2'nin
> sert bloklayıcısıdır ve testçi bulunamazsa **sahte test kaydı üretilmez**.
