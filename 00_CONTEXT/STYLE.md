# STYLE — The Myth Hunter's Field Book

> Sürüm **1.1 · Faz 1 pilot kalibrasyonu** · 13 Ağustos 2026.
> Faz 2'de **çocuk testiyle** yeniden kalibre edilir ve v2.0 olur.
> `project_config.json § style` ve `§ safety` ile senkron kalmalıdır.
>
> v1.0 → v1.1'de değişen tek şey § 3'tür: tek okunabilirlik bandı,
> **üç ayrı register bandına** ayrıldı. Gerekçe ölçümdür, tercih değil.

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

---

## 3 · Ölçülen bantlar — **register register**

> ### Bir talimat bir anlatı cümlesi değildir.

Bootstrap tek bir bant taşıyordu (9–14 kelime · 3.–5. sınıf) ve o bant
World Myths'in **anlatı** prozasından devralınmıştı. Faz 1 pilotu bandın
bu kitapta yanlış olduğunu **ölçtü**: beş aktivitenin harmanı 8,28
kelime/cümle ve FK 2,95 çıktı — "bandın altında".

Kusur metinde değil ölçümdeydi. Sayfada **üç ayrı register** var:

| Register | Ölçülen (pilot) | Bant | Kapı |
|---|---:|---|---|
| **Talimat** (`Your mission:` + adımlar) | 6,96 kelime · FK 2,03 | 5–11 kelime · FK ≤ 4,0 | `qa_readability` |
| **Field note** (kültürel bilgi) | 10,36 kelime · FK 4,70 | 9–14 kelime · FK 3,0–5,9 | `qa_readability` |
| **İpucu** | 9,38 kelime · FK 2,86 | FK ≤ 4,5 | `qa_readability` |

### Ve bir değişmez

```
fk(talimat)  <  fk(field note)
```

**Bir talimat, tanıttığı içerikten daha zor olamaz.** Olursa çocuk görevi
değil cümleyi çözmeye çalışır. Pilotta 2,03 < 4,70 — geçti.

| Diğer ölçüt | Hedef | Kapı |
|---|---|---|
| Talimat cümlesi azami | **18 kelime** (pilotta en uzun 11) | `qa_readability` · `qa_age` |
| Adım sayısı | ≤4; ★ için ≤2 | `qa_age` |
| Field note boyu | 15–35 kelime (~25) | `qa_readability` |
| Üç heceli sözcük oranı | ≤ %20 (pilotta %3,9) | `qa_readability` |
| Bölge açılışı | ~150 kelime | `qa_length` (Faz 2) |
| ★★★ oranı (bölüm içi) | ≤ %30 | `qa_age` |

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
