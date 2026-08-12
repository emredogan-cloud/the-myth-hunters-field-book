# THE MYTH HUNTER'S FIELD BOOK — UYGULAMA YOL HARİTASI

> **Bu belge tek doğruluk kaynağıdır.** Altı faz, kapılar, testler, DoD.
> Bir ajan bu dosyayı altı ay sonra açtığında ne yapacağını, hangi sırayla
> yapacağını, neyin PASS neyin FAIL olduğunu buradan öğrenir.
>
> Sürüm: **1.0 · bootstrap** · Tarih: **12 Ağustos 2026** · Kapı: `phase0`
> Depo: `emredogan-cloud/the-myth-hunters-field-book`
>
> **Bu proje diğer projelerden İZOLEDİR** — ama
> `THE-GREAT-BOOK-OF-WORLD-MYTHS`'ten **veri devralır**. Devralma bir
> *kopyalama + köken kaydı*dır, **canlı bağımlılık değildir**:
> [`00_CONTEXT/INHERITANCE_ARCHITECTURE.md`](00_CONTEXT/INHERITANCE_ARCHITECTURE.md)

---

## 0 · Bu kitap nedir, neden bu kitap

**The Myth Hunter's Field Book** — 8–12 yaş için, 22 kültürü gezen tek bir
"saha görevi" olarak kurulmuş, 120 aktivitelik ekransız bir keşif defteri.

Pazar gerekçesi: çocuk kurgu-dışı 2026 H1'de **+%4,0** büyüdü ve Circana
bu büyümenin motorunu doğrudan **aktivite kitapları** olarak gösteriyor.
Rafta ise ya lisanslı IP (Highlights, Disney, Minecraft) ya da binlerce
jenerik bulmaca dolgusu var. **Bilgi taşıyan aktivite kitabı neredeyse yok.**

Ve bu kitabın en büyük ticari avantajı ürünün kendisinde değil,
**elimizde hazır duran okurda**: *The Great Book of World Myths*'in alıcısı
ile bu kitabın alıcısı **aynı kişidir**.

Kaynak: `AMAZON-KDP-2026-MARKET-OPPORTUNITY-REPORT.html` § 8 · WS-2 ve § 11 · Kitap B.

| | |
|---|---|
| Fırsat skoru | **6,0 / 10** — üçünün en düşüğü, **ve bu bilinçlidir** |
| Sıra | **#2 · ikinci yazılacak** |
| Ciltsiz birim telif (hipotez) | **5,55 $** · başabaş ACOS %37,0 |
| AI hendeği | 6 / 10 |
| Üretim zorluğu | **4 / 10** — portföyün en kolayı |

> **Neden en düşük skorlu kitabı yazıyoruz?** Çünkü bu kitabın işi tek
> başına para kazanmak değil: *World Myths'in öksüzlüğünü bitirmek*.
> World Myths portföyün en dar marjlı, en pahalı raftaki, **read-through'suz**
> ürünüdür. Bu kitap ona bir ikinci ürün verir ve tek kitabı bir seriye
> çevirir. Değeri kendi P&L'inde değil, **portföy etkisinde** ölçülür.

---

## 1 · BU KİTABIN İKİ BENZERSİZ RİSKİ

### Risk A — Çocuk ürünü riski
Alıcı ebeveyndir, okur çocuktur. Yanlış tonlanmış bir görev
*"çocuğum için fazla karanlık"* yorumuna dönüşür ve **o yorum silinmez**.
World Myths'in `AGE_POLICY` disiplini burada **aktivite** biçimine uyarlanır —
çünkü çocuk artık yalnızca okumuyor: **yazıyor, çiziyor, çözüyor.**

### Risk B — Devralma riski
Bu proje hazır bir araştırma tabanından besleniyor. **Bu bir avantaj ve
aynı zamanda bir tuzaktır:** devralınan veri otomatik olarak güvenilir
sayılırsa, World Myths'in anlatı için yeterli olan bir iddiası burada
bir **bulmaca cevabı** hâline gelir ve yanlışsa çocuk *"ben yanlış yaptım"*
diye düşünür.

> Bir hikâye anlatmak ile bir aktivite tasarlamak **aynı iddia değildir**.

Öncelik sırası — çakışmada yukarıdaki kazanır:

1. **Çocuğun güvenliği ve yaş uygunluğu**
2. **Cevap kesinliği** (tek ve doğru cevap)
3. Kültürel doğruluk ve kısıt taraması
4. Talimat netliği (çocuk tek başına anlayabilmeli)
5. Öğrenme değeri
6. Sayfa / kelime bütçesi
7. Üretim hızı

---

## 2 · Altı faz · tek bakışta

