# FAZ 4 RAPORU — manuscript özünde tamam, ve bir çelişki mekanikleşti

> **The Myth Hunter's Field Book** · Faz 4 · 14 Ağustos 2026
> Dal `faz/4-blok-2` → `main` · Kapı **`phase1`'de KALDI** · Etiket `v0.4.0`
>
> Faz 3'ün sorusu *"sistem üç bölgeye ölçekleniyor mu"* idi. Bu fazınki
> başkaydı:
>
> **Kitap kapanabiliyor mu — ve kapanırken hangi vaatler tutmuyor?**
>
> Cevap: **evet, kapanıyor.** Ve tutmayan üç vaat bulundu: bir kapı eşiği,
> üç araştırma iddiası ve iki sayfa. Üçü de bulunması gereken yerde
> bulundu.

---

## 0 · Tek bakışta

| | Hedef | Ölçülen | Durum |
|---|---:|---:|---|
| Yeni sayfa | 60 | **60** | ✅ |
| Kümülatif sayfa | 120 | **120** | ✅ |
| Yazılmış bölge | 6 | **6 / 6** | ✅ |
| Kültür | 22 | **22** | ✅ |
| Final görev | var | **5 sayfa** | ✅ |
| Arka madde | yol haritası § 2 | **14 sayfa · 6 bölüm** | ✅ |
| Cevap anahtarı | 120/120 | **120** (105 kapalı · 15 ölçüt) | ✅ |
| Mühür yuvası | 37 | **37 / 37** | ✅ |
| Hasar yarıçapı | 1 | **1** | ✅ |
| Zincirleme bağımlılık | 0 | **0** | ✅ |
| Yeniden doğrulanan iddia | cevap üreten hepsi | **51 yeni** · 108 kümülatif | ✅ |
| **Reddedilen iddia** | — | **3** | ⚠ *bulundu* |
| Doğrulanmış devralma kaydı | — | **54 / 76** (Faz 3: 31) | ✅ |
| `safe` oranı | ≥%90 | **%96,7** (116/120) | ✅ |
| `safe-with-adult` | ≤%10 | **%3,3** (4/120) | ✅ |
| `do-not-use` | 0 | **0** | ✅ |
| Talimat registeri | 5–11 kel · FK ≤4,0 | **7,91 · 2,53** | ✅ |
| Field note registeri | 9–14 kel · FK 3,0–5,9 | **12,40 · 5,39** | ✅ |
| Okunabilirlik değişmezi | fk(talimat) < fk(note) | **2,53 < 5,39** | ✅ |
| Cevap belirlenimi | çift cevap yok | **120/120** | ✅ |
| Dil ayrımı | ticari %100 İngilizce | **814/814 dize** | ✅ |
| Görsel şartnamesi | her sayfa | **120** · 700 zorunlu etiket | ✅ |
| **Üretilmiş görsel** | Faz 5'e ait | **0** | ✅ *bilerek* |
| Sayfa modeli | 148 ±%6 | **144** (−%2,7) · **6/6 ölçüldü** | ✅ |
| Yeni kapı | qa_answerkey | **qa_answerkey** + validate_spec § ⑥ | ✅ |
| Kapı öz-testi | yeşil | **178 denetim** (Faz 3: 151) | ✅ |
| İç editoryal inceleme | koşsun | **9 bulgu · 2 bloklayıcı** | ⚠ *bulundu ve düzeltildi* |
| **Çocuk saha oturumu** | — | **0 oturum** | ⏳ **BEKLİYOR** |

```
FAZ 4 ÜRETİMİ           ✅ TAMAM       120 sayfa · 6 bölge · final görev · arka madde
A11 ÇELİŞKİSİ           ✅ KAPANDI     K29 · ve TÜRETMEYE çevrildi
KURUCU AŞMASI           ✅ GENİŞLEDİ   K30 · tavan DEĞİŞMEDİ
DIŞ ÇOCUK DOĞRULAMASI   ⏳ BEKLİYOR    0 oturum · A10 AÇIK

Bunlar TOPLANMAZ. MANUSCRIPT'İN BİTMESİ, FAZ 2'NİN KAPANMASI DEĞİLDİR.
```

---

## 1 · Faz 4 kapsamı

Yol haritası Faz 4'ü *"Bölge bloğu II + final görev"* diye tanımlıyor.
Yapılan iş:

```
① A11 çelişkisini KAPAT ve KÖK NEDENİ kapat        K29 · validate_spec § ⑥
② kurucu aşmasını Faz 4'e genişlet, TAVANI TUTMA   K30
③ 51 yeni iddiayı iddia düzeyinde doğrula          üç revalidation dosyası
④ 60 yeni sayfa yaz — İngilizce, doğrudan          24 + 20 + 16
⑤ final görevi kapat                               The Cartographer's Seal · 5 sayfa
⑥ arka maddeyi yaz                                 6 bölüm · 14 sayfa
⑦ cevap anahtarını üret                            120/120 · KORUMALI
⑧ bir kapı daha doğur                              qa_answerkey · 25 denetim
⑨ sayfa modelini ALTI bölgeyle ölç                 3/6 → 6/6
⑩ bağımsız editoryal kırmızı takımı koştur         iç inceleme · çocuk testi DEĞİL
```

**Yazılmayan:** ön madde, görsel varlıkları, dizgi, KDP paketi. Yol
haritası bunları Faz 5–6'ya veriyor ve bu faz sınırı aşmadı.

---

## 2 · A11 kararı — ve neden 80'i 60 yapmak YETMEZDİ

Kurucu talimatı § 2 açıktı: Faz 3 kapı eşiği **60**'tır, 80 değil; 80
*"tutarsız bir artık gerekliliktir."* Karar **K29** olarak kayda geçti.

| Kapı | Alan | **ESKİ** | **YENİ** | Kaynak |
|---|---|---:|---:|---|
| `phase3` | `activitiesLocked` / `Written` | **80** | **60** | ⭑ kurucu onayı |
| `phase2` | `activitiesLocked` / `Written` | 20 | **16** | türetme sonucu |
| `phase4` | her ikisi | 120 | 120 | değişmedi |

**Eski değerler silinmedi.** `project_config § gates.requirementsHistory`
onları makine okunur biçimde taşıyor ve `validate_spec § ⑥(g)` kaydın
silinmesini kırmızı yakıyor.

### 2.1 · Kök neden: 80 bir hata değil bir ARTIKTI

Merdivenin tamamı bootstrap'ın **"6 bölge × 20 aktivite"** varsayımından
elle türetilmişti: `20 · 40 · 60 · 80 · 100 · 120`. Faz 1 o varsayımı
yıktı ve kotaları **arza göre eşitsiz** kurdu (**K18**):

```
16 · 20 · 24 · 24 · 20 · 16  =  120
```

Eşitsiz kotalarla *"üç bölge"* otomatik olarak 60 etmez ve *"bir bölge"*
20 etmez. O günden sonra merdivenin her basamağı bir **tahmindi** ve iki
basamağı yanlıştı.

> ### Bir düzeltme, düzelttiği kusurun TEKRARINI engellemiyorsa bir düzeltme değil bir ERTELEMEDİR.

Bu yüzden eşik artık okunmuyor, **türetiliyor**:

```
gates.productionPlan[faz]  ×  scope.regionsHypothesis[].activityQuota
       →  kümülatif toplam  ==  gates.requirements[faz].activitiesLocked
```

`validate_spec § ⑥` türetmeyi her koşuda yeniden hesaplıyor. Config'teki
sayılar artık bir **kopyadır** ve kopya sürüklenirse kapı hangi basamağın
hangi yönde kaydığını söylüyor.

### 2.2 · `phase2` 20 → 16 — kurucunun sorusunda ADI GEÇMEDİ

Bu şeffaflık gerektiriyor ve rapor onu gizlemiyor. Kurucu **phase3**'ü
sordu ve **phase3**'ü yanıtladı. `phase2` aynı artığın bir basamak
aşağısıdır: pilot bölgesi `jaguar-condor`'un kotası **16**'dır (K18) ve
Faz 2 gerçekten 16 sayfa yazdı. Eski 20, Faz 2 tamamlandığı gün kapıyı
**yanlış yere** kırmızı yakardı — bir *yanlış-kırmızı*ydı ve yanlış-kırmızı
yanlış-yeşil kadar zarar verir: kapıya olan güveni bitirir.

`requirementsHistory` iki alanı **ayrı** tutuyor:
`founderApproved: ["phase3"]` · `derivedConsequence: ["phase2"]`.
Bir kurucu talimatıyla geri alınabilir.

### 2.3 · Yol haritası da düzeltildi — silinerek değil, ANNOTE EDİLEREK

Yol haritasının özet tablosu bir kez `20 · 60 · 40` diyordu ve **üçü de**
aynı bootstrap varsayımından geliyordu. Tablo düzeltildi, eski sayılar
üstü çizili olarak **görünür bırakıldı** ve düzeltmenin gerekçesi tablonun
altına K29 kutusu olarak kondu.

