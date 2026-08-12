# DECISIONS — karar kaydı

> İki şey taşır: **alınmış kararlar** (`K##`) ve **AÇIK KARARLAR** (`A#`).
> Bir varsayım sessizce proje gerekliliğine dönüşemez.

---

## AÇIK KARARLAR — kurucudan yanıt bekleyen

Durum tablosu · 12 Ağustos 2026 (bootstrap)

| # | Soru | Aciliyet | Ne zaman kapanmalı | Durum |
|---|---|---|---|---|
| **A1** | Manuscript public depoda mı duracak? | **YÜKSEK** | **Faz 1 başlamadan** | AÇIK (varsayım: hayır) |
| **A2** | **Devralma politikası onayı** | **YÜKSEK** | **Faz 1 başlamadan** | AÇIK |
| **A3** | 6 bölge ve mühür mimarisi | YÜKSEK | Faz 1 sonu | AÇIK |
| **A4** | 120 aktivitenin nihai listesi | YÜKSEK | Faz 1 sonu | AÇIK |
| **A5** | Ciltli hediye sürümü v1.0'a girecek mi | DÜŞÜK | Faz 4 | AÇIK (varsayım: hayır) |
| **A6** | Yazar biyografisi metni | ORTA | Faz 5 | AÇIK |
| **A7** | **≥2 çocuk testçi kim** | **YÜKSEK** | **Faz 2 başlamadan** | AÇIK |

---

### A2 · Devralma politikası — bu projenin en kritik açık kararı

World Myths'ten hangi veriyi, hangi koşulla devralıyoruz?

| Şık | Ne demek | Sonuç |
|---|---|---|
| **(a)** | Kopyala + sha256 kaydet + kullanım tipine göre yeniden doğrula | **Bootstrap bunu varsaydı.** İzolasyon korunur, köken izlenir |
| (b) | Her kaydı sıfırdan yeniden araştır | Projenin maliyet avantajını yok eder |
| (c) | Devralınanı doğrulanmış say | **Tehlikeli** — yanlış bir cevap çocuğu suçlu hissettirir |

**Bootstrap'ın varsayımı: (a).** Gerekçe ve mekanizma:
[`00_CONTEXT/INHERITANCE_ARCHITECTURE.md`](00_CONTEXT/INHERITANCE_ARCHITECTURE.md)

Kurucu (c)'yi seçerse `project_config.json § inheritance.lockRequiresStatus`
değişir — ama `selftest.py § ②(i)` bu gevşetmeyi **yakalar ve CI'ı kırmızı
yakar**. Yani karar bilinçli olmak zorundadır, sessizce olamaz.

### A7 · Çocuk testçiler — Faz 2'nin sert bloklayıcısı

Ajan çocukla test yapamaz. Testçi bulunamazsa **Faz 2 bloklanır**.
Bu kabul edilen bir bloktur: **sahte test kaydı üretilmez.**

Kimlikler anonimdir (`tester-01`) ve gerçek ad depoya **hiçbir koşulda**
girmez — `validate_structure.py § check_child_privacy` denetler.

---

## ALINMIŞ KARARLAR

### K1 · Ortak kütüphane YOK — üç proje tam izole
**12 Ağustos 2026 · bootstrap.** Talimat § 31 bir ajanın tek klasörle
çalışabilmesini şart koşuyor. Paylaşılan bir dosyadaki değişiklik üç projeyi
birden kırar. **Kopyalanan kod biraz fazlalıktır; bağımlılık bir kırılganlıktır.**

### K2 · Faz kapısı `.gate` dosyasından okunur
Kapı tahmin edilmez. `--fix` kapıya dokunmaz (Bestiarium dersi).

### K3 · Tek format: ciltsiz
Aktivite kitabı **üzerine yazılır**. Kindle üretilmez — e-okuyucuda
çalışmaz ve kötü yorum üretir. Bu bir gelir kaybı değil, **itibar korumasıdır**.
Ciltli hediye sürümü A5 kararına bağlıdır.

### K4 · Bulmaca içerikten türer, süslenmez
Dekoratif tema **yasaktır**. Bir aktivite "hangi mitolojik bilgiyi öğretiyor"
sorusuna cevap veremiyorsa kitaba girmez. Bu, kitabın rakiplerinden ayrıldığı
tek yerdir ve bir üslup kuralı değil bir **kapsam kuralıdır**.

### K5 · Yaş politikası World Myths'ten KOPYALANMAZ, yeniden yazılır
Orada risk *okunan şiddetti*; burada risk **yapılan görev**. Çocuk artık
yazıyor, çiziyor, çözüyor. Altı yasak çerçeve
[`00_CONTEXT/AGE_POLICY.md`](00_CONTEXT/AGE_POLICY.md)'de tanımlıdır.

### K6 · Devralma = kopyalama + köken kaydı, canlı bağımlılık DEĞİL
World Myths deposunun kardeş dizinde bulunması **zorunlu değildir**.
Bu proje onsuz build alır, test edilir ve CI'ı yeşil yanar.
`--cross-check` yalnızca depo **varsa** çalışır ve yoksa **atlar**.

### K7 · Kalite kapıları üçüncü taraf paket kullanmaz
`validate.yml` saniyeler içinde biter. Ağır bağımlılıklar yalnızca görsel
ve dizgi işlerine aittir (`run_optional`).

### K8 · Kapsam sayıları Faz 1'e kadar HİPOTEZDİR
`scope.locked: false`. Faz 1 doğrular veya değiştirir.

### K9 · Doğrulanmamış devralma LOCKED OLAMAZ
**Bu projenin bel kemiği.** `inherited-provisional` bir kayda dayanan hiçbir
aktivite `locked` olamaz, dolayısıyla yazılamaz.

İki ayrı kapı denetler (`validate_spec.py` ve `validate_inheritance.py`) ve
`selftest.py` sözleşmenin **gevşetilmesini** de yakalar. Tek bir kapının
unutulması sistemi açmaz.

### K10 · Cevap anahtarı ve çocuk kimliği public depoya giremez
Cevaplar **ürünün kendisidir**; public depoda duran cevap ürünü değersizleştirir.
Çocuk testçi adları hiçbir koşulda depoya girmez.
`validate_structure.py` her ikisini de içerik taramasıyla denetler.
