# ÇOCUK SAHA TESTİ KAYDI

> Protokol: [`CHILD_TEST_PROTOCOL.md`](CHILD_TEST_PROTOCOL.md) · karar **A7**

---

## DURUM · 13 Ağustos 2026

| | |
|---|---|
| Yapılan oturum | **0** |
| Testçi | **0** |
| Test edilen sayfa | **0** |
| Yardımsız anlaşılma oranı | **ÖLÇÜLMEDİ** |
| Faz 2 çocuk kapısı | ⏳ **DIŞ DOĞRULAMA BEKLİYOR** |

### Bu tablo neden boş

Kurucu henüz çocuk testçi sağlamadı (karar **A7**, açık). Ajan çocukla
test yapamaz ve **sahte kayıt üretmez**.

Boş bir tablo bir eksiklik değil, bir **beyandır**: bu satırların altında
uydurulmuş bir oturum yok.

> Aşağıdaki tablo, gerçek bir oturum yapıldığında ve **yalnızca o zaman**
> dolar.

---

## Oturumlar

| # | Tarih | Testçi | Yaş | Sayfa | Yardımsız | Sonuç | İpucu | Not |
|---|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — | *kayıt yok* |

---

## Sayfa bazında özet

| activityId | Deneme | Yardımsız anlaşıldı | Takılma noktası |
|---|---:|---:|---|
| *16 pilot sayfasının hiçbiri henüz test edilmedi* | 0 | — | — |

---

## Ölçüt hatırlatması

| Yardımsız anlaşılma | Sonuç |
|---|---|
| ≥ %80 | PASS |
| %60–80 | talimat dili yeniden yazılır |
| < %60 | **şablon bozuk — ŞABLONU DÜZELT** |

---

## Mahremiyet

Bu dosyaya **yalnızca** anonim kimlik (`tester-01`), yaş ve sonuç girer.
Gerçek ad, okul, adres, doğum tarihi, fotoğraf veya ses **hiçbir koşulda**
girmez.

`validate_structure.py § check_child_privacy` `tester` alanını
`tester-\d{2}` biçimine karşı **mekanik olarak** denetler ve uymayan bir
değer CI'ı kırmızı yakar.

Ham oturum kayıtları `03_EDITORIAL/child_tests_raw/` altında durur ve o
dizin `.gitignore § ①c` ile depodan dışlanmıştır.