Artık **altı kaynak aynı şeyi söylüyor**: yol haritası, `project_config`,
`validate_spec`, `selftest`, `DECISIONS`, `CHANGELOG`.

### 2.4 · Kanıt — `selftest § ⑰`

| Kurgu | Beklenen | Sonuç |
|---|---|---|
| **eski 80 geri yazılır** | ⭑ KIRMIZI | ✅ |
| eski 20 geri yazılır | KIRMIZI | ✅ |
| bir bölge iki fazda üretilir | KIRMIZI | ✅ |
| bir bölge hiç planlanmaz | KIRMIZI | ✅ |
| **kota değişir, eşik değişmez** | ⭑ KIRMIZI | ✅ |
| eşik geri gider | KIRMIZI | ✅ |
| tarihî kayıt silinir / ESKİ değer düşürülür | KIRMIZI | ✅ |
| üretim planı silinir | KIRMIZI | ✅ |
| **temiz türetilmiş config** | **YEŞİL** | ✅ |

Beşincisi denetimin asıl işidir: mimari kayarsa kapı da kayar, **sessizce
ayrılmazlar**.

---

## 3 · A10 çocuk testi durumu

| | |
|---|---|
| Testçi | ✅ **2** — kurucu beyanı (A7 → K26) |
| Test paketi | ✅ hazır · Türkçe 16 sayfa · depo dışı |
| **Yapılan oturum** | **0** |
| Üretilen sahte kayıt | **0** |
| `CHILD_TEST_LOG.md` | ✅ var · **boş** |
| `externalValidation` | ⏳ **`pending`** |
| A10 | **AÇIK** — K27 ile ertelendi, K30 ile Faz 4'e uzatıldı, **kapanmadı** |

> ### ÇOCUK DOĞRULAMASI: YAPILMADI.

Bu satır bu raporun en önemli satırıdır. Aşağıdaki her *"doğrulandı"*
sözcüğü **İÇ / TEKNİK DOĞRULAMA** anlamındadır:

```
① proje-testli tasarım kuralları       ✅ uygulandı
② İngilizce okunabilirlik kalibrasyonu ✅ ölçüldü
③ iç editoryal inceleme                ✅ koşturuldu
④ mekanik çözülebilirlik               ✅ 120/120
⑤ güvenlik kapıları                    ✅ yeşil
⑥ ilerleme ve kurtarma kapıları        ✅ yeşil
⑦ cevap anahtarı kapısı                ✅ yeşil
────────────────────────────────────────────────────
   ÇOCUK DOĞRULAMASI                   ❌ YAPILMADI
```

Kurucu talimatı § 3 bunu ayrıca şart koşuyor ve rapor ona uyuyor: A10
**PASS · CLOSED · COMPLETED · VERIFIED** olarak işaretlenmedi. `.gate`
`phase1`'de kaldı ve `validate_spec § ⑤` onu oraya kilitliyor.

**Yüz yirmi sayfanın tamamlanması sıfır çocuk oturumunu bir çocuk oturumu
yapmaz.** `phaseOverride.doesNotImply` listesine bu cümle beşinci madde
olarak eklendi.

---

## 4 · The Northern Ice — 24 sayfa

| Eksen | Ölçülen | Şart |
|---|---|---|
| Tip | cipher 6 · sort 7 · observe 5 · map 3 · make 3 | asgari 3/4/2/2/2 ✅ |
| Zorluk | ★10 · ★★10 · ★★★4 | profil {10,10,4} ✅ **tam** |
| Kültür | norse 8 · finnish 6 · irish 6 · inuit 4 | kota ✅ **tam** |
| Güvenlik | safe **24** · safe-with-adult 0 | ≥%90 ✅ |
| Açık uçlu | 3 (%12,5) | yalnızca `make` ✅ |
| Düzen | **9 ayrı** | ≥3 ✅ |
| Mühür | 5 yuva · **FROST** | ✅ |

Bölgenin ekseni **yazı**: dört halkın dördü de ayrı bir yazı dizgesi
taşıyor — Inuktitut hecelemesi, Genç Futhark, ogham ve Fince ünlü uyumu.
Bölge açılışı dördünü tek cümlede karşılaştırıyor ve hiçbirini "kod"
diye adlandırmıyor.

### 4.1 · Bölgenin en iyi sayfası ve neden

`norse-futhark-key` çocuğa bir belirsizliği **yaşatıyor**: on altı rün
yirmi dört sesi taşımak zorunda, `ᚴ` hem k hem g demek, ve şerit hem
KORM hem GORM okunabiliyor. Çocuk ikisini de yazıyor, sonra Jelling
taşları hakkındaki basılı bilgiyle ayırıyor. Sayfa bir şifre değil bir
**yazı sistemi problemi** öğretiyor.

---

## 5 · The Middle Sea — 20 sayfa

| Eksen | Ölçülen | Şart |
|---|---|---|
| Tip | cipher 5 · observe 5 · map 4 · sort 4 · make 2 | asgari ✅ |
| Zorluk | ★8 · ★★8 · ★★★4 | profil {8,8,4} ✅ **tam** |
| Kültür | greek 9 · mesopotamian 6 · egyptian 5 | kota ✅ **tam** |
| Güvenlik | safe **20** · safe-with-adult 0 | ✅ |
| Açık uçlu | 2 (%10) | yalnızca `make` ✅ |
| Düzen | **10 ayrı** — kitabın tamamı | ≥3 ✅ |
| Mühür | 6 yuva · **SCRIBE** | ✅ |

Bu bölge on düzenin **onunu birden** kullanan tek bölge ve bu bir kaza
değil: üç kültür de yazının doğduğu yer ve üçü de farklı bir levha
istiyor — kama, kartuş, alfabe.

---

## 6 · Sun and Savanna — 16 sayfa

| Eksen | Ölçülen | Şart |
|---|---|---|
| Tip | cipher 4 · sort 4 · observe 3 · make 3 · map 2 | asgari ✅ |
| Zorluk | ★6 · ★★7 · ★★★3 | profil {6,7,3} ✅ **tam** |
| Kültür | akan 7 · yoruba 5 · zulu 4 | kota ✅ **tam** |
| Güvenlik | safe **16** · safe-with-adult 0 | ✅ |
| Açık uçlu | 3 (%18,8) | yalnızca `make` ✅ |
| Düzen | **9 ayrı** | ≥3 ✅ |
| Mühür | 7 yuva · **MESSAGE** | ✅ |

`region_index § sun-savanna` bir uyarı taşıyor: *"'Afrika mitolojisi'
diye bir bölüm YOKTUR. Üç kültür kendi adıyla anılır."* Bölge açılışı
üçünü **ilk cümlede adıyla** sayıyor ve bölge boyunca "Afrika" sözcüğü
bir kez bile bir kültür adı yerine kullanılmıyor.

Bu, yazımın en kısıtlı bölgesiydi ve kısıt **bir tasarım girdisi** oldu:
üç daraltmanın üçü de kültürel sınırdan geldi ve üçü de sayfayı
zayıflatmadı (§ 10.1).

---

## 7 · 120 aktivite — kümülatif durum

| Bölge | Kota | Yazılan | Mühür | Düzen |
|---|---:|---:|---:|---:|
| north-ice | 24 | **24** | 5 · FROST | 9 |
| middle-sea | 20 | **20** | 6 · SCRIBE | 10 |
| sun-savanna | 16 | **16** | 7 · MESSAGE | 9 |
| monsoon | 24 | 24 | 7 · MONSOON | 6 |
| great-ocean | 20 | 20 | 6 · VOYAGE | 8 |
| jaguar-condor | 16 | 16 | 6 · CONDOR | 5 |
| **toplam** | **120** | **120** | **37** | — |

**22 kültürün 22'si temsil ediliyor** ve hiçbiri tek sayfalık değil:
en az 3 (andean · hawaiian · hindu), en çok 9 (greek).

Alt başlıktaki **120** ve **22** artık ölçülmüş vaatlerdir ve
`validate_spec § check_gate_scope` onları `phase4`+ kapılarında sert
denetliyor.

---

## 8 · Araştırma doğrulaması

**51 yeni iddia · 108 kümülatif · 23 devralma kaydı yükseltildi.**

| Verdict | Faz 2 | Faz 3 | **Faz 4** | Toplam |
|---|---:|---:|---:|---:|
| `confirmed` | 10 | 39 | **43** | 92 |
| `corrected` | 3 | 3 | **7** | 13 |
| `rejected` | 0 | 0 | **3** | **3** |

| Devralma durumu | Faz 2 | Faz 3 | **Faz 4** |
|---|---:|---:|---:|
| `inherited-provisional` | 69 | 45 | **22** |
| `inherited-verified` | 7 | 31 | **54** |

Kayıtlar: `north-ice-revalidation.json` (21) · `middle-sea-revalidation.json`
(18) · `sun-savanna-revalidation.json` (12). Üçü de **depoda durur** ve
içlerinde **cevap yoktur**.

### 8.1 · Faz 4'ün kendi dersi

