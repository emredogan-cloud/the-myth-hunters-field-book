# A+ İÇERİK ÜRETİM HATTI — şartname · **HENÜZ ÇALIŞTIRILMADI**

> **The Myth Hunter's Field Book** · 16 Ağustos 2026 · Aşama **1 · BEKLEME**
>
> Bu belge A+ varlıklarının **nasıl kurulacağını** yazar. Hiçbiri
> kurulmadı: ham görsel teslim edilmedi ve hat kurucu **DEVAM** diyene
> kadar çalıştırılmaz.
>
> Promptlar: [`../07_ASSETS/IMAGE_PROMPT_LIBRARY.html § 9.3`](../07_ASSETS/IMAGE_PROMPT_LIBRARY.html)

---

## 0 · Çıktı

```
08_OUTPUT/APLUS/                nihai görseller (< 3 MB her biri)
03_APLUS/APLUS_COPY_DECK.md     modül metinleri — Aşama 2'de yazılır
06_REPORTS/aplus.json           ölçüm çıktısı
```

⚠ **Görsel `08_OUTPUT/` altına gider, depoya girmez** (`.gitignore § ⑤`).
`03_APLUS/` altında yalnızca **ölçüm ve metin** durur — K18'in kuralı:
*rapor depoda durur, ürün durmaz.*

---

## 1 · ⭑ EN ÖNEMLİ KURAL: METİN GÖRSELE GÖMÜLMEZ ⭑

Amazon *Image & Text Overlay* modüllerinde arka plan görseline metin
eklenmemesini açıkça tavsiye ediyor. Metin modülün **kendi alanına**
girer.

```
GÖRSEL   →  sahne · ışık · kompozisyon · BOŞ metin alanı
AMAZON   →  başlık · gövde · madde işareti
```

Üç gerekçe, üçü de ticari:

| # | Gerekçe |
|---|---|
| ① | Gömülü metin **düzeltilemez** — kopya değişirse görsel yeniden üretilir |
| ② | Gömülü metin **ölçeklenmez** — mobilde okunmaz, Amazon küçültür |
| ③ | Gömülü metin **çevrilmez** — başka pazara açılırsa hepsi yeniden çizilir |

---

## 2 · Modül seti — 7 modül · 12 görsel

| # | Modül | Amaç | Görsel | Ölçü | Metin-güvenli alan |
|---|---|---|---:|---|---|
| 01 | Standard Image & Text Overlay | HERO / kitap fikri | 1 | 1940 × 600 | **sol %45** |
| 02 | Standard Three Image & Text | çocuk ne yapıyor | 3 | 600 × 600 | alt %15 |
| 03 | Standard Image Header with Text | altı bölge | 1 | 1940 × 600 | **üst %30** |
| 04 | Standard Single Image & Sidebar | gerçek kültürler / araştırma | 1 | 600 × 600 | **sağ %35** |
| 05 | Standard Four Image & Text | ekransız deneyim | 4 | 600 × 600 | alt %15 |
| 06 | Standard Single Left Image | harita · kod · gözlem | 1 | 600 × 600 | **sağ kenar** |
| 07 | Standard Image & Text Overlay | bitirme / saha yolculuğu | 1 | 1940 × 600 | **sağ %45** |

- **Banner:** kabul edilen asgari görsel alan **970 × 300 px**; teslim
  **1940 × 600 px** — 2× kaynak, yeniden örnekleme payı bırakır.
- **Kare:** teslim **600 × 600 px**.
- Nihai dosya **< 3 MB**.

> ⚠ **Panel modül sayısını sınırlar.** Kurucu KDP A+ İçerik
> Yöneticisi'ndeki güncel sınırı görür ve bu setten **yukarıdan aşağıya**
> seçer. Sıra öncelik sırasıdır: **01 · 03 · 05** en yüksek ticari
> sinyali taşır (vaat · kapsam · satın alma gerekçesi).

---

## 3 · Hat — sekiz adım

```
① ENVANTER   teslim edileni ÖLÇ (ad · px · oran · renk · profil · boyut)
② DOĞRULA    metin var mı · logo · filigran · SIZINTI  → varsa RET
③ KIRP       modül oranına — merkezden değil, KOMPOZİSYONDAN
④ ÖLÇEKLE    modül hedefine · gerçek yeniden örnekleme
⑤ SIKIŞTIR   < 3 MB · kaliteyi ölç, tahmin etme
⑥ EŞLE       görsel → modül → yuva (sıra numarasıyla)
⑦ KOPYA      modül metnini AYRI hazırla (görsele girmez)
⑧ PAKET      08_OUTPUT/APLUS/ + aplus.json + kopya destesi
```

