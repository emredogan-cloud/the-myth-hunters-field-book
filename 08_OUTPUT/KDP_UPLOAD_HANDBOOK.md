# KDP YÜKLEME EL KİTABI — The Myth Hunter's Field Book

> **Ciltsiz (paperback) · tek format** · 16 Ağustos 2026
>
> Bu belge kurucunun KDP panelinde adım adım izleyeceği tek belgedir.
>
> ```
> AJAN-HAZIRLADI    dosyalar üretildi ve denetlendi
> KURUCU-EYLEMİ     panele giren her tıklama
> ```
>
> **AJAN KDP PANELİNE HİÇ DOKUNMADI. HİÇBİR ŞEY YÜKLENMEDİ, HİÇBİR ŞEY
> YAYIMLANMADI.**

---

## 0 · Yüklenecek dosyalar — AJAN HAZIRLADI

| Dosya | Ne | sha256 (ilk 16) |
|---|---|---|
| `08_OUTPUT/PAPERBACK/interior.pdf` | iç blok · **156 sayfa** · 40,6 MB | `c51045c443a235db` |
| `08_OUTPUT/PAPERBACK/cover.pdf` | kapak · **tek PDF** · arka+sırt+ön · 52,6 MB | `c90f910349892d3b` |
| `08_OUTPUT/PAPERBACK/metadata.json` | panele girilecek DEĞERLER | `5ffee7d6ac204430` |
| `08_OUTPUT/PAPERBACK/checksums.txt` | doğrulama | — |
| `08_OUTPUT/APLUS/` | 11 A+ görseli + modül haritası | ayrı dosyada |

Yüklemeden önce doğrula:

```bash
cd 08_OUTPUT/PAPERBACK && sha256sum -c checksums.txt
```

---

## 1 · Ciltsiz kitap — panel adımları

### ① Bookshelf

**KURUCU EYLEMİ.** kdp.amazon.com → oturum aç → **Bookshelf** →
**+ Create** → **Create paperback**.

> Kindle sürümü **oluşturulmaz**. Yol haritası Faz 6 § 2: üzerine
> yazılan bir kitap e-okuyucuda çalışmaz ve kötü yorum üretir. Bu bir
> gelir kaybı değil, itibar korumasıdır.

### ② Paperback Details

Her alan `metadata.json` içinden BİREBİR kopyalanır. Elle yazma.

| KDP alanı | Değer |
|---|---|
| **Language** | English |
| **Book Title** | `The Myth Hunter's Field Book` |
| **Subtitle** | `A Screen-Free Quest Through 22 Cultures — 120 Puzzles, Maps, Codes and Challenges for Ages 8–12` |
| **Series** | boş bırak (Cilt 1; seri sonra kurulur) |
| **Edition Number** | `1` |
| **Author** | Primary Author: `Emre` / `Doğan` |
| **Contributors** | yok |
| **Description** | ↓ § 2.1 |
| **Publishing Rights** | ⦿ *I own the copyright and I hold the necessary publishing rights* |
| **Primary Audience** | Sexually explicit: **No** · Reading age: **8–12** |
| **Primary Marketplace** | Amazon.com |
| **Categories** | ↓ § 2.2 |
| **Keywords** | ↓ § 2.3 |
| **AI-Generated Content** | ↓ § 2.4 — **KURUCU KARARI** |

### 2.1 · Description — kopyala/yapıştır

```
Twenty-two peoples. One hundred and twenty puzzles across one hundred
and fifty-six pages. Six seals to earn. This is not a puzzle book with
a mythology theme — every puzzle is built out of what a people actually
made: a writing system, a counting system, a map of a real place, a
message that had to travel. Children decode Younger Futhark and
Inuktitut syllabics, count in Maya bars and dots, trace the Red River
delta, and sort the Akan day names. Answers are checked against
museums, archives and universities, and the back of the book says which
ones. Screen-free, written in, and finished with a certificate.
```

