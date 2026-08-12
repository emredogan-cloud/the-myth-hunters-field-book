# KAYNAK STANDARDI — The Myth Hunter's Field Book

> Bestiarium ve World Myths'in kaynak disiplininin **aktivite** biçimine
> uyarlanmış hâli. Devralma kuralları için ayrıca bkz.
> [`INHERITANCE_ARCHITECTURE.md`](INHERITANCE_ARCHITECTURE.md).
>
> Sürüm 1.0 · Faz 1'de onaylanır

---

## 1 · Kaynak sayılan

| Tip | Örnek |
|---|---|
| `book` | Akademik mitoloji/folklor monografisi |
| `journal` | Hakemli makale |
| `museum` | Müze envanter kaydı |
| `ethnography` | Saha etnografyası, derleme |
| `archive` | Arşiv belgesi |
| `inherited` | **World Myths'ten devralınan kayıt** — manifest kimliği zorunlu |

## 2 · Kaynak SAYILMAYAN

- Kaynak göstermeyen mitoloji siteleri
- Wiki maddeleri (izleri takip edilebilir, kendisi kaynak değildir)
- Çocuk kitabı yeniden anlatımları (ikincil aktarım)
- Popüler kültür uyarlamaları
- LLM çıktısı — **hiçbir koşulda**

---

## 3 · Doğrulama eşiği kullanıma göre değişir

Bu, projenin en ince kuralıdır:

| Kullanım | Eşik |
|---|---|
| Anlatı arka planı, kültürel çerçeve | 1 kaynak yeterli · `inherited-provisional` olabilir |
| **Bir aktivitenin cevabını üreten iddia** | **≥2 bağımsız kaynak** veya `inherited-verified` |
| Telaffuz | `inherited-verified` **zorunlu** |
| Ad yazımı ve diakritikler | `inherited-verified` **zorunlu** |

Gerekçe: bkz. [`INHERITANCE_ARCHITECTURE.md § 2`](INHERITANCE_ARCHITECTURE.md).

---

## 4 · Kısıt taraması

Her aktivite dört durumdan birini alır. Taranmamış aktivite envantere giremez.

| Durum | Kitapta |
|---|---|
| `open` | ✅ |
| `attributed` | ✅ + kültürel atıf zorunlu |
| `restricted` | ⛔ **çocuk oyununa çevrilemez** |
| `excluded` | ⛔ gerekçe kayıtta kalır |

### Bu kitapta kısıt taraması neden daha sert

Bir yetişkin referans cildinde bir gelenek **anlatılabilir**. Bir çocuk
aktivite kitabında aynı gelenek **yaptırılır** — çizdirilir, çözdürülür,
taklit ettirilir.

> Yaşayan bir topluluğun kutsal anlatısını bir bulmacaya çevirmek,
> onu anlatmaktan **kategorik olarak farklıdır**.

Şüphe `excluded` lehine çözülür. 160 adaylık havuz tam olarak bunun içindir.

---

## 5 · Araştırma → yazım kilidi

```
inherited-provisional  →  LOCKED OLAMAZ  →  YAZILAMAZ
research.verified != true  →  YAZILAMAZ
```

`validate_inheritance.py` ve `validate_spec.py` bunu **iki ayrı kapıdan**
denetler. Tek bir kapının unutulması sistemi açmaz.
