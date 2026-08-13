# İLERLEME MİMARİSİ — kitap neden bitirilir

> Bu belge kitabın **ürün** tarafını tanımlar: çocuk neden ikinci sayfaya,
> neden altmışıncı sayfaya, neden son sayfaya gider.
>
> Sürüm 1.0 · 13 Ağustos 2026 · `01_SOURCE/region_index.json` bunu uygular
> · Faz 1'de **donduruldu**; değişiklik kurucu kararı gerektirir (A3)

---

## 1 · Çözülmesi gereken problem

Rafın tamamı **bitirilmeyen** aktivite kitaplarıyla dolu. Çocuk on beş sayfa
çözer, sıkılır, bırakır. Ebeveyn bunu ikinci kez satın almaz.

Jenerik bulmaca kitabında sayfa 12 ile sayfa 96 arasında **hiçbir fark
yoktur** — ilerleme yoktur, dolayısıyla bitirme güdüsü de yoktur.

> Bu kitabın tek bir yapısal cevabı vardır: **çocuk bir yerden bir yere
> gider ve gittiğini görür.**

---

## 2 · Beş hareket

```
BAŞLANGIÇ  →  YOLCULUK  →  İLERLEME  →  KEŞİF  →  TAMAMLANMA
```

| Hareket | Sayfada ne var | Çocuk ne hisseder |
|---|---|---|
| **Başlangıç** | Görev emri · araç listesi · **boş** rota haritası · **boş** mühür sayfası | "Bana bir iş verildi" |
| **Yolculuk** | Altı bölge, sırayla; her biri kendi arazisi ve açılışıyla | "Yer değiştiriyorum" |
| **İlerleme** | Her bölge sonunda bir mühür; rota haritasına işlenir | "Biriktiriyorum" |
| **Keşif** | Bölgeler arası tasnif: aynı motif başka kültürde | "Bunu daha önce gördüm" |
| **Tamamlanma** | Final görev · tasnif tablosu · sertifika | "Bitirdim ve elimde bir şey var" |

**Boş** sözcüğü kritiktir: ön maddedeki harita ve mühür sayfası boş
başlar. Boş bir ızgara doldurulmak ister; dolu bir ızgara bir dekordur.

---

## 3 · Mühür mekaniği

### Nasıl çalışır

```
① Bölge içindeki bazı aktiviteler bir MÜHÜR YUVASI taşır  (sealSlot: 1…N)
② O aktivitenin cevabından TEK BİR HARF yuvaya gider
③ Bölgenin son sayfasında yuvalar sırayla bir SÖZCÜK kurar
④ Çocuk sözcüğü mühür kutusuna yazar → bölge tamamlanır
⑤ Mührün kenarındaki ÇENTİK bir sayı gösterir
⑥ O sıradaki harf FİNAL GÖREVE taşınır
⑦ Altı çentik harfi final görevde tek bir sözcük kurar
```

### Neden bu mekanik

Üç ölçüte göre seçildi:

| Ölçüt | Nasıl karşılanıyor |
|---|---|
| **Basit** | Çocuk tek bir kural öğrenir ve altı kez kullanır |
| **Kendi kendini doğrulayan** | Sözcük **anlamlıdır**; yanlış harf sözcüğü bozar ve çocuk hangi aktiviteye döneceğini bilir |
| **Kırılgan olmayan** | Bir aktivite düşerse yuva başka bir aktiviteye taşınır; mimari değişmez |

> **En önemli özellik ikincisidir.** Çocuk cevap anahtarına bakmadan
> yanlış yaptığını anlayabilir ve **düzeltebilir**. Bu, "pes etmeme"
> vaadinin (BRIEF § 6.3) mekanik karşılığıdır.

### Kurallar — `qa_matrix.py` denetler

| Kural | Gerekçe |
|---|---|
| Yuvalar bitişik: 1…N, boşluk yok | Bir yuva boşsa sözcük kurulamaz |
| Bir yuva **tam bir** aktivite tarafından beslenir | İki aktivite aynı yuvaya harf veremez |
| `openEnded: true` bir aktivite mühre harf **veremez** | Cevabı tek değildir |
| Mühür besleyen aktivite `inherited-provisional` olamaz | Yanlış harf bütün bölgeyi çözülemez yapar |

Son kural bu projenin bel kemiğinin ilerleme sistemine uzanan koludur:
**doğrulanmamış bir devralma, bir bölgeyi kilitleyebilir.**

