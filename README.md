# The Myth Hunter's Field Book

**A Screen-Free Quest Through 22 Cultures — 120 Puzzles, Maps, Codes and
Challenges for Ages 8–12**

---

## Bu depo nedir

Bu depo bir **kitap üretim sistemidir**, kitabın kendisi değil.

Çocuk aktivite rafı ikiye ayrılmış: bir yanda lisanslı IP ve markalı
kitaplar — kaliteli ama **temasız**. Öbür yanda binlerce jenerik
"Ultimate Activity Book Ages 8-12" — ucuz ve **içeriksiz**. Çocuk
bulmacayı çözünce hiçbir şey öğrenmiyor.

Bu kitap o boşluğu doldurur: 120 görev, 22 kültür, tek bir saha macerası.
Labirent "labirent" değil **Girit labirentidir**; şifre **Ogham alfabesidir**;
eşleştirme aynı motifin **dört kültürdeki** hâlidir.

Depoda duran şey: **devralma manifestosu, aktivite şeması, doğrulama
kapıları, CI/CD, dizgi ve KDP üretim hattı, ölçüm raporları ve belgeler.**

Depoda **durmayan** üç şey: **aktivite prozası**, **cevap anahtarı** ve
**ham çocuk testi kayıtları**. Bir aktivite kitabının cevapları ürünün
kendisidir. Bir yol kalıbı yeni bir ada konan dosyayı yakalamaz, bu yüzden
ikinci bir hat vardır: CI takip edilen dosyaların **içeriğine** bakar.

---

## Durum

| | |
|---|---|
| Faz | **2 · TEKNİK PİLOT TAMAM** · çocuk doğrulaması **BEKLİYOR** |
| Kapı (`.gate`) | `phase1` — **bilerek yükseltilmedi** |
| Aday aktivite | **168** / ≥160 |
| Kilitli aktivite | **16** / 120 — `jaguar-condor` bölgesinin tamamı |
| Yazılmış aktivite | **16** / 120 |
| Devralınan kayıt | **76** · hepsi sha256'lı · **7'si yeniden doğrulandı** |
| Kültür · bölge | **22** · **6** |
| Görsel öğe | 0 / ~150 |
| Kapı öz-testi | **106 denetim** |
| **Sonraki adım** | **KURUCU: A7 — en az iki çocuk testçi** |

> ⚠ **Faz 2 tam olarak kapanmadı.** Teknik pilot geçti; Faz 2'nin PASS
> ölçütü *çocuk testinde ≥%80 yardımsız anlaşılma* ve **0 testçi** var.
> `.gate` bu yüzden `phase1`'de: yapılmamış bir test geçmiş sayılamaz.

Faz 2 raporu: [`06_REPORTS/PHASE_2_REPORT.md`](06_REPORTS/PHASE_2_REPORT.md)
Faz 1 raporu: [`06_REPORTS/PHASE_1_REPORT.md`](06_REPORTS/PHASE_1_REPORT.md)

Ölçülmüş güncel durum: [`BOOK_STATS.md`](BOOK_STATS.md) ·
[`ROADMAP_PROGRESS.md`](ROADMAP_PROGRESS.md)

---

## Bu kitabın iki riski

### Çocuk artık okumuyor — yapıyor
Alıcı ebeveyn, okur çocuktur. Ve çocuk bu kitapta yalnızca okumuyor:
**yazıyor, çiziyor, çözüyor.** Yanlış tonlanmış bir görev, ebeveyn
yorumunda geri döner ve **o yorum silinmez**.
→ [`00_CONTEXT/AGE_POLICY.md`](00_CONTEXT/AGE_POLICY.md)

### Devralma bir kısayol değil, bir sözleşme
Bu kitap *The Great Book of World Myths*'in 22 kültürlük araştırma
tabanından besleniyor. Ama:

> **Bir hikâye anlatmak ile bir aktivite tasarlamak aynı iddia değildir.**