---

## 4 · Adım ② — RET koşulları

| Ret | Neden |
|---|---|
| Görselde **herhangi bir metin** | § 1 · metin modülde |
| Logo · filigran · imza | marka ihlali · Amazon reddi |
| **Bir bulmaca cevabı** | § 5 |
| **Çözülmüş** bir sayfa | § 5 |
| **Mühür harfi / yıldız sözcüğü** | § 5 |
| Tanınabilir çocuk yüzü | çocuk gizliliği · yalnızca eller |
| Ekran (telefon · tablet · TV) | *screen-free* konumlandırmasını yalanlar |
| Ürün iddiası (ödül · onay · sayı) | doğrulanamayan iddia |

---

## 5 · ⭑ SIZINTI: A+ GÖRSELİ MANUSCRIPT'TEN DAHA AÇIKTIR ⭑

> ### Ürün sayfası herkese açıktır. A+ görselinde sızdırılan bir cevap, kitabın içindekinden DAHA GENİŞ yayılır.

Manuscript `.gitignore` ile korunur, cevap anahtarı depoya girmez,
prompt kütüphanesinin dolu hâli yereldedir. **A+ görseli ise Amazon'da
herkese açıktır ve indekslenir.**

Bu yüzden A+ sızıntı denetimi iç bloğunkinden **daha sıkıdır**:

- hiçbir hücre dolu çizilmez
- hiçbir kart numaralanmış görünmez
- hiçbir mühür harfli basılmaz
- hiçbir yazma satırı doldurulmuş görünmez
- hiçbir gerçek aktivite sayfası **birebir** gösterilmez

> İki örnek sayfa göstermek yol haritasının ticari planında var
> (Faz 6 § 18) — ama **gösterilen sayfa ÇÖZÜLMEMİŞ olmalıdır.**

---

## 6 · Adım ⑦ — kopya destesi

`03_APLUS/APLUS_COPY_DECK.md` Aşama 2'de yazılır ve her modül için:

| Alan | Kural |
|---|---|
| Başlık | modül sınırına sığar · **iddia doğrulanabilir** |
| Gövde | ölçülmüş sayı kullanır: **120 aktivite · 22 kültür · 6 bölge · 160 sayfa** |
| Yaş | **8–12** · `metadata.json § audience` ile aynı |
| Ton | `00_CONTEXT/STYLE.md` |

> ⚠ **`120 puzzles` doğru, `120 pages` YANLIŞ.** Faz 6 metadata'sı bu
> hatayı yapmıştı; `metadata.py § ⑤` artık mekanik olarak yakalıyor.
> A+ kopyası aynı ölçümden okur ve aynı kapıdan geçer.

Kopya **hiçbir yerde** şunu iddia edemez: ödül, onay, *bestseller*,
eğitim kurumu tavsiyesi, **çocuk testi**.

> ### ⛔ "Çocuklarla test edildi" YAZILAMAZ.
>
> `externalValidation = overridden-zero-sessions`. **Sıfır oturum, sıfır
> testçi.** Bir pazarlama metninde bunun aksini söylemek, kayıtla
> çelişen bir iddiadır ve bu proje o iddiayı yasaklar.

---

## 7 · Yazılacak araç

```
04_BUILD/aplus.py               hat + --check
06_REPORTS/aplus.json           ölçüm çıktısı
03_APLUS/APLUS_COPY_DECK.md     modül metinleri
```

Yol haritası Faz 6 § 8 `aplus.py --check`'i zaten şart koşuyordu; araç
**Aşama 2'de** doğar.

---

> ## HAT KURULMADI. AJAN DURDU.
>
> ```
> PROMPT      ✅ IMAGE_PROMPT_LIBRARY § 9.3 · 7 modül · 12 görsel
> HAM GÖRSEL  ⛔ KURUCUYA AİT — teslim edilmedi
> aplus.py    ⛔ Aşama 2'de yazılacak
> KOPYA       ⛔ Aşama 2'de yazılacak
> A+ PAKETİ   ⛔ ÜRETİLMEDİ
> ```
>
> **A+ paneline dokunulmadı.**
