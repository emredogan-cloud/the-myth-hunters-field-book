# A+ İÇERİK MODÜL HARİTASI — The Myth Hunter's Field Book

<!-- ÜRETİLMİŞTİR — 04_BUILD/aplus.py · ELLE DÜZENLEMEYİN -->

> Kurucu bu belgeyi KDP **Marketing → A+ Content Manager** ekranında modül modül uygular.
> Görseller `08_OUTPUT/APLUS/` altındadır ve **yüklenmedi**.

```
MODÜL  →  GÖRSEL  →  BAŞLIK  →  GÖVDE
```

## ⭑ METİN GÖRSELE GÖMÜLÜ DEĞİLDİR — VE BU BİLİNÇLİ BİR AYRIMDIR ⭑

Aşağıdaki bütün metinler Amazon'un **kendi modül alanlarına** girilir. Arka plan görselleri metinsizdir ve öyle kalmalıdır: gömülü metin düzeltilemez, mobilde ölçeklenmez ve dil değişirse yeniden çizim ister.

> ### ⚠ KARDEŞ KİTAPTAN FARKLI — ALANLARI BOŞ BIRAKMAYIN
>
> *The Great Book of World Myths* A+ metinlerini **görselin içine** bastı ve playbook'u modül alanlarını **boş bırakmayı** söyler. Gerekçesi oydu: o projede görsel üreteci kapakta kitabın adını **yanlış yazmıştı**, bu yüzden bütün tipografi görsele deterministik olarak basıldı.
>
> **O gerekçe bu kitapta YOKTUR.** Buradaki metinler de üreteçten gelmiyor: `metadata.json` ölçümlerinden türetiliyor ve Amazon onları kendi alanlarında **duyarlı** olarak basıyor.
>
> Amazon, *Image & Text Overlay* modüllerinde arka plan görseline metin eklenmemesini zaten tavsiye ediyor.
>
> **Bu kitapta modül alanları DOLDURULUR.** İki kitabın sözleşmesi birbirinin tersidir; kardeş kitabın alışkanlığıyla burada alanları boş bırakmak, ürün sayfasını **metinsiz** bırakır.

## ⚠ BU METİNLERİN İDDİA ETMEDİĞİ ŞEYLER

- ödül · onay · *bestseller* · eğitim kurumu tavsiyesi
- **çocuk testi** — `externalValidation = overridden-zero-sessions`; sıfır oturum, sıfır testçi. Hiçbir A+ satırı bunun aksini söylemez.
- bir bulmaca cevabı, çözülmüş bir sayfa veya bir mühür harfi

---

## 1 · HERO — kitabın ne olduğu tek bakışta

| | |
|---|---|
| **Modül tipi** | `Standard Image & Text Overlay` |
| **Görsel sayısı** | 1 |
| **Modül kimliği** | `aplus-01-hero` |

**MODÜL BAŞLIĞI** — Amazon'daki *headline* alanına:

> Not a puzzle book with a mythology theme

**MODÜL GÖVDESİ** — Amazon'daki *body text* alanına:

> Every puzzle is built out of what a people actually made: a writing system, a counting system, a map of a real place, a message that had to travel. 120 puzzles across 22 cultures.

### Görsel

| | |
|---|---|
| Dosya | `aplus-01-hero.jpg` |
| Ölçü | 1940 × 600 px |
| Boyut | 0.41 MB (JPEG q95) |
| sha256 | `e47666a738f322a3515ef4a7d2396219` |

**Alt text** — *zorunlu · erişilebilirlik*:

> A closed navy field notebook with a gold compass emblem lying on a wooden desk beside a folded map, a pencil and a coil of rope.

---

## 2 · ÇOCUK NE YAPIYOR — çöz · diz · mühürle

| | |
|---|---|
| **Modül tipi** | `Standard Three Image & Text` |
| **Görsel sayısı** | 3 |
| **Modül kimliği** | `aplus-02-what-children-do` |

**MODÜL BAŞLIĞI** — Amazon'daki *headline* alanına:

> Work it out. Write it down. Earn the seal.

**MODÜL GÖVDESİ** — Amazon'daki *body text* alanına:

> Children decode, sort and draw their way through the book — then press a seal at the end of every region.

### Görseller ve KENDİ metin alanları

> ⚠ Bu modül **3 ayrı görsel yuvası** taşır ve her yuvanın KENDİ başlığı ve gövdesi vardır. Modül başlığı yalnızca **bir kez** girilir; aşağıdakiler yuvaların içine girer.

#### Yuva 1 — `aplus-02-what-children-do-01.jpg`

