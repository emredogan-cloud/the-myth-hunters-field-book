# YÜKLEME ÖNCESİ DENETİM — Aşama 1 · ölçüm raporu

> **The Myth Hunter's Field Book** · 16 Ağustos 2026 · Kapı `release`
>
> Faz 6 *"KDP paketi hazır"* diyerek kapandı. Bu denetim aynı pakete
> **yükleyecek biri gibi** baktı ve altı kalemi tek tek ölçtü.
>
> Sonuç: **paket hazır değil.** Bir kalem bu koşuda kapandı, beşi açık
> ve biri Faz 6 raporunda **yazandan daha büyük** çıktı.

---

## ⚠ ÖNCE BU: CI YEŞİL, KİTAP HAZIR DEĞİL

```
qa_all.sh          ✅ YEŞİL      22 kapı · selftest 230
KDP'ye hazır       ⛔ HAYIR      5 açık bloker
```

> ### Bir kapı ancak SORDUĞU soruyu ölçer. Sormadığı soru yeşil görünür.
>
> Faz 5 bunu A1/A2 ile öğrenmişti: üç doğru kapı bir kusurun **arasından**
> geçirmişti. Bu denetimin en büyük bulgusu (§ 4) aynı sınıftandır —
> **hiçbir kapı levhanın dizgiyle ÇAKIŞIP çakışmadığını sormamış.**

---

## 0 · Altı kalem — tek bakışta

| # | Kalem | Faz 6 ne diyordu | **Ölçüm** | Durum |
|---|---|---|---|---|
| **A** | İki yer tutucu | 2 varlık eksik | **doğrulandı** · s.60 · s.120 | ⛔ bloker |
| **B** | Metadata "120 pages" | — | **yanlıştı** · kök neden bulundu | ✅ **bu koşuda kapandı** |
| **C** | 46 editoryal bulgu | 9 sayfada sızıntı | **11 sayfa** · 9 değil | ⛔ bloker |
| **D** | `writingSpaceLines` ⇄ `pagePrints` | 63 sayfada uyuşmuyor | **çiftleme** · 37 + 75 sayfa | ⛔ **bloker · büyüdü** |
| **E** | 150 dpi | "ölçüt düşürüldü" | **158/158 · 300 dpi'a ulaşan 0** | ⛔ kurucu kararı |
| **F** | Kapak sanatı | kurucuya ait | geometri ✅ · sanat ⛔ | ⛔ bloker |

---

## A · İKİ YER TUTUCU — doğrulandı, basımı bloke eder

**Ölçüm yöntemi:** `interior.pdf` sayfa sayfa raster'a çevrildi ve iki
sayfa göz ile denetlendi.

| | |
|---|---|
| `fig-yoruba-underdot-letters` | **sayfa 60** · 1050 × 600 px hedef |
| `fig-korean-river-crossing-sort` | **sayfa 120** · 975 × 900 px hedef |

İki sayfada da çapraz taramalı bir kutu ve içinde üç satır duruyor:
varlık kimliği, `PLACEHOLDER` ve **`art not supplied — do not print`**.

> ### Yer tutucu DÜRÜST. Sorun onun yalan söylemesi değil, BASILABİLİR olması.

Manifest `status: placeholder-art-missing` taşıyor ve gerekçe kayıtlı.
Faz 6 bu ikisini gizlemedi — **ama iç blok PDF'i onlarla üretildi ve o
PDF teslim paketinde duruyor.**

**Karşılık:** § 9.4'te iki prompt yazıldı. Ham üretim kurucuya ait.
Hat, yer tutucuyu **silmez**, `07_ASSETS/rejected/` altına arşivler.

---

## B · METADATA "120 PAGES" — ✅ **bu koşuda kapandı**

### B.1 · Ne yanlıştı

`06_REPORTS/tracked/metadata.json § description` — yani **müşterinin
Amazon'da okuyacağı tek metin** — şöyle başlıyordu:

```
Twenty-two peoples. One hundred and twenty pages. …
```

Kitap **160 sayfa**. Fark **40 sayfa**.

### B.2 · Kök neden: sayı doğruydu — **BAĞLI DEĞİLDİ**

Cümle Faz 6'da **elle yazıldı** ve yazıldığı gün sayfa modeli 144'tü
(alt başlıktaki 120 vaadiyle karışmış hâlde). `pageWeight` düzeltilip
dizgi **160** ölçtüğünde (**K38**) açıklama ölçümle birlikte hareket
etmedi — çünkü ölçüme bağlı değildi.

