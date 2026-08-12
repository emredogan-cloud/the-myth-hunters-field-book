# DEVRALMA MİMARİSİ

> Bu belge bu projenin **en özgün yapısal parçasını** tanımlar:
> `THE-GREAT-BOOK-OF-WORLD-MYTHS`'ten veri nasıl devralınır ve
> hangi koşulla kullanılabilir.
>
> Sürüm 1.0 · Faz 1'de onaylanır · Değişiklik kurucu kararı gerektirir

---

## 1 · Neden devralıyoruz

*The Great Book of World Myths* 22 kültürü **kilitledi**: kültür indeksi,
araştırma kayıtları, telaffuz rehberi, kültürel notlar. O iş yapıldı ve
kapılardan geçti.

Bu kitabın **maliyet avantajının tamamı** budur. Rakip aktivite kitapları
araştırma yükü kaldıramaz çünkü rafın ekonomisi ucuzluk üzerine kuruludur
(6,99–9,99 $). Bizim marjinal araştırma maliyetimiz yapısal olarak düşüktür —
**çünkü araştırmayı zaten yaptık.**

---

## 2 · Ama devralma bir kısayol değildir

> ### Bir hikâye anlatmak ile bir aktivite tasarlamak aynı iddia değildir.

World Myths'te *"bu mitte kahraman üç sınavdan geçer"* cümlesi **anlatı için
yeterlidir**. Okur onu okur ve devam eder.

Burada aynı cümle bir **bulmaca cevabı** olur. Çocuk kutuya "3" yazar.
Cümle yanlışsa çocuk **kendini suçlar** — ve ebeveyn bunu yorumda yazar.

Doğrulama eşiği farklıdır çünkü **kullanım** farklıdır.

---

## 3 · Devralma bir KOPYALAMA + KÖKEN KAYDIdır

**Canlı bağımlılık değildir.**

| | |
|---|---|
| World Myths deposu kardeş dizinde olmalı mı | **HAYIR** |
| Bu proje onsuz build alır mı | **EVET** |
| Onsuz test edilir mi | **EVET** |
| Onsuz CI yeşil yanar mı | **EVET** |

Devralınan her kayıt `01_SOURCE/inherited/IMPORT_MANIFEST.json` içine
**sha256 ile** yazılır. Manifest kendi kendine yeterlidir.

Kaynak depo **varsa** `validate_inheritance.py --cross-check` sha256'ları
karşılaştırır ve sürüklenmeyi bildirir. **Yoksa bu bir kusur değildir** —
kapı "atlandı" der, kırmızı yanmaz.

### Manifest kaydı

```json
{
  "recordId": "culture-korean-pronunciation",
  "sourceRepo": "emredogan-cloud/the-great-book-of-world-myths",
  "sourcePath": "01_RESEARCH/research/korean.json",
  "sourceSha256": "…64 hex…",
  "importedAt": "2026-09-01",
  "status": "inherited-provisional",
  "revalidatedAt": null,
  "revalidatedBy": null,
  "note": "Telaffuz rehberi — çocuk deftere yazacağı için yeniden doğrulanmalı"
}
```

---

## 4 · Üç durum ve tek kural

| Durum | Anlam | `locked` olabilir mi |
|---|---|---|
| `inherited-provisional` | Kopyalandı, **bağımsız doğrulanmadı** | ❌ **HAYIR** |
| `inherited-verified` | Bu projede yeniden doğrulandı | ✅ |
| `new-researched` | World Myths'te yok, sıfırdan araştırıldı | ✅ |

> ## TEK KURAL
> **`inherited-provisional` bir kayda dayanan hiçbir aktivite
> `locked` olamaz — dolayısıyla yazılamaz.**

Bu kural `project_config.json § inheritance.lockRequiresStatus` içinde
durur ve **iki ayrı kapı** tarafından denetlenir:
`validate_spec.py` ve `validate_inheritance.py`.

Ve `selftest.py § ②(i)` bu sözleşmenin **gevşetilmesini** de yakalar:
biri `lockRequiresStatus` listesine `inherited-provisional` eklerse
kapı kırmızı yanar.

---

## 5 · Yeniden doğrulama ZORUNLU olan alanlar

Devralınan her kayıt yeniden doğrulanmak zorunda değildir. Ama şunlar
**zorunludur** — çünkü hepsi çocuğun **yazacağı** veya **cevaplayacağı**
şeye dönüşür:

| Alan | Neden |
|---|---|
| Bir aktivitenin **cevabını** üreten her kültürel iddia | Yanlışsa çocuk kendini suçlar |
| **Telaffuz** | Çocuk yüksek sesle okuyacak |
| **Ad yazımı ve diakritikler** | Çocuk deftere yazacak |
| **Çocuğun deftere yazacağı her şey** | Kalıcı, düzeltilemez |

Anlatı arka planı, kültürel bağlam ve genel çerçeve
`inherited-provisional` kalabilir — çünkü bunlar **cevap üretmez**.

---

## 6 · Neden World Myths deposuna canlı bağlanmıyoruz

Talimat § 31: *"Bir ajan bu klasörü açtığında diğer projelere ihtiyaç
duymamalıdır."*

Canlı bağımlılık üç şeyi kırar:

1. **İzolasyon** — World Myths'te bir dosya taşınırsa bu projenin CI'ı kırılır
2. **Yeniden üretilebilirlik** — build, başka bir deponun o anki durumuna bağlanır
3. **Denetlenebilirlik** — "hangi sürümü devraldık" sorusu cevapsız kalır

Kopyalama + sha256 üçünü de çözer: veri **burada**, kökeni **kayıtlı**,
sürüklenme **ölçülebilir**.

Karar: [`../DECISIONS.md`](../DECISIONS.md) § K9.
