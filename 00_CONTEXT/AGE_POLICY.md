# YAŞ POLİTİKASI — aktivite biçimine uyarlanmış

> World Myths'in `AGE_POLICY.md` disiplini burada **kopyalanmadı, yeniden
> yazıldı**. Gerekçe: orada risk *okunan şiddetti*; burada risk
> **yapılan görev**.
>
> Sürüm **2.0 · 13 Ağustos 2026** — Faz 1'de güvenlik sınıflandırması
> mekanikleştirildi · `qa_age.py` bu belgeyi **uygular**

---

## 1 · Temel fark

| | World Myths | Field Book |
|---|---|---|
| Çocuk ne yapıyor | **Okuyor** | **Yazıyor, çiziyor, çözüyor** |
| Risk | Sahnelenmiş şiddet | **Yapılması istenen eylem** |
| Kalıcılık | Sayfa kapanır | **Deftere yazılan kalır** |
| Başarısızlık | "Fazla karanlık" | "Çocuğum yapamadı / yanlış öğrendi" |

Bir çocuğa bir sahneyi *okutmak* ile bir görevi *yaptırmak* aynı şey değildir.

---

## 2 · Altı yasak çerçeve

Bir aktivite bunlardan birine giriyorsa **kitaba giremez**.
`qa_age.py` bunları mekanik olarak tarar.

| # | Yasak | Neden |
|---|---|---|
| 1 | **Kutsal ritüelin taklidi** | Bir ayini "oyun" hâline getirmek, o geleneği taşıyan aileyi rencide eder |
| 2 | **Kapalı bilginin "çözülmesi"** | Bazı bilgiler bir topluluğa aittir; onu bulmaca yapmak sahiplenmedir |
| 3 | **Gerçek kişi/topluluğun karikatürleştirilmesi** | Klişe, öğretmenin kitabı rafa koymamasına yeter |
| 4 | **Şiddetin sahnelenmesini gerektiren görev** | "Savaşı çiz" ≠ "kahramanı çiz" |
| 5 | **Çocuğun evden çıkmasını gerektiren görev** | Ebeveyn denetimi olmadan güvenli değil |
| 6 | **Kesici alet, ateş veya yiyecek gerektiren görev** | Aynı gerekçe; ayrıca alerji riski |

Kültürel taraftaki ayrıntılı karşılıkları:
[`CULTURE_POLICY.md § 7`](CULTURE_POLICY.md)

---

## 3 · GÜVENLİK SINIFI — deterministik, tahmin edilmez

> **Her aktivite üç sınıftan tam birini alır ve sınıf HESAPLANIR.**
> Bir insan "bence bu güvenli" diyemez; kural malzemeden türer.

```
safe              → kitapta · ebeveyn notu isteğe bağlı
safe-with-adult   → kitapta · ebeveyn notu ZORUNLU · sayfada işaret
do-not-use        → KİTABA GİREMEZ · gerekçe kayıtta kalır
```

### 3.1 · Malzeme beyaz listesi

Bir aktivite **yalnızca** listedeki malzemeleri isteyebilir. Listede
olmayan bir malzeme **tanınmaz** ve aktivite `do-not-use` olur.

> **Kapı kapalı yönde arızalanır.** "Bilmiyorum" cevabı `safe` değildir.

| Kademe | Malzeme | Sınıf katkısı |
|---|---|---|
| **T0** | `book` · `pencil` · `coloured-pencils` · `eraser` · `ruler` · `paper-strip` · `window-view` | `safe` |
| **T1** | `mirror` · `string` · `coin` · `torch` · `read-aloud-partner` | `safe-with-adult` |
| **TX** | `scissors` · `blade` · `needle` · `pin` · `fire` · `match` · `candle` · `food` · `liquid` · `small-parts` · `magnet` · `balloon` · `outdoor-site` · `heat-source` | `do-not-use` |

**T1 neden bu beş ve yalnızca bu beş:**

| Malzeme | Yetişkin neden gerekli |
|---|---|
| `mirror` | Cam. Kırılır ve kenarı keser |
| `string` | Uzun ip küçük çocukta dolanma riskidir; sonra kaldırılır |
| `coin` | Küçük parça — evde daha küçük bir kardeş varsa yutulur |
| `torch` | Pil bölmesi ve düğme pil; düğme pil yutulması acil bir durumdur |
| `read-aloud-partner` | Tanım gereği ikinci bir kişi ister |

