#!/usr/bin/env python3
"""
TEKRAR VE KÜLTÜREL DÜZLEŞME KAPISI — The Myth Hunter's Field Book
================================================================================
Faz 2 raporu bu kapıyı adıyla istedi ve gerekçesini de yazdı:

    Tek hikâyeli kültürler (Zulu · And) tekrar gibi okunuyor mu?

Bir aktivite kitabının en sinsi kusuru budur. Altı bölge ayrı ayrı
kusursuz olabilir ve kitap yine de TEK BİR SES gibi okunabilir — çünkü
yazan tek kişidir ve insan eli kendi kalıbına döner. Bunu 120. sayfada
fark etmek geç olur: o noktada düzeltmek yeniden yazmaktır.

⭑ BU KAPININ EN ÖNEMLİ KURALI — NE OLMADIĞI ⭑

    Bu kapı "her şey farklı olsun" demez ve diyemez.

Bir aktivite kitabı KASITLI TEKRAR üzerine kurulur ve bu bir kusur
değil bir tasarımdır:

    "Copy that letter into the seal slot."   → çocuk bunu bir kez
                                                öğrenir, altı kez kullanır
    "Number them from first to last."        → sıralama görevinin kalıbı
    "Your mission: …"                        → sayfanın imzası

Bir sayfa dili KALIP demektir. Kalıbı cezalandıran bir kapı, kitabın
öğrettiği alışkanlığı bozar ve çocuğu her sayfada yeniden okumaya
zorlar. Bu yüzden yapısal nakaratlar `project_config § echo.allowedRefrains`
içinde AÇIKÇA BEYAN EDİLİR — yani bir karar olurlar, bir kaza değil.

Ve beyan bir muafiyet değildir: § ⑥ her nakaratın kaç sayfayı kapladığını
ÖLÇER. Bir nakarat sayfaların yarısından çoğunu kaplıyorsa, o artık bir
kalıp değil bir ŞABLONDUR ve kapı kırmızı yanar.

⭑ İKİNCİ KURAL — KÜLTÜREL TERİM CEZALANDIRILMAZ ⭑

Bir Maya sayfası "Maya" der. Bir hangul sayfası "hangul" der. Beş
Çin sayfasının beşinde de "Chinese" geçer ve bu bir tekrar DEĞİL bir
ATIF ZORUNLULUĞUDUR (`qa_age § ⑨` onu ayrıca şart koşuyor).

İki kapı birbirine ters çalışamaz. Bu yüzden ölçümden ÖNCE bütün
kültürel terimler MASKELENİR: kültür adları, yazı dizgesi terimleri,
sayfanın kendi özel adları. Geriye kalan şey yazarın KENDİ dilidir ve
tekrar tam olarak orada aranır.

Altı denetim:

  ① AÇILIŞ KALIBI    — field note'lar aynı iskeletle mi başlıyor
  ② GÖREV KALIBI     — görev satırları aynı biçimle mi kuruluyor
  ③ DÜZLEŞTİRİCİ DİL — "ancient peoples believed" sınıfı kapalı liste
  ④ SAYFA BENZERLİĞİ — iki sayfanın field note'u fazla mı örtüşüyor
  ⑤ TEK KAYNAKLI KÜLTÜR — tek hikâyeden çok sayfa üreten kültürler
  ⑥ NAKARAT PAYI     — beyan edilmiş kalıp kitabı ele geçirmiş mi

③ NEDEN KAPALI LİSTE: kültürel düzleşme bir üslup meselesi değil bir
ZARARDIR ve sezgiselle aranmaz. Liste kısa, açık ve tartışılabilir
olmalıdır — çünkü ona bir şey eklemek editoryal bir karardır.

⑤ NEDEN VAR: kotası hikâye arzıyla orantılı verilmiştir (K15) ama
orantı mükemmel değildir. Zulu'nun bir kullanılabilir hikâyesi ve dört
aktivitesi var. Aynı hikâyeden dört sayfa üretmek, dördünü de aynı
cümlelerle yazmanın en kısa yoludur. Kapı o kültürleri ADIYLA izler ve
onlara DAHA SIKI bir eşik uygular.

⚠ MANUSCRIPT DEPODA DEĞİLDİR. Dosya yoksa kapı BOŞ KOŞAR ve yeşil yanar;
körlüğü `05_TESTS/selftest.py § ⑮` kapatır.

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

CONFIG = os.path.join(ROOT, "project_config.json")
ACTIVITY_INDEX = os.path.join(ROOT, "01_SOURCE", "activity_index.json")
CULTURE_INDEX = os.path.join(ROOT, "01_SOURCE", "culture_index.json")
BOOK = os.path.join(ROOT, "02_MANUSCRIPT", "book.json")

MASK = "□"          # maskelenmiş kültürel terim

# ── ③ DÜZLEŞTİRİCİ DİL ─────────────────────────────────────────────────────
# Kapalı liste. Her madde bir HALKI tekilleştiren, geçmişe hapseden ya da
# egzotikleştiren bir kalıptır. Eklemek editoryal bir karardır.
FLATTENING = [
    (r"\bancient\s+peoples?\b",            "'ancient people' — halkı çağa hapseder"),
    (r"\bthese\s+people\s+(?:believed|thought|felt)\b",
                                           "'these people believed' — tekilleştirme"),
    (r"\bprimitive\b",                     "'primitive'"),
    (r"\bexotic\b",                        "'exotic'"),
    (r"\bmysterious\s+(?:people|tribe|land|ritual)\b", "'mysterious …'"),
    (r"\bsimple\s+(?:folk|people|tribe)\b", "'simple folk'"),
    (r"\ba\s+tribe\s+of\b",                "'a tribe of'"),
    (r"\blong\s+ago\s+in\s+a\s+far\b",     "'long ago in a far…' — masal açılışı"),
    (r"\bthey\s+had\s+no\s+(?:science|writing|idea)\b",
                                           "'they had no science/writing' — eksiklikle tanımlama"),
    (r"\bstrange\s+(?:custom|ritual|belief)s?\b", "'strange custom'"),
    (r"\bsuperstition\b",                  "'superstition'"),
    (r"\bthe\s+natives?\b",                "'the natives'"),
]
FLATTENING_RE = [(re.compile(p, re.IGNORECASE), name) for p, name in FLATTENING]

WORD = re.compile(r"[a-z0-9']+")
# Ölçüme KATILMAYAN işlev sözcükleri: bunların tekrarı bir üslup değil,
# İngilizcenin kendisidir.
STOP = {
    "a", "an", "the", "and", "or", "but", "if", "so", "then", "than", "that",
    "this", "these", "those", "it", "its", "is", "are", "was", "were", "be",
    "been", "of", "in", "on", "to", "into", "from", "with", "for", "at", "by",
    "as", "you", "your", "yours", "they", "them", "their", "he", "she", "his",
    "her", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "not", "no", "all", "each", "every", "some", "any", "can",
    "will", "would", "has", "have", "had", "do", "does", "did", "there",
    "here", "up", "down", "out", "over", "under", "when", "where", "which",
    "who", "what", "how", "why", "own", "same", "other", "more", "most",
}


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


def merged(index_doc, book_doc):
    design = {a["activityId"]: a for a in (index_doc or {}).get("activities", [])}
    out = []
    for p in (book_doc or {}).get("activities", []):
        base = dict(design.get(p.get("activityId"), {}))
        base.update(p)
        out.append(base)
    return out


# ═══════════════════════════════════════════════════════════════════════════
# MASKELEME — bu kapının bel kemiği
#
# Kültürel terim tekrar SAYILMAZ. Maskelenen şeyler:
#   · kültür adları ve eşanlamlıları        (culture_index)
#   · yazı dizgesi terimleri                (culture_index § writingSystem)
#   · sayfanın kendi özel adları            (büyük harfle başlayan sözcükler)
#   · Latin dışı her şey                    (Çince, hangul, kana, Devanagari…)
#
# Geriye kalan, yazarın kendi cümle kurma alışkanlığıdır. Tekrar orada
# aranır ve YALNIZCA orada anlamlıdır.
# ═══════════════════════════════════════════════════════════════════════════
def build_culture_terms(cultures) -> set[str]:
    terms: set[str] = set()
    for c in cultures:
        for field in ("id", "name", "nameTr"):
            v = c.get(field)
            if v:
                terms |= set(WORD.findall(v.lower()))
        ws = c.get("writingSystem") or ""
        # Yazı dizgesi açıklaması Türkçedir; içinden yalnızca ÖZEL ADLARI
        # ve parantez içi terimleri alıyoruz — açıklamanın kendisi değil.
        for tok in re.findall(r"[A-ZĀĒĪŌŪ][\wʻ'’Ā-ſ]+", ws):
            terms.add(tok.lower())
        for tok in re.findall(r"\(([^)]*)\)", ws):
            terms |= set(WORD.findall(tok.lower()))
        for s in c.get("usableStories", []):
            terms |= {t for t in s.split("-") if len(t) > 2}
    terms |= {"maya", "aztec", "andean", "khipu", "chinampa", "nahuatl"}
    return {t for t in terms if len(t) > 2}


def mask_text(text: str, culture_terms: set[str]) -> list[str]:
    """Metni maskelenmiş belirteç listesine çevirir."""
    if not text:
        return []
    out = []
    for raw in re.findall(r"\S+", text):
        bare = raw.strip(".,;:!?()[]\"'—·").strip()
        low = bare.lower()
        toks = WORD.findall(low)
        if not toks:
            out.append(MASK)           # Latin dışı: karakter, kana, hangul…
            continue
        # Özel ad → maske. Cümle başındaki büyük harf sayılmaz; bunu
        # yaklaşık olarak ayırt etmek için sözcüğün İÇİNDE de büyük harf
        # ya da diakritik aranır, ya da terim listesine bakılır.
        if any(t in culture_terms for t in toks):
            out.append(MASK)
            continue
        if bare[:1].isupper() and (len(out) > 0):
            out.append(MASK)
            continue
        if re.search(r"[À-ɏʻḀ-ỿ]", bare):
            out.append(MASK)
            continue
        out.append(toks[0])
    return out


def content_tokens(masked: list[str]) -> set[str]:
    return {t for t in masked if t != MASK and t not in STOP and len(t) > 2}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def norm_refrain(s: str) -> str:
    return " ".join(WORD.findall(s.lower()))


# ── ① AÇILIŞ KALIBI ────────────────────────────────────────────────────────
def check_openers(acts, terms, cfg, rep):
    print("\n── ① field note açılış kalıbı ──")
    n = cfg.get("openerTokens", 4)
    limit = cfg.get("openerMaxPages", 3)
    groups = collections.defaultdict(list)
    for a in acts:
        m = mask_text(a.get("fieldNote", ""), terms)
        if len(m) < n:
            continue
        groups[" ".join(m[:n])].append(a)
    bad = []
    for shape, pages in sorted(groups.items()):
        cultures = {p.get("culture") for p in pages}
        if len(pages) > limit and len(cultures) > 1:
            bad.append("'%s…' → %d sayfa / %d kültür"
                       % (shape, len(pages), len(cultures)))
    rep.facts["openerShapes"] = len(groups)
    rep.check(not bad,
              "hiçbir field note açılışı %d sayfadan çoğunu kaplamıyor" % limit
              + ("" if not bad else " — KALIP: %s" % bad[:4]))


# ── ② GÖREV KALIBI ─────────────────────────────────────────────────────────
def check_mission_shapes(acts, terms, cfg, rep):
    print("\n── ② görev satırı kalıbı ──")
    n = cfg.get("missionTokens", 3)
    limit = cfg.get("missionMaxPages", 4)
    groups = collections.defaultdict(list)
    for a in acts:
        p = re.sub(r"^\s*your mission:\s*", "", a.get("prompt", ""),
                   flags=re.IGNORECASE)
        m = mask_text(p, terms)
        if len(m) < n:
            continue
        groups[" ".join(m[:n])].append(a)
    bad = ["'%s…' → %d sayfa" % (s, len(p))
           for s, p in sorted(groups.items())
           if len(p) > limit and len({x.get("culture") for x in p}) > 1]
    rep.facts["missionShapes"] = len(groups)
    rep.check(not bad,
              "hiçbir görev satırı kalıbı %d sayfadan çoğunu kaplamıyor" % limit
              + ("" if not bad else " — KALIP: %s" % bad[:4]))


# ── ③ DÜZLEŞTİRİCİ DİL ─────────────────────────────────────────────────────
def check_flattening(acts, rep):
    print("\n── ③ kültürel düzleştirici dil ──")
    hits = []
    for a in acts:
        blob = " ".join([a.get("prompt", ""), a.get("fieldNote", "")]
                        + list(a.get("steps") or [])
                        + list(a.get("hints") or []))
        for rx, name in FLATTENING_RE:
            if rx.search(blob):
                hits.append("%s → %s" % (a["activityId"], name))
    rep.check(not hits, "düzleştirici kalıp yok"
              + ("" if not hits else " — İHLAL: %s" % hits[:5]))


# ── ④ SAYFA BENZERLİĞİ ─────────────────────────────────────────────────────
def check_similarity(acts, terms, cfg, rep):
    print("\n── ④ field note örtüşmesi ──")
    thr = cfg.get("fieldNoteJaccardMax", 0.55)
    toks = {}
    for a in acts:
        t = content_tokens(mask_text(a.get("fieldNote", ""), terms))
        if len(t) >= 4:
            toks[a["activityId"]] = (t, a.get("region"), a.get("culture"))
    worst = 0.0
    pairs = []
    ids = sorted(toks)
    for i, x in enumerate(ids):
        for y in ids[i + 1:]:
            tx, rx, cx = toks[x]
            ty, ry, cy = toks[y]
            j = jaccard(tx, ty)
            worst = max(worst, j)
            if j >= thr:
                pairs.append("%s ↔ %s (%.2f)" % (x, y, j))
    rep.facts["fieldNoteJaccardMax"] = round(worst, 3)
    rep.check(not pairs,
              "hiçbir iki field note eşiği aşmıyor (en yüksek %.2f < %.2f)"
              % (worst, thr)
              + ("" if not pairs else " — ÖRTÜŞME: %s" % pairs[:4]))


# ── ⑤ TEK KAYNAKLI KÜLTÜR ──────────────────────────────────────────────────
def check_single_source(acts, cultures, terms, cfg, rep):
    """Tek hikâyeden çok sayfa üreten kültürler EN YÜKSEK tekrar riskidir.

    Faz 2 raporu bu kapıyı tam olarak bunun için istedi. Eşik burada
    genel eşikten SIKIDIR: aynı hikâyeden yazılmış iki sayfa zaten aynı
    sözcük havuzundan besleniyor ve benzemek için çabalamasına gerek yok.
    """
    print("\n── ⑤ tek kaynaklı kültürler ──")
    thr = cfg.get("singleSourceJaccardMax", 0.40)
    cmap = {c["id"]: c for c in cultures}
    watched = []
    bad = []
    by_culture = collections.defaultdict(list)
    for a in acts:
        by_culture[a.get("culture")].append(a)

    for cid, pages in sorted(by_culture.items()):
        c = cmap.get(cid)
        if not c:
            continue
        stories = len(c.get("usableStories") or [])
        if stories > 1 or len(pages) < 2:
            continue
        watched.append("%s (%d hikâye → %d sayfa)" % (cid, stories, len(pages)))
        toks = [(p["activityId"],
                 content_tokens(mask_text(p.get("fieldNote", ""), terms)))
                for p in pages]
        for i, (x, tx) in enumerate(toks):
            for y, ty in toks[i + 1:]:
                j = jaccard(tx, ty)
                if j >= thr:
                    bad.append("%s ↔ %s (%.2f)" % (x, y, j))
    rep.facts["singleSourceCultures"] = watched
    if watched:
        print("  · izlenen: %s" % ", ".join(watched))
    rep.check(not bad,
              "tek kaynaklı kültürlerin sayfaları birbirine benzemiyor "
              "(eşik %.2f)" % thr
              + ("" if not bad else " — TEKRAR: %s" % bad[:4]))


# ── ⑥ NAKARAT PAYI ─────────────────────────────────────────────────────────
def check_refrains(acts, cfg, rep):
    """Beyan edilmiş nakarat bir MUAFİYET DEĞİL bir BÜTÇEDİR.

    Kasıtlı tekrar bu kitabın tasarımıdır: çocuk mühür kuralını bir kez
    öğrenir, altı kez kullanır. Ama bir kalıp sayfaların çoğunu kaplarsa
    o artık bir kalıp değil bir ŞABLONDUR ve sayfalar birbirinden
    ayırt edilemez hâle gelir.
    """
    print("\n── ⑥ beyan edilmiş nakaratların payı ──")
    refrains = [norm_refrain(r) for r in cfg.get("allowedRefrains", [])]
    share_max = cfg.get("maxRefrainShare", 0.60)
    n = len(acts)
    rep.facts["refrainsDeclared"] = len(refrains)
    if not refrains:
        rep.warn("beyan edilmiş nakarat yok — kasıtlı kalıplar "
                 "project_config § echo.allowedRefrains içinde durmalı")
    over = []
    counts = {}
    for r in refrains:
        hit = 0
        for a in acts:
            blob = norm_refrain(" ".join([a.get("prompt", "")]
                                         + list(a.get("steps") or [])))
            if r and r in blob:
                hit += 1
        counts[r] = hit
        if n and hit / n > share_max:
            over.append("'%s' → %d/%d sayfa (%.0f%%)" % (r, hit, n, 100 * hit / n))
    rep.facts["refrainCounts"] = counts
    rep.check(not over,
              "hiçbir nakarat sayfaların %%%.0f'inden çoğunu kaplamıyor"
              % (100 * share_max)
              + ("" if not over else " — ŞABLON: %s" % over))

    # Beyan edilmemiş bir adım BİREBİR üç sayfada geçiyorsa, o bir
    # nakarattır ve beyan edilmemiştir. Sessiz nakarat, kararı olmayan
    # bir kalıptır.
    step_counts = collections.Counter()
    for a in acts:
        for s in set(a.get("steps") or []):
            step_counts[norm_refrain(s)] += 1
    undeclared = ["'%s' → %d sayfa" % (s, c)
                  for s, c in step_counts.most_common()
                  if c >= cfg.get("undeclaredStepMax", 3)
                  and not any(r and r in s for r in refrains)]
    rep.check(not undeclared,
              "birebir yinelenen her adım beyan edilmiş"
              + ("" if not undeclared else " — BEYANSIZ: %s" % undeclared[:5]))


def check_front_matter_echo(book, cfg, rep):
    """⑦ ÖN MADDE ↔ ARKA MADDE — İKİ OKUR, İKİ METİN (Faz 5 · bulgu E1).

    Faz 4 arka maddeye `how-to-use` ve `hint-rule` koymuştu ve ikisi de
    ÇOCUĞA sesleniyordu. Faz 5 çocuğa bakan işletim bilgisini ÖN MADDEYE
    taşıdı ve o üç sayfanın OKURUNU değiştirdi (`audience: adult`).

        Bir kullanım kılavuzu, kullanımdan SONRA gelirse
        bir kılavuz değil bir ÖZETTİR.

    Ama bir okur ayrımı beyan edilerek KURULMAZ, yazılarak kurulur. İki
    bölüm aynı cümleleri taşımaya devam ederse ayrım bir etiketten ibaret
    kalır ve kitap aynı şeyi iki kez basar.

    Bu denetim o ayrımın GERÇEKTEN yazıldığını ölçer — ve E1 kararını
    geri alınamaz kılar: biri ötekine yaklaşırsa kapı yanar.
    """
    print("\n── ⑦ ön madde ↔ arka madde ayrımı (E1) ──")
    fm = (book.get("frontMatter") or {}).get("sections") or []
    bm = (book.get("backMatter") or {}).get("sections") or []
    if not fm or not bm:
        print("  ⊘ ön veya arka madde yok — boş koştu")
        return

    thr = cfg.get("fieldNoteJaccardMax", 0.55)

    def bag(text):
        return {w for w in re.findall(r"[a-z']+", (text or "").lower())
                if len(w) > 3}

    front = {}
    for s in fm:
        if s.get("role", "teaching") != "teaching":
            continue
        front[s.get("id")] = bag(s.get("bodyText"))
    back = {}
    for s in bm:
        back[s.get("id")] = bag((s.get("purpose") or "") + " " +
                                " ".join(s.get("prints") or []))

    worst, pair = 0.0, None
    for fk, fv in front.items():
        for bk, bv in back.items():
            v = jaccard(fv, bv)
            if v > worst:
                worst, pair = v, (fk, bk)
    rep.facts["frontBackOverlapMax"] = round(worst, 3)
    rep.facts["frontBackOverlapPair"] = list(pair) if pair else None
    print("  en yüksek örtüşme %.3f  %s" % (worst, pair))
    rep.check(worst <= thr,
              "ön madde ile arka madde AYNI metni basmıyor (%.3f ≤ %.2f)"
              % (worst, thr)
              + ("" if worst <= thr else " — ÇAKIŞAN: %s" % (pair,)))

    # Ön maddenin kendi içinde de tekrar olamaz: sekiz sayfa aynı şeyi
    # dört kez anlatırsa çocuk hangisinin kural olduğunu bilemez.
    ks = list(front)
    worst_in, pair_in = 0.0, None
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            v = jaccard(front[ks[i]], front[ks[j]])
            if v > worst_in:
                worst_in, pair_in = v, (ks[i], ks[j])
    rep.facts["frontInternalOverlapMax"] = round(worst_in, 3)
    print("  ön madde iç örtüşmesi %.3f  %s" % (worst_in, pair_in))
    rep.check(worst_in <= thr,
              "ön madde bölümleri birbirini tekrar etmiyor (%.3f ≤ %.2f)"
              % (worst_in, thr)
              + ("" if worst_in <= thr else " — ÇAKIŞAN: %s" % (pair_in,)))

    # Ve okur ayrımı BEYAN edilmiş olmalı: beyansız bir ayrım, bir sonraki
    # yazarın farkında olmadan geri alabileceği bir ayrımdır.
    noaud = [s.get("id") for s in bm if not s.get("audience")]
    rep.check(not noaud, "her arka madde bölümü okurunu beyan ediyor"
              + ("" if not noaud else " — BEYANSIZ: %s" % noaud))
    adults = [s.get("id") for s in bm if s.get("audience") == "adult"]
    rep.check(len(adults) >= 1,
              "arka madde en az bir YETİŞKİN bölümü taşıyor (%d)" % len(adults))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    print("=" * 74)
    print("  TEKRAR VE KÜLTÜREL DÜZLEŞME")
    print("=" * 74)

    rep = Report(args.verbose)
    conf = load(CONFIG, rep)
    if conf is None:
        return 1
    cfg = conf.get("echo", {})
    index_doc = load(ACTIVITY_INDEX, rep, required=False)
    cul_doc = load(CULTURE_INDEX, rep, required=False)
    book_doc = load(BOOK, rep, required=False)

    if not book_doc:
        print("\n  ⊘ manuscript depoda yok — BOŞ KOŞTU")
        print("=" * 74)
        if args.json:
            os.makedirs(os.path.dirname(args.json), exist_ok=True)
            with open(args.json, "w", encoding="utf-8") as fh:
                json.dump({"status": "empty", "checks": 0, "errors": [],
                           "warnings": [], "facts": {}}, fh,
                          ensure_ascii=False, indent=2)
        return 0

    acts = merged(index_doc, book_doc)
    cultures = (cul_doc or {}).get("cultures", [])
    terms = build_culture_terms(cultures)
    rep.facts["activities"] = len(acts)
    rep.facts["maskedTerms"] = len(terms)
    print("\n  · %d sayfa ölçülüyor · %d kültürel terim maskelendi"
          % (len(acts), len(terms)))

    check_openers(acts, terms, cfg, rep)
    check_mission_shapes(acts, terms, cfg, rep)
    check_flattening(acts, rep)
    check_front_matter_echo(book_doc, cfg, rep)
    check_similarity(acts, terms, cfg, rep)
    check_single_source(acts, cultures, terms, cfg, rep)
    check_refrains(acts, cfg, rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · %d sayfa · en yüksek örtüşme %.2f"
              % (rep.checks, len(acts),
                 rep.facts.get("fieldNoteJaccardMax", 0.0)))
        status = "pass"
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": status, "checks": rep.checks,
                       "errors": rep.errors, "warnings": rep.warnings,
                       "facts": rep.facts}, fh, ensure_ascii=False, indent=2)
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
