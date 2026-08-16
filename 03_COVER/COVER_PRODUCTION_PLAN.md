# KAPAK ÜRETİM HATTI — şartname · **HENÜZ ÇALIŞTIRILMADI**

> **The Myth Hunter's Field Book** · 16 Ağustos 2026 · Aşama **1 · BEKLEME**
>
> Bu belge kapağın **nasıl kurulacağını** yazar. Kapak **kurulmadı**:
> ham sanat teslim edilmedi ve hat kurucu **DEVAM** diyene kadar
> çalıştırılmaz.
>
> Geometri: [`COVER_SPEC.md`](COVER_SPEC.md) — **üretilir, elle yazılmaz.**
> Promptlar: [`../07_ASSETS/IMAGE_PROMPT_LIBRARY.html § 9.2`](../07_ASSETS/IMAGE_PROMPT_LIBRARY.html)

---

## 0 · Tek çıktı

```
08_OUTPUT/PAPERBACK/cover.pdf
```

**TEK PDF** · içinde soldan sağa: **ARKA + SIRT + ÖN** · 0,125 in bleed
· düzleştirilmiş · yazı tipleri gömülü.

KDP ciltsiz kapağı bu biçimde ister ve şablon/hesaplayıcıdan türetilmiş
ölçüyü şart koşar.

---

## 1 · ⛔ SIRT GENİŞLİĞİ BU BELGEDE YOKTUR — VE BU BİLİNÇLİDİR

Sırt `metadata.py` tarafından **sayfa sayısından türetilir** ve
`COVER_SPEC.md`'ye yazılır. Burada ikinci bir kopya tutmak, ikisinin bir
gün ayrışması demektir — ve ayrıştığı gün kapak **yanlış sırtla basılır.**

```
sayfa sayısı  →  metadata.py  →  COVER_SPEC.md  →  covers.py
                                                    ↑
                                        hat sırtı BURADAN okur
```

> ### Elle yazılmış bir sırt, bir sonraki dizgide bayatlayan bir sırttır.

⚠ **Sayfa sayısı Aşama 2'de yeniden ölçülecek.** İki yer tutucu
değişince ve editoryal düzeltmeler girince iç blok yeniden dizilir.
Sayfa sayısı 160'ta kalmayabilir. Hat bu yüzden **kapağı iç bloktan
SONRA** kurar ve sırtı **o günkü ölçümden** alır.

---

## 2 · Hat — on adım

```
① ENVANTER      teslim edilen ham dosyayı ÖLÇ (ad · px · renk · profil · alfa)
② DOĞRULA       metin var mı · logo var mı · filigran var mı  → varsa RET
③ GEOMETRİ      COVER_SPEC.md'yi OKU (sırtı hesaplama, OKU)
④ KIRP          panel panel: arka · sırt · ön
⑤ ÖLÇEKLE       300 dpi tuvale — gerçek piksel, etiket değil
⑥ RENK          sRGB normalize · profil göm · alfa düzleştir
⑦ TİPOGRAFİ     ön · sırt · arka metni VEKTÖR olarak bas
⑧ GÜVENLİ ALAN  taşma · sırt toleransı · barkod kutusu ölç
⑨ DÜZLEŞTİR     tek katman · yazı tipi göm · şeffaflık yok
⑩ PDF           tek dosya · piksel denetimi · rapor
```

Her adım kendi ölçümünü `06_REPORTS/cover.json` içine yazar. **Rapora
girmeyen adım koşmamış sayılır.**

---

## 3 · Adım ② — RET koşulları

Ham sanat şunlardan **birini** taşıyorsa hat durur ve dosyayı
`07_ASSETS/rejected/` altına koyar:

| Ret | Neden |
|---|---|
| Görselde **herhangi bir harf** | tipografi CLI'ın işi · gömülü metin düzeltilemez |
| Logo · filigran · imza | KDP reddeder · marka ihlali riski |
| Gömülü ISBN veya barkod | KDP kendi barkodunu basar |
| Şeffaflık kanalı | baskıda öngörülemez |
| CMYK profili | KDP ciltsiz kapak için sRGB bekler |
| Sahte yazı sistemi / uydurma glif | kültürel yanlışlık |

> **Tespit ölçümledir, güvenle değil.** OCR taraması + kenar/kontrast
> analizi koşar; sonuç raporda sayı olarak durur.

---

## 4 · Adım ⑤ — 300 dpi: **gerçek piksel, etiket değil**

| Durum | Hat ne yapar |
|---|---|
| Ham ≥ hedef piksel | **hiçbir şey** — birebir yerleştirir |
| Ham < hedef piksel | gerçek yeniden örnekleme + **kaynak dpi'ı rapora yazar** |
| Ham çok küçük (< %60) | **RET** — kurucudan daha büyük kaynak ister |

```
⛔ YASAK: pikseli değiştirmeden DPI etiketini 300 yapmak.
   Bir etiket çözünürlük değildir ve hat bunu yapmaz.
```

Nihai rapor her panel için **gerçek kaynak dpi**'ı ayrı satırda yazar.
Hedefin altında kalan varsa **istisna olarak açıkça** durur —
gizlenmez, yuvarlanmaz.

---

## 5 · Adım ⑦ — tipografi

### 5.1 · Ne basılacak