| Faz | Ad | Yazım | Kapı | Dal |
|---|---|---|---|---|
| **1** | Devralma mimarisi, aktivite taksonomisi, yaş çerçevesi | **yok** | `phase1` | `faz/1-devralma` |
| **2** | Pilot: bir bölge (20 aktivite) + **çocuk saha testi** | ~3.700 kelime | `phase2` | `faz/2-pilot` |
| **3** | Bölge bloğu I — üç bölge (60 aktivite) | ~7.400 kelime | `phase3` | `faz/3-blok-1` |
| **4** | Bölge bloğu II — üç bölge + final görev (40 aktivite) | ~6.900 kelime | `phase4` | `faz/4-blok-2` |
| **5** | Editoryal yakınsama + sayfa tasarımı + görsel üretim | ~4.000 kelime | `phase5` | `faz/5-yakinsama` |
| **6** | Nihai üretim + KDP paketi | **yok** | `release` | `faz/6-uretim` |

**Faz 4 sonunda manuscript ÖZÜNDE TAMAMDIR.**

Pazar raporunun üretim tahmini **7–9 hafta**. Bu bir *planlama referansıdır,
garanti değil* — ve yalnızca araştırma devralındığı için gerçekçidir.

---

# FAZ 1 — DEVRALMA MİMARİSİ, AKTİVİTE TAKSONOMİSİ, YAŞ ÇERÇEVESİ

### 1. Faz amacı
Üç şeyi kurmak: **(a)** World Myths'ten neyin devralınacağı ve hangi
koşulla, **(b)** aktivite taksonomisi ve aday havuzu, **(c)** çocuk ürünü
güvenlik çerçevesi. Bu fazda tek bir aktivite yazılmaz.

### 2. Kapsam
- Devralma manifestosu: hangi kayıt, hangi sha256, hangi doğrulama durumu
- ≥160 aktivite adayı (120'lik hedefin %33 fazlası)
- 6 bölge × 5 aktivite tipi matrisi ve **her hücrenin dolu olduğunun kanıtı**
- Mühür/ilerleme sisteminin mimarisi
- `AGE_POLICY.md` — aktivite biçimine uyarlanmış
- Aktivite veri şeması

### 3. Teslimatlar
| Dosya | Ne |
|---|---|
| `01_SOURCE/inherited/IMPORT_MANIFEST.json` | **Devralınan her kayıt · sha256 · köken · doğrulama durumu** |
| `01_SOURCE/activity_index.json` | ≥160 aday · şemaya uygun |
| `01_SOURCE/activity.schema.json` | Aktivite kaydı şeması |
| `01_SOURCE/region_index.json` | 6 bölge · kültür eşlemesi · mühür tanımı |
| `00_CONTEXT/INHERITANCE_ARCHITECTURE.md` | **Devralma sözleşmesi** |
| `00_CONTEXT/AGE_POLICY.md` | Yaş uygunluğu çerçevesi — aktivite biçimi |
| `00_CONTEXT/SOURCING_STANDARD.md` | Kaynak ve kısıt taraması |
| `00_CONTEXT/STYLE.md` v1.0 | Faz 2'de kalibre edilecek |
| `04_BUILD/validate_spec.py` · `validate_structure.py` · `validate_inheritance.py` | Kapılar |
| `05_TESTS/selftest.py` | **Kapıların kendi testi** |
| `06_REPORTS/PHASE_1_REPORT.md` | Faz raporu |

### 4. Yazım hedefi
**YOK.** Araştırma ve mimari fazı.

### 5. Yaklaşık kelime hedefi
0 (aktivite). Belgeler ~9.000 kelime.

### 6. Yaklaşık sayfa hedefi
0 manuscript sayfası. Sayfa modeli üretilir:
ön madde 8 + 6 bölge × 20 sayfa + final görev 10 + arka madde 14 = **152**
→ hedef 144 ile karşılaştırılır ve **fark Faz 1'de kapatılır**.

### 7. Araştırma gereksinimleri
**Bu fazın en kritik kararı devralma politikasıdır.** Üç durum tanımlanır:

| Durum | Anlam | `locked` olabilir mi |
|---|---|---|
| `inherited-provisional` | Kopyalandı, **bağımsız doğrulanmadı** | ❌ **HAYIR** |
| `inherited-verified` | Bu projede yeniden doğrulandı | ✅ |
| `new-researched` | World Myths'te yok, sıfırdan araştırıldı | ✅ |

**Yeniden doğrulama ZORUNLU olan alanlar:**
- Bir aktivitenin **cevabını** üreten her kültürel iddia
- Telaffuz
- Ad yazımı ve diakritikler
- **Çocuğun deftere yazacağı her şey**

Gerekçe: World Myths'te *"bu mitte X olur"* cümlesi anlatı için yeterlidir.
Burada aynı cümle bir **bulmaca cevabıdır** ve yanlışsa çocuk kendini
suçlar.

### 8. Test altyapısı
| Betik | Ne denetler |
|---|---|
| `validate_spec.py` | Şema, kimlik tekilliği, kapsam, kapı seviyesi |
| `validate_inheritance.py` | **Manifest bütünlüğü**: her devralınan kayıt sha256'lı mı, kökeni yazılı mı, durumu geçerli mi |
| `validate_structure.py` | Depo, belge, gömülü değer, manuscript sızıntısı |
| `qa_matrix.py` | 6×5 bölge-tip matrisinin her hücresi dolu mu |
| `selftest.py` | **Kapılar gerçekten ısırıyor mu** |

### 9. QA kapıları
```bash
./04_BUILD/qa_all.sh phase1
```

### 10. Definition of Done
- [ ] `IMPORT_MANIFEST.json` üretildi; devralınan her kayıt sha256'lı
- [ ] Devralma politikası (§ 7) `INHERITANCE_ARCHITECTURE.md`'de yazılı ve onaylı
- [ ] ≥160 aktivite adayı, şemayı geçiyor
- [ ] 6×5 matrisin **her hücresi** minimum sayıyı sağlıyor
- [ ] `AGE_POLICY.md` onaylı — 6 yasak çerçeve tanımlı
- [ ] Kısıt taraması 160/160 muafiyetsiz
- [ ] Mühür sistemi mimarisi tanımlı
- [ ] Sayfa modeli üretildi
- [ ] `selftest.py` yeşil
- [ ] CI **YEŞİL** · `.gate` → `phase1`

### 11. PASS kriterleri
- ≥160 aday; 22 kültürün **tamamı** temsil ediliyor
- 6×5 matrisin 30 hücresinin hepsi dolu
- Devralınan kayıtların ≥%80'i `inherited-verified` veya doğrulama planı var
- Sayfa modeli 144 ± %6

### 12. FAIL kriterleri
- Aday <160 → kapsam gerçekçi değil
- Bir matris hücresi boş → **o bölge o tipte aktivite üretemiyor**; taksonomi değişir
- Devralınan bir kayıt sha256'sız → **manifest geçersiz**, faz kapanamaz
- Sayfa modeli 144'ü >%6 aşıyor → kapsam düşer (**fiyat 14,99 $'da kalmalı**)

