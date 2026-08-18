# KAPAK ÇÖZÜNÜRLÜK DEĞİŞİMİ + A+ KARŞILAŞTIRMALI DENETİM

> **The Myth Hunter's Field Book** · 18 Ağustos 2026
> Bu tur üç iş yaptı: **çözünürlük değişimi**, **tipografi korunumu**,
> **A+ uygulama denetimi**. Yeni sanat yönü YOK, yeni kopya YOK.

---

## 1 · Kapak sanatı — eski ↔ yeni

| | ESKİ | **YENİ** |
|---|---:|---:|
| Dosya | `kdp-cover-option-01.png` | **`kdp-cover-option-01-4x-300dpi.png`** |
| Piksel | 1569 × 1003 | **6276 × 4012** |
| Megapiksel | 1,57 | **25,18** |
| **Etkin dpi** (17,6013 × 11,2500 in) | **89.1** | **356.6** |
| Gömülü dpi üstverisi | yok | 299,9994 *(beyan)* |
| Dosya | 3,2 MB | 37,3 MB |

> ### ⭑ DOSYA ADI BİR KANIT DEĞİLDİR ⭑
> Dosya adı *4x-300dpi* diyor ve üstveri *299,9994* yazıyor. İkisi de
> **iddiadır**. Kabul kararı ölçümden verildi:
> `etkin dpi = piksel / gerçek fiziksel boy`.

## 2 · Yeni sanatın kabul denetimi

| Denetim | Ölçüm | Sonuç |
|---|---|---|
| Aynı kompozisyon mu | yeni→eski ölçekte **PSNR 32.3 dB** (MAE 4.17/255) | ✅ onaylı sanatın ta kendisi |
| Gerçek detay eklendi mi | kenar enerjisi **4.66×** saf bicubic taban | ✅ super-resolution, yumuşak büyütme DEĞİL |
| En-boy oranı | 1.56431 ↔ gereken 1.56456 (sapma %0.016) | ✅ |
| Kompozisyon uyumu | cilt şeridi 0.4616 ↔ eski 0.4614 | ✅ hizalama birebir çalışır |
| Şeffaflık | her iki dosya tam opak | ✅ |
| Kırpma sonrası dpi | **329.2 dpi** (5794 px) | ✅ hâlâ ≥300 |
| Gömülü tipografi · filigran · logo | 1:1 görsel denetim | ✅ yok |
| Barkod · ISBN | 1:1 görsel denetim | ✅ yok |
| Halüsinasyon metin | defter sayfaları · mühürler · etiket kartları · şerit | ✅ yok — mühürler BOŞ |
| Bozucu yapay artefakt | pusula · ızgara · kabuk · halat 1:1 | ✅ halka/ringing yok |

**SONUÇ: KABUL.** Yeni dosya kanonik kapak sanatıdır.

## 3 · Eski sanatın emekliye ayrılması

Sıra **şart koşulduğu gibi** izlendi: eski dosya ancak yeni dosya
bütün hattı geçtikten SONRA yerinden alındı.

```
① yeni sanat ölçüldü ve kabul edildi
② cover.pdf yeni sanattan YENİDEN üretildi
③ cover-preview.png render edildi
④ KDP ön uçuş 61/61 YEŞİL
⑤ ancak bundan sonra eski dosya arşivlendi
⑥ teslim haritası ve sağlamalar güncellendi
```

Eski dosya **silinmedi**:
`07_ASSETS/rejected/kdp-cover-option-01.superseded-89dpi.png`
gerekçesi ve sha256'sı ile duruyor. `asset_intake --verify` artık
aşılmış teslimleri **arşivde** doğruluyor — kayıp bir arşiv de bir kusurdur.

> **Tek kanonik kapak sanatı vardır.** `07_ASSETS/raw/` altında yalnızca
> yeni dosya ve reddedilmiş Seçenek 2 duruyor.

## 4 · Nihai kapak ölçüleri

| | |
|---|---:|
| Sayfa (iç bloktan ÖLÇÜLDÜ) | **156** |
| Tam kapak | **17.6013 × 11.2500 in** |
| **Sırt** | **0.3513 in** |
| Sırt sol · merkez · sağ | 8.6250 · **8.8006** · 8.9763 in |
| Kullanılan sanat (hizalama sonrası) | 5794 × 3704 px · **329.2 dpi** |
| Yazı tipi | **5 / 5 GÖMÜLÜ** |
| cover.pdf | 52.6 MB · tek sayfa |

## 5 · Sırt optik ortalama — yeniden ölçüldü

```
sapma (önce)        +0.0100 in
optik düzeltme      -0.0100 in
sapma (sonra)       +0.0033 in     ← ölçüt ±0,004
mürekkep kutusu     8.7307 .. 8.8906 in
mürekkep genişliği  0.1600 in      ← sırt bandı 0.3513 in
dikey merkez        5.6350 in      ← hedef 5.6250
```

