# SATIR EDİTÖRÜ RAPORU — Faz 5 · takip edilen özet

> # ⚠ İÇ EDİTORYAL İNCELEME — ÇOCUK DOĞRULAMASI DEĞİLDİR
> # INTERNAL EDITORIAL VALIDATION — NOT CHILD VALIDATION
>
> Bu belge tek bir soruyu sorar: **bir yetişkin sayfada basılı olan metni
> harfi harfine okuduğunda kusur görüyor mu?**
>
> **Hiçbir çocuk oturumu yapılmadı. Sıfır testçi.** Bu rapordaki hiçbir
> satır bir çocuğun bir şeyi yapabildiğine ya da yapamadığına dair kanıt
> değildir.
>
> İnceleyen: bağımsız satır editörü + tasarım kırmızı takımı · 14 Ağustos 2026
> Sınıflandırma şeması `PHASE_4_REPORT.md § 27` ile aynıdır.

---

## ⚠ TAM KAYIT BU DOSYADA DEĞİLDİR — VE OLAMAZ

İncelemenin tam hâli her bulguyu **sayfadan birebir alıntıyla** kanıtlıyor.
O alıntılar aktivite prozası ve **cevap** taşıyor; ikisi de karar **K10** ve
**K11** ile public depoya giremez. `validate_structure § ④⑤` bunu mekanik
olarak yakaladı ve raporun kendisi kapıya takıldı.

> ### Bir inceleme raporu, incelediği metni alıntılayarak kanıtlar — ve o alıntı, metnin kendisi kadar korumalıdır.

| Katman | Ne taşır | Depoda |
|---|---|---|
| `06_REPORTS/LINE_EDITOR_REPORT.md` | sınıf · sayı · sayfa kimliği · **karşılık** | ✅ |
| `06_REPORTS/editorial/LINE_EDITOR_FINDINGS.md` | **tam kayıt · birebir alıntılar** | ❌ `.gitignore § ②` |

Bu, envanterin ve prompt kütüphanesinin izlediği ayrımın aynısıdır.

---

## 0 · Tek bakışta

| Sınıf | Bulgu | Karşılık |
|---|---:|---|
| **A · BLOKLAYICI** | **13** | **13 düzeltildi** |
| **B · CİDDİ** | **26** | 4 düzeltildi · **22 kayıtlı, Faz 6'ya** |
| **C · KÜÇÜK** | 19 | **19 kayıtlı, Faz 6'ya** |
| **D · GÖRSEL KISIT** | 8 | 3 düzeltildi · **5 kayıtlı, Faz 6'ya** |
| **Toplam** | **66** | **20 düzeltildi · 46 kayıtlı** |

**Kapsam:** ön maddenin bütün bölümleri · 6 bölge açılışının hepsi · final
görevin 5 sayfası · arka maddenin 6 bölümü · **120 aktivitenin 120'si** ·
37 mühür kutusunun 37'si **birer birer yeniden hesaplandı** · 642 kısıt
satırı.

> ### Faz 4 on bulgu buldu; bu inceleme altmış altı buluyor. Bu bir kalite düşüşü değildir.
>
> Faz 4 **60 yeni sayfayı** inceledi. Bu inceleme **kitabın tamamını** ve
> Faz 5'te yazılmış **ön maddeyi** inceledi — ön madde daha hiç
> incelenmemişti. Ve ilk kez **37 mühür kutusunun aritmetiği** birer birer
> yeniden hesaplandı; A1 ile A2 oradan çıktı ve **hiçbir kapı onları
> görmemişti**.

---

## 1 · A · BLOKLAYICI — 13 bulgu · **13'ü de düzeltildi**