### 13. Ajan öz-notları
- **Devralma bir kısayol değil, bir sözleşmedir.** "World Myths'te yazıyordu"
  bir doğrulama değildir. Manifest bunu mekanikleştirir.
- 6×5 matrisi erken kur. "Kuzeyin Buzları bölgesinde 4 tasnif aktivitesi
  bulamıyorum" sorununu 90. aktivitede öğrenmek pahalıdır.
- `AGE_POLICY`'yi World Myths'ten **kopyalama**; uyarla. Orada risk
  *okunan şiddetti*; burada risk *yapılan görev*.

### 14. Kurucu bağımlılıkları
| # | Ne | Ne zaman |
|---|---|---|
| A1 | Manuscript public depoda mı duracak? | **Faz 1 başlamadan** |
| A2 | Devralma politikası onayı | **Faz 1 başlamadan** |
| A3 | 6 bölge ve mühür mimarisi onayı | Faz 1 sonu |
| A4 | 120 aktivitenin nihai listesi | Faz 1 sonu |

### 15. Git kilometre taşı
```
dal: faz/1-devralma  ·  etiket: v0.1.0
```

### 16. CI gereksinimleri
`validate.yml` yeşil: `gate` · `data` · `inheritance` · `structure` ·
`gates-selftest` · `production-model`.

### 17. Beklenen çıktılar
`IMPORT_MANIFEST.json` · `activity_index.json` · `region_index.json` ·
`activity.schema.json` · `AGE_POLICY.md` · `page-budget.json` ·
`PHASE_1_REPORT.md`

### 18. Riskler
| Risk | Azaltma |
|---|---|
| Devralınan veri sessizce doğrulanmamış kalır | `inherited-provisional` **`locked` olamaz** — mekanik kilit |
| 22 kültür 6 bölgeye dengesiz dağılıyor | Bölge tanımı Faz 1'de esnektir; kültür sayısı sabittir |
| Yaş politikası aktiviteye uymuyor | Politika World Myths'ten kopyalanmaz, **yeniden yazılır** |

### 19. Faz devri
Faz 2'ye girmek için: `.gate` = `phase1`, CI yeşil, A2 ve A3 kapalı,
**çocuk testçileri belirlenmiş** (A7).

---

# FAZ 2 — PİLOT: BİR BÖLGE + ÇOCUK SAHA TESTİ

