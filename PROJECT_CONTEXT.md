# PROJECT CONTEXT — The Myth Hunter's Field Book

> **Projeye yeni giren her ajanın ve her insanın okuyacağı ilk belgedir.**
> Hafızası olmayan bir ajan buradan başlar.
>
> Son güncelleme: **16 Ağustos 2026** · Faz: **6 TAMAM** · Kapı: `release`
>
> ⚠ **Kapı ile faz AYRIŞMIŞTIR ve bu bilinçlidir.** Kurucu Faz 3'ü, Faz
> 2'nin çocuk oturumu (**A10**) yapılmadan başlattı — karar **K27** —,
> Faz 4'ü aynı aşmayla açtı — karar **K30** — ve Faz 5'i de aynı aşmayla
> açtı — karar **K34**.
> Aşma **üç kez uzadı ve tavan bir kez bile kalkmadı.** Kayıtlıdır, gizli
> değildir ve `validate_spec § ⑤` tarafından mekanik olarak
> kilitlenmiştir.

---

## 1 · Proje kimliği

| | |
|---|---|
| Başlık | **The Myth Hunter's Field Book** |
| Alt başlık (hipotez) | A Screen-Free Quest Through 22 Cultures — 120 Puzzles, Maps, Codes and Challenges for Ages 8–12 |
| Seri | "The Great Book of…" · **Field Book alt serisi** · Cilt 1 |
| Depo | `emredogan-cloud/the-myth-hunters-field-book` |
| Okur | 8–12 yaş · **Alıcı** ebeveyn/büyükanne/öğretmen/kütüphaneci |
| Kaynak | `AMAZON-KDP-2026-MARKET-OPPORTUNITY-REPORT.html` § 11 · Kitap B |
| Portföy yeri | **Kitap B · ikinci** · huni tamamlayıcı |


> **Pazar raporu bu depoda DEĞİLDİR.** `AMAZON-KDP-2026-MARKET-OPPORTUNITY-REPORT.html`
> kurucunun çalışma dizininde duran **özel bir strateji belgesidir** ve üç
> public depoya kopyalanmaz. Bu belgede ona **künyeyle** atıf yapılır, bağ
> verilmez: bir depoyu klonlayan kişi o dosyaya ulaşamaz ve kırık bir bağ
> görmemelidir.

---

## 2 · Amaç ve ticari mantık

120 aktivitelik, 22 kültürü gezen tek bir "saha görevi". Çocuk bulmacayı
çözerken **gerçekten mitoloji öğrenir**.

Ama bu kitabın işi tek başına para kazanmak **değildir**:

> **World Myths'in öksüzlüğünü bitirmek.**

*The Great Book of World Myths* portföyün en dar marjlı, en pahalı raftaki,
**read-through'suz** ürünüdür. Bu kitap ona bir ikinci ürün verir ve tek
kitabı bir seriye çevirir. Değeri kendi P&L'inde değil, **portföy etkisinde**
ölçülür.

Fırsat skoru **6,0/10** — üçünün en düşüğü, **ve bu bilinçlidir**.

---

## 3 · Bu proje ne DEĞİLDİR

| Değildir | Neden |
|---|---|
| *World Myths'in aktivite eki* | Ayrı ürün, ayrı ISBN, ayrı depo, **ayrı yazım** |
| *Jenerik bir bulmaca kitabı* | Her bulmaca içerikten türer; dekoratif tema **yasaktır** |
| *World Myths araştırmasının kopyala-yapıştırı* | Devralma bir **sözleşmedir**, kısayol değil (§ 5) |

---

## 4 · Şu anki durum

