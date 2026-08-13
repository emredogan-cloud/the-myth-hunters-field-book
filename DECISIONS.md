# DECISIONS — karar kaydı

> İki şey taşır: **alınmış kararlar** (`K##`) ve **AÇIK KARARLAR** (`A#`).
> Bir varsayım sessizce proje gerekliliğine dönüşemez.

---

## AÇIK KARARLAR — kurucudan yanıt bekleyen

Durum tablosu · **13 Ağustos 2026 · Faz 1 sonu**

| # | Soru | Aciliyet | Ne zaman kapanmalı | Durum |
|---|---|---|---|---|
| ~~A1~~ | ~~Manuscript public depoda mı duracak?~~ | — | — | ✅ **KAPANDI → K11** |
| ~~A2~~ | ~~Devralma politikası onayı~~ | — | — | ✅ **KAPANDI → K12** |
| **A3** | **6 bölge ve mühür mimarisi onayı** | **YÜKSEK** | **şimdi** | AÇIK · Faz 1 önerisi hazır |
| **A4** | 168 adaydan 120'sinin nihai seçimi | **YÜKSEK** | Faz 2 başlarken | AÇIK |
| **A8** | **YENİ** — 148 sayfa kabul edilip BRIEF § 7 mi güncellenecek | ORTA | Faz 2 | AÇIK |
| **A7** | **≥2 çocuk testçi kim** | **YÜKSEK** | **Faz 2 başlamadan** | AÇIK · **SERT BLOKLAYICI** |
| **A5** | Ciltli hediye sürümü v1.0'a girecek mi | DÜŞÜK | Faz 4 | AÇIK (varsayım: hayır) |
| **A6** | Yazar biyografisi metni | ORTA | Faz 5 | AÇIK |

---

### A3 · Bölge ve mühür mimarisi — Faz 1'in önerisi

**Bootstrap'ın altı bölgesi 22 kültüre oturmuyordu.** Okyanusya'ya iki
kültür düşüyor, Amerikalara **hiç bölge kalmıyordu**. Faz 1 bölgeleri
kıtaya göre değil **araziye** göre yeniden kurdu:

| # | Bölge | Kültür | Aktivite | Mühür |
|---|---|---:|---:|---:|
| 1 | The Northern Ice | 4 | 24 | 5 harf |
| 2 | The Middle Sea | 3 | 20 | 6 harf |
| 3 | Sun and Savanna | 3 | 16 | 7 harf |
| 4 | Mountain and Monsoon | 5 | 24 | 7 harf |
| 5 | The Great Ocean | 4 | 20 | 6 harf |
| 6 | Jaguar and Condor | 3 | 16 | 6 harf |

Kotalar **bilinçli olarak eşit değildir**: her bölge kendi kullanılabilir
hikâye arzıyla orantılı pay alır. Ayrıntı ve mühür mekaniği:
[`00_CONTEXT/PROGRESSION_ARCHITECTURE.md`](00_CONTEXT/PROGRESSION_ARCHITECTURE.md)

**Kurucu onayı bekleniyor.** Onaylanırsa mimari Faz 2'de dondurulur;
değişiklik sonrasında bir karar kaydı gerektirir.

### A8 · 148 sayfa mı, 144 sayfa mı — YENİ

Faz 1'in ölçtüğü sayfa modeli **148** (forma hizalı). Hedef 144'tü.
148 tolerans bandının içinde (**+%2,8**, sınır %6) ama BRIEF § 7'nin
telif hipotezinden **0,07 $** sapıyor.

| Şık | Sonuç |
|---|---|
| **(a)** 148'i kabul et | BRIEF § 7 güncellenir: telif **5,48 $**, başabaş ACOS %36,5 |
| (b) 4 sayfa kıs | Final görev 5→4 **veya** arka madde 14→13. Kapsam daralır |

**Faz 1'in önerisi: (a).** Gerekçe: 4 sayfa kısmak, final görevi veya
cevap anahtarını sıkıştırmak demektir ve ikisi de ürünün işlevidir.
0,07 $ bir modelleme farkıdır; sıkışmış bir cevap anahtarı bir **yorum**.

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

---

## FAZ 1 KARARLARI — 13 Ağustos 2026

### K11 · Manuscript public depoda DURMAZ (A1 kapandı)
**Bootstrap varsayımı onaylandı.** `.gitignore § ①` manuscript prozasını,
cevap anahtarını ve çocuk testçi kayıtlarını dışlar; `validate_structure.py`
ikinci hat olarak takip edilen dosyaların **içeriğine** bakar.