### 1. Faz amacı
Bir bölgenin tamamını (20 aktivite) yazıp **gerçek çocuklarla test etmek**.
Bu faz bir üretim fazı değil, bir **doğrulama fazıdır**.

### 2. Kapsam
Bir bölge · 5 aktivite tipinin hepsi · bölge mührü · zorluk merdiveni.

**Hangi bölge?** En zor olanı — kültürel kısıt taraması en yoğun,
şifre sistemi en yabancı olan. Kolay bölgeyle kalibre edilen bir şablon
zor bölgede kırılır ve bunu 100. aktivitede öğrenirsiniz.

### 3. Teslimatlar
| Dosya | Ne |
|---|---|
| `02_MANUSCRIPT/book.json` | 20 aktivite · **depo dışı** |
| `03_EDITORIAL/CHILD_TEST_LOG.md` | **Çocuk saha testi kayıtları** |
| `03_EDITORIAL/AGE_REVIEW_LOG.md` | Yaş incelemesi |
| `00_CONTEXT/STYLE.md` v2.0 | Ölçümle kalibre |
| `04_BUILD/qa_age.py` · `qa_solvable.py` · `qa_instruction.py` | Kapılar |
| `04_BUILD/qa_readability.py` | Okunabilirlik (3.–5. sınıf) |
| `06_REPORTS/PHASE_2_REPORT.md` | **Kalibrasyon raporu** |

### 4. Yazım hedefi
20 aktivite + bölge açılışı + bölge mührü.

### 5. Yaklaşık kelime hedefi
**~3.700**. Aktivite kitabında kelime azdır; asıl iş **sayfa tasarımıdır**.

### 6. Yaklaşık sayfa hedefi
**~24 sayfa** dizilmiş — 144 sayfalık modelin ilk gerçek doğrulaması.

### 7. Araştırma gereksinimleri
20 aktivitenin dayandığı her kültürel iddia `inherited-verified` veya
`new-researched` olmalıdır. **`inherited-provisional` kalan hiçbir iddia
pilotta kullanılamaz.**

### 8. Test altyapısı
Faz 1 kapıları + dört yeni kapı:

```
qa_age.py          → 6 yasak çerçeve · yaş kalibrasyonu
qa_solvable.py     → her aktivitenin TEK ve DOĞRU cevabı var mı
                     (openEnded: true olanlar hariç)
qa_instruction.py  → talimat cümleleri ≤18 kelime · ikinci tekil şahıs
qa_readability.py  → 3.–5. sınıf bandı · cümle ort. 9–14 kelime
```

### 9. QA kapıları
```bash
./04_BUILD/qa_all.sh phase2
```

### 10. Definition of Done
- [ ] 20 aktivite yazıldı, `locked`
- [ ] **≥2 çocukla saha testi yapıldı ve kaydedildi**
- [ ] Çocukların **tek başına** anlayamadığı her talimat yeniden yazıldı
- [ ] `qa_solvable` 20/20 — çift cevaplı aktivite yok
- [ ] Zorluk merdiveni doğrulandı (8 yaş da 12 yaş da kullanabiliyor)
- [ ] `STYLE.md` ölçümle güncellendi
- [ ] Gerçek dizgi ölçümü → sayfa modeli güncel
- [ ] CI **YEŞİL** · `.gate` → `phase2`

### 11. PASS kriterleri
- 20/20 aktivite tek cevaplı (veya açıkça `openEnded`)
- Çocuk testinde **≥%80 aktivite yardımsız anlaşıldı**
- Sayfa/aktivite ölçüldü ve modelle uyumlu
- Okunabilirlik 3.–5. sınıf bandında

### 12. FAIL kriterleri
- **≥3 aktivite çift cevaplı** → aktivite tasarım şablonu bozuk. **ŞABLONU DÜZELT.**
- Çocuk testinde <%60 yardımsız anlaşılma → talimat dili yeniden yazılır
- Sayfa/aktivite modeli >%15 aşıyor → kapsam 120'den düşürülür

> **Bu fazın en önemli kuralı:** pilot bozuk bir tasarım kuralını açığa
> çıkarırsa **KURALI DÜZELT**. Sonraki 100 aktiviteyi bozuk kurala uydurmak,
> hatayı beş katına çıkarmaktır.

### 13. Ajan öz-notları
- **Çocuk testini sen yapamazsın.** Testçi çocuktur ve yalnızca sayfadaki
  talimatı okur. Bir yetişkin "ne demek istediğini" açıklarsa test geçersizdir.
- Bir çocuk takılıyorsa suç çocukta değil talimattadır.
- `openEnded: true` bir kaçış kapısı değildir. "Çiz/yaz" tipi dışında
  kullanılırsa `qa_solvable` kırmızı yanar.