| | |
|---|---|
| Faz | **6 · TAMAM** — KDP paketi hazır |
| Kapı (`.gate`) | `release` — ⚠ **A10 KANITLA DEĞİL KARARLA kapandı (K40)** |
| Aday aktivite | **168** / ≥160 ✅ |
| Kilitli / yazılmış | **120** / 120 — **altı bölgenin altısı** ✅ |
| Devralınan kayıt | **76**; **54'ü yeniden doğrulandı** (Faz 3: 31) |
| Doğrulanmış iddia | **108** · 92 teyit · 13 düzeltme · **3 RET** |
| Kültür · bölge | **22** · **6** ✅ · yazılmış bölge **6/6** ✅ |
| Sayfa modeli | **160** DİZİLDİ = hedef **160** · sapma **%0** · ✅ **A13 → K38** |
| Ön madde | **9 sayfa** · 8 bölüm · başlık ve künye dâhil ✅ |
| Kelime | **21.283** / 22.000 ±%15 ✅ |
| Görsel envanteri | **158** varlık (120 + 22 vinyet + 6 damga + 6 rozet + 4 ön madde) |
| Görsel şartnamesi | **725 zorunlu etiket** · **üretilmiş varlık 0** — ham üretim kurucuya ait |
| Görsel hattı | ✅ kuruldu ve **dosya katmanında sınandı** (K35) |
| Kapı öz-testi | **234 denetim yeşil** |
| Çocuk testi | ⏳ **2 testçi · 0 OTURUM · DIŞ DOĞRULAMA BEKLİYOR** |
| **Sonraki adım** | Faz 5 raporu → **DUR**. Faz 6 kurucu talimatı ister. |

⚠ **FAZ 2 HÂLÂ KAPANMADI — VE 120 SAYFA ONU KAPATMAZ.**

Kurucu Faz 3'ü, Faz 4'ü ve Faz 5'i A10 beklenmeden başlattı
(**K27** · **K30** · **K34**). Bu bir **sıra** kararıdır, bir **sonuç**
değil:

```
TEKNİK ÜRETİM          ✅ TAMAM     120 sayfa · 6 bölge · final görev · arka madde
DIŞ ÇOCUK DOĞRULAMASI  ⏳ BEKLİYOR  0 oturum
                       ← bu ikisi TOPLANMAZ
```

`.gate` bu yüzden `phase1`'de duruyor ve aşma kaydı onu **oraya
kilitliyor**: `validate_spec § ⑤` aşma etkinken kapının yükselmesine
izin vermiyor. Yani aşma, kapıyı açmak için **kullanılamaz**.

Faz 5 raporu: [`06_REPORTS/PHASE_5_REPORT.md`](06_REPORTS/PHASE_5_REPORT.md)
Faz 4 raporu: [`06_REPORTS/PHASE_4_REPORT.md`](06_REPORTS/PHASE_4_REPORT.md)
Faz 3 raporu: [`06_REPORTS/PHASE_3_REPORT.md`](06_REPORTS/PHASE_3_REPORT.md)
Faz 2 raporu: [`06_REPORTS/PHASE_2_REPORT.md`](06_REPORTS/PHASE_2_REPORT.md)
Faz 1 raporu: [`06_REPORTS/PHASE_1_REPORT.md`](06_REPORTS/PHASE_1_REPORT.md)

### Faz 1'in kurduğu altı katman

```
① DEVRALMA      IMPORT_MANIFEST.json ····· 76 kayıt · sha256'lı
② KÜLTÜR        culture_index.json ······· 22 kültür · A/B/C kademesi
③ BÖLGE+MÜHÜR   region_index.json ········ 6 bölge · 37 mühür yuvası
④ AKTİVİTE      activity_index.json ······ 168 aday · 30 hücre dolu
⑤ GÜVENLİK      AGE_POLICY § 3 ··········· safetyClass HESAPLANIR
⑥ SAYFA         page-budget.json ········· 144 sayfa · 5,55 $ telif
```

Her katmanın kendi kapısı var ve her kapı `selftest.py` tarafından
sınanıyor. **Hiçbir katman bir insana güvenmiyor.**

---

## 5 · Bu projenin iki benzersiz riski

### Risk A — Çocuk ürünü riski
Alıcı ebeveyn, okur çocuktur. Yanlış tonlanmış bir görev
*"çocuğum için fazla karanlık"* yorumuna dönüşür ve **o yorum silinmez**.
Çocuk artık yalnızca okumuyor: **yazıyor, çiziyor, çözüyor.**
→ [`00_CONTEXT/AGE_POLICY.md`](00_CONTEXT/AGE_POLICY.md)

