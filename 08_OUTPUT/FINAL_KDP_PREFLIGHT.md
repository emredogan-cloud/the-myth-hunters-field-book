# NİHAİ KDP ÖN UÇUŞ — ölçüm raporu

> **The Myth Hunter's Field Book** · 16 Ağustos 2026 · Aşama 2
> Üretici: `04_BUILD/kdp_preflight.py` · ham çıktı: `06_REPORTS/kdp-preflight.json`

```
DENETİM      61
YEŞİL        61
KIRMIZI      0
UYARI        1
```

> ⚠ **BU BETİK KDP PREVIEWER'IN YERİNE GEÇMEZ.** Previewer bir Amazon
> hizmetidir ve yalnızca panelde koşar. **Çalıştırılmadı.** Aşağıdaki
> § 6 onun yerine kurucunun elle bakacağı listeyi verir.

---

## 1 · İÇ BLOK PDF

| Ölçüm | Değer | Ölçüt |
|---|---:|---|
| Sayfa | **156** | 110–828 ✅ · ×4 ✅ |
| Trim | 8.500 × 11.000 in | 8,5 × 11,0 ✅ |
| Yazı tipi | **4 / 4 GÖMÜLÜ** | hepsi ✅ |
| Görsel nesnesi | 598 | gömülü ✅ |
| Dosya | 40.6 MB | 650 MB altı ✅ |
| Ek açıklama · JS · gömülü dosya | **0** | yok ✅ |
| Kaza eseri boş sayfa | **0** | ✅ |
| Yer tutucu / `do not print` | **0** | ✅ |
| Yerel dosya yolu · sahte ISBN | **0** | ✅ |
| Türkçe editör metni | **0** | ✅ |

> ⭑ Faz 6'da bu tablonun **yazı tipi satırı 0/3'tü** ve hiçbir kapı onu
> sormamıştı. Aynı kusur `Māori` kelimesini `M■ori` diye bastırıyordu.

## 2 · KAPAK PDF

| Ölçüm | Değer | Ölçüt |
|---|---:|---|
| Sayfa | **1** | tek PDF ✅ |
| Ölçü | **17.6013 × 11.2500 in** | metadata ile aynı ✅ |
| Sırt | **0.3513 in** | 156 sayfadan türetildi ✅ |
| Panel toplamı | arka+sırt+ön = tam en | ✅ |
| Yazı tipi | **4/4 GÖMÜLÜ** | ✅ |
| Başlık ⇄ metadata | birebir | ✅ |
| Yazar ⇄ metadata | birebir | ✅ |
| Sahte ISBN · barkod | **yok** | ✅ |
| Ek açıklama | **0** | ✅ |
| Barkod alanı | 2,00 × 1,20 in **BOŞ** | ✅ |
| **Sanat çözünürlüğü** | **89 dpi** | ⚠ **300 ALTINDA** |

> ⚠ Tek açık kalem. Yukarı örnekleme YAPILMADI; tipografi vektör olduğu
> için METİN keskin. Ayrıntı ve kurucu seçenekleri:
> [`KDP_UPLOAD_HANDBOOK § 5`](KDP_UPLOAD_HANDBOOK.md)

## 3 · A+ PAKETİ

| Ölçüm | Değer |
|---|---:|
| Modül | 7 |
| Görsel | **11** |
| Ölçü sapması | 0 |
| 3 MB üstü dosya | 0 |
| Bayat sayfa sayısı iddiası | 0 |
| Ödül / bestseller / çocuk-testi iddiası | **0** |

> Bir panel **düşürüldü**: `aplus-05`'in kit fotoğrafı CETVEL gösteriyordu
> ve kitapta cetvel kullanan **0** sayfa var (Faz 5 · B22). Ürün sayfası,
> ürünün içermediği bir şeyi göstermez.

## 4 · VERİ TUTARLILIĞI

| Karşılaştırma | Sonuç |
|---|---|
| metadata aktivite = manuscript | **120 == 120** ✅ |
| metadata sayfa = PDF sayfa | **156 == 156** ✅ |
| açıklama sayfa iddiası = PDF | **156** ✅ |
| sırt = sayfa × 0,002252 | **0.3513** ✅ |
| kapak eni = 2×(trim+bleed)+sırt | ✅ |
| kültür · bölge | **22 · 6** ✅ |
| BOOK_STATS ⇄ ölçüm | ✅ |

## 5 · SIZINTI

| Tarama | Sonuç |
|---|---|
| Aktivite sayfalarına birebir düşen cevap | **0** ✅ |
| Nihai mühür sözcüğü çözülmüş hâlde | **0** ✅ |
| Takip edilen 125 dosyada sır | **0** ✅ |
| Takip edilen dosyalarda yerel yol | **0** ✅ |
| PDF üstverisinde yerel yol | **0** ✅ |

> Cevap anahtarı **kitapta vardır ve olmalıdır** — ön madde ve arka kapak
> onu söz veriyor. Tarama cevabın kitapta olmasını değil, **aktivite
> sayfasında** olmasını arar.

## 6 · KDP PREVIEWER TESLİM LİSTESİ — ⭑ KURUCU EYLEMİ ⭑

Previewer çalıştırılmadı. Panelde açıldığında bakılacaklar:

**Beklenen değerler**

```
sayfa sayısı        156
trim                8,5 × 11,0 in
kapak               17.6013 × 11.2500 in
sırt                0.3513 in
ilk sayfa           BAŞLIK SAYFASI (boş değil, 'Title Page' yazmıyor)
son sayfa           Field Notes — cetvelli not sayfası
```

**Elle bakılacak sayfalar**

| Sayfa | Neden |
|---|---|
| 1 | başlık sayfası hiyerarşisi — Faz 6'da BOZUKTU |
| 2 | künye paragrafları — Faz 6'da tek bloğa erimişti |
| 60 | Yorùbá alt-nokta — noktanın kendisi içerik |
| 113 | Māori makron — çizgi görünmeli |
| 121 | Korece nehir — yeni levha |
| 125 | mühür sayfası — **tek** yıldız kutusu olmalı |
| 149 | sözlük — İngilizce, 22 kültür |
| 151–154 | cevap anahtarı — kana glifleri, tofu YOK |
| 156 | Field Notes — boş sayfa DEĞİL |
| kapak | sırt hizası · barkod alanı · metin keskinliği |

**Previewer uyarısı beklenen tek yer:** kapak sanatı çözünürlüğü (§ 2).

---

> **AJAN KDP PANELİNE DOKUNMADI. PREVIEWER ÇALIŞTIRILMADI.**
> **HİÇBİR DOSYA YÜKLENMEDİ.**
