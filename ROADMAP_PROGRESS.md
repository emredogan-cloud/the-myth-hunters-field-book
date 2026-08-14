# ROADMAP PROGRESS — The Myth Hunter's Field Book

<!-- ÜRETİLMİŞTİR — 04_BUILD/update_docs.py · ELLE DÜZENLEMEYİN -->

> Kapı: `phase1`

> ### ⚠ KURUCU FAZ AŞMASI ETKİN — `K27`
>
> Yetkilendirilen faz: **phase4** · kapı tavanı: **`phase1`**
>
> Ertelenen blokaj: **A10** — open-not-performed
>
> Bu aşma bir SIRAYI değiştirir, bir SONUCU üretmez:
> **A10 hâlâ açıktır ve çocuk oturumu YAPILMAMIŞTIR.**
> `.gate` bu yüzden `phase1`'de tutulur.

---

## Faz durumu

| Faz | Ad | Durum | Kapı | Dal | Etiket |
|---|---|---|---|---|---|
| **0** | Bootstrap | ✅ **TAMAM** | `phase0` | `main` | — |
| **1** | Devralma mimarisi, taksonomi, yaş çerçevesi | ✅ **TAMAM** | `phase1` | `faz/1-devralma` | v0.1.0 |
| **2** | Pilot: bir bölge + çocuk saha testi | ⏸ **AŞILDI — kapanmadı (A10)** | `phase2` | `faz/2-pilot` | v0.2.0 |
| **3** | Bölge bloğu I — üç bölge | ⏸ **AŞILDI — kapanmadı (A10)** | `phase3` | `faz/3-blok-1` | v0.3.0 |
| **4** | Bölge bloğu II + final görev | ▶ **AŞMAYLA SÜRÜYOR (K27)** | `phase4` | `faz/4-blok-2` | v0.4.0 |
| **5** | Editoryal yakınsama + sayfa tasarımı | ⏸ beklemede | `phase5` | `faz/5-yakinsama` | v0.5.0 |
| **6** | Nihai üretim + KDP paketi | ⏸ beklemede | `release` | `faz/6-uretim` | v1.0.0 |

---

## Ölçülen ilerleme

| | Ölçülen | Hedef |
|---|---:|---:|
| Aday aktivite | **168** | ≥160 |
| Kilitli aktivite | **84** | 120 |
| Yazılmış aktivite | **84** | 120 |
| Devralınan kayıt | **76** | — |
| Kültür | **22** | 22 |
| Bölge (tanımlı) | **6** | 6 |
| **Bölge (yazılmış)** | **4** | 6 |
| Sayfa basım maddesi (`pagePrints`) | **380** | — |
| Görsel şartnamesi | **84** | ~150 |
| Görsel varlık (üretilmiş) | **0** | ~150 |
| Kelime | **6.464** | ~22.000 |

---

## Sonraki izinli eylem

> **Faz 4 — Bölge bloğu II + final görev** · kurucu aşmasıyla YETKİLİ (K27)
>
> Dal: `faz/4-blok-2` · Etiket: v0.4.0
>
> ⚠ Kapı `phase1`'de kalır. **A10 kapanmadı.**
>
> Bir sonraki fazı kurucu talimatı olmadan **BAŞLATMA**.