---

## 4 · Altı bölge ve rota

Bölgeler **kıtaya göre değil araziye göre** kuruldu. Bir saha defteri
iklimi izler, siyasî sınırları değil — ve bu pedagojik bir tercihtir:
çocuk coğrafyanın hikâyeyi biçimlendirdiğini görür.

| # | Bölge | Arazi | Kültür | Aktivite | Mühür |
|---|---|---|---|---:|---:|
| 1 | **The Northern Ice** | buz, kuzey denizleri | 4 | 24 | 5 harf |
| 2 | **The Middle Sea** | Akdeniz, Nil, Fırat–Dicle | 3 | 20 | 6 harf |
| 3 | **Sun and Savanna** | Sahra altı savan | 3 | 16 | 7 harf |
| 4 | **Mountain and Monsoon** | İran yaylası → Himalaya → muson | 5 | 24 | 7 harf |
| 5 | **The Great Ocean** | Pasifik: doğu Asya + Polinezya | 4 | 20 | 6 harf |
| 6 | **Jaguar and Condor** | Mezoamerika + And | 3 | 16 | 6 harf |

**Rota sıralıdır.** Zorluk merdiveni de bu sırayla yükselir: ★★★ oranı
1. bölgede %17, 6. bölgede %25.

### Kota neden eşit değil

Bölge kotası, o bölgenin **kullanılabilir devralınmış hikâye arzıyla**
orantılıdır:

| Bölge | Hikâye | Aktivite | Hikâye başına |
|---|---:|---:|---:|
| north-ice | 12 | 24 | 2,0 |
| middle-sea | 8 | 20 | 2,5 |
| sun-savanna | 5 | 16 | 3,2 |
| monsoon | 11 | 24 | 2,2 |
| great-ocean | 10 | 20 | 2,0 |
| jaguar-condor | 6 | 16 | 2,7 |

Eşit dağıtım (6 × 20) beş hikâyeli bir bölgeden yirmi aktivite çıkarmayı
zorlardı ve bu **tekrar üretir** — `qa_echo`'nun Faz 3'te yakalayacağı
kusurun ta kendisi. Dengesizlik bir kusur değil, bir **azaltmadır**.

---

## 5 · Final görev — The Cartographer's Seal

Altı mühür çentiği altı harf verir; harfler tek bir sözcük kurar.

> **Sözcük bu belgede yoktur.** Cevaplar ürünün kendisidir ve public
> depoya giremez (karar K10). Sözcük `01_SOURCE/answers/seal_key.json`
> içindedir ve o dizin `.gitignore § ①b` ile dışlanmıştır.

Final görevin işi bir bulmacayı bitirmek değil, **kitabın tezini çocuğa
buldurmaktır**: yirmi iki kültür ayrı ayrı değil, birbirine bakarak anlaşılır.

Kapanış üç parça taşır:

1. **Büyük tasnif tablosu** — 22 kültürün ortak motifleri, çocuk doldurur
2. **Saha araştırmacısı sertifikası** — adını yazar
3. **World Myths köprü sayfası** — huninin diğer ucu

---

## 6 · Bir aktivite düşerse ne olur

160 adaylık havuzun asıl işi budur. Bir aktivite kısıt taramasında,
yaş kapısında veya çocuk testinde düşerse:

```
① aktivite  status: dropped  +  droppedReason
② havuzdan aynı bölge × aynı tip bir aday çekilir
③ aktivite mühür besliyorduysa YUVA yeni aktiviteye taşınır
④ mühür sözcüğü DEĞİŞMEZ — mimari sarsılmaz
```

Bu yüzden `sealSlot` bir aktivite özelliği değil, bir **bölge özelliğidir**
ve aktiviteye atanır. Yuva kalıcı, sakini değiştirilebilir.

---

## 7 · Bu mimarinin bilmediği

| Bilinmeyen | Ne zaman öğrenilir |
|---|---|
| Çocuk mühür kuralını yardımsız anlıyor mu | **Faz 2 · çocuk saha testi** |
| Yedi harfli mühür sekiz yaşındaki için uzun mu | **Faz 2** |
| Final görev çok mu zor | **Faz 4 · ayrı çocuk testi** |
| Rota haritası sayfada kaç yer kaplıyor | **Faz 5 · gerçek dizgi** |
