# KURUCU VARLIK TESLİM SÖZLEŞMESİ — yükleme öncesi geçiş

> **The Myth Hunter's Field Book** · 16 Ağustos 2026 · Aşama **1 · BEKLEME**
>
> Bu belge tek bir soruyu cevaplar: **kurucu tam olarak hangi dosyaları,
> hangi ölçüde, hangi adla, nereye koyacak?**
>
> Promptların kendisi burada değil:
> [`IMAGE_PROMPT_LIBRARY.html § 9`](IMAGE_PROMPT_LIBRARY.html)
> (dolu hâl: `IMAGE_PROMPT_LIBRARY.local.html § 9` — depoya girmez).

---

## ⚠ AJAN DURDU. HAT KURULDU AMA ÇALIŞTIRILMADI.

```
PROMPTLAR        ✅ yazıldı ve kütüphaneye eklendi   (§ 9)
İŞLEME HATTI     ✅ tarif edildi                     (03_COVER · 03_APLUS)
GÖRSEL ÜRETİMİ   ⛔ KURUCUYA AİT — ajan üretmez
HAT KOŞUSU       ⛔ kurucu "DEVAM" diyene kadar YOK
```

---

## 0 · Tek bakışta — teslim edilecek 16 dosya

| # | Sınıf | Dosya | Ölçü (px) | Durum |
|---|---|---|---:|---|
| 1 | kapak | `kdp-cover-option-01.png` | 5283 × 3375 | ⏳ bekliyor |
| 2 | kapak | `kdp-cover-option-02.png` | 5283 × 3375 | ⏳ bekliyor |
| 3 | A+ | `aplus-01-hero.png` | 1940 × 600 | ⏳ bekliyor |
| 4–6 | A+ | `aplus-02-what-children-do-01…03.png` | 600 × 600 | ⏳ bekliyor |
| 7 | A+ | `aplus-03-six-regions.png` | 1940 × 600 | ⏳ bekliyor |
| 8 | A+ | `aplus-04-real-cultures.png` | 600 × 600 | ⏳ bekliyor |
| 9–12 | A+ | `aplus-05-screen-free-01…04.png` | 600 × 600 | ⏳ bekliyor |
| 13 | A+ | `aplus-06-maps-and-codes.png` | 600 × 600 | ⏳ bekliyor |
| 14 | A+ | `aplus-07-completion.png` | 1940 × 600 | ⏳ bekliyor |
| 15 | **iç blok** | `fig-yoruba-underdot-letters.png` | 1050 × 600 | ⏳ **BASIM BLOKERİ** |
| 16 | **iç blok** | `fig-korean-river-crossing-sort.png` | 975 × 900 | ⏳ **BASIM BLOKERİ** |

> **İki kapak seçeneğinden yalnızca BİRİ basılır.** İkisi de üretilir,
> kurucu seçer, seçilmeyen `07_ASSETS/rejected/` altına arşivlenir —
> silinmez.

---

## 1 · Üç sınıf, üç AYRI kural takımı

Bu belgenin en pahalı hatası, üç sınıfı tek kuralla teslim etmek olurdu.
Üçü aynı kitabın parçası ama **üç ayrı üretim standardı** taşıyor:

| | **KAPAK** | **A+** | **EKSİK İÇ BLOK** |
|---|---|---|---|
| Renk | RGB **renkli** | RGB **renkli** | **gri tonlama** |
| Üslup | boyalı editoryal illüstrasyon | fotografik-illüstratif | **siyah çizgi · gölgesiz** |
| Çözünürlük | **gerçek 300 dpi** | 300 dpi'lık kaynak | **150 dpi ölçütü (K39)** |
| Metin | **YOK** — CLI basar | **YOK** — Amazon basar | **YOK** — CLI dizer |
| Kültürel kısıt | § 9.2 | § 9.3 | **§ 7 · sayfaya özel** |
| Nihai biçim | **tek PDF** | PNG/JPEG < 3 MB | PNG |