> ### Elle yazılmış bir sayı, kaynağı değiştiği gün sessizce yalan söylemeye başlar.
>
> Bu, `pageWeight = 0,75`'in **birebir aynı** dersidir. O sayı da
> ölçülmemiş, **atanmıştı** ve beş faz yaşadı. Aynı sınıf, ikinci kez.

Ve iki büyüklük gerçekten **AYRIDIR**:

```
120  =  AKTİVİTE (bulmaca) sayısı   ← alt başlığın vaadi · DOĞRU
160  =  SAYFA sayısı                ← dizgiden ölçüldü   · DOĞRU
```

İkisini aynı sözcükle anmak bir pazarlama tercihi değil, bir **hatadır**.

### B.3 · Nasıl düzeltildi — örnek değil, SINIF kapatıldı

`04_BUILD/metadata.py`:

1. Açıklama artık bir **kalıptır**; iki sayı ölçümden gelir
   (`activities` manuscript'ten **sayılır**, `pages` PDF'ten **ölçülür**).
2. `descriptionFacts` alanı açıklamanın **iddia ettiği** sayıları taşır.
3. Yeni kapı **`metadata § ⑤`** dört denetim ekler:

| Denetim | Ne yakalar |
|---|---|
| sayfa iddiası = ölçüm | bayat sayfa sayısı |
| aktivite iddiası = manuscript | bayat aktivite sayısı |
| ölçülen sayfa sayısı metinde geçiyor | sayının düşmesi |
| aktivite sayısı **`pages`** diye anılmıyor | **120 puzzle ≠ 120 page** karışması |
| rakamlı bayat sayfa iddiası yok | `"120 pages"` biçiminin geri gelmesi |

`metadata` kapısı **11 → 16 denetim**.

### B.4 · Yeni açıklama

```
Twenty-two peoples. One hundred and twenty puzzles across one hundred
and sixty pages. Six seals to earn. …
```

> Pazarlama dili **eklenmedi**. Yanlış sözcük (`pages`) doğrusuyla
> (`puzzles`) değiştirildi ve eksik olan gerçek (`160 pages`) yazıldı.
> Cümlenin geri kalanı **değişmedi**.

---

## C · 46 EDİTORYAL BULGU — sızıntı kümesi **9 değil, 11**

Kayıt: [`LINE_EDITOR_REPORT.md`](LINE_EDITOR_REPORT.md) (özet, takip
edilir) · tam kayıt `06_REPORTS/editorial/` altında ve **depoya girmez**
(K10/K11 · alıntılar cevap taşır).

### C.1 · Dağılım

| Sınıf | Toplam | Düzeltildi | **Açık** |
|---|---:|---:|---:|
| A · BLOKLAYICI | 13 | 13 | **0** |
| B · CİDDİ | 26 | 4 | **22** |
| C · KÜÇÜK | 19 | 0 | **19** |
| D · GÖRSEL KISIT | 8 | 3 | **5** |
| **Toplam** | **66** | **20** | **46** |

### C.2 · ⭑ Sızıntı kümesi yeniden sayıldı: **11 sayfa** ⭑

Faz 6 raporu *"dokuz sayfada field note cevabı söylüyor"* diyor. Aynı
kayıt yeniden okundu ve **aynı kusur iki sayfada daha bulundu** — ama
field note'ta değil, **ipucu katmanında**:

| Katman | Bulgu | Sayfa |
|---|---:|---|
| field note / görev satırı cevabı veriyor | **9** | `B5` `B6` `B7` `B8` `B9` `B10` `B11` `B12` `B13` |
| **ipucu** cevabı veriyor | **2** | `B14` `B15` |
| **Toplam okuru çalıştırmadan cevaba ulaştıran sayfa** | **11** | |

> ### Bir sızıntı, hangi kutuda durduğuyla değil, NE YAPTIĞIYLA sınıflanır.
>
> Küme *"field note"* diye adlandırıldığı için ipucu katmanındaki iki
> örnek kümenin dışında kaldı ve **öncelik listesine girmedi**. İkisi de
> tam olarak aynı şeyi yapıyor: okur sayfayı çalışmadan doğru cevabı
> öğreniyor.
>
> `DESIGN_SYSTEM § 1.1` field note'u **ödül** olarak konumlandırıyor;
> ön madde ipucunun cevabı **vermediğini** açıkça vaat ediyor. On bir
> sayfada ikisi de tutmuyor.