> ### Bir iddia doğru olabilir, cevap üretebilir — ve yine de METNİ EKSİK olabilir.

Faz 2 *"kayıt doğrulamak ile iddia doğrulamak aynı şey değildir"* dedi.
Faz 3 *"bir iddianın doğruluğu ile bir cevabın dayanağı olabilmesi aynı
şey değildir"* dedi. Faz 4 bir kat daha indi:

**Üç iddia yanlış değildi. Üçü de KANONİK ya da TAM değildi.**

### 8.2 · Üç reddedilen iddia

#### ① Yggdrasil'in "dokuz dünyası" — **KANONİK LİSTE YOK**

Eski Norse kaynakları dokuz dünyadan **söz eder** ama hiçbiri dokuzunu
birlikte **saymaz**: Völuspá sayıyı anar, adları vermez; Snorri de tam
bir liste kurmaz. Dolaşımdaki listeler ikincil derlemelerdir ve
birbirinden farklıdır.

`norse-nine-worlds-map` dört ipucundan dokuz dünyayı yerleştirtecekti.
Sayfa çocuğa **ikincil bir derlemeyi birincil kaynak diye** öğretirdi.
Düştü; yerine aynı bölge × aynı kültürden `norse-apples-sequence` geçti.
Bölgenin harita sayısı 4 → 3 düştü, **asgari 2 korundu**.

#### ② Etana'nın yükseliş yükseklikleri — **METİN EKSİK**

Aday `mesopotamian-eagle-height-plate` dört yüksekliği "yeryüzü şuna
benzer" betimlemeleriyle eşleştirecekti. Britannica destanın olay
örgüsünü veriyor ve şunu **açıkça** söylüyor: *"the result of Etana's
quest is uncertain because of the incomplete state of the texts."*
Yükseklik pasajlarına iki bağımsız erişilebilir kaynakta ulaşılamadı.

Sayfa düştü. **MÜHÜR YUVASI 6 TAŞINDI:**
`mesopotamian-seal-cylinder-plate` yuvayı devraldı
(`PROGRESSION_ARCHITECTURE § 6`: yuva kalıcı, sakini değiştirilebilir).

#### ③ Tabletlerin yakalama-satırı düzeni — **DOĞRULANAMADI**

Destanın on iki tablet üzerinde durduğu ve on birincisinin Tufan tableti
olduğu doğrulanıyor (Britannica · British Museum K.3375). Ama
*"her tablet bir sonrakinin ilk satırıyla biter"* düzeninin kendisi iki
bağımsız erişilebilir kaynakta bulunamadı. `mesopotamian-tablet-order`
düştü; yerine `mesopotamian-two-rivers-map` geçti ve bölge zorluk
profili `greek-god-domains` (★) → `greek-vase-plate` (★★) takasıyla
yeniden dengelendi.

> **Bir sayfa düşünce yalnızca o sayfa düşmez: profil, kota ve tip
> asgarileri birlikte yeniden çözülür.** 168'lik havuz tam olarak bunun
> için var.

### 8.3 · Yedi düzeltme

| Sayfa | Neydi | Ne oldu |
|---|---|---|
| `finnish-kantele-strings` | *"telleri say"* | tel sayısı **değişken** (5·8·10·12·39) → iki kökeni okutuyor |
| `irish-swans-count` | *"kuşları say ve grupla"* | bir **sayma alıştırmasıydı**, kültürel bilgi taşımıyordu (K4) → CELT'in üç suyu |
| `greek-labyrinth-cipher` | *"labirentin tek yolu vardı"* | tek yollu olan **madenî para tasarımıdır**, edebî betimlemeler çelişir |
| `greek-seasons-six-seeds` | bir **sayı** vaat ediyordu | süre kaynağa göre değişiyor (üçte bir / dört ay / altı ay) → hiçbir sayı cevap değil |
| `egyptian-boat-plate` | *"nehir teknesinde omurga yoktur"* | doğrulanamadı → yalnızca **sayılabilir** olan soruluyor |
| `akan-story-trade` | **dört** yaratık | erişilen iki kaynak **üç** veriyor → dördüncüsü girmedi |
| `yoruba-counting-to-twenty` | Yoruba **sayı adları** | birebir yazımlar doğrulanamadı → **yöntem** sınanıyor |

### 8.4 · Yöntem dürüstlüğü

Kaynaklar ağ üzerinden okundu. Bir künye **yalnızca** o sayfanın ilgili
cümlesi görüldüğünde yazıldı. Britannica doğrudan çekmeyi reddediyor
(HTTP 403); o sayfaların ilgili cümleleri arama katmanının döndürdüğü
alıntılardan okundu ve künyeye **`accessVia: search-snippet`** ile geçti.
ETCSL'de aranıp **bulunamayan** Etana pasajı da künyeye **negatif sonuç
olarak** yazıldı.

> **Okunmamış bir kaynağı kaydetmek uydurmadır ve yapılmadı.**

Kurum künyeleri: UNESCO · Danimarka Milli Müzesi · Historiska museet ·
Roskilde Viking Gemi Müzesi · Viking Society for Northern Research (UCL) ·
British Museum · Metropolitan Museum · Penn Museum · Smithsonian
(Folkways · NMAH · Chandra) · Ashmolean · Heritage Ireland (OPW) ·
DIAS Ogham in 3D · CELT (UCC) · dúchas.ie (UCD) · UCL Digital Egypt ·
Kalevalaseura · Suomalaisen Kirjallisuuden Seura · Finna / Suomen
kansallismuseo · Jyväskylä · Tampere · Helsinki · SOAS · Cambridge
University Press · SIL Global · Gana Üniversitesi · KwaZulu-Natal
Üniversitesi · South African History Online · Inuit Tapiriit Kanatami ·
Nunavut Hükûmeti · Parks Canada · Tusaalanga · Britannica.

---

## 9 · Aktivite tipi dağılımı

| Tip | Faz 3 (60) | **Faz 4 yeni (60)** | **Kümülatif (120)** | Oran | Havuz |
|---|---:|---:|---:|---:|---:|
| `cipher` | 19 | **15** | **34** | %28,3 | %24,4 |
| `sort` | 15 | **15** | **30** | %25,0 | %25,6 |
| `observe` | 10 | **13** | **23** | %19,2 | %20,8 |
| `map` | 9 | **9** | **18** | %15,0 | %14,3 |
| `make` | 7 | **8** | **15** | %12,5 | %14,9 |

Faz 3 raporu bir öngörüde bulunmuştu: *"cipher oranı havuzun üstünde;
Faz 4'ün üç bölgesi dizge açısından daha hafif."* **Öngörü tuttu ama
tam tutmadı.** `cipher` %31,7 → **%28,3**'e indi, havuz oranına yaklaştı
ve hâlâ üstünde. Sebep içerikten geliyor: Faz 4'ün üç bölgesi de yedi
ayrı yazı dizgesi taşıyor (Inuktitut hecelemesi, Genç Futhark, ogham,
Yunan alfabesi, hiyeroglif, çivi yazısı, Yoruba diakritikleri) ve
*"bir şifre süs değildir"* (K4) her dizgeyi en az bir kez okutmayı
zorunlu kılıyor.

`observe` %16,7 → **%19,2** ile havuz oranına oturdu ve bu bilinçliydi:
Faz 4'ün üç bölgesi müze nesnesi bakımından zengin (rün taşı, kartuş,
silindir mühür, altın ağırlığı).

**Faz 4'ün 60 sayfası kendi içinde daha dengeli:** cipher 15 · sort 15 ·
observe 13 · map 9 · make 8. Faz 3'ün cipher ağırlığı tekrarlanmadı ve
kurucu talimatı § 9 tam olarak bunu istiyordu.

---

## 10 · Kültürel bütünlük ve kısıtlar

Faz 4 üç Kademe A, bir Kademe B ve bir Kademe C kültürüyle çalıştı.
Kısıtlar **bir tasarım girdisi** olarak kullanıldı, bir engel olarak değil.

### 10.1 · Uygulanan daralmalar

| Sayfa | Kültür | Ne çıkarıldı | Gerekçe |
|---|---|---|---|
| `inuit-*` (4 sayfa) | inuit · **Kademe C** | avlanma tekniği · şaman uygulaması | `culture_index` yasak biçim 2–3 |
| `norse-binding-riddle` | norse | kurdun bağlanması · Týr'ın el kaybı | yasak biçim 1 · AGE_POLICY § 2 |
| `norse-who-owns-what` | norse | Loki'nin bahis bedeli | AGE_POLICY § 2 çerçeve 4 |
| `irish-name-changes` | irish | köpeğin öldürülmesi · *ríastrad* | yasak biçim 1 |
| `irish-swans-count` | irish | üvey anne zulmü | yasak biçim 2 |
| `greek-seasons-six-seeds` | greek | kaçırılma anı | yasak biçim 1 |
| `egyptian-cartouche-key` | egyptian | mumyalama · mezar | yasak biçim 2 |
| `mesopotamian-plant-quest-steps` | mesopotamian | Enkidu'nun ölümü ve yas | AGE_POLICY § 2 |
| `yoruba-river-map` | yoruba · **Kademe B** | tanrıça · tapınma · sunu · tören | yasak biçim 2–3 |
| `yoruba-*` (5 sayfa) | yoruba | **kutsal ad hiçbir şifrenin cevabı değil** | yasak biçim 3 |
| `akan-spider-draw` | akan | çocuğa sembol tasarlatma | yasak biçim 1 |
| `akan-goldweight-plate` | akan | Adinkra ile karıştırma | yasak biçim 2 |
| `zulu-two-messengers` | zulu | ölümün sahnelenmesi | biçim daraltması (K13 § ①) |
| `zulu-click-letters` | zulu | telaffuz taklidi istemek | dille alay riski |