> ### İç bloğun 150 dpi ölçütü KAPAĞA UYGULANMAZ.
>
> K39 bir **iç blok** kararıdır: teslim edilmiş 156 çizgi sanatı için
> ölçüt düşürüldü ve baskı yumuşaklığı kabul edildi. Kapak **yeni
> üretiliyor** ve düşürülmüş bir ölçütü miras almasının hiçbir gerekçesi
> yok. Kapak 300 dpi'da üretilir.

---

## 2 · KAPAK SANATI

### 2.1 · Ölçü — sayfa sayısından türer, elle yazılmaz

| | inç | piksel @300 dpi |
|---|---:|---:|
| **Tam sarmal** (arka+sırt+ön, bleed dâhil) | **17,6103 × 11,2500** | **5283 × 3375** |
| Arka panel (soldaki) | 8,6250 × 11,2500 | 2587 × 3375 |
| **Sırt** (160 sayfa) | **0,3603** × 11,2500 | 108 × 3375 |
| Ön panel (sağdaki) | 8,6250 × 11,2500 | 2588 × 3375 |
| Trim | 8,50 × 11,00 | — |
| Bleed · güvenli kenar | 0,125 · 0,25 | — |

```
2587 + 108 + 2588 = 5283 ✓
```

> ⚠ **Sırt 160 SAYFADAN türedi.** İç blok yeniden üretilir ve sayfa
> sayısı değişirse **sırt da değişir** ve bu tablo geçersizdir.
> `./04_BUILD/metadata.py` yeniden koşar, `03_COVER/COVER_SPEC.md`
> yeniden yazılır, kapak yeniden dizilir. **Hiçbir ölçü elle taşınmaz.**

### 2.2 · Tek üreteç bu ölçüyü tek karede vermez — iki dürüst yol

| Yol | Nasıl | Sonuç |
|---|---|---|
| ① **Panel panel** | ön ve arka **ayrı** üretilir (her biri ≥2588 × 3375), sırt CLI'da düz doku | **gerçek 300 dpi** |
| ② **Yerel yeniden çizim** | üreteç kendi maksimumunda üretir, CLI 300 dpi tuvale gerçek büyütmeyle taşır | 300 dpi **tuval**, kaynak dpi **rapora yazılır** |

> ### ⛔ Üçüncü bir yol YOK: pikseli değiştirmeden DPI etiketini 300 yapmak.
>
> Bir dosyanın başlığındaki `300` sayısını değiştirmek çözünürlük
> üretmez. Hat bunu yapmaz ve yapmadığını `06_REPORTS` altına yazar.

**Tercih:** ① panel panel. Founder'ın üreteci 2588 × 3375 veremiyorsa ②
ye düşülür ve gerçek kaynak dpi **nihai raporda açıkça** durur.

### 2.3 · Görselde OLMAYACAK, CLI'ın SONRADAN basacağı metin

| Yer | Metin | Kaynak |
|---|---|---|
| ÖN | `THE MYTH HUNTER'S FIELD BOOK` | `metadata.json § title` |
| ÖN | `EMRE DOĞAN` | `metadata.json § author` |
| SIRT | başlık + yazar | aynı |
| ARKA | tanıtım metni | `metadata.json § description` |
| ARKA | yaş bandı **8–12** · *screen-free* · *120 puzzles · 22 cultures* | `metadata.json § audience` |
| ARKA | yazar biyografisi | `metadata.json § authorBio` |
| ARKA | **barkod alanı BOŞ** | KDP kendi barkodunu basar |

> **Kapak metni KDP metadata'sıyla HARFİ HARFİNE eşleşmek zorundadır.**
> Bu yüzden metin görsele gömülmez: gömülü metin metadata değişince
> sessizce yalan söyler ve kapağı yeniden ürettirir.

