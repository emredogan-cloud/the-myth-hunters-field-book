# 02_MANUSCRIPT — bu dizin neden boş

Bu depo **public**tir. Ama "depo public" ile "manuscript public" aynı şey
değildir — ve bu kitapta bir üçüncü katman daha vardır: **cevap anahtarı**.

Depoda **durmayan** üç şey:

1. **Aktivite prozası** — `.gitignore § ①`
2. **Cevap anahtarı** — `.gitignore § ①b`. Bir aktivite kitabının cevapları
   **ürünün kendisidir**; public depoda duran cevaplar ürünü değersizleştirir.
3. **Ham çocuk testi kayıtları** — `.gitignore § ①c`. Depoda yalnızca
   anonim özet durur (`tester-01`, yaş, sonuç).

İkinci hat: `04_BUILD/validate_structure.py` takip edilen dosyaların
**içeriğine** bakar:

- `check_manuscript_leak()` → aktivite metni
- `check_answer_leak()` → cevap alanları
- `check_child_privacy()` → gerçek çocuk adı

Bir yol kalıbı **yeni bir ada konan** dosyayı yakalamaz. Politikayı
disipline değil mekanizmaya bağlarız.

Karar: [`../DECISIONS.md`](../DECISIONS.md) § A1.