### 14. Kurucu bağımlılıkları
| # | Ne |
|---|---|
| A7 | **≥2 çocuk testçi** — Faz 2'nin SERT BLOKLAYICISI |
| A5 | Kalibre edilmiş `STYLE.md` onayı |

### 15. Git kilometre taşı
```
dal: faz/2-pilot  ·  etiket: v0.2.0
```

### 16. CI gereksinimleri
`gates-selftest` yeni dört kapıyı da kapsamalı.

### 17. Beklenen çıktılar
`book.json` (20) · `CHILD_TEST_LOG.md` · `STYLE.md` v2.0 ·
`phase2-typeset-measurement.json` · `PHASE_2_REPORT.md`

### 18. Riskler
| Risk | Azaltma |
|---|---|
| Çocuk testçi bulunamıyor | Faz 2 **bloklanır**. Kabul edilen blok; sahte kayıt üretilmez |
| Aktivite çok kolay/zor çıkıyor | Zorluk merdiveni her bölümde ★–★★★ olarak ölçülür |
| Devralınan veri yanlış çıkıyor | Tam da bunun için pilot var — 20'de bulmak 120'de bulmaktan ucuz |

### 19. Faz devri
Faz 3'e girmek için: 20/20 tek cevaplı, çocuk testi geçti,
`STYLE.md` v2.0 onaylı, `.gate` = `phase2`.

---

# FAZ 3 — BÖLGE BLOĞU I · ÜÇ BÖLGE

### 1. Faz amacı
İlk büyük üretim bloğu: üç bölge. Pilotun kalibre ettiği şablonun
**ölçekte** çalıştığını kanıtlamak.

### 2. Kapsam
3 bölge × 20 aktivite = **60 aktivite** (pilot dahil → net 40 yeni)
\+ 3 bölge açılışı + 3 bölge mührü

### 3. Teslimatlar
- `book.json` → 60 aktivite
- 3 bölge mührü, mekanik olarak doğrulanmış
- Ara çocuk testi (≥1 oturum)
- `06_REPORTS/PHASE_3_REPORT.md`

### 4. Yazım hedefi
40 yeni aktivite + 3 bölge açılışı.

### 5. Yaklaşık kelime hedefi
**~7.400** · kümülatif ~11.100.

### 6. Yaklaşık sayfa hedefi
~72 dizilmiş sayfa.

### 7. Araştırma gereksinimleri
60/60 aktivitenin kültürel dayanağı `inherited-verified` veya
`new-researched`. Kısıt taraması tam.

### 8. Test altyapısı
Faz 2 kapıları + `qa_progression.py`:

```
qa_progression.py → her bölge mührü, o bölümde GERÇEKTEN bulunan
                    cevaplardan mı türüyor
                  → mühür kodu benzersiz mi
                  → final görev bütün mühürleri istiyor mu
```

### 9. QA kapıları
```bash
./04_BUILD/qa_all.sh phase3
```

### 10. Definition of Done
- [ ] 60 aktivite yazıldı ve `locked`
- [ ] 3 bölge mührü mekanik olarak doğrulandı
- [ ] `qa_solvable` 60/60
- [ ] Sürüklenme ölçüldü (pilot ↔ blok I)
- [ ] CI **YEŞİL** · `.gate` → `phase3`

### 11. PASS kriterleri
- 60/60 tek cevaplı · matris hücreleri dolu
- Mühür bütünlüğü 3/3
- Okunabilirlik bandı korunuyor

### 12. FAIL kriterleri
- Bir mühür, kitapta bulunmayan bir cevaba dayanıyor → **bloklayıcı**
- Çift cevaplı aktivite → o aktivite `candidate`'a düşer, havuzdan değişir
- Sürüklenme eşiği aşıldı → **ölç, yorumla, sonra düzelt**

### 13. Ajan öz-notları
- Mühür sistemi kitabın tamamlanma güdüsüdür. Bir çocuk mührü çözemezse
  kitabı bitiremez ve ebeveyn bunu yorumda yazar.
- Yedek aktiviteler Faz 1'in 160'lık havuzundan gelir.

### 14. Kurucu bağımlılıkları
Ara çocuk testi (≥1 oturum). Görsel üretimi bu fazda gerekmez.

### 15. Git kilometre taşı
```
dal: faz/3-blok-1  ·  etiket: v0.3.0
```

### 16. CI gereksinimleri
Tam `validate.yml`.

### 17. Beklenen çıktılar
`book.json` (60) · `qa-progression.json` · `qa-drift.json` · `PHASE_3_REPORT.md`

### 18. Riskler
| Risk | Azaltma |
|---|---|
| Aktiviteler tekrar ediyor gibi okunuyor | `qa_echo` + 5 tipin bölge içinde zorunlu dağılımı |
| Mühür mekaniği karmaşıklaşıyor | Mimari Faz 1'de donduruldu; değişiklik karar gerektirir |

