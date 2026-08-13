# ÇOCUK SAHA TESTİ KAYDI

> Protokol: [`CHILD_TEST_PROTOCOL.md`](CHILD_TEST_PROTOCOL.md) · karar **A7**

---

## DURUM · 13 Ağustos 2026

| | |
|---|---|
| Testçi | ✅ **2** — kurucu onayladı (**A7 → K26**) |
| Türkçe materyal | ✅ **üretildi** · 16 sayfa · `01_SOURCE/pilot_tr/` |
| **Yapılan oturum** | **0** |
| Test edilen sayfa | **0** |
| Yardımsız anlaşılma oranı | **ÖLÇÜLMEDİ** |
| Faz 2 çocuk kapısı | ⏳ **DIŞ DOĞRULAMA BEKLİYOR** |

### Bu tablo neden hâlâ boş

Testçiler bulundu ve materyal hazır. **Oturum henüz yapılmadı.**

> ### PAKET ÜRETMEK, TEST YAPMAK DEĞİLDİR.

Ajan çocukla test yapamaz ve **sahte kayıt üretmez**. Boş bir tablo bir
eksiklik değil, bir **beyandır**: bu satırların altında uydurulmuş bir
oturum yok.

`qa_language § ⑤` bunu her koşuda hatırlatıyor: testçi onaylı ve materyal
üretilmiş ama oturum yoksa kapı uyarı basıyor.

> Aşağıdaki tablo, gerçek bir oturum yapıldığında ve **yalnızca o zaman**
> dolar.

---

## Oturum nasıl koşturulur

```
① Veli 01_SOURCE/pilot_tr/tester-pack-tr.txt paketinin ilk sayfasını okur
② Çocuğa YALNIZCA şu söylenir:
     "Bu bir saha defteri. Sayfada ne yazıyorsa onu yap."
③ En çok dört sayfa · 20–30 dakika
④ Gözlemci SUSAR ve yalnızca not alır
⑤ Oturum sonu üç soru (PROTOKOL § 5)
⑥ Ham kayıt 03_EDITORIAL/child_tests_raw/ altına (depo dışı)
⑦ Anonim özet AŞAĞIDAKİ tabloya
⑧ project_config § externalValidation güncellenir
```

**Türkçe pilotun mühür sözcüğü `KATMAN`'dır** (ticari `CONDOR` değil —
gerekçe `DECISIONS.md § K26`). Değerlendiren kişi anahtarı
`01_SOURCE/pilot_tr/source-tr.json § sealKeyTest` içinde bulur ve
**testçiye vermez**.

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
