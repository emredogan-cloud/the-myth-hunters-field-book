# PROJECT CONTEXT — The Myth Hunter's Field Book

> **Projeye yeni giren her ajanın ve her insanın okuyacağı ilk belgedir.**
> Hafızası olmayan bir ajan buradan başlar.
>
> Son güncelleme: **13 Ağustos 2026** · Faz: **1 TAMAM** · Kapı: `phase1`

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
| Faz | **2 · TEKNİK PİLOT TAMAM** — çocuk doğrulaması **BEKLİYOR** |
| Kapı (`.gate`) | `phase1` — **bilerek yükseltilmedi** |
| Aday aktivite | **168** / ≥160 ✅ |
| Kilitli / yazılmış | **16** / 120 — `jaguar-condor` bölgesinin tamamı |
| Devralınan kayıt | **76**; **7'si Faz 2'de yeniden doğrulandı** |
| Doğrulanmış iddia | **13** · 10 teyit · **3 DÜZELTME** |
| Kültür · bölge | **22** · **6** ✅ |
| Sayfa modeli | **144** ölçüldü (hedef 148 ±%6) ✅ · 1/6 bölge gerçek |
| Kapı öz-testi | **106 denetim yeşil** |
| Çocuk testi | ⏳ **0 testçi · DIŞ DOĞRULAMA BEKLİYOR** |
| **Sonraki adım** | **KURUCU: A7 (çocuk testçi)** → sonra Faz 3 |

⚠ **FAZ 2 TAM OLARAK KAPANMADI ve kapanamaz.**

Teknik pilot geçti: 16 sayfa yazıldı, 13 kapı yeşil, mühür uçtan uca
doğrulandı. Ama Faz 2'nin PASS ölçütü *"çocuk testinde ≥%80 yardımsız
anlaşılma"* der ve **0 testçi** var.

```
TEKNİK PİLOT           ✅ GEÇTİ
DIŞ ÇOCUK DOĞRULAMASI  ⏳ BEKLİYOR   ← bu ikisi TOPLANMAZ
```

`.gate` bu yüzden `phase1`'de bırakıldı: kapıyı yükseltmek, yapılmamış
bir testi geçmiş saymak olurdu.

Faz 2 raporu: [`06_REPORTS/PHASE_2_REPORT.md`](06_REPORTS/PHASE_2_REPORT.md)
Faz 1 raporu: [`06_REPORTS/PHASE_1_REPORT.md`](06_REPORTS/PHASE_1_REPORT.md)

### Faz 1'in kurduğu altı katman

```
① DEVRALMA      IMPORT_MANIFEST.json ····· 76 kayıt · sha256'lı
② KÜLTÜR        culture_index.json ······· 22 kültür · A/B/C kademesi
③ BÖLGE+MÜHÜR   region_index.json ········ 6 bölge · 37 mühür yuvası
④ AKTİVİTE      activity_index.json ······ 168 aday · 30 hücre dolu
⑤ GÜVENLİK      AGE_POLICY § 3 ··········· safetyClass HESAPLANIR
⑥ SAYFA         page-budget.json ········· 148 sayfa · 5,48 $ telif
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
| [`00_CONTEXT/STYLE.md`](00_CONTEXT/STYLE.md) | Ses, sayfa dili, **üç register bandı** | Faz 2'de yeniden kalibre |
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
| **A4** | 168 adaydan 120'sinin nihai seçimi | kurucu | Faz 3 başlarken · pilot 16'sını seçti |
| **A7** | **≥2 çocuk testçi** | kurucu | **AÇIK · paket hazır, test koşmadı** |
| **A9** | **fizikî prova** | kurucu | Faz 5–6 · **kurucuya ait** |
| A5 | Ciltli hediye sürümü | kurucu | Faz 4 |
| A6 | Yazar biyografisi metni | kurucu | Faz 5 |
| — | İki ebeveyn okuması | kurucu | Faz 5 |
| — | ~150 görselin üretilmesi | kurucu | Faz 5 |
| — | KDP paneli işlemleri | kurucu | Faz 6 sonrası |

---

## 11 · Sonraki izinli eylem

> **KURUCU ONAYI BEKLENİYOR — A7.**
>
> Faz 2'nin teknik pilotu tamamlandı ve CI yeşil. **Faz 3 başlatılmadı.**
>
> Bekleyen tek şey:
> **A7 — en az iki çocuk testçi.** Test paketi hazır
> ([`03_EDITORIAL/CHILD_TEST_PROTOCOL.md`](03_EDITORIAL/CHILD_TEST_PROTOCOL.md)),
> kayıt defteri açık ve **boş**. Testçi bulunamazsa dış doğrulama
> beklemede kalır ve **sahte test kaydı üretilmez**.
>
> Testçiler Türkçe konuşuyorsa tester-facing materyal geçici olarak
> Türkçe üretilebilir (K21) — `child_test_pack.py --lang tr`, ki o betik
> kurucu onayı gelene kadar üretmeyi **reddeder**.
>
> Onay geldiğinde ilk iş: `faz/2-pilot` dalını açmak ve **en zor bölgeyi**
> seçmek — kolay bölgeyle kalibre edilen bir şablon zor bölgede kırılır.
