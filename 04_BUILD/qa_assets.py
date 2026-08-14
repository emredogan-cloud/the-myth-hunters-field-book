#!/usr/bin/env python3
"""
GÖRSEL VARLIK KAPISI — The Myth Hunter's Field Book
================================================================================
Faz 4 **120 şartname ve 700 etiket** üretti ve **sıfır varlık**. Faz 5
varlıkları üretir — ve bu kapı ikisi arasındaki mesafeyi ölçer.

⭑ BU KAPININ ASIL İŞİ: BİR YOLU BİR VARLIK SANMAMAK ⭑

    Manifest'te `rawLocation` dolu olması, o dosyanın VAR OLDUĞU
    anlamına gelmez. Envanter bir NİYETTİR; disk bir OLGUDUR.

Bu ayrım Faz 3'ten beri `BOOK_STATS`'te iki ayrı satırda duruyor
(*görsel şartnamesi* · *görsel varlık*) ve bu kapı onu mekanikleştirir:
her sayı DİSKTEN okunur, manifestten değil.

Ne denetler:

  ① ENVANTER TAMLIĞI   — manifest güncel mi, her şartnamenin kaydı var mı
  ② KİMLİK             — assetId · activityId · region · culture · dosya adı
  ③ KATMAN HARİTASI    — raw / processed / final / rejected tutarlı mı
  ④ RAW DOKUNULMAZLIĞI — işlenmiş varlık RAW'ın sha256'sını taşıyor mu
  ⑤ ÖLÇÜ               — boyut · en-boy oranı · çözünürlük · biçim · mod
  ⑥ ZORUNLU ETİKET     — şartnamenin istediği etiket levhadan TÜRÜYOR mu
  ⑦ CEVAP GÖZLEMLENEBİLİRLİĞİ — ölçüm gerektiren sayfa kısıtını taşıyor mu
  ⑧ KÜLTÜREL GÜVENLİK  — her varlık kültürünün yasak biçimlerini taşıyor mu
  ⑨ MÜHÜR SESSİZLİĞİ   — hiçbir damga/rozet harf veya sözcük istemiyor mu
  ⑩ RET KAYDI          — reddedilen varlık gerekçesiyle duruyor mu

⚠ HAM VARLIK YOKKEN KAPI BOŞ KOŞMAZ, YARIM KOŞAR.

Bu önemli bir ayrım. Ham varlık kurucuya aittir ve henüz üretilmemiş
olabilir — ama ŞARTNAME katmanı bugün de denetlenebilir ve
denetlenmelidir. Kapı bu yüzden ikiye bölünmüştür:

    ŞARTNAME denetimleri  → HER ZAMAN koşar (①②③⑥⑦⑧⑨)
    DOSYA denetimleri     → varlık VARSA koşar (④⑤⑩)

Böylece kusurlu bir şartname, görsel üretilmeden ÖNCE yakalanır. Faz 5'in
en pahalı hatası, kusurlu bir şartnameye göre üretilmiş kusursuz bir
görseldir: görsel doğrudur, sayfa çözülemez.

TASARIM: şartname katmanı yalnızca standart kütüphane (karar K7).
Dosya katmanı Pillow ister ve yoksa o denetimleri ATLAR — ama bunu
SÖYLER; sessizce yeşil yanmaz.

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

MANIFEST = os.path.join(ROOT, "07_ASSETS", "ASSET_MANIFEST.json")
MANIFEST_LOCAL = os.path.join(ROOT, "07_ASSETS", "ASSET_MANIFEST.local.json")

# ⭑ TAM KAYIT YEREL DOSYADADIR ⭑
# Takip edilen envanter içerik taşımaz (K10): requiredLabels ve
# restrictions cevabın kendisini taşıyabilir. Hat ve kapı tam kaydı
# yerelden okur; yerel kayıt yoksa takip edilenle YARIM koşar ve bunu
# SÖYLER — sessizce eksik denetim yapmaz.
def manifest_path():
    return MANIFEST_LOCAL if os.path.isfile(MANIFEST_LOCAL) else MANIFEST
BOOK = os.path.join(ROOT, "02_MANUSCRIPT", "book.json")
ACTS = os.path.join(ROOT, "01_SOURCE", "activity_index.json")
CULTURES = os.path.join(ROOT, "01_SOURCE", "culture_index.json")
REGIONS = os.path.join(ROOT, "01_SOURCE", "region_index.json")
SEAL_KEY = os.path.join(ROOT, "01_SOURCE", "answers", "seal_key.json")
CONFIG = os.path.join(ROOT, "project_config.json")

PROC_DIR = os.path.join(ROOT, "07_ASSETS", "processed", "interior")
FINAL_DIR = os.path.join(ROOT, "07_ASSETS", "final", "interior")
REJECT_DIR = os.path.join(ROOT, "07_ASSETS", "rejected")

ASPECT_TOL = 0.02

# ⭑ DOLULUK EŞİĞİ — YANLIŞ ŞABLONU YAKALAR, KIRPMA GÜRÜLTÜSÜNÜ YAKALAMAZ ⭑
#
# Hat kırpar, sığdırır ve hedef kutuya beyazla doldurur. Doldurma oranı
# GİZLEMEZ, ÖLÇER: sanat kutunun ne kadarını dolduruyor.
#
#   %100–95  kırpma kaynaklı normal sapma
#   %95–85   dikkat çeker ama üretimi durdurmaz          → UYARI
#   %85 altı YANLIŞ ŞABLON: dikey sanat yatay kutuda      → KIRMIZI
#
# Eşik ilk hâlde %92'ydi ve kırpma kaynaklı %91'lik meşru bir çıktıyı
# kırmızı yakıyordu. Bir eşik meşru işi durduruyorsa ölçtüğü şey yanlış
# değil, SINIRI yanlıştır.
FILL_FAIL = 0.85
FILL_WARN = 0.95

# ⑦ Ölçüm gerektiren aktivite tipleri. Bir cevap SAYIYA, SIRAYA veya
# KONUMA dayanıyorsa, görsel o ölçümü MÜMKÜN KILMAK ZORUNDADIR.
MEASURE_WORDS = re.compile(
    r"\b(count|counted|countable|exactly|order|ordered|number(?:ed)?|"
    r"nearest|closest|furthest|farthest|adjacent|distant|mirror|mirrored|"
    r"identical|same scale|taller|shorter|larger|smaller|between)\b", re.I)

# ⭑ BU İKİ ÖRÜNTÜ BU KAPININ İLK KOŞUSUNDA DOĞDU ⭑
#
# Kapının ilk hâli SABİT bir cümle arıyordu ("No answer may be visible")
# ve 57 sayfayı kırmızı yaktı. Elli yedisi de DOĞRUYDU: Faz 4 aynı kuralı
# sayfaya ÖZGÜ biçimde yazmıştı ve o hâli daha güçlüdür —
#
#     "No tick may appear in any tick box and no name may be
#      written on any writing line."
#
# genel bir yasaktan daha denetlenebilirdir, çünkü NEYİN boş kalacağını
# söyler. Kapıyı yeşile çevirmenin en ucuz yolu bu cümleleri silip yerine
# kalıp yapıştırmaktı — yani KESİN bir kısıtı GENEL bir kısıtla
# değiştirmek.
#
#     Bir kapı doğru olanı pahalı hâle getiriyorsa,
#     düzeltilmesi gereken KAPIDIR.  (Faz 3 § 21.1 · Faz 4 § 24.1)
#
# Bu yüzden kapı artık CÜMLEYİ değil SINIFI arıyor: cevabın görünmesini
# engelleyen HERHANGİ bir kısıt sayılır.
ANSWER_HIDDEN = re.compile(
    # açık beyan
    r"no answer may be visible"
    r"|no part of the answer"
    # "no X may be <fiil>" — bütün aile; fiil listesi kovalanmaz
    r"|\bno\b[\w\s,'-]{0,40}\bmay\s+(?:be|appear)\b"
    # "must (all) be/stay/remain (printed/drawn/left) empty|blank|unmarked"
    r"|\bmust\s+(?:all\s+)?(?:be|stay|remain)\s+"
    r"(?:printed\s+|drawn\s+|left\s+)?(?:empty|blank|unmarked)\b"
    r"|(?:stay|stays|stayed|remain|remains|left|drawn|printed)\s+"
    r"(?:empty|blank|unmarked)\b"
    r"|\bempty\s+(?:writing\s+)?lines?\b"
    # "print no X" / "do not print X" / "draw no X"
    r"|\bprint\s+no\b|\bdraw\s+no\b|\bdo\s+not\s+(?:print|label|mark|draw|trace|ring)\b",
    re.I)


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
        return bool(cond)

    def warn(self, label: str) -> None:
        self.warnings.append(label)
        print("  ! %s" % label)


def load(path, rep, required=True):
    if not os.path.isfile(path):
        if required:
            rep.check(False, "dosya yok: %s" % os.path.relpath(path, ROOT))
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        rep.check(False, "JSON bozuk: %s — %s" % (os.path.relpath(path, ROOT), exc))
        return None


# ── ① ENVANTER TAMLIĞI ─────────────────────────────────────────────────────
def check_inventory(man, book, rep):
    print("\n── ① envanter tamlığı ──")
    assets = man.get("assets") or []
    rep.facts["manifestAssets"] = len(assets)
    rep.facts["counts"] = man.get("counts")

    rep.check(bool(assets), "envanter boş değil (%d)" % len(assets))

    ids = [a.get("assetId") for a in assets]
    dupes = [k for k, v in collections.Counter(ids).items() if v > 1]
    rep.check(not dupes, "her varlık kimliği tekil"
              + ("" if not dupes else " — YİNELENEN: %s" % dupes))

    files = [a.get("filename") for a in assets]
    fdupes = [k for k, v in collections.Counter(files).items() if v > 1]
    rep.check(not fdupes, "her dosya adı tekil"
              + ("" if not fdupes else " — YİNELENEN: %s" % fdupes))

    # ⭑ HİÇBİR ŞARTNAME ENVANTERİN DIŞINDA KALAMAZ ⭑
    # Envanterden düşen bir şartname, üretilmeyen bir görseldir — ve
    # eksikliği ancak dizgi sırasında, en pahalı anda fark edilir.
    spec_ids = {a["visualSpec"]["assetId"] for a in (book or {}).get("activities", [])
                if a.get("visualSpec")}
    orphan = sorted(spec_ids - set(ids))
    rep.check(not orphan, "her aktivite şartnamesinin envanterde bir kaydı var"
              + ("" if not orphan else " — ENVANTER DIŞI: %s" % orphan[:5]))

    # Ve tersi: envanterde kaynağı olmayan bir varlık ne için üretilecek?
    ghost = [a["assetId"] for a in assets if not a.get("sourceSpec")]
    rep.check(not ghost, "her varlık bir kaynak şartnameye işaret ediyor"
              + ("" if not ghost else " — KAYNAKSIZ: %s" % ghost[:5]))

    # Yol haritası tahmini bir HEDEF değildir; sapma bilgi amaçlıdır.
    est = man.get("roadmapEstimate")
    if est:
        delta = len(assets) - est
        rep.facts["roadmapDelta"] = delta
        print("  envanter %d · yol haritası tahmini %d · fark %+d"
              % (len(assets), est, delta))


# ── ② KİMLİK ───────────────────────────────────────────────────────────────
def check_identity(man, book, index, regions, cultures, rep):
    print("\n── ② kimlik ──")
    assets = man.get("assets") or []
    design = {a["activityId"]: a for a in (index or {}).get("activities", [])}
    region_ids = {r["id"] for r in (regions or {}).get("regions", [])}
    culture_ids = {c["id"] for c in (cultures or {}).get("cultures", [])}
    acts = {a["activityId"]: a for a in (book or {}).get("activities", [])}

    bad_act, bad_reg, bad_cul, bad_fn = [], [], [], []
    for a in assets:
        aid = a.get("assetId") or ""
        # dosya adı kimlikten türer — ikisi ayrılırsa hat yanlış dosyayı yazar
        if a.get("filename") != aid + ".png":
            bad_fn.append(aid)
        if a.get("assetClass") == "activity":
            act = a.get("activityId")
            if act not in acts:
                bad_act.append(aid)
            else:
                d = design.get(act, {})
                if a.get("region") != d.get("region"):
                    bad_reg.append(aid)
                if a.get("culture") != d.get("culture"):
                    bad_cul.append(aid)
        if a.get("region") and a["region"] not in region_ids:
            bad_reg.append(aid)
        if a.get("culture") and a["culture"] not in culture_ids:
            bad_cul.append(aid)

    rep.check(not bad_fn, "dosya adı varlık kimliğinden türüyor"
              + ("" if not bad_fn else " — AYRIK: %s" % bad_fn[:5]))
    rep.check(not bad_act, "her aktivite varlığı var olan bir sayfaya bağlı"
              + ("" if not bad_act else " — BAĞSIZ: %s" % bad_act[:5]))
    rep.check(not bad_reg, "bölge kimlikleri tutarlı"
              + ("" if not bad_reg else " — TUTARSIZ: %s" % sorted(set(bad_reg))[:5]))
    rep.check(not bad_cul, "kültür kimlikleri tutarlı"
              + ("" if not bad_cul else " — TUTARSIZ: %s" % sorted(set(bad_cul))[:5]))

    # Her kültürün bir vinyeti var mı — alt başlıktaki 22 vaadi görselde de
    # tutulur; bir kültürün yalnızca bulmacada görünmesi K13'e aykırıdır.
    vig = {a.get("culture") for a in assets
           if a.get("assetClass") == "culture-vignette"}
    missing = sorted(culture_ids - vig)
    rep.check(not missing, "yirmi iki kültürün yirmi ikisinin de vinyeti var"
              + ("" if not missing else " — VİNYETSİZ: %s" % missing))

    # Her bölgenin bir mühür damgası var mı
    stamps = {a.get("region") for a in assets
              if a.get("assetClass") == "seal-stamp"}
    ms = sorted(region_ids - stamps)
    rep.check(not ms, "altı bölgenin altısının da mühür damgası var"
              + ("" if not ms else " — DAMGASIZ: %s" % ms))


# ── ③ KATMAN HARİTASI ──────────────────────────────────────────────────────
def check_layers(man, rep):
    print("\n── ③ katman haritası ──")
    assets = man.get("assets") or []
    layers = man.get("layers") or {}
    rep.check(set(layers) >= {"raw", "processed", "final", "rejected"},
              "dört katmanın dördü de tanımlı (%s)" % sorted(layers))

    bad = []
    for a in assets:
        fn = a.get("filename") or ""
        for key, base in (("rawLocation", layers.get("raw")),
                          ("processedLocation", layers.get("processed")),
                          ("finalLocation", layers.get("final")),
                          ("rejectedLocation", layers.get("rejected"))):
            v = a.get(key) or ""
            if not base or not v.startswith(base) or not v.endswith(fn):
                bad.append("%s.%s" % (a.get("assetId"), key))
    rep.check(not bad, "her varlık dört katmanın dördünde de doğru yolu taşıyor"
              + ("" if not bad else " — YANLIŞ YOL: %s" % bad[:5]))

    # ⭑ RAW İLE PROCESSED AYNI YERE YAZAMAZ ⭑
    # Aynı yolu paylaşan iki katman, işlemenin RAW'ın üstüne yazması
    # demektir ve RAW geri getirilemez (K35).
    same = [a["assetId"] for a in assets
            if a.get("rawLocation") == a.get("processedLocation")]
    rep.check(not same, "⭑ hiçbir varlıkta RAW ile PROCESSED aynı yol değil"
              + ("" if not same else " — ÜZERİNE YAZMA RİSKİ: %s" % same[:5]))


# ── ④ RAW DOKUNULMAZLIĞI ───────────────────────────────────────────────────
def check_raw_integrity(man, rep):
    print("\n── ④ RAW dokunulmazlığı ──")
    assets = man.get("assets") or []
    proc = [a for a in assets
            if os.path.isfile(os.path.join(PROC_DIR, a["filename"]))]
    rep.facts["processedOnDisk"] = len(proc)
    if not proc:
        print("  ⊘ işlenmiş varlık yok — denetlenecek köken kaydı yok")
        return

    noprov, drift = [], []
    for a in proc:
        meta = os.path.join(PROC_DIR, a["filename"] + ".source.json")
        if not os.path.isfile(meta):
            noprov.append(a["assetId"])
            continue
        try:
            with open(meta, encoding="utf-8") as fh:
                m = json.load(fh)
        except (json.JSONDecodeError, OSError):
            noprov.append(a["assetId"])
            continue
        if not m.get("sourceSha256"):
            noprov.append(a["assetId"])
            continue
        raw = os.path.join(ROOT, a["rawLocation"])
        if os.path.isfile(raw):
            import hashlib
            h = hashlib.sha256()
            with open(raw, "rb") as fh:
                for chunk in iter(lambda: fh.read(65536), b""):
                    h.update(chunk)
            if h.hexdigest() != m["sourceSha256"]:
                drift.append(a["assetId"])

    rep.check(not noprov,
              "⭑ her işlenmiş varlık kaynağının sha256'sını taşıyor"
              + ("" if not noprov else " — KÖKENSİZ: %s" % noprov[:5]))
    rep.check(not drift,
              "⭑ hiçbir işlenmiş varlık kaynağından SÜRÜKLENMEMİŞ"
              + ("" if not drift else " — RAW DEĞİŞTİ: %s" % drift[:5]))


# ── ⑤ ÖLÇÜ ─────────────────────────────────────────────────────────────────
def check_dimensions(man, rep):
    print("\n── ⑤ ölçü · oran · çözünürlük ──")
    assets = man.get("assets") or []
    on_disk = [(a, os.path.join(PROC_DIR, a["filename"])) for a in assets
               if os.path.isfile(os.path.join(PROC_DIR, a["filename"]))]
    if not on_disk:
        print("  ⊘ işlenmiş varlık yok — ölçü denetlenemedi")
        rep.facts["dimensionChecked"] = 0
        return

    try:
        from PIL import Image
    except ImportError:
        # ⚠ SESSİZ YEŞİL YOK. Bağımlılık yoksa kapı bunu SÖYLER.
        rep.warn("Pillow yok — %d varlığın ÖLÇÜSÜ DENETLENEMEDİ "
                 "(pip install -r 04_BUILD/requirements.txt)" % len(on_disk))
        rep.facts["dimensionChecked"] = 0
        return

    small, box, fmt, mode, thin, loose = [], [], [], [], [], []
    for a, path in on_disk:
        try:
            im = Image.open(path)
        except OSError:
            fmt.append(a["assetId"])
            continue
        w, h = im.size
        tw, th = a["targetDimensions"]

        # ⭑ İŞLENMİŞ VARLIK HEDEF KUTUYU TAM DOLDURUR ⭑
        # Hat kırpar, sığdırır ve beyazla DOLDURUR; çıktı bu yüzden her
        # zaman hedefin BİREBİR aynısı olmalıdır. Değilse hat o varlığı
        # işlememiş ya da yarıda bırakmış demektir.
        if (w, h) != (tw, th):
            box.append("%s (%dx%d ≠ %dx%d)" % (a["assetId"], w, h, tw, th))

        if (im.format or "").upper() != (a.get("format") or "png").upper():
            fmt.append(a["assetId"])
        if a.get("colour") == "grayscale" and im.mode not in ("L", "1"):
            mode.append(a["assetId"])

        # Köken kaydından ölçülen gerçekler: doldurma ORANI GİZLEMEZ, ÖLÇER.
        meta_p = path + ".source.json"
        if os.path.isfile(meta_p):
            try:
                with open(meta_p, encoding="utf-8") as fh:
                    m = json.load(fh)
            except (json.JSONDecodeError, OSError):
                m = {}
            # ⭑ HEDEFTEN KÜÇÜK BİR GÖRSEL BÜYÜTÜLMEZ, REDDEDİLİR ⭑
            # Yukarı örnekleme çözünürlük kazandırmaz; yalnızca 300 dpi
            # iddiasını YALAN hâline getirir.
            if m.get("underTarget"):
                aw, ah = m.get("artSize") or [0, 0]
                small.append("%s (%dx%d < %dx%d)" % (a["assetId"], aw, ah, tw, th))
            # Düşük doluluk = YANLIŞ ŞABLON. Doldurma onu görünmez yapmaz;
            # bu satır tam olarak onu görünür kılmak için var.
            fr = m.get("fillRatio")
            if fr is not None:
                if fr < FILL_FAIL:
                    thin.append("%s (kutunun %%%.0f'i)" % (a["assetId"], fr * 100))
                elif fr < FILL_WARN:
                    loose.append("%s (%%%.0f)" % (a["assetId"], fr * 100))

    rep.facts["dimensionChecked"] = len(on_disk)
    rep.check(not small, "⭑ hiçbir varlık hedef çözünürlüğün ALTINDA değil"
              + ("" if not small else " — DÜŞÜK: %s" % small[:5]))
    rep.check(not box, "her işlenmiş varlık hedef kutuyu BİREBİR dolduruyor"
              + ("" if not box else " — KUTU: %s" % box[:5]))
    rep.check(not thin, "sanat hedef kutunun oranına oturuyor (doluluk ≥ %%%.0f)"
              % (FILL_FAIL * 100)
              + ("" if not thin else " — YANLIŞ ŞABLON: %s" % thin[:5]))
    if loose:
        rep.warn("doluluk %%%.0f–%%%.0f arasında olan %d varlık — kırpma "
                 "kaynaklı olabilir, bir insan bakmalı: %s"
                 % (FILL_FAIL * 100, FILL_WARN * 100, len(loose), loose[:5]))
    rep.check(not fmt, "dosya biçimi şartnameyle aynı"
              + ("" if not fmt else " — BİÇİM: %s" % fmt[:5]))
    rep.check(not mode, "gri tonlama isteyen varlık gri tonlamada"
              + ("" if not mode else " — MOD: %s" % mode[:5]))


# ── ⑥ ZORUNLU ETİKET ───────────────────────────────────────────────────────
def check_labels(man, book, rep):
    print("\n── ⑥ zorunlu etiket ──")
    assets = man.get("assets") or []
    acts = {a["activityId"]: a for a in (book or {}).get("activities", [])}

    total = sum(len(a.get("requiredLabels") or []) for a in assets)
    rep.facts["requiredLabels"] = total
    print("  zorunlu etiket toplamı: %d" % total)

    # ⭑ ETİKET LEVHADAN TÜRER, İCAT EDİLMEZ (karar K25) ⭑
    #
    # Bir etiket `pagePrints`te karşılığı yoksa, illüstratör onu basacak
    # ama sayfa onu istemeyecektir — ya da tersi, ki daha kötüsüdür:
    # sayfa bir şeyi "the X" diye anar ve levhada X yoktur.
    #
    # ⚠ İKİ MEŞRU SAPMA VAR ve ikisi de burada tanınır:
    #   · SAYI GENİŞLETMESİ — "numbered 1 to 4" → '1','2','3','4'
    #   · NORMALLEŞTİRME    — "人 or 亻 person" → '人 person'
    # Bunları kusur saymak, doğru yazılmış bir şartnameyi bozmaya iter.
    orphan = []
    for a in assets:
        if a.get("assetClass") != "activity":
            continue
        act = acts.get(a.get("activityId"))
        if not act:
            continue
        blob = " ".join(act.get("pagePrints") or []).lower()
        for lab in a.get("requiredLabels") or []:
            low = lab.lower()
            if low in blob:
                continue
            # sayı genişletmesi: levha "numbered X to Y" diyorsa aradaki
            # her sayı meşrudur
            if low.isdigit():
                ok = False
                for m in re.finditer(r"numbered\s+(\d+)\s+to\s+(\d+)", blob):
                    if int(m.group(1)) <= int(low) <= int(m.group(2)):
                        ok = True
                        break
                if ok:
                    continue
            # normalleştirme: etiketin bütün sözcükleri levhada geçiyorsa
            toks = [t for t in re.split(r"\s+", low) if t]
            if toks and all(t in blob for t in toks):
                continue
            orphan.append("%s → %r" % (a["assetId"], lab))

    rep.check(not orphan,
              "⭑ her zorunlu etiket levhadan (pagePrints) TÜRÜYOR"
              + ("" if not orphan else " — TÜREMEYEN %d: %s"
                 % (len(orphan), orphan[:5])))

    # Vinyet bir levha değildir: TEK bir etiket taşır, kültürün adı.
    fat = [a["assetId"] for a in assets
           if a.get("assetClass") == "culture-vignette"
           and len(a.get("requiredLabels") or []) != 1]
    rep.check(not fat,
              "her kültür vinyeti YALNIZCA kültürün adını taşıyor"
              + ("" if not fat else " — FAZLA ETİKET: %s" % fat[:5]))


# ── ⑦ CEVAP GÖZLEMLENEBİLİRLİĞİ ────────────────────────────────────────────
def check_observability(man, book, rep):
    print("\n── ⑦ cevap gözlemlenebilirliği ──")
    assets = {a.get("activityId"): a for a in (man.get("assets") or [])
              if a.get("assetClass") == "activity"}
    STD = ("No answer may be visible", "No decorative text", "No photographic",
           "culture_index", "KAPALI KATMAN")

    need, have = [], 0
    for act in (book or {}).get("activities", []):
        ans = act.get("answer") or ""
        steps = " ".join(act.get("steps") or [])
        # Cevap bir ÖLÇÜME dayanıyor mu: sayı, sıra, konum, eşleşme
        if not MEASURE_WORDS.search(ans + " " + steps):
            continue
        a = assets.get(act["activityId"])
        if not a:
            continue
        extra = [r for r in (a.get("restrictions") or [])
                 if not r.startswith(STD)]
        if extra:
            have += 1
        else:
            need.append(act["activityId"])

    rep.facts["measurementPages"] = have + len(need)
    rep.facts["measurementConstrained"] = have
    print("  ölçüme dayanan sayfa: %d · kısıt taşıyan: %d" % (have + len(need), have))

    # ⭑ FAZ 4'ÜN KURALI, MEKANİKLEŞMİŞ HÂLİ ⭑
    #
    #     Bir cevap ölçülebilir diye yazıldıysa, görsel şartnamesi
    #     o ölçümü MÜMKÜN KILMAK ZORUNDADIR.
    #
    # Kısıtsız bir ölçüm sayfası, üreteç eline bırakılmış bir cevaptır:
    # "on iki kalas" isteyen bir sayfa on üç kalasla gelirse cevap
    # değişir ve kimse fark etmez.
    # ⭑ BU BİR UYARI DEĞİL BİR KAPIDIR — VE BİLİNÇLİ OLARAK ÖYLE ⭑
    #
    # İlk hâli bir uyarıydı ve 23 sayfayı işaret etti. Yirmi üçü de gerçek
    # kusurdu: cevabı bir sayıya, bir sıraya ya da bir glife dayanan
    # sayfalar, o ölçümü hiçbir yerde ŞART KOŞMUYORDU.
    #
    #     Yalnızca uyaran bir kural, uyulmayan bir kuraldır.
    #
    # Yirmi üçü de kapatıldıktan sonra denetim SERTLEŞTİRİLDİ: bundan sonra
    # kısıtsız bir ölçüm sayfası eklemek kapıyı kırmızı yakar.
    rep.check(not need,
              "⭑ ölçüme dayanan her sayfa o ölçümü ŞART KOŞAN bir kısıt taşıyor "
              "(%d/%d)" % (have, have + len(need))
              + ("" if not need else " — KISITSIZ: %s" % need[:8]))

    # Cevap görselde GÖRÜNEMEZ. Kalıp değil SINIF aranır (bkz. ANSWER_HIDDEN).
    missing = [a["assetId"] for a in (man.get("assets") or [])
               if not any(ANSWER_HIDDEN.search(r)
                          for r in (a.get("restrictions") or []))]
    rep.check(not missing,
              "⭑ her varlık cevabın GÖRÜNMESİNİ engelleyen bir kısıt taşıyor"
              + ("" if not missing else " — KISITSIZ: %s" % missing[:5]))


# ── ⑧ KÜLTÜREL GÜVENLİK ────────────────────────────────────────────────────
def check_cultural_safety(man, cultures, rep):
    print("\n── ⑧ kültürel görsel güvenliği ──")
    assets = man.get("assets") or []
    cmap = {c["id"]: c for c in (cultures or {}).get("cultures", [])}

    # ⭑ ZORUNLULUK RİSKE GÖRE ÖLÇEKLENİR — VE BU BİLİNÇLİDİR ⭑
    #
    # Kapının ilk hâli HER kültür varlığından o kültürün BÜTÜN yasak
    # biçimlerini istiyordu. Bu yanlıştı ve yanlışlığı ince: bir sayfa
    # rün taşları hakkındaysa, prompta "Loki'nin bahis bedeli" uyarısı
    # koymak o sayfayı korumaz — yalnızca promptu uzatır.
    #
    #     Okunmayan bir uyarı, olmayan bir uyarıdır.
    #     İlgisiz uyarı yığmak, ilgili olanı gizlemenin en kolay yoludur.
    #
    # Bu yüzden zorunluluk riske göre ölçeklenir:
    #   · Kademe C veya `restricted` kültür  → kısıt ZORUNLU
    #   · kültür vinyeti (saf kültürel tasvir) → kısıt ZORUNLU
    #   · diğer aktivite sayfaları            → sayfaya özgü kısıt yeter
    #
    # CULTURE_POLICY'nin daralma sırasıyla aynı mantık: sertlik kültürün
    # kademesinden gelir, hepsine aynı muamele yapılmaz.
    naked = []
    for a in assets:
        cid = a.get("culture")
        if not cid or cid not in cmap:
            continue
        c = cmap[cid]
        forbidden = c.get("forbiddenForms") or []
        if not forbidden:
            continue
        high_risk = (c.get("eligibilityTier") == "C"
                     or c.get("restrictionStatus") == "restricted"
                     or a.get("assetClass") == "culture-vignette")
        if not high_risk:
            continue
        blob = " ".join(a.get("restrictions") or [])
        # İllüstratör `culture_index`i okumaz; prompta ne yazdıysa onu çizer.
        if ("culture_index § %s" % cid) not in blob:
            naked.append(a["assetId"])
    rep.check(not naked,
              "⭑ Kademe C / kısıtlı kültürün ve her vinyetin varlığı o "
              "kültürün YASAK BİÇİMLERİNİ taşıyor"
              + ("" if not naked else " — KISITSIZ: %s" % naked[:5]))

    # Ve düşük riskli sayfalar da kültürel olarak başıboş değildir:
    # her aktivite varlığı EN AZ bir sayfaya özgü kısıt taşımalıdır.
    STD3 = ("No answer may be visible", "No decorative text", "No photographic")
    bland = [a["assetId"] for a in assets
             if a.get("assetClass") == "activity"
             and not [r for r in (a.get("restrictions") or [])
                      if not r.startswith(STD3)]]
    rep.check(not bland,
              "her aktivite varlığı sayfaya ÖZGÜ en az bir kısıt taşıyor"
              + ("" if not bland else " — YALNIZCA KALIP: %s" % bland[:5]))

    # Yaşayan gelenek: vinyet onu bir kalıntı gibi göstermemeli.
    living = []
    for a in assets:
        if a.get("assetClass") != "culture-vignette":
            continue
        c = cmap.get(a.get("culture") or "")
        if c and c.get("livingTradition"):
            if not any("living tradition" in r for r in (a.get("restrictions") or [])):
                living.append(a["assetId"])
    rep.check(not living,
              "yaşayan geleneğin vinyeti onu YAŞAYAN olarak istiyor"
              + ("" if not living else " — EKSİK: %s" % living[:5]))

    # ⭑ EVRENSEL YASAKLAR TEK YERDE DURUR — VE ORASI ŞARTNAME DEĞİLDİR ⭑
    #
    # Kapının ilk hâli HER şartnameden "gerçekçi insan yüzü yok" kısıtını
    # istiyordu ve 55 sayfayı kırmızı yaktı. Yanlıştı: bu kısıt evrenseldir
    # ve zaten TEK bir yerde duruyor — `image_prompts.py § NEGATIVE` her
    # prompta on evrensel yasağı ekliyor.
    #
    #     Evrensel bir kuralı 158 şartnameye kopyalamak, onu 158 kez
    #     sürüklenebilir hâle getirmektir.
    #
    # Doğru denetim şu: evrensel katman VAR MI ve o yasakları TAŞIYOR MU.
    # Tek kaynak denetlenir, kopya aranmaz (D17).
    prompt_gen = os.path.join(ROOT, "04_BUILD", "image_prompts.py")
    if os.path.isfile(prompt_gen):
        with open(prompt_gen, encoding="utf-8") as fh:
            gen = fh.read()
        for rule, label in (
                ("realistic human faces", "gerçekçi insan yüzü"),
                ("no answer visible", "cevap görünürlüğü"),
                ("no colour", "renk"),
                ("religious ritual", "dinî ritüel"),
                ("no weapon in use", "silah")):
            rep.check(rule in gen,
                      "evrensel yasak listesi '%s' kuralını taşıyor" % label)
    else:
        rep.check(False, "evrensel yasak listesi yok (image_prompts.py)")


# ── ⑨ MÜHÜR SESSİZLİĞİ ─────────────────────────────────────────────────────
def check_seal_silence(man, seal, rep):
    """⚠ Bu fonksiyon hiçbir mühür sözcüğünü ekrana BASMAZ."""
    print("\n── ⑨ mühür sessizliği ──")
    assets = man.get("assets") or []

    # Damga ve rozetler HİÇBİR etiket taşımaz: harf çocuğun yazdığı şeydir.
    lettered = [a["assetId"] for a in assets
                if a.get("assetClass") in ("seal-stamp", "badge")
                and (a.get("requiredLabels") or [])]
    rep.check(not lettered,
              "⭑ hiçbir mühür damgası veya rozet BİR ETİKET İSTEMİYOR"
              + ("" if not lettered else " — HARFLİ: %s" % lettered[:5]))

    # Ve şartname bunu AÇIKÇA söylemeli: sessizlik bir varsayım değil,
    # prompta yazılmış bir kısıt olmalıdır.
    silent = [a["assetId"] for a in assets
              if a.get("assetClass") == "seal-stamp"
              and not any("NO letters" in r for r in (a.get("restrictions") or []))]
    rep.check(not silent,
              "her mühür damgası 'harf yok' kısıtını AÇIKÇA taşıyor"
              + ("" if not silent else " — SESSİZ DEĞİL: %s" % silent[:5]))

    if not seal:
        print("  ⊘ mühür anahtarı depoda yok — sözcük taraması atlandı")
        return

    words = {(s.get("word") or "").strip().lower()
             for s in (seal.get("seals") or [])}
    words = {w for w in words if w}
    fin = ((seal.get("finalQuest") or {}).get("word") or "").strip().lower()
    if fin:
        words.add(fin)

    # ⭑ SORULACAK DOĞRU SORU ⭑
    #
    # Kapının ilk hâli bütün şartname metninde mühür sözcüğü aradı ve üç
    # varlık buldu. Üçü de YANLIŞ POZİTİFTİ ve Faz 4 § 24.1 bu tuzağı
    # tam olarak adıyla anmıştı:
    #
    #     Mühür sözcükleri sıradan İngilizce sözcüklerdir ve bir levha
    #     metninde meşru olarak geçerler — bir vazo panelinin sözcük
    #     bankasında ya da bir davul altyazısında.
    #
    #     Kapı "bu sözcük geçiyor" diyordu.
    #     Sorulması gereken şey "bu sözcük MÜHÜR OLARAK OKUNABİLİYOR mu" idi.
    #
    # Ve kapıyı yeşile çevirmenin en ucuz yolu o sözcük bankasından
    # doğru bir girdiyi SİLMEK olurdu — yani doğru yazılmış bir sayfayı
    # bozmak.
    #
    # Denetim bu yüzden GÖRSELDE AYRI BİR ETİKET OLARAK BASILACAK şeye
    # daraltıldı: `requiredLabels`. Bir levhada tek başına duran ve yıldız
    # kutusunun yanında okunan bir etiket, mühür olarak okunabilir.
    # Akıcı bir altyazının içindeki aynı sözcük okunamaz.
    #
    # Daraltma bir gevşetme DEĞİLDİR: yerine ⑨b geldi ve o gerçek bir
    # tasarım riskidir.
    leak = []
    for a in assets:
        for lab in (a.get("requiredLabels") or []):
            if lab.strip().lower() in words:
                leak.append(a["assetId"])
                break
    rep.check(not leak,
              "⭑ hiçbir ZORUNLU ETİKET bir mühür sözcüğü değil"
              + ("" if not leak else " — SIZINTI: %s" % sorted(set(leak))[:5]))

    # ⑨b ⭑ VE BİR MÜHÜR SAYFASININ ETİKETİ, O BÖLGENİN SÖZCÜĞÜNÜ
    #      HARFLERİYLE KURAMAZ ⭑
    #
    # Yıldız kutusu taşıyan bir sayfada, o bölgenin mühür sözcüğüyle aynı
    # HARF DİZİSİNİ taşıyan bir etiket basılırsa çocuk sözcüğü kazara
    # okur ve altı sayfalık toplama işi anlamsızlaşır. Bu bir sızıntı
    # değil bir MEKANİK ÇÖKÜŞTÜR — qa_answerkey § ⑤c'nin görsel katmandaki
    # karşılığı.
    seals_by_region = {}
    for s in (seal.get("seals") or []):
        rid = s.get("regionId") or s.get("region")
        w = (s.get("word") or "").strip().lower()
        if rid and w:
            seals_by_region[rid] = w
    collapse = []
    for a in assets:
        w = seals_by_region.get(a.get("region") or "")
        if not w:
            continue
        for lab in (a.get("requiredLabels") or []):
            if lab.strip().lower().replace(" ", "") == w.replace(" ", ""):
                collapse.append(a["assetId"])
                break
    rep.check(not collapse,
              "⭑ hiçbir etiket kendi bölgesinin mühür sözcüğüne ÇÖKMÜYOR"
              + ("" if not collapse else " — ÇÖKME: %s" % collapse[:5]))


# ── ⑩ RET KAYDI ────────────────────────────────────────────────────────────
def check_rejections(man, rep):
    print("\n── ⑩ ret kaydı ──")
    if not os.path.isdir(REJECT_DIR):
        print("  ⊘ reddedilen varlık yok")
        rep.facts["rejected"] = 0
        return
    pngs = [f for f in os.listdir(REJECT_DIR) if f.lower().endswith(".png")]
    rep.facts["rejected"] = len(pngs)
    if not pngs:
        print("  ⊘ reddedilen varlık yok")
        return
    print("  reddedilen: %d" % len(pngs))
    # ⭑ SİLİNEN BİR RET, AYNI HATANIN İKİNCİ KEZ YAPILMASINI SERBEST BIRAKIR
    noreason = [f for f in pngs
                if not os.path.isfile(os.path.join(REJECT_DIR, f + ".reason.json"))]
    rep.check(not noreason,
              "⭑ reddedilen her varlık GEREKÇESİYLE duruyor"
              + ("" if not noreason else " — GEREKÇESİZ: %s" % noreason[:5]))


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    print("=" * 74)
    print("  GÖRSEL VARLIK KAPISI")
    print("=" * 74)

    rep = Report(args.verbose)

    book = load(BOOK, rep, required=False)
    if book is None:
        # Manuscript depoda durmaz (K10). Envanter ondan türer, dolayısıyla
        # denetlenecek bir şey de yoktur. Körlüğü selftest kapatır.
        print("\n  ⊘ manuscript depoda yok (K10) — BOŞ KOŞTU")
        print("=" * 74)
        if args.json:
            os.makedirs(os.path.dirname(args.json), exist_ok=True)
            with open(args.json, "w", encoding="utf-8") as fh:
                json.dump({"status": "empty", "checks": 0, "errors": [],
                           "warnings": [], "facts": {}}, fh,
                          ensure_ascii=False, indent=2)
        return 0

    mpath = manifest_path()
    man = load(mpath, rep, required=True)
    if man is not None and mpath == MANIFEST:
        # Yarım koşuyoruz ve bunu söylüyoruz: içerik denetimleri (⑥⑦⑧⑨)
        # tam kayıt olmadan yapılamaz.
        rep.warn("tam envanter (ASSET_MANIFEST.local.json) yok — içerik "
                 "denetimleri ⑥⑦⑧⑨ ATLANDI. Tazele: ./04_BUILD/asset_manifest.py")
    if man is None:
        print("\n  ⛔ envanter yok — ./04_BUILD/asset_manifest.py")
        print("=" * 74)
        return 1

    index = load(ACTS, rep, required=False)
    regions = load(REGIONS, rep, required=False)
    cultures = load(CULTURES, rep, required=False)
    seal = load(SEAL_KEY, rep, required=False)

    check_inventory(man, book, rep)
    check_identity(man, book, index, regions, cultures, rep)
    check_layers(man, rep)
    check_raw_integrity(man, rep)
    check_dimensions(man, rep)
    check_labels(man, book, rep)
    check_observability(man, book, rep)
    check_cultural_safety(man, cultures, rep)
    check_seal_silence(man, seal, rep)
    check_rejections(man, rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · %d varlık · %d etiket · diskte %d işlenmiş"
              % (rep.checks, rep.facts.get("manifestAssets", 0),
                 rep.facts.get("requiredLabels", 0),
                 rep.facts.get("processedOnDisk", 0)))
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
