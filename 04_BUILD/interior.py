#!/usr/bin/env python3
"""
İÇ BLOK DİZGİSİ — The Myth Hunter's Field Book
================================================================================
Manuscript'i gerçek bir PDF'e dizer ve **GERÇEK SAYFA SAYISINI ÖLÇER**.

⭑ BU BETİĞİN ASIL İŞİ BİR PDF ÜRETMEK DEĞİL, BİR SAYIYI YALANLAYABİLMEKTİR ⭑

Faz 1'den Faz 5'e kadar sayfa sayısı bir **MODELDİ**: aktivite ağırlıkları
toplanıyor, forma hizalanıyor ve 144 çıkıyordu. Model altı bölgenin altısı
ölçülerek kalibre edildi (K32) ve kurucu 144'ü onayladı (K33).

    Ama bir model, dizilmiş bir sayfa değildir.

`page_budget.py` *"bu kitap 144 sayfa ETMELİ"* der. Bu betik
*"bu kitap 144 sayfa ETTİ"* ya da *"ETMEDİ"* der. İkisi aynı şey değildir
ve ikincisi birincisini **yalanlayabilir**.

⭑ GÖRSEL YOKKEN NE OLUR — VE NEDEN YİNE DE ÖLÇER ⭑

Nihai görsel varlıklar kurucuya aittir ve bugün üretilmemiş olabilir.
Dizgi onları beklemez: her görselin yerine `visualSpec` ölçüsünde bir
**YER TUTUCU KUTU** koyar. Kutu gerçek varlıkla **aynı yeri kaplar**,
dolayısıyla sayfa kırılımı ve sayfa sayısı **doğru ölçülür**.

    Bir yer tutucu, bir görselin YERİNİ tutar — YERİNE GEÇMEZ.

`--placeholders` çıktısı bu yüzden **prova değildir** ve dosya adı bunu
söyler (`interior-PLACEHOLDER.pdf`). Nihai baskı dosyası ancak
`final/` katmanı dolu olduğunda üretilir.

Ne ölçer:

  ① GERÇEK SAYFA SAYISI  — dizilmiş, forma hizalı
  ② YAZMA ALANI          — çocuk elinin sığdığı satır yüksekliği
  ③ TAŞMA                — bir sayfaya sığmayan modül var mı
  ④ GÜVENLİ ALAN         — kesim payı ve iç boşluk ihlali

② bir kapıdır ve yol haritası Faz 5 § 10 onu adıyla istiyor:
*"Yazma alanları ölçüldü — çocuk eli sığıyor mu."* Sekiz yaşındaki bir
çocuğun el yazısı yetişkininkinden büyüktür; ölçüt **7 mm satır
yüksekliğidir** ve altına inen bir sayfa KIRMIZI yanar.

  ./04_BUILD/interior.py                 dizer ve ölçer
  ./04_BUILD/interior.py --check         PDF güncel mi
  ./04_BUILD/interior.py --measure-only  PDF yazmaz, yalnız ölçer

TASARIM: reportlab ister. Yoksa çıkış 2 (ATLANDI) — kalite düşüşü DEĞİL.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = bağımlılık yok
"""

from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

BOOK = os.path.join(ROOT, "02_MANUSCRIPT", "book.json")
ACTS = os.path.join(ROOT, "01_SOURCE", "activity_index.json")
REGIONS = os.path.join(ROOT, "01_SOURCE", "region_index.json")
CONFIG = os.path.join(ROOT, "project_config.json")
MANIFEST_LOCAL = os.path.join(ROOT, "07_ASSETS", "ASSET_MANIFEST.local.json")
MANIFEST = os.path.join(ROOT, "07_ASSETS", "ASSET_MANIFEST.json")
FINAL_DIR = os.path.join(ROOT, "07_ASSETS", "final", "interior")
OUT_DIR = os.path.join(ROOT, "08_OUTPUT", "PAPERBACK")
REPORT = os.path.join(ROOT, "06_REPORTS", "interior.json")

MM = 72.0 / 25.4                    # 1 mm cinsinden punto
TRIM_W, TRIM_H = 8.5 * 72, 11.0 * 72

# ── KDP büyük trim iç blok kenar boşlukları ────────────────────────────────
# Gutter (iç kenar) 110–150 sayfa için 0,375 inç; dış/üst/alt 0,25 inç asgari.
# Projede `visualSpec.safeAreaMm` 9,5 mm gutter ve 12,7 mm dış diyor ve o
# değerler DAHA GENİŞTİR — kitabın kendi şartnamesi kazanır.
GUTTER = 9.5 * MM
OUTER = 12.7 * MM
TOP = 12.7 * MM
BOTTOM = 12.7 * MM