| # | Sayfa / bölüm | Kusur | Karşılık |
|---|---|---|---|
| **A1** | 9 mühür sayfası | Basılı `★` sayısı **harf sırası değil yuva numarasıydı**. İkisi aritmetik olarak imkânsızdı (altı harfli sözcükte ★7, dört harfli sözcükte ★5). `monsoon`'un yedi mühür sayfasının **altısı** listedeydi — o bölgenin mühür sözcüğü **kurulamazdı**. | ✅ dokuz levha düzeltildi · **`qa_progression § ⑧` doğdu** |
| **A2** | ön madde + 6 bölge açılışı + `DESIGN_SYSTEM § 4` | Basılı kural iki **ayrı** büyüklüğü aynı sayı ilan ediyordu. Ölçüm: `sealStarIndex ≠ sealSlot` → **37 sayfanın 27'sinde**. Levha doğruydu, **KURAL yanlıştı**. | ✅ kural yeniden yazıldı (ok yetkili) · şema düzeltildi · **`qa_progression § ⑨` doğdu** |
| **A3** | ön madde + arka madde | *"Hiçbir sayfa başka bir sayfanın cevabına bağlı değildir"* garantisi **kendi paragrafının altı satır altında** yalanlanıyordu; üç karşı örnek ölçüldü. | ✅ vaat doğru olduğu yere daraltıldı (*activity page*) |
| **A4** | `akan-story-web-map` | Levha ve kısıt **beş** kasabayla **beş** bacak istiyordu; beş kasaba **dört** bacak verir. Cevabın istediği 100 mil **altı** kasaba gerektiriyor. | ✅ altı kasaba · cevap değişmedi |
| **A5** | `aztec-maize-journey-sort` | **Faz 5'in kendi ölçüm kısıtı** ("hiçbir kart kendi numaralı yerinde durmasın") levhanın *"card two"* göndermesiyle çelişiyordu. | ✅ adım konuma değil **içeriğe** bağlandı · kısıt korundu |
| **A6** | `maori-macron-length` | Sayfa **üç farklı sayfa** olarak tarif edilmişti (çift / tekil / çift). | ✅ üçü de cevabın kullandığı tekil modele çekildi · beş sözcük `requiredLabels`'a girdi |
| **A7** | `aztec-town-sign-make` | Adım **gri tonlamalı** bir örnekten **renk** kopyalatıyordu; 120 şartnamenin 120'si `grayscale`. | ✅ adım desene bağlandı · levha `hatching` basıyor · etiket eklendi |
| **A8** | `norse-runestone-read` | Adım *"tek kişi"* istiyordu; **iki** ad her iki taşta geçiyor. Cevap ölçütünü sonradan ekliyordu ve o ölçüt de tutmuyordu. | ✅ adım ve cevap ikili hâle getirildi |
| **A9** | `persian-joined-letters` | Adım tekil *"the shape"*, cevap **iki** şekil. Ayrıca ölçüt sözcüğü levhada hiç basılı değildi. | ✅ adım çoğullaştı · ölçüt **levhaya** basılıyor |
| **A10** | `finnish-vowel-harmony` | Üç kusur: adım 3'ün **üç** geçerli cevabı vardı · altıncı test sözcüğü basılı kuralı **bozmuyordu** · field note cevabı veriyordu. | ✅ adım ölçülebilir · test sözcüğü gerçek kural bozanla değişti · field note kültürel bilgiye çevrildi |
| **A11** | `akan-day-name-pairs` | Adım 2 **başka bir sayfanın** levhasını gerektiriyordu — ön maddenin *"hiçbir olgu için geri dönmeyeceksin"* garantisini bozuyordu. | ✅ adım levhada basılı olana bağlandı |
| **A12** | `zulu-click-letters` | `safe-with-adult` sayfanın **zorunlu ebeveyn notu** `book.json`'da yoktu; sayfa ikinci kişi gerektiren tek malzemesini duyurmuyordu. | ✅ not taşındı · 4/4 sayfa notlu |
| **A13** | ön madde + 4 aktivite | Ön madde imlâ kuralını **kendi sayfasında** çiğniyordu; kitapta 14 işaretsiz ad geçişi. | ✅ 14 geçiş düzeltildi (`Yorùbá` · `Òṣun-Òṣogbo` · `Skíðblaðnir` · `Mjölnir` · `Cú Chulainn` · `Sétanta`) |

### 1.1 · A1 ve A2 neden hiçbir kapıdan geçmemişti

Üç kapı bu sayfalara bakıyordu ve **üçü de doğruydu**:

| Kapı | Ne denetliyordu | Sonuç |
|---|---|---|
| `qa_solvable § ⑦` | mühür **HARFİ** yeniden hesaplanıyor mu | ✅ 37/37 doğru |
| `qa_design § ②` | yıldız kutusu **VAR mı** | ✅ 37/37 var |
| `qa_progression § ②` | harf **gerçek bir cevaptan** mı türüyor | ✅ 37/37 |

> ### Kimse **basılı sayının doğru sayı** olduğunu sormamıştı.
>
> Harf doğruydu, kutu vardı, türetme doğruydu — ve levhaya basılan yıldız
> numarası yine de yanlıştı. Bir kusur, üç kapının **arasından** geçebilir.

`qa_progression` 7 → **14 denetim**.

---

## 2 · B · CİDDİ — 26 bulgu · 4 düzeltildi

**Düzeltilenler:** B21 (`egyptian-nile-map` adımı levhada basılmayan bir
özelliğe gönderiyordu) · B24 ve B25 (ön maddenin çocuğa söylemesi gereken
iki şey yalnızca **yetişkin** arka maddesinde duruyordu — Faz 5'in kendi E1
ayrımının sınadığı yer) · B22 (kit sayfası ölçümle çelişiyordu).

**Kayıtlı kalan 22 bulgu üç kümede toplanıyor:**

| Küme | Adet | Ne |
|---|---:|---|
| **Field note cevabı söylüyor** | 9 | `DESIGN_SYSTEM § 1.1` field note'u **ödül** olarak konumlandırıyor; dokuz sayfada **ipucu** olmuş |
| **Yıldız sözcüğü çıkarılamıyor** | 2 | sözcük bankasındaki doğru girdi levhada **tanımlanmamış** |
| **Adım ↔ cevap ↔ levha ayrışması** | 11 | tekil/çoğul, sayım, birim ve ölçüt uyuşmazlıkları |

Dokuz sızıntının hepsi **aynı sınıftan** ve Faz 4 § 27.3 aynı sınıfı dört
sayfada bulmuştu: `qa_solvable § ⑧` anlamlı sözcük örtüşmesiyle çalışıyor
ve **kısa cümleler eşiğin altında kalıyor**.

> **Kapı yanlış değil, ÇÖZÜNÜRLÜĞÜ yetersiz — ve bu bir kapı gevşetme
> gerekçesi değil, bir İNSAN OKUMASI gerekçesidir.**

---

## 3 · C · KÜÇÜK — 19 bulgu · kayıtlı

Sayım tutarsızlıkları (*"the tablet strip"* ↔ dört şerit), kart etiketi
uyuşmazlıkları (levha **harfle**, cevap **numarayla**), birim karışıklığı
(metrik ↔ imperial), terim tutarsızlığı (**peoples** ↔ **cultures**), iki
glif hatası (`٤٧` Arap-Hint, Farsça `۴۷` olmalı; `omega` yerine `omicron`)
ve dört field note ↔ kural şeridi tekrarı.

⚠ **C16 bir Faz 4 kalıntısıdır:** `finnish-lakes-map`'in çift basımı Faz 4
§ 27.3'te **B4 olarak kabul edilmişti** ve hâlâ duruyor. Beş düzeltmeden
dördü uygulanmış, biri uygulanmamış.

---

## 4 · D · GÖRSEL KISIT — 8 bulgu · 3 düzeltildi

Bu sınıf sayfayı **bugün** bozmuyor; **görsel üretildiğinde** bozar.

**Düzeltilenler:** D5 (`aztec-town-sign-make` etiketsizdi — A7 ile birlikte)
· D6 (`maori-macron-length` beş sözcüğü şart koşmuyordu — A6 ile birlikte)
· `persian-joined-letters` ölçüt etiketi (A9 ile birlikte).

**Kayıtlı kalan 5:** iki sayfada `requiredLabels` boş · bir sayfada panel
içerikleri kısıtsız · bir sayfada sayfaya özel hiç kısıt yok · dört
`pagePrints` maddesinde **tasarım gerekçesi** levha metnine sızmış (harfi
harfine dizilirse ikisi cevabı sayfaya basar).