### 19. Faz devri
Faz 4: kalan üç bölge + final görev.

---

# FAZ 4 — BÖLGE BLOĞU II + FİNAL GÖREV

### 1. Faz amacı
**Manuscript'i özünde tamamlamak.**

### 2. Kapsam
3 bölge × 20 = **60 aktivite** (kümülatif 120)
\+ **FINAL QUEST · The Cartographer's Seal**
\+ arka madde: kademeli ipuçları · cevap anahtarı · kültür sözlüğü ·
World Myths köprü sayfası

### 3. Teslimatlar
- `book.json` → **120 aktivite**
- Final görev: 6 mührü tek çözüme bağlayan meta-bulmaca
- **Büyük tasnif tablosu** — 22 kültürün ortak motifleri (doldurulacak boş tablo)
- Saha araştırmacısı sertifikası
- Arka madde tamam
- `06_REPORTS/PHASE_4_REPORT.md`

### 4. Yazım hedefi
60 aktivite + final görev + arka maddenin tamamı.

### 5. Yaklaşık kelime hedefi
**~6.900** · kümülatif **~18.000**.

### 6. Yaklaşık sayfa hedefi
~130 → arka madde ile **~144**.

### 7. Araştırma gereksinimleri
120/120 doğrulanmış. **Kısıt taraması 160/160 muafiyetsiz.**

### 8. Test altyapısı
Tam kapı seti + `qa_answerkey.py` (cevap anahtarı 120/120 tam mı,
ipuçları cevabı sızdırıyor mu).

### 9. QA kapıları
```bash
./04_BUILD/qa_all.sh phase4
```

### 10. Definition of Done
- [ ] **120 aktivite yazıldı ve `locked`**
- [ ] 6 bölge mührü + final görev doğrulandı
- [ ] Cevap anahtarı 120/120
- [ ] Kademeli ipuçları tamam · **hiçbiri cevabı içermiyor**
- [ ] 22 kültürün tamamı temsil ediliyor — **alt başlık doğrulandı**
- [ ] **Manuscript özünde tamam**
- [ ] CI **YEŞİL** · `.gate` → `phase4`

### 11. PASS kriterleri
- 120 aktivite · 22 kültür · 6 bölge · 5 tip
- Toplam kelime 22.000 ± %15
- Sayfa modeli 144 ± %6

### 12. FAIL kriterleri
- Aktivite <120 → **alt başlık değişir** (kurucu kararı) veya havuzdan tamamlanır
- Kültür <22 → alt başlık değişir
- Sayfa >153 → **fiyat modeli bozulur**; kapsam düşer

### 13. Ajan öz-notları
- Alt başlıktaki **120** ve **22** doğrulanabilir vaatlerdir.
  `validate_spec.py` bunları kapıya bağlar.
- Final görev kitabın entelektüel doruğudur: çocuk 22 kültürü ayrı ayrı
  değil, **birbirine bakarak** anlar. Aceleye getirme.

### 14. Kurucu bağımlılıkları
| # | Ne |
|---|---|
| — | **İki ebeveyn okuması** (World Myths H8 disiplini) |
| A5 | Ciltli hediye sürümü kararı |

### 15. Git kilometre taşı
```
dal: faz/4-blok-2  ·  etiket: v0.4.0  ·  "manuscript özünde tamam"
```

### 16. CI gereksinimleri
`validate_spec.py --gate phase4` kapsamı **sert** denetler.

### 17. Beklenen çıktılar
`book.json` (120) · cevap anahtarı · `qa-answerkey.json` · `PHASE_4_REPORT.md`

### 18. Riskler
| Risk | Azaltma |
|---|---|
| Son 60 aktivitede kalite düşer | `qa_drift` blok I ↔ blok II |
| Final görev çok zor | Çocuk testinde ayrıca test edilir |
| İpucu cevabı sızdırıyor | `qa_answerkey` mekanik olarak denetler |

### 19. Faz devri
Faz 5'e girmek için manuscript tam, CI yeşil.

---

# FAZ 5 — EDİTORYAL YAKINSAMA + SAYFA TASARIMI + GÖRSEL ÜRETİM

### 1. Faz amacı
Metni yakınsamak, **sayfa tasarımını** çözmek ve görselleri üretmek.

> **Bu kitapta sayfa tasarımı, metinden daha önemlidir.** Çocuk sayfayı
> okumaz, **kullanır**: yazacak yer, çizecek alan, okunaklı ızgara.

### 2. Kapsam
- Ön madde: görev emri · araçlar · mühür sayfası · ipucu kuralı
- **LINE EDITOR alt-ajanı** — çocuk okunabilirliği ve talimat netliği odaklı
- ~150 görsel öğe: 120 aktivite düzeni + 22 kültür vinyeti + mühür/rozet seti
- `IMAGE_PROMPT_LIBRARY.html`
- İç blok dizgisi + metadata