Cetvel, kâğıt şerit ve pencereden bakmak **T0'dır**: plastik bir cetvelin
gerçek bir tehlikesi yoktur ve gereksiz bir "yetişkin çağır" işareti
ebeveynin satın aldığı meşguliyeti azaltır. Kapı gerçek riski işaretler,
her şeyi değil.

**TX gerekçeleri** — her biri gerçek bir çocuk ürünü riskidir:

| Malzeme | Risk |
|---|---|
| `scissors` · `blade` · `needle` · `pin` | kesik · delme |
| `fire` · `match` · `candle` · `heat-source` | yanık · yangın |
| `food` | alerji · boğulma · denetimsiz tüketim |
| `liquid` | dökülme · elektrik · kitabın kendisi bozulur |
| `small-parts` · `magnet` · `balloon` | **boğulma** ve mıknatıs yutulması (bağırsak perforasyonu) |
| `outdoor-site` | denetimsiz dış mekân · yasak çerçeve 5 |

`magnet` ve `balloon` listede olmalarının nedeni bir mit değil: küçük
mıknatıslar ve balon parçaları çocuk ürünlerinde **belgelenmiş** boğulma
ve yutma riskidir. Bir aktivite kitabının bunlara ihtiyacı yoktur.

### 3.2 · Karar ağacı

```
① Malzemede TX var mı?                      → EVET: do-not-use
② Altı yasak çerçeveden birine giriyor mu?  → EVET: do-not-use
③ Evden çıkmayı gerektiriyor mu?            → EVET: do-not-use
④ Malzemede tanınmayan bir şey var mı?      → EVET: do-not-use   (kapalı arıza)
⑤ Malzemede T1 var mı?                      → EVET: safe-with-adult
⑥ Yüksek sesle okuma / ebeveyn eşliği ister mi? → EVET: safe-with-adult
⑦ Çözülmemiş duygusal işaret taşıyor mu?    → EVET: safe-with-adult
⑧ Aksi hâlde                                → safe
```

Bu ağaç `04_BUILD/qa_age.py § classify()` içinde **birebir** kodlanmıştır ve
`05_TESTS/selftest.py` her dalının ısırdığını kanıtlar.

### 3.3 · Hedef dağılım

Bu kitap masada, kalemle çözülür. Beklenen dağılım:

| Sınıf | Hedef | Neden |
|---|---|---|
| `safe` | **≥ %90** | Ekransız + denetimsiz çözülebilir olmak ürünün vaadidir |
| `safe-with-adult` | ≤ %10 | Cetvel, ayna veya yüksek sesle okuma isteyen birkaç aktivite |
| `do-not-use` | **0** (kitapta) | Havuzda kalır, kitaba girmez |

`safe-with-adult` oranı %10'u aşarsa ürün vaadi bozulur: ebeveyn
"meşguliyet" satın aldı, **kendisine iş** değil.

---

## 4 · Duygusal risk — devralınan işaretlerden türer

Kaynak projedeki her hikâye `contentFlags` taşır ve bu işaretler
`IMPORT_MANIFEST.json`'a **taşınır**. Aktivite biçimindeki karşılıkları:

| İşaret | Aktivitede |
|---|---|
| `sexuality` | **Hikâye aktivite dışı.** Tartışma yok. |
| `cannibalism` · `abuse` · `torture` | Yalnızca **sonuç katmanı**; bölüm `forbiddenLayer` olarak kapalı |
| `sacrifice` · `supernatural-horror` | Sonuç katmanı; betimleme isteyen görev yok |
| `death` · `grief` · `violence` · `war` · `revenge` · `kidnapping` | Serbest — **sonuç anlatılır, dehşet betimlenmez** |
| `monsters` · `frightening-imagery` | Serbest. 8–12 yaş canavar ister; canavar korkulacak şey değildir |
| `religious` · `culturally-sensitive` | Atıf zorunlu; kutsal katman cevap olamaz ([`CULTURE_POLICY.md`](CULTURE_POLICY.md)) |

### Betimleme fiili taraması

`qa_age.py` çocuğa görünen metinde şu **eşleşmeyi** arar:

```
betimleme fiili   ×   işaretli ad
(draw, sketch, colour, show, act out, describe, retell)
                  ×
(wound, blood, killing, corpse, sacrifice, torture, devour, beheading, drowning)
```

Eşleşme varsa aktivite **kırmızıdır**. Bu, "Savaşı çiz" ile "Kahramanı çiz"
arasındaki farkı bir insana değil bir **kapıya** bağlar.

---

## 5 · Şiddet ve trajedi: saklanmaz, sahnelenmez

World Myths'in kuralı burada da geçerlidir ve **aynı cümleyle** durur:

> *Şiddet ve trajedi **saklanmaz** ama **sahnelenmez**: sonuç anlatılır,
> dehşet betimlenmez.*

Aktivite biçimindeki karşılığı:

| ✅ Olur | ❌ Olmaz |
|---|---|
| "Bu kahraman üç sınavdan geçti. Sınavları sırala." | "Kahramanın yaralarını çiz." |
| "Canavarın hangi kültürde ne ad aldığını eşleştir." | "Canavarın avını nasıl parçaladığını anlat." |
| "Yeraltına inen tanrıçanın yolunu bul." | "Ölüler diyarını betimle." |

---

## 6 · Zorluk merdiveni — 8 yaş da 12 yaş da kullanabilmeli

Her bölümde aktiviteler **★ → ★★★** sırasıyla dizilir.

| Yıldız | Yaş | Yapı |
|---|---|---|
| ★ | 8–9 | tek adımlı · örnekli · ipuçsuz çözülür |
| ★★ | 10–11 | iki adımlı · ipuçsuz çözülebilir |
| ★★★ | 12 | çok adımlı · **kademeli ipucu var** |

Bir bölümde ★★★ oranı **%30'u aşamaz**. Aşarsa küçük çocuk kitabı bırakır.

Ölçülen dağılım (Faz 1 · `region_index.json § difficultyProfile`):

| Bölge | ★ | ★★ | ★★★ | ★★★ oranı |
|---|---:|---:|---:|---:|
| north-ice | 10 | 10 | 4 | %16,7 |
| middle-sea | 8 | 8 | 4 | %20,0 |
| sun-savanna | 6 | 7 | 3 | %18,8 |
| monsoon | 9 | 10 | 5 | %20,8 |
| great-ocean | 7 | 8 | 5 | %25,0 |
| jaguar-condor | 5 | 7 | 4 | %25,0 |

Merdiven **rota boyunca** yükselir: 1. bölge %16,7 → 6. bölge %25,0.

---

## 7 · Talimat netliği bir yaş meselesidir

Çocuk takılıyorsa **suç çocukta değil talimattadır**.

| Ölçüt | Değer | Kapı |
|---|---|---|
| Talimat cümlesi azami | **18 kelime** | `qa_instruction` |
| Adım sayısı azami | **4** (★ için 2) | `qa_instruction` |
| Cümle ortalaması | 9–14 kelime | `qa_readability` |
| Okuma seviyesi | 3.–5. sınıf | `qa_readability` |
| Şahıs | ikinci tekil (`you`) | `qa_instruction` |
| Küçümseyen ton | **YASAK** | `qa_voice` |

**Faz 2'nin sert ölçütü:** çocuk testinde aktivitelerin **≥%80'i yardımsız
anlaşılmalıdır**. Bir yetişkin "ne demek istediğini" açıklarsa test geçersizdir.

---

## 8 · İki ebeveyn okuması

World Myths'in H8 disiplini burada da zorunludur ve `project_config.json §
safety.parentReadingsRequired = 2` içinde durur.

Kanıt cinsi **açıkça** kaydedilir: kurucu beyanı mı, imzalı okuyucu kaydı mı.
Uydurulmuş okuyucu adı, tarihi veya alıntısı **yasaktır**.

---

## 9 · Çocuk testçi mahremiyeti

Çocuk testçilerinin adları **hiçbir koşulda** depoya girmez.
Kayıtlar yalnızca anonim kimlik (`tester-01`), yaş ve sonuç taşır.

`validate_structure.py § check_child_privacy` bunu mekanik olarak denetler:
`tester` alanı `tester-\d{2}` biçiminde değilse **CI kırmızı yanar**.