⚠ **Sırt yazısı çok dar bir banda sığar.** Sırt 0,3603 in; KDP sırt
metnini iki kenardan 0,0625 in içeride tutmayı şart koşuyor →
kullanılabilir bant **0,2353 in ≈ 16,9 pt**. Sırt puntosu bunun altında
kalmalı. CLI ölçer ve taşarsa **kırmızı yakar**.

---

## 3 · A+ İÇERİK VARLIKLARI

### 3.1 · Modül seti — öncelik sırasıyla

| # | Modül | Amaç | Görsel | Ölçü |
|---|---|---|---:|---|
| 01 | Standard Image & Text Overlay | HERO / kitap fikri | 1 | 1940 × 600 |
| 02 | Standard Three Image & Text | çocuk ne yapıyor | 3 | 600 × 600 |
| 03 | Standard Image Header with Text | altı bölge | 1 | 1940 × 600 |
| 04 | Standard Single Image & Sidebar | gerçek kültürler / araştırma | 1 | 600 × 600 |
| 05 | Standard Four Image & Text | ekransız deneyim | 4 | 600 × 600 |
| 06 | Standard Single Left Image | harita · kod · gözlem | 1 | 600 × 600 |
| 07 | Standard Image & Text Overlay | bitirme / saha yolculuğu | 1 | 1940 × 600 |

- **Banner:** kabul edilen asgari görsel alan **970 × 300 px**; teslim
  **1940 × 600 px** (2× kaynak — yeniden örnekleme payı bırakır).
- **Kare:** teslim **600 × 600 px**.
- Her nihai dosya **< 3 MB**.

> ⚠ **KDP paneli bir A+ belgesine eklenebilecek modül sayısını
> sınırlar.** Kurucu paneldeki güncel sınırı görür ve bu setten
> **yukarıdan aşağıya** seçer. Sıra öncelik sırasıdır; 01 · 03 · 05 en
> yüksek ticari sinyali taşır.

### 3.2 · Metin görselde DEĞİL, modülde

Amazon *Image & Text Overlay* modüllerinde arka plan görseline metin
eklenmemesini açıkça tavsiye ediyor. Kopya modülün kendi metin alanına
girer.

```
GÖRSEL  →  sahne · ışık · kompozisyon · BOŞ metin alanı
AMAZON  →  başlık · gövde · madde işareti
```

Her modülün **metin-güvenli alanı** § 9.3'te ayrı ayrı yazılıdır.

### 3.3 · A+ pazarlama varlığıdır — ve bu bir SIZINTI riskidir

> ### Ürün sayfası herkese açıktır: A+ görselinde sızdırılan bir cevap, kitabın içindekinden DAHA GENİŞ yayılır.

Hiçbir A+ görseli şunları gösteremez:

- bir bulmaca **cevabı**
- **çözülmüş** bir sayfa (doldurulmuş satır, işaretlenmiş kart)
- bir **mühür harfi** veya **yıldız sözcüğü**
- kitapta olmayan bir **ürün iddiası** (sayfa sayısı, aktivite sayısı,
  ödül, onay)

Bütün hücreler, kutular ve mühür izleri **BOŞ** çizilir.

---

## 4 · İKİ EKSİK İÇ BLOK LEVHASI — **basım blokeri**

### 4.1 · Şu an ne var

`08_OUTPUT/PAPERBACK/interior.pdf` **sayfa 60** ve **sayfa 120**'de
çapraz taramalı, üzerinde şu yazan kutular duruyor:

```
PLACEHOLDER
fig-yoruba-underdot-letters
art not supplied — do not print
```

Yer tutucu **sanat değildir ve öyle olduğunu iddia etmiyor** — ama
basıma girerse kitabı bozar.

### 4.2 · `fig-yoruba-underdot-letters`

| | |
|---|---|
| Aktivite | `yoruba-underdot-letters` · sayfa 60 |
| Ölçü | **1050 × 600 px** · 7,00 × 4,00 in @ 150 dpi |
| Oran · yön | 7:4 · yatay |
| Renk | gri tonlama · siyah çizgi · gölgesiz |
| HAM | `07_ASSETS/raw/fig-yoruba-underdot-letters.png` |
| Nihai | `07_ASSETS/final/interior/fig-yoruba-underdot-letters.png` |