> ⚠ **Bu metin ÜRETİLMİŞTİR ve iki sayısı ÖLÇÜMDEN gelir.**
> `120 puzzles` aktivite sayısıdır, `156 pages` dizilmiş sayfa sayısıdır.
> İkisi AYRI büyüklüktür; Faz 6 bunları karıştırmıştı (`120 pages`) ve
> `metadata § ⑤` kapısı artık karışmayı mekanik olarak yakalıyor.
> Sayfa sayısı değişirse **metni elle düzeltmeyin** —
> `./04_BUILD/metadata.py` koşturun.

### 2.2 · Categories

**KURUCU EYLEMİ.** KDP artık üç kategori seçtiriyor. BISAC karşılıkları:

| Öncelik | BISAC | Panel yolu (yaklaşık) |
|---|---|---|
| 1 | `JNF001000` | Juvenile Nonfiction → Activity Books → General |
| 2 | `JUV045000` | Juvenile Fiction → Legends, Myths, Fables → General |
| 3 | `JNF025000` | Juvenile Nonfiction → History → General |

> Panel ağacı BISAC kodunu doğrudan sormaz; en yakın dalı seçin ve
> seçtiğinizi buraya not edin.

### 2.3 · Keywords — yedi kutu

```
1  screen free activity book kids 8-12
2  mythology puzzles for children
3  world cultures activity book
4  codes and ciphers for kids
5  maps and mazes puzzle book
6  gift for curious kids age 9
7  homeschool world mythology
```

### 2.4 · AI-Generated Content beyanı — ⭑ KURUCU KARARI ⭑

**AJAN BU SEÇİMİ YAPMAZ VE YAPAMAZ.** Karar kurucuya aittir ve
`metadata.json § aiDisclosure.founderConfirmed = false` olarak
kayıtlıdır.

Kararı verirken bilinmesi gerekenler — **ölçülmüş gerçekler**:

| Katman | Nasıl üretildi |
|---|---|
| **Metin** (120 aktivite · ön/arka madde) | yapay zekâ yardımıyla yazıldı; her kültürel iddia kaynaklarla yeniden doğrulandı |
| **Görseller** (158 iç blok · kapak · A+) | **yapay zekâ üreteciyle** üretildi (kurucu tarafından) |
| **Dizgi · geometri · cevap anahtarı** | deterministik betikler (yapay zekâ değil) |

KDP beyanı üç şey sorar: **metin**, **görseller**, **çeviri**.
Bu kitap için görsellerin AI kaynaklı olduğu **açıktır**; metin de AI
yardımıyla üretilmiştir. Beyanı buna göre doldurun.

> ⚠ Beyanı eksik vermek KDP'nin hesap kapatma gerekçesidir.
> Ajan burada bir tavsiye değil, **ölçülmüş bir envanter** verir.

### ③ ISBN

**KURUCU EYLEMİ.** ⦿ **Assign me a free KDP ISBN**.

> ⚠ `metadata.json § isbn.paperback = null`. Ajan **sahte ISBN
> üretmedi** ve kapağa **barkod basmadı**: KDP ücretsiz ISBN veriyor ve
> barkodu arka kapağın alt bölgesine kendisi basıyor. Kapakta o alan
> **boş ve açık** bırakıldı (2,00 × 1,20 in) ve boşluğu ön uçuş
> denetiminde ölçüldü.

### ④ Manuscript

**KURUCU EYLEMİ.** **Upload paperback manuscript** →
`08_OUTPUT/PAPERBACK/interior.pdf`

| Ayar | Değer |
|---|---|
| Print Options | **Black & white interior with white paper** |
| Trim Size | **8.5 x 11 in** |
| Bleed | **No bleed** |
| Paperback cover finish | **Matte** (önerilir; yazılan bir kitapta parlak yansır) |

### ⑤ Cover

**KURUCU EYLEMİ.** **Upload a cover you already have (print-ready PDF)**
→ `08_OUTPUT/PAPERBACK/cover.pdf`