### Risk B — Devralma riski
> **Bir hikâye anlatmak ile bir aktivite tasarlamak aynı iddia değildir.**

World Myths'te *"bu mitte X olur"* anlatı için yeterlidir. Burada aynı cümle
bir **bulmaca cevabıdır** — yanlışsa çocuk kendini suçlar.
→ [`00_CONTEXT/INHERITANCE_ARCHITECTURE.md`](00_CONTEXT/INHERITANCE_ARCHITECTURE.md)

Öncelik sırası — çakışmada yukarıdaki kazanır:

1. **Çocuğun güvenliği ve yaş uygunluğu**
2. **Cevap kesinliği** (tek ve doğru cevap)
3. Kültürel doğruluk ve kısıt taraması
4. Talimat netliği
5. Öğrenme değeri
6. Sayfa / kelime bütçesi
7. Üretim hızı

---

## 6 · İzolasyon ve devralma — ikisi birden

| | |
|---|---|
| **İzolasyon** | Ortak dosya, ortak build, ortak `.gate`, ortak rapor **YOK** |
| **Devralma** | World Myths'ten veri **kopyalanır**, kökeni sha256 ile kaydedilir |
| World Myths deposu gerekli mi | **HAYIR** — bu proje onsuz build alır ve CI yeşil yanar |

Devralma **canlı bağımlılık değildir**. Ayrıntı ve gerekçe:
[`00_CONTEXT/INHERITANCE_ARCHITECTURE.md`](00_CONTEXT/INHERITANCE_ARCHITECTURE.md)

---

## 7 · Altı faz — özet

| Faz | Ad | Yazım | Kapı |
|---|---|---|---|
| 1 | Devralma mimarisi, taksonomi, yaş çerçevesi | yok | `phase1` |
| 2 | Pilot: bir bölge + **çocuk saha testi** | ~3.700 | `phase2` |
| 3 | Bölge bloğu I — üç bölge | ~7.400 | `phase3` |
| 4 | Bölge bloğu II + final görev | ~6.900 | `phase4` |
| 5 | Editoryal yakınsama + sayfa tasarımı | ~4.000 | `phase5` |
| 6 | Nihai üretim + KDP paketi | yok | `release` |

Tam yol haritası:
[`THE_MYTH_HUNTERS_FIELD_BOOK_IMPLEMENTATION_ROADMAP.md`](THE_MYTH_HUNTERS_FIELD_BOOK_IMPLEMENTATION_ROADMAP.md)

---

## 8 · Belge haritası