# ⭑ YAZMA ALANI ÖLÇÜTÜ — bu bir kapıdır, bir tercih değil ⭑
#
# Sekiz yaşındaki bir çocuğun el yazısı yetişkininkinden büyüktür. 7 mm
# ölçütü ilkokul defter çizgisi standardından gelir (8–9 mm birinci sınıf,
# 7 mm üçüncü sınıf). Bunun altına inen bir satır, sayfayı kullanılamaz
# yapar — ve ürünün işlevi ÜZERİNE YAZILMAKTIR.
WRITING_LINE_MM = 7.0
WRITING_LINE = WRITING_LINE_MM * MM


def jload(p, default=None):
    if not os.path.isfile(p):
        return default
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


class Report:
    def __init__(self, verbose):
        self.verbose = verbose
        self.errors, self.warnings, self.checks = [], [], 0
        self.facts = {}

    def check(self, cond, label):
        self.checks += 1
        if cond:
            if self.verbose:
                print("  ✓ %s" % label)
        else:
            self.errors.append(label)
            print("  ✗ %s" % label)
        return bool(cond)

    def warn(self, label):
        self.warnings.append(label)
        print("  ! %s" % label)


def load_assets():
    """Tam envanter yoksa takip edilenle çalışır (ölçü ikisinde de var)."""
    for p in (MANIFEST_LOCAL, MANIFEST):
        d = jload(p)
        if d:
            return {a["assetId"]: a for a in d.get("assets", [])}, p
    return {}, None