> **Cover Creator KULLANILMAZ.** Kapak tek PDF olarak hazırdır:
> **17,6013 × 11,2500 in**, sırt **0,3513 in** (156 sayfadan türetildi),
> 0,125 in bleed, bütün yazı tipleri gömülü.

✅ **Kapak sanatı 329 dpi** (sırt hizalama kırpmasından sonra ölçüldü) —
KDP 300 dpi ölçütünü karşılıyor. ↓ § 5.

### ⑥ Previewer

**KURUCU EYLEMİ.** **Launch Previewer** → her sayfayı gözden geçirin.

Denetim listesi: [`08_OUTPUT/FINAL_KDP_PREFLIGHT.md § Previewer`](FINAL_KDP_PREFLIGHT.md)

> Previewer bir Amazon hizmetidir ve yalnızca panelde koşar.
> **Ajan onu ÇALIŞTIRMADI ve çalıştırdığını iddia etmiyor.**

#### ⭑ ÖNCEKİ PREVIEWER KOŞUSUNUN BULDUĞU İKİ HATA — KAYNAKTA DÜZELTİLDİ ⭑

Bu kitap daha önce gerçek Previewer'da açıldı ve iki hata bildirdi:

```
Insufficient gutter. Books with 156 pages require at least 0.5" (12.700mm)
for the gutter / inside margin and at least 0.25" (6.35mm) for the
outside, top and bottom margins.
```
```
This text is outside the margins.        (sayfa 47)
```

İkisi de **gerçekti** ve **kaynakta** düzeltildi — nihai PDF elle
yamalanmadı (K56 · K57). Bugünkü ölçüm:

| ölçü | değer |
|---|---|
| iç kenar (gutter) | **0,5300 in** kullanıldı · KDP asgarisi 0,5000 |
| ölçülen en dar iç kenar | **0,5067 in** |
| ölçülen en dar dış / üst / alt | 0,4800 / 0,3000 / 0,3333 in |
| ihlal eden sayfa | **0 / 156** |
| sayfa 47 | iç 0,5267 · dış 0,5000 · üst 0,3733 · alt 0,3333 → **geçiyor** |

Adli döküm: [`KDP_MARGIN_FORENSIC_REPORT.md`](KDP_MARGIN_FORENSIC_REPORT.md)
— 156 satır, sayfa başına dört mesafe ve tek hüküm.

> ⚠ Yerel `qa_margins.py` KDP Previewer'ı **taklit veya simüle etmez**.
> KDP'nin yayımlanmış kurallarını modelleyip basılı dosyayı onlara karşı
> ölçer. **Nihai hüküm yalnızca Previewer'ındır** ve onu yalnızca kurucu
> çalıştırabilir.

### ⑦ Pricing · Territories · Royalty

| Alan | Değer |
|---|---|
| Territories | **All territories (worldwide rights)** |
| Primary Marketplace | Amazon.com |
| Royalty Plan | **60%** |
| List Price (USD) | **14,99 $** |
| Other marketplaces | ⦿ *Set automatically based on US price* |

Ölçülen ekonomi (156 sayfa):

```
baskı maliyeti   1,00 $ + 156 × 0,017 $ = 3,65 $
telif            14,99 × 0,60 − 3,65     = 5,34 $
başabaş ACOS     5,34 / 14,99            = %35,6
```

> Fiyat testi (14,99 $ ↔ 12,99 $) yayından SONRA ve **kurucuya** aittir.

### ⑧ Publish

**KURUCU EYLEMİ.** **Publish Your Paperback Book**.

> ⚠ **Yayından önce fizikî prova (A9) sipariş edilmesi önerilir.**
> `08_OUTPUT/PROOF_HANDOFF.md`

### ⑨ Yayından sonra doğrulanacaklar

**KURUCU EYLEMİ**, 24–72 saat içinde:

- [ ] Ürün sayfası açılıyor, başlık ve alt başlık doğru
- [ ] Kapak küçük resmi net; başlık küçük boyda okunuyor
- [ ] **Look Inside** açıldı ve ilk sayfa **başlık sayfası** (boş değil)
- [ ] Sayfa sayısı **156** görünüyor
- [ ] Yaş bandı **8–12** görünüyor
- [ ] Barkod arka kapağa **Amazon tarafından** basılmış
- [ ] Kategoriler doğru dalda
- [ ] Fiyat 14,99 $

