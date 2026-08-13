# ÇOCUK SAHA TESTİ PROTOKOLÜ

> Faz 2 teslimatı · 13 Ağustos 2026 · karar **A7**
>
> **DURUM: PAKET HAZIR · TESTÇİ 0 · KOŞTURULMADI.**
>
> Bu belge testin **nasıl** yapılacağını tanımlar. Testin **yapıldığını**
> iddia etmez ve etmeyecektir. Sonuçlar
> [`CHILD_TEST_LOG.md`](CHILD_TEST_LOG.md) içindedir ve bugün **boştur**.

---

## 0 · Neden bu test var ve neden ajan yapamaz

Faz 1 altı katman kurdu, Faz 2 on altı sayfa yazdı ve on üç kapı hepsini
denetliyor. Kapıların **hiçbiri** şu soruyu cevaplayamaz:

> ### Sekiz yaşındaki bir çocuk bu sayfayı yardımsız yapabiliyor mu?

`qa_readability` cümlenin kaç kelime olduğunu sayar. `qa_instruction`
adımın bir fiille başladığını doğrular. İkisi de metnin **ölçülebilir**
tarafını görür. Anlaşılıp anlaşılmadığını yalnızca **bir çocuk** gösterir.

Ve bir yetişkin "ne demek istediğini" açıklarsa test **geçersizdir** —
çünkü ölçtüğümüz şey çocuğun zekâsı değil, **sayfanın netliğidir**.

> **Çocuk takılıyorsa suç çocukta değil talimattadır.**

---

## 1 · Testçi gereksinimi

| | |
|---|---|
| Asgari testçi | **2** |
| Yaş aralığı | 8–12 |
| İdeal dağılım | en az biri **8–9**, en az biri **11–12** |
| Mevcut | **0** |

Yaş dağılımı önemlidir çünkü kitap iki uca birden söz veriyor: ★ sayfaları
sekiz yaşındaki için, ★★★ sayfaları on iki yaşındaki için. Yalnızca on iki
yaşındakilerle yapılan bir test **kolaylık yanılsaması** üretir.

---

## 2 · Test dili — geçici Türkçe izni

Ticari kitap **İngilizcedir** (K21). Ama testçi bulunabilen çocuklar
Türkçe konuşuyorsa, tester-facing materyal **geçici olarak Türkçe**
üretilebilir.

```
GEÇERLİ    → Türkçe test sayfası ile ölçülen: talimat NETLİĞİ,
             görev MANTIĞI, mühür kuralının anlaşılırlığı, süre,
             takılma noktası, duygusal tepki
GEÇERSİZ   → Türkçe testin İngilizce sürümü de doğruladığı iddiası
```

> **Türkçe pilotun geçmesi İngilizce sürümün geçtiği anlamına GELMEZ.**
> İngilizce sürüm kendi kapılarından **bağımsız olarak** geçer ve
> mümkünse ayrıca İngilizce konuşan bir çocukla sınanır.

Türkçe materyal `04_BUILD/child_test_pack.py --lang tr` ile üretilir ve
o betik `founder.childTesters.founderConfirmed` **false** iken üretmeyi
**reddeder**. Gerekçe tek cümledir:

> Sahte test materyali, sahte test kaydının bir adım öncesidir.

---

## 3 · Ebeveyn/veli talimatı

Bu metin test paketiyle birlikte veliye verilir.

> **Ne yapıyoruz:** çocuğunuzdan bir aktivite kitabının birkaç sayfasını
> denemesini istiyoruz. Sınav değil; **sayfayı** sınıyoruz, çocuğu değil.
>
> **Sizden ricamız — en önemli kısım budur:**
>
> - Sayfayı **açıklamayın**. Çocuk "ne demek bu?" derse *"sende nasıl
>   duruyorsa öyle"* deyin ve bekleyin.
> - Cevabı **söylemeyin**, ima etmeyin, yüzünüzle onaylamayın.
> - Çocuk **takılırsa bırakabilir**. Takıldığı yer bizim için en değerli
>   bilgidir; tamamlanmış bir sayfadan daha değerlidir.
> - Çocuk **istediği an durabilir**. Israr etmeyin.
> - Yardım etmek zorunda kaldıysanız **lütfen yazın** — kaydı geçersiz
>   yapmaz, tam tersine kullanılabilir kılar.
>
> **Süre:** oturum başına 20–30 dakika, en çok 4 sayfa.
>
> **Toplamadığımız şeyler:** çocuğunuzun adı, soyadı, okulu, adresi,
> doğum tarihi, fotoğrafı, sesi. Kayıtta yalnızca `tester-01` gibi
> anonim bir kod, yaş ve sonuç durur.

---

## 4 · Oturum akışı

```
① Veli talimatı okur ve sözlü onay verir
② Çocuğa yalnızca şu söylenir:
     "Bu bir saha defteri. Sayfada ne yazıyorsa onu yap."
③ Süre başlatılır
④ Gözlemci SUSAR ve yalnızca not alır
⑤ Çocuk bitirdiğinde ya da bıraktığında süre durdurulur
⑥ Üç soru sorulur (§ 5)
⑦ Kayıt anonim kodla yazılır
```