**Hiçbir daraltmada kültür, hikâye veya kota düşürülmedi** — K13 § ①
daralma sırasının yalnızca **ilk basamağı** (biçim daraltma) kullanıldı.

### 10.2 · Kademe C ebeveyn notları

`qa_age § ⑩` Kademe C sayfalarının ebeveyn notu taşımasını şart koşuyor.
Faz 4'ün dört inuit sayfasının dördü de not taşıyor; kitap genelinde
**17 sayfa** ebeveyn notu taşıyor (13 Kademe C + 4 `safe-with-adult`).

### 10.3 · Atıf

`qa_age § ⑨` — atıf gereken **80/80** sayfada kültürün adı çocuğun
gördüğü field note'ta geçiyor.

---

## 11 · Güvenlik

| Sınıf | Sayfa | Oran | Hedef |
|---|---:|---:|---:|
| `safe` | **116** | %96,7 | ≥%90 ✅ |
| `safe-with-adult` | **4** | %3,3 | ≤%10 ✅ |
| `do-not-use` | **0** | %0 | 0 ✅ |

**Faz 4'ün 60 sayfasının 60'ı `safe`.** Bu bir hedef değildi ve zorlanmadı:
üç bölgenin malzemesi (yazı dizgeleri, müze nesneleri, coğrafya) doğal
olarak malzemesiz çalışıyor. Kitabın dört `safe-with-adult` sayfasının
dördü de Faz 2–3'ten geliyor.

---

## 12 · İngilizce okunabilirlik

Ölçüm **120 İngilizce sayfa** üzerinde yapıldı.

| Register | Faz 2 (16) | Faz 3 (60) | **Faz 4 (120)** | Bant |
|---|---:|---:|---:|---|
| Talimat | 6,64 · FK 1,28 | 6,77 · FK 1,92 | **7,91 · FK 2,53** | 5–11 · ≤4,0 ✅ |
| Field note | 10,94 · FK 3,87 | 11,73 · FK 4,68 | **12,40 · FK 5,39** | 9–14 · 3,0–5,9 ✅ |
| **Değişmez** | 1,28 < 3,87 | 1,92 < 4,68 | **2,53 < 5,39** | fk(tal) < fk(note) ✅ |

| Ölçüt | Faz 4 | Bant |
|---|---:|---|
| En uzun talimat cümlesi | **17** | ≤18 ✅ |
| Bölge açılışları | 6 açılış · hepsi bantta | 120–170 kelime ✅ |
| Ticari dize | **814** | %100 İngilizce ✅ |

**Üç register de yine yukarı kaydı.** Sebep aynı ve beklenen: Faz 4'ün
kültürleri daha uzun özel adlar taşıyor (qaniujaaqpait, Derravaragh,
Osun-Osogbo, Skíðblaðnir, abrammuo) ve bunlar **field note'ta** durur,
talimatta değil. Değişmezin arası Faz 3'te 2,76 sınıftı, şimdi **2,86** —
yani açılıyor, kapanmıyor.

Field note FK'si 5,39 ile bandın üst yarısında ve **bu izleniyor**: bant
5,9'da bitiyor. Faz 5 ön madde yazarken bu sayı bir kez daha ölçülmeli.

`STYLE.md` **v1.2**'de kaldı. **v2.0 numarası ilk gerçek çocuk oturumuna
ayrılmıştır** (K23) ve Faz 4 o numaraya dokunmadı.

---

## 13 · Çözülebilirlik

`qa_solvable.py` · sekiz denetim · **120/120**

| # | Denetim | Sonuç |
|---|---|---|
| ① | Açık uçlu olmayan her sayfanın cevabı var | **105/105** ✅ |
| ② | `openEnded` yalnızca `make` tipinde | **15/15** ✅ |
| ③ | Açık uçlu sayfa **ölçülebilir** ölçüt taşıyor | 15/15 ✅ |
| ④ | Belirsiz dil (*or · may vary · about N*) | **0** ✅ |
| ⑤ | İpucu cevabı içermiyor | 50 ipucu ✅ |
| ⑥ | Cevap alanı kalabalık değil | ✅ |
| ⑦ | Mühür harfi yeniden hesaplandı | **37/37** ✅ |
| ⑧ | Field note cevabı söylemiyor | 120/120 ✅ |

Açık uçlu oran **%12,5** (15/120) ve hepsi `make`. Mühür besleyen hiçbir
sayfa açık uçlu değil.

---

## 14 · Talimat QA

`qa_instruction.py` · dokuz denetim · **120/120** — talimat kalıbı, emir
kipi, adım sayısı, adım birliği, öncülsüz zamir, yazma alanı ve
**belirtili gönderme** (`pagePrints`, 568 madde).

★ sayfalarının hiçbiri iki adımı aşmıyor (45 sayfa denetlendi) ve hiçbir
sayfa dört adımı aşmıyor.

---

## 15 · İlerleme ve kurtarma

| Mekanizma | Ölçülen |
|---|---|
| **Hasar yarıçapı 1** — bir yuvayı tam bir aktivite besler | ✅ 37/37 |
| **Zincir yok** — hiçbir sayfa başka bir sayfanın cevabına bağlı değil | ✅ 0 |
| **Sözcük anlamlı** — yanlış harf sözcüğü bozar, çocuk hangi sayfaya döneceğini bilir | ✅ 6/6 |
| **Final görev kurtarması** — altı kare, altı bölge, bir kare bir bölge | ✅ |

`qa_progression.py` · yedi denetim · yeşil · **37 yuva**.

⚠ Kapı hiçbir mühür sözcüğünü ekrana **basmaz**.

### 15.1 · Ölçülen bonus korunuyor

**37 mühür harfinin yalnızca 6'sı** (%16,2) final göreve taşınıyor. Yani
bir bölgede yapılan bir hata final cevabı **çoğu zaman hiç etkilemez** —
ve etkilediğinde, hangi bölgeye dönüleceğini kare numarası söyler.

---

## 16 · Mühür sistemi — 37/37 tamam

| Bölge | Yuva | Çentik | Faz |
|---|---:|---:|---|
| jaguar-condor | 6 | 3 | Faz 2 |
| monsoon | 7 | 4 | Faz 3 |
| great-ocean | 6 | 2 | Faz 3 |
| **north-ice** | **5** | 4 | ⭑ **Faz 4** |
| **middle-sea** | **6** | 6 | ⭑ **Faz 4** |
| **sun-savanna** | **7** | 5 | ⭑ **Faz 4** |
| **toplam** | **37** | 6 | ✅ **yapı bütün** |

Faz 4 **18 yeni yuva** doldurdu ve mimariye tek bir satır eklemedi:
her yuva bir aktiviteden, her harf bir cevaptan, her çentik bir konumdan
mekanik olarak çıkıyor. **Hiçbir mühür harfi elle yazılmadı.**

### 16.1 · Bir yuva taşındı

`mesopotamian-eagle-height-plate` reddedilen bir iddiaya dayandığı için
düştü ve **yuva 6** `mesopotamian-seal-cylinder-plate`'e taşındı. Bu
Faz 3'te de bir kez olmuştu (`korean-sky-rope-plate`) ve mimarinin
öngördüğü davranıştır: **yuva kalıcı, sakini değiştirilebilir.**

---

## 17 · Tasarım dizgesi

`00_CONTEXT/DESIGN_SYSTEM.md` **v1.0** — Faz 3'te donduruldu ve Faz 4
**tek bir satırını değiştirmedi**. On modül, on düzen, kapalı liste.

| Bölge | Sayfa | Ayrı düzen |
|---|---:|---:|
| jaguar-condor | 16 | 5 |
| monsoon | 24 | 6 |
| great-ocean | 20 | 8 |
| **north-ice** | 24 | **9** |
| **middle-sea** | 20 | **10** |
| **sun-savanna** | 16 | **9** |

`qa_design § ⑥` her bölgeden en az üç ayrı düzen istiyor; en düşük bölge
**beş** kullanıyor. Faz 4'ün üç bölgesi düzen çeşitliliğinde kitabın en
zenginleri ve `middle-sea` **onun onunu birden** kullanıyor.

> **Yapı tutarlılığı korundu, kültürel homojenlik oluşmadı.**

---

## 18 · pagePrint kapsamı

