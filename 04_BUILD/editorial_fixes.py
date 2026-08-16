#!/usr/bin/env python3
"""
EDİTORYAL DÜZELTMELER — Aşama 2 · The Myth Hunter's Field Book
================================================================================
Faz 5'in bağımsız incelemesinden **46 bulgu** düzeltilmeden kalmıştı.
Yükleme öncesi denetim en ağır kümeyi yeniden saydı ve **11 sayfada**
cevabın okura çalıştırılmadan verildiğini ölçtü — rapor dokuz demişti;
aynı kusur **ipucu katmanında iki sayfada daha** duruyordu.

    Bir sızıntı, hangi kutuda durduğuyla değil,
    NE YAPTIĞIYLA sınıflanır.

⭑ İKİ AYRI KUSUR SINIFI — VE BUNLAR ZIT YÖNDE DÜZELTİLİR ⭑

  SIZINTI      field note / ipucu / görev satırı bulmaca cevabını
               veriyor  →  METİN CEVAPTAN ARINDIRILIR
               (`DESIGN_SYSTEM § 1.1`: field note bir ÖDÜLDÜR, ipucu değil)

  ÇIKARILAMAZ  yıldız sözcüğü sayfada hiçbir yerde tanımlanmamış
               →  SAYFA SÖZCÜĞÜ ÖĞRETİR
               (`qa_progression`: mühür harfi sayfadan türemek ZORUNDA)

İkisi karıştırılırsa düzeltme kusuru büyütür: bir yıldız sözcüğünü
gizlemek mühür mekaniğini kırar, bir bulmaca cevabını söylemek sayfayı
öldürür.

⭑ ÇÖZÜLEBİLİRLİK KORUNUR — VE BU İKİ SAYFADA DÜZELTMEYİ DEĞİŞTİRDİ ⭑

`mesopotamian-plant-quest-steps` görev satırından *"ends where it
started"* çıkarılınca adım 3 CEVAPSIZ kalıyordu: levha yalnızca
*"Uruk, the king's city"* kartını basıyor, dönüşü basmıyor. Bu yüzden
sızıntı metinden silinirken ADIM da levhanın gerçekten bastığı şeye
bağlandı.

`maori-macron-length` aynı sınıftan: adım 3 bir OLGU HATIRLAMAYA
bağlıydı ("resmî adlar işareti taşır"). Adım GÖZLEME bağlandı; olgu
field note'ta kaldı çünkü artık cevap yolu değil, bağlam.

    Bir sızıntıyı kapatmak, sayfayı çözülemez yapmayı haklı çıkarmaz.

Betik İDEMPOTENTTİR: her düzeltme yalnızca ESKİ metin birebir
eşleşirse uygulanır. İkinci koşu hiçbir şeyi değiştirmez ve
uygulanmamış düzeltme varsa SÖYLER.

  ./04_BUILD/editorial_fixes.py            uygula
  ./04_BUILD/editorial_fixes.py --check    uygulanmamış varsa KIRMIZI

Çıkış kodları:  0 = tamam   1 = KIRMIZI   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BOOK = os.path.join(ROOT, "02_MANUSCRIPT", "book.json")
ANSWER_KEY = os.path.join(ROOT, "01_SOURCE", "answers", "answer_key.json")

# ─────────────────────────────────────────────────────────────────────────
# Her kayıt: (activityId, alan, indeks|None, ESKİ, YENİ, bulgu, gerekçe)
# `indeks` yalnızca liste alanları (steps · hints) içindir.
# ─────────────────────────────────────────────────────────────────────────
FIXES = [
    # ── B5 ────────────────────────────────────────────────────────────────
    ("zulu-two-messengers", "fieldNote", None,
     "Two Zulu messengers are sent out one after the other, each with a "
     "different message. The one sent first stops on the way and arrives last.",
     "Zulu accounts of the first people are told by many families across "
     "southern Africa, and the two messengers appear in most of them. The "
     "animals carry words, not objects.",
     "B5", "field note dört adımın üçünün cevabını veriyordu: sıra, "
           "'sent first' ve 'arrived first'."),

    # ── B6 ────────────────────────────────────────────────────────────────
    ("maya-ballcourt-sort", "fieldNote", None,
     "A Spanish writer watched the Aztec game and wrote its rules down. Other "
     "things we know from balls and courts dug up. The Maya rules were never "
     "written down.",
     "The ball game was played across Mesoamerica for over a thousand years, "
     "by Maya and Aztec cities alike. Courts survive at hundreds of sites, "
     "and a version is still played in western Mexico today.",
     "B6", "field note üç sütunun ÜÇÜNÜ de cevaplıyordu — sayfanın bütün "
           "sınıflandırma işi field note'ta yapılmıştı. ⚠ İlk düzeltme "
           "'Maya' sözcüğünü de düşürmüştü ve `qa_language § atıf` kapısı "
           "onu yakaladı: atıf gereken bir sayfa kültür adını ANMAK "
           "zorundadır. Ad geri kondu, sütun eşlemesi geri konmadı."),

    # ── B7 · sızıntı + ÇÖZÜLEBİLİRLİK ────────────────────────────────────
    ("mesopotamian-plant-quest-steps", "prompt", None,
     "Your mission: order a long journey that ends where it started.",
     "Your mission: order a long Mesopotamian journey from first to last.",
     "B7", "görev satırı adım 3'ün cevabını (başlangıç = bitiş) İLAN "
           "EDİYORDU. ⚠ İlk düzeltme 'put a…' kalıbını beşinci sayfaya "
           "taşımıştı ve `qa_echo` kapısı onu yakaladı (tavan 4); özgün "
           "fiil 'order' korundu, yalnızca sızdıran kuyruk değişti."),
    ("mesopotamian-plant-quest-steps", "fieldNote", None,
     "A king travels a very long way to find one plant, gets it, and loses it "
     "on the way home. The story is written on twelve clay tablets.",
     "This story is written on twelve clay tablets and is one of the oldest "
     "long poems anyone has found. Copies were kept in palace libraries for "
     "more than a thousand years.",
     "B7", "field note kart sırasını üç adımıyla anlatıyordu."),
    ("mesopotamian-plant-quest-steps", "steps", 2,
     "Write where the king is at the beginning and at the end.",
     "Write the name of the king's city.",
     "B7", "⭑ ÇÖZÜLEBİLİRLİK: levha yalnızca 'Uruk, the king's city' "
           "kartını basıyor, KRALIN DÖNDÜĞÜNÜ basmıyor. Sızıntı görev "
           "satırından silinince adım cevapsız kalıyordu; adım levhanın "
           "GERÇEKTEN bastığı şeye bağlandı."),
    ("mesopotamian-plant-quest-steps", "answer", None,
     "1 the king sets out to find the man who survived the flood · 2 he is "
     "shown where the plant grows · 3 he takes the plant and starts home · "
     "4 a serpent takes the plant and he goes on without it · beginning and "
     "end: Uruk",
     "1 the king sets out to find the man who survived the flood · 2 he is "
     "shown where the plant grows · 3 he takes the plant and starts home · "
     "4 a serpent takes the plant and he goes on without it · the king's "
     "city: Uruk",
     "B7", "cevap kaydı yeni adımla hizalandı."),

    # ── B8 ────────────────────────────────────────────────────────────────
    ("aztec-maize-journey-sort", "fieldNote", None,
     "In this Aztec account the people have no maize at all. Quetzalcoatl "
     "watches an ant and follows it to a mountain.",
     "Maize is the crop that made large cities possible in Mesoamerica, and "
     "this Aztec account explains where people first got it. Nahua "
     "communities still tell it today.",
     "B8", "field note birinci, ikinci ve üçüncü kartı SIRASIYLA "
           "anlatıyordu."),

    # ── B9 ────────────────────────────────────────────────────────────────
    ("inuit-syllabic-signs", "fieldNote", None,
     "Inuktitut is written in Nunavut with signs called qaniujaaqpait. One "
     "sign stands for one consonant, and turning that sign changes the vowel "
     "that comes after it.",
     "Inuktitut is written in Nunavut with signs called qaniujaaqpait. The "
     "system was adapted in the 1800s and is used today on road signs, in "
     "schools and in the territory's own laws.",
     "B9", "field note görevin TAM cevabını veriyordu — cevabın üçüncü "
           "bileşeni ('the sign is turned, not changed') birebir oradaydı."),

    # ── B10 ───────────────────────────────────────────────────────────────
    ("japanese-eight-of-everything", "fieldNote", None,
     "In older Japanese writing eight often means simply very many. The gods "
     "are counted as eight million, and nobody ever counted them.",
     "In older Japanese writing the number eight often stands for simply very "
     "many, rather than an exact count. Several other old languages use a "
     "number the same way.",
     "B10", "field note adım 3'ün cevabını birebir veriyordu."),
    ("japanese-eight-of-everything", "hints", 1,
     "A number nobody could ever check is not really a number.",
     "Compare how big the four counts are.",
     "B10", "ipucu adım 3'ün cevabını veriyordu; yerine GÖZLENEBİLİR bir "
            "yöntem kondu."),

    # ── B11 · sızıntı + ÇÖZÜLEBİLİRLİK ───────────────────────────────────
    ("maori-macron-length", "steps", 2,
     "Write the official spelling of the place name.",
     "Write the place name as it is spelled with the macron.",
     "B11", "⭑ ÇÖZÜLEBİLİRLİK: adım bir OLGUYU HATIRLAMAYA bağlıydı "
            "('resmî adlar işareti taşır') ve o olgu yalnızca field "
            "note'taydı — okunmazsa %50 tahmin, okunursa cevap. Adım "
            "levhanın bastığı iki yazımdan GÖZLEMLE seçmeye bağlandı."),

    # ── B12 · ⭑ DÜZELTME YÖNÜ DEĞİŞTİ ⭑ ────────────────────────────────
    #
    # İlk düzeltme field note'tan kafiye olgusunu SİLMİŞTİ. `validate_research`
    # onu reddetti: `CLM-NI-KALEVALA-METRE` kaydı `usedIn: ["field-note"]`
    # diyor — o cümle KAYNAKLI BİR İDDİADIR ve field note onun taşıyıcısıdır.
    #
    #     Kusur field note'un olguyu SÖYLEMESİ değildi;
    #     ADIMIN çocuktan o olguyu yeniden KEŞFETMESİNİ istemesiydi.
    #
    # `DESIGN_SYSTEM § 1.1` field note'u ÖDÜL olarak konumlandırıyor: çocuk
    # aliterasyonu sayar, sonra field note ona bu şiirin neden kafiyesiz
    # olduğunu söyler. Adım 4 o ödülü bir soruya çevirip sayfayı bozuyordu —
    # üstelik YANLIŞ BİR ÖNVARSAYIMLA ("hangi satır", geçerli cevap "hiçbiri").
    #
    # Bu yüzden field note KORUNDU ve ADIM 4 KALDIRILDI.
    ("finnish-alliteration", "steps", 3,
     "Write which line ends with a rhyme.",
     None,
     "B12", "adım YANLIŞ BİR ÖNVARSAYIMLA soruyordu ve cevabı field "
            "note'ta zaten basılı olan KAYNAKLI bir olguydu. Adım "
            "kaldırıldı; olgu ödül olarak kaldı."),
    ("finnish-alliteration", "answer", None,
     "line 1 three circled · line 2 two circled · line 3 three circled · "
     "line 4 two circled · the line that ends with a rhyme: none of them",
     "line 1 three circled · line 2 two circled · line 3 three circled · "
     "line 4 two circled",
     "B12", "kaldırılan adımın cevap kuyruğu da kaldırıldı."),

    # ── B13 ───────────────────────────────────────────────────────────────
    ("greek-labyrinth-cipher", "steps", 3,
     "Write one line saying how the coin and the written stories disagree.",
     "Write one line comparing the coin design with the written stories.",
     "B13", "adım 4, adım 3'ün cevabını İLAN EDİYORDU: uyuşmadıklarını "
            "söyleyerek 'kaybolunamaz' cevabını veriyordu."),

    # ── B14 ───────────────────────────────────────────────────────────────
    ("greek-constellation-plate", "hints", 0,
     "Two of the six names belong to stories about a hunter and a bear.",
     "Look for names that appear together in the same story.",
     "B14", "ipucu 1 adım 3'ün cevabını (Orion · Ursa Major) veriyordu."),
    ("greek-constellation-plate", "hints", 1,
     "The four that go together are drawn touching or nearly touching on the "
     "chart.",
     "The chart shows where each group sits — use it for the last step.",
     "B14", "ipucu 2 adım 4'ün cevabını ('yakın') veriyordu."),

    # ── B15 ───────────────────────────────────────────────────────────────
    ("japanese-turtle-time-plate", "hints", 1,
     "One of these four hangs on a wall.",
     "Look at what each item is, not only at its year.",
     "B15", "ipucu adım 4'ün cevabını (baskı) doğrudan veriyordu."),

    # ── B2 · ÇIKARILAMAZ yıldız sözcüğü (SIZINTININ TERSİ) ───────────────
    ("egyptian-cartouche-key", "fieldNote", None,
     "Egyptian scribes drew an oval ring round a royal name. The ring is a "
     "sign in its own right and it means protection.",
     "Egyptian scribes drew an oval ring round a royal name. The ring is a "
     "sign in its own right, it means protection, and its name is a "
     "cartouche.",
     "B2", "⭑ TERS KUSUR: yıldız sözcüğü 'cartouche' sayfanın HİÇBİR "
           "yerinde tanımlı değildi; sözcük bankası dört seçenek veriyor "
           "ama hiçbiri sayfadan türetilemiyordu. Mühür harfi sayfadan "
           "TÜREMEK ZORUNDA (qa_progression § ②)."),

    # ── B3 · ÇIKARILAMAZ yıldız sözcüğü ──────────────────────────────────
    ("zulu-click-letters", "fieldNote", None,
     "In isiZulu the letters c, q and x are three separate consonants. Each "
     "one is made in a different place in the mouth.",
     "In isiZulu the letters c, q and x are three separate consonants, each "
     "made in a different place in the mouth. Sounds made this way are "
     "called clicks.",
     "B3", "⭑ TERS KUSUR: yıldız sözcüğü 'clicks' sayfada hiç basılmıyordu."),

    # ── B17 · ⭑ OLGUSAL HATA · LEVHA SABİT, DİZGİ ONARIYOR ⭑ ─────────────
    #
    # Levha anahtarı `ㅇ silent` basıyor. Bu YANLIŞTIR: ㅇ yalnızca hece
    # BAŞINDA sessizdir, hece SONUNDA /ng/ okunur. 광주'nun ilk hecesinde
    # ㅇ sondadır. Anahtarı harfi harfine uygulayan bir çocuk `Gwaju`
    # yazar; cevap `Gwangju` der.
    #
    #     Sayfa hem ÇÖZÜLEMEZ hem de bir yazı sistemi hakkında
    #     YANLIŞ BİLGİ öğretiyordu.
    #
    # Anahtar `pagePrints`tedir, yani LEVHANIN İÇİNE çizilmiştir ve
    # kurucunun teslim ettiği sanat değiştirilemez. Ama field note DİZGİ
    # katmanındadır ve eksik kuralı O taşıyabilir.
    #
    #     Sabit bir levhanın hatası, dizgi katmanından onarılabiliyorsa
    #     onarılır — sayfa yanlış kalmaz.
    #
    # Glif metne KONMADI: iç blok yazı tipi (DejaVu Sans) Hangul
    # kapsamaz ve gömülmemiş bir glif tofu basar. Kural glifsiz yazıldı.
    ("korean-hangul-place-names", "fieldNote", None,
     "Hangul is an alphabet with a small fixed set of letters. Once you have "
     "the key, you can sound out a name. You do not need to know any Korean.",
     "Hangul is an alphabet with a small fixed set of letters. The circle "
     "letter is silent at the start of a sound block, but says ng at the end "
     "of one.",
     "B17", "OLGUSAL HATA: levha anahtarı ㅇ'yi sessiz ilan ediyor; hece "
            "sonunda /ng/ okunur ve altı addan biri (Gwangju) tam olarak "
            "buna bağlı. Eksik kural dizgi katmanına kondu."),

    # ── B1 · ⭑ OLGUSAL HATA · İDDİA GÖZLEME ÇEVRİLDİ ⭑ ───────────────────
    #
    # Adım 2 *"never come out onto the ice"* diyordu ve cevap halkalı foku
    # (natsiq) o kümeye koyuyordu. Halkalı fok buzda DİNLENİR ve yavrusunu
    # buz üstündeki kar ininde doğurur — bu, kutup ayısının onu buzda
    # avlamasının nedenidir.
    #
    # Beş hayvandan yalnızca BİRİ (beluga) suyu gerçekten hiç terk etmez;
    # yani sayfanın önvarsayımı ikiye bölünemez. Levha ise üç hayvanı buz
    # çizgisinin üstünde, ikisini altında basıyor ve DEĞİŞTİRİLEMEZ.
    #
    # Bu yüzden adım bir BİYOLOJİ İDDİASINDAN bir GÖZLEME çevrildi:
    # levhanın gerçekten bastığı şey sorulur, cevap aynı kalır ve yanlış
    # bilgi ortadan kalkar.
    ("inuit-sea-creatures-plate", "steps", 1,
     "Tick the two animals that never come out onto the ice.",
     "Tick the two animals drawn below the ice line.",
     "B1", "OLGUSAL HATA: halkalı fok buza çıkar. Adım biyoloji "
           "iddiasından levha gözlemine çevrildi."),
    ("inuit-sea-creatures-plate", "fieldNote", None,
     "These five animals all have Inuktitut names, and the names are still "
     "used every day across Nunavut. Two of the five never leave the water.",
     "These five animals all have Inuktitut names, and the names are still "
     "used every day across Nunavut. Some of them spend far more of their "
     "lives in the water than others.",
     "B1", "field note aynı yanlış iddiayı taşıyordu ve ayrıca adım 2'nin "
           "cevabını sayıyla veriyordu."),

    # ── B19 · CEVAP KAYDI EKSİK ──────────────────────────────────────────
    ("hawaiian-day-length-plate", "answer", None,
     "Hawaiʻi summer 100 winter 67 · latitude 40 degrees summer 100 winter 33 "
     "· latitude 50 degrees summer 100 winter 20 · closest pair: Hawaiʻi · "
     "star box: winter",
     "Hawaiʻi summer 100 winter 67 · latitude 40 degrees summer 100 winter 33 "
     "· latitude 50 degrees summer 100 winter 20 · closest pair: Hawaiʻi · "
     "why the Hawaiian row is different: Hawaiʻi lies nearest the equator, so "
     "its winter day is closest to its summer day · star box: winter",
     "B19", "⭑ EKSİK ÜRÜN: adım 3 ('Write why the Hawaiian row is "
            "different') bir ★★★ sayfanın adımıydı ve CEVABI KAYITTA "
            "YOKTU. Arka madde 'sayfa sırasına göre her sayfa için bir "
            "giriş' vaat ediyor; bu bir üslup kusuru değil, EKSİK BİR "
            "ÜRÜNDÜ."),
]


def jload(p):
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def apply(book, check):
    """`new is None` + `idx` verilmişse o LİSTE ÖĞESİ SİLİNİR.

    Silme ayrı bir işlem olarak gerekiyor: `finnish-alliteration`'ın
    dördüncü adımı yeniden yazılamazdı, çünkü sorduğu şeyin cevabı
    field note'ta KAYNAKLI bir iddia olarak durmak zorundaydı."""
    acts = {a["activityId"]: a for a in book.get("activities", [])}
    applied, pending, broken = [], [], []
    for aid, field, idx, old, new, finding, why in FIXES:
        a = acts.get(aid)
        if a is None:
            broken.append("%s · aktivite YOK: %s" % (finding, aid))
            continue
        cur = a.get(field)
        delete = (new is None and idx is not None)

        if idx is not None:
            if not isinstance(cur, list):
                broken.append("%s · %s.%s liste değil" % (finding, aid, field))
                continue
            if delete and old not in cur:
                applied.append(finding)          # zaten silinmiş
                continue
            if idx >= len(cur):
                broken.append("%s · %s.%s[%d] YOK" % (finding, aid, field, idx))
                continue
            val = cur[idx]
        else:
            val = cur

        if not delete and val == new:
            applied.append(finding)
            continue
        if val != old:
            broken.append("%s · %s.%s ESKİ METİNLE EŞLEŞMİYOR — elle "
                          "değiştirilmiş olabilir" % (finding, aid, field))
            continue
        pending.append((finding, aid, field + ("[sil]" if delete else "")))
        if not check:
            if delete:
                cur.pop(idx)
            elif idx is not None:
                cur[idx] = new
            else:
                a[field] = new
    return applied, pending, broken