| Belge | Ne söyler | Kim değiştirir |
|---|---|---|
| [`THE_MYTH_HUNTERS_FIELD_BOOK_IMPLEMENTATION_ROADMAP.md`](THE_MYTH_HUNTERS_FIELD_BOOK_IMPLEMENTATION_ROADMAP.md) | **Tek doğruluk kaynağı** | kurucu onayıyla |
| [`BRIEF.md`](BRIEF.md) | Ürün, kitle, ticari model | kurucu |
| [`00_CONTEXT/INHERITANCE_ARCHITECTURE.md`](00_CONTEXT/INHERITANCE_ARCHITECTURE.md) | **Devralma sözleşmesi** | kurucu onayıyla |
| [`00_CONTEXT/AGE_POLICY.md`](00_CONTEXT/AGE_POLICY.md) | Yaş uygunluğu · 6 yasak çerçeve · **güvenlik sınıfı ağacı** | kurucu onayıyla |
| [`00_CONTEXT/CULTURE_POLICY.md`](00_CONTEXT/CULTURE_POLICY.md) | **Hangi kültür hangi biçimde aktiviteye girer** | kurucu onayıyla |
| [`00_CONTEXT/ACTIVITY_TAXONOMY.md`](00_CONTEXT/ACTIVITY_TAXONOMY.md) | Beş tip · on öğrenme boyutu | Faz 2'de kalibre |
| [`00_CONTEXT/PROGRESSION_ARCHITECTURE.md`](00_CONTEXT/PROGRESSION_ARCHITECTURE.md) | **Kitap neden bitirilir** · mühür mekaniği | kurucu onayıyla (A3) |
| [`00_CONTEXT/SOURCING_STANDARD.md`](00_CONTEXT/SOURCING_STANDARD.md) | Kaynak ve kısıt taraması | kurucu onayıyla |
| [`00_CONTEXT/STYLE.md`](00_CONTEXT/STYLE.md) | Ses, **sayfa dili kalıplarının tek sahibi**, üç register bandı | Faz 2'de yeniden kalibre |
| [`00_CONTEXT/DESIGN_SYSTEM.md`](00_CONTEXT/DESIGN_SYSTEM.md) | **On modül · on düzen** · yapı tutarlılığı ⇄ kültürel çeşitlilik | Faz 3'te donduruldu |
| [`00_CONTEXT/LESSONS_FROM_CODEX.md`](00_CONTEXT/LESSONS_FROM_CODEX.md) | Taşınan disiplin | sabit |
| [`DECISIONS.md`](DECISIONS.md) | Kararlar + **AÇIK KARARLAR** | her faz |
| [`CHANGELOG.md`](CHANGELOG.md) | Ne değişti, neden | her faz |
| [`BOOK_STATS.md`](BOOK_STATS.md) | Ölçülen sayılar | **üretilir** |
| [`ROADMAP_PROGRESS.md`](ROADMAP_PROGRESS.md) | Faz ilerlemesi | **üretilir** |

---

## 9 · Bir ajan işe nasıl başlar

```bash
cd THE-MYTH-HUNTERS-FIELD-BOOK

cat .gate                            # aktif faz kapısı
cat ROADMAP_PROGRESS.md              # ilerleme
grep -n "AÇIK KARAR" DECISIONS.md    # kurucudan yanıt bekleyenler

./04_BUILD/qa_all.sh                 # yeşilse CI de yeşil olur
```

**Kural:** kapı `.gate`ten okunur, tahmin edilmez. CI kırmızıyken hiçbir
şey ilerlemez.

---

## 10 · Açık bağımlılıklar

| # | Ne | Kimden | Ne zaman |
|---|---|---|---|
| ~~A1~~ | ~~Manuscript public depoda mı duracak?~~ | — | ✅ **kapandı → K11** |
| ~~A2~~ | ~~Devralma politikası onayı~~ | — | ✅ **kapandı → K12** |
| ~~A3~~ | ~~6 bölge ve mühür mimarisi onayı~~ | — | ✅ **kapandı → K18** |
| ~~A8~~ | ~~148 sayfa kabul mü~~ | — | ✅ **kapandı → K19** |
| ~~A7~~ | ~~≥2 çocuk testçi~~ | — | ✅ **kapandı → K26** |
| ~~A11~~ | ~~`gates.requirements.phase3` 80 mi 60 mı~~ | — | ✅ **kapandı → K29** · kurucu **60** dedi |
| ~~A4~~ | ~~168 adaydan 120'sinin nihai seçimi~~ | — | ✅ **kapandı → K31** |
| ~~A12~~ | ~~148 mi 144 mü — dayanak~~ | — | ✅ **kapandı → K33** · kurucu **144** dedi |
| **A10** | **gerçek çocuk oturumu** | kurucu | **AÇIK · K27/K30/K34 ile ERTELENDİ, kapanmadı** |
| **A9** | **fizikî prova** | kurucu | Faz 5–6 · **kurucuya ait** |
| **A15** | **mobilya çiftlemesi — hangi taraf bırakacak** | kurucu | **AŞAMA 2 ÖNCESİ · YÜKSEK** |
| **A16** | **156 levha 300 dpi'da yeniden üretilecek mi** | kurucu | **A15 İLE BİRLİKTE · YÜKSEK** |
| **A17** | **16 varlık dosyası** (kapak · A+ · 2 levha) | kurucu | **AŞAMA 2 ÖNCESİ · YÜKSEK** |
| A5 | Ciltli hediye sürümü | kurucu | Faz 4 |
| A6 | Yazar biyografisi metni | kurucu | Faz 6 |
| — | İki ebeveyn okuması | kurucu | Faz 5 |
| — | ~150 görselin **RAW üretimi** | kurucu | Faz 5 · hat hazır (**K35**) |
| — | KDP paneli işlemleri | kurucu | Faz 6 sonrası |