Orada *"bu mitte X olur"* anlatı için yeterlidir. Burada aynı cümle bir
**bulmaca cevabıdır** — yanlışsa çocuk kendini suçlar.

Bu yüzden `inherited-provisional` bir kayda dayanan hiçbir aktivite
`locked` olamaz.
→ [`00_CONTEXT/INHERITANCE_ARCHITECTURE.md`](00_CONTEXT/INHERITANCE_ARCHITECTURE.md)

---

## Hızlı başlangıç

```bash
git clone https://github.com/emredogan-cloud/the-myth-hunters-field-book.git
cd the-myth-hunters-field-book

# Bütün kalite kapıları — CI'ın koştuğu komutun birebir aynısı.
# Hiçbiri venv gerektirmez; hepsi Python standart kütüphanesiyle koşar.
./04_BUILD/qa_all.sh

# Ağır işler (görsel ölçümü, dizgi) için:
python3 -m venv 04_BUILD/.venv
04_BUILD/.venv/bin/pip install -r 04_BUILD/requirements.txt
```

Yeşilse CI de yeşil olur. Kırmızıysa ilerleme yoktur.

---

## Dizin yapısı

```
00_CONTEXT/     proje bağlamı, üslup, yaş politikası, DEVRALMA MİMARİSİ
01_SOURCE/      aktivite envanteri, bölge indeksi, şema, DEVRALMA MANİFESTOSU
02_MANUSCRIPT/  aktivite prozası ve cevap anahtarı — DEPO DIŞINDA (bkz. README)
03_COVER/       kapak çalışması
03_EDITORIAL/   yaş incelemesi, çocuk testi ve ebeveyn okuma kayıtları (anonim)
03_APLUS/       A+ içerik modülleri
04_BUILD/       doğrulayıcılar, kalite kapıları, üretim hattı
05_TESTS/       kapıların kendi testi ve kurgu üreteci
06_REPORTS/     ölçüm raporları ve faz raporları
07_ASSETS/      görseller: raw (salt okunur) → processed → print/kindle/web
08_OUTPUT/      üretilmiş yayın dosyaları — depoda durmaz
09_ARCHIVE/     düşen maddeler ve devre dışı sürümler
```

---

## Altı faz

| Faz | Ad | Kapı |
|---|---|---|
| 1 | Devralma mimarisi, taksonomi, yaş çerçevesi | `phase1` |
| 2 | Pilot: bir bölge + çocuk saha testi | `phase2` |
| 3 | Bölge bloğu I — üç bölge | `phase3` |
| 4 | Bölge bloğu II + final görev | `phase4` |
| 5 | Editoryal yakınsama + sayfa tasarımı | `phase5` |
| 6 | Nihai üretim + KDP paketi | `release` |

Tam yol haritası:
[`THE_MYTH_HUNTERS_FIELD_BOOK_IMPLEMENTATION_ROADMAP.md`](THE_MYTH_HUNTERS_FIELD_BOOK_IMPLEMENTATION_ROADMAP.md)

---

## İzolasyon

Bu proje `CODEX_BESTIARIUM`, `THE-GREAT-BOOK-OF-WORLD-GAMES` ve
`CODEX-ENIGMATICA`'dan **tamamen ayrıdır**. Ortak dosya, ortak build,
ortak `.gate` yoktur.

`THE-GREAT-BOOK-OF-WORLD-MYTHS`'ten **veri devralır** — ama ona **bağlı
değildir**: o deponun kardeş dizinde bulunması zorunlu değildir ve bu depo
onsuz da klonlanır, test edilir, CI'ı yeşil yanar. Devralma bir
*kopyalama + köken kaydı*dır.

Taşınan disiplin ve gerekçeleri:
[`00_CONTEXT/LESSONS_FROM_CODEX.md`](00_CONTEXT/LESSONS_FROM_CODEX.md)

---

## Lisans ve künye

Yayıncı: **Vâliçe Press** · Belgeler Türkçe, kitap İngilizcedir.
