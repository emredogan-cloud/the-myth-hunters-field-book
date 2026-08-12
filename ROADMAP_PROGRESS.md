# ROADMAP PROGRESS — The Myth Hunter's Field Book

<!-- Faz 1'den itibaren 04_BUILD/update_docs.py tarafından ÜRETİLİR -->

> Kapı: `phase0` · Son güncelleme: **12 Ağustos 2026**
>
> Bu dosya şu an **elle yazılmış bootstrap iskeletidir**. Faz 1'de
> `update_docs.py` devreye girer ve buradaki her sayı **ölçülmüş** olur.

---

## Faz durumu

| Faz | Ad | Durum | Kapı | Dal | Etiket |
|---|---|---|---|---|---|
| **0** | Bootstrap | ✅ **TAMAM** | `phase0` | `main` | — |
| **1** | Devralma mimarisi, taksonomi, yaş çerçevesi | ⏸ **BAŞLAMADI** | `phase1` | `faz/1-devralma` | v0.1.0 |
| **2** | Pilot: bir bölge + çocuk saha testi | ⏸ beklemede | `phase2` | `faz/2-pilot` | v0.2.0 |
| **3** | Bölge bloğu I — üç bölge | ⏸ beklemede | `phase3` | `faz/3-blok-1` | v0.3.0 |
| **4** | Bölge bloğu II + final görev | ⏸ beklemede | `phase4` | `faz/4-blok-2` | v0.4.0 |
| **5** | Editoryal yakınsama + sayfa tasarımı | ⏸ beklemede | `phase5` | `faz/5-yakinsama` | v0.5.0 |
| **6** | Nihai üretim + KDP paketi | ⏸ beklemede | `release` | `faz/6-uretim` | v1.0.0 |

---

## Faz 0 · Bootstrap — tamamlanan

- [x] Dizin yapısı (24 dizin)
- [x] `project_config.json` — tek doğruluk kaynağı
- [x] Altı fazlık uygulama yol haritası
- [x] `PROJECT_CONTEXT.md` · `BRIEF.md` · `DECISIONS.md` · `CHANGELOG.md`
- [x] `00_CONTEXT/`: STYLE · SOURCING_STANDARD · **AGE_POLICY** · **INHERITANCE_ARCHITECTURE** · LESSONS_FROM_CODEX
- [x] `01_SOURCE/activity.schema.json` — veri şeması
- [x] Test altyapısı: `validate_spec.py` · **`validate_inheritance.py`** · `validate_structure.py` · `selftest.py`
- [x] `04_BUILD/qa_all.sh` — CI'ın birebir aynısı
- [x] `.github/workflows/validate.yml` — CI iskeleti
- [x] `.gitignore` + iki hatlı manuscript koruması
- [x] `.gate` = `phase0`
- [x] Git deposu ve `main` dalı

---

## Ölçülen ilerleme

| | Ölçülen | Hedef |
|---|---:|---:|
| Aday aktivite | **0** | ≥160 |
| Kilitli aktivite | **0** | 120 |
| Yazılmış aktivite | **0** | 120 |
| Devralınan kayıt | **0** | Faz 1'de belirlenir |
| Kültür | **0** | 22 |
| Görsel öğe | **0** | ~150 |
| Kelime | **0** | ~22.000 |

---

## Sonraki izinli eylem

> ⛔ **FAZ 1 BAŞLAMADI ve kurucu onayı olmadan başlamaz.**
>
> Onay geldiğinde ilk üç iş:
> 1. `faz/1-devralma` dalını aç
> 2. A1 (manuscript politikası) ve A2 (devralma politikası) kararlarını kapat
> 3. `IMPORT_MANIFEST.json`'u üret — devralma **ilk** iştir, envanter ondan türer
