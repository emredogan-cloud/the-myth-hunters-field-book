# NİHAİ SÜRÜM RAPORU — Faz 6 · proje kapanışı

> **The Myth Hunter's Field Book** · 16 Ağustos 2026
> Dal `faz/6-uretim` → `main` · Kapı **`release`** · Etiket `v1.0.0`
>
> Altı faz. Bu sonuncusu üç kalemi kapattı ve bir kalemi **kanıtla değil
> kararla** kapattı. Rapor ikisini birbirinden ayırıyor.

---

## ⚠ ÖNCE BU: ÇOCUK DOĞRULAMASI YAPILMADI

```
GERÇEK ÇOCUK OTURUMU     0
TEST EDİLEN ÇOCUK        0
externalValidation       overridden-zero-sessions    ← 'passed' DEĞİL
A10                      KAPANDI — kurucu aşmasıyla (K40)
.gate                    release
```

Kurucu, gerçek bir çocuk oturumu **yapılmadan** A10'u kapatmayı ve kapıyı
yükseltmeyi açıkça seçti. Karar kayıtlıdır, gizli değildir ve
**hiçbir yerde 'passed' olarak yazılmamıştır**.

> ### Bir kapanış KANITLA da olur KARARLA da. İkisi aynı şey değildir ve kayıt hangisi olduğunu söyler.

`project_config § founder.childTesters.closure.whatThisIsNot` beş maddeyi
kalıcı olarak reddediyor: *bir çocuk bu kitabı test etti · kitap
çocuk-doğrulandı · talimatların anlaşıldığı ölçüldü · Faz 2'nin PASS
ölçütü sağlandı · externalValidation 'passed' oldu.*

Araç hazır: `interactive_child_test.html`. Kurucu iki testçisiyle
koşturursa kayıt `CHILD_TEST_LOG.md`'ye girer ve alan **o zaman**
`passed` olabilir.

---

## 0 · Teslim paketi

| Dosya | Ne | Durum |
|---|---|---|
| `08_OUTPUT/PAPERBACK/interior.pdf` | iç blok · **160 sayfa** · 40 MB | ✅ |
| `06_REPORTS/tracked/metadata.json` | KDP alan değerleri | ✅ |
| `03_COVER/COVER_SPEC.md` | sırt ve kapak geometrisi | ✅ |
| `07_ASSETS/final/interior/` | **158 / 158** nihai görsel | ✅ |
| `01_SOURCE/pilot_tr/interactive_child_test.html` | çocuk testi aracı | ✅ *depo dışı* |
| Kapak **sanatı** | — | ❌ **kurucuya ait** |