### C.3 · Diğer açık kümeler

| Küme | Adet |
|---|---:|
| Yıldız sözcüğü levhadan çıkarılamıyor | 2 (`B2` `B3`) |
| Adım ⇄ cevap ⇄ levha ayrışması | 11 |
| Olgusal hata | 3 (`B1` `B17` `B19`) |
| C · küçük (sayım · etiket · birim · glif) | 19 |
| D · görsel kısıt (görsel üretilince bozar) | 5 |

⚠ **`B19` özel:** bir ★★★ sayfanın cevabı **kayıtta yok**. Arka madde
*sayfa sırasına göre her sayfa için bir giriş* vaat ediyor. Bu bir
üslup kusuru değil, **eksik bir üründür.**

⚠ **`C16` bir Faz 4 kalıntısı:** beş düzeltmeden dördü uygulanmış, biri
uygulanmamış ve iki fazdır duruyor.

### C.4 · Neden hiçbir kapı yakalamıyor

`qa_solvable § ⑧` sızıntıyı **anlamlı sözcük örtüşmesiyle** arıyor ve
**kısa cümleler eşiğin altında kalıyor**. Faz 4 aynı sınıfı dört sayfada
görmüştü.

> **Kapı yanlış değil, ÇÖZÜNÜRLÜĞÜ yetersiz** — ve bu bir kapı gevşetme
> gerekçesi değil, bir **insan okuması** gerekçesidir.

**Aşama 2 önceliği:** 11 sızıntı → `B19` → `B2`/`B3` → olgusal hatalar →
kalan B → D → C.

---

## D · ⭑ EN BÜYÜK BULGU: LEVHA VE DİZGİ AYNI ŞEYİ İKİ KEZ BASIYOR ⭑

Faz 6 raporu bunu şöyle yazmıştı:

> *"`writingSpaceLines` alanı ile `pagePrints`'in saydığı yazma satırı
> 120 sayfanın 63'ünde uyuşmuyor; dizgi `writingSpaceLines`i kullandı."*

**Sayı doğrulandı — teşhis eksik.** Bu bir *"hangi sayı doğru"*
sorusu değil.

### D.1 · Ölçüm

`pagePrints` ifadelerindeki yazma satırı sayısı ile `writingSpaceLines`
alanı 120 sayfada karşılaştırıldı:

| Sınıf | Sayfa |
|---|---:|
| ikisi de > 0 ve **farklı** | **63** ← raporun saydığı |
| `pagePrints` sessiz, alan > 0 | 45 |
| ikisi de > 0 ve **eşit** | 12 |

**63 sayısı birebir doğrulandı.** Ama asıl soru şu değildi.

### D.2 · İki alan aynı şeyi saymıyor — ve **İKİSİ DE BASILIYOR**

```
pagePrints "… writing lines"   →  LEVHANIN İÇİNDE   (sanata çizildi)
writingSpaceLines              →  DİZGİNİN ÇİZDİĞİ  (interior.py, levhanın ALTINA)
```

`interior.py` levhayı yerleştiriyor **ve ardından** kendi cetvelli
satırlarını çiziyor. Levha zaten satır taşıyorsa sayfa **iki ayrı yazma
alanı** taşıyor.

Aynı şey mühür kutusu için de geçerli: `pagePrints` levhaya yıldız
kutusunu bastırıyor, `interior.py` `sealSlot` gördüğünde **bir tane
daha** çiziyor.

### D.3 · Kaç sayfa — ölçüldü

| Çiftleme | Sayfa |
|---|---:|
| **Yıldız kutusu iki kez basılıyor** (levha + dizgi) | **37 / 37** |
| **Yazma alanı iki kez basılıyor** (levha + dizgi) | **75 / 120** |
| Hiçbir çiftleme taşımayan sayfa | **21 / 120** |

**Doğrulama:** `interior.pdf` sayfa 125 raster'a çevrildi ve göz ile
denetlendi. Sayfada **iki yıldız kutusu** ve **iki ayrı yazma satırı
öbeği** var; ikisi de doldurulabilir, ikisi de aynı şeyi istiyor.

