# FAZ 3 RAPORU — ölçek, tasarım dizgesi ve bir aşmanın kilitlenmesi

> **The Myth Hunter's Field Book** · Faz 3 · 13 Ağustos 2026
> Dal `faz/3-blok-1` · Kapı **`phase1`'de KALDI** · Etiket `v0.3.0`
>
> Faz 2 mimarinin gerçek içerik taşıdığını bir bölgede kanıtladı.
> Bu fazın sorusu başkaydı:
>
> **Sistem üç bölgeye ölçekleniyor mu — ve ölçeklenirken ne bozuluyor?**
>
> Cevap: **evet, ölçekleniyor.** Ve bozulan üç şey bulundu, üçü de
> bulunması gereken yerde bulundu: **kapıların kendisinde.**

---

## 0 · Tek bakışta

| | Hedef | Ölçülen | Durum |
|---|---:|---:|---|
| Yazılmış sayfa | 60 (yol haritası Faz 3) | **60** | ✅ |
| Yazılmış bölge | 3 | **3** | ✅ |
| Yeni sayfa | 44 | **44** | ✅ |
| Ölçülmüş bölge (sayfa modeli) | ≥3 | **3 / 6** | ✅ |
| Sayfa modeli | 148 ±%6 | **144** (−%2,7) | ✅ |
| Yeniden doğrulanan iddia | cevap üreten hepsi | **42 yeni** · 55 toplam | ✅ |
| Bulunan iddia hatası | — | **3 düzeltme · 1 düşen sayfa** | ⚠ *bulundu* |
| İç editoryal inceleme | koşsun | **82 bulgu · 21 bloklayıcı** | ⚠ *bulundu ve düzeltildi* |
| Doğrulanmış devralma kaydı | — | **31 / 76** (Faz 2: 7) | ✅ |
| `safe` oranı | ≥%90 | **%95,0** | ✅ |
| `do-not-use` | 0 | **0** | ✅ |
| Talimat registeri | 5–11 kel · FK ≤4,0 | **6,77 · 1,92** | ✅ |
| Field note registeri | 9–14 kel · FK 3,0–5,9 | **11,73 · 4,68** | ✅ |
| Okunabilirlik değişmezi | fk(talimat) < fk(note) | **1,92 < 4,68** | ✅ |
| Cevap belirlenimi | çift cevap yok | **60/60** | ✅ |
| Mühür harfi türevi | mekanik | **19/19** hesaplandı | ✅ |
| Hasar yarıçapı | 1 | **1** | ✅ |
| Zincirleme bağımlılık | 0 | **0** | ✅ |
| Dil ayrımı | ticari %100 İngilizce | **388/388 dize** | ✅ |
| Görsel şartnamesi | her sayfa | **60** · 317 zorunlu etiket | ✅ |
| **Üretilmiş görsel** | Faz 5'e ait | **0** | ✅ *bilerek* |
| Yeni kapı | qa_echo (+ gerekli olanlar) | **qa_echo · qa_design** + 3 denetim | ✅ |
| Kapı öz-testi | yeşil | **151 denetim** (Faz 2: 114) | ✅ |
| **Çocuk saha oturumu** | — | **0 oturum** | ⏳ **BEKLİYOR** |

```
FAZ 3 ÜRETİMİ           ✅ TAMAM       60 sayfa · 3 bölge
KURUCU AŞMASI           ✅ KAYITLI     K27 · kilide çevrildi
DIŞ ÇOCUK DOĞRULAMASI   ⏳ BEKLİYOR    0 oturum · A10 AÇIK

Bunlar TOPLANMAZ ve hiçbiri diğerinin yerine geçmez.
FAZ 3'ÜN BİTMESİ, FAZ 2'NİN KAPANMASI DEĞİLDİR.
```

---

## 1 · Faz 3 kapsamı

Yol haritası Faz 3'ü *"Bölge bloğu I — üç bölge · 60 aktivite (pilot
dâhil)"* diye tanımlıyor. Yapılan iş:

```
① kurucu aşmasını KAYDA GEÇİR ve KİLİTLE      K27 · validate_spec § ⑤
② bölgeleri ÖLÇÜLMÜŞ YÜKLE seç                K28 · region_difficulty
③ 42 yeni iddiayı iddia düzeyinde doğrula     iki revalidation dosyası
④ 44 yeni sayfa yaz — İngilizce, doğrudan     monsoon 24 · great-ocean 20
⑤ tasarım dizgesini kitap geneline çıkar      DESIGN_SYSTEM.md v1.0
⑥ iki yeni kapı doğur                         qa_echo · qa_design
⑦ 60 sayfanın 60'ına görsel şartnamesi yaz    317 zorunlu etiket
⑧ sayfa modelini ÜÇ bölgeyle ölç              1/6 → 3/6
⑨ bağımsız editoryal kırmızı takımı koştur    iç inceleme · çocuk testi DEĞİL
```

**Yazılmayan:** kalan üç bölge, final görev, arka madde, görsel
varlıkları. Yol haritası bunları Faz 4–5'e veriyor ve bu faz sınırı
aşmadı.

---

## 2 · Kurucu aşma durumu — K27

**Kurucu talimatı:** *"Test aşamasını atlayıp tasarım (Faz 3) aşamasına
geç."*

Bu meşru bir kurucu kararıdır ve uygulandı. Tehlikeli olan karar değil,
kararın **sessiz kalmasıdır**: altı ay sonra depoyu açan bir ajan 60
sayfalık içeriği görür ve Faz 2'nin kapandığını **sanar**.

Bu yüzden aşma yalnızca yazılmadı, **kodlandı**:

`project_config § founder.phaseOverride` + `validate_spec § ⑤`

| Kilit | Ne yapar |
|---|---|
| `.gate ≤ gateCeiling` | kapı aşmayla **yükseltilemez** |
| `externalValidation ≠ passed` | aşma bir testi **geçmiş saydıramaz** |
| `deferredBlockerStatus ≠ closed` | A10 **kapanmış görünemez** |
| `documentedIn` taraması | belgede **anılmayan** aşma kırmızı yanar |

Dördüncüsü bir liste denetimi değildir: kapı o dosyaları **açar** ve
içlerinde `K27` ya da `A10` geçtiğini arar. Aşma bir belgeden düşerse CI
kırmızı yanar.

`selftest § ⑭` dört kilidin dördünü de kusurlu kurguyla sınadı; beşincisi
aşmanın **kapatılabildiğini** kanıtlıyor.

> **Bir aşma, bir sonucu üretmez. Yalnızca bir SIRAYI değiştirir.**

---

## 3 · A10 çocuk testi durumu

| | |
|---|---|
| Testçi | ✅ **2** — kurucu beyanı (A7 → K26) |
| Test paketi | ✅ hazır |
| Türkçe materyal | ✅ 16 sayfa · `01_SOURCE/pilot_tr/` · depo dışı |
| **Yapılan oturum** | **0** |
| Üretilen sahte kayıt | **0** |
| `CHILD_TEST_LOG.md` | ✅ var · **boş** |
| `externalValidation` | ⏳ **`pending`** |
| A10 | **AÇIK** — K27 ile ertelendi, **kapanmadı** |

> ### ÇOCUK DOĞRULAMASI: YAPILMADI.

Bu satır bu raporun en önemli satırıdır ve hiçbir ölçüm onun yerine
geçmez. Aşağıdaki bölümlerde geçen her *"doğrulandı"* sözcüğü
**İÇ / TEKNİK DOĞRULAMA** anlamındadır:

```
① proje-testli tasarım kuralları     ✅ uygulandı
② İngilizce okunabilirlik kalibrasyonu ✅ ölçüldü
③ iç editoryal inceleme               ✅ koşturuldu
④ mekanik çözülebilirlik              ✅ 60/60
⑤ güvenlik kapıları                   ✅ yeşil
⑥ ilerleme kapıları                   ✅ yeşil
────────────────────────────────────────────────
   ÇOCUK DOĞRULAMASI                  ❌ YAPILMADI
```

Faz 3, Faz 2'nin PASS ölçütünü karşılamaz ve karşıladığını iddia etmez.

---

## 4 · Tamamlanan bölgeler — ve neden bu ikisi

Kurucu talimatı § 11 sırayı **ölçüme** bağladı ve § 9 `monsoon`'un erken
planlanmasını şart koştu. `region_difficulty.py` yükü Faz 2'de zaten
ölçmüştü:

| Bölge | YÜK | Kota | Faz |
|---|---:|---:|---|
| ~~jaguar-condor~~ | 82,17 | 16 | Faz 2 pilotu |
| **monsoon** | **87,68** | **24** | ⭑ **Faz 3** |
| **great-ocean** | **75,50** | **20** | ⭑ **Faz 3** |
| north-ice | 58,50 | 24 | Faz 4 |
| middle-sea | 52,00 | 20 | Faz 4 |
| sun-savanna | 29,70 | 16 | Faz 4 |

**Yazılmamış iki en ağır bölge alındı.** Ve sayı kendiliğinden oturdu:

```
16 + 24 + 20 = 60   ✅ yol haritası Faz 3 (kümülatif)
24 + 20 + 16 = 60   ✅ yol haritası Faz 4 (yeni)
                ───
                120
```

A3 kotaları eşit olmadığı için *"üç bölge"* otomatik olarak 60 etmez.
Bu seçimde ediyor. **Sayı uydurulmadı; iki bağımsız kısıt aynı bölünmeyi
verdi.** Karar: **K28**.

### 4.1 · Ölçülen bir çelişki — kurucuya not (A11)

`project_config § gates.requirements.phase3` **80** kilitli aktivite
istiyor; yol haritası **60** diyor. İkisi aynı anda doğru olamaz.

Ajan **hiçbirini değiştirmedi.** Yol haritası *"tek doğruluk
kaynağıdır"* ve kapsam sayıları `scope.locked` altında bir **kurucu
kararıdır** (K8). 80 büyük olasılıkla bootstrap'ın "6 bölge × 20"
varsayımından kalan bir artıktır — ama *büyük olasılıkla* bir doğrulama
değildir.

Bugün ısırmıyor (`.gate` `phase1`). Kapı `phase3`'e yükseltilmek
istendiğinde **ısıracak**. Açık kalem: **A11**.

---

## 5 · Tamamlanan aktiviteler

**44 yeni sayfa · 60 kümülatif.**

### Mountain and Monsoon · 24 sayfa

| Eksen | Ölçülen | Şart |
|---|---|---|
| Tip | cipher 7 · sort 6 · map 4 · observe 4 · make 3 | asgari 3/4/2/2/2 ✅ |
| Zorluk | ★9 · ★★10 · ★★★5 | profil {9,10,5} ✅ **tam** |
| Kültür | chinese 7 · persian 5 · turkic 5 · vietnamese 4 · hindu 3 | kota ✅ **tam** |
| Güvenlik | safe **24** · safe-with-adult 0 | ≥%90 ✅ |
| Açık uçlu | 3 (%12,5) | yalnızca `make` ✅ |
| Mühür | 7 yuva · **MONSOON** | ✅ |
| Süre | 308 dk · ort 12,8 dk | ≤45 dk/sayfa ✅ |

### The Great Ocean · 20 sayfa

| Eksen | Ölçülen | Şart |
|---|---|---|
| Tip | cipher 6 · sort 5 · observe 4 · map 3 · make 2 | asgari ✅ |
| Zorluk | ★7 · ★★8 · ★★★5 | profil {7,8,5} ✅ **tam** |
| Kültür | korean 7 · japanese 6 · maori 4 · hawaiian 3 | kota ✅ **tam** |
| Güvenlik | safe 18 · safe-with-adult **2** | ≥%90 · ≤%10 ✅ |
| Açık uçlu | 2 (%10) | yalnızca `make` ✅ |
| Mühür | 6 yuva · **VOYAGE** | ✅ |
| Süre | 261 dk · ort 13,1 dk | ≤45 dk/sayfa ✅ |

### 5.1 · Üç kısıt yine BİRLİKTE denetlendi

Faz 2'nin en pahalı dersi *"ayrı ayrı sağlanan üç kısıt, birlikte
sağlanamayabilir"* idi ve `qa_matrix § ⑧` o dersten doğdu. Bu fazda
seçimler o kapıdan **önce** kuruldu: her iki bölge de profil × kota ×
tip asgarilerini **tam** karşılıyor, artık yok.

---

## 6 · Ticari dil durumu — İngilizce

Faz 3'ün 44 sayfası **doğrudan İngilizce yazıldı.** Hiçbir noktada
Türkçe bir ara metin kullanılmadı; Türkçe yalnızca `answerNote` ve
`$comment` alanlarında durur ve o alanlar sayfaya çıkmaz.

`qa_language.py` beş denetim · **388 ticari dize** tarandı · temiz.

| # | Denetim | Sonuç |
|---|---|---|
| ① | Ticari katmanın her alanı İngilizce mi | **388/388** ✅ |
| ② | Türkçeye özgü harf/sözcük imzası | temiz ✅ |
| ③ | Karışık cümle | yok ✅ |
| ④ | TEST-ONLY materyal izolasyonu | temiz ✅ |
| ⑤ | Testçi yokken materyal | uyarı: **oturum yok** ⏳ |

Kültürel diakritikler **korundu ve ölçüldü**: `ā` (Māori), `ʻ`
(Hawaiʻi), `ơ ư ạ ủ` (Vietnamese), `é í á` (Nahuatl, Quechua).
`qa_language § ②` bunları Türkçe sanmıyor çünkü ölçüt yalnızca
`ı ğ ş İ Ğ Ş` üzerine kurulu (K21 · Faz 2 § 12.1).

---

## 7 · Türkçe test katmanının izolasyonu

| Hat | Durum |
|---|---|
| `.gitignore § ①d` — `01_SOURCE/pilot_tr/` depoya girmez | ✅ |
| `qa_language § ④` — TEST-ONLY etiketi test dizini dışında | ✅ temiz |
| `child_test_pack.py` — onaysız veya kaynaksız üretimi reddeder | ✅ |

Faz 3'te Türkçe katmana **hiç dokunulmadı**: yeni Türkçe materyal
üretilmedi, var olan 16 sayfa değişmedi ve İngilizce katmana hiçbir şey
sızmadı. Türkçe pilot **jaguar-condor** bölgesine aittir; Faz 3'ün iki
bölgesinin Türkçe karşılığı **yoktur ve gerekmiyor** — oturum
yapılmadan ikinci bir test paketi üretmek, ilkini üretmenin hatasını
tekrarlamak olurdu.

---

## 8 · Araştırma yeniden doğrulaması

**42 yeni iddia · 55 kümülatif · 24 devralma kaydı yükseltildi.**

| Verdict | Faz 2 | **Faz 3** | Toplam |
|---|---:|---:|---:|
| `confirmed` | 10 | **39** | 49 |
| `corrected` | 3 | **3** | 6 |
| `rejected` | 0 | **0** | 0 |

| Devralma durumu | Faz 2 | **Faz 3** |
|---|---:|---:|
| `inherited-provisional` | 69 | **45** |
| `inherited-verified` | 7 | **31** |

Kayıtlar: `01_SOURCE/research/monsoon-revalidation.json` (24 iddia) ve
`great-ocean-revalidation.json` (18 iddia). İkisi de **depoda durur** ve
içlerinde **cevap yoktur**.

### 8.1 · Faz 3'ün kendi dersi

> ### Bir iddia DOĞRU olabilir ve yine de bir CEVAP olamaz.

Faz 2 *"kayıt doğrulamak ile iddia doğrulamak aynı şey değildir"*
demişti. Faz 3 bir kat daha indi: **bir iddianın doğruluğu ile bir
cevabın dayanağı olabilmesi de aynı şey değildir.**

Üç iddia doğru görünüyordu, muhtemelen doğruydu, ve **iki bağımsız
kaynakta doğrulanamadı**. Üçü de cevap kademesinden çıkarıldı.

### 8.2 · Üç düzeltme ve bir düşen sayfa

#### ① `hindu-river-names-sort` — iki ayrı kusur, ikisi de aktivite düzeyinde

> **Faz 1:** *"Every great river on this map starts in ice."*
> **Faz 1:** *"matches five rivers to the RANGES they rise in."*

**Birincisi yanlıştı.** Sutlej buzuldan değil, Tibet'teki **La'nga
gölünden** doğar. Bir anlatı cildinde *"hepsi dağdan iner"* zararsız bir
genellemedir; burada aynı cümle çocuğun deftere yazacağı bir cevabı
yanlışlar.