| Ölçüm | Değer |
|---|---:|
| Sayfa (PDF'ten sayıldı) | **160** |
| Model ↔ ölçüm sapması | **%0,0** |
| Trim | 8,5 × 11,0 in |
| **Sırt** | **0,3603 in** |
| **Tam kapak (bleed dâhil)** | **17,6103 × 11,2500 in** |
| Liste · baskı | 14,99 $ · 3,72 $ |
| **Ciltsiz telif** | **5,27 $** |
| Başabaş ACOS | %35,2 |
| Efektif çözünürlük | **150 dpi** (158/158 · ölçüt 150) |

---

## 1 · A13 — sayfa **160** · ölçüm modeli yendi (K38)

Faz 6 gerçek dizgi motorunu kurdu ve sayfa sayısını beş fazda **ilk kez
ölçtü**. Sonuç modeli yalanladı.

```
MODEL  (page_budget · pageWeight toplamı)   144
ÖLÇÜM  (interior · dizilmiş PDF)            160     ← +16
```

**Kök neden ölçüldü, sayı yamanmadı.** `pageWeight` Faz 1'de **tipe göre**
atanmıştı — `cipher`/`sort` → 0,75 — ve bu *"iki hafif sayfa bir sayfayı
paylaşır"* demekti:

| Ağırlık | Sayfa | Gerçek dikey ihtiyaç |
|---|---:|---:|
| 1,00 | 56 | 8,01" |
| 0,75 | 64 | **8,57"** ← *daha ağır* |

Kullanılabilir yükseklik **10,00"**; paylaşım için gereken **≤5,00"**.
**64 hafif sayfanın sıfırı sığıyor.**

> ### `cipher` ve `sort` sayfaları hafif değildir. 0,75 ölçülmedi, ATANDI.

Ve `DESIGN_SYSTEM § 1.1` zaten sayfa başına **tek** modül yığını
tanımlıyordu; paylaşım dizgenin kendisiyle de çelişiyordu.

168 adayın `pageWeight`i **1,0**'a çekildi. Model artık dizgiyle birebir:
**160 = 160 · sapma %0,0.**

**Kurucu kararı:** 160 kabul edildi, **hiçbir aktivite kesilmedi**. Alt
başlıktaki **120** vaadi korundu; 16 sayfanın bedeli (−0,28 $ telif)
üstlenildi.

---

## 2 · A14 — ölçüt 300 → **150 dpi** (K39)

Teslim edilen 156 ham görselin **hepsi 1,57 MP**. Aktivite hedeflerinde
efektif çözünürlük 166–202 dpi çıkıyordu. Kurucu görselleri yeniden
üretmemeyi ve ölçütü düşürmeyi seçti.

> ### Bir ölçüt düşürülüyorsa, düşürüldüğü SÖYLENMELİDİR.

`production.minDpiHistory` eski değeri, gerekçeyi **ve sonucunu** taşıyor:
*"İç blok çizgi sanatı 150–200 dpi bandında basılacak. KDP tavsiyesi 300
dpi'dır; bu ölçüt düşürülmesi bir kurucu kararıdır ve baskı yumuşaklığı
KABUL EDİLMİŞTİR."*

Fiziksel boy **değişmedi**; `targetPx` yarılandı — aynı inç, yarı piksel.

### 2.1 · ⭑ SIRALI EŞLEME UYGULANMADI — ÖLÇÜLEREK YANLIŞLANDI ⭑

Talimat *"001–156'yı manifestin ilk 156 girdisine sırayla eşle"* diyordu.
Eşleme **görsel olarak sınandı ve yanlış çıktı**:

| Dosya | Gerçekte ne | Sıralı eşleme ne derdi |
|---|---|---|
| `001.png` | **Inuktitut hecelemesi** levhası | `fig-maya-bar-dot-numbers` |
| `121.png` | **Irish** kültür vinyeti | `vig-finnish` |

> **Yanlış aktiviteye bağlanmış kusursuz bir görsel, o sayfayı ÇÖZÜLEMEZ
> yapar** — ve bir kültürü başka bir kültürün sanatıyla etiketler.
> Sıralı eşleme 120 aktivite sayfasının tamamında yanlış resim basardı.

**Doğru eşleme bulundu ve kanıtlandı.** Dosyalar manifest sırasında değil,
**prompt kütüphanesi sırasında** (bölge sırası × sayfa sırası); aradan
**iki** girdi eksik:

```
yönelim eşleşmesi   156 / 156        %100
görsel çapa         001 → inuit-syllabic-signs    ✅
görsel çapa         119 → vig-finnish             ✅
görsel çapa         121 → vig-irish               ✅
görsel çapa         141 → seal-north-ice          ✅
eksik girdi         yoruba-underdot-letters · korean-river-crossing-sort
```

### 2.2 · İki eksik varlık — **dürüst** yer tutucu

Çapraz taramalı, üzerinde `PLACEHOLDER` ve **`art not supplied — do not
print`** yazan kutular. Manifest'te `status: placeholder-art-missing` ve
gerekçe kayıtlı.

> ⚠ **BASIMA GİRMEDEN ÖNCE DEĞİŞTİRİLMELİDİR.** Bu ikisi sanat değildir
> ve öyle olduklarını iddia etmiyorlar.

### 2.3 · Kutular sanata oturtuldu, sanat kutuya zorlanmadı

46 varlıkta teslim edilen sanat kutudan kısaydı. Fark beyazla
doldurulabilirdi — beyaz sayfada görünmez — ama kutu **yanlış boy iddia
etmeye** devam ederdi. Kutular daraltıldı: **yukarı örnekleme yok, kırpma
yok**, doluluk ≈%100.

Bir varlık (`fig-korean-animal-plate`) hedeften 6×97 px küçüktü ve hat
**büyütmeyi reddetti** — K35'in doğru davranışı. Kutusu sanata oturtuldu.

**Sonuç: 158/158 nihai varlık · efektif çözünürlük 150 dpi · ölçüt altı 0.**

---

## 3 · A10 — kurucu aşmasıyla kapandı (K40)

§ 0'ın üstündeki kutu bu kalemin tamamıdır ve tekrar edilmeyecek kadar
açıktır. Kayıt disiplini:

- `externalValidation` **`passed` yapılmadı** — değeri
  `overridden-zero-sessions`
- `sessionsPerformed: 0` · `childrenTested: 0` **açıkça** yazılı
- Aşma kaydı **silinmedi**: üç fazlık genişletme geçmişi (K27 · K30 ·
  K34) ve tavanın üç faz boyunca `phase1`'de kaldığı duruyor
- `gateCeilingHistory` tavanın **ne zaman ve neden** kalktığını taşıyor

---

## 4 · Faz 6'da doğan araçlar

| Betik | Ne yapar |
|---|---|
| `interior.py` | manuscript → **gerçek PDF** · sayfa sayısını ÖLÇER · yazma alanı kapısı |
| `metadata.py` | KDP alanları + **sırt ve kapak geometrisi** (sayfadan türetilir) |
| `child_test_html.py` | Türkçe pilotun ekran sürümü + gözlemci paneli |

`interior.py`'nin asıl işi bir PDF üretmek değil, **bir sayıyı
yalanlayabilmekti** — ve ilk koşusunda yalanladı.

---

## 5 · CI iki kez kırmızı yandı

Rapor bunu gizlemiyor; ikisi de **aynı sınıftandı**.

| # | Ne | Ders |
|---|---|---|
| ① | `07_ASSETS/processed/.gitkeep` hattı temizlerken silindi | takip edilen bir dizin işareti silinebilir |
| ② | `metadata --check` `interior.pdf`i şart koştu | `08_OUTPUT` üretilmiş çıktıdır ve depoda durmaz |

> ### Üretilmemiş bir çıktı, bozuk bir çıktı değildir.

Aynı hata Faz 5'te `update_docs` ile bir kez yapılmıştı. Düzeltmeden
sonra CI ortamı **tam olarak** yeniden sınandı: takip edilen dosyalarla,
manuscript ve build çıktısı olmadan — **22 kapının 22'si + selftest yeşil.**

---

## 6 · Nihai kapı durumu

| Kapı | Denetim |
|---|---:|
| `validate_spec` (release) | 81 |
| `validate_structure` | 75 |
| `qa_assets` | 40 |
| `qa_answerkey` | 35 |
| `validate_research` | 27 |
| `qa_matrix` | 23 |
| `qa_design` | 19 |
| `qa_readability` | 18 |
| `qa_age` · `qa_progression` · `qa_echo` · … | 17 · 14 · 11 · … |
| `metadata` | 8 |
| `interior` | 5 |
| **`selftest`** | **230** |

`qa_all.sh` **yeşil** · kapı **`release`** · başarısız denetim **0**.

⚠ `selftest` 237 → 230: kurucu aşması artık **etkin değil** (A10 kapandı)
ve `§ ⑭` o yüzden atlanıyor. Bu bir körlük değil, kapsam dışı kalmış bir
bölümdür.

---

## 7 · Kurucuya kalan — KDP yüklemesi öncesi

| # | İş | Neden ajanda değil |
|---|---|---|
| 1 | **Kapak sanatı** (17,6103 × 11,2500 in) | tasarım · kurucuya ait |
| 2 | **İki yer tutucunun değiştirilmesi** | ham görsel üretimi kurucuya ait |
| 3 | **Fizikî prova** (A9) | sipariş ve değerlendirme kurucuya ait |
| 4 | **KDP AI beyanı** | panel seçimi kurucuya ait |
| 5 | **ISBN** | KDP ücretsiz verir · sahte ISBN yasak |
| 6 | **İki ebeveyn okuması** | insan okuması |
| 7 | **Gerçek çocuk oturumu** | araç hazır · A10 kanıtla kapanabilir |

### Açık kalan editoryal borç

Faz 5'in bağımsız incelemesinden **46 bulgu** kayıtlı ve düzeltilmedi
(22 B · 19 C · 5 D). En büyük küme: **dokuz sayfada field note cevabı
söylüyor**. `06_REPORTS/LINE_EDITOR_REPORT.md`.

Ayrıca `writingSpaceLines` alanı ile `pagePrints`'in saydığı yazma satırı
**120 sayfanın 63'ünde** uyuşmuyor; dizgi `writingSpaceLines`i kullandı.

---

## 8 · Altı fazın ölçülen özeti

| | Faz 1 | Faz 4 | Faz 5 | **Faz 6** |
|---|---:|---:|---:|---:|
| Yazılmış aktivite | 0 | 120 | 120 | **120** |
| Kültür | 22 | 22 | 22 | **22** |
| Sayfa | 148 *(model)* | 144 *(model)* | 144 *(model)* | **160 *(ÖLÇÜLDÜ)*** |
| Görsel şartnamesi | 0 | 120 | 158 | **158** |
| **Üretilmiş görsel** | 0 | 0 | 0 | **158** |
| Kapı | 5 | 15 | 16 | **18** |
| `selftest` | 47 | 178 | 237 | **230** |
| Doğrulanmış iddia | 0 | 108 | 108 | **108** |
| **Çocuk oturumu** | 0 | 0 | 0 | **0** |

Son satır altı fazda hiç değişmedi ve bu raporun en dürüst satırıdır.

---

## 9 · Bu proje neyi kanıtladı

| Soru | Cevap |
|---|---|
| Bir model bir ölçümle yalanlanabilir mi | **Evet.** 144 beş faz dayandı, dizgi 160 dedi |
| Elle atanmış bir sayı ne kadar yaşar | **Beş faz.** `pageWeight` 0,75 hiç ölçülmemişti |
| Bir kusur üç kapının arasından geçebilir mi | **Evet.** A1/A2 üç DOĞRU kapının arasından geçti |
| Bir eşleme tahmin edilebilir mi | **HAYIR.** Sıralı eşleme 120 sayfada yanlış resim basardı |
| Bir kapı doğru olanı pahalı hâle getirebilir mi | **Evet — üç kez.** Üçünde de düzeltilen kapıydı |
| Bir inceleme raporu sızıntı olabilir mi | **Evet.** Alıntı, metnin kendisi kadar korumalıdır |
| **Çocuklar talimatları yardımsız anlıyor mu** | **HÂLÂ BİLİNMİYOR** |

---

> ## PROJE FAZ 6 SONUNDA. AJAN DURUR.
>
> ```
> İÇ BLOK        ✅ 160 sayfa · 158 gerçek görsel · 40 MB
> METADATA       ✅ KDP alanları + kapak geometrisi
> KAPI           ✅ release · qa_all yeşil · selftest 230
> KAPAK SANATI   ❌ KURUCUYA AİT
> YER TUTUCU     ⚠ 2 varlık — basımdan önce DEĞİŞTİRİLMELİ
> ÇOCUK OTURUMU  ❌ 0 — A10 kararla kapandı, kanıtla değil
> ```
>
> **KDP paneline dokunulmadı. Prova sipariş edilmedi. Yükleme yapılmadı.**
>
> Yükleme kurucunun işidir ve bu rapor onun için yazıldı.