def sync_answer_key(book, check):
    """⭑ CEVAP ANAHTARI MANUSCRIPT'LE BİRLİKTE HAREKET ETMEK ZORUNDA ⭑

    `qa_answerkey § ③` iki kaydı birebir karşılaştırıyor ve ilk koşuda
    tam da bunu yakaladı: manuscript düzeltildi, anahtar bayat kaldı.

        Bir cevabı iki yerde tutmak, bir gün ikisinin
        ayrışması demektir — ve ayrıştığı gün ÜRÜN yanlıştır.

    Anahtar burada yeniden yazılmaz; manuscript'ten SENKRONLANIR."""
    if not os.path.isfile(ANSWER_KEY):
        return [], []
    with open(ANSWER_KEY, encoding="utf-8") as fh:
        akey = json.load(fh)
    pages = {a["activityId"]: a for a in book.get("activities", [])}
    drifted = []
    for e in akey.get("entries", []):
        p = pages.get(e.get("activityId"))
        if p is None or p.get("openEnded"):
            continue
        if e.get("answer") and p.get("answer") and e["answer"] != p["answer"]:
            drifted.append(e["activityId"])
            if not check:
                e["answer"] = p["answer"]
    if drifted and not check:
        with open(ANSWER_KEY, "w", encoding="utf-8") as fh:
            json.dump(akey, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
    return drifted, []


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    print("=" * 74)
    print("  EDİTORYAL DÜZELTMELER · Aşama 2")
    print("=" * 74)

    book = jload(BOOK)
    if book is None:
        print("  ⊘ manuscript depoda yok (K10) — BOŞ KOŞTU")
        print("=" * 74)
        return 0

    applied, pending, broken = apply(book, args.check)
    print("  düzeltme kaydı : %d" % len(FIXES))
    print("  zaten uygulanmış: %d" % len(applied))
    print("  uygulanacak     : %d" % len(pending))
    print("  kaynağı bozuk   : %d" % len(broken))

    for f in broken:
        print("     ⛔ %s" % f)

    if broken:
        print("=" * 74)
        return 1

    if args.check:
        if pending:
            print("\n  ✗ %d düzeltme UYGULANMAMIŞ: %s"
                  % (len(pending), [p[0] for p in pending]))
            print("\n  Uygula: ./04_BUILD/editorial_fixes.py")
            print("=" * 74)
            return 1
        drifted, _ = sync_answer_key(book, True)
        if drifted:
            print("\n  ✗ cevap anahtarı manuscript'ten SÜRÜKLENMİŞ: %s" % drifted)
            print("=" * 74)
            return 1
        print("\n  ✅ bütün editoryal düzeltmeler uygulanmış · anahtar senkron")
        print("=" * 74)
        return 0

    if pending:
        with open(BOOK, "w", encoding="utf-8") as fh:
            json.dump(book, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print("\n  yazıldı: %s" % os.path.relpath(BOOK, ROOT))
        for f, aid, fld in pending:
            print("     ✓ %-5s %-34s %s" % (f, aid, fld))
    else:
        print("\n  değişiklik yok")

    drifted, _ = sync_answer_key(book, False)
    if drifted:
        print("\n  cevap anahtarı senkronlandı: %s" % drifted)
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