**İkincisi çift cevap üretiyordu.** Beş nehrin dördü için *"Himalaya"*
ya da *"Tibet"* savunulabilirdi — eşleştirme **ayırt edici değildi**.

**Düzeltme:** görev artık sıradağa değil **adlandırılmış kaynağa**
eşleşiyor (Gangotri · Yamunotri · Chemayungdung · Kailash · La'nga).
Beş kaynak farklı, beş cevap tek. Ve dördü buz, biri göl olduğu için
sayfa artık bir **çıkarım** istiyor: *hangisi ötekilere benzemiyor.*
**Kusur bir ders hâline geldi.**

#### ② `vietnamese-mountain-water-sort` — "dört tur" yoktu

Aktivite *"yarışmanın dört turunu sıraya koy"* diyordu. Ulaşılan
akademik kaynaklar anlatının **nedensel omurgasını** doğruluyor — iki
ruh, bir prenses, dağın kazanması, suyun her yıl geri gelmesi — ama
"turlar" ayrıntısını **hiçbiri vermiyor**.

**Düzeltme:** sıralama artık yalnızca kaynakların **birlikte söylediği**
dört adımı kuruyor. Uydurulmuş bir tur dizisi sayfaya girmedi.

#### ③ `japanese-turtle-time-plate` — sayı değişkeye göre değişiyor

Aktivite anlatının sayılarını okutuyordu (üç yıl / üç yüz yıl). Ulaşılan
tek kaynak cümlenin kendisinde *"bir değişkede"* diyor — yani sayı
**değişkeye göre değişiyor** ve tek cevaplı bir bulmacanın girdisi
olamaz.

**Düzeltme:** sayfa artık anlatının sayılarını değil **metinlerin
tarihlerini** okutuyor: Tango Fudoki 713 · Nihon Shoki 720 · Man'yōshū
759 · bir Meiji baskısı. Cevap tek ve doğrulanabilir.

Ve ders **güçlendi**: çocuk *"iki hızda akan zaman"*ı hikâyenin içinde
değil, hikâyenin **kendi yaşında** görüyor. Bin üç yüz yıldır anlatılan
bir hikâye, zamanın iki hızda aktığının kendi kanıtıdır.

#### ④ `korean-sky-rope-plate` — **kitaptan DÜŞTÜ**

Sayfa *"hangi kardeş güneşi aldı ve sıra neden önemli"* diye soruyordu.
Bu, anlatının belirli bir değişkesine dayanan bir **cevaptır** ve iki
bağımsız kaynakta doğrulanamadı. Ayrıca anlatının açılışı bir kaplanın
anneyi öldürmesidir (`AGE_POLICY § 2` çerçeve 4).

Sayfa düştü, **havuzda `candidate` olarak kaldı**, yerine aynı bölge ×
aynı kültürden `korean-hangul-build` geçti. Mühür yuvası taşındı
(`PROGRESSION_ARCHITECTURE § 6`: yuva kalıcı, sakini değiştirilebilir).
Kültür kotası, zorluk profili ve tip asgarileri **bozulmadı** — 160'lık
havuz tam olarak bunun için var.

### 8.3 · Yöntem dürüstlüğü

Kaynaklar ağ üzerinden okundu. Bir künye **yalnızca** o sayfanın ilgili
cümlesi görüldüğünde yazıldı. Bazı yayıncılar (Britannica, korea.net)
doğrudan çekmeyi reddediyor; o sayfaların ilgili cümleleri arama
katmanının döndürdüğü alıntılardan okundu ve künyeye **bu biçimde**
geçti. Erişilemeyen hiçbir kaynak künyeye yazılmadı.

> **Okunmamış bir kaynağı kaydetmek uydurmadır ve yapılmadı.**

---

## 9 · Aktivite tipi dağılımı

| Tip | Faz 2 (16) | **Faz 3 (60)** | Oran | Havuz oranı |
|---|---:|---:|---:|---:|
| `cipher` | 6 | **19** | %31,7 | %24,4 |
| `sort` | 4 | **15** | %25,0 | %25,6 |
| `observe` | 2 | **10** | %16,7 | %20,8 |
| `map` | 2 | **9** | %15,0 | %14,3 |
| `make` | 2 | **7** | %11,7 | %14,9 |

`cipher` havuz oranının üstünde ve bu **içerikten geliyor, kolaylıktan
değil**: Faz 3'ün iki bölgesi dokuz ayrı yazı dizgesi taşıyor —
Fars-Arap, Orhun runik, Devanagari, Vietnam ton işaretleri, Çin
karakterleri, hiragana, katakana, hangul, Māori makronu. *"Bir şifre
süs değildir"* (K4) kuralı burada bir **kota baskısı** üretiyor: dizgesi
olan her kültür en az bir kez okunmalı.

`make` %11,7 ile alt sınırda ve bu da bilinçli: açık uçlu aktivite
mühür besleyemez ve ölçülemez (`ACTIVITY_TAXONOMY § 4`).

---

## 10 · Yaş ve güvenlik

| Sınıf | Sayfa | Oran | Hedef |
|---|---:|---:|---:|
| `safe` | **57** | %95,0 | ≥%90 ✅ |
| `safe-with-adult` | **3** | %5,0 | ≤%10 ✅ |
| `do-not-use` | **0** | %0 | 0 ✅ |

Faz 3'ün iki `safe-with-adult` sayfası:

| Sayfa | Malzeme | Ebeveyn notu neyi şart koşuyor |
|---|---|---|
| `korean-hangul-shapes` | `mirror` (T1) | ayna verilir ve **sonra kaldırılır** |
| `maori-macron-length` | `read-aloud-partner` (T1) | çiftleri bir kez **sesli okur** |

İkisi de kaçınılabilirdi ve kaçınılmadı: hangul harflerinin biçimi
ancak çocuk **kendi ağzına bakarsa** anlaşılır, ve ünlü uzunluğu
görülmez, **duyulur**. Malzeme sayfanın dersinin parçasıdır.

### 10.1 · Uygulanan kültürel daralmalar

Beş sayfada `K13 § ①` daralma sırasının **ilk basamağı** kullanıldı —
biçim daraldı, kültür/hikâye/kota **hiç** düşürülmedi:

| Sayfa | Ne çıkarıldı | Gerekçe |
|---|---|---|
| `chinese-chase-the-sun` | Kua Fu'nun ölümü | sıralama dört kartla biter; son kart şeftali ormanıdır |
| `turkic-one-eyed-giants` | körleştirme ve öldürme | `forbiddenLayer`; kartlar yalnızca göz, mağara, sürü, ad |
| `japanese-eight-of-everything` | ejderhanın öldürülmesi | `forbiddenLayer`; sayfa yalnızca **sayıyor** |
| `japanese-cave-sequence` | mağaraya çekilme sebebi | `forbiddenLayer`; sıralama kapanmadan **sonra** başlar |
| `persian-great-birds-sort` | Zal'ın dağa bırakılması | sekiz yaşındaki için bir bebeğin terk edilmesi |

Ve iki Kademe C kültüründe **cevap kademesi** ayrıca daraltıldı:

- **hindu** — kutsal hece, mantra ve tanrı adı hiçbir şifrenin cevabı
  değil. Ganga sayfası bir **coğrafya** sayfasıdır; hac ve arınma
  anılmıyor.
- **maori** — whakapapa bir cevap değil; sıralama **olay** sırası
  soruyor, soy sırası değil.
- **hawaiian** — Pele bir cevap değil; adaların yaş sırası **jeolojidir**.

### 10.2 · Bir aday K4 gerekçesiyle düştü

`hindu-sun-distance-plate` seçime **girmedi**. Gerekçe kültürel değil
**kapsamsaldır**: öğrenme gerekçesi *"Comparing very large numbers is a
skill you can practise"* diyor — bu bir **matematik** becerisidir,
kültürel bilgi değil. `K4` böyle bir sayfayı **dekoratif** sayar ve
kitaba almaz.

---

## 11 · Okunabilirlik

Ölçüm **60 İngilizce sayfa** üzerinde yapıldı.

| Register | Faz 2 (16) | **Faz 3 (60)** | Bant |
|---|---:|---:|---|
| Talimat | 6,64 · FK 1,28 | **6,77 · FK 1,92** | 5–11 · ≤4,0 ✅ |
| Field note | 10,94 · FK 3,87 | **11,73 · FK 4,68** | 9–14 · 3,0–5,9 ✅ |
| İpucu | 7,50 · FK 3,27 | **9,07 · FK 3,56** | ≤4,5 ✅ |
| **Değişmez** | 1,28 < 3,87 | **1,92 < 4,68** | fk(talimat) < fk(note) ✅ |

| Ölçüt | Faz 3 | Bant |
|---|---:|---|
| En uzun talimat cümlesi | **13** | ≤18 ✅ |
| Adım sayısı | ort 2,55 · azami 4 | ≤4 · ★ için ≤2 ✅ |
| Field note boyu | 17–31 | 15–35 ✅ |
| Üç heceli sözcük oranı | **%4,7** | ≤%20 ✅ |
| Bölge açılışı | 144 · 154 · 147 kelime | 120–170 ✅ |

**Üç register de yukarı kaydı ve bu beklenen bir harekettir.** Faz 3'ün
kültürleri daha uzun özel adlar taşıyor (Devanagari, Chemayungdung,
Amaterasu, Whangārei) ve bunlar field note'ta durur — talimatta değil.
Değişmezin arası **2,76 sınıf** ile açık kalıyor.

`STYLE.md` **v1.2**'de kaldı. **v2.0 numarası ilk gerçek çocuk oturumuna
ayrılmıştır** (K23) ve Faz 3 o numaraya dokunmadı.

---

## 12 · Çözülebilirlik

`qa_solvable.py` · sekiz denetim · **60/60**

| # | Denetim | Sonuç |
|---|---|---|
| ① | Açık uçlu olmayan her sayfanın cevabı var | 53/53 ✅ |
| ② | `openEnded` yalnızca `make` tipinde | 7/7 ✅ |
| ③ | Açık uçlu sayfa **ölçülebilir** ölçüt taşıyor | 7/7 ✅ |
| ④ | Belirsiz dil (*or · may vary · about N*) | **0** ✅ |
| ⑤ | İpucu cevabı içermiyor | 28 ipucu ✅ |
| ⑥ | Cevap alanı kalabalık değil | ✅ |
| ⑦ | Mühür harfi yeniden hesaplandı | **19/19** ✅ |
| ⑧ | Field note cevabı söylemiyor | 60/60 ✅ |

`qa_instruction.py` · dokuz denetim · **60/60** — talimat kalıbı, emir
kipi, adım sayısı, adım birliği, öncülsüz zamir, yazma alanı ve
**belirtili gönderme** (`pagePrints`, 255 madde).

---

## 13 · Mühür sistemi

| Bölge | Sözcük | Yuva | Çentik | Durum |
|---|---|---:|---:|---|
| jaguar-condor | 6 harf | 6 | 3 | ✅ Faz 2 |
| **monsoon** | **7 harf** | **7** | 4 | ✅ **Faz 3** |
| **great-ocean** | **6 harf** | **6** | 2 | ✅ **Faz 3** |
| kalan üç bölge | 18 harf | 18 | — | Faz 4 |
| **toplam** | **37** | **37** | 6 | ✅ yapı bütün |

`qa_progression.py` · yedi denetim · yeşil:

| # | Denetim | Sonuç |
|---|---|---|
| ① | Yuvalar 1…N bitişik, her biri **tam bir** kez dolu | **37/37** ✅ |
| ② | Yıldızlı sözcüğün harfi bölge sözcüğünü kuruyor | **19/19** ✅ |
| ③ | Çentik harfi sözcükten doğru konumda çıkıyor | 6/6 ✅ |
| ④ | Altı çentik harfi final sözcüğü kuruyor | ✅ |
| ⑤ | Zincirleme bağımlılık | **0** ✅ |
| ⑥ | Hasar yarıçapı | **1** ✅ |
| ⑦ | Sözcük tek hatadan kurtarılabilir uzunlukta | 6/6 ✅ |

⚠ Kapı hiçbir mühür sözcüğünü ekrana **basmaz**.

### 13.1 · Faz 1'den kalan yuvalar temizlendi

Faz 1 mühür yuvalarını bütün havuza dağıtmıştı. Faz 3 seçimi yapınca
üç **seçilmemiş** aday hâlâ yuva taşıyordu ve `qa_progression § ①`
"yuva iki kez dolu" diye kırmızı yandı. Kapı haklıydı: yuva bir bölge
özelliğidir ve **iki sakini olamaz**. Üç aday temizlendi.

---

## 14 · İlerleme ve kurtarma

Faz 2'nin kanıtladığı üç mekanizma **üç bölgede de** tutuyor:

| Mekanizma | Ölçülen |
|---|---|
| **Hasar yarıçapı 1** — bir yuvayı tam bir aktivite besler | ✅ 19/19 |
| **Zincir yok** — hiçbir sayfa başka bir sayfanın cevabına bağlı değil | ✅ 0 |
| **Sözcük anlamlı** — yanlış harf sözcüğü bozar, çocuk hangi sayfaya döneceğini bilir | ✅ 3/3 |

Ve ölçülen bonus korunuyor: **37 mühür harfinin yalnızca 6'sı** (%16,2)
final göreve taşınıyor.

---

## 15 · Tasarım dizgesi

`00_CONTEXT/DESIGN_SYSTEM.md` **v1.0** — Faz 2'nin tek bölgelik sayfa
dili kitap geneline çıkarıldı ve donduruldu.

```
SABİT   → on modül ve yerleri        (görev satırı → ipucu şeridi)
SEÇMELİ → on düzen, tipe bağlı       (key-decode … make-frame)
SERBEST → levhanın içeriği           (pagePrints · sayfaya özel)
```

### 15.1 · Çözülen gerilim

Kurucu talimatı § 15: *structure consistency without cultural
homogeneity.* İki gereklilik birbirini yer:

- Yapı gevşerse çocuk her sayfada **yeniden öğrenir** ve mühür kuralını
  oturtamaz.
- Yapı fazla sıkarsa altı bölge **tek şablonun altı kopyası** olur ve
  kitabın tezi sayfa düzeninin kendisi tarafından yalanlanır.

Çözüm mekanik: modüller sabit, düzen tipten gelir, içeriği kültür
belirler. Ve `qa_design § ⑥` her bölgenin **en az üç ayrı düzen**
kullanmasını şart koşar.

| Bölge | Sayfa | Ayrı düzen |
|---|---:|---:|
| jaguar-condor | 16 | **5** |
| monsoon | 24 | **6** |
| great-ocean | 20 | **8** |

### 15.2 · Neden `qa_matrix` bunu göremezdi

`qa_matrix` her bölgede beş **TİPİN** dağılımını denetliyor. Ama tip ile
**DÜZEN** aynı şey değildir: beş tip de dolu olduğu hâlde bütün sayfalar
aynı levha biçimini kullanabilir ve `qa_matrix` yeşil yanar.

> **Altı bölge farklı içerik taşıyıp aynı ŞABLON gibi okunabilir.**

`selftest § ⑯(g)` bunu kanıtlıyor: beş tipi de dolu, düzeni tek olan bir
kurgu `qa_matrix`ten geçiyor ve `qa_design`den **geçmiyor**.

---

## 16 · pagePrint kapsamı

| | Faz 2 | **Faz 3** |
|---|---:|---:|
| `pagePrints` maddesi | 67 | **255** |
| Kapsanan sayfa | 16/16 | **60/60** |

Faz 2 `pagePrints`i bir **kapı girdisi** olarak doğurdu. Faz 3 onu
**görsel şartnamesinin girdisi** hâline getirdi ve zinciri kapattı:

```
talimat → pagePrints → visualSpec → prompt → varlık
```

⚠ **Faz 3'ün 44 sayfası `pagePrints` ile BİRLİKTE yazıldı, sonra
değil.** Her belirtili gönderme yazılırken levhaya bir madde ekledi.
Faz 2'de sıra tersti ve 16 sayfanın 11'i çözülemezdi.

---

## 17 · Görsel şartnameleri

**60 şartname · 317 zorunlu etiket · 0 üretilmiş varlık.**

Her sayfa on beş alanlık bir `visualSpec` taşıyor: `assetId` ·
`visualClass` · `layout` · `purpose` · `subject` · `requiredLabels` ·
`orientation` · `targetPx` · `aspect` · `safeAreaMm` · `restrictions` ·
`format` · `filename` · `destination` · `status`.

`requiredLabels` **elle yazılmadı, levhadan TÜRETİLDİ**: `pagePrints`
içindeki her iki-nokta listesi levhanın basmak zorunda olduğu şeydir.
Türetme iki sayfada **boş döndü** ve ikisi de gerçek bir şartname
açığıydı — levha *"bir anahtar paneli"* diyordu ama hangi girdileri
basacağını söylemiyordu. Faz 5 o cümleyle görsel üretemezdi.

### 17.1 · Prompt kütüphanesi artık ÜRETİLİYOR

`04_BUILD/image_prompts.py` `IMAGE_PROMPT_LIBRARY.html`'i
`visualSpec`lerden üretir ve `--check` bayatlığı denetler (K17).

> Elle yazılan bir varlık listesi, bir sayfa değişince **sessizce yalan
> söylemeye başlar** — ve görsel hattı yanlış aktiviteye bağlanmış
> kusursuz bir görsel üretir. Faz 5'in en pahalı hatası budur.

### 17.2 · K10 sınırı mekanikleşti

`pagePrints` listeleri **cevabın kendisidir**. Bu yüzden kütüphaneye
girmez: promptlar `{PRINT_LIST}` yer tutucusuyla durur ve Faz 5'te
**elindeki manuscript'ten** doldurulur. Public depo dolu hâlini hiçbir
zaman görmez.

> ### ŞARTNAME BİR VARLIK DEĞİLDİR.
>
> `BOOK_STATS.md` ikisini **ayrı satırlarda** sayar: *görsel şartnamesi*
> **60**, *görsel varlık (üretilmiş)* **0**. Birini diğerinin yerine
> saymak, olmayan bir varlığı var göstermektir.

---

## 18 · qa_echo — tekrar ve kültürel düzleşme

Faz 2 raporu bu kapıyı **adıyla** istedi: *tek hikâyeli kültürler
(Zulu · And) tekrar gibi okunuyor mu.*

### 18.1 · Kapının çözdüğü asıl problem

Kapı naif kurulsaydı **kendi projesine zarar verirdi**: `qa_age § ⑨`
her sayfada kültürün adının **geçmesini** şart koşuyor. Beş Çin
sayfasının beşinde de *"Chinese"* geçer ve bu bir tekrar değil bir
**atıf zorunluluğudur**.

> **İki kapı birbirine ters çalışamaz.**

Çözüm: ölçümden **önce** bütün kültürel terimler maskelenir — kültür
adları, yazı dizgesi terimleri, özel adlar, Latin dışı her şey (**162
terim**). Geriye kalan yazarın **kendi dilidir** ve tekrar orada aranır.

### 18.2 · Altı denetim ve ölçüm

| # | Denetim | Ölçülen |
|---|---|---|
| ① | field note açılış kalıbı | temiz ✅ |
| ② | görev satırı kalıbı | temiz ✅ |
| ③ | düzleştirici dil (12 kalıplık kapalı liste) | **0 ihlal** ✅ |
| ④ | field note örtüşmesi | en yüksek **0,33** (eşik 0,55) ✅ |
| ⑤ | tek kaynaklı kültür | `andean` izleniyor (1 hikâye → 3 sayfa) ✅ |
| ⑥ | nakarat payı | 6 beyan · hiçbiri %60'ı aşmıyor ✅ |

### 18.3 · Kasıtlı tekrar bir kusur değildir

Bu kitap kasıtlı tekrar üzerine kurulur: çocuk mühür kuralını bir kez
öğrenir, altı kez kullanır. Kalıbı cezalandıran bir kapı, kitabın
öğrettiği alışkanlığı bozar.

Bu yüzden yapısal nakaratlar `project_config § echo.allowedRefrains`
içinde **beyan edilir** — bir karar olurlar, bir kaza değil. Ve beyan
bir muafiyet değil bir **bütçedir**: `maxRefrainShare` %60. Beyan
edilmemiş ama üç sayfada **birebir** yinelenen bir adım da kırmızı
yanar; **sessiz nakarat, kararı olmayan bir kalıptır.**

`selftest § ⑮` sekiz kusur fikstürü koşturuyor **ve bir yanlış-pozitif
testi**: kültür adını her sayfada tekrarlayan bir kurgu **geçmek
zorundadır** ve geçiyor.

---

## 19 · Sayfa modeli — üç bölge gerçek

| Bölge | Kota | Ort. ağırlık | Kaynak | Aktivite s. | Yapı s. | Toplam |
|---|---:|---:|---|---:|---:|---:|
| north-ice | 24 | 0,875 | havuz | 21,0 | 2 | 23,0 |
| middle-sea | 20 | 0,875 | havuz | 17,5 | 2 | 19,5 |
| sun-savanna | 16 | 0,875 | havuz | 14,0 | 2 | 16,0 |
| **monsoon** | 24 | **0,865** | **ÖLÇÜLDÜ** | 20,8 | 2 | 22,8 |
| **great-ocean** | 20 | **0,863** | **ÖLÇÜLDÜ** | 17,2 | 2 | 19,2 |
| **jaguar-condor** | 16 | **0,844** | **ÖLÇÜLDÜ** | 13,5 | 2 | 15,5 |

```
ön madde        8
bölgeler      116,0
final görev     5
arka madde     14
──────────────────
ham model     143,0  →  yuvarlanmış 143  →  forma hizalı 144
```

| | Hedef | Ölçülen |
|---|---:|---:|
| Sayfa | 148 | **144** (−%2,7 · bant ±%6 ✅) |
| Ciltsiz baskı | 3,52 $ | 3,45 $ |
| Ciltsiz telif | 5,48 $ | 5,55 $ |
| Başabaş ACOS | %36,5 | %37,0 |

### 19.1 · Model ÜÇ ölçümle sağlamlaştı

Faz 2'de tek bir bölge ölçülmüştü ve *"bir bölgeden bütün kitaba
genelleme yapılmaz"* denmişti. Artık üç bölge var ve üçü **birbirine
çok yakın**:

```
0,844   0,863   0,865      → ortalama 0,857
havuz tahmini 0,875        → ölçüm tahminin %2 ALTINDA, tutarlı
```

Kalan üç bölge de 0,857'de gelirse model **yine 144** eder. Yani model
artık bir tahmin değil bir **eğilimdir**.

**148 hedefi yerinde kaldı** (K19). 0,07 $ için içerik kısılmıyor ve
karar yeniden açılmıyor. Kalan üç bölge ölçüldüğünde dayanak gözden
geçirilir ve o **kurucu kararıdır**.

### 19.2 · Kelime modeli — Faz 2'nin tahmini DOĞRULANDI

Faz 2 kelime açığının *"sayfa mobilyasında"* olduğunu tahmin etmişti.
Mobilya artık yazıldı ve ölçüldü:

| | Ölçülen | / sayfa |
|---|---:|---:|
| Proza (talimat · field note · ipucu · ölçüt) | 3.958 | 66,0 |
| **Levha mobilyası (`pagePrints`)** | **2.968** | **49,5** |
| Bölge açılışları (3) | 488 | — |
| **Toplam ölçülen** | **7.414** | — |

Mobilya prozanın **%75'i kadar** ve çocuğun **okuduğu** metindir.

120 sayfaya çıkarım: **≈14.800 kelime** gövde + arka/ön madde. Hedef
22.000 hâlâ yüksek görünüyor ama açık %61'den **%33'e** indi ve kalan
fark yazılmamış ön/arka maddededir.

> **Fiyat modeli etkilenmiyor:** sayfa modeli `pageWeight`ten türüyor,
> kelimeden değil.

---

## 20 · Kültürel atıf

`qa_age § ⑨` — atıf gereken **60/60** sayfada kültürün adı çocuğun
gördüğü metinde geçiyor.

Yazım sırasında **altı sayfa** bu kapıdan geçemedi (Ganga, nehir
kaynakları, Alborz, büyük kuşlar, tek gözlü devler, Kızıl Nehir) ve
altısının da field note'u yeniden yazıldı: kültür adı **bir bilgiye
bağlandığı yere** kondu, bir etiket olarak başlığa değil.

### 20.1 · Ve kapı DOĞRU İMLÂYI cezalandırıyordu

Üç Māori sayfası *"atıfsız"* diye kırmızı yandı — oysa üçünde de
**Māori** yazıyordu. Eşleyici diakritiksiz biçimleri arıyor ve
`"māori"` içinde `"maori"` alt-dizesi **yoktur**.

Kusurun tehlikeli tarafı yanlış pozitif olması değil, **önerdiği
çözümdür**: kapıyı yeşile çevirmenin en kolay yolu sayfada makronu
düşürüp *"Maori"* yazmaktı. `validate_research § ⑧` diakritiklerin
korunmasını **şart koşuyor**; iki kapı birbirine ters çalışıyordu.

> **Bir kapı, doğru olanı yapmayı pahalı hâle getiriyorsa,
> düzeltilmesi gereken kapıdır.**

Eşleyici düzeltildi (`māori` · `việt` · `dede korkut` eklendi).

---

## 21 · İç editoryal inceleme — bu fazın en sert dersi

> ⚠ **İÇ İNCELEME ÇOCUK DOĞRULAMASI DEĞİLDİR.**
>
> İnceleme *"bir yetişkin bu talimatı harfi harfine okuduğunda kusur
> görüyor mu"* sorusunu sorar. Çocuk testi *"sekiz yaşındaki onu
> yardımsız yapabiliyor mu"* sorusunu sorar. İkincisini yalnızca bir
> çocuk cevaplayabilir ve bu ayrım rapor boyunca korunmuştur.

Bağımsız bir editoryal alt-ajan 44 yeni sayfayı ve iki bölge açılışını,
**yalnızca basılı metni okuyarak**, sekiz yaşındaki bir çocuk gibi harfi
harfine çalıştı.

| Sınıf | Bulgu |
|---|---:|
| **A · BLOKLAYICI** (çocuk takılır) | **21** |
| **B · CİDDİ** (çocuk büyük olasılıkla yanlış yapar) | **28** |
| **C · KÜÇÜK** | 9 |
| **D · MÜHÜR** | 1 |
| **E · SAYFALAR ARASI** | 6 |
| **F · KÜLTÜREL** | 5 |
| **G · İDDİA SÜRÜKLENMESİ** | **12** |
| **Toplam** | **82** |
| En az bir bloklayıcı taşıyan sayfa | **27 / 44** |

### 21.1 · Ve işte fazın dersi

> ### Kapı yeşildi. Kapı doğruydu. Sayfa yine çözülemezdi.

Faz 2'nin dersi *"kapılar cümlenin BİÇİMİNİ ölçüyor, kusur cümlenin
GÖNDERMESİNDE"* idi ve `qa_instruction § ⑨` o dersten doğdu. Faz 3'ün 44
sayfası o kapıdan **geçti** ve on bir sayfa yine çözülemezdi:

```
levha: beş renk kartı        ✓ basılı
levha: beş yön kartı         ✓ basılı
hangisi hangisiyle gider     ✗ HİÇBİR YERDE
```

`§ ⑨` bir adımın işaret ettiği **ADI** çözüyor. Bir eşleştirmenin
gerektirdiği **İLİŞKİYİ** çözmüyor. İki ayrı sorudur ve ikincisi hiç
sorulmamıştı.

> **Bir kapı bir kusur sınıfını kapatır, sınıfın komşusunu değil.**

### 21.2 · İkinci örüntü: yeni katman, eski kusur

`visualSpec` Faz 3'ün en iyi fikriydi ve **aynı kusuru bir kat yukarıda
yeniden üretti**. `requiredLabels` kapalı bir beyaz listedir ve şu kısıtla
gelir: *"print only the labels listed in requiredLabels."*

Yedi sıralama sayfasında `requiredLabels` boştu — çünkü türetme
`pagePrints` içindeki iki-nokta listelerinden besleniyordu ve o sayfalarda
liste yoktu. Sonuç: **kartların üzerindeki cümleleri basmayı yasaklayan
bir görsel şartnamesi.** Yedi sayfa da boş kart levhası tarif ediyordu.

Cümleler `answer` alanında duruyordu ve aynı kısıt *"no answer may be
visible"* diyordu. Yani şartname kendi kendisiyle çelişiyordu.

> **Bir beyaz liste, neyi dışarıda bıraktığını söylemez.**

### 21.3 · Üçüncü örüntü: ele alındığı YAZILAN risk

Üç `designConstraint` alanı *"field note şunu söyler"* diyordu ve üçünde
de field note onu söylemiyordu. Bu, Faz 2 § 18.5'in bir kat yukarısıdır:
orada dolu bir **tasarım** alanı basılı bir ad sanılıyordu; burada dolu
bir **araştırma** alanı yazılmış bir cümle sanılıyor.

> **Bir riskin ele alındığını YAZMAK, ele almak değildir.**

### 21.4 · En ciddi tekil bulgu — G1

`hawaiian-day-length-plate` *"günün ne kadar değiştiğini"* soruyordu ve
basılı sayı **güneş enerjisi oranıydı**. Çocuk bir Hawai kış gününün yaz
gününün üçte ikisi — yaklaşık sekiz saat — olduğunu çıkarırdı. Honolulu'da
gerçek aralık yaklaşık **%81**'dir.

Faz 3 saatler tablosunu iki kaynakta doğrulayamadığı için **düşürmüştü**
(§ 8.2). Ama onu gerektiren **çerçeveyi** düşürmemişti. Sayfa artık ışığın
**gücünü** soruyor ve iddia tam olarak onu söylüyor.

> **Bir veriyi düşürmek yetmez; onu isteyen soruyu da düşürmek gerekir.**

### 21.5 · İkinci en ciddi — G2

`vietnamese-mountain-water-sort` § 8.2'de **tam olarak** yarışma ayrıntısı
iki kaynakta bulunamadığı için yeniden tasarlanmıştı. Yeni kartlardan biri
*"the mountain spirit **arrives first** and wins her"* diyordu.

*"Arrives first"* yarışmanın kendisidir. Daraltılmış iddia **bir sözcükle**
geri gelmişti — ve o sözcük çocuğun sıraya koyduğu bir kartın üzerindeydi.

> **Bir daraltma, daraltılan şeyin adını taşıyan tek bir sözcükle geri gelir.**

### 21.6 · Kabul edilmeyen bir bulgu — D1

İnceleme, `monsoon` bölge açılışının mühür sözcüğünü (**MONSOON**) iki kez
bastığını ve bölgenin ödül yapısını ilk sayfada bozduğunu söyledi. Öneri:
başlığı *"Mountain and Rain"* yapmak.

**Reddedildi.** İki gerekçe:

1. **Bölge adı A3 ile kilitlidir** (K18) ve başlığı değiştirmek bir kurucu
   kararı gerektirir.
2. Daha önemlisi: eşleşme **bilinçli bir tasarım aygıtıdır**.
   `seal_key.json` gerekçesi bunu açıkça yazıyor — *"bölgenin adını taşır;
   çocuk sözcüğü kurduğunda bölge başlığıyla eşleştiğini görür ve
   doğruluğundan emin olur."* Mühür sisteminin bütün tasarımı **kendi
   kendini doğrulamak** üzerine kurulu (`PROGRESSION_ARCHITECTURE`).

İnceleme `seal_key.json`'u görmedi — göremezdi, dosya depoda değil. Bulgu
**tasarım gerekçesi olmadan** verildi ve gerekçe okununca düşüyor.

**Kısmen kabul:** açılış prozasındaki ikinci geçiş gereksizdi ve kaldırıldı
(*"the rains take over"*). Başlık ve şerit motifi durur.

> Bu, alt-ajanın körü körüne kabul edilmemesinin somut örneğidir
> (yol haritası § 13). 82 bulgunun 81'i kabul edildi; biri gerekçesiyle
> birlikte reddedildi ve **ret de kayda geçti**.

---

## 22 · Bulunan bütün kusurlar

Yazım ve kapılar 17 kusur buldu; iç inceleme 82 tane daha. Aşağıdaki tablo
**kapıların** bulduklarıdır; incelemenin bulguları § 21'de sınıflandı.

| # | Kusur | Bulan | Düzeltme |
|---|---|---|---|
| 1 | *"Her büyük nehir buzda başlar"* — Sutlej **gölden** doğar | yeniden doğrulama | iddia daraltıldı |
| 2 | Nehir→sıradağ eşleştirmesi **çift cevaplıydı** | yeniden doğrulama | adlandırılmış kaynağa çevrildi |
| 3 | *"Yarışmanın dört turu"* iki kaynakta **yok** | yeniden doğrulama | nedensel omurgaya indirildi |
| 4 | Urashima'nın yılları **değişkeye göre değişiyor** | yeniden doğrulama | metin tarihlerine çevrildi |
| 5 | *"Hangi kardeş güneşi aldı"* doğrulanamadı | yeniden doğrulama | **sayfa düştü** |
| 6 | **`qa_age § ⑨` doğru imlâyı cezalandırıyordu** | yazım | eşleyiciye diakritik eklendi |
| 7 | **`selftest` kurgusu elle bakım istiyordu** | `qa_all` | dizin **taranıyor** |
| 8 | **`update_docs` açılışı sayımdan düşürüyordu** | kod okuması | alan düzeltildi (1.015 → 1.175) |
| 9 | Faz 1'den kalan mühür yuvaları | `qa_progression § ①` | üç aday temizlendi |
| 10 | Yıldızlı sözcük **levhada basılı değildi** | `qa_design § ②` | levhaya eklendi |
| 11 | İki levha anahtar girdilerini saymıyordu | `visualSpec` türetmesi | girdiler sayıldı |
| 12 | **`DESIGN_SYSTEM.md` kalıpları ikinci kez basıyordu** | `validate_structure § ③` | tek sahip `STYLE.md` |
| 13 | Prompt kütüphanesinin **kendi örneği** bir cevaptı | K10 okuması | soyutlandı |
| 14 | İki künye **ISBN taşıyordu** | `validate_structure` | yayıncı + yıl biçimine |
| 15 | Bir düzen **yanlış türetiliyordu** | `qa_design § ⑤` | levha kart biçimine |
| 16 | Bir adım **tanınmayan fiille** başlıyordu | `qa_instruction § ①` | **adım değişti, liste değil** |
| 17 | *"the account"* levhada yoktu | `qa_instruction § ⑨` | başlık eklendi |
| **18** | **Eşleştirmenin bir tarafı hiç basılı değildi** | **`qa_design § ⑧` (YENİ)** | anahtar tamamlandı |
| **19** | **`andean-altitude-map` dayanaksızdı** | **`qa_design § ⑧` (YENİ)** | yükseklikler basıldı |
| **20** | **Dokuz Kademe C sayfası ebeveyn notsuzdu** | **`qa_age § ⑩` (YENİ)** | dokuz not yazıldı |

### 22.1 · İki yeni kapı, iki FAZ 2 PİLOT sayfasında kusur buldu

`qa_design § ⑧` yazıldığı gün `aztec-place-glyphs` ve
`andean-altitude-map` sayfalarını kırmızı yaktı — **ikisi de Faz 2
pilotundan**, ikisi de Faz 2'nin 61 bulgulu iç incelemesinden geçmiş.

- `aztec-place-glyphs`: cevap *"grasshopper"* diyordu, anahtar
  **chapulin**'i hiç basmıyordu. Ve kök ile ad arasındaki ilişki hiçbir
  yerde durmuyordu: çocuk *Tenochtitlan*'ın içinde *nochtli* olduğunu
  **bilmek** zorundaydı.
- `andean-altitude-map`: Faz 2 field note'u cevabı veriyordu ve yeniden
  yazılmıştı — ama **yerine bir dayanak konmamıştı**. Sayfa o günden beri
  dayanaksızdı.

> **Bir kapı yalnızca sonraki sayfaları korumaz; önceki sayfaları da
> yeniden yargılar.**

---

## 23 · Kök nedenler ve uygulanan düzeltmeler

Doksan dokuz kusur beş köke iniyor:

### ① Devralınan veri ANLATI eşiğinde doğrulanmıştı — 5 kusur + 12 G bulgusu

*Bir iddianın doğru olması, bir cevabın dayanağı olabilmesi anlamına
gelmiyor.* Ve daha incesi: bir iddia daraltıldıktan **sonra** bile, sayfa
metni daraltılmış sınırın dışına tek bir sözcükle taşabilir (G2).

### ② Kapılar birbirini görmüyordu — 3 kusur

`qa_age` diakritikleri bilmiyordu, `validate_research` onları şart
koşuyordu. `DESIGN_SYSTEM.md` kalıpları basıyordu, `validate_structure`
onu sızıntı sayıyordu. F3 düzeltmesi `qa_solvable § ⑧`'i tetikledi.
**Üçünde de çözüm bir kapıyı gevşetmek değil, doğru katmanı bulmaktı.**

### ③ Ölçek varsayımları elle yazılmıştı — 3 kusur

Tekil alan, sabit dosya adı, havuza dağıtılmış yuva.
*Bir sistemin ölçeklendiği yer, elle yazılmış sabitlerin kırıldığı yerdir.*

### ④ Bir kapı bir sınıfı kapatır, komşusunu değil — 11 A bulgusu

`§ ⑨` ADI çözüyordu, İLİŞKİYİ değil. → `qa_design § ⑧` doğdu.

### ⑤ Denetlenmeyen bir politika bir NİYETTİR — 9 F bulgusu + 3 G12

`CULTURE_POLICY § 3` Kademe C için ebeveyn notu şart koşuyordu ve hiçbir
kapı denetlemiyordu. Faz 1 ve 2'de **ısırmazdı bile** — o fazlarda
yazılmış bir Kademe C sayfası yoktu. Faz 3 dokuz tane yazdı ve dokuzu da
notsuz çıktı. → `qa_age § ⑩` doğdu.

Aynı kök `designConstraint` beyanlarında: → `validate_research § ⑪` doğdu.

### Uygulanan düzeltmeler

| Biçim | Adet |
|---|---:|
| Levha tamamlandı (anahtar · ilişki · kart metni · etiket) | 24 |
| Field note yeniden yazıldı (atıf · sürüklenme · cevap sızıntısı) | 21 |
| Adım yeniden yazıldı | 19 |
| Cevap kaydı düzeltildi | 9 |
| Kademe C ebeveyn notu yazıldı | 9 |
| İddia daraltıldı / kısıt denetlenebilir yazıldı | 7 |
| Bölge açılışı düzeltildi | 2 |
| Sayfa düştü, havuzdan yedek geçti | 1 |
| **Yeni kapı doğdu** | **3** (`qa_design § ⑧` · `qa_age § ⑩` · `validate_research § ⑪`) |
| **Kapı sıkılaştırıldı** | **1** (`qa_age § ⑨` — ad artık field note'ta aranıyor) |
| **Reddedilen bulgu** | **1** (D1 · § 21.6) |

**Hiçbir kapı gevşetilmedi.** Bir kez bir fiil listesini genişletmek
gündeme geldi ve reddedildi: *bir kapıyı susturmanın en kolay yolu,
genellikle onu yok etmektir.*

---

## 24 · Test altyapısı

| Kapı | Yeni | Denetim |
|---|---|---:|
| `validate_spec.py` | **§ ⑤ yeni** | 44 |
| `validate_structure.py` | — | 74 |
| `validate_inheritance.py` | — | 9 |
| `validate_research.py` | **§ ⑪ YENİ** | **27** |
| `qa_matrix.py` | — | 23 |
| `qa_age.py` | **§ ⑨ sıkılaştırıldı · § ⑩ YENİ** | **17** |
| `qa_solvable.py` | — | 9 |
| `qa_instruction.py` | — | 11 |
| `qa_readability.py` | — | 11 |
| `qa_language.py` | — | 7 |
| `qa_progression.py` | — | 7 |
| **`qa_echo.py`** | ✅ **YENİ** | **7** |
| **`qa_design.py`** | ✅ **YENİ** (§ ⑧ dâhil) | **19** |
| `page_budget.py` | — | 6 |
| **`image_prompts.py`** | ✅ **YENİ** | *üreteç · `--check`* |
| `update_docs.py` | **sayım düzeltildi** | *üreteç · `--check`* |

### Kapıların kendi testi: 114 → **151 denetim**

`selftest.py` on altı bölüme çıktı. Faz 3'te eklenen ⑭–⑯:

- **⑭ kurucu aşması bir KİLİT mi** — kapı yükseltme · `passed` beyanı ·
  blokaj kapatma · **sessiz aşma** · gerekçesiz aşma · aşma yokken boş koşma
- **⑮ tekrar** — açılış kalıbı · görev kalıbı · düzleştirici dil ·
  sayfa örtüşmesi · beyansız nakarat · nakarat payı · tek kaynaklı
  kültür · **zorunlu kültürel terim cezalandırılmıyor**
- **⑯ tasarım dizgesi** — basılmayan mühür kuralı · bant dışı açılış ·
  tarif edilmeyen yıldızlı kutu · yuva çelişkisi · **basılmayan yıldızlı
  sözcük** · izinsiz düzen · **tek düzene çökmüş bölge** · şartnamesiz
  sayfa · eksik alan · etiketsiz levha · yinelenen assetId · sözleşme
  dışı dosya adı · **eşleştirmenin basılmayan tarafı** · *iki tarafı da
  basılı eşleştirme GEÇER*

Ve iç incelemeden doğan üç denetim ayrıca sınandı:

- **⑤c** ebeveyn notsuz Kademe C sayfası yakalanıyor mu
- **⑦b** field note'ta karşılanmayan `designConstraint` beyanı
- **⑯(m)(n)** eşleştirmenin basılmayan tarafı · ve yanlış pozitif yok

Her yeni kapı için **kusur fikstürü + selftest + CI entegrasyonu**
üçlüsü tamamlandı.

---

## 25 · Git ve CI

| | |
|---|---|
| Dal | `faz/3-blok-1` |
| Faz 2 dalı | `main`'e merge edilmişti · **v0.2.0** · silinmiş |
| Açık PR (faz başında) | **0** |
| CI (`main`, faz başında) | ✅ success |
| `.gate` | **`phase1`** — değişmedi |
| Depoda **olmayan** | `book.json` · `seal_key.json` · `pilot_tr/` · ham test kayıtları |
| Depoda **olan** | kod · şema · kapılar · **iki yeni doğrulama künyesi** · ölçüm raporları · **görsel kütüphanesi** |

CI iki kez kırmızı yandı ve **ikisi de gerçek kusurdu**:

1. `DESIGN_SYSTEM.md` sayfa kalıplarını ikinci kez basıyordu → sızıntı
2. İki kaynak künyesi ISBN taşıyordu → sahte ISBN kapısı

İkisi de düzeltildi ve sonraki koşu yeşil yandı. **CI kırmızıyken
hiçbir şey ilerlemedi.**

---

## 26 · Kalan kurucu bağımlılıkları

| # | Ne | Kimden | Blokladığı |
|---|---|---|---|
| **A10** | **gerçek çocuk oturumu** | kurucu | **Faz 2'nin kapanması · `.gate` → `phase2`** |
| **A11** | `gates.requirements.phase3` 80 mi 60 mı | kurucu | kapının `phase3`'e yükseltilmesi |
| A4 | kalan 60 aktivitenin seçimi | kurucu | Faz 4 (Faz 3 60'ını seçti) |
| A9 | fizikî prova | kurucu | Faz 5–6 · **KURUCUYA AİT** |
| A5 | ciltli hediye sürümü | kurucu | Faz 4 |
| A6 | yazar biyografisi | kurucu | Faz 6 (`authorBio` null → kırmızı) |
| — | iki ebeveyn okuması | kurucu | Faz 4–5 |
| — | ~150 görselin üretilmesi | kurucu | Faz 5 |

### Açık riskler

| Risk | Ölçü | Azaltma |
|---|---|---|
| **Çocuk oturumu yapılmadı** | 0 oturum · 2 testçi hazır | materyal hazır; **sahte kayıt üretilmedi** |
| 45 kayıt hâlâ provisional | 45/76 | doğrulama **kullanıma göre** ilerliyor; cevap üretemiyorlar |
| Kelime hedefi %33 açık | 14.800 vs 22.000 | ön/arka madde yazılmadı; **fiyat modeli etkilenmiyor** |
| `cipher` oranı havuzun üstünde | %31,7 vs %24,4 | içerikten geliyor; Faz 4'ün üç bölgesi dizge açısından daha hafif |
| 3 bölge hâlâ havuz tahmininde | 3/6 ölçüldü | üç ölçüm birbirine yakın (0,844–0,865) |
| Görsel varlığı **0** | 60 şartname | Faz 5; şartname zinciri kapandı |

---

## 27 · Faz 4 hazırlığı

### Girmek için gereken

- [x] Yol haritası Faz 3 kapsamı — **60 kümülatif aktivite**
- [x] Üç bölge yazıldı ve `written`
- [x] Mountain and Monsoon **erken** planlandı (yükle seçildi)
- [x] Ticari dil **İngilizce** · Türkçe test-only kaldı
- [x] Cevap üreten her yeni iddia yeniden doğrulandı
- [x] Hiçbir provisional iddia cevap kaynağı değil
- [x] Beş aktivite tipi korundu
- [x] Bölge matrisi geçerli
- [x] Yaş · çözülebilirlik · talimat · ilerleme kapıları yeşil
- [x] Mühür mantığı belirlenimci · 19/19
- [x] `pagePrints` 60/60 · görsel şartnamesi 60/60
- [x] Tasarım dizgesi donduruldu ve **kapıya bağlandı**
- [x] `qa_echo` doğdu ve **ısırdığı kanıtlandı**
- [x] Üç bölge sayfa modeliyle ölçüldü
- [x] 148 modeli gerçek veriyle güncellendi (144 · −%2,7)
- [x] Manuscript ve cevap sızıntısı yok
- [x] `selftest` yeşil (**151**) · CI yeşil
- [x] İç editoryal inceleme koşturuldu · 82 bulgu · 81 kabul · 1 gerekçeli ret
- [ ] **A10 — gerçek oturum** ⏳ **BEKLİYOR**
- [ ] `.gate` → `phase2` — **A10 kapanmadan yükseltilmez**
- [ ] **A11 — Faz 3 kapı eşiği** ⏳ kurucu kararı

### Faz 4'ün ilk üç işi

1. **Oturum koşulunca** bulguları uygula, `STYLE.md`'yi v2.0 yap,
   `.gate`'i `phase2`'ye yükselt. Türkçe bulgular İngilizce sürüme
   **yeniden yazılarak** taşınır (K21).
2. Kalan üç bölge: `north-ice` (24) · `middle-sea` (20) ·
   `sun-savanna` (16) = **60 yeni** → kümülatif 120.
3. Final görev **The Cartographer's Seal** ve arka madde.

---

## 28 · Faz 3 neyi kanıtladı

| Soru | Cevap |
|---|---|
| Sistem üç bölgeye ölçekleniyor mu | **Evet.** 60 sayfa on yedi kapıdan geçti |
| Bant içinde olmak sayfayı çözülebilir yapıyor mu | **HAYIR.** On yedi kapı yeşilken 27 sayfa çözülemezdi |
| Ölçeklenirken ne bozuluyor | **Elle yazılmış sabitler.** Üç kusur bu sınıftan |
| İki bağımsız kaynak eşiği iş yapıyor mu | **Evet.** Üç iddiayı cevap kademesinden düşürdü |
| Altı bölge tek şablona çöker mi | **Ölçülüyor artık.** `qa_design § ⑥` · 5–6–8 düzen |
| Kültürel terim tekrarı bir kusur mu | **Hayır** — ve `qa_echo` onu cezalandırmıyor |
| Sayfa modeli genellenebilir mi | **Artık evet.** Üç ölçüm 0,844–0,865 arasında |
| Faz 2'nin kelime tahmini doğru muydu | **Evet.** Mobilya prozanın %75'i kadar |
| Görsel zinciri kapandı mı | **Evet.** talimat → pagePrints → visualSpec → prompt |
| **Çocuklar talimatları yardımsız anlıyor mu** | **HÂLÂ BİLİNMİYOR** |

Son satır Faz 2'de de aynıydı ve bu bir kusur değil bir **dış
bağımlılıktır**. Faz 3 onu çözmedi, çözdüğünü de iddia etmiyor.

---

> ## FAZ 3 TAMAM. AJAN DURUR.
>
> ```
> FAZ 3 ÜRETİMİ           ✅ TAMAM      60 sayfa · 3 bölge · 2 yeni kapı
> KURUCU AŞMASI           ✅ KAYITLI    K27 · kilitlendi
> DIŞ ÇOCUK DOĞRULAMASI   ⏳ BEKLİYOR   0 oturum
> ```
>
> **ÇOCUK DOĞRULAMASI: YAPILMADI.**
>
> `.gate` **`phase1`'de bırakıldı** ve aşma kaydı onu oraya
> **kilitliyor**. Kapı yalnızca gerçek bir çocuk oturumundan sonra
> `phase2` olur.
>
> **Faz 4 başlatılmadı** ve kurucu talimatı olmadan başlamaz.
> **Faz 5 başlatılmadı.** Görsel üretilmedi. Prova sipariş edilmedi.
> KDP'ye dokunulmadı.
