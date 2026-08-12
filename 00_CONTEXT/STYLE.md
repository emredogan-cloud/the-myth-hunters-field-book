# STYLE — The Myth Hunter's Field Book

> Sürüm **1.0 · bootstrap**. Faz 2'de **ölçümle** kalibre edilir ve v2.0 olur.
> `project_config.json § style` ve `§ safety` ile senkron kalmalıdır.

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

## 3 · Ölçülen bantlar

| Ölçüt | Hedef | Kapı |
|---|---|---|
| Talimat cümlesi azami | **18 kelime** | `qa_instruction` |
| Cümle ortalaması | 9,0–14,0 kelime | `qa_readability` |
| Okuma seviyesi | 3.–5. sınıf | `qa_readability` |
| Field note | ~25 kelime | `qa_length` |
| Bölge açılışı | ~150 kelime | `qa_length` |
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