> ### ⭑ GLİFLER ÜRETEÇTEN GELMEZ ⭑
>
> Üreteç **yalnızca levhayı** üretir: cetveller, kutular, hücreler,
> panel ve yazma satırları. **Her harf hücresi BOŞ bırakılır** ve
> gerçek glifleri CLI tipografi katmanı gömülü yazı tipiyle dizer.
>
> Gerekçe: bir görsel üreteci harf altına gelen noktayı güvenilir
> biçimde yerleştiremez — **ve bu sayfada nokta İÇERİĞİN KENDİSİDİR.**
> Uydurulmuş, kaymış veya düşmüş bir nokta levhayı biraz yanlış yapmaz;
> **sayfayı çözülemez ve dilbilimsel iddiayı yanlış yapar.**

### 4.3 · `fig-korean-river-crossing-sort`

| | |
|---|---|
| Aktivite | `korean-river-crossing-sort` · sayfa 120 |
| Ölçü | **975 × 900 px** · 6,50 × 6,00 in @ 150 dpi |
| Oran · yön | 13:12 · yatay |
| Renk | gri tonlama · siyah çizgi · gölgesiz |
| HAM | `07_ASSETS/raw/fig-korean-river-crossing-sort.png` |
| Nihai | `07_ASSETS/final/interior/fig-korean-river-crossing-sort.png` |

> ### ⭑ KART METNİ ÜRETEÇTEN GELMEZ ⭑
>
> Üreteç **yalnızca levhayı** üretir: nehir, iki kıyı, **boş** kart
> dikdörtgenleri, **boş** kare numara kutuları ve yazma satırı. Kart
> metnini CLI dizer.
>
> Gerekçe: **kartların sırası cevabın kendisidir.** Üretecin yerleştirdiği
> bir metnin karışık sırada duracağı garanti edilemez ve kendi numaralı
> yerine düşen bir kart cevabı okura verir.

İki sayfaya özel kısıt (`visualSpec § restrictions`) promptun içinde
durur ve **kısaltılamaz** — özellikle:

- suya **hiçbir şey** çizilmez (yükselen/toplanan hiçbir canlı)
- hiçbir harf görselde **halkalanmaz**
- sayfaya **hiçbir Yorùbá sözcüğü** basılmaz, yalnızca tek harfler

### 4.4 · Yer tutucu ÜZERİNE YAZILMAZ, ARŞİVLENİR

`rawLocation` şu an yer tutucuyu tutuyor. Hat şunu yapar:

```
raw/fig-….png  →  rejected/fig-….placeholder.png   (arşiv)
teslim edilen  →  raw/fig-….png                    (yeni HAM)
raw/           →  processed/  →  final/            (türetilmiş kopyalar)
```

> **HAM teslimden sonra DEĞİŞTİRİLMEZ.** CLI işleme her zaman
> **türetilmiş kopya** üretir. Yer tutucu bir teslim değildir; bu yüzden
> silinmez, **arşivlenir**.

### 4.5 · Dosya adı — iki ad dolaşımda

Aşama-1 brifingi HAM adı `yoruba-underdot-letters.png` diye yazdı;
manifest `fig-yoruba-underdot-letters.png` diyor ve **hat manifesti
okur**.

> **Kanonik ad manifesttekidir:** `fig-` önekiyle.
> Kurucu öneksiz kaydederse intake adımı yeniden adlandırır ve bunu
> rapora yazar. **İki ad da kabul edilir; sessiz eşleşmezlik olmaz.**

---

## 5 · Teslim biçimi — bütün sınıflar için

