# PROJECT CONTEXT — The Myth Hunter's Field Book

> **Projeye yeni giren her ajanın ve her insanın okuyacağı ilk belgedir.**
> Hafızası olmayan bir ajan buradan başlar.
>
> Son güncelleme: **12 Ağustos 2026** · Faz: **0 · Bootstrap** · Kapı: `phase0`

---

## 1 · Proje kimliği

| | |
|---|---|
| Başlık | **The Myth Hunter's Field Book** |
| Alt başlık (hipotez) | A Screen-Free Quest Through 22 Cultures — 120 Puzzles, Maps, Codes and Challenges for Ages 8–12 |
| Seri | "The Great Book of…" · **Field Book alt serisi** · Cilt 1 |
| Depo | `emredogan-cloud/the-myth-hunters-field-book` |
| Okur | 8–12 yaş · **Alıcı** ebeveyn/büyükanne/öğretmen/kütüphaneci |
| Kaynak | [`AMAZON-KDP-2026-MARKET-OPPORTUNITY-REPORT.html`](../AMAZON-KDP-2026-MARKET-OPPORTUNITY-REPORT.html) § 11 · Kitap B |
| Portföy yeri | **Kitap B · ikinci** · huni tamamlayıcı |

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
| Faz | **0 · Bootstrap** — altyapı kuruldu, Faz 1 **başlamadı** |
| Kapı (`.gate`) | `phase0` |
| Aday aktivite | 0 / ≥160 |
| Kilitli / yazılmış | 0 / 120 |
| Devralınan kayıt | 0 |
| **Sonraki adım** | **KURUCU ONAYI** → sonra Faz 1 |

⚠ **Faz 1 BAŞLAMADI ve kurucu onayı olmadan başlamaz.**

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
| [`00_CONTEXT/AGE_POLICY.md`](00_CONTEXT/AGE_POLICY.md) | Yaş uygunluğu · 6 yasak çerçeve | kurucu onayıyla |
| [`00_CONTEXT/SOURCING_STANDARD.md`](00_CONTEXT/SOURCING_STANDARD.md) | Kaynak ve kısıt taraması | kurucu onayıyla |
| [`00_CONTEXT/STYLE.md`](00_CONTEXT/STYLE.md) | Ses, sayfa dili, yasak kalıp | Faz 2'de kalibre |
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
| A1 | Manuscript public depoda mı duracak? | kurucu | **Faz 1 başlamadan** |
| A2 | **Devralma politikası onayı** | kurucu | **Faz 1 başlamadan** |
| A3 | 6 bölge ve mühür mimarisi | kurucu | Faz 1 sonu |
| A4 | 120 aktivitenin nihai listesi | kurucu | Faz 1 sonu |
| A5 | Ciltli hediye sürümü | kurucu | Faz 4 |
| A6 | Yazar biyografisi metni | kurucu | Faz 5 |
| A7 | **≥2 çocuk testçi** | kurucu | **Faz 2 bloklayıcısı** |
| — | İki ebeveyn okuması | kurucu | Faz 5 |
| — | ~150 görselin üretilmesi | kurucu | Faz 5 |
| — | KDP paneli işlemleri | kurucu | Faz 6 sonrası |

---

## 11 · Sonraki izinli eylem

> **KURUCU ONAYI BEKLENİYOR.**
>
> Bootstrap tamamlandı. Faz 1 **başlatılmadı**.
> İzin verildiğinde ilk iş: `faz/1-devralma` dalını açmak ve
> `IMPORT_MANIFEST.json`'u üretmek — envanter ondan türer.