### 3. Teslimatlar
| Dosya | Ne |
|---|---|
| `07_ASSETS/IMAGE_PROMPT_LIBRARY.html` | Kopyalanabilir prompt kütüphanesi |
| `07_ASSETS/raw/` | Kurucunun PNG'leri — **SALT OKUNUR** |
| `04_BUILD/interior.py` · `metadata.py` | Üretim |
| `06_REPORTS/LINE_EDITOR_REPORT.md` | Alt-ajan bulguları |
| `06_REPORTS/PHASE_5_REPORT.md` | Faz raporu |

### 4. Yazım hedefi
Ön madde · görev emri anlatısı. **Yeni aktivite yazılmaz.**

### 5. Yaklaşık kelime hedefi
**~4.000** · kümülatif **~22.000**.

### 6. Yaklaşık sayfa hedefi
8 ön madde → toplam **~144**.

### 7. Araştırma gereksinimleri
Yeni araştırma yok. Devralma manifestosu **dondurulur** ve son hâli
raporlanır: kaç kayıt devralındı, kaçı doğrulandı.

### 8. Test altyapısı
Tam kapı seti + görsel hattı. **Envanter ölçümden ÖNCE koşar** —
yanlış aktiviteye bağlanmış kusursuz bir görsel, aktiviteyi çözülemez yapar.

### 9. QA kapıları
```bash
./04_BUILD/qa_all.sh phase5
```

### 10. Definition of Done
- [ ] Ön madde yazıldı
- [ ] **LINE EDITOR raporu alındı ve geçerli düzeltmeler uygulandı**
- [ ] 150/150 görsel üretildi ve doğru aktiviteye bağlandı
- [ ] **Yazma alanları ölçüldü** — çocuk eli sığıyor mu
- [ ] İç blok PDF üretildi — **gerçek sayfa sayısı**
- [ ] **İki ebeveyn okuması tamamlandı**
- [ ] CI **YEŞİL** · `.gate` → `phase5`

### 11. PASS kriterleri
- Gerçek sayfa 144 ± %6
- Görsel envanteri 150/150 · ≥300 dpi efektif
- Line Editor'ın bloklayıcı bulgusu kalmadı

### 12. FAIL kriterleri
- Yazma alanı yetersiz → **bloklayıcı** (ürünün işlevi bozulur)
- Görsel ↔ aktivite uyuşmazlığı → bloklayıcı
- Sayfa bandı aşıyor → fiyat modeli bozulur

### 13. Ajan öz-notları
- **Line Editor bir alt-ajandır ve körü körüne kabul edilmez.**
- Bu kitapta Line Editor'ın özel görevi: **çocuk okunabilirliği ve
  talimat netliği**.
- Yazma alanı ölçümü gerçek bir kapıdır: 8 yaşındaki bir çocuğun el
  yazısı yetişkininkinden büyüktür.

### 14. Kurucu bağımlılıkları
| # | Ne |
|---|---|
| — | **150 görselin üretilmesi** |
| — | **İki ebeveyn okuması** |
| A6 | Yazar biyografisi metni |

### 15. Git kilometre taşı
```
dal: faz/5-yakinsama  ·  etiket: v0.5.0
```

### 16. CI gereksinimleri
`validate.yml` + `images.yml` + `build.yml` yeşil.

### 17. Beklenen çıktılar
`IMAGE_PROMPT_LIBRARY.html` · işlenmiş varlıklar · iç blok PDF ·
`LINE_EDITOR_REPORT.md` · `PHASE_5_REPORT.md`

### 18. Riskler
| Risk | Azaltma |
|---|---|
| Sayfa tasarımı yazma alanını yiyor | Ölçüm kapısı; tasarım metne değil **kullanıma** göre |
| Görseller geç geliyor | Yazım fazları görsele bağlı değildi |

### 19. Faz devri
Faz 6: format üretimi ve KDP paketi.

---

# FAZ 6 — NİHAİ ÜRETİM + KDP PAKETİ

### 1. Faz amacı
Yüklemeye hazır dosyaları üretmek ve kurucuya teslim paketi vermek.

### 2. Kapsam
**Tek format: ciltsiz.** Kapak · A+ varlıkları · metadata · teslim kılavuzu.

> Kindle **üretilmez**. Üzerine yazılan bir kitap e-okuyucuda çalışmaz ve
> kötü yorum üretir. Bu bir gelir kaybı değil, **itibar korumasıdır**.