Public kalan: kod · CI · şema · doğrulayıcı · **devralma manifestosu** ·
belgeler · araştırma künyeleri · **ölçüm raporları**.

Sonuç: mühür sözcükleri (`01_SOURCE/answers/`) ve pilot prozası
(`02_MANUSCRIPT/pilot/`) depoda **yoktur**; raporlar yalnızca **sayı** taşır.

### K12 · Devralma politikası (a) — kopyala + sha256 + kullanıma göre doğrula (A2 kapandı)
Kurucunun *"START PHASE 1"* talimatı bootstrap varsayımını onayladı.

Devralma bir **kopyalama + köken kaydıdır**, canlı bağımlılık değil.
World Myths deposu kardeş dizinde bulunmak **zorunda değildir**: bu proje
onsuz build alır, test edilir ve CI'ı yeşil yanar. Depo **varsa**
`--cross-check` sha256'ları karşılaştırır ve sürüklenmeyi bildirir.

Şık (c) — *"devralınanı doğrulanmış say"* — **reddedildi**. Seçilseydi
`selftest § ②(i)` gevşetmeyi yakalayıp CI'ı kırmızı yakacaktı; yani karar
zaten sessizce alınamazdı.

### K13 · Kültür düşürülmez, BİÇİM daralır
`22` alt başlıkta yazan **doğrulanabilir bir vaattir**. Kısıt bulunduğunda
daralma sırası: **yasak biçim → izinli tip → kota → hikâye → (son çare) kültür**.

Faz 1'de ilk dördü kullanıldı, sonuncusu **hiç** kullanılmadı: iki hikâye
aktivite dışı bırakıldı (`egyptian-horus-seth` · `hindu-ganesha-head`),
yirmi hikâyede kapalı katman işaretlendi, dört kültür Kademe C'ye alındı.
**22 kültürün hepsi kitapta.**

Ayrıntı: [`00_CONTEXT/CULTURE_POLICY.md`](00_CONTEXT/CULTURE_POLICY.md)

### K14 · Güvenlik sınıfı HESAPLANIR, beyan edilmez
Bir insan *"bence bu güvenli"* diyemez. `safetyClass` malzemeden,
yasak çerçeveden ve kısıt durumundan **türetilir**
([`AGE_POLICY.md § 3.2`](00_CONTEXT/AGE_POLICY.md)) ve `qa_age.py`
beyan ile hesabı karşılaştırır.

**Kapı kapalı yönde arızalanır:** beyaz listede olmayan bir malzeme
`safe` sayılmaz, `do-not-use` olur. *"Bilmiyorum"* güvenli değildir.

`selftest § ⑤(k)` belgeyi, kodu ve şemayı **birbirine bağlar**: üçü
ayrıldığı an CI kırmızı yanar.

### K15 · Bölgeler kıtaya göre değil ARAZİYE göre kurulur
Bir saha defteri iklimi izler, siyasî sınırları değil — ve bu pedagojik
bir tercihtir: çocuk coğrafyanın hikâyeyi biçimlendirdiğini görür.

Bölge kotaları **eşit değildir** ve bu bilinçlidir: kota, o bölgenin
kullanılabilir hikâye arzıyla orantılıdır. Eşit dağıtım beş hikâyeli bir
bölgeden yirmi aktivite çıkarmayı zorlar ve bu **tekrar üretir**.

### K16 · Okunabilirlik bandı metne değil REGİSTERE bağlanır
Faz 1 pilotu bootstrap'ın tek bandının (9–14 kelime · 3.–5. sınıf)
bu kitapta **yanlış** olduğunu ölçtü. O bant World Myths'in **anlatı**
prozasından geliyordu.

> **Bir talimat bir anlatı cümlesi değildir.**

Üç register ayrı ölçülür (talimat · field note · ipucu) ve bir **değişmez**
eklenir: `fk(talimat) < fk(field note)` — bir talimat, tanıttığı içerikten
daha zor olamaz.

Ölçüm ve bantlar: [`00_CONTEXT/STYLE.md § 3`](00_CONTEXT/STYLE.md)

### K17 · Üretilen belgeler elle yazılmaz
`BOOK_STATS.md` ve `ROADMAP_PROGRESS.md` `04_BUILD/update_docs.py`
tarafından **üretilir** ve `--check` bayrağıyla bayatlıkları denetlenir.

Gerekçe: elle yazılan bir sayı bir süre sonra sessizce yanlış olur ve
kimse fark etmez — çünkü onu kimse denetlemez. İki belge de bootstrap'ta
zaten *"hiçbiri elle yazılmayacaktır"* diye söz vermişti.