**Gözlemcinin tek işi susmaktır.** Not alırken şunlara bakar:

- çocuk hangi cümleyi **iki kez** okudu
- parmağını nereye koydu, nerede durdu
- hangi adımı **atladı**
- ipucuna baktı mı, kaçıncı dakikada
- yüzü ne zaman değişti

---

## 5 · Oturum sonu üç soru

Kapalı uçlu sormayın; "beğendin mi?" sorusu her zaman "evet" alır.

1. **"Bu sayfada senden ne yapmanı istiyordu?"**
   → talimat anlaşıldı mı, kendi cümlesiyle
2. **"En zor yer neresiydi?"**
   → takılma noktası
3. **"Bunu bir arkadaşına anlatsan ne derdin?"**
   → görevin kendisi akılda kaldı mı

---

## 6 · Anonim kayıt şeması

Her sayfa denemesi bir kayıt üretir. Şema
`01_SOURCE/activity.schema.json § childTests` ile **birebir** aynıdır ve
`validate_structure.py § check_child_privacy` kimliği mekanik denetler.

```json
{
  "date": "2026-09-01",
  "tester": "tester-01",
  "age": 9,
  "understoodUnaided": false,
  "result": "partial",
  "notes": "…"
}
```

| Alan | Kural |
|---|---|
| `tester` | **`tester-\d{2}`** biçimi ZORUNLU. Gerçek ad CI'ı kırmızı yakar |
| `age` | yalnızca yaş; doğum tarihi **YOK** |
| `understoodUnaided` | yetişkin tek kelime açıkladıysa **false** |
| `result` | `solved` · `partial` · `stuck` |
| `notes` | çocuğu değil **sayfayı** tarif eder |

### Ayrıca toplanan (ham kayıtta, depoya girmez)

```
startedAt · endedAt            → süre
hintsUsed                      → 0 · 1 · 2
confusionPoints[]              → hangi cümlede duraksadı
misreadInstructions[]          → neyi yanlış anladı
difficultyFelt                 → çok kolay · uygun · çok zor
emotionalNote                  → sıkıldı · keyif aldı · gerildi · nötr
adultInterventions[]           → ne söylendi, hangi dakikada
quotes[]                       → çocuğun kendi cümleleri
```

Ham kayıtlar **yalnızca** `03_EDITORIAL/child_tests_raw/` altında durur ve
o dizin `.gitignore § ①c` ile dışlanmıştır. Depoya **yalnızca** anonim
özet girer.

---

## 7 · Ne toplamıyoruz — ve neden

| Toplanmaz | Gerekçe |
|---|---|
| Ad, soyad | Gerekli değil; anonim kod aynı işi görür |
| Okul, sınıf, adres | Gerekli değil ve kimliklendirir |
| Doğum tarihi | Yaş yeter; tarih bir kimlik bilgisidir |
| Fotoğraf, ses, video | Gerekli değil ve saklanması risktir |
| Ebeveyn iletişim bilgisi | Depoda durmaz; veli kaydı ayrı tutulur |

Gerekçe basit: **toplanmayan veri sızmaz.**

---

## 8 · Başarı ölçütü

Yol haritası Faz 2 için sert bir eşik koyuyor:

| Ölçüt | Eşik |
|---|---|
| Yardımsız anlaşılan sayfa oranı | **≥ %80** → PASS |
| | %60–80 → talimat dili **yeniden yazılır** |
| | **< %60** → şablon bozuk, **ŞABLONU DÜZELT** |

Ve bir kural daha, sayıdan bağımsız:

> **İki çocuğun ikisinin de takıldığı bir cümle, ölçü ne derse desin
> yeniden yazılır.**

---

## 9 · Test bittiğinde ne olur

```
① Ham kayıtlar child_tests_raw/ altına yazılır (depo dışı)
② Anonim özet CHILD_TEST_LOG.md'ye işlenir
③ Takılınan her talimat YENİDEN YAZILIR
④ Yeniden yazılan metin bütün kapılardan TEKRAR geçer
⑤ Türkçe testse: bulgular İngilizce sürüme YENİDEN YAZILARAK taşınır
   — makine çevirisiyle DEĞİL (K21)
⑥ İngilizce sürüm kapılardan BAĞIMSIZ olarak geçer
⑦ project_config § childTesters.externalValidation güncellenir
```

⑦ yalnızca **gerçek bir oturumdan sonra** değişir. `qa_language.py § ⑤`
testçi sayısı eşiğin altındayken `passed` yazılmasını **engeller**.

---

## 10 · Bu protokolün bilmediği

| Bilinmeyen | Ne zaman öğrenilir |
|---|---|
| Mühür kuralı yardımsız anlaşılıyor mu | ilk oturum |
| Yedi harfli mühür sekiz yaşındaki için uzun mu | ilk oturum |
| ★★★ sayfalar on iki yaşındakini de zorluyor mu | ilk oturum |
| Yıldızlı kutu fikri kaç saniyede anlaşılıyor | ilk oturum |
| Türkçe bulgular İngilizceye taşınabiliyor mu | ikinci tur |

Beşinin de cevabı **bugün yoktur** ve bu belge onları uydurmaz.