⚠ **Ayrıca ölçüldü:** `writingSpaceLines` alanı ile `pagePrints`'in saydığı
yazma satırı **120 sayfanın 63'ünde** uyuşmuyor. İki alan da satır sayısı
iddia ediyor ve dizgicinin hangisine uyacağı belirsiz. **Faz 6 dizgiden
önce birini yetkili ilan etmelidir.**

---

## 5 · DENETLENEN VE TEMİZ BULUNAN — sayılarla

> Bulgu yokluğu ancak **ölçülmüşse** kanıttır.

### Ön madde iddiaları

| Basılı iddia | Ölçüm | Sonuç |
|---|---|---|
| *"otuz yedi sayfa yıldız kutusu taşır"* | 37 | ✅ |
| *"adımlar dörtten fazla olmaz"* | azami 4 · ★ sayfalarda >2 adım: 0/45 | ✅ |
| *"yalnızca üç yıldızlı sayfalar ipucu taşır"* | ★★★ 25 · ipuçlu 25 · kesişim 25 · her birinde tam 2 | ✅ |
| *"yüz on dokuz sayfa daha"* | 120 − 1 | ✅ |
| *"hiçbir sayfa başkasının cevabına bağlı değil"* | 3 karşı örnek | ❌ **A3 · düzeltildi** |
| *"hiçbir olgu için geri dönmeyeceksin"* | 1 karşı örnek | ❌ **A11 · düzeltildi** |
| *"kit'in tamamı bu"* | `ruler` 0/120 · anılmayan malzeme 38+2+1+1 | ❌ **B22 · düzeltildi** |
| *"rotayı kendin çizeceksin"* | iki harita da noktalı çizgiyle basılı | ❌ **B23 · kayıtlı** |

### Mühür mimarisi — 37 kutunun 37'si yeniden hesaplandı

| Denetim | Sonuç |
|---|---|
| Yuvalar bitişik 1…N, boşluk yok | **6/6 bölge temiz** |
| Açılışın duyurduğu sayı = gerçek yuva sayısı | **6/6** · toplam 37 |
| `sealContribution` = `sealStarWord[sealStarIndex−1]` | **37/37** — elle yazılmış tek harf yok |
| Kare sayısı = sözcük uzunluğu | **37/37** |
| Çerçeveli kare = harf sırası | **37/37** |
| Basılı yuva numarası = kayıt | **37/37** |
| Yıldız sözcüğü sayfada basılı | **37/37** · çıkarılabilir **35/37** |
| `openEnded` sayfa mühre harf veriyor mu | **0/15** |
| Basılı ★ = çerçeveli kare | **28/37 → düzeltmeden sonra 37/37** |

### Ses, kalıp, okunabilirlik

| Denetim | Sonuç |
|---|---|
| `Your mission:` kalıbı | **120/120** |
| Field note 15–35 kelime | **120/120** · ortalama 25,7 |
| 18 kelimeyi aşan talimat cümlesi | **0/120** |
| Sayfa başına ikiden fazla ünlem | **0/120** |
| `STYLE § 4` yasak kalıpları | **0 eşleşme** (145 blok) |
| Britanya imlâsı | **0 Amerikan biçim** |
| Türkçe test materyali sızıntısı | **0** |
| Kademe C ebeveyn notu | **14/14** |

---

## 6 · İNCELENMEYEN

- **Gerçek dizgi.** Sayfa kırılımı, satır sonu, gerçek yazma alanı ölçüsü.
  Faz 6'ya ait ve o gün yeniden okunmalıdır.
- **Görsel varlıklar.** Sıfır ham görsel üretildi; D sınıfı bulgular
  **şartname** okunarak yazıldı, görsel okunarak değil.
- **Araştırma iddialarının kendisi.** İnceleme bir iddianın DOĞRU olup
  olmadığını sormadı — `validate_research`'ün işi budur. Tek istisna B1:
  basılı ölçüt, sayfanın kendi kültürel bağlamıyla çelişiyordu.
- **Ve en önemlisi:** *"sekiz yaşındaki bir çocuk bu sayfayı yardımsız
  yapabiliyor mu."* Bunu yalnızca **bir çocuk** cevaplayabilir.

> ### ÇOCUK DOĞRULAMASI: YAPILMADI.