| Panel | İçerik | Kaynak |
|---|---|---|
| **ÖN** | `THE MYTH HUNTER'S FIELD BOOK` | `metadata.json § title` |
| **ÖN** | alt başlık | `metadata.json § subtitle` |
| **ÖN** | `EMRE DOĞAN` | `metadata.json § author` |
| **SIRT** | başlık + yazar | aynı |
| **ARKA** | tanıtım metni | `metadata.json § description` |
| **ARKA** | yaş bandı **8–12** | `metadata.json § audience` |
| **ARKA** | *screen-free* · *120 puzzles · 22 cultures* | `metadata.json` |
| **ARKA** | yazar biyografisi | `metadata.json § authorBio` |
| **ARKA** | barkod alanı — **BOŞ** | KDP basar |

> ### Kapak metni metadata'dan OKUNUR, elle yazılmaz.
>
> KDP paneline girilen başlık ile kapakta basılı başlık **harfi harfine**
> aynı olmak zorundadır. İkisini iki ayrı yerde tutmak, bir gün
> ayrışmaları demektir. Hat tek kaynaktan okur ve **eşleşmeyi denetler**.

⚠ **`120 puzzles` doğru, `120 pages` YANLIŞ.** İkisi ayrı büyüklüktür:
**120 aktivite**, **160 sayfa**. `metadata.py § ⑤` bu karışmayı artık
mekanik olarak yakalıyor.

### 5.2 · Kural

- **Vektör metin** — rasterleştirilmiş metin yasak
- **Yazı tipi gömülü** — `07_ASSETS/fonts/`
- Bütün metin **güvenli alanın** (0,25 in) içinde
- Sırt metni sırt kenarlarından **0,0625 in** içeride

### 5.3 · ⚠ Sırt bandı çok dar — ölçülmüş kısıt

```
sırt genişliği            0,3603 in
KDP sırt toleransı        2 × 0,0625 = 0,1250 in
kullanılabilir bant       0,2353 in  ≈  16,9 pt
```

Sırt puntosu bu bandın **altında** kalmalı. Hat ölçer; taşarsa
**kırmızı yakar** ve puntoyu sessizce küçültmez — sessiz küçültme,
okunmayan bir sırt demektir.

---

## 6 · Adım ⑧ — barkod kutusu

KDP arka kapağın alt bölgesinde barkod için bir alan ayırır ve kendi
barkodunu oraya basar. Kural:

- alan **boş** bırakılır — açık, düz, deseni bozmayan bir zemin
- oraya **hiçbir metin, hiçbir odak nesne** girmez
- kurucu **sahte barkod basmaz**

> ### ⭑ KUTUNUN KOORDİNATI ELLE YAZILMAZ ⭑
>
> Kesin konum ve ölçü **KDP kapak şablonundan** okunur: kurucu nihai
> sayfa sayısıyla şablonu indirir, hat kutuyu **şablon PDF'inden**
> çıkarır. Bu belgeye yazılmış bir koordinat, şablon değişince
> bayatlar — ve bayat bir barkod kutusu kapağı reddettirir.

---

## 7 · Adım ⑩ — çıktıdan önce denetlenecekler

| Denetim | Ölçüt |
|---|---|
| Tek PDF · tek sayfa | evet |
| Sayfa ölçüsü | `COVER_SPEC` ile birebir |
| Bleed | 0,125 in · dört kenar |
| Sırt konumu | tuvalin ortası ± 1 px |
| Panel toplamı | arka + sırt + ön = tam en |
| Yazı tipleri | **hepsi gömülü** |
| Şeffaflık | yok |
| Katman · yorum · ek açıklama | yok |
| Kırpma işareti | yok |
| Güvenli alan taşması | 0 |
| Sırt metni tolerans dışı | 0 |
| Barkod alanı | boş ve açık |
| Yer tutucu / şablon çizgisi | **yok** |
| Başlık ⇄ metadata | birebir aynı |
| Yazar ⇄ metadata | birebir aynı |
| Etkin çözünürlük | her panel için **rapora yazılı** |

Denetim **piksel incelemesiyle** biter: hat PDF'i raster'a çevirir ve
metnin gerçekten güvenli alanın içinde durduğunu **görüntüden** ölçer.
Koordinat hesabı yeterli değildir — bir hesap doğru, bir yerleşim yanlış
olabilir.

---

## 8 · Yazılacak araç

```
04_BUILD/covers.py              hat + --check
06_REPORTS/cover.json           ölçüm çıktısı
06_REPORTS/tracked/cover-qa.md  insan okunur özet
```

Yol haritası Faz 6 § 8 `covers.py --check`'i zaten şart koşuyordu; araç
**Aşama 2'de** doğar. Bu belge onun sözleşmesidir.

---

> ## HAT KURULMADI. AJAN DURDU.
>
> ```
> GEOMETRİ     ✅ COVER_SPEC.md · 160 sayfadan türetildi
> PROMPT       ✅ IMAGE_PROMPT_LIBRARY § 9.2 · iki seçenek
> HAM SANAT    ⛔ KURUCUYA AİT — teslim edilmedi
> covers.py    ⛔ Aşama 2'de yazılacak
> cover.pdf    ⛔ ÜRETİLMEDİ
> ```
>
> Kapak, **iç blok yeniden dizildikten sonra** kurulur: sırt o günkü
> sayfa sayısından gelir.
