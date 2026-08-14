# TASARIM DİZGESİ — The Myth Hunter's Field Book

> Sürüm **1.0 · Faz 3** · 13 Ağustos 2026 · `04_BUILD/qa_design.py` uygular
>
> Faz 2 tek bir bölgenin sayfa dilini kalibre etti. Bu belge onu
> **kitap geneline** çıkarır ve **dondurur**.
>
> ⚠ Bu belge sayfanın NE TAŞIYACAĞINI söyler, NASIL GÖRÜNECEĞİNİ değil.
> Tipografi, ızgara ölçüsü ve gerçek dizgi **Faz 5**'e aittir. Burada
> donan şey **yapıdır**; Faz 5 o yapıyı milimetreye çevirir.

---

## 0 · Bu dizgenin çözmeye çalıştığı tek gerilim

```
YAPI TUTARLILIĞI          ⇄          KÜLTÜREL ÇEŞİTLİLİK
"aynı kitap gibi okunsun"            "altı bölge aynı olmasın"
```

İkisi de gerçek gerekliliktir ve birbirini yer:

- Yapı gevşerse çocuk her sayfada **yeniden öğrenmek** zorunda kalır ve
  mühür kuralını hiç oturtamaz.
- Yapı fazla sıkarsa altı bölge **tek bir şablonun altı kopyası** olur ve
  kitabın tezi — *yirmi iki kültür birbirine benzemez* — sayfa
  düzeninin kendisi tarafından yalanlanır.

> **Kurucu talimatı § 15 bunu tek cümlede söylüyor:**
> *structure consistency without cultural homogeneity.*

Bu belgenin çözümü basit ve mekaniktir:

```
SABİT   → sayfanın MODÜLLERİ ve yerleri        (10 modül · değişmez)
SEÇMELİ → sayfanın DÜZENİ                      (10 düzen · tipe göre)
SERBEST → levhanın İÇERİĞİ                     (pagePrints · sayfaya özel)
```

Modüller her sayfada aynıdır. Düzen aktivite tipinden gelir. İçeriği
kültür belirler. `qa_design.py` her bölgenin **en az üç ayrı düzen**
kullanmasını şart koşar — yani bir bölge tek bir şablona çökemez.

---

## 1 · On modül — **SABİT**

> ⚠ **Sayfa kalıplarının tek sahibi [`STYLE.md § 2`](STYLE.md)'dir.**
> Bu belge modüllerin **yerini** ve **zorunluluğunu** dondurur, sözcük
> kalıplarını yeniden basmaz. Kalıbı iki belgede tutmak, iki belgeyi er
> geç iki farklı şey söyletir — ve `validate_structure § ③` bu ikinci
> kopyayı zaten bir sızıntı olarak yakalıyor.

Her aktivite sayfası bu modüllerden kurulur. Sıra da sabittir: çocuk
gözünü bir kez eğitir, 120 sayfa boyunca aynı yerlere bakar.

| # | Modül | Zorunlu | Ne taşır | Kapı |
|---|---|---|---|---|
| ① | **görev satırı** | ✅ her sayfa | tek cümle · kalıp: `STYLE § 2` | `qa_instruction § ⑤` |
| ② | **zorluk işareti** | ✅ her sayfa | ★ · ★★ · ★★★, görev satırının sağında | `qa_age § ⑦` |
| ③ | **levha** | ✅ her sayfa | `pagePrints`in bastığı her şey | `qa_instruction § ⑨` |
| ④ | **adımlar** | ✅ her sayfa | numaralı, ≤4, ★ için ≤2 | `qa_instruction § ③` |
| ⑤ | **field note** | ✅ her sayfa | 15–35 kelime · kalıp: `STYLE § 2` | `qa_readability § ⑥` |
| ⑥ | **kültürel atıf** | ✅ atıf gerektiğinde | kültürün adı, field note içinde | `qa_age § ⑨` |
| ⑦ | **yazma alanı** | ✅ yazdıran sayfada | `writingSpaceLines` satır | `qa_instruction § ⑧` |
| ⑧ | **yıldızlı kutu** | mühür sayfasında | harf kareleri + `★n → seal slot m` (**n ≠ m**) | `qa_design § ②` |
| ⑨ | **ipucu şeridi** | yalnızca ★★★ | iki kademeli ipucu, ters basılı | `ACTIVITY_TAXONOMY § 5` |
| ⑩ | **ebeveyn notu** | `safe-with-adult` sayfada | tek cümle, sayfa dibinde | `qa_age § ③` |

### 1.1 · Modül sırası donduruldu

```
┌──────────────────────────────────────────────┐
│ ① görev satırı                       ② ★★    │
├──────────────────────────────────────────────┤
│                                              │
│                 ③ LEVHA                      │
│         (pagePrints burada basılır)          │
│                                              │
├──────────────────────────────────────────────┤
│ ④ 1. … 2. … 3. …          ⑧ ★n → seal slot m │
├──────────────────────────────────────────────┤
│ ⑦ yazma alanı                                │
├──────────────────────────────────────────────┤
│ ⑤ field note               ⑥ (kültür adı)    │
├──────────────────────────────────────────────┤
│ ⑨ ipucu şeridi (yalnız ★★★)  ⑩ ebeveyn notu  │
└──────────────────────────────────────────────┘
```

