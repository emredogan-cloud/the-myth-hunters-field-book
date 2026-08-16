#!/usr/bin/env python3
"""
SAYFA BÜTÇESİ VE TELİF MODELİ — The Myth Hunter's Field Book
================================================================================
SAYFA SAYISI FİYAT MODELİNİN KENDİSİDİR.

144 yerine 160 sayfa, 14,99 $ fiyat noktasını savunulamaz hâle getirir:
baskı maliyeti sayfa başına 0,017 $ artar ve rafın çapası zaten 9,99 $.
Bu yüzden sayfa bütçesi bir tasarım tercihi değil, bir KAPIDIR.

Model dört bloktan kurulur:

    ön madde  +  altı bölge  +  final görev  +  arka madde

Bölge bloğu VERİDEN türer: her aktivitenin `pageWeight` alanı toplanır.
Bir tam sayfalık gözlem levhası 1,0; iki sığan bir şifre 0,75. Toplam,
o bölgenin kotası kadar aktivitenin ORTALAMA ağırlığıyla hesaplanır —
çünkü 120'lik nihai seçim Faz 2–4'te yapılır, bugün değil.

Üç denetim:

  ① SAYFA BANDI   — model hedefin ± toleransı içinde mi
  ② BASKI SINIRI  — KDP asgari/azami sayfa ve dörde bölünebilirlik
  ③ TELİF         — her açık sürümde telif pozitif mi, hipotezle uyuşuyor mu

TASARIM: yalnızca Python standart kütüphanesi (karar K7).

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CONFIG = os.path.join(ROOT, "project_config.json")
ACTIVITY_INDEX = os.path.join(ROOT, "01_SOURCE", "activity_index.json")
REGION_INDEX = os.path.join(ROOT, "01_SOURCE", "region_index.json")

# ── SABİT BLOKLAR ──────────────────────────────────────────────────────────
# Bu sayılar Faz 1'de kararlaştırıldı ve Faz 5'te GERÇEK DİZGİYLE ölçülecek.
# Bugün bir MODELDİR ve model olduğunu söyler.
FRONT_MATTER = {
    "title-and-copyright": 2,
    "mission-order": 2,          # görev emri — kitabın açılış anlatısı
    "how-to-use-and-tools": 1,
    "hint-rule": 1,              # ipucu kuralı: ne zaman arkaya bakılır
    "route-map-blank": 1,        # BOŞ rota haritası — doldurulmak ister
    "seal-page-blank": 1,        # BOŞ mühür sayfası
}
PER_REGION_STRUCTURAL = {
    "opening": 1,                # bölge açılışı ~150 kelime + arazi
    "seal-page": 1,              # mühür kutusu ve çentik
}
FINAL_QUEST_PAGES = 5
# ⭑ ASAMA 2 · MODEL ÖLÇÜME HİZALANDI ⭑
#
# Bu sözlük Faz 1'de bir TAHMİNDİ ve on dört sayfa varsayıyordu. Arka
# madde Aşama 2'de gerçekten dizildi ve dokuz sayfa ÖLÇÜLDÜ: `pages: N`
# alanı bir sayfa bütçesiydi, dizgi onu TEKRAR sanıyordu ve on üç
# sayfanın yedisi birebir kopyaydı. Akış dizgisine geçildi.
#
#     Model yamanmadı — ölçüm modeli yalanladı ve model ölçüme uydu.
#     (Aynı ders: `pageWeight` 0,75 · K38.)
BACK_MATTER = {
    "how-to-use": 1,
    "hint-rule": 1,
    "culture-glossary": 1,
    "sources": 1,
    "answer-key": 4,
    "world-myths-bridge": 1,
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


def measured_matter(rep):
    """⭑ FAZ 5 — ÖN/ARKA MADDE VE FİNAL GÖREV ARTIK ÖLÇÜLÜR ⭑

    Faz 1 bu üç sayıyı ELLE yazmıştı ve o gün doğruydular: manuscript
    yoktu, tahmin etmekten başka yol da yoktu. Faz 4 arka maddeyi, Faz 5
    ön maddeyi yazdı — ve o günden sonra elle yazılmış sayı bir TAHMİN
    değil bir RİSK oldu.

    ⚠ BULGU P1 — VE İKİ SAYININ NEDEN UYUŞMASI YETMEZ:

    Faz 1 ön maddeyi 8 sayıyordu ve o 8'in ikisi 'title-and-copyright'tı.
    Manuscript'in ön maddesi de 8 sayfaydı — ama içinde ne başlık ne telif
    sayfası vardı.

        İki liste TOPLAMDA uyuşuyordu ve BAŞKA BİR KİTABI tarif ediyordu.

    Toplamın eşitliği bir doğrulama değildir. Bu yüzden model artık
    manuscript'i OKUR; elle yazılmış tablo yalnızca manuscript YOKKEN
    (CI · K10) kullanılan bir YEDEKTİR ve rapor hangisinin kullanıldığını
    söyler.
    """
    front = sum(FRONT_MATTER.values())
    back = sum(BACK_MATTER.values())
    quest = FINAL_QUEST_PAGES
    source = "tahmin (manuscript depoda yok)"

    book_p = os.path.join(ROOT, "02_MANUSCRIPT", "book.json")
    if os.path.isfile(book_p):
        try:
            with open(book_p, encoding="utf-8") as fh:
                book = json.load(fh)
        except (json.JSONDecodeError, OSError):
            book = None
        if book:
            fm = book.get("frontMatter") or {}
            bm = book.get("backMatter") or {}
            fq = book.get("finalQuest") or {}
            f_secs = fm.get("sections") or []
            b_secs = bm.get("sections") or []
            if f_secs and b_secs:
                front = sum(s.get("pages", 0) for s in f_secs)
                back = sum(s.get("pages", 0) for s in b_secs)
                quest = fq.get("pages", quest)
                source = "ÖLÇÜLDÜ (manuscript)"
                # Bildirilen bütçe ile bölümlerin toplamı ayrılamaz.
                for label, secs, budget in (("ön madde", f_secs, fm.get("pageBudget")),
                                            ("arka madde", b_secs, bm.get("pageBudget"))):
                    tot = sum(s.get("pages", 0) for s in secs)
                    if budget is not None and tot != budget:
                        rep.check(False, "%s bölüm toplamı bildirilen bütçeyle "
                                  "aynı (%d ≠ %s)" % (label, tot, budget))
    rep.facts["matterSource"] = source
    return front, back, quest, source


def build_model(cfg, acts, regions, rep):
    front, back, quest, msource = measured_matter(rep)
    structural_per_region = sum(PER_REGION_STRUCTURAL.values())

    print("\n── sayfa modeli ──")
    print("  ön madde                     %3d   [%s]" % (front, msource))

    region_rows = []
    activity_pages_total = 0.0
    measured_regions = 0
    for r in regions:
        quota = r.get("activityQuota", 0)
        pool = [a for a in acts if a.get("region") == r["id"]
                and a.get("status") != "dropped"]

        # ⭑ FAZ 2 · GERÇEK SEÇİM MODELDEN ÜSTÜNDÜR ⭑
        #
        # Model, o bölgenin BÜTÜN adaylarının ortalamasını alıyordu — çünkü
        # Faz 1'de hangi 16'sının kitaba gireceği bilinmiyordu. Bir bölgenin
        # seçimi KİLİTLENDİĞİNDE tahmin etmeye gerek kalmaz: ölç.
        #
        # Fark küçük görünür ama yönü önemlidir. Havuz, kitaba girmeyecek
        # adayları da sayar ve onların ağırlıkları farklıdır.
        locked = [a for a in pool if a.get("status") in ("locked", "written")]
        if len(locked) >= quota:
            chosen = sorted(locked, key=lambda a: a.get("activityId"))[:quota]
            avg = sum(a.get("pageWeight", 1.0) for a in chosen) / len(chosen)
            source = "ÖLÇÜLDÜ"
            measured_regions += 1
        elif not pool:
            rep.warn("%s bölgesinde aday yok — model bu bölge için tahmin kullanıyor"
                     % r["id"])
            avg = 0.875
            source = "tahmin"
        else:
            avg = sum(a.get("pageWeight", 1.0) for a in pool) / len(pool)
            source = "havuz"

        pages = quota * avg
        activity_pages_total += pages
        region_rows.append({
            "region": r["id"], "quota": quota,
            "avgPageWeight": round(avg, 3),
            "weightSource": source,
            "lockedActivities": len(locked),
            "activityPages": round(pages, 1),
            "structuralPages": structural_per_region,
            "totalPages": round(pages + structural_per_region, 1),
        })
        print("  %-14s kota=%2d ort=%.3f (%-7s) aktivite=%5.1f + yapı=%d"
              % (r["id"], quota, avg, source, pages, structural_per_region))
    rep.facts["regionsMeasured"] = measured_regions

    regions_total = activity_pages_total + structural_per_region * len(regions)
    print("  bölgeler toplamı             %5.1f" % regions_total)
    print("  final görev                  %3d" % quest)
    print("  arka madde                   %3d   [%s]" % (back, msource))

    raw = front + regions_total + quest + back
    # Basılı kitap dörde bölünebilir bir forma sayısında biter.
    modeled = int(raw + 0.999)
    padded = modeled + (-modeled) % 4

    print("  ─────────────────────────────────")
    print("  ham model                    %5.1f" % raw)
    print("  yuvarlanmış                  %5d" % modeled)
    print("  forma dolgusuyla (×4)        %5d" % padded)

    rep.facts.update({
        "frontMatter": front,
        "backMatter": back,
        "structuralPerRegion": structural_per_region,
        "finalQuest": quest,
        "activityPages": round(activity_pages_total, 1),
        "regionsTotal": round(regions_total, 1),
        "modelRaw": round(raw, 1),
        "modelPages": modeled,
        "modelPagesSignatureAligned": padded,
        "regions": region_rows,
    })
    return padded


def check_band(cfg, pages, rep):
    print("\n── ① sayfa bandı ──")
    target = cfg["scope"]["pageTarget"]
    tol = cfg["scope"]["pageTolerancePct"] / 100.0
    lo, hi = target * (1 - tol), target * (1 + tol)
    delta = (pages - target) / target * 100
    rep.facts["pageTarget"] = target
    rep.facts["pageDeltaPct"] = round(delta, 2)
    rep.check(lo <= pages <= hi,
              "sayfa modeli banda oturuyor: %d ∈ [%.0f, %.0f] (hedef %d, sapma %+.1f%%)"
              % (pages, lo, hi, target, delta))


def check_print_limits(cfg, pages, rep):
    print("\n── ② baskı sınırları ──")
    pc = cfg["production"]["kdpPrintCost"]
    band = pc["paperbackLargeTrimBW"]
    rep.check(pages >= band["minPages"],
              "KDP asgari sayfa sağlanıyor (%d ≥ %d)" % (pages, band["minPages"]))
    rep.check(pages <= band["maxPages"],
              "KDP azami sayfa aşılmıyor (%d ≤ %d)" % (pages, band["maxPages"]))
    rep.check(pages % 4 == 0, "sayfa sayısı dörde bölünüyor (%d)" % pages)


def check_royalty(cfg, pages, rep):
    print("\n── ③ telif modeli ──")
    prod = cfg["production"]
    pc = prod["kdpPrintCost"]
    for ed in prod["editionsHypothesis"]:
        if not ed.get("enabled") or ed.get("list") is None:
            continue
        key = ("paperbackLargeTrimBW" if ed["id"] == "paperback"
               else "hardcoverLargeTrimBW")
        band = pc.get(key)
        if not band:
            continue
        cost = band["fixed"] + pages * band["perPage"]
        rate = (pc["royaltyRateAtOrAbove999"] if ed["list"] >= 9.99
                else pc["royaltyRateBelow999"])
        royalty = ed["list"] * rate - cost
        acos = royalty / ed["list"] if ed["list"] else 0
        rep.facts["royalty_%s" % ed["id"]] = round(royalty, 2)
        rep.facts["printCost_%s" % ed["id"]] = round(cost, 2)
        rep.facts["breakevenAcos_%s" % ed["id"]] = round(acos * 100, 1)
        print("  %-10s liste %.2f $ · baskı %.2f $ · telif %.2f $ · başabaş ACOS %%%.1f"
              % (ed["id"], ed["list"], cost, royalty, acos * 100))
        rep.check(royalty > 0, "%s telifi pozitif (%.2f $)" % (ed["id"], royalty))

    # BRIEF § 7 dayanağı config'ten OKUNUR, buraya gömülmez.
    #
    # ⚠ Faz 2'de düzeltildi: bu sayı (5,55 $) betiğe gömülüydü ve kurucu
    # kararı A8→K19 kapandığında BRIEF ile birlikte İKİ YERDE birden
    # değiştirilmesi gerekiyordu. İki yerde duran bir sayı er geç iki
    # farklı şey söyler. Tek doğruluk kaynağı project_config.json'dur.
    base = prod.get("royaltyBaseline", {})
    hyp = base.get("paperback")
    warn_at = base.get("driftWarnAt", 0.05)
    fail_at = base.get("driftFailAt", 0.25)
    got = rep.facts.get("royalty_paperback")
    if got is not None and hyp is not None:
        drift = abs(got - hyp)
        rep.facts["royaltyBaseline"] = hyp
        rep.facts["royaltyDriftVsBaseline"] = round(got - hyp, 2)
        rep.check(drift <= fail_at,
                  "ciltsiz telifi kabul edilen dayanakla uyumlu (%.2f $ ≈ %.2f $)"
                  % (got, hyp))
        # Sessiz sapma yasaktır: model dayanaktan ayrıldığı anda GÖRÜNÜR olur.
        #
        # ⚠ SAPMANIN YÖNÜ ÖNEMLİDİR ve ilk hâl bunu ayırt etmiyordu.
        # Model UCUZLADIĞINDA "BRIEF güncellenmeli VEYA sayfa kısılmalı"
        # demek anlamsızdır — kısacak bir şey yoktur, model zaten küçüldü.
        # Bir uyarı yanlış eylemi öneriyorsa, o uyarı bir gürültüdür.
        if drift > warn_at:
            measured = rep.facts.get("regionsMeasured", 0)
            total_regions = len(rep.facts.get("regions", []) or [])
            coverage = ("%d/%d bölge GERÇEK içerikle ölçüldü"
                        % (measured, total_regions))
            if got > hyp:
                # ⚠ FAZ 5: A12 KAPANDI — KURUCU 144'Ü ONAYLADI (K33).
                #
                # Faz 4'te bu dal "dayanağın gözden geçirilmesi artık bir
                # KURUCU KARARIDIR" diyordu ve doğruydu: o an karar
                # bekliyordu. Karar geldi ve dayanak ölçümle hizalandı, yani
                # bu dal artık NORMAL koşulda hiç yanmaz — yanarsa dayanak
                # ile model YENİDEN ayrılmış demektir ve söylenecek şey
                # başkadır.
                #
                # Bir uyarı, beklediği karar alındıktan sonra hâlâ o kararı
                # BEKLİYOR gibi konuşursa, okuyanı kapanmış bir kalemi
                # yeniden açmaya çağırır.
                decision = (cfg.get("scope", {}).get("pageTargetDecision")
                            or "kayıtsız")
                tail = ("A12 KAPANDI (%s): dayanak ÖLÇÜLMÜŞ modelle "
                        "hizalanmıştı ve şimdi yeniden AYRILDI — sebebi "
                        "bulunmalıdır." % decision
                        if measured >= total_regions and total_regions else
                        "Bir bölgeden bütün kitaba genelleme YAPILMAZ; kalan "
                        "bölgeler ölçülünce dayanak gözden geçirilir.")
                rep.warn("ciltsiz telifi dayanaktan %+.2f $ YÜKSEK "
                         "(%.2f $ vs %.2f $) — sayfa modeli KÜÇÜLDÜ. %s. %s "
                         "Hedef SESSİZCE değiştirilmez: değişiklik "
                         "scope.pageTargetHistory'ye bir kayıt EKLER "
                         "(validate_spec § ⑦)."
                         % (got - hyp, got, hyp, coverage, tail))
            else:
                rep.warn("ciltsiz telifi dayanaktan %+.2f $ DÜŞÜK "
                         "(%.2f $ vs %.2f $) — sayfa modeli BÜYÜDÜ. %s. "
                         "BRIEF § 7 ve project_config § royaltyBaseline "
                         "güncellenmeli VEYA kapsam kısılmalı; bu bir "
                         "KURUCU kararıdır."
                         % (got - hyp, got, hyp, coverage))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    print("=" * 74)
    print("  SAYFA BÜTÇESİ VE TELİF MODELİ")
    print("=" * 74)

    rep = Report(args.verbose)
    cfg = load(CONFIG, rep)
    if cfg is None:
        return 1

    acts_doc = load(ACTIVITY_INDEX, rep, required=False)
    reg_doc = load(REGION_INDEX, rep, required=False)
    if reg_doc is None:
        rep.warn("region_index.json yok — Faz 1 teslimatı; sayfa bütçesi boş koşuyor")
        print("\n" + "=" * 74)
        print("  ⊘ boş koştu")
        print("=" * 74)
        if args.json:
            os.makedirs(os.path.dirname(args.json), exist_ok=True)
            with open(args.json, "w", encoding="utf-8") as fh:
                json.dump({"status": "empty", "checks": 0, "errors": [],
                           "warnings": rep.warnings, "facts": {}},
                          fh, ensure_ascii=False, indent=2)
        return 0

    acts = (acts_doc or {}).get("activities", []) if acts_doc else []
    regions = reg_doc.get("regions", reg_doc)

    pages = build_model(cfg, acts, regions, rep)
    check_band(cfg, pages, rep)
    check_print_limits(cfg, pages, rep)
    check_royalty(cfg, pages, rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · model %d sayfa · ciltsiz telif %.2f $"
              % (rep.checks, pages, rep.facts.get("royalty_paperback", 0)))
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
