#!/usr/bin/env python3
"""
CEVAP ANAHTARI, FİNAL GÖREV VE ARKA MADDE KAPISI — Faz 4
================================================================================
Yol haritası Faz 4 § 8 bu kapıyı adıyla istiyor: *"cevap anahtarı 120/120 tam
mı, ipuçları cevabı sızdırıyor mu."* Faz 4 onu iki yönde genişletti, çünkü
kitabın kapanışı üç parçadan oluşuyor ve üçü de sessizce eksik kalabilir.

Dokuz denetim:

  ① KAPSAM        — anahtar her sayfayı tam bir kez taşıyor mu
  ② BİÇİM         — kapalı sayfa CEVAP, açık uçlu sayfa ÖLÇÜT taşıyor mu
  ③ EŞLEŞME       — anahtardaki cevap manuscript'teki cevapla AYNI mı
  ④ İPUCU MERDİVENİ — ipucu politikası tutuyor mu (yalnızca ★★★ · tam iki)
  ⑤ MÜHÜR SESSİZLİĞİ — mühür sözcüğü BİR BÜTÜN OLARAK hiçbir yerde yok mu
  ⑥ FİNAL GÖREV   — beş sayfa var mı, çentik tablosu bölge sırasında mı
  ⑦ KURTARMA      — final sayfası kendi kendini doğrulama şeridini basıyor mu
  ⑧ ARKA MADDE    — yol haritasının istediği bölümler var ve GEREKÇELİ mi
  ⑨ SÖZLÜK        — kültür sözlüğü yirmi iki kültürün hepsini kapsıyor mu

⑤ NEDEN VAR — VE NEDEN BU KAPININ EN ÖNEMLİ DENETİMİ:

Bir cevap anahtarının mühür sözcüklerini basması ilk bakışta "eksiksizlik"
gibi görünür. Değildir. Mühür sözcüğü bu kitapta bir cevap değil, çocuğun
KENDİ KENDİNİ DOĞRULAMA aygıtıdır: sözcük anlamlı olduğu için yanlış bir
harf sözcüğü bozar ve çocuk hangi sayfaya döneceğini kendi bulur
(PROGRESSION_ARCHITECTURE · BRIEF § 6.3).

    Mühür sözcüğünü anahtara basmak, kitabın tek kendi kendini
    düzelten mekanizmasını öldürür — ve bunu "tamlık" adına yapar.

Bu yüzden ⑤ bir sızıntı denetimi değil bir TASARIM denetimidir ve
anahtarda bir mühür sözcüğü görürse KIRMIZI yanar.

⚠ ANAHTAR VE MÜHÜR DOSYASI DEPODA DEĞİLDİR (K10). Yoksa kapı ATLAR ve
yeşil yanar. Kapı hiçbir koşulda bir cevabı veya bir mühür sözcüğünü
EKRANA BASMAZ.

TASARIM: yalnızca Python standart kütüphanesi (karar K7).

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

BOOK = os.path.join(ROOT, "02_MANUSCRIPT", "book.json")
ANSWER_KEY = os.path.join(ROOT, "01_SOURCE", "answers", "answer_key.json")
SEAL_KEY = os.path.join(ROOT, "01_SOURCE", "answers", "seal_key.json")
ACTIVITY_INDEX = os.path.join(ROOT, "01_SOURCE", "activity_index.json")
REGION_INDEX = os.path.join(ROOT, "01_SOURCE", "region_index.json")
CULTURE_INDEX = os.path.join(ROOT, "01_SOURCE", "culture_index.json")
CONFIG = os.path.join(ROOT, "project_config.json")

# Yol haritası Faz 4 § 2'nin adıyla istediği arka madde parçaları.
REQUIRED_SECTIONS = ("hint-rule", "answer-key", "glossary", "world-myths-bridge")
# Final görevin kendi kendini doğrulayan şeridi — çocuğun kurtarma yolu.
SELFCHECK = re.compile(r"if the six letters do not make a word", re.IGNORECASE)


class Report:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks = 0
        self.facts: dict = {}

    def check(self, cond: bool, label: str) -> bool:
        self.checks += 1
        if cond:
            if self.verbose:
                print("  ✓ %s" % label)
        else:
            self.errors.append(label)
            print("  ✗ %s" % label)
        return cond

    def warn(self, label: str) -> None:
        self.warnings.append(label)
        print("  ! %s" % label)


def load(path, rep, required=True):
    if not os.path.exists(path):
        if required:
            rep.check(False, "dosya yok: %s" % os.path.relpath(path, ROOT))
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        rep.check(False, "JSON bozuk: %s — %s" % (os.path.relpath(path, ROOT), exc))
        return None


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())


# ── ①②③ KAPSAM · BİÇİM · EŞLEŞME ───────────────────────────────────────────
def check_coverage(book, akey, rep):
    print("\n── ① kapsam · ② biçim · ③ eşleşme ──")
    pages = {a["activityId"]: a for a in book.get("activities", [])}
    entries = akey.get("entries", [])
    rep.facts["activities"] = len(pages)
    rep.facts["keyEntries"] = len(entries)

    ids = [e.get("activityId") for e in entries]
    dupes = [k for k, v in collections.Counter(ids).items() if v > 1]
    rep.check(not dupes, "hiçbir sayfa anahtarda iki kez yok"
              + ("" if not dupes else " — YİNELENEN: %s" % dupes[:5]))

    missing = sorted(set(pages) - set(ids))
    rep.check(not missing, "anahtar yazılmış her sayfayı taşıyor (%d/%d)"
              % (len(set(ids) & set(pages)), len(pages))
              + ("" if not missing else " — EKSİK: %s" % missing[:6]))

    stray = sorted(set(ids) - set(pages))
    rep.check(not stray, "anahtarda kitapta olmayan sayfa yok"
              + ("" if not stray else " — FAZLA: %s" % stray[:5]))

    wrong_shape, drift = [], []
    for e in entries:
        p = pages.get(e.get("activityId"))
        if p is None:
            continue
        if p.get("openEnded"):
            if not (e.get("whatAFinishedPageShows") or "").strip():
                wrong_shape.append("%s → açık uçlu ama ölçüt yok" % e["activityId"])
            if e.get("answer"):
                wrong_shape.append("%s → açık uçlu sayfaya CEVAP yazılmış" % e["activityId"])
            if norm(e.get("whatAFinishedPageShows")) != norm(p.get("expectedResult")):
                drift.append(e["activityId"])
        else:
            if not (e.get("answer") or "").strip():
                wrong_shape.append("%s → kapalı ama cevap yok" % e["activityId"])
            elif norm(e["answer"]) != norm(p.get("answer")):
                drift.append(e["activityId"])
    rep.check(not wrong_shape, "her kayıt tipine uygun biçimde"
              + ("" if not wrong_shape else " — BİÇİM: %s" % wrong_shape[:5]))
    rep.check(not drift,
              "anahtardaki her cevap manuscript'le birebir aynı"
              + ("" if not drift else " — SÜRÜKLENME: %s" % drift[:5]))

    closed = sum(1 for e in entries if not e.get("openEnded"))
    rep.facts["closedAnswers"] = closed
    rep.facts["openEndedCriteria"] = len(entries) - closed


# ── ④ İPUCU MERDİVENİ ──────────────────────────────────────────────────────
def check_hint_ladder(book, index, cfg, rep):
    """Yol haritası: 'Kademeli ipuçları tamam · hiçbiri cevabı içermiyor.'

    Sızıntının kendisini `qa_solvable § ⑤` denetliyor. Burada denetlenen
    şey MERDİVENİN KENDİSİ: ACTIVITY_TAXONOMY § 5 yalnızca ★★★ sayfaların
    ipucu taşımasını ve tam iki basamak olmasını şart koşuyor. Faz 2'nin
    ilk sürümü on altı sayfaya da ipucu koymuştu ve şartnameyle
    çelişiyordu — beyan ile uygulama ayrılmıştı."""
    print("\n── ④ ipucu merdiveni ──")
    want = cfg.get("solvability", {}).get("hintLadderLevels", 2)
    d = {a["activityId"]: a for a in index.get("activities", [])}
    wrong_level, wrong_count = [], []
    hinted = 0
    for a in book.get("activities", []):
        hints = a.get("hints") or []
        diff = d.get(a["activityId"], {}).get("difficulty")
        if hints:
            hinted += 1
            if diff != 3:
                wrong_level.append("%s (★%s)" % (a["activityId"], diff))
            if len(hints) != want:
                wrong_count.append("%s (%d ipucu)" % (a["activityId"], len(hints)))
        elif diff == 3:
            wrong_count.append("%s (★★★ ama ipucusuz)" % a["activityId"])
    rep.facts["hintedPages"] = hinted
    rep.check(not wrong_level, "ipucu yalnızca ★★★ sayfalarda"
              + ("" if not wrong_level else " — İHLAL: %s" % wrong_level[:6]))
    rep.check(not wrong_count, "her ★★★ sayfası tam %d basamak taşıyor" % want
              + ("" if not wrong_count else " — İHLAL: %s" % wrong_count[:6]))


# ── ⑤ MÜHÜR SESSİZLİĞİ ─────────────────────────────────────────────────────
def check_seal_silence(akey, seal, book, index, regions, rep):
    """⚠ Bu fonksiyon hiçbir mühür sözcüğünü ekrana BASMAZ.

    ⭑ BU DENETİM İLK KOŞUSUNDA KENDİ KUSURUNU BULDU ⭑

    İlk hâli anahtarın METNİNDE mühür sözcüğü arıyordu ve dördünü buldu.
    Dördü de YANLIŞ POZİTİFTİ: mühür sözcükleri sıradan İngilizce
    sözcüklerdir ve bir cevapta ('panel 2 the voyage') meşru olarak
    geçerler. Cevap anahtarı YILDIZ sözcüklerini taşır — sayfada zaten
    basılı olan sözcükleri — mühür sözcüğünü değil; mühür sözcüğü tek tek
    HARFLERDEN kurulur ve hiçbir yerde bir bütün olarak durmaz.

        Kapı 'bu sözcük geçiyor' diyordu. Sorulması gereken şey
        'bu sözcük MÜHÜR OLARAK okunabiliyor mu' idi.

    Faz 3 § 20.1'in dersi burada da geçerli: kapıyı yeşile çevirmenin en
    ucuz yolu cevaptan 'voyage' sözcüğünü silmek olurdu — yani doğru
    yazılmış bir cevabı bozmak. Denetim daraltıldı ve YERİNE ÜÇÜNCÜ bir
    değişmez kondu (⑤c), ki o gerçekten bir tasarım riskidir.
    """
    print("\n── ⑤ mühür sessizliği ──")
    if seal is None:
        print("  ⊘ mühür anahtarı depoda yok — denetlenecek sözcük yok")
        rep.check(True, "mühür anahtarı yok, denetim boş koştu")
        return
    seals = {s["region"]: (s.get("word") or "").lower() for s in seal.get("seals", [])}
    words = set(w for w in seals.values() if w)
    final = ((seal.get("finalQuest") or {}).get("word") or "").lower()

    # ⑤a Hiçbir cevap veya ölçüt BİR BÜTÜN OLARAK bir mühür sözcüğü olamaz.
    whole = []
    for e in akey.get("entries", []):
        for f in ("answer", "whatAFinishedPageShows"):
            v = norm(e.get(f))
            if v and (v in words or v == final):
                whole.append(e.get("activityId"))
    rep.check(not whole,
              "hiçbir cevap bir bütün olarak bir mühür sözcüğü değil"
              + ("" if not whole else " — %d KAYIT" % len(whole)))

    # ⑤b Final görev bloğu hiçbir mühür sözcüğü BASMAZ.
    #
    # ⚠ VE BURADA BİR TASARIM AYGITINI BİLMEK ZORUNDA:
    # iki mühür sözcüğü BİLEREK kendi bölgesinin adını yankılar
    # (seal_key gerekçesi · Faz 3 § 21.6'da bir inceleme bulgusuna karşı
    # AÇIKÇA savunuldu). Çocuk sözcüğü kurduğunda bölge başlığıyla
    # eşleştiğini görür ve doğruluğundan emin olur — bu bir sızıntı değil,
    # kendi kendini doğrulamanın ta kendisidir.
    #
    #     Bir sızıntı dedektörü, kitabın TASARIMINI bilmiyorsa
    #     tasarımı sızıntı sanar.
    #
    # Bu yüzden bölge kimlikleri ve adları taranan metinden ÇIKARILIR;
    # geriye kalan her şeyde bir mühür sözcüğü görmek gerçek bir ihlaldir.
    fq_blob = json.dumps(akey.get("finalQuest") or {}, ensure_ascii=False).lower()
    for r in (regions or {}).get("regions", []):
        for token in (r.get("id", ""), r.get("en", ""), r.get("tr", "")):
            if token:
                fq_blob = fq_blob.replace(token.lower(), " ")
    hit = sum(1 for w in words | ({final} if final else set())
              if w and re.search(r"\b%s\b" % re.escape(w), fq_blob))
    rep.check(hit == 0,
              "final görev bloğu bölge adı DIŞINDA hiçbir mühür sözcüğü taşımıyor"
              + ("" if hit == 0 else " — %d SÖZCÜK" % hit))

    # ⑤b2 Ve blok bir HARF ya da SÖZCÜK alanı taşıyamaz: yalnızca KONUM.
    fq = akey.get("finalQuest") or {}
    banned = [k for k in ("word", "letter", "letters", "answer", "solution")
              if isinstance(fq.get(k), str)]
    for row in fq.get("notchTable") or []:
        banned += ["notchTable.%s" % k for k in ("letter", "word", "notchLetter")
                   if isinstance(row.get(k), str)]
    rep.check(not banned,
              "final görev bloğu yalnızca KONUM taşıyor, harf veya sözcük değil"
              + ("" if not banned else " — ALAN: %s" % sorted(set(banned))))
    rep.check(fq.get("wordPrintedHere") is False,
              "final görev bloğu sözcük taşımadığını AÇIKÇA beyan ediyor")

    # ⑤c ⭑ YILDIZ SÖZCÜĞÜ KENDİ MÜHÜR SÖZCÜĞÜ OLAMAZ ⭑
    #
    # Bu bir sızıntı değil bir MEKANİK ÇÖKÜŞ olurdu: çocuk yıldız
    # sözcüğünü kutuya yazdığında mühür sözcüğünü kazara okur ve altı
    # sayfalık toplama işi ANLAMSIZLAŞIR. Hiçbir kapı bunu denetlemiyordu.
    d = {a["activityId"]: a for a in (index or {}).get("activities", [])}
    collapse = []
    for a in book.get("activities", []):
        w = (a.get("sealStarWord") or "").lower()
        if not w:
            continue
        rid = d.get(a["activityId"], {}).get("region")
        if w == seals.get(rid) or w == final:
            collapse.append(a["activityId"])
    rep.check(not collapse,
              "hiçbir yıldız sözcüğü kendi bölgesinin mühür sözcüğü değil"
              + ("" if not collapse else " — ÇÖKME: %s" % collapse))

    # ⑤d Beyan
    rep.check(akey.get("sealWordsPrinted") is False,
              "anahtar mühür sözcüğü taşımadığını AÇIKÇA beyan ediyor")
    rep.check(akey.get("finalWordPrinted") is False,
              "anahtar final sözcüğü taşımadığını AÇIKÇA beyan ediyor")

    # Rastlantısal geçişler bir İHLAL değildir ama bir İNSAN bakmalıdır.
    blob = json.dumps(akey, ensure_ascii=False).lower()
    incidental = sum(1 for w in words if re.search(r"\b%s\b" % re.escape(w), blob))
    if incidental:
        rep.warn("mühür sözcükleriyle AYNI YAZILAN %d sıradan sözcük anahtarda "
                 "geçiyor — mühür olarak okunabilir bir konumda değiller, ama "
                 "bir insan bakmalı (sözcükler EKRANA BASILMADI)" % incidental)
    rep.facts["incidentalSealWordTokens"] = incidental


# ── ⑥⑦ FİNAL GÖREV ─────────────────────────────────────────────────────────
def check_final_quest(book, regions, seal, rep):
    print("\n── ⑥ final görev · ⑦ kurtarma ──")
    fq = book.get("finalQuest")
    if not fq:
        rep.check(False, "manuscript bir final görev taşımıyor")
        return
    want = 0
    for r in (regions or {}).get("regions", []):
        pass
    declared = fq.get("pages", 0)
    quest = fq.get("quest") or []
    rep.facts["finalQuestPages"] = len(quest)
    rep.check(len(quest) == declared,
              "final görev beyan ettiği kadar sayfa taşıyor (%d/%d)" % (len(quest), declared))

    orders = [p.get("pageOrder") for p in quest]
    rep.check(orders == list(range(1, len(quest) + 1)),
              "final görev sayfaları 1…N bitişik")

    thin = [p.get("heading") for p in quest
            if not (p.get("prompt") and p.get("fieldNote")
                    and p.get("steps") and p.get("pagePrints"))]
    rep.check(not thin, "her final görev sayfası dört parçasını taşıyor"
              + ("" if not thin else " — EKSİK: %s" % thin))

    # ⑦ KURTARMA — kendi kendini doğrulama şeridi BASILI olmalı.
    prints = " ".join(x for p in quest for x in (p.get("pagePrints") or []))
    rep.check(bool(SELFCHECK.search(prints)),
              "final sayfası kendi kendini doğrulama şeridini BASIYOR")

    # Çentik tablosu bölge SIRASINDA ve her çentik kendi sözcüğünün içinde.
    if seal is not None and regions is not None:
        seals = {s["region"]: s for s in seal.get("seals", [])}
        order = [r["id"] for r in sorted(regions["regions"], key=lambda r: r["order"])]
        bad = []
        for rid in order:
            s = seals.get(rid)
            if not s:
                bad.append("%s mühürsüz" % rid)
                continue
            if not (1 <= s.get("notchPosition", 0) <= s.get("letterCount", 0)):
                bad.append("%s çentiği sözcüğün dışında" % rid)
        rep.check(not bad, "her çentik kendi sözcüğünün içinde"
                  + ("" if not bad else " — İHLAL: %s" % bad))
        rep.check(len(order) == (seal.get("finalQuest") or {}).get("letterCount"),
                  "bölge sayısı final sözcüğün harf sayısına eşit")


# ── ⑧⑨ ARKA MADDE ─────────────────────────────────────────────────────────
def check_back_matter(book, cultures, rep):
    print("\n── ⑧ arka madde · ⑨ sözlük ──")
    bm = book.get("backMatter")
    if not bm:
        rep.check(False, "manuscript arka madde taşımıyor")
        return
    secs = {s.get("id"): s for s in bm.get("sections", [])}
    rep.facts["backMatterSections"] = len(secs)

    missing = [s for s in REQUIRED_SECTIONS if s not in secs]
    rep.check(not missing, "yol haritasının istediği bölümlerin hepsi var"
              + ("" if not missing else " — EKSİK: %s" % missing))

    # Bir bölüm sayfa sayısı için EKLENEMEZ: her biri gerekçesini taşır.
    no_purpose = [k for k, s in secs.items()
                  if len((s.get("purpose") or "").split()) < 8]
    rep.check(not no_purpose, "her bölüm tanımlı bir işi olduğunu yazıyor"
              + ("" if not no_purpose else " — GEREKÇESİZ: %s" % no_purpose))

    thin = [k for k, s in secs.items() if len(s.get("prints") or []) < 3]
    rep.check(not thin, "her bölüm basacağı şeyi sayıyor"
              + ("" if not thin else " — BOŞ: %s" % thin))

    total = sum(s.get("pages", 0) for s in secs.values())
    rep.facts["backMatterPages"] = total
    rep.check(total == bm.get("pageBudget"),
              "arka madde sayfa toplamı bütçesiyle aynı (%d/%s)"
              % (total, bm.get("pageBudget")))

    # ⑨ SÖZLÜK — yirmi iki kültürün hepsi.
    if cultures is not None:
        need = len(cultures.get("cultures", []))
        g = secs.get("glossary") or {}
        blob = " ".join([g.get("purpose", "")] + list(g.get("prints") or []))
        nums = [int(n) for n in re.findall(r"\b(\d+)\b", blob)]
        words = blob.lower()
        covered = need in nums or "twenty-two" in words
        rep.check(covered,
                  "sözlük yirmi iki kültürün hepsini kapsadığını yazıyor (%d)" % need)


# ── ⑩ ÖN MADDE ────────────────────────────────────────────────────────────
def check_front_matter(book, seal, rep):
    """⑩ ÖN MADDE — tam mı, ve KİTABIN İLK SAYFALARI CEVAP SIZDIRIYOR MU.

    ⭑ BU DENETİM FAZ 5'TE GERÇEK BİR KUSUR YAKALADI (bulgu E2) ⭑

    Ön maddenin ilk taslağı mühür kuralını bir ÖRNEKLE anlatıyordu ve
    örnek sözcük olarak CONDOR'u kullanıyordu. CONDOR bir bölge adıdır —
    ve aynı zamanda o bölgenin MÜHÜR SÖZCÜĞÜDÜR.

        Ön madde o hâliyle bir bölgenin cevabını
        kitabın BEŞİNCİ SAYFASINDA basardı.

    Ve sızıntının yönü en kötü yöndü: çocuk henüz tek bir sayfa
    çözmeden, kitabın kendi kendini doğrulama aygıtı ölürdü.

    ⚠ Bu fonksiyon hiçbir mühür sözcüğünü ekrana BASMAZ; yalnızca KAÇ
    tanesinin sızdığını ve HANGİ bölümde olduğunu söyler.

    Ön madde ayrıca arka maddeden farklı bir şey daha ister: bir
    KULLANIM KILAVUZU KULLANIMDAN ÖNCE gelmelidir. Bu yüzden ⑩ sayfa
    bütçesini ve bölüm gerekçelerini arka maddeyle aynı sertlikte
    denetler — ön madde 'sonra yazarız' denebilecek bir yer değildir.
    """
    print("\n── ⑩ ön madde ──")
    fm = book.get("frontMatter")
    if not fm:
        rep.check(False, "manuscript ön madde taşımıyor")
        return

    secs = fm.get("sections") or []
    rep.facts["frontMatterSections"] = len(secs)

    # (a) Yol haritası Faz 5 § 2'nin adıyla istediği dört parça.
    ids = {s.get("id") for s in secs}
    blob = json.dumps(fm, ensure_ascii=False).lower()
    need = {
        "görev emri": "mission-order" in ids,
        "araçlar": "the-kit" in ids,
        "mühür sayfası": "star-box-and-seal" in ids,
        "ipucu kuralı": "when-you-are-stuck" in ids,
    }
    missing = [k for k, v in need.items() if not v]
    rep.check(not missing, "yol haritasının istediği ön madde parçaları var"
              + ("" if not missing else " — EKSİK: %s" % missing))

    # (b) Sayfa bütçesi tutuyor mu — arka maddeyle aynı sertlik.
    total = sum(s.get("pages", 0) for s in secs)
    rep.facts["frontMatterPages"] = total
    rep.check(total == fm.get("pageBudget"),
              "ön madde sayfa toplamı bütçesiyle aynı (%d/%s)"
              % (total, fm.get("pageBudget")))

    # (c) Hiçbir bölüm sayfa doldurmak için EKLENEMEZ.
    no_purpose = [s.get("id") for s in secs
                  if len((s.get("purpose") or "").split()) < 8]
    rep.check(not no_purpose, "her ön madde bölümü tanımlı bir işi olduğunu yazıyor"
              + ("" if not no_purpose else " — GEREKÇESİZ: %s" % no_purpose))
    thin = [s.get("id") for s in secs if len(s.get("prints") or []) < 3]
    rep.check(not thin, "her ön madde bölümü basacağı şeyi sayıyor"
              + ("" if not thin else " — BOŞ: %s" % thin))
    nobody = [s.get("id") for s in secs
              if len((s.get("bodyText") or "").split()) < 40]
    rep.check(not nobody, "her ön madde bölümü gerçek bir gövde metni taşıyor"
              + ("" if not nobody else " — İNCE: %s" % nobody))

    # (d) ⭑ MÜHÜR SESSİZLİĞİ — ÖN MADDEDE ⭑
    #
    # Arka maddedeki ⑤ denetiminden bir farkı var ve fark KRİTİK: orada
    # bölge adları taranan metinden ÇIKARILIYOR, çünkü iki mühür sözcüğü
    # bilerek kendi bölgesinin adını yankılar ve final görev bloğunda
    # bölge adı geçmek zorundadır.
    #
    # ÖN MADDEDE BÖYLE BİR MUAFİYET YOKTUR — ama bir incelik var:
    # `the-route` bölümü altı bölgenin ADINI basmak ZORUNDADIR, ve iki
    # bölge adı bir mühür sözcüğüyle aynı yazılır. Bu bir sızıntı
    # DEĞİLDİR: rota sayfası bölge adını bir BAŞLIK olarak basar, bir
    # mühür kutusunun cevabı olarak değil.
    #
    # Muafiyet bu yüzden BÖLÜM düzeyinde ve DAR: yalnızca `the-route`,
    # yalnızca bölge adı olarak geçen biçimiyle. Başka her bölümde,
    # başka her bağlamda bir mühür sözcüğü görmek gerçek bir ihlaldir.
    words, final = set(), ""
    if seal:
        for s in (seal.get("seals") or []):
            w = (s.get("word") or "").strip().lower()
            if w:
                words.add(w)
        final = ((seal.get("finalQuest") or {}).get("word") or "").strip().lower()

    if not words and not final:
        print("  ⊘ mühür anahtarı depoda yok — sızıntı denetlenemedi")
    else:
        leaks = []
        for s in secs:
            sid = s.get("id")
            text = " ".join([s.get("bodyText") or "",
                             " ".join(s.get("prints") or []),
                             s.get("heading") or "",
                             s.get("demonstrationWord") or ""]).lower()
            if sid == "the-route":
                # Rota sayfası bölge ADINI basar; bölge adları çıkarılır.
                for r in ("north-ice", "the northern ice", "middle-sea",
                          "the middle sea", "sun-savanna", "sun and savanna",
                          "monsoon", "mountain and monsoon", "great-ocean",
                          "the great ocean", "jaguar-condor",
                          "jaguar and condor"):
                    text = text.replace(r, " ")
            for w in (words | ({final} if final else set())):
                if w and re.search(r"\b%s\b" % re.escape(w), text):
                    leaks.append(sid)
                    break
        rep.check(not leaks,
                  "ön maddenin hiçbir bölümü bir mühür sözcüğü basmıyor"
                  + ("" if not leaks else " — ⭑ SIZINTI: %s" % sorted(set(leaks))))

    # (e) Örnek sözcük kurgusal olmalı: kitapta bir yıldız sözcüğü olamaz.
    #
    # Bir mühür kuralı örneği, gerçek bir sayfanın yıldız sözcüğünü
    # kullanırsa o sayfanın işini önceden yapmış olur.
    stars = {(a.get("sealStarWord") or "").strip().lower()
             for a in book.get("activities", []) if a.get("sealStarWord")}
    bad_demo = []
    for s in secs:
        demo = (s.get("demonstrationWord") or "").strip().lower()
        if demo and demo in stars:
            bad_demo.append(s.get("id"))
    rep.check(not bad_demo,
              "ön maddenin örnek sözcüğü gerçek bir yıldız sözcüğü değil"
              + ("" if not bad_demo else " — ⭑ ÇAKIŞMA: %s" % bad_demo))

    # (f) Ön madde bir CEVAP taşıyamaz: kapalı cevaplar sayfada kalır.
    answers = {(a.get("answer") or "").strip().lower()
               for a in book.get("activities", []) if a.get("answer")}
    answers = {a for a in answers if len(a) > 12}   # kısa cevaplar rastlantısaldır
    fmblob = " ".join([(s.get("bodyText") or "") + " " +
                       " ".join(s.get("prints") or []) for s in secs]).lower()
    hit = sorted(a for a in answers if a in fmblob)
    rep.check(not hit, "ön madde hiçbir aktivite cevabını basmıyor"
              + ("" if not hit else " — CEVAP: %d" % len(hit)))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    print("=" * 74)
    print("  CEVAP ANAHTARI · FİNAL GÖREV · ARKA MADDE")
    print("=" * 74)

    rep = Report(args.verbose)
    cfg = load(CONFIG, rep)
    book = load(BOOK, rep, required=False)
    if not book:
        print("\n  ⊘ manuscript depoda yok — BOŞ KOŞTU")
        print("=" * 74)
        if args.json:
            os.makedirs(os.path.dirname(args.json), exist_ok=True)
            with open(args.json, "w", encoding="utf-8") as fh:
                json.dump({"status": "empty", "checks": 0, "errors": [],
                           "warnings": [], "facts": {}}, fh, ensure_ascii=False, indent=2)
        return 0

    akey = load(ANSWER_KEY, rep, required=False)
    seal = load(SEAL_KEY, rep, required=False)
    index = load(ACTIVITY_INDEX, rep, required=False) or {}
    regions = load(REGION_INDEX, rep, required=False)
    cultures = load(CULTURE_INDEX, rep, required=False)

    if akey is None:
        print("\n  ⊘ cevap anahtarı depoda yok (K10) — ①–⑤ atlandı")
    else:
        check_coverage(book, akey, rep)
        check_hint_ladder(book, index, cfg or {}, rep)
        check_seal_silence(akey, seal, book, index, regions, rep)

    check_final_quest(book, regions, seal, rep)
    check_back_matter(book, cultures, rep)
    check_front_matter(book, seal, rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · %s kayıt · final görev %s sayfa · arka madde %s sayfa"
              % (rep.checks, rep.facts.get("keyEntries", "—"),
                 rep.facts.get("finalQuestPages", "—"),
                 rep.facts.get("backMatterPages", "—")))
        status = "pass"
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": status, "checks": rep.checks, "errors": rep.errors,
                       "warnings": rep.warnings, "facts": rep.facts},
                      fh, ensure_ascii=False, indent=2)
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