| | Faz 2 | Faz 3 | **Faz 4** |
|---|---:|---:|---:|
| `pagePrints` maddesi | 67 | 255 | **568** |
| Kapsanan sayfa | 16/16 | 60/60 | **120/120** |
| Sayfa başına ortalama | 4,2 | 4,25 | **4,73** |

Faz 4'ün 60 sayfası da `pagePrints` ile **birlikte** yazıldı, sonra
değil — Faz 3 § 16'nın dersi uygulandı ve tekrar etmedi.

---

## 19 · Görsel şartnameleri

**120 şartname · 700 zorunlu etiket · 0 üretilmiş varlık.**

Her sayfa on beş alanlık bir `visualSpec` taşıyor. `requiredLabels` elle
yazılmadı, **levhadan türetildi**.

Faz 4'ün şartnameleri bir şey daha yapıyor: **cevabın gözlemlenebilir
olmasını mekanik olarak şart koşuyor.** Örnekler:

- *"Exactly twelve overlapping strakes must be countable on the near side."*
- *"Each impression must be the exact mirror of its stone."*
- *"The four story constellations must be drawn adjacent; Orion and Ursa Major must be clearly distant."*
- *"The contours over sentences 1 and 4 must be the closest pair on the page."*

> **Bir cevap ölçülebilir diye yazıldıysa, görsel şartnamesi o ölçümü
> MÜMKÜN KILMAK ZORUNDADIR.** Faz 5 bu satırları okumadan görsel
> üretemez ve üretirse sayfa çözülemez hâle gelir.

### 19.1 · Şartname bir varlık değildir

`BOOK_STATS.md` ikisini **ayrı satırlarda** sayıyor: *görsel şartnamesi*
**120**, *görsel varlık (üretilmiş)* **0**. Kurucu talimatı § 16 bunu
şart koşuyor ve rapor ona uyuyor.

---

## 20 · qa_design

`qa_design.py` · **19 denetim · yeşil** · 120 şartname · 700 etiket.

Faz 3'ün § 21.1 dersi (*"bir kapı bir sınıfı kapatır, komşusunu değil"*)
Faz 4'te bir kez daha ısırdı: `§ ⑧` eşleştirme ilişkisi denetimi Faz 4
yazımı sırasında **dört sayfada** kırmızı yandı ve dördü de gerçek
kusurdu — cevabın bir parçası levhada basılı değildi.

Kapı ayrıca **altı uyarı** üretti (*"ilişki tek bir maddede durmuyor"*).
Altısı da bakıldı ve altısı da meşru **çıkarım tasarımı** çıktı: örneğin
`norse-weekday-names`'te çocuk *"Woden"*u *"Wednesday"*in **içinde**
görmek zorunda ve bu sayfanın dersinin kendisidir. Uyarı doğru yerde
durdu ve bir insan baktı.

---

## 21 · qa_echo

`qa_echo.py` · **7 denetim · yeşil** · 120 sayfa · en yüksek field note
örtüşmesi **0,33** (eşik 0,55).

Kapı Faz 4 yazımı sırasında **iki kez** kırmızı yandı ve ikisi de gerçek
kusurdu:

1. *"read the four event cards"* üç sayfada **birebir** yineleniyordu.
   Beyansız bir nakarattı ve üçü de yeniden yazıldı.
2. *"in this □ account…"* beş sayfada, **beş ayrı kültürde** field note
   açılış kalıbı olmuştu. Tam olarak kapının doğduğu kusur: beş kültür
   tek sesle konuşuyordu. Beşi de yeniden yazıldı.

> **İkincisi kapının varlık sebebidir ve tam da olacağı yerde oldu:**
> altıncı bölge yazılırken, yazarın kendi kalıbı otomatikleşmişken.

Kapı hiçbir zorunlu kültürel terimi cezalandırmadı — `selftest § ⑮`'in
yanlış-pozitif testi hâlâ geçiyor.

---

## 22 · Final görev — The Cartographer's Seal

**5 sayfa. Yeni bir mekanik icat edilmedi.**

Kurucu talimatı § 20 bunu açıkça şart koşuyordu: *"Do NOT invent a
separate final game unrelated to the current seal architecture."* Final
görev **K18'de dondurulan** mimariyi kapatıyor:

```
① The Route                — altı mühür rota sırasına konur
② The Notch                — çentik numarası ve sözcük uzunluğu okunur
③ The Cartographer's Seal  — altı kare, altı harf, bir sözcük
④ The Great Sorting Table  — 22 kültür × 6 motif, çocuk doldurur
⑤ Field Researcher         — ad, tarih, tamamlanan bölge sayısı
```

| Şart (kurucu talimatı § 20) | Durum |
|---|---|
| bölgesel ilerlemeyi sentezler | ✅ altı bölgenin altısı |
| yalnızca meşru kazanılmış bilgiyi kullanır | ✅ altı mühür sözcüğü çocuğun kendi yazdığı |
| cevabı erken açmaz | ✅ sözcük hiçbir yerde basılı değil |
| mekanik olarak belirlenimci | ✅ `qa_progression § ②③④` |
| anlamlı bir kapanış verir | ✅ sözcük kitabın tezidir |
| yeni bir bağımlılık sistemi getirmez | ✅ mevcut çentik mekaniği |
| *"bir hata kitabı yok etmez"* özelliğini korur | ✅ § 22.1 |

### 22.1 · Kurtarma — final görevde de yarıçap 1

Altı kare, altı bölge, **bir kare bir bölge**. Bir harf yanlışsa:

- sözcük **anlamlı** olduğu için çocuk bunu **kendi görür**,
- kare **numaralı** olduğu için hangi bölgeye döneceğini **bilir**,
- diğer beş kare **etkilenmez**.

Sayfa bunu ayrıca **basıyor**: *"if the six letters do not make a word you
know, one seal is wrong and the square tells you which region to go back
to."* `qa_answerkey § ⑦` bu şeridin sayfadan düşmesini kırmızı yakıyor
ve `selftest § ⑱(g)` düşürülmüş bir şeridin yakalandığını kanıtlıyor.

### 22.2 · Büyük tasnif tablosu

Yol haritası bunu *"22 kültürün ortak motifleri — doldurulacak boş
tablo"* diye istiyor. Tablo **22 satır × 6 sütun** ve altı sütun başlığı
kitabın gerçekten öğrettiği altı şey:

> bir yazı dizgesi · su üzerinde bir yolculuk · yılın dönüşü hakkında bir
> hikâye · adı olan gerçek bir yer · bir sayma dizgesi · yol alması
> gereken bir mesaj

Tablo **boş basılıyor** ve altyazısı bir şey daha söylüyor: *"an empty
row is a real result too."* Bir kültürün bir sütunda ticksiz kalması bir
başarısızlık değil bir **ölçümdür**.

---

## 23 · Arka madde

**14 sayfa · 6 bölüm.** Yol haritası Faz 4 § 2'nin adıyla istediği
dördü de var (kademeli ipuçları · cevap anahtarı · kültür sözlüğü ·
World Myths köprü sayfası).

| Bölüm | Sayfa | İşi |
|---|---:|---|
| `how-to-use` | 2 | rota, yıldız kutusu ve mühür yuvası **bir kez** anlatılır |
| `hint-rule` | 1 | ipucu bir başarısızlık değil bir basamaktır |
| `glossary` | 4 | **22 kültür**, her biri kendi adıyla, yazı dizgesiyle, yaşayan mı |
| `sources` | 2 | kurumlar bölgeye göre — okur kitabı **denetleyebilsin** |
| `answer-key` | 4 | her kapalı cevap bir kez, sayfa sırasında |
| `world-myths-bridge` | 1 | köprü sayfası · fiyat yok, sipariş yok, **tek kez** |

**Sayfa sayısı için hiçbir bölüm eklenmedi.** `qa_answerkey § ⑧` her
bölümün gerekçesini denetliyor ve `selftest § ⑱(i)` gerekçesi boşaltılmış
bir bölümün yakalandığını kanıtlıyor.

### 23.1 · `sources` bölümü ne yapıyor

Bu bölüm kitabın en alışılmadık arka madde parçası ve bilinçli: bir
çocuk kitabının kaynaklarını **okura göstermesi** yaygın değildir. Bölüm
üç şey basıyor:

- kurumlar, bölgeye göre gruplanmış
- *"her cevap en az iki tanesine karşı denetlendi"*
- **ve neyin dışarıda bırakıldığı:** *"üç iddia iki kez denetlenemedi ve
  onları gerektiren sayfalar yeniden tasarlandı."*

> **Bir kitap neyi bilmediğini söylerse, bildiği şeye güvenilir.**

### 23.2 · Cevap anahtarı — ve mühür sözcüklerinin yokluğu

Anahtar **120/120** kayıt taşıyor: 105 kapalı cevap + 15 açık uçlu
**ölçüt**. Açık uçlu bir sayfaya "doğru cevap" yazmak açık uçluluğu yok
etmek olurdu ve `qa_answerkey § ②` bunu kırmızı yakıyor.