---

## 2 · A+ İçerik — ayrı akış

**KURUCU EYLEMİ.** Kitap yayımlandıktan sonra:

1. KDP → kitabın satırında **⋯** → **Marketing**
2. Marketplace **Amazon.com** → **A+ Content** → **Manage A+ Content**
3. **Start creating A+ content** → **Basic** → dil **English**
4. Modülleri **sırayla** ekle — tam eşleme:
   [`08_OUTPUT/APLUS/APLUS_MODULE_MAP.md`](APLUS/APLUS_MODULE_MAP.md)
5. Her modüle görselini yükle, **başlık** ve **gövde** metnini yapıştır
6. **Preview** → **Submit for approval**
7. Amazon moderasyonu birkaç iş günü sürer
8. Canlı ürün sayfasında görün

> ⚠ **Panel bir A+ belgesindeki modül sayısını sınırlar.** Sınır 11
> görselden azsa modül haritasını yukarıdan aşağıya uygulayın: sıra
> **öncelik sırasıdır**.

> **AJAN AMAZON'A HİÇBİR GÖRSEL YÜKLEMEDİ.**

---

## 3 · Ajanın YAPMADIKLARI — açıkça

```
KDP paneline giriş           ❌ YAPILMADI
Herhangi bir dosya yükleme   ❌ YAPILMADI
Previewer çalıştırma         ❌ YAPILMADI  (Amazon hizmeti)
Fizikî prova siparişi        ❌ YAPILMADI
Yayımlama                    ❌ YAPILMADI
A+ gönderimi                 ❌ YAPILMADI
Fiyat testi                  ❌ YAPILMADI
```

Bu satırların hiçbiri "hazır" ya da "tamamlandı" olarak
raporlanmamıştır ve raporlanmayacaktır.

---

## 4 · Çocuk doğrulaması — DEĞİŞMEDİ

```
GERÇEK ÇOCUK OTURUMU     0
TEST EDİLEN ÇOCUK        0
externalValidation       overridden-zero-sessions    ← 'passed' DEĞİL
```

Hiçbir KDP alanı, hiçbir A+ satırı ve hiçbir kapak cümlesi bu kitabın
çocuklarla test edildiğini iddia **etmez**. Araç hazır:
`01_SOURCE/pilot_tr/interactive_child_test.html`.

---

## 5 · ✅ KAPAK ÇÖZÜNÜRLÜĞÜ — ÇÖZÜLDÜ

Bu bir eksik DEĞİL artık. Kurucu 18 Ağustos 2026'da aynı kompozisyonun
4× super-resolution sürümünü teslim etti ve ölçülerek kabul edildi.

| | ESKİ | **YENİ** |
|---|---:|---:|
| Piksel | 1569 × 1003 | **6276 × 4012** |
| Etkin dpi (tam kapak) | 89,1 | **356,6** |
| Sırt hizalama kırpması sonrası | — | **329.2 dpi** |
| KDP 300 dpi ölçütü | ✗ | **✅ KARŞILANDI** |

Kabul dosya adına göre değil ÖLÇÜME göre verildi: aynı kompozisyon
(PSNR 32,3 dB), saf bicubic tabana göre **4,66× kenar enerjisi**
(gerçek detay), metin/filigran/logo/barkod yok.

Eski dosya silinmedi:
`07_ASSETS/rejected/kdp-cover-option-01.superseded-89dpi.png`

> `covers.py` artık etkin dpi < 300 ise **KIRMIZI yanar**. Düşük
> çözünürlüklü bir sanat geri konursa kapak sessizce basılmaz.

⚠ İç blok görselleri hâlâ 150 dpi'dır (K39 · kurucu kararı) — bu ayrı
bir kalemdir ve bu turda değişmedi.