**Field note neden ALTTA:** üstte olursa çocuk görevden önce okur ve
`qa_solvable § ⑧`'in yasakladığı şey gerçekleşir — kutu görevi bitirir.
Altta durunca bir **ödül** olur: çocuk çözer, sonra neden öyle olduğunu
öğrenir.

**Yıldızlı kutu neden ADIMLARIN yanında:** Faz 2'nin en pahalı bulgusu
mühür kuralının çocuğa hiç basılmamasıydı. Kutu adımın bittiği yerde
duruyor, çünkü çocuk oraya adımı bitirince gelir.

---

## 2 · On düzen — **SEÇMELİ, tipe bağlı**

Düzen listesi **kapalıdır**. Yeni bir düzen eklemek bilinçli bir
karardır ve `project_config § design.layouts` ile `qa_design` birlikte
değişir.

| Düzen | Tip | Levha ne yapar |
|---|---|---|
| `key-decode` | `cipher` | anahtar paneli + çözülecek öğeler + cevap satırları |
| `key-build` | `cipher` | parça bankası + kurma çerçeveleri |
| `sort-cards` | `sort` | numara kutulu kartlar, karışık basılı |
| `sort-columns` | `sort` | iki sütun, aralarında çizilecek çizgiler |
| `plate-label` | `observe` | tek bir nesne, numaralı işaretçiler, etiket satırları |
| `plate-compare` | `observe` | iki ya da daha çok özne yan yana, fark işaretleri |
| `data-table` | `observe` | sayı tablosu + karşılaştırma kutuları |
| `map-trace` | `map` | harita + izlenecek rota + işaretlenecek noktalar |
| `map-overlay` | `map` | harita + üzerine yatırılacak bir biçim |
| `make-frame` | `make` | tek büyük çerçeve + kısıt + yazma satırı |

### 2.1 · Bir bölge tek düzene çökemez

`qa_design § ⑥` her yazılmış bölgede **en az üç ayrı düzen** arar.

Gerekçe ölçülebilir: bir bölgenin 20 sayfası da `sort-cards` olsaydı
`qa_matrix` yine yeşil yanardı (tip asgarileri tipe bakar, düzene
değil) ve kitap yine de tek bir şablon gibi okunurdu. Tip ile düzen
**aynı şey değildir** ve bu kapı farkı ölçer.

---

## 3 · Bölge açılışı — **SABİT iskelet, DEĞİŞKEN ses**

Her bölge tam olarak üç parça taşır:

| Parça | Uzunluk | Ne yapar |
|---|---|---|
| `heading` | 2–4 kelime | bölgenin adı |
| `terrainLine` | ≤20 kelime | araziyi tek nefeste söyler |
| `openingText` | **120–170 kelime** | bölgenin tezi + **mühür kuralı** |

### 3.1 · Mühür kuralı her açılışın SON paragrafındadır

Bu bir üslup tercihi değil, Faz 2'nin 1 numaralı bloklayıcısının
düzeltmesidir. `qa_design § ①` açılış metninde şu üç şeyi **arar**:

```
star box   ·   seal slot   ·   letter
```

Üçü de yoksa bölge açılışı **eksiktir** ve kapı kırmızı yanar.

### 3.2 · Ses bölgeye göre değişir ve bu ölçülür

Açılışlar aynı iskeleti taşır ama aynı cümleleri taşıyamaz.
`qa_echo § ①` bunu zaten izliyor: iki bölge açılışı aynı kalıpla
başlarsa kapı yanar.

---

## 4 · Mühür modülü — **kitabın tek gerçek arayüzü**

```
★n → seal slot m          ⚠ n ile m AYNI DEĞİLDİR
┌─┬─┬─┬─┬─┬─┬─┬─┐
│ │ │▓│ │ │ │ │ │      ▓ = çerçeveli kare, mühre giden harf
└─┴─┴─┴─┴─┴─┴─┴─┘
   n = HARF sırası (sözcüğün kaçıncı harfi)
   m = YUVA sırası (mühürdeki kaçıncı yer)
```

> ### ⚠ FAZ 5 · BULGU A2 — bu şema bir kez `★n → seal slot n` diyordu
>
> Ve o hâliyle **37 mühür sayfasının 27'sinde yanlıştı.** Yıldız sayısı
> sözcüğün **kaçıncı harfi** olduğunu sayar; yuva sayısı o harfin
> **mühürdeki yerini** sayar. İkisi ayrı büyüklüktür ve yalnızca
> tesadüfen eşit olur.
>
> Aynı yanlış varsayım ön maddede ve altı bölge açılışında **basılı bir
> kural** olarak duruyordu (*"the seal slot with the same number"*).
> Levha zaten doğru oku basıyordu — yani **sayfa doğruydu, KURAL
> yanlıştı** — ve bir kuralı okuyup levhaya bakmayan bir okur harfleri
> yanlış yuvalara yazardı.
>
> `qa_progression § ⑧` bu değişmezi artık mekanik olarak denetliyor.