> ### 37 mühür sayfasının 37'sinde çocuk İKİ yıldız kutusu görüyor ve hangisini dolduracağını bilmiyor.
>
> Faz 5 `A1` ile yıldız kutusunun **basılı sayısını** düzeltmişti —
> aritmetik artık doğru. Ama **kutunun kaç kez basıldığını** kimse
> sormamıştı. Doğru sayı, iki kez basılınca doğru kalmıyor.

### D.4 · Kök neden

Zincir Faz 5'te doğru kurulmuştu:

```
talimat → pagePrints → visualSpec → prompt → varlık
```

Faz 6 promptu **doldururken** `pagePrints`'in tamamını üretece verdi —
*sayfa mobilyası dâhil*: yazma satırları, yıldız kutusu, numara
kutuları. Üreteç hepsini **sanatın içine çizdi**. Dizgi ise aynı
mobilyayı **kendi işi** sanmaya devam etti.

> ### `pagePrints` iki AYRI şey listeliyor ve liste hangisi olduğunu söylemiyor:
>
> ```
> LEVHANIN çizeceği     anahtar paneli · kartlar · harita · nesne
> DİZGİNİN çizeceği     yazma satırı · yıldız kutusu · numara kutusu
> ```
>
> Ayrım hiçbir yerde **yazılı değil**, bu yüzden ikisi de ikisini de çizdi.

Bu ayrıca kütüphanenin **kendi tipografi politikasını** yalanlıyor
(§ 4: *"Görsele metin GÖMÜLMEZ"*) — teslim edilen levhalar etiketleri,
panel başlıklarını ve kutu yazılarını **gömülü** taşıyor.

### D.5 · Hangi kaynak yetkili

| Soru | Cevap |
|---|---|
| Hangisi yetkili | **`writingSpaceLines`** — dizgiye ulaşan tek alan odur |
| Şartname bayat mı | **Hayır** — `pagePrints` doğru, ama **kime** hitap ettiği yazılı değil |
| Manuscript düzeni yanlış mı | **Hayır** — düzen doğru, **rol ayrımı** eksik |
| Zararsız metadata mı | **HAYIR** — 112 sayfada basılı, görünür bir kusur |
| Basılan sayfaları etkiliyor mu | **EVET** — 99 sayfada (37 kutu + 75 satır, kesişimle) |

### D.6 · Aşama 2 karşılığı — **iki taraf da körlemesine yazılmaz**

1. `pagePrints` maddelerine **rol** eklenir: `plate` / `typeset`.
   Ayrım **ölçülür**, tahmin edilmez.
2. Prompt üretimi yalnızca `plate` rollü maddeleri üretece verir.
3. `interior.py` yalnızca `typeset` rollü mobilyayı çizer.
4. **İki eksik levha bu kuralla üretilir** — § 9.4 promptları zaten
   *"mobilya levhada, metin dizgide"* demiyor: *"levha yalnızca boş
   mobilya, glif ve metin dizgide"* diyor.
5. Yeni kapı: **bir sayfa aynı mobilyayı iki kez basamaz.**

⚠ **Bu düzeltme 156 mevcut levhayı da ilgilendiriyor.** Levhalar gömülü
mobilya taşıyor; ya dizgi o sayfalarda kendi mobilyasını çizmeyi
bırakacak, ya levhalar yeniden üretilecek. **Kurucu kararı gerektirir**
— ve seçim sayfa sayısını değiştirebilir, yani **sırtı da**.

---

## E · 300 dpi — **158 varlığın 158'i ölçütün altında**

### E.1 · Tarihî karar korundu

`production.minDpiHistory` **silinmedi ve değiştirilmedi**:

```
300  →  Faz 1 bootstrap · KDP tavsiyesi        supersededBy: K39
150  →  K39 · kurucu · 16 Ağustos 2026         supersededBy: null
```

K39'un kendi ifadesi zaten dürüst: *"KDP tavsiyesi 300 dpi'dır; bu
ölçüt düşürülmesi bir kurucu kararıdır ve baskı yumuşaklığı KABUL
EDİLMİŞTİR."*

### E.2 · Ama "kapı yeşil" ≠ "KDP uyumlu"

> ### 150 dpi bir PROJE İÇİ İNDİRİLMİŞ EŞİKTİR — KDP asgarisine uygunluk KANITI DEĞİLDİR.
>
> `qa_assets` yeşil yanıyor çünkü **ölçüt 150'ye indirildi**. Kapı
> kendi ölçütünü doğruluyor, KDP'ninkini değil. İkisini aynı cümlede
> anmak yanlış bir güven verir.