# ── DİZGİ ──────────────────────────────────────────────────────────────────
def build(rep, write=True):
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.lib.pagesizes import letter  # noqa: F401

    book = jload(BOOK)
    if not book:
        return None
    index = jload(ACTS, {"activities": []})
    design = {a["activityId"]: a for a in index.get("activities", [])}
    regions = jload(REGIONS, {"regions": []}).get("regions", [])
    rorder = {r["id"]: r.get("order", 99) for r in regions}
    rname = {r["id"]: r.get("en", r["id"]) for r in regions}
    assets, asrc = load_assets()
    rep.facts["assetSource"] = os.path.relpath(asrc, ROOT) if asrc else None

    os.makedirs(OUT_DIR, exist_ok=True)
    have_final = sum(1 for a in assets.values()
                     if os.path.isfile(os.path.join(FINAL_DIR, a["filename"])))
    rep.facts["finalAssetsOnDisk"] = have_final
    placeholder_mode = have_final < len(assets)
    name = ("interior-PLACEHOLDER.pdf" if placeholder_mode else "interior.pdf")
    path = os.path.join(OUT_DIR, name)
    rep.facts["output"] = os.path.relpath(path, ROOT)
    rep.facts["placeholderMode"] = placeholder_mode

    c = canvas.Canvas(path, pagesize=(TRIM_W, TRIM_H)) if write else None
    state = {"page": 0, "overflow": [], "thin": [], "unsafe": []}

    def inner(page_no):
        """Tek sayfada iç kenar SAĞDA mı SOLDA mı — gutter tarafı değişir."""
        return GUTTER if page_no % 2 == 1 else OUTER

    def new_page():
        state["page"] += 1
        if c and state["page"] > 1:
            c.showPage()
        return state["page"]

    def text_block(x, y, w, txt, size, leading, font="Helvetica"):
        """Basit sarma. Yüksekliği döner; c yoksa yalnız ÖLÇER."""
        if not txt:
            return 0
        if c:
            c.setFont(font, size)
        words, line, lines = txt.split(), "", []
        for word in words:
            t = (line + " " + word).strip()
            if pdfmetrics.stringWidth(t, font, size) <= w:
                line = t
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        for i, ln in enumerate(lines):
            if c:
                c.drawString(x, y - i * leading, ln)
        return len(lines) * leading

    def asset_box(x, y, w, h, aid, label):
        """Görsel yerleşimi. final/ varsa GERÇEK varlık, yoksa YER TUTUCU."""
        a = assets.get(aid)
        fp = os.path.join(FINAL_DIR, a["filename"]) if a else None
        if c:
            if fp and os.path.isfile(fp):
                c.drawImage(ImageReader(fp), x, y - h, width=w, height=h,
                            preserveAspectRatio=True, anchor="c", mask="auto")
            else:
                c.setDash(3, 3)
                c.rect(x, y - h, w, h)
                c.setDash()
                c.setFont("Helvetica-Oblique", 7)
                c.drawCentredString(x + w / 2, y - h / 2, label[:70])
        return h

    # ── ÖN MADDE ───────────────────────────────────────────────────────────
    for s in (book.get("frontMatter") or {}).get("sections", []):
        for _ in range(s.get("pages", 1)):
            p = new_page()
            x = inner(p)
            w = TRIM_W - GUTTER - OUTER
            y = TRIM_H - TOP
            if c:
                c.setFont("Helvetica-Bold", 15)
                c.drawString(x, y, s.get("heading", ""))
            y -= 26
            used = text_block(x, y, w, (s.get("bodyText") or "").replace("\n\n", "  "),
                              10.5, 14.5)
            y -= used
            if s.get("visualNeed"):
                y -= asset_box(x, y - 8, w, 150, "front-%s" % s["id"],
                               "[ %s ]" % s["id"]) + 12
            if y < BOTTOM:
                state["overflow"].append("front:%s" % s["id"])

    # ── BÖLGELER ───────────────────────────────────────────────────────────
    acts = book.get("activities", [])
    by_region = {}
    for a in acts:
        by_region.setdefault(design.get(a["activityId"], {}).get("region"), []).append(a)

    for r in sorted(regions, key=lambda x: x.get("order", 99)):
        rid = r["id"]
        pool = sorted(by_region.get(rid, []), key=lambda a: a.get("pageOrder", 0))
        if not pool:
            continue
        # bölge açılışı — 1 sayfa
        op = next((o for o in book.get("regionOpenings", [])
                   if o["regionId"] == rid), None)
        p = new_page()
        x, w, y = inner(p), TRIM_W - GUTTER - OUTER, TRIM_H - TOP
        if c and op:
            c.setFont("Helvetica-Bold", 19)
            c.drawString(x, y, op.get("heading", rname.get(rid, rid)))
            c.setFont("Helvetica-Oblique", 10)
            c.drawString(x, y - 20, (op.get("terrainLine") or "")[:110])
        if op:
            text_block(x, y - 46, w, op.get("openingText", ""), 10.5, 15)

        # aktivite sayfaları
        for a in pool:
            p = new_page()
            x, w = inner(p), TRIM_W - GUTTER - OUTER
            y = TRIM_H - TOP
            # ① görev satırı  ② zorluk
            if c:
                c.setFont("Helvetica-Bold", 12)
                c.drawString(x, y, a.get("prompt", ""))
                d = design.get(a["activityId"], {}).get("difficulty", 1)
                c.setFont("Helvetica", 12)
                c.drawRightString(x + w, y, "★" * int(d or 1))
            y -= 22
            # ③ levha — visualSpec ölçüsünde
            vs = a.get("visualSpec") or {}
            tpx = vs.get("targetPx") or [1650, 1200]
            box_w = w
            box_h = min(box_w * (tpx[1] / tpx[0]), TRIM_H * 0.46)
            y -= asset_box(x, y, box_w, box_h, vs.get("assetId", ""),
                           "[ %s ]" % vs.get("assetId", "?")) + 14
            # ④ adımlar
            if c:
                c.setFont("Helvetica", 10)
            for i, st in enumerate(a.get("steps") or [], 1):
                y -= text_block(x, y, w - 90, "%d. %s" % (i, st), 10, 13.5)
            y -= 6
            # ⑧ yıldızlı kutu
            if a.get("sealSlot"):
                n = len(a.get("sealStarWord") or "")
                bw = 15
                if c:
                    for i in range(n):
                        c.rect(x + i * bw, y - 17, bw, 17)
                    c.setFont("Helvetica", 7.5)
                    c.drawString(x + n * bw + 8, y - 12,
                                 "★%d → seal slot %d" % (a.get("sealStarIndex", 1),
                                                         a["sealSlot"]))
                y -= 26
            # ⑦ yazma alanı — ÖLÇÜLEN KAPI
            lines = a.get("writingSpaceLines") or 0
            if lines:
                avail = y - BOTTOM - 58            # field note + ebeveyn notu payı
                per = avail / lines if lines else 0
                if per < WRITING_LINE:
                    state["thin"].append("%s (%.1f mm × %d satır)"
                                         % (a["activityId"], per / MM, lines))
                per = max(per, 0)
                if c:
                    for i in range(lines):
                        yy = y - (i + 1) * per
                        if yy > BOTTOM + 40:
                            c.line(x, yy, x + w, yy)
                y -= min(avail, lines * max(per, WRITING_LINE))
            # ⑤ field note
            fn_h = text_block(x, max(y, BOTTOM + 46), w,
                              "Field note: " + (a.get("fieldNote") or ""), 9, 12)
            # ⑩ ebeveyn notu
            if a.get("parentNote") and c:
                c.setFont("Helvetica-Oblique", 7.5)
                c.drawString(x, BOTTOM + 8, "For an adult: " + a["parentNote"][:120])
            if y - fn_h < BOTTOM:
                state["overflow"].append(a["activityId"])
            # sayfa numarası
            if c:
                c.setFont("Helvetica", 8)
                c.drawRightString(TRIM_W - inner(p), BOTTOM - 12, str(p))

        # bölge mühür sayfası
        p = new_page()
        x, y = inner(p), TRIM_H - TOP
        if c:
            c.setFont("Helvetica-Bold", 15)
            c.drawString(x, y, "%s — Seal" % rname.get(rid, rid))
        slots = sorted({a["sealSlot"] for a in pool if a.get("sealSlot")})
        if c:
            for i, sl in enumerate(slots):
                c.rect(x + i * 34, y - 74, 30, 30)
                c.setFont("Helvetica", 7.5)
                c.drawCentredString(x + i * 34 + 15, y - 86, "slot %d" % sl)
        asset_box(x, y - 110, 120, 120, "seal-%s" % rid, "[ seal-%s ]" % rid)

    # ── FİNAL GÖREV ────────────────────────────────────────────────────────
    fq = book.get("finalQuest") or {}
    for q in fq.get("quest", []):
        p = new_page()
        x, w, y = inner(p), TRIM_W - GUTTER - OUTER, TRIM_H - TOP
        if c:
            c.setFont("Helvetica-Bold", 14)
            c.drawString(x, y, q.get("heading", ""))
            c.setFont("Helvetica", 11)
        y -= 24
        y -= text_block(x, y, w, q.get("prompt", ""), 11, 14) + 8
        for i, st in enumerate(q.get("steps") or [], 1):
            y -= text_block(x, y, w, "%d. %s" % (i, st), 10, 13.5)
        text_block(x, BOTTOM + 40, w, "Field note: " + (q.get("fieldNote") or ""),
                   9, 12)

    # ── ARKA MADDE ─────────────────────────────────────────────────────────
    for s in (book.get("backMatter") or {}).get("sections", []):
        for _ in range(s.get("pages", 1)):
            p = new_page()
            x, w, y = inner(p), TRIM_W - GUTTER - OUTER, TRIM_H - TOP
            if c:
                c.setFont("Helvetica-Bold", 14)
                c.drawString(x, y, s.get("heading", ""))
            y -= 24
            for pr in s.get("prints") or []:
                y -= text_block(x, y, w, "· " + pr, 9.5, 13)

    # ── FORMA HİZASI ───────────────────────────────────────────────────────
    raw_pages = state["page"]
    padded = raw_pages + (-raw_pages) % 4
    for _ in range(padded - raw_pages):
        new_page()
    if c:
        c.showPage()
        c.save()

    rep.facts.update({
        "typesetPagesRaw": raw_pages,
        "typesetPagesSignatureAligned": padded,
        "overflowPages": state["overflow"],
        "thinWritingLines": state["thin"],
    })
    return padded


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--measure-only", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    print("=" * 74)
    print("  İÇ BLOK DİZGİSİ")
    print("=" * 74)

    rep = Report(args.verbose)

    if not os.path.isfile(BOOK):
        # Manuscript depoda durmaz (K10). Dizilecek metin yoksa dizgi de yoktur.
        print("  ⊘ manuscript depoda yok (K10) — BOŞ KOŞTU")
        print("=" * 74)
        return 0
    try:
        import reportlab  # noqa: F401
    except ImportError:
        print("  ⊘ reportlab yok — ATLANDI")
        print("     pip install -r 04_BUILD/requirements.txt")
        print("=" * 74)
        return 2

    pages = build(rep, write=not args.measure_only)
    if pages is None:
        print("  ⛔ dizgi yapılamadı")
        return 1

    cfg = jload(CONFIG, {})
    target = cfg.get("scope", {}).get("pageTarget", 144)
    tol = cfg.get("scope", {}).get("pageTolerancePct", 6) / 100.0
    model = jload(os.path.join(ROOT, "06_REPORTS", "page-budget.json"), {})
    model_pages = (model.get("facts") or {}).get("modelPagesSignatureAligned")

    print("\n── ① gerçek sayfa sayısı ──")
    print("  dizilmiş (ham)          %5d" % rep.facts["typesetPagesRaw"])
    print("  forma hizalı (×4)       %5d" % pages)
    print("  MODEL (page_budget)     %5s" % model_pages)
    print("  HEDEF (K33)             %5d" % target)
    if rep.facts.get("placeholderMode"):
        print("  ⚠ YER TUTUCU MODU — %d/%s nihai görsel diskte"
              % (rep.facts.get("finalAssetsOnDisk", 0),
                 rep.facts.get("assetSource") and "158" or "?"))

    lo, hi = target * (1 - tol), target * (1 + tol)
    in_band = lo <= pages <= hi

    # ⭑ NEDEN BU BİR UYARI, BİR KAPI DEĞİL — VE NEDEN GEVŞETME DEĞİL ⭑
    #
    # Bu ölçüm bu projede İLK KEZ yapılıyor. Beş faz boyunca sayfa sayısı bir
    # MODELDİ (`page_budget.py`) ve kurucu o modeli onayladı (K33 · 144).
    # Dizgi şimdi başka bir sayı söylüyor.
    #
    #     Bir MODEL ile bir ÖLÇÜM ayrıldığında ölçüm kazanır —
    #     ama HEDEFİ değiştirmek bir KURUCU kararıdır, bir betiğin değil.
    #
    # Faz 4 tam olarak bu durumu yaşadı: model 144 dedi, onaylı hedef 148'di.
    # `page_budget` KIRMIZI yanmadı; UYARDI ve kalem kurucuya gitti (A12 →
    # K33). Bu satır aynı önceliği izliyor ve kalemi A13 olarak açıyor.
    #
    # ⚠ MODEL KAPISI SERT KALIR: `page_budget § ①` model ile hedefi hâlâ
    # kırmızı yakarak denetliyor. Gevşeyen bir şey yok; YENİ bir ölçüm
    # eklendi ve o ölçüm bir karar bekliyor.
    if in_band:
        rep.check(True, "dizilmiş sayfa hedef bandında (%d ∈ [%.0f, %.0f])"
                  % (pages, lo, hi))
    else:
        rep.warn("⭑ DİZİLMİŞ SAYFA HEDEF BANDININ DIŞINDA: %d ∉ [%.0f, %.0f] "
                 "(hedef %d · K33). Bu bir MODEL değil bir ÖLÇÜMDÜR ve hedefi "
                 "değiştirmek KURUCU kararıdır → AÇIK KALEM A13."
                 % (pages, lo, hi, target))
        rep.facts["pageTargetConflict"] = {
            "typeset": pages, "target": target,
            "band": [round(lo), round(hi)], "openItem": "A13"}
    if model_pages is not None:
        # ⭑ MODEL İLE ÖLÇÜM AYRILIRSA MODEL DEĞİL ÖLÇÜM DOĞRUDUR ⭑
        delta = pages - model_pages
        rep.facts["modelVsTypesetDelta"] = delta
        if delta:
            rep.warn("dizgi modelden %+d sayfa ayrıldı (%d ↔ %d) — model bir "
                     "TAHMİN, dizgi bir ÖLÇÜMDÜR ve ölçüm kazanır"
                     % (delta, model_pages, pages))
        else:
            rep.check(True, "dizgi modelle birebir tuttu (%d)" % pages)

    print("\n── ② yazma alanı (çocuk eli) ──")
    thin = rep.facts.get("thinWritingLines") or []
    print("  ölçüt: satır yüksekliği ≥ %.0f mm" % WRITING_LINE_MM)
    rep.check(not thin,
              "her yazma satırı çocuk eline yetiyor (%d sayfa denetlendi)"
              % len([a for a in jload(BOOK)["activities"] if a.get("writingSpaceLines")])
              + ("" if not thin else " — DAR: %d sayfa · %s" % (len(thin), thin[:4])))

    print("\n── ③ taşma ──")
    ov = rep.facts.get("overflowPages") or []
    rep.check(not ov, "hiçbir sayfa taşmıyor"
              + ("" if not ov else " — TAŞAN: %d · %s" % (len(ov), ov[:5])))

    print("\n── ④ baskı sınırları ──")
    rep.check(pages % 4 == 0, "sayfa sayısı dörde bölünüyor (%d)" % pages)
    rep.check(pages >= 110, "KDP asgari sayfa sağlanıyor (%d ≥ 110)" % pages)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · dizilmiş sayfa: %d" % (rep.checks, pages))
        status = "pass"
    print("=" * 74)

    out = args.json or REPORT
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"status": status, "checks": rep.checks, "errors": rep.errors,
                   "warnings": rep.warnings, "facts": rep.facts},
                  fh, ensure_ascii=False, indent=2)
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