### 3. Teslimatlar
`08_OUTPUT/PAPERBACK/` · `03_APLUS/` · `06_REPORTS/tracked/metadata.json` ·
`KDP_UPLOAD_PLAYBOOK.md` · `06_REPORTS/FINAL_RELEASE_REPORT.md`

### 4–6. Yazım / kelime / sayfa
**Yeni yazım yok.** Sayfa sayısı ölçülür ve dondurulur.

### 7. Araştırma gereksinimleri
Yok. Devralma manifestosu dondurulmuş hâlde raporlanır.

### 8. Test altyapısı
`package_selftest.py` · `covers.py --check` · `aplus.py --check` ·
`handoff.py --check`

### 9. QA kapıları
```bash
./04_BUILD/qa_all.sh release
```

### 10. Definition of Done
- [ ] Ciltsiz üretildi ve doğrulandı
- [ ] Gerçek sayfa sayısı ölçüldü, sırt hesaplandı
- [ ] Kapak geometrisi · bleed · güvenli alan doğrulandı
- [ ] Metadata tam · **`authorBio` dolu**
- [ ] **World Myths köprü sayfası** doğrulandı
- [ ] `KDP_UPLOAD_PLAYBOOK.md` yazıldı
- [ ] CI **YEŞİL** · `.gate` → `release`
- [ ] **AJAN DURUR**

### 11. PASS kriterleri
Üretim kapıları yeşil · teslim paketi eksiksiz · nihai rapor yazıldı.

### 12. FAIL kriterleri
- `authorBio` null → kırmızı
- Sahte ISBN → kırmızı
- Cevap anahtarı eksik → kırmızı

### 13. Ajan öz-notları
- **KDP paneline dokunma.**
- Fiyat testi (14,99 $ vs 12,99 $) **kurucunun** işidir ve yayından sonra
  gelir; ajan fiyat değiştirmez.
- Nihai raporu yazdıktan sonra **DUR**.

### 14. Kurucu bağımlılıkları
KDP paneli · prova kopya · fiyat testi · yayın kararı.

### 15. Git kilometre taşı
```
dal: faz/6-uretim  ·  etiket: v1.0.0  ·  "release candidate"
```

### 16. CI gereksinimleri
`validate.yml` + `build.yml` + `release.yml` yeşil.

### 17. Beklenen çıktılar
Yüklemeye hazır ciltsiz · kapak · A+ · metadata · playbook · nihai rapor.

### 18. Riskler
| Risk | Azaltma |
|---|---|
| 14,99 $ raf çapasının (9,99 $) üstünde | A+ içerik iki örnek sayfayı gösterir; fiyat testi planlı |
| KDP metadata reddi | Yer tutucu metin YASAK |

### 19. Faz devri
**YOK — proje burada biter.**

---

## 3 · Sürekli kurallar

### Git akışı
Faz dalı → yerel `qa_all.sh` yeşil → commit → push → PR → **CI'ı bekle** →
yeşilse merge + etiket + `.gate` yükselt. **CI kırmızıyken hiçbir şey ilerlemez.**

### Devralma kilidi
```
inherited-provisional  →  LOCKED OLAMAZ  →  YAZILAMAZ
```
`validate_inheritance.py` bunu denetler.

### Araştırma → yazım kilidi
Doğrulanmamış hiçbir kültürel iddia bir aktivite **cevabı** olamaz.

### Public depo / özel içerik
| Public | Korumalı |
|---|---|
| kod · CI · şema · doğrulayıcı · **devralma manifestosu** | aktivite prozası · **cevap anahtarı** |
| belgeler · araştırma künyeleri · ölçüm raporları | ham görseller · çocuk testçi kimlikleri · `.env` |

> **Çocuk testçilerinin adları asla depoya girmez.** `CHILD_TEST_LOG.md`
> yalnızca anonim kimlik (`tester-01`), yaş ve sonuç taşır.

### Sürüklenme disiplini
**Ölç → yorumla → düzelt.** Metrik için proza yeniden yazılmaz.

---

## 4 · Bu yol haritasının bilmediği şeyler

| Bilinmeyen | Ne zaman öğrenilir |
|---|---|
| Devralınan verinin ne kadarı yeniden doğrulama gerektiriyor | **Faz 1** |
| 6×5 matrisin her hücresi dolabiliyor mu | **Faz 1** |
| Çocuklar talimatları yardımsız anlıyor mu | **Faz 2** |
| 120 aktivite 144 sayfaya sığıyor mu | **Faz 2** (gerçek dizgi) |
| Yazma alanları çocuk eline yetiyor mu | **Faz 5** |
| World Myths alıcısı ikinci ürünü alıyor mu | **yayından sonra — bu yol haritasının kapsamı dışında** |

Son satır bu projenin **varlık sebebidir** ve yol haritası onu
kanıtlayamaz — yalnızca test edilebilir hâle getirir.
