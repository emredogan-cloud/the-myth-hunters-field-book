# AKTİVİTE TAKSONOMİSİ — beş tip ve ne öğrettikleri

> Bu belge kitabın **pedagojik** tarafını tanımlar: her aktivite tipi neyi
> öğretir, hangi biçimlerde görünür, hangi hatalara açıktır.
>
> Sürüm 1.0 · 13 Ağustos 2026 · `01_SOURCE/activity.schema.json § type`
> bunu uygular · `qa_matrix.py` dağılımı denetler

---

## 1 · Tek ölçüt

> ### Bir aktivite "hangi mitolojik ya da kültürel bilgiyi öğretiyor" sorusuna cevap veremiyorsa **dekoratiftir ve kitaba girmez.**

Bu bir üslup tercihi değil, bir **kapsam kuralıdır** (karar K4). Rafın
tamamı dekoratif tema üzerine kurulu: üstünde ejderha resmi olan rastgele
bir labirent. Bu kitabın rakiplerinden ayrıldığı **tek yer** budur.

| ❌ Dekoratif | ✅ İçerikten türeyen |
|---|---|
| Rastgele labirent + ejderha çizimi | **Knossos sarayının planı** — mitin doğduğu yapı |
| Rastgele bir şifre | **Ogham** · **Orhun** · **çivi yazısı** — gerçek yazı dizgeleri |
| Rastgele eşleştirme | Aynı motifin **dört kültürdeki** hâli |
| "Vikingleri renklendir" | **Gemi levhası** — sığ nehir teknesi ile açık deniz teknesi farkı |

Her adayın `learningDimensions` alanı **en az bir** boyut taşır.
Boyutsuz bir kayıt şemadan geçmez.

---

## 2 · Beş tip

| Tip | Ne yapar | Sayfa ağırlığı | Açık uçlu olabilir mi |
|---|---|---:|---|
| `cipher` | Gerçek bir yazı dizgesini okutur veya yazdırır | 0,75 | ❌ |
| `map` | Rota, coğrafya, plan | 1,0 | ❌ |
| `sort` | Tasnif, sıralama, eşleştirme | 0,75 | ❌ |
| `observe` | Gözlem levhası: bak, say, etiketle, çıkar | 1,0 | ❌ |
| `make` | Çiz ve yaz | 1,0 | ✅ **tek açık uçlu tip** |

### 2.1 · `cipher` — şifre ve kod · 41 aday

Bu kitabın imzası. Şifre **süs değildir**: çocuk her seferinde gerçek bir
yazı dizgesiyle karşılaşır ve onu okumayı öğrenir.

22 kültürün **hepsinin** kamuya açık bir yazı veya notasyon dizgesi vardır
ve bu, kültür seçiminin ölçütlerinden biriydi:

| Dizge | Kültür | Neden güvenli |
|---|---|---|
| Ogham · Genç Futhark · Orhun runik | İrlanda · İskandinav · Türk | Tarihsel, yaşayan bir ibadetin parçası değil |
| Hiyeroglif · çivi yazısı · Yunan alfabesi | Mısır · Mezopotamya · Yunan | Çözülmüş, yayımlanmış, müzede |
| Hangul · kana · Çince karakter · Devanagari | Kore · Japon · Çin · Hindu | Bugün okulda öğretiliyor |
| Inuktitut hecelemesi | İnuit | Nunavut'ta yol tabelalarında |
| Ton ve imlâ işaretleri | Yoruba · Vietnam · Māori · Hawaii · Zulu | İmlâ herkese açıktır |
| Çubuk-nokta · bayrak-tüy · khipu düğümü | Maya · Aztek · And | Sayı dizgesi, kehanet değil |
| Gün-adları | Akan | Kamuya açık adlandırma dizgesi |

> **Kutsal ad veya ritüel sözcük üzerinden şifre kurulmaz.**
> Ayrıntı: [`CULTURE_POLICY.md § 4`](CULTURE_POLICY.md).

**Alt biçimler:** anahtarla yazma · anahtarla okuma · yön çıkarma
(hangi uçtan başlanır) · birleştirme (iki işaret üçüncüyü kurar) ·
sayı dizgesi.

**Tipik kusur:** anahtar sayfada yok, arka maddede. Çocuk sayfa çevirir
ve pes eder. **Anahtar her zaman aynı açılımdadır.**

### 2.2 · `map` — harita ve rota · 24 aday

Coğrafya bu kitapta bir dekor değil bir **açıklamadır**: hikâyenin neden
o hikâye olduğunu arazi söyler.

**Alt biçimler:** rota izleme · plan okuma (Knossos, ball court, chinampa)
· nehir izleme (Nil, Ganj, Sarı Nehir) · yükseklik kuşağı (And) ·
şekil örtme (Te Ika-a-Māui balık şekli).

**Tipik kusur:** harita çok kalabalık. 8 yaş dört noktadan fazlasını
işaretleyemez.

### 2.3 · `sort` — tasnif ve eşleştirme · 43 aday

**Codex tezinin çocuk hâli** ve kitabın entelektüel omurgası: aynı motif
başka kültürde başka ad alır.

**Alt biçimler:** olay sıralama · eşleştirme · kültürler arası tasnif
(`crossCultureRefs`) · bilinen/bilinmeyen ayrımı · gruplama.