| | |
|---|---|
| Ölçü | 600 × 600 px |
| Boyut | 0.12 MB (JPEG q95) |
| sha256 | `ba161000acf178981cc5f201a2f0770d` |

**Alt text** — *zorunlu · erişilebilirlik*:

> A child's hands writing with a pencil on the ruled page of an open field notebook.

**Yuva başlığı:**

> Decode and write

**Yuva gövdesi:**

> A key is printed on the page and a line is ruled beneath it. Every answer comes from the plate — never from something a child is expected to already know.

#### Yuva 2 — `aplus-02-what-children-do-02.jpg`

| | |
|---|---|
| Ölçü | 600 × 600 px |
| Boyut | 0.12 MB (JPEG q95) |
| sha256 | `70fba9716e4ee93e771d1f08af407aef` |

**Alt text** — *zorunlu · erişilebilirlik*:

> A child's hands arranging blank paper cards in a row on a wooden desk.

**Yuva başlığı:**

> Sort the evidence

**Yuva gövdesi:**

> Cards arrive out of order with empty number boxes. The reader puts an account back the way it happened, then checks it against the page itself.

#### Yuva 3 — `aplus-02-what-children-do-03.jpg`

| | |
|---|---|
| Ölçü | 600 × 600 px |
| Boyut | 0.13 MB (JPEG q95) |
| sha256 | `013fef5bda4b5de3e40eb6efd2d715e5` |

**Alt text** — *zorunlu · erişilebilirlik*:

> A child's hand pressing a stamp beside a row of round seal impressions on a paper strip.

**Yuva başlığı:**

> Earn the seal

**Yuva gövdesi:**

> Six regions, six seals. The star box on each page collects one letter at a time until a region's seal word is complete.

---

## 3 · KAPSAM — altı bölge, yirmi iki halk

| | |
|---|---|
| **Modül tipi** | `Standard Image Header with Text` |
| **Görsel sayısı** | 1 |
| **Modül kimliği** | `aplus-03-six-regions` |

**MODÜL BAŞLIĞI** — Amazon'daki *headline* alanına:

> Six regions. 22 peoples. One quest.

**MODÜL GÖVDESİ** — Amazon'daki *body text* alanına:

> From sea ice to cloud forest, the route crosses six regions and 22 cultures — each named by its own name.

### Görsel

| | |
|---|---|
| Dosya | `aplus-03-six-regions.jpg` |
| Ölçü | 1940 × 600 px |
| Boyut | 0.45 MB (JPEG q95) |
| sha256 | `7b297bdd8d787a476e6ae5317cf2633f` |

**Alt text** — *zorunlu · erişilebilirlik*:

> Six painted landscape panels in a row: sea ice, a warm coastal town, open savanna, monsoon mountains, an island sea and cloud forest terraces.

---

## 4 · GÜVENİLİRLİK — cevaplar kaynaklarla denetlendi

| | |
|---|---|
| **Modül tipi** | `Standard Single Image & Sidebar` |
| **Görsel sayısı** | 1 |
| **Modül kimliği** | `aplus-04-real-cultures` |

**MODÜL BAŞLIĞI** — Amazon'daki *headline* alanına:

> Checked against museums, archives and universities

**MODÜL GÖVDESİ** — Amazon'daki *body text* alanına:

> Every cultural claim in the book was revalidated against primary and institutional sources, and the back of the book says which ones.

### Görsel

| | |
|---|---|
| Dosya | `aplus-04-real-cultures.jpg` |
| Ölçü | 600 × 600 px |
| Boyut | 0.14 MB (JPEG q95) |
| sha256 | `744f0b65829c37b26e55fbdc30a8d994` |

**Alt text** — *zorunlu · erişilebilirlik*:

> A stack of reference books, an archive folder, a magnifier and cotton handling gloves on a desk.

---

## 5 · SATIN ALMA GEREKÇESİ — masa başı, ekransız

| | |
|---|---|
| **Modül tipi** | `Standard Three Image & Text` |
| **Görsel sayısı** | 3 |
| **Modül kimliği** | `aplus-05-screen-free` |

**MODÜL BAŞLIĞI** — Amazon'daki *headline* alanına:

> A pencil. That is the whole kit.

**MODÜL GÖVDESİ** — Amazon'daki *body text* alanına:

> No screen, no app, no batteries. 156 pages a child writes in, at a table, with a pencil.

### Görseller ve KENDİ metin alanları

> ⚠ Bu modül **3 ayrı görsel yuvası** taşır ve her yuvanın KENDİ başlığı ve gövdesi vardır. Modül başlığı yalnızca **bir kez** girilir; aşağıdakiler yuvaların içine girer.

#### Yuva 1 — `aplus-05-screen-free-01.jpg`