### E.3 · Ölçüm — 158 varlığın hepsi tek tek okundu

| | |
|---|---:|
| Ölçülen varlık | **158 / 158** |
| Etkin çözünürlük **≥ 300 dpi** | **0** |
| Etkin çözünürlük **= 150 dpi** | **158** |
| Toplam mevcut piksel | **120,4 MP** |
| Gerçek 300 dpi için gereken | **481,5 MP** |
| **Gereken çarpan** | **× 4,00** |

Örnek: `fig-maya-bar-dot-numbers` — 975 × 679 px, fiziksel boy
6,50 × 4,53 in. Gerçek 300 dpi **1950 × 1359 px** ister.

### E.4 · Bunun anlamı — ve anlamı OLMAYANI

```
✅ YAPILABİLİR   iki EKSİK levhayı 300 dpi'da üretmek       (2 varlık)
✅ YAPILABİLİR   KAPAĞI gerçek 300 dpi'da üretmek           (yeni üretim)
✅ YAPILABİLİR   A+ görsellerini 300 dpi kaynaktan üretmek  (yeni üretim)
⛔ YAPILAMAZ     156 mevcut levhayı büyütmek                (piksel yok)
```

> ### ⛔ Piksel eklemeden DPI etiketini 300 yapmak bir düzeltme değil, bir YANLIŞ BEYANDIR.
>
> Hat bunu yapmaz. Yapılmadığı `06_REPORTS` altına **sayı olarak** yazılır.

**Kurucu kararı gerekiyor** ve üç seçenek var:

| # | Seçenek | Bedel |
|---|---|---|
| ① | 156 levhayı **yeniden üret** (4× piksel) | zaman + üretim maliyeti |
| ② | 150 dpi'da **kal**, istisnayı nihai raporda **açıkça** yaz | baskı yumuşaklığı · KDP tavsiyesinin altında |
| ③ | Yalnızca **çizgi yoğunluğu yüksek** sayfaları yeniden üret | karma · ölçümle seçilir |

⚠ **§ D.6 bu kararı etkiliyor:** levhalar zaten yeniden üretilecekse
(gömülü mobilya yüzünden), **300 dpi'ı aynı koşuda almak neredeyse
bedavadır.** İki kararı ayrı ayrı vermek, işi iki kez yapmaktır.

---

## F · KAPAK — geometri hazır, sanat yok

| | |
|---|---|
| Geometri | ✅ `03_COVER/COVER_SPEC.md` · **160 sayfadan türetildi** |
| Sırt | **0,3603 in** · hesaplanmış, elle yazılmamış |
| Tam sarmal | **17,6103 × 11,2500 in** → **5283 × 3375 px @ 300 dpi** |
| Panel aritmetiği | 2587 + 108 + 2588 = **5283** ✓ |
| Ham sanat | ⛔ **teslim edilmedi** |
| `cover.pdf` | ⛔ **üretilmedi** |
| `covers.py` | ⛔ **yazılmadı** (yol haritası Faz 6 § 8 şart koşuyor) |

**Karşılık:** § 9.2'de iki prompt · `03_COVER/COVER_PRODUCTION_PLAN.md`
hattı tarif ediyor.

⚠ **Sırt geçicidir.** § A ve § D düzeltilince iç blok yeniden dizilir ve
sayfa sayısı 160'ta kalmayabilir. Kapak **iç bloktan sonra** kurulur.

---

## G · Denetlenen ve TEMİZ bulunan

> Bulgu yokluğu ancak **ölçülmüşse** kanıttır.

| Denetim | Sonuç |
|---|---|
| `qa_all.sh` · 22 kapı | ✅ yeşil |
| `selftest` | ✅ 230 denetim |
| Sayfa sayısı: PDF ölçümü ⇄ metadata ⇄ kapak | ✅ 160 · 160 · 160 |
| Sırt formülü sayfa sayısından türüyor | ✅ elle yazılmış sırt yok |
| Takip edilen dosyalarda cevap sızıntısı | ✅ 0 |
| Takip edilen dosyalarda manuscript sızıntısı | ✅ 0 |
| Sahte ISBN | ✅ 0 |
| Yer tutucu **metin** (metadata) | ✅ 0 |
| `authorBio` dolu | ✅ |
| Görsel ⇄ aktivite eşlemesi | ✅ 156/156 ölçülerek doğrulandı (Faz 6) |
| Prompt kütüphanesinin **takip edilen** sürümü cevap taşıyor mu | ✅ hayır — `{PRINT_LIST}` · `{REQUIRED_LABELS}` |
| İç blok PDF açılıyor · font gömülü | ✅ |