| | |
|---|---|
| Biçim | **PNG** (aksi açıkça yazılmadıkça) |
| Renk profili | kapak/A+ **sRGB** · iç blok **gri tonlama** |
| Şeffaflık | **yok** — düz beyaz zemin |
| Katman | **yok** — düzleştirilmiş |
| Ad | tablodaki ad, **birebir** |
| Konum | kapak/iç blok → `07_ASSETS/raw/` · A+ → `07_ASSETS/raw/aplus/` |

⚠ `07_ASSETS/raw/aplus/` **henüz yok**; hat ilk koşuda oluşturur.
Kurucu elle de oluşturabilir. `07_ASSETS/raw/**` depoya girmez
(`.gitignore § ③`) — ham görsel hiçbir zaman public depoda durmaz.

---

## 6 · Teslimden sonra ne olur

Kurucu dosyaları koyar ve **DEVAM** der. Ajan o zaman:

```
① envanter        teslim edilen dosyalar ÖLÇÜLÜR (ad · ölçü · renk · dpi)
② eşleme          hangi dosya hangi şartnameye — SIRAYLA DEĞİL, ÖLÇÜMLE
③ işleme          kırp · ölçekle · renk normalize · türetilmiş kopya
④ yer tutucu      arşivlenir, kaldırılır
⑤ doğrulama       çözünürlük · oran · kısıt · SIZINTI
⑥ iç blok         yeniden dizilir, sayfa sayısı YENİDEN ÖLÇÜLÜR
⑦ kapak           sırt yeniden hesaplanır, tek PDF kurulur, tipografi basılır
⑧ A+              modüllere eşlenir, kopya ayrı hazırlanır
⑨ metadata        yeniden üretilir
⑩ QA              tam ön izleme denetim listesi
⑪ el kitabı       08_OUTPUT/KDP_UPLOAD_HANDBOOK.md
⑫ DUR             yükleme KURUCUNUNDUR
```

> ### ⭑ ② NEDEN "SIRAYLA DEĞİL, ÖLÇÜMLE" ⭑
>
> Faz 6 bunu pahalı öğrendi: *"001–156'yı manifestin ilk 156 girdisine
> sırayla eşle"* talimatı **ölçülerek yanlışlandı** — `001.png` aslında
> Inuktitut levhasıydı, sıralı eşleme ona `fig-maya-bar-dot-numbers`
> derdi. **Yanlış aktiviteye bağlanmış kusursuz bir görsel, o sayfayı
> çözülemez yapar.** Eşleme tahmin edilmez.

---

## 7 · Bu teslim NEYİ ÇÖZMEZ

Dürüstlük gereği: kurucu 16 dosyayı da teslim etse bile şunlar **açık
kalır** ve hiçbiri görselle kapanmaz.

| # | Açık kalan | Sahibi |
|---|---|---|
| 1 | **46 editoryal bulgu** — 9'u *field note cevabı söylüyor* | Aşama 2 · ajan |
| 2 | **Levha ⇄ dizgi çiftlemesi** — 37 mühür kutusu, 75 yazma alanı | Aşama 2 · ajan |
| 3 | **156 iç blok görselinin 300 dpi'ı** — hiçbiri ulaşmıyor | kurucu kararı |
| 4 | **Gerçek çocuk oturumu** (A10) | kurucu · 0 oturum |
| 5 | **Fizikî prova** (A9) | kurucu |
| 6 | **KDP AI beyanı** · **ISBN** | kurucu · panel |
| 7 | **İki ebeveyn okuması** | kurucu |

Ayrıntılı ölçüm ve sınıflandırma:
[`06_REPORTS/KDP_PREFLIGHT_AUDIT.md`](../06_REPORTS/KDP_PREFLIGHT_AUDIT.md)

---

> ## AJAN BURADA DURUR.
>
> Prompt yazıldı · hat tarif edildi · dosya adı ve hedefi belirlendi.
> **Görsel üretilmedi. Yer tutucu kaldırılmadı. Kapak kurulmadı.
> KDP'ye dokunulmadı.**
>
> Kurucu varlıkları teslim edip **DEVAM** dediğinde Aşama 2 başlar.