> **A15 ve A16 BİRLİKTE verilmelidir.** A15'in ② yolu seçilirse levhalar
> zaten yeniden üretiliyor demektir ve 300 dpi'ı aynı koşuda almak
> neredeyse bedavadır. Ayrı ayrı vermek, işi iki kez yapmaktır.

---

## 11 · Sonraki izinli eylem

> **YÜKLEME ÖNCESİ GEÇİŞ · AŞAMA 1 BİTTİ. AJAN DURDU VE BEKLİYOR.**
>
> Faz 6 *"KDP paketi hazır"* diyerek kapanmıştı. Yükleme öncesi denetim
> aynı pakete **yükleyecek biri gibi** baktı ve pakedin hazır
> **olmadığını** ölçtü.
>
> ```
> AŞAMA 1        ✅ prompt yazıldı · denetim yapıldı · ÜRETİM YOK
> AŞAMA 2        ⏳ kurucu "DEVAM" diyene kadar BAŞLAMAZ
>
> İÇ BLOK        ✅ 160 sayfa · 08_OUTPUT/PAPERBACK/  ⚠ 2 yer tutucuyla
> METADATA       ✅ DÜZELTİLDİ — "120 pages" → 120 puzzles / 160 pages (K41)
> KAPAK ÖLÇÜSÜ   ✅ 03_COVER/COVER_SPEC.md · sırt 0,3603" · GEÇİCİ
> PROMPTLAR      ✅ IMAGE_PROMPT_LIBRARY § 9 · kapak 2 · A+ 12 · levha 2
>
> KAPAK SANATI   ❌ KURUCUYA AİT — A17
> YER TUTUCU     ⛔ 2 varlık — s.60 · s.120 — BASIMI BLOKE EDER
> MOBİLYA        ⛔ 99 sayfada İKİ KEZ basılıyor — A15 · KURUCU KARARI
> 300 dpi        ⛔ 158/158 ölçütün altında — A16 · KURUCU KARARI
> EDİTORYAL      ⛔ 46 bulgu · 11 sayfada cevap sızıyor (9 değil)
> ÇOCUK OTURUMU  ❌ 0 — A10 KARARLA kapandı (K40), kanıtla değil
> ```
>
> **externalValidation = `overridden-zero-sessions`** — hiçbir yerde
> `passed` yazmıyor ve yazmayacak. Kitap çocuk doğrulamasından
> **geçmemiştir**.
>
> ⚠ **CI YEŞİL, KİTAP HAZIR DEĞİL.** Bir kapı ancak sorduğu soruyu
> ölçer; mobilya çiftlemesini **hiçbir kapı sormamıştı**. Artık
> `qa_design § ⑨` ölçüyor (uyarı olarak; A15 uygulanınca hataya
> yükseltilecek).
>
> **Kurucudan bekleniyor:** A15 · A16 (birlikte verilmeli) ve A17'nin
> 16 dosyası.
>
> Ölçüm raporu: [`06_REPORTS/KDP_PREFLIGHT_AUDIT.md`](06_REPORTS/KDP_PREFLIGHT_AUDIT.md)
> Teslim sözleşmesi: [`07_ASSETS/FOUNDER_ASSET_DELIVERY.md`](07_ASSETS/FOUNDER_ASSET_DELIVERY.md)
> Faz 6 raporu: [`06_REPORTS/FINAL_RELEASE_REPORT.md`](06_REPORTS/FINAL_RELEASE_REPORT.md)
>
> **KDP paneline dokunulmadı. Prova sipariş edilmedi. Hiçbir görsel
> üretilmedi. Yükleme kurucunundur.**
