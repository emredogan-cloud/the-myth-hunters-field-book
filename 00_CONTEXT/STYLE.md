# STYLE — The Myth Hunter's Field Book

> Sürüm **1.2 · Faz 2 pilot ölçümü** · 13 Ağustos 2026.
> `project_config.json § style` ve `§ safety` ile senkron kalmalıdır.
>
> v1.1 → v1.2'de bantlar **DEĞİŞMEDİ**. Değişen şey, bantların artık 5
> değil **16 gerçek sayfayla** ölçülmüş olması ve iki yeni kuralın
> (§ 2.1 mühür kuralı · § 3.1 talimat tabanı) eklenmesidir.
>
> ---
>
> ### ⚠ BU BELGE v2.0 DEĞİLDİR VE OLAMAZ
>
> Yol haritası Faz 2 teslimatını *"`STYLE.md` v2.0 — **ölçümle** kalibre"*
> diye tanımlıyor ve o ölçümün adı **çocuk testidir**.
>
> **Çocuk testi yapılmadı** (karar A7 · 0 testçi). Bu belgeyi v2.0
> numaralamak, yapılmamış bir testin sonucunu ima etmek olurdu.
>
> v2.0 numarası **ilk gerçek çocuk oturumuna ayrılmıştır**.

---

## 1 · Ses

Çocuğa **doğrudan** hitap eden, sıcak, hızlı, küçümsemeyen bir saha
araştırmacısı sesi. Okur bir öğrenci değil, bir **meslektaştır**.

| ✅ | ❌ |
|---|---|
| "Your mission: find the three names hidden in this plate." | "Now, little explorer, let's learn about names!" |
| "Field note: the Inuit called this creature by two names." | "Did you know that the Inuit people had many names?" |
| "Draw the guardian you would put at this gate." | "Try your best to draw something nice!" |

---

## 2 · Sayfa dili — sabit kalıplar

Sayfa üç sabit kalıpla kurulur ve bu kalıplar **değişmez**:

```
Your mission: …        → görev satırı, her aktivitenin başında
Field note: …          → kültürel bilgi kutusu, ~25 kelime
Write your answer …    → yazma alanı yönlendirmesi
```

Talimatlar emir kipinde ve ikinci tekil şahıstadır:
*Solve the cipher.* · *Draw the creature.* · *Match each name to its culture.*

`qa_instruction.py § ①` adımın **tanınmış bir emir fiiliyle** başlamasını
şart koşar. Liste kapalıdır; yeni bir fiil eklemek bilinçli bir karardır.

---

## 2.1 · Mühür kuralı — **çocuk bunu bir kez öğrenir, altı kez kullanır**

Faz 2 mühür harfinin sayfaya nasıl bağlandığını dondurdu:

```
Mühür taşıyan her sayfada YILDIZLI bir kutu vardır.
Yıldızın içindeki küçük sayı, o kutuya yazılan sözcüğün
KAÇINCI harfinin mühre gideceğini söyler.
```

**Yıldızlı kutuya yazılan sözcük sayfada BASILIDIR** — bir etiket, bir
sözcük bankası girdisi veya anahtarın bir satırı. Çocuk onu **kopyalar,
üretmez**.

Üç şeyi birden çözdüğü için böyle:

| Sorun | Nasıl çözülüyor |
|---|---|
| Yanlış yazım | Sözcük basılı; çocuk harf uydurmuyor |
| Diakritik kazası | Aynı gerekçe — kopyalanan şey doğrudur |
| Sayısal cevaptan harf çıkarma | Cevap sayı olsa bile yıldızlı kutu **sözcük** ister |

`qa_solvable.py § ⑦` harfi **yeniden hesaplar** ve elle yazılmış bir
`sealContribution` ile ayrıldığı an kırmızı yanar.

---

## 3 · Ölçülen bantlar — **register register**

> ### Bir talimat bir anlatı cümlesi değildir.

Bootstrap tek bir bant taşıyordu (9–14 kelime · 3.–5. sınıf) ve o bant
World Myths'in **anlatı** prozasından devralınmıştı. Faz 1 pilotu bandın
bu kitapta yanlış olduğunu **ölçtü**: beş aktivitenin harmanı 8,28
kelime/cümle ve FK 2,95 çıktı — "bandın altında".

Kusur metinde değil ölçümdeydi. Sayfada **üç ayrı register** var:

| Register | Faz 1 (5 sayfa) | **Faz 2 (16 sayfa)** | Bant | Kapı |
|---|---:|---:|---|---|
| **Talimat** (`Your mission:` + adımlar) | 6,96 · FK 2,03 | **6,42 · FK 0,75** | 5–11 kelime · FK ≤ 4,0 | `qa_readability` |
| **Field note** (kültürel bilgi) | 10,36 · FK 4,70 | **11,45 · FK 4,02** | 9–14 kelime · FK 3,0–5,9 | `qa_readability` |
| **İpucu** | 9,38 · FK 2,86 | **7,34 · FK 1,63** | FK ≤ 4,5 | `qa_readability` |

Üç register de bantta. Ama iki hareket var ve ikisi de **kasıtlıdır**:

- **Field note yukarı çıktı** (4,70 → 4,02'ye düştü ama kelime 10,36 →
  11,45'e çıktı). Kültürel bilgi kutuları daha uzun, daha somut cümlelerle
  yazıldı ve daha az soyut sözcük kullandı.
- **Talimat aşağı indi** (2,03 → 0,75). Adımlar tek işleme indirildi ve
  çok heceli sözcükler talimattan **field note'a taşındı**.

### Ve bir değişmez

```
fk(talimat)  <  fk(field note)
```

**Bir talimat, tanıttığı içerikten daha zor olamaz.** Olursa çocuk görevi
değil cümleyi çözmeye çalışır. Faz 1'de 2,03 < 4,70; Faz 2'de
**0,75 < 4,02** — arada üç sınıflık bir boşluk var ve bu boşluk kasıtlıdır.

---

## 3.1 · Talimat registerinin TABANI yoktur — ve bu bilinçli

Faz 2 talimat FK'sı **0,75**'e indi. Bant yalnızca bir tavan taşıyor
(≤ 4,0) ve bir taban **eklenmeyecek**.

Gerekçe: bir talimatın kolaylığının alt sınırı yoktur.

> *"Count the dots beside each basket."*

Yedi kelime, hepsi tek heceli, FK ölçeğinde neredeyse sıfır. Ve sekiz
yaşındaki için **doğru cümle budur**. Onu zorlaştırmak metni kötüleştirir.

Ölçülmesi gereken şey talimatın kolaylığı değil, talimat ile içerik
**arasındaki mesafedir** — onu da değişmez ölçüyor.

> **Bir metriğe taban koymak, metriği hedefe çevirir.**
> Bu kitapta hedef metrik değil, çocuğun görevi anlamasıdır.

| Diğer ölçüt | Hedef | Faz 2 ölçümü | Kapı |
|---|---|---:|---|
| Talimat cümlesi azami | **18 kelime** | **11** | `qa_readability` · `qa_instruction` |
| Adım sayısı | ≤4; ★ için ≤2 | ort **2,69** · azami 3 | `qa_instruction` · `qa_age` |
| Field note boyu | 15–35 kelime (~25) | **20–27** · ort 23,6 | `qa_readability` |
| Üç heceli sözcük oranı | ≤ %20 | **%2,0** | `qa_readability` |
| Bölge açılışı | ~150 kelime | **145** | ölçüldü |
| ★★★ oranı (bölüm içi) | ≤ %30 | **%25,0** | `qa_age` |
| Adım tek işlem mi | zorunlu | 16/16 | `qa_instruction § ⑥` |
| Yazma alanı var mı | zorunlu | 16/16 | `qa_instruction § ⑧` |

---

## 4 · Yasak kalıplar

- "sadece … değil, aynı zamanda" / "not only … but also"
- "dive into" · "unlock the secrets" · "embark on a journey"
- "little explorer" · "young reader" · her türlü küçümseyen hitap
- Ünlem yığını (bir sayfada ikiden fazla `!`)
- Retorik soru zinciri ("Ready? Excited? Let's go!")

---

## 5 · Bulmaca içerikten türer, süslenmez

Bu kitabın rakiplerinden ayrıldığı tek yer budur ve üslup kuralı hâline gelir:

| ❌ Dekoratif tema | ✅ İçerikten türeyen |
|---|---|
| Rastgele bir labirent, üstünde ejderha resmi | **Girit labirenti** — mitin kendisi |
| Rastgele bir şifre | **Ogham** veya **runik** alfabe — gerçek yazı sistemi |
| Rastgele bir eşleştirme | Aynı motifin **dört kültürdeki** hâli — Codex tezinin çocuk biçimi |

Bir aktivite "hangi mitolojik bilgiyi öğretiyor" sorusuna cevap veremiyorsa
**dekoratiftir ve kitaba girmez**.

---

## 6 · Belirsizlik gizlenmez

Kaynaklar çeliştiğinde metin bunu söyler — çocuk diliyle:

> *"Different storytellers tell this part differently. Some say three
> brothers, some say five. Write down the number you think fits best."*

Bu bir zaaf değil, **öğretici bir andır**: çocuk bilginin tek biçimli
olmadığını öğrenir.