---

## H · Format kapsamı — **yalnızca ciltsiz**

Soru soruldu ve kayıttan cevaplandı:

| Format | `project_config` | Karar |
|---|---|---|
| **Ciltsiz** | `enabled: true` | ✅ **üretilir** |
| Ciltli | `enabled: false` | ⏸ **A5 · kurucu · açık** |
| Kindle | `enabled: false` | ⛔ **üretilmez** |

> Yol haritası Faz 6 § 2: *"Kindle üretilmez. Üzerine yazılan bir kitap
> e-okuyucuda çalışmaz ve kötü yorum üretir. Bu bir gelir kaybı değil,
> **itibar korumasıdır**."*

⚠ **Yol haritası DoD'sinde bir madde açık kaldı:** *`KDP_UPLOAD_PLAYBOOK.md`
yazıldı* — **yazılmadı.** Aşama 2'de
`08_OUTPUT/KDP_UPLOAD_HANDBOOK.md` olarak üretilecek.

---

## I · Aşama 2 iş sırası — bağımlılığa göre

Sıra keyfî değil: her adım bir öncekinin çıktısını **ölçüyor**.

```
①  eksik iki levha üretilir ve doğrulanır          (§ A)
②  pagePrints ROL ayrımı yapılır: plate / typeset  (§ D)   ← KURUCU KARARI
③  11 sızıntı + B19 + kalan editoryal borç          (§ C)
④  levha/dpi kararı — ① ve ② ile AYNI koşuda        (§ E)   ← KURUCU KARARI
⑤  iç blok yeniden dizilir · SAYFA YENİDEN ÖLÇÜLÜR
⑥  metadata yeniden üretilir  → sırt yeniden hesaplanır
⑦  kapak kurulur (tek PDF · tipografi · barkod alanı) (§ F)
⑧  A+ paketi kurulur
⑨  tam ön izleme denetimi
⑩  08_OUTPUT/KDP_UPLOAD_HANDBOOK.md
⑪  DUR — yükleme kurucunundur
```

> ### ⑤ neden ⑦'den önce: sayfa sayısı değişirse SIRT değişir.
> Kapağı önce kurmak, onu iki kez kurmaktır.

**Kurucudan iki karar bekleniyor** (② ve ④) ve ikisi **birlikte**
verilmelidir: levhalar zaten yeniden üretilecekse 300 dpi'ı aynı koşuda
almak neredeyse bedavadır.

---

## J · Bu denetimin kapatmadığı

| # | Açık | Sahibi |
|---|---|---|
| A10 | **Gerçek çocuk oturumu — 0** | kurucu · `externalValidation = overridden-zero-sessions` |
| A9 | **Fizikî prova** | kurucu |
| A5 | Ciltli sürüm | kurucu |
| — | KDP AI beyanı · ISBN | kurucu · panel |
| — | İki ebeveyn okuması | kurucu |

> ### ÇOCUK DOĞRULAMASI: HÂLÂ YAPILMADI.
>
> Bu denetim **bir yetişkinin ölçtüğü** kusurları sayar. *"Sekiz
> yaşındaki bir çocuk bu sayfayı yardımsız yapabiliyor mu"* sorusu altı
> fazdır cevapsız ve bu rapor onu cevaplamıyor.

---

> ## AŞAMA 1 BİTTİ. AJAN DURDU.
>
> ```
> DÜZELTİLDİ   metadata "120 pages" → 120 puzzles / 160 pages  + kapı
> ÖLÇÜLDÜ      6 kalem · 1 tanesi raporda yazandan BÜYÜK çıktı
> YAZILDI      kapak · A+ · iki eksik levha promptları  (§ 9)
> YAZILDI      teslim sözleşmesi · kapak hattı · A+ hattı
> ÜRETİLMEDİ   hiçbir görsel · hiçbir kapak · hiçbir A+ varlığı
> DOKUNULMADI  KDP paneli
> ```
>
> **Kurucu varlıkları teslim edip DEVAM diyene kadar Aşama 2 başlamaz.**