Yöntem değişmedi: kapak **iki kez** render edilir (sırt yazısıyla ve
yazısız), fark alınır ve o fark tam olarak mürekkebin kendisidir.

## 6 · Ön / arka tipografi — korundu

| Ölçüt | Durum |
|---|---|
| Opak panel | **0** — dört beyaz kutu geri gelmedi |
| Kontrast desteği | harf halesi (bulanık glif maskesi) · kenarsız |
| Mürekkep seçimi | zemin parlaklığından ÖLÇÜLEREK |
| Sanat sürekliliği | cilt şeridi 0.4616 → **0.5000** (sırt merkezi 0,5000) |
| Arka sütun | ölçülen açıklık **1.695 .. 7.815 in** |
| Barkod alanı | 2.00 × 1.20 in **BOŞ** |

**Harf altı karşıtlık (WCAG · ölçüldü):**

| Blok | Oran | Eşik |
|---|---:|---:|
| `back-0` | **15.57 : 1** | 3.0 ✅ |
| `back-1` | **14.14 : 1** | 4.5 ✅ |
| `back-2` | **13.51 : 1** | 4.5 ✅ |
| `back-3` | **13.29 : 1** | 4.5 ✅ |
| `back-4` | **13.15 : 1** | 4.5 ✅ |
| `front-author` | **16.92 : 1** | 3.0 ✅ |
| `front-subtitle` | **11.29 : 1** | 3.0 ✅ |
| `front-title` | **16.32 : 1** | 3.0 ✅ |
| `spine` | **16.43 : 1** | 4.5 ✅ |

Daha keskin sanat karşıtlığı **yükseltti**: en düşük oran 8,77 → **11.29**.

## 7 · ⭑ A+ KARŞILAŞTIRMALI DENETİM ⭑

### 7.1 · Kardeş projede GERÇEKTE ne yapılmış

*The Great Book of World Myths* · `04_BUILD/aplus.py` + `APLUS_UPLOAD_PLAYBOOK.md` okundu ve on modülün görselleri açıldı.

| Soru | Ölçülen cevap |
|---|---|
| Metin görselin İÇİNDE mi | **EVET.** `aplus.py` PIL `ImageDraw.text` ile JPEG'e basıyor |
| Amazon modül alanına da giriliyor mu | **HAYIR — kasıtlı.** Playbook: *"Headline / body → BOŞ bırakılır (görsel zaten taşıyor)"* |
| Neden | Playbook açıkça yazıyor: o projede **görsel üreteci kapakta kitabın adını yanlış yazmıştı**; bütün tipografi görsele deterministik basıldı |
| İstisna | Modül 6 *Single Image & Sidebar* — görselde yazı yok, **sidebar metni panele girilir** |
| Modül tipleri | Image Header with Text · Image & Light Text Overlay · Four Image & Text · Single Right/Left Image · Single Image & Sidebar · Company Logo |
| Ölçüler | 970×600 · 970×300 · 4×220×220 · 300×300 · 300×400 · 600×180 (**asgari** ölçüler) |
| Alt text | **her görselde ZORUNLU** olarak dolduruluyor |

**Görsel gözlem:** kardeş projenin metni **opak krem panellere** basılmış —
kurucunun bu kitabın kapağında reddettiği örüntünün ta kendisi. Ayrıca
`aplus-009-parent` modülünde alt satır (*"nothing made gentler than it is"*)
**kırpılmış** durumda.

### 7.2 · Karar: bu kitapta kopyalanmadı — ve gerekçe ölçülebilir

> ### Kardeş kitabın gerekçesi bu kitapta YOKTUR.
>
> O proje tipografiyi görsele bastı çünkü **üreteç metni yanlış
> yazıyordu**. Bu kitapta metin de üreteçten gelmiyor:
> `metadata.json` ölçümlerinden türetiliyor ve Amazon onu kendi
> alanlarında **duyarlı** olarak basıyor. Aynı riski çözmek için
> aynı bedeli ödemeye gerek yok.

Baskın nedenler:

| # | Neden görsele gömülmüyor |
|---|---|
| ① | Amazon *Image & Text Overlay* modüllerinde arka plana metin eklenmemesini **tavsiye ediyor**; gömülü metin overlay ile **iki kez** görünür |
| ② | Gömülü metin **düzeltilemez** — bu kitabın sayfa sayısı zaten 160 → 156 değişti; gömülü bir A+ görseli o gün bayatlardı |
| ③ | Gömülü metin **mobilde ölçeklenmez** ve dil değişirse yeniden çizim ister |
| ④ | Bu projenin kendi şartnamesi (`APLUS_PRODUCTION_PLAN § 1`) zaten bunu söylüyor |