> **"Bilinen ve bilinmeyen" alt biçimi bu kitaba özgüdür.**
> `maya-ballcourt-sort` çocuğa top oyunu hakkında dört önerme verir ve
> hangisinin **kesin**, hangisinin **hâlâ tahmin** olduğunu ayırttırır.
> Bu, bir aktivite kitabının öğretebileceği en yetişkin şeydir:
> bilginin sınırı da bilgidir.

**Tipik kusur:** iki seçenek de savunulabilir → **çift cevap**.
`qa_solvable` (Faz 2) bunu kırmızı yakar.

### 2.4 · `observe` — gözlem levhası · 35 aday

Bir saha defterinin kalbi. Çocuk **bakar**, sayar, etiketler ve bir sonuç
çıkarır.

**Alt biçimler:** parça etiketleme · fark bulma · sayı/veri okuma
(gün uzunluğu, yükseklik, tarih) · örüntü bulma (kente, mon, silindir mühür)
· tekrar birimi bulma.

**Tipik kusur:** levha "bul-boya" seviyesine düşer. Her gözlem
aktivitesi bir **çıkarım** istemelidir, yalnızca bir işaretleme değil.

### 2.5 · `make` — çiz ve yaz · 25 aday

**Tek açık uçlu tip.** `openEnded: true` yalnızca burada olabilir.

> `openEnded` bir kaçış kapısı **değildir**. "Cevabı zor buldum, açık uçlu
> yapayım" demek `qa_solvable`'ı kırmızı yakar.

**Alt biçimler:** tasarla (mühür, glif, bahçe, labirent) · adlandır
(yer adı, kenning, cümle-ad) · yeniden çiz (levhadan) · seç ve gerekçelendir.

**Tipik kusur:** boş bir kutu ve "hayal gücünü kullan". Her `make`
aktivitesi bir **kısıt** taşır: tek yollu labirent, düz çizgili işaret,
suyla dörde bölünmüş bahçe. **Kısıt yaratıcılığı öldürmez, mümkün kılar.**

---

## 3 · On öğrenme boyutu

Her aktivite en az birini taşır. Faz 1 havuzundaki dağılım:

| Boyut | Ne öğretir |
|---|---|
| `pattern-recognition` | Örüntü görme — şifrelerin ve tasnifin temeli |
| `observation` | Bakmayı öğrenme; saha defterinin kendisi |
| `vocabulary` | Kültürün kendi sözcükleriyle |
| `geography` | Arazi hikâyeyi biçimlendirir |
| `storytelling` | Sıra, neden, sonuç |
| `comparative-mythology` | Aynı motif, başka kültür |
| `cultural-comparison` | Aynı ihtiyaç, başka çözüm |
| `memory` | Tutma ve geri çağırma |
| `historical-reasoning` | Kaynak, tarih, kanıt |
| `creative-interpretation` | Kısıtla üretme |

> **Eğitim sayfaya gömülüdür, sayfanın üstüne yazılmaz.** Hiçbir sayfada
> "Öğrendiklerimiz" kutusu yoktur. Çocuk görevi yapar; öğrenme görevin
> içindedir.

---

## 4 · Tip dağılımı ve neden bu dağılım

| Tip | Aday | Oran | Bölge başına asgari |
|---|---:|---:|---:|
| `sort` | 43 | %25,6 | 4 |
| `cipher` | 41 | %24,4 | 3 |
| `observe` | 35 | %20,8 | 2 |
| `make` | 25 | %14,9 | 2 |
| `map` | 24 | %14,3 | 2 |

`sort` ve `cipher` birlikte havuzun **yarısıdır** — çünkü ikisi de
kitabın tezini doğrudan taşır: karşılaştırma ve gerçek yazı.

`make` %15'te tutuldu: açık uçlu aktivite bir aktivite kitabında
gereklidir ama **ölçülemez**. Fazlası, kitabın "kendi kendini doğrulayan"
vaadini zayıflatır ve mühür sistemini besleyemez.

**6 bölge × 5 tip = 30 hücrenin hepsi doludur** ve hiçbiri asgarinin
altında değildir. `qa_matrix.py` bunu her koşuda denetler.

---

## 5 · Zorluk merdiveni

| ★ | Yaş | Adım | İpucu | Havuzda |
|---|---|---|---|---:|
| ★ | 8–10 | ≤2 | yok | 50 |
| ★★ | 9–12 | ≤4 | yok | 90 |
| ★★★ | 10–12 | ≤4 | **kademeli, 2 seviye** | 28 |

★★★ oranı hiçbir bölgede **%30'u aşamaz** (`AGE_POLICY § 6`).

> **Zorluk sabit bir özellik değil, bir tasarım koludur.** Faz 1'de altı
> aday ★★'dan ★'a indirildi çünkü üç bölge en kolay bantta havuzsuz
> kalıyordu — `qa_matrix.py` bunu yakaladı. Bir aday düşerse aynı kol
> yeniden kullanılır: bir ★★ sadeleştirilip ★ olur, adım eklenip ★★★ olur.

---

## 6 · Bir aktivitenin geçmesi gereken beş kapı

```
① şema        → alan adları, malzeme beyaz listesi, boyut zorunluluğu
② kültür      → kademe, izinli tip, yasak biçim        (CULTURE_POLICY)
③ güvenlik    → malzeme → safetyClass                  (AGE_POLICY § 3)
④ araştırma   → hikâye → kültür → kaynak → gerekçe     (SOURCING_STANDARD)
⑤ çözülebilirlik → tek ve doğru cevap                  (Faz 2 · qa_solvable)
```

Faz 1'de ①–④ koşuyor. ⑤ proza yazıldığında doğar.