| | |
|---|---|
| Ölçü | 600 × 600 px |
| Boyut | 0.14 MB (JPEG q95) |
| sha256 | `9513ce2b8428e414097c34d527577101` |

**Alt text** — *zorunlu · erişilebilirlik*:

> A closed navy field notebook with a gold compass emblem beside a single sharpened pencil.

**Yuva başlığı:**

> Closed and ready

**Yuva gövdesi:**

> One book and one pencil. Nothing to charge, nothing to install and nothing that needs a grown-up's password.

#### Yuva 2 — `aplus-05-screen-free-02.jpg`

| | |
|---|---|
| Ölçü | 600 × 600 px |
| Boyut | 0.12 MB (JPEG q95) |
| sha256 | `feb60ffd770877782177d18bdfd909b3` |

**Alt text** — *zorunlu · erişilebilirlik*:

> An open field notebook showing blank ruled and gridded pages with a pencil resting across them.

**Yuva başlığı:**

> Open and working

**Yuva gövdesi:**

> Ruled writing space on every page, measured against the hand of an eight-year-old rather than an adult's.

#### Yuva 3 — `aplus-05-screen-free-03.jpg`

| | |
|---|---|
| Ölçü | 600 × 600 px |
| Boyut | 0.12 MB (JPEG q95) |
| sha256 | `7e3faa9028812dde2a505713b3d486c7` |

**Alt text** — *zorunlu · erişilebilirlik*:

> The closed field notebook beside a mug and a switched-off desk lamp at the end of a session.

**Yuva başlığı:**

> Finished for today

**Yuva gövdesi:**

> A quest with an ending. When the sixth seal is in, the last page opens and the certificate is filled in.

---

## 6 · AKTİVİTE TÜRLERİ — harita · kod · gözlem · sıralama

| | |
|---|---|
| **Modül tipi** | `Standard Single Left Image` |
| **Görsel sayısı** | 1 |
| **Modül kimliği** | `aplus-06-maps-and-codes` |

**MODÜL BAŞLIĞI** — Amazon'daki *headline* alanına:

> Maps, keys, plates and cards

**MODÜL GÖVDESİ** — Amazon'daki *body text* alanına:

> Four kinds of work, 120 times over: trace a real coast, build a key, label a plate, put an account back in order.

### Görsel

| | |
|---|---|
| Dosya | `aplus-06-maps-and-codes.jpg` |
| Ölçü | 600 × 600 px |
| Boyut | 0.15 MB (JPEG q95) |
| sha256 | `387953e32bf44e75ed484d0e228ac2df` |

**Alt text** — *zorunlu · erişilebilirlik*:

> Four activity sheets fanned across a desk: an outline coast map, a ruled key panel with empty cells, an observation plate and blank numbered cards.

---

## 7 · TAMAMLAMA — bu kitap BİTİRİLİR

| | |
|---|---|
| **Modül tipi** | `Standard Image & Text Overlay` |
| **Görsel sayısı** | 1 |
| **Modül kimliği** | `aplus-07-completion` |

**MODÜL BAŞLIĞI** — Amazon'daki *headline* alanına:

> Six seals, and a certificate at the end

**MODÜL GÖVDESİ** — Amazon'daki *body text* alanına:

> The book is a single quest with an ending. Six regions, six seals, and a final page that only opens when all six are in.

### Görsel

| | |
|---|---|
| Dosya | `aplus-07-completion.jpg` |
| Ölçü | 1940 × 600 px |
| Boyut | 0.36 MB (JPEG q95) |
| sha256 | `5706c237a50efd03a3327928f48b9e98` |

**Alt text** — *zorunlu · erişilebilirlik*:

> The finished field notebook closed on a desk beside a blank certificate card and a folded map.

---

## Kurucuya kalan

1. KDP → kitabın satırında **⋯** → **Marketing**
2. Marketplace **Amazon.com** → **A+ Content** → **Manage A+ Content**
3. **Start creating A+ content** · **Basic** · dil **English**
4. Yukarıdaki modülleri **numara sırasıyla** ekle
5. Her modülün **başlığını** ve **gövdesini** kendi alanına yapıştır
6. Çok görselli modüllerde her **yuvaya** kendi görselini, kendi başlığını ve kendi gövdesini gir
7. **Preview** → **Submit for approval**

> ⚠ **Panel bir A+ belgesindeki modül sayısını sınırlar.** Sınır bu setten azsa modülleri **yukarıdan aşağıya** seçin: sıra öncelik sırasıdır (1 · 3 · 5 en yüksek ticari sinyali taşır).

> **AJAN AMAZON'A HİÇBİR ŞEY YÜKLEMEDİ.**