### 7.3 · Peki bu paket eksik miydi?

**Başlık ve gövde açısından HAYIR** — onlar modül alanlarına ait ve
haritada tam olarak duruyorlar. Ama denetim **gerçek bir eksik** buldu:

> ### ⚠ ALT TEXT hiçbir görselde yoktu.
>
> Kardeş projenin playbook'u onu *"erişilebilirlik; zorunlu"* diye
> işaretliyor ve KDP paneli ayrı bir alan olarak soruyor. Bu haritada
> hiç yoktu.
>
> Alt metin bir pazarlama alanı değildir: **görmeyen bir okurun
> gördüğü tek şeydir.**

**Eklendi:** 11 görselin 11'ine betimleyici alt metin. Metinler görseli
TARİF eder, pazarlama cümlesini tekrarlamaz.

**Ayrıca eklenen kapı** — kardeş projenin pahalı dersinden:
o projede iki modül **metinsiz** çıkmış ve hiçbir kapı görmemişti
(doğrulama yalnızca ölçü/renk/dosya boyutuna bakıyordu). Artık her
görsel için başlık · gövde · alt metin · yuva başlığı · yuva gövdesi
**boş olamaz**; `aplus` kapısı 32 → **77 denetim**.

**Ve haritaya bir uyarı kondu:** iki kitabın sözleşmesi birbirinin
**tersidir**. Kardeş kitabın alışkanlığıyla burada alanları boş
bırakmak ürün sayfasını metinsiz bırakır.

## 8 · A+ paketi — doğrulanan sayılar

| | Beyan | **Ölçüm** |
|---|---:|---:|
| Modül | 7 | **7** ✅ |
| Görsel | 11 | **11** ✅ |
| Alt metin | — | **11 / 11** ✅ |
| Ölçü sapması | — | **0** ✅ |
| 3 MB üstü dosya | — | **0** ✅ |
| Bayat sayfa iddiası | — | **0** ✅ |
| Çocuk testi iddiası | — | **0** ✅ |
| Ödül / bestseller iddiası | — | **0** ✅ |
| Yinelenen kopya | — | **0** — üç görselli iki modülün altı yuvası ayrı metin taşıyor ✅ |
| Cevap / mühür sızıntısı | — | **0** ✅ |

QA önizlemesi: `08_OUTPUT/APLUS/preview/` — yedi modülün ürün
sayfasında nasıl dizileceğini gösterir. **Yüklenmez**; nihai görseller
metinsizdir ve öyle kalır.

## 9 · Testler

| Süit | Sonuç |
|---|---|
| `qa_all.sh` | ✅ bütün kapılar yeşil |
| KDP ön uçuş | ✅ **61 / 61** · **uyarı 0** |
| `selftest` | ✅ **230** |
| `covers.py` | ✅ **13** denetim · uyarı 0 |
| `aplus.py` | ✅ **77** denetim |
| `asset_intake --verify` | ✅ **30** denetim |
| CI ortamı (yalnız takip edilen dosyalar) | ✅ yeşil |

> ⭑ **Kapak dpi uyarısı KAYBOLDU** — çünkü artık bir uyarı değil, bir
> **kapı**: `covers.py` etkin dpi < 300 ise KIRMIZI yanıyor. Bir eşik,
> karşılanabilir hâle geldiği gün kapıya dönüşür.

## 10 · Kurucuya kalan

| # | İş |
|---|---|
| 1 | **KDP paneli** — yükleme, Previewer, yayımlama |
| 2 | **A+ gönderimi** — modül alanlarını haritadan doldur, alt metinleri gir |
| 3 | **AI beyanı** |
| 4 | **Fizikî prova** (A9) |
| 5 | **Gerçek çocuk oturumu** (A10 · hâlâ **0 oturum**) |
| 6 | İki ebeveyn okuması · fiyat testi |

İç blok tarafında değişmeyen kalemler: 150 dpi levhalar (K39), Farsça
`٤٧` glifi, iki cevap kaydında Arapça harf birleşimi, hangul.

---

> ## DURUM
>
> ```
> KAPAK SANATI     ✅ 329 dpi (kırpma sonrası) · KDP ölçütü KARŞILANDI
> KAPAK TİPOGRAFİ  ✅ opak panel 0 · sırt optik ortalı
> A+               ✅ 7 modül · 11 görsel · 11 alt metin
> KDP UPLOAD READY ✅
> KDP PUBLISHED    ❌ ajan panele dokunamaz
> ```
>
> **Hiçbir şey yüklenmedi, gönderilmedi, yayımlanmadı; prova
> sipariş edilmedi.**