**Anahtar altı mühür sözcüğünün hiçbirini basmıyor ve basmayacak.**
Gerekçe bir güvenlik gerekçesi değil bir **tasarım** gerekçesidir: mühür
sözcüğü çocuğun kendi kendini doğrulama aygıtıdır. Basılırsa kitabın tek
kendi kendini düzelten mekanizması ölür ve pes etme riski yükselir
(`BRIEF § 6.3`).

Anahtar **depoya girmez** (`.gitignore § ①b`).

---

## 24 · Yeni kapı — qa_answerkey

**25 denetim.** Yol haritası Faz 4 § 8 bu kapıyı adıyla istiyordu; Faz 4
onu iki yönde genişletti çünkü kitabın kapanışı **üç** parçadan oluşuyor
ve üçü de sessizce eksik kalabilir.

```
① kapsam  ② biçim  ③ eşleşme  ④ ipucu merdiveni  ⑤ mühür sessizliği
⑥ final görev  ⑦ kurtarma  ⑧ arka madde  ⑨ sözlük
```

### 24.1 · Kapı ilk koşusunda KENDİ kusurunu buldu — iki kez

**Birinci hâl** anahtarın metninde mühür sözcüğü aradı ve **dördünü
buldu**. Dördü de yanlış pozitifti: mühür sözcükleri sıradan İngilizce
sözcüklerdir ve bir cevapta meşru olarak geçerler (*"panel 2 the
voyage"*). Cevap anahtarı **yıldız** sözcüklerini taşır — sayfada zaten
basılı olanları — mühür sözcüğünü değil; mühür sözcüğü tek tek
**harflerden** kurulur ve hiçbir yerde bütün olarak durmaz.

**İkinci hâl** bölge adlarını sızıntı sandı. Oysa **iki mühür sözcüğü
bilerek kendi bölgesinin adını yankılar** — bu bir tasarım aygıtıdır ve
Faz 3 § 21.6'da bir inceleme bulgusuna karşı **açıkça savunulmuştu**.

> ### Bir sızıntı dedektörü, kitabın TASARIMINI bilmiyorsa tasarımı sızıntı sanar.

Ve tuzağın yönü Faz 3 § 20.1'in aynısıydı: kapıyı yeşile çevirmenin en
ucuz yolu cevaptan *"voyage"* sözcüğünü **silmek** olurdu — doğru
yazılmış bir cevabı bozmak.

### 24.2 · Daraltma bir gevşetme değildi: yerine gerçek bir değişmez kondu

`⑤c` — **hiçbir yıldız sözcüğü kendi bölgesinin mühür sözcüğü olamaz.**

Bu bir sızıntı değil bir **mekanik çöküş** olurdu: çocuk yıldız sözcüğünü
kutuya yazdığında mühür sözcüğünü kazara okur ve altı sayfalık toplama
işi **anlamsızlaşır**. **Hiçbir kapı bunu denetlemiyordu.**

`selftest § ⑱` on bir kusurlu kurgu koşturuyor ve sonuncusu bir
**yanlış-pozitif testidir**: bölge adını yankılayan bir mühür sözcüğü
**geçmek zorundadır** ve geçiyor.

---

## 25 · Sayfa modeli — altı bölge de gerçek

| Bölge | Kota | Ort. ağırlık | Kaynak | Aktivite s. | Yapı s. | Toplam |
|---|---:|---:|---|---:|---:|---:|
| jaguar-condor | 16 | **0,844** | ÖLÇÜLDÜ | 13,5 | 2 | 15,5 |
| great-ocean | 20 | **0,863** | ÖLÇÜLDÜ | 17,2 | 2 | 19,2 |
| monsoon | 24 | **0,865** | ÖLÇÜLDÜ | 20,8 | 2 | 22,8 |
| **north-ice** | 24 | **0,865** | ⭑ ÖLÇÜLDÜ | 20,8 | 2 | 22,8 |
| **sun-savanna** | 16 | **0,875** | ⭑ ÖLÇÜLDÜ | 14,0 | 2 | 16,0 |
| **middle-sea** | 20 | **0,887** | ⭑ ÖLÇÜLDÜ | 17,8 | 2 | 19,8 |

```
ön madde        8
bölgeler      116,0
final görev     5
arka madde     14
──────────────────
ham model     143,0  →  yuvarlanmış 143  →  forma hizalı 144
```

| | Hedef | Ölçülen |
|---|---:|---:|
| Sayfa | 148 | **144** (−%2,7 · bant ±%6 ✅) |
| Ciltsiz baskı | 3,52 $ | 3,45 $ |
| Ciltsiz telif | 5,48 $ | **5,55 $** |
| Başabaş ACOS | %36,5 | %37,0 |

### 25.1 · Faz 3'ün öngörüsü tuttu

Faz 3 üç ölçümle (0,844–0,865) *"kalan üç bölge de 0,857'de gelirse model
yine 144 eder"* demişti. Kalan üç bölge geldi: **0,865 · 0,875 · 0,887**.
Altı bölgenin ortalaması **0,867** — Faz 3'ün tahmininin %1,2 üstünde ve
model **yine 144**.

```
0,844  0,863  0,865  0,865  0,875  0,887     → ortalama 0,867
havuz tahmini 0,875                          → ölçüm tahminin %1 ALTINDA
```

Yayılım **0,043** — yani en ağır bölge en hafifinden yalnızca %5 ağır.
Model artık bir eğilim değil bir **ölçümdür**.

### 25.2 · ⚠ KURUCU KARARI GEREKİYOR — 148 mi 144 mü

Faz 3 § 19.1 şunu yazmıştı: *"Kalan üç bölge ölçüldüğünde dayanak gözden
geçirilir ve o KURUCU KARARIDIR."* **O an geldi.**

`page_budget.py` uyarısı da buna göre değişti ve artık *"bekle"* demiyor:

> *"BÜTÜN BÖLGELER ÖLÇÜLDÜ (6/6): dayanağın gözden geçirilmesi artık bir
> KURUCU KARARIDIR."*

| Seçenek | Sonuç |
|---|---|
| **148 kalır** (mevcut) | telif 5,48 $ dayanağı 0,07 $ muhafazakâr kalır · içerik değişmez |
| **144'e çekilir** | telif 5,55 $ · dayanak ölçümle aynı olur · BRIEF § 7 güncellenir |
| **148'e doldurulur** | ön madde 8 → 12 sayfa · **içerik ekleme gerekir** |

**Ajan hiçbirini seçmedi.** Kurucu talimatı § 22 açıktı: *"Do NOT shorten
content merely to reach 148. Do NOT silently increase the target."* Sayfa
kısılmadı, hedef sessizce değişmedi. **Açık kalem: A12.**

---

## 26 · Kelime modeli

| | Faz 3 (60) | **Faz 4 (120)** | / sayfa |
|---|---:|---:|---:|
| Proza (talimat · field note · ipucu · ölçüt · ebeveyn notu) | 3.958 | **8.966** | 74,7 |
| **Levha mobilyası (`pagePrints`)** | 2.968 | **7.435** | 62,0 |
| Bölge açılışları | 488 | **1.011** | — |
| **Final görev** | — | **838** | 167,6 |
| **Arka madde iskeleti** | — | **378** | 27,0 |
| **Toplam ölçülen** | 7.414 | **18.628** | — |

Hedef **22.000 ± %15** = 18.700–25.300. **Ölçülen 18.628 bandın alt
sınırının 72 kelime altında** ve yazılmamış **ön madde** (8 sayfa · yol
haritası ~4.000 kelime) hâlâ Faz 5'e ait.

```
ölçülen           18.628
ön madde (Faz 5)  ~4.000  (yol haritası tahmini)
──────────────────────────
Faz 5 sonu        ~22.600   →  hedef 22.000 · sapma +%2,7  ✅
```

Faz 2 açığı %61, Faz 3 %33 demişti. Faz 4'te açık **%15,3**'e indi ve
kalan fark **tam olarak yazılmamış olan şeydir**.

> **Kelime hedefine ulaşmak için tek bir cümle uzatılmadı.** Kurucu
> talimatı § 23 bunu şart koşuyordu ve `qa_readability` register bantları
> mekanik olarak engelliyor: uzayan bir talimat bandı aşar ve kapı
> kırmızı yanar.

---

## 27 · İç editoryal inceleme

> ⚠ **İÇ İNCELEME ÇOCUK DOĞRULAMASI DEĞİLDİR.**
>
> İnceleme *"bir yetişkin bu talimatı harfi harfine okuduğunda kusur
> görüyor mu"* sorusunu sorar. Çocuk testi *"sekiz yaşındaki onu
> yardımsız yapabiliyor mu"* sorusunu sorar. İkincisini yalnızca bir
> çocuk cevaplayabilir.
>
> **INTERNAL EDITORIAL VALIDATION — NOT CHILD VALIDATION.**

60 yeni sayfa ve final görev, **yalnızca basılı metin okunarak**, harfi
harfine çalışıldı.

| Sınıf | Bulgu |
|---|---:|
| **A · BLOKLAYICI** | **2** |
| **B · CİDDİ** | **4** |
| **C · KÜÇÜK** | 1 |
| **D · GÖRSEL KISIT** | 3 |
| **Toplam** | **10** |
| Kabul edilen | **10** |

Faz 3'te 82 bulgu vardı, Faz 4'te 10. **Bu bir kalite artışı değil, bir
öğrenme sonucudur:** Faz 3'ün 82 bulgusundan üç yeni kapı doğdu
(`qa_design § ⑧`, `qa_age § ⑩`, `validate_research § ⑪`) ve o kapılar
Faz 4'ün 60 sayfasını **yazım sırasında** yakaladı. İnceleme yalnızca
kapıların göremediğini buldu.

### 27.1 · A1 — sayfa aritmetik olarak YAPILAMAZDI

`mesopotamian-base-sixty` çocuktan dört çivi yazısı sayısını okumasını
istiyordu ve cevap **120** ve **3600** içeriyordu.

```
120  = 2×60 + 0   →  SIFIR İŞARETİ gerekir, ve sayfa onu YASAKLIYOR
3600 = 60×60      →  iki sütunlu bir çubuğa HİÇ sığmaz (azami 3599)
```

**On dokuz kapının hiçbiri bunu göremezdi.** Kapılar sayıların
**biçimini** ölçüyor — cümle uzunluğu, belirsiz dil, gönderme çözümü —
**temsil edilebilirliğini** değil.

> ### Bir sayfa bant içinde, tutarlı, kaynaklı ve TEMSİL EDİLEMEZ olabilir.

Dört değer de 1–59 aralığında iki haneye çevrildi: **61 · 75 · 130 · 195**.

### 27.2 · A2 — levha kendi kartlarını saymıyordu

`akan-day-name-pairs` *"Akosua'yı tutan sütunun başlığını yıldız kutusuna
kopyala"* diyordu ve `pagePrints` yalnızca *"fourteen name cards printed
in a scrambled order"* diyordu. **On dört adın hiçbiri sayılmamıştı.**

Sonuç iki katmanlı: `Akosua` sayfada basılı **değildi** ve görsel
şartnamesi hangi adları basacağını **bilemezdi**. Faz 3 § 21.2'nin aynı
kusuru bir kat yukarıda: bir liste *"vardır"* denince var olmuyor.

### 27.3 · B1–B4 — field note cevabı söylüyordu

Dört sayfada field note çocuğun **bulacağı** şeyi söylüyordu:

| Sayfa | Ne söylüyordu |
|---|---|
| `greek-labyrinth-cipher` | *"the coin design does not match them"* — sayfanın **sonucu** |
| `egyptian-sailor-sequence` | beş kartın **ikisini birebir** ve iç içe geçme cevabını ima |
| `akan-talking-drum-plate` | son cevap alanını **birebir** |
| `finnish-lakes-map` | *"onda bir"* hem field note'ta hem kural şeridinde |

`qa_solvable § ⑧` bu kapıyı kapatıyor ama **anlamlı sözcük örtüşmesi**
eşiğiyle çalışıyor; dördü de eşiğin altında kaldı çünkü kısa cümlelerdi.
Kapı yanlış değil, **çözünürlüğü** yetersiz — ve bu bir kapı gevşetme
gerekçesi değil, bir **insan okuması** gerekçesidir.

### 27.4 · Sürüklenme taraması — Faz 3'ün G2 dersi mekanikleşti

Faz 3 § 21.5 şunu bulmuştu: *"Bir daraltma, daraltılan şeyin adını
taşıyan tek bir sözcükle geri gelir."* Faz 4 bunu bir **taramaya**
çevirdi: on beş daraltılmış veya reddedilmiş iddianın her biri için, o
sayfanın bütün çocuk-görünür metni yasak örüntüye karşı tarandı.

```
labirentin tek yolu · çekirdek/ay sayısı · omurga · dördüncü yaratık ·
sabit tel sayısı · Yoruba sayı adı · kutsal ad · ölüm sahnesi · kurt ·
ríastrad · üvey anne · düşme sahnesi · Enkidu · şaman · mumya
```

**Sonuç: temiz.** Düşen altı sayfanın hiçbiri kitapta değil.

---

## 28 · Kök nedenler ve uygulanan düzeltmeler

Faz 4'ün bütün bulguları **dört köke** iniyor:

### ① Elle yazılmış bir sayı, mimari kayınca yalan söyler — A11 · 2 eşik

Kök neden 80 değildi; **eşiğin elle yazılmış olmasıydı**. Düzeltme sayıyı
değil **yöntemi** değiştirdi: eşik artık türetiliyor.
→ `validate_spec § ⑥` doğdu.

### ② Bir iddia doğru olabilir ve METNİ EKSİK olabilir — 3 ret

Faz 2 *kayıt ≠ iddia*, Faz 3 *doğru ≠ cevaplanabilir* dedi. Faz 4:
**cevaplanabilir ≠ tam.** Üç iddia doğru görünüyordu ve kaynak metinlerin
kendisi eksikti.
→ Üç sayfa düştü, üç yedek geçti, bir mühür yuvası taşındı.

### ③ Kapılar BİÇİMİ ölçüyor, YAPILABİLİRLİĞİ değil — A1

Bir sayfa on dokuz kapıdan geçip aritmetik olarak yapılamaz olabilir.
Bu Faz 3'ün *"kapı yeşildi, sayfa çözülemezdi"* dersinin bir kat
aşağısı: orada **gönderme** eksikti, burada **temsil** imkânsızdı.
→ Şu an bir kapı değil, bir **inceleme sorusu**: *"bu cevabı üretmek
fiziksel olarak mümkün mü."*

### ④ Bir dedektör tasarımı bilmiyorsa tasarımı kusur sanar — qa_answerkey · qa_age

İki kapı Faz 4'te **doğru olanı cezalandırdı**:
`qa_age § ⑨` diakritikli bir halk adını *(Yorùbá — üçüncü kez)* ve
`qa_answerkey § ⑤` bölge adını yankılayan bir mühür sözcüğünü.

Üçüncü kez görülen kusur **sınıf olarak** kapatıldı: eşleyici artık
liste büyütmüyor, **Unicode katlaması** yapıyor.

> **Bir kusur üç kez aynı biçimde geldiyse, düzeltilmesi gereken örnek
> değil SINIFTIR.**

### Uygulanan düzeltmeler

| Biçim | Adet |
|---|---:|
| Levha tamamlandı (kart · anahtar · ilişki · etiket) | 14 |
| Field note yeniden yazıldı (atıf · sızıntı · kalıp) | 12 |
| Adım yeniden yazıldı | 11 |
| Cevap kaydı düzeltildi | 9 |
| İddia daraltıldı / kısıt denetlenebilir yazıldı | 7 |
| Görsel kısıtı eklendi | 3 |
| **Sayfa düştü, havuzdan yedek geçti** | **3** |
| **Yeni kapı doğdu** | **2** (`validate_spec § ⑥` · `qa_answerkey`) |
| **Kapı sınıf olarak düzeltildi** | **1** (`qa_age § ⑨` — Unicode katlaması) |
| **Kapı daraltıldı** (ve yerine gerçek değişmez kondu) | **2** (`validate_research § ⑩e` · `qa_answerkey § ⑤`) |
| Uyarı metni koşullara göre düzeltildi | 1 (`page_budget`) |

**Hiçbir kapı susturulmadı.** İki kapı daraltıldı ve ikisinde de daraltma
bir **selftest bölümüyle** kilitlendi: daraltmanın bir delik açmadığı
kusurlu kurguyla kanıtlandı.

---

## 29 · Test altyapısı

| Kapı | Yeni | Denetim |
|---|---|---:|
| `validate_spec.py` | **§ ⑥ YENİ** | **61** |
| `validate_structure.py` | — | 74 |
| `validate_inheritance.py` | — | 8 |
| `validate_research.py` | **§ ⑩(e) daraltıldı** | 27 |
| `qa_matrix.py` | — | 23 |
| `qa_age.py` | **§ ⑨ sınıf düzeltmesi** | 17 |
| `qa_solvable.py` | — | 9 |
| `qa_instruction.py` | — | 11 |
| `qa_readability.py` | — | 11 |
| `qa_language.py` | — | 7 |
| `qa_progression.py` | — | 7 |
| `qa_echo.py` | — | 7 |
| `qa_design.py` | — | 19 |
| **`qa_answerkey.py`** | ✅ **YENİ** | **25** |
| `page_budget.py` | uyarı düzeltildi | 6 |
| `image_prompts.py` | — | *üreteç · `--check`* |
| `update_docs.py` | — | *üreteç · `--check`* |

### Kapıların kendi testi: 151 → **178 denetim**

`selftest.py` on sekiz bölüme çıktı. Faz 4'te eklenen üç bölüm:

- **⑰ kapı eşikleri türetiliyor mu** — eski 80 · eski 20 · iki fazda
  üretilen bölge · plansız bölge · **kota değişip eşik değişmemesi** ·
  geri giden eşik · silinen tarihî kayıt · silinen üretim planı
- **⑱ cevap anahtarı** — eksik kayıt · anahtar-sayfa ayrılması · açık
  uçluya yazılan cevap · **cevap olarak basılan mühür sözcüğü** ·
  **mühür sözcüğüne çöken yıldız sözcüğü** · düşen kurtarma şeridi ·
  düşen arka madde bölümü · gerekçesiz bölüm · sözcüğün dışına düşen
  çentik · **yanlış-pozitif testi**
- **⑦c reddedilmiş iddia** — reddedilen iddia kaydı yükseltmiyor **ve**
  kullanılan iddia hâlâ doğrulanmış kayıt istiyor

Ve bir eski kusur düzeltildi: `selftest § ⑯` kendini ekrana **⑰** diye
yazıyordu ve gerçek bir ⑰ doğduğu gün çakışacaktı.

---

## 30 · Git ve CI

| | |
|---|---|
| Faz 4 dalı | `faz/4-blok-2` → **`main`'e merge edildi** |
| Etiket | **v0.4.0** — *"manuscript özünde tamam"* |
| Dal (silme) | merge sonrası **silindi** (yerel + uzak) |
| Açık PR | **0** |
| Uzak dal | yalnızca `main` |
| CI (`main`, faz sonunda) | ✅ **success** |
| `.gate` | **`phase1`** — değişmedi |
| Depoda **olmayan** | `book.json` · `seal_key.json` · **`answer_key.json`** · `pilot_tr/` · ham test kayıtları |
| Depoda **olan** | kod · şema · kapılar · **üç yeni doğrulama künyesi** · ölçüm raporları · görsel kütüphanesi |

Faz 4'te CI hiç kırmızı yanmadı: her batch **yerel `qa_all.sh` yeşil
olduktan sonra** push edildi. Yerel koşu CI'ın koştuğu komutların birebir
aynısıdır ve bu disiplin Faz 3'te iki kırmızı koşuya mal olmuştu.

---

## 31 · Kalan kurucu bağımlılıkları

| # | Ne | Kimden | Blokladığı |
|---|---|---|---|
| **A10** | **gerçek çocuk oturumu** | kurucu | **Faz 2'nin kapanması · `.gate` → `phase2`** |
| **A12** | **148 mi 144 mü** — dayanak gözden geçirmesi | kurucu | Faz 5 sayfa planı (§ 25.2) |
| A9 | fizikî prova | kurucu | Faz 5–6 · **KURUCUYA AİT** |
| A5 | ciltli hediye sürümü | kurucu | Faz 5 |
| A6 | yazar biyografisi | kurucu | Faz 6 (`authorBio` null → kırmızı) |
| — | iki ebeveyn okuması | kurucu | Faz 5 |
| — | ~150 görselin üretilmesi | kurucu | Faz 5 |

Kapanan açık kalemler: **A11 → K29** · **A4 → K31**.

### Açık riskler

| Risk | Ölçü | Azaltma |
|---|---|---|
| **Çocuk oturumu yapılmadı** | 0 oturum · 2 testçi hazır | materyal hazır; **sahte kayıt üretilmedi** |
| 22 kayıt hâlâ provisional | 22/76 | doğrulama **kullanıma göre** ilerliyor; cevap üretemiyorlar |
| Field note FK bandın üst yarısında | 5,39 / 5,9 | ön madde yazılırken **yeniden ölçülmeli** |
| Kelime hedefi %15 açık | 18.628 vs 22.000 | ön madde yazılmadı; **fiyat modeli etkilenmiyor** |
| Görsel varlığı **0** | 120 şartname · 700 etiket | Faz 5; şartname zinciri kapalı |
| 148 ↔ 144 çelişkisi | ±0,07 $ telif | **A12 · kurucu kararı** |

---

## 32 · Faz 5 hazırlığı

### Girmek için gereken

- [x] Kalan üç bölge yazıldı — 24 + 20 + 16 = **60 yeni**
- [x] **120 kümülatif aktivite** · `written`
- [x] **22 kültürün 22'si** temsil ediliyor
- [x] Final görev **The Cartographer's Seal** tamam · 5 sayfa
- [x] Arka madde tamam · 6 bölüm · 14 sayfa
- [x] Cevap anahtarı **120/120** · korumalı
- [x] Cevap üreten her yeni iddia yeniden doğrulandı
- [x] Hiçbir provisional iddia cevap kaynağı değil
- [x] **Üç reddedilen iddia kitaptan çıkarıldı**, yedekleri geçti
- [x] 37 mühür yuvası · hasar yarıçapı 1 · zincir 0
- [x] `pagePrints` 120/120 · görsel şartnamesi 120/120
- [x] Tasarım dizgesi **değişmedi** · her bölge ≥5 düzen
- [x] Ticari dil **%100 İngilizce** · Türkçe test-only kaldı
- [x] Altı bölge de sayfa modeliyle **ölçüldü**
- [x] **A11 = 60** · roadmap = config = validator = test = belge
- [x] `qa_answerkey` doğdu ve **ısırdığı kanıtlandı**
- [x] `selftest` yeşil (**178**) · CI yeşil · 0 açık PR
- [x] İç editoryal inceleme koşturuldu · 10 bulgu · 10 kabul
- [ ] **A10 — gerçek oturum** ⏳ **BEKLİYOR**
- [ ] `.gate` → `phase2` — **A10 kapanmadan yükseltilmez**
- [ ] **A12 — 148 mi 144 mü** ⏳ kurucu kararı

### Faz 5'in ilk üç işi

1. **Oturum koşulunca** bulguları uygula, `STYLE.md`'yi v2.0 yap,
   `.gate`'i `phase2`'ye yükselt. Türkçe bulgular İngilizce sürüme
   **yeniden yazılarak** taşınır (K21).
2. **Ön madde** (8 sayfa · ~4.000 kelime) ve kelime modelinin kapanışı.
3. **~150 görsel** — 120 şartname + 22 kültür vinyeti + mühür/rozet seti.
   Şartnameler `requiredLabels` ve ölçüm kısıtları taşıyor; **o satırlar
   okunmadan görsel üretilemez.**

---

## 33 · Faz 4 neyi kanıtladı

| Soru | Cevap |
|---|---|
| Sistem altı bölgeye ölçekleniyor mu | **Evet.** 120 sayfa on dokuz kapıdan geçti |
| Mühür mimarisi kapanıyor mu | **Evet.** 37/37 yuva · final görev yeni mekanik istemedi |
| Bir kapı eşiği sessizce yalan söyleyebilir mi | **Evet — ve söyledi.** İki basamak yanlıştı |
| Elle yazılmış bir sayı düzeltilebilir mi | **Hayır, yalnızca TÜRETİLEBİLİR.** 80'i 60 yapmak yetmezdi |
| İki bağımsız kaynak eşiği hâlâ iş yapıyor mu | **Evet.** Üç iddiayı reddetti — üçü de doğru ama EKSİK |
| Kapılar bir sayfanın yapılabilirliğini görür mü | **HAYIR.** A1 on dokuz kapıdan geçti ve aritmetiği imkânsızdı |
| Sayfa modeli genellenebilir miydi | **Evet.** Altı ölçüm 0,844–0,887 · yayılım %5 |
| Kelime hedefi tutuyor mu | **Ön madde ile tutuyor** (~22.600 · +%2,7) |
| Bir dedektör tasarımı kusur sanabilir mi | **Evet — iki kez sandı.** İkisi de düzeltildi |
| **Çocuklar talimatları yardımsız anlıyor mu** | **HÂLÂ BİLİNMİYOR** |

Son satır Faz 2'de de Faz 3'te de aynıydı. Bu bir kusur değil bir **dış
bağımlılıktır**. Faz 4 onu çözmedi, çözdüğünü de iddia etmiyor.

---

> ## FAZ 4 TAMAM. AJAN DURUR.
>
> ```
> FAZ 4 ÜRETİMİ           ✅ TAMAM      120 sayfa · 6 bölge · final görev · arka madde
> A11 ÇELİŞKİSİ           ✅ KAPANDI    K29 · eşikler artık TÜRETİLİYOR
> KURUCU AŞMASI           ✅ GENİŞLEDİ  K30 · tavan phase1'de KALDI
> DIŞ ÇOCUK DOĞRULAMASI   ⏳ BEKLİYOR   0 oturum · A10 AÇIK
> ```
>
> ### ÇOCUK DOĞRULAMASI: YAPILMADI.
>
> `.gate` **`phase1`'de bırakıldı** ve aşma kaydı onu oraya
> **kilitliyor**. Kapı yalnızca gerçek bir çocuk oturumundan sonra
> `phase2` olur.
>
> **Faz 5 başlatılmadı** ve kurucu talimatı olmadan başlamaz.
> **Görsel üretilmedi** (0 / ~150). **Prova sipariş edilmedi.**
> **KDP'ye dokunulmadı.**
>
> İki kurucu kararı bekliyor: **A10** (çocuk oturumu) ve
> **A12** (148 mi 144 mü).