Dört kural, dördü de mekanik olarak denetleniyor:

| Kural | Kapı |
|---|---|
| Yıldızlı sözcük **sayfada basılıdır**; çocuk kopyalar, üretmez | `qa_solvable § ⑦` |
| Kutu **harf karelerine** bölünür ve hedef kare çerçevelidir | `qa_design § ②` |
| Kutunun yanında `★n → seal slot m` **basılıdır** ve **m okun tek kaynağıdır** | `qa_design § ②` · `qa_progression § ⑧` |
| Harf **hesaplanır**, elle yazılmaz | `qa_solvable § ⑦` · `qa_progression § ②` |

---

## 5 · Kültürel atıf — **görünür, gizli değil**

> **Dolu bir metadata alanı, sayfada basılı bir ad demek değildir.**

Atıf gereken her sayfada kültürün adı **çocuğun gördüğü metinde**
geçer. Yeri field note'tur, çünkü orası adın **bir bilgiye bağlandığı**
yerdir; başlıkta duran bir ad yalnızca bir etikettir.

⚠ Faz 3'te bir kapı kusuru bulundu: eşleyici `Māori` yazımını
tanımıyordu ve kapıyı susturmanın en kolay yolu **makronu düşürmekti**.
Kapı düzeltildi (`qa_age § ⑨`). Bir kapı doğru olanı pahalı hâle
getiriyorsa, düzeltilmesi gereken kapıdır.

---

## 6 · Kaynak ve künye sunumu

Sayfada **kaynak künyesi basılmaz**. Gerekçe yaş: sekiz yaşındaki bir
okur için dipnot sayfayı kalabalıklaştırır ve hiçbir işe yaramaz.

Künyeler iki yerde durur ve ikisi de **erişilebilir**:

| Yer | Ne taşır | Kim okur |
|---|---|---|
| `01_SOURCE/research/*-revalidation.json` | iddia → kaynak zinciri | ajan, kapı, kurucu |
| arka madde · kültür sözlüğü | kültür başına okuma önerisi | ebeveyn, öğretmen |

---

## 7 · Sayfa numarası ve ilerleme göstergeleri

| Öğe | Yer | Kural |
|---|---|---|
| Sayfa numarası | dış alt köşe | ön maddede rakamsız |
| Bölge şeridi | dış kenar | bölgeye özel motif · `region_index § sealStampMotif` |
| Mühür sayacı | bölge sonu | `n / N` doldurulmuş yuva |
| Rota haritası | ön madde · bölge sonu | çocuk kendi doldurur |

**Bölge şeridi kültürel çeşitliliğin taşındığı yerdir:** yapı aynı,
motif altı bölgede altı ayrı şeydir ve `region_index.json` onları
zaten taşıyor.

---

## 8 · Görsel şartnamesi — **metnin ihtiyacından türer**

Karar **K25**: *bir talimat "the X" derse, levha X'i basmak zorundadır.*

Faz 3 bunu bir adım ileri götürüyor: `pagePrints` artık yalnızca bir
kapı girdisi değil, **görsel şartnamesinin girdisi**. Her görsel
gerektiren sayfa bir `visualSpec` taşır:

| Alan | Ne |
|---|---|
| `assetId` | tekil kimlik · `07_ASSETS` içindeki ad |
| `visualClass` | şema sınıfı (`region_index` ile aynı sözlük) |
| `purpose` | görsel sayfada **hangi işi** yapıyor |
| `subject` | tam olarak ne çizilecek |
| `requiredLabels` | levhada **basılı olması gereken** her etiket |
| `orientation` | `portrait` · `landscape` · `square` |
| `targetPx` · `aspect` | hedef ölçü ve oran |
| `safeAreaMm` | kesim payı ve iç boşluk |
| `restrictions` | kültürel/yaş kısıtları — **çizilmeyecek olan** |
| `format` · `filename` · `destination` | üretim çıktısı |

⚠ **Şartname bir varlık DEĞİLDİR.** Faz 3 sonunda üretilmiş görsel
sayısı **sıfırdır** ve `BOOK_STATS` bunu iki ayrı satırda sayar:
*görsel şartnamesi* ve *görsel varlık*. Birini diğerinin yerine saymak,
olmayan bir varlığı var göstermektir.

---

## 9 · Bu dizgenin DEĞİŞTİRMEDİĞİ şeyler

- Okunabilirlik bantları (`STYLE § 3`) — Faz 2'de ölçüldü, değişmedi
- Mühür mekaniği (`PROGRESSION_ARCHITECTURE`) — A3 ile kilitli
- Beş aktivite tipi (`ACTIVITY_TAXONOMY § 2`) — Faz 1'de kilitli
- Sayfa hedefi — kurucu kararı · **Faz 5'te 148 → 144 oldu (`K33` · A12)**
  ve bu bir tasarım kararı DEĞİLDİR: altı bölge gerçek içerikle ölçüldü
  ve model zaten 144'tü. Dizge bu sayıyı okur, üretmez.

> Bir tasarım dizgesi, kendisinden önce alınmış kararları yeniden
> açmaz. Açarsa o bir dizge değil bir revizyondur.
