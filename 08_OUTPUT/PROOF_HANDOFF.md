# FİZİKÎ PROVA TESLİMİ — A9 · KURUCUYA AİT

> **The Myth Hunter's Field Book** · 16 Ağustos 2026
>
> ```
> PROVA SİPARİŞ EDİLDİ Mİ   ❌ HAYIR
> BASKI KALİTESİ DOĞRULANDI ❌ HAYIR
> ```
>
> **Ajan prova sipariş etmedi, edemez ve ettiğini iddia etmiyor.**
> Bu belge kurucunun provayı NASIL değerlendireceğini yazar.

---

## 0 · Sipariş edilecek şey

| | |
|---|---|
| Format | Ciltsiz · **8,5 × 11 in** |
| Sayfa | **156** |
| İç blok | siyah-beyaz · **beyaz kâğıt** |
| Kapak | mat |
| Dosyalar | `interior.pdf` · `cover.pdf` (bu depodakiler) |

KDP akışı: yayımlamadan önce **Proof Your Book** → *Order a proof copy*.

---

## 1 · ⭑ ÖNCE BU İKİSİ — prova tam olarak bunlar için sipariş ediliyor ⭑

### ① Kapak keskinliği — 89 dpi arka plan

Kapak sanatı **1569 × 1003 px** teslim edildi; 300 dpi için
**5280 × 3375 px** gerekiyordu. Sanat yukarı örneklenmedi.

**Provada bakılacak:** kapağı kol mesafesinde tut ve **eğik ışıkta**
bak. Aranan şey:

- harita ve defter dokusunda **yumuşaklık / bulanıklık**
- ince çizgilerde **basamaklanma**
- başlık ve yazar adı — bunlar **vektördür** ve KESKİN olmalı

> Metin keskin ama arka plan yumuşaksa: beklenen sonuç budur.
> **Metin de yumuşaksa** bir şey ters gitmiştir — bildirin.

**Karar:** yumuşaklık kabul edilebilir mi? Değilse kapak sanatı
yeniden üretilir (`KDP_UPLOAD_HANDBOOK § 5`).

### ② İç blok görselleri — 150 dpi

158 iç blok görselinin **hepsi** 150 dpi etkin çözünürlükte
(kurucu kararı **K39**; KDP tavsiyesi 300 dpi).

**Provada bakılacak sayfalar** — en ince çizgili levhalar:

| Sayfa | Neden |
|---|---|
| **11** | Inuktitut hece anahtarı — ince işaretler, döndürülmüş formlar |
| **26** | Fin dizesi — küçük punto, yoğun metin |
| **39** | Girit labirenti — tek piksel genişliğinde uzun yol |
| **42** | Takımyıldız levhası — nokta ızgarası, ince bağlantı çizgileri |
| **60** | **Yorùbá alt-nokta** — noktanın kendisi İÇERİK · ↓ § 2 |
| **113** | Māori makron — çizginin görünmesi ŞART |
| **121** | Korece nehir — geniş açık alan + ince kıyı çizgisi |
| **149** | Sözlük — 9 pt yoğun metin bloğu |
| **151–154** | Cevap anahtarı — en küçük punto, kana glifleri |

---

## 2 · Bu kitaba ÖZGÜ üç kontrol

### ⭑ Sayfa 60 — nokta görünüyor mu ⭑

Sayfanın bütün iddiası harfin **altındaki noktadır**:
`e ẹ o ọ s ṣ`. Bu noktalar dizgi katmanında gömülü yazı tipiyle
basıldı (üretecin uydurmasına bırakılmadı).

**Basılı kâğıtta nokta ile lekeyi ayırt edebiliyor musunuz?**
Ayırt edilemiyorsa sayfa çözülemez ve punto büyütülmelidir.

### ⭑ Sayfa 113 — makron görünüyor mu ⭑

`kererū` `tūī` `Māori` — üstteki çizgi kaybolursa sayfa çöker.

### ⭑ Yazma satırları — çocuk eli sığıyor mu ⭑

Ölçüt **7 mm** ve dizgi bunu her sayfada denetliyor. Provada
**gerçekten bir kurşun kalemle yazın**: 8 yaşındaki bir el sığıyor mu?

Bakılacak: **s.125** (levha içi satırlar) · **s.11** (dizgi satırları).

---

## 3 · Genel baskı denetimi

| Denetim | Nasıl bakılır |
|---|---|
| Cilt payı | iç kenardaki metin cilde **girmiyor** mu (s.2, 3, 156) |
| Arka yüz gölgesi | ters ışıkta arkadaki görsel önden **görünüyor** mu |
| Kesim kayması | sayfa numaraları aynı yükseklikte mi |
| Sırt hizası | ön kapak deseni sırtta **kaymış** mı |
| Sırt yazısı | **0,2263 in** bant · taşmış mı, kaymış mı |
| Barkod | Amazon barkodu arka kapağa **basılmış** mı, deseni bozuyor mu |
| Mat kaplama | kalem kapak üstünde **kayıyor** mu (çocuk kitabı üstüne yazar) |
| Boş sayfa | **kaza eseri boş sayfa YOK** — dolgu sayfaları *Field Notes* cetvelli sayfasıdır |

---

## 4 · Provadan sonra

Bulunan her kusur için:

```
sayfa numarası → ne görünüyor → ne beklenirdi → fotoğraf
```

Kaynak düzeltilir, `./04_BUILD/interior.py` yeniden koşar ve **sayfa
sayısı yeniden ÖLÇÜLÜR**. Sayfa sayısı değişirse sırt ve kapak
kendiliğinden yeniden üretilir — elle hiçbir ölçü taşınmaz.

> ⚠ **Prova kitabın çocuklarla test edildiği anlamına GELMEZ.**
> Prova baskıyı ölçer, anlaşılırlığı değil. A10 hâlâ açıktır:
> **sıfır oturum, sıfır testçi.**
