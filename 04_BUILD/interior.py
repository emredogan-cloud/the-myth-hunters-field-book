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
import re
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

# ═══════════════════════════════════════════════════════════════════════════
# KDP KENAR BOŞLUKLARI — İÇ KENAR SAYFA SAYISINDAN TÜRETİLİR
# ═══════════════════════════════════════════════════════════════════════════
#
# ⭑ BU SABİT YAZILDIĞI GÜN DOĞRUYDU VE SESSİZCE YANLIŞ OLDU ⭑
#
# Eski hâl:
#
#     # Gutter (iç kenar) 110–150 sayfa için 0,375 inç
#     GUTTER = 9.5 * MM        # = 0,374 in
#
# Yorum kendi kademesini de yazıyordu: **110–150 sayfa**. Kitap 144 →
# 160 → 156 sayfaya taşındı ve sabit taşınmadı. 156 sayfa KDP'nin
# **151–300** kademesindedir ve **0,5 inç** ister.
#
# Gerçek KDP Print Previewer bunu buldu; yerel CI yeşildi:
#
#     "Insufficient gutter. Books with 156 pages require at least 0.5\"
#      (12.700mm) for the gutter / inside margin…"
#
# Ölçüm: **156 sayfanın 152'si** iç kenarı ihlal ediyordu (0,367–0,447 in).
#
#     Sayfa sayısından TÜREMESİ gereken bir ölçü elle yazılırsa,
#     sayfa sayısı değiştiği gün sessizce yanlış olur.
#
# `metadata § açıklama` ile birebir aynı sınıf (K41). Çözüm de aynı:
# sayı artık TÜRETİLİYOR ve `qa_margins` onu basılı sayfadan ölçüyor.
#
# ⚠ İÇ KENAR SAYFA SAYISINA, SAYFA SAYISI DİZGİYE BAĞLI.
# Bu döngüseldir ve YAKINSAMAYLA çözülür: dizgi bir kademeyle koşar,
# gerçek sayfa sayısını ölçer, kademe değiştiyse YENİDEN koşar.
GUTTER_TIERS = [
    (24, 150, 0.375),
    (151, 300, 0.500),
    (301, 500, 0.625),
    (501, 700, 0.750),
    (701, 828, 0.875),
]
# Bleed YOK: dış/üst/alt asgarisi 0,25 in. Proje 0,5 in kullanıyor ve
# bu DAHA GENİŞTİR — kitabın kendi şartnamesi kazanır (ve KDP'yi aşar).
OUTSIDE_MIN_NO_BLEED = 0.25
OUTSIDE_MIN_WITH_BLEED = 0.375


def kdp_gutter_inches(pages):
    """KDP iç kenar asgarisi — kademe SAYFA SAYISI seçer, insan değil."""
    for lo, hi, val in GUTTER_TIERS:
        if lo <= pages <= hi:
            return val
    return GUTTER_TIERS[-1][2] if pages > 828 else GUTTER_TIERS[0][2]


# ⭑ ASGARİNİN TAM ÜSTÜNDE OTURMAK KIRILGANDIR ⭑
#
# Ölçüm, dizginin KDP asgarisine (0,5 in) TAM oturduğunu gösterdi. Bu
# uyumludur — ama sıfır paylıdır ve iki gerçek risk taşır:
#
#   ① KDP ">= 0,5" mi ">0,5" mi uyguluyor bilinmiyor; tam sınırda
#      duran bir sayfa, aracın yuvarlamasına bağımlı hâle gelir.
#   ② 156 sayfalık tutkallı bir ciltte "binding creep" vardır: orta
#      formalarda iç kenar GÖRSEL olarak daralır.
#
# Bu yüzden asgarinin üstüne KÜÇÜK ve BEYAN EDİLMİŞ bir pay eklenir.
# Sütun 7,500 → 7,470 inç olur (%0,4 daralma) ve hiçbir yazma alanı,
# levha ya da kart bundan zarar görmez (`qa_margins` + yazma alanı
# kapısı ikisini de ölçüyor).
#
#     Bu bir kapıyı susturma payı DEĞİLDİR — ölçüm zaten geçiyordu.
#     Bu, ciltlenmiş bir kitabın gerçeğine ayrılmış paydır.
GUTTER_SAFETY = 0.03

# ⭑ İÇ BLOK SANATI İÇİN ETKİN ÇÖZÜNÜRLÜK TABANI ⭑
# K39 kurucu kararı: iç blok 150 dpi. Bu bir PROJE İÇİ indirilmiş
# eşiktir ve KDP'nin 300 dpi tavsiyesine uygunluk KANITI DEĞİLDİR —
# ama beyan edildiği için TUTULMAK ZORUNDADIR. Dizgi bir görseli bu
# tabanın altına düşürecek kadar büyütemez.
ART_DPI_FLOOR = 150.0

# Çalışma anında `build()` tarafından sayfa sayısından yeniden atanır.
GUTTER = 0.5 * 72
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

# ═══════════════════════════════════════════════════════════════════════════
# YAZI TİPİ — GÖMÜLÜR, VE BU İKİ AYRI KUSURU BİRDEN KAPATIR
# ═══════════════════════════════════════════════════════════════════════════
#
# Faz 6 iç bloğu base-14 `Helvetica` ile dizdi. Ölçüldü:
#
#     pdffonts interior.pdf
#       Helvetica       Type 1   WinAnsi   emb=no
#       Helvetica-Bold  Type 1   WinAnsi   emb=no
#       ZapfDingbats    Type 1   ...       emb=no
#
# ① HİÇBİR YAZI TİPİ GÖMÜLÜ DEĞİLDİ. KDP ciltsiz iç bloğu bütün yazı
#    tiplerinin gömülü olmasını ister; gömülmemiş bir yazı tipi
#    basımevinin ikamesiyle basılır ve satır sonları kayar.
#
# ② WinAnsi KİTABIN KENDİ İMLÂSINI TAŞIYAMIYORDU. Faz 5'in `A13`
#    düzeltmesi on dört ad geçişine işaret eklemişti — `Yorùbá`,
#    `Òṣun-Òṣogbo`, `Skíðblaðnir`, `Mjölnir`, `Cú Chulainn`, `Whangārei`.
#    Bu kod noktaları WinAnsi'de YOKTUR ve dizgide DÜŞTÜ. Basılan:
#
#        M■ori          ← ön maddede · imlâ kuralını ÖĞRETEN sayfada
#
#    Kaynak doğruydu, dizgi onu basamıyordu.
#
#     ⭑ Bir kitabın "işaretler önemlidir" diyen sayfası,
#       işareti basamıyordu. ⭑
#
# DejaVu Sans Latin Genişletilmiş Ek'i (U+1E00–U+1EFF) ve `★` (U+2605)
# kapsar. Yazı tipleri `07_ASSETS/fonts/` altındadır ve depoya girmez
# (.gitignore § ④); build makinesinde yoksa sistem yolları denenir.
FONT_DIR = os.path.join(ROOT, "07_ASSETS", "fonts")
SYS_FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/local/share/fonts/dejavu",
]
FONT_FILES = {
    "Body": "DejaVuSans.ttf",
    "Body-Bold": "DejaVuSans-Bold.ttf",
    "Body-Italic": "DejaVuSans-Oblique.ttf",
}

# ⭑ CJK YEDEĞİ — CEVAP ANAHTARI HANGUL VE KANJİ TAŞIYOR ⭑
#
# Cevap anahtarı gerçek cevapları basar ve bazıları Latin DEĞİLDİR:
# 서울 · 광주 · 済州 · ひらがな · カタカナ. DejaVu bu blokları
# KAPSAMAZ ve ilk dizgide hepsi TOFU (boş kutu) olarak bastı.
#
#     Bir cevabın basılamaması, o cevabın yanlış basılmasıdır.
#
# reportlab kendiliğinden yedek yazı tipine düşmez; bu yüzden CJK
# taşıyan satırlar AYRI bir yazı tipiyle dizilir.
# ⚠ Noto CJK KULLANILAMADI: `.ttc` dosyaları PostScript (CFF) dış hat
# taşıyor ve reportlab onları gömemiyor ("postscript outlines are not
# supported"). Gömülemeyen bir yazı tipi bu kitap için YOK demektir.
# Droid Sans Fallback TrueType'tır ve CJK + kana KAPSAR.
CJK_CANDIDATES = [
    ("/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf", None),
]
FONT_CJK = "Body-CJK"


# Kayıtlı yazı tiplerinin gerçekten BASABİLDİĞİ kod noktaları.
# Bir karakteri "basıyoruz" sanıp tofu bırakmak, basmamaktan kötüdür.
CMAPS: dict = {}


def renderable(txt, fonts):
    """Basılabilen metni ve DÜŞÜRÜLEN karakter sayısını döner.

    ⭑ HANGUL BU MAKİNEDE BASILAMIYOR — VE BU GİZLENMEZ ⭑

    Cevap anahtarı Korece yer adlarını hem hangul hem romanizasyonla
    taşıyor: `서울 Seoul · 부산 Busan`. Sistemde gömülebilir (TrueType)
    hiçbir yazı tipi hangul kapsamıyor: Noto CJK CFF dış hatlı,
    Droid Sans Fallback ise hangul taşımıyor.

        Basılamayan bir karakteri yine de basmak,
        sayfaya BOŞ KUTU koymaktır — ve boş kutu, eksik bilgiden
        daha kötüdür: yanlış basılmış gibi görünür.

    Bu yüzden basılamayan koşular DÜŞÜRÜLÜR, romanizasyon KALIR ve
    cevap anahtarı sayfası bunu okura AÇIKÇA söyler. Düşen karakter
    sayısı rapora yazılır; sessiz bir kayıp yoktur."""
    if not txt:
        return txt, 0
    ok, dropped = [], 0
    for ch in txt:
        if ch in " \t·—-–,.:;()[]/'\"":
            ok.append(ch)
            continue
        if any(ord(ch) in CMAPS.get(f, ()) for f in fonts) or not CMAPS:
            ok.append(ch)
        else:
            dropped += 1
    out = " ".join("".join(ok).split())
    return out, dropped


def has_cjk(txt):
    """Latin dışı CJK/Hangul/Kana taşıyor mu."""
    return any(
        0x2E80 <= ord(ch) <= 0x9FFF or 0xAC00 <= ord(ch) <= 0xD7AF
        or 0x3040 <= ord(ch) <= 0x30FF or 0xF900 <= ord(ch) <= 0xFAFF
        for ch in (txt or ""))
# Kayıt başarısız olursa base-14'e düşülür — ama SESSİZCE DEĞİL:
# `rep.facts["fontsEmbedded"]` false olur ve `§ ⑥` kapısı KIRMIZI yanar.
FONT, FONT_B, FONT_I = "Body", "Body-Bold", "Body-Italic"


def register_fonts(rep):
    """Gömülebilir TTF'leri kaydeder. (başarılı_mı, kaynak_dizin) döner."""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    for d in [FONT_DIR] + SYS_FONT_DIRS:
        if all(os.path.isfile(os.path.join(d, f)) for f in FONT_FILES.values()):
            try:
                for name, fn in FONT_FILES.items():
                    pdfmetrics.registerFont(TTFont(name, os.path.join(d, fn)))
                # ⚠ MUTLAK YOL RAPORA YAZILMAZ.
                # `06_REPORTS/interior.json` TAKİP EDİLEN bir dosyadır ve
                # ilk hâl oraya `/home/<kullanıcı>/…` yazıyordu. Bir build
                # makinesinin dizin ağacı public depoda durmaz — ön uçuş
                # denetimi bunu sızıntı olarak yakaladı.
                rep.facts["fontDir"] = (os.path.relpath(d, ROOT)
                                        if d.startswith(ROOT) else d)
                rep.facts["fontsEmbedded"] = True
                # CJK yedeği — bulunamazsa dizgi yine koşar ama
                # `§ ⑥` bunu SÖYLER; sessizce tofu basılmaz.
                rep.facts["cjkFont"] = None
                for cp, idx in CJK_CANDIDATES:
                    if os.path.isfile(cp):
                        try:
                            ft = (TTFont(FONT_CJK, cp) if idx is None
                                  else TTFont(FONT_CJK, cp, subfontIndex=idx))
                            pdfmetrics.registerFont(ft)
                            rep.facts["cjkFont"] = os.path.basename(cp)
                            CMAPS[FONT_CJK] = set(ft.face.charToGlyph)
                            break
                        except Exception:                      # noqa: BLE001
                            continue
                for nm, fn in FONT_FILES.items():
                    try:
                        CMAPS[nm] = set(
                            TTFont(nm + "-probe",
                                   os.path.join(d, fn)).face.charToGlyph)
                    except Exception:                          # noqa: BLE001
                        pass
                return True, d
            except Exception as exc:                       # noqa: BLE001
                rep.facts["fontError"] = str(exc)
    rep.facts["fontsEmbedded"] = False
    return False, None


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

    # ⭑ YAZI TİPİ KAYDI ÖLÇÜMDEN ÖNCE GELİR ⭑
    # `stringWidth` kayıtlı yazı tipinin metriklerini kullanır: kayıt
    # yapılmadan ölçülen bir sayfa sayısı BAŞKA bir yazı tipinin sayfa
    # sayısıdır. Kayıt burada, ilk `text_block` çağrısından önce.
    ok, fdir = register_fonts(rep)
    if ok:
        # ⚠ TUVALİN VARSAYILAN YAZI TİPİ DE DEĞİŞTİRİLMELİDİR.
        #
        # Bütün `setFont` çağrıları DejaVu'ya çevrildikten sonra bile
        # `pdffonts` çıktısında gömülmemiş bir `Helvetica` kalmıştı:
        # reportlab tuvali `rl_config.canvas_basefontname` ile açar ve o
        # ad sayfa kaynak sözlüğüne HİÇ KULLANILMASA DA yazılır.
        #
        #     Kullanılmayan ama BEYAN EDİLEN bir yazı tipi de
        #     gömülmemiş bir yazı tipidir — ve denetim onu görür.
        from reportlab import rl_config
        rl_config.canvas_basefontname = FONT
    if not ok:
        rep.warn("gömülebilir yazı tipi BULUNAMADI — base-14'e düşülüyor; "
                 "iç blok KDP'ye HAZIR DEĞİL (§ ⑥ kırmızı yanacak)")
        globals()["FONT"] = "Helvetica"
        globals()["FONT_B"] = "Helvetica-Bold"
        globals()["FONT_I"] = "Helvetica-Oblique"

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
    state = {"page": 0, "overflow": [], "thin": [], "unsafe": [],
             "droppedGlyphs": 0}
    # Her yerleştirmenin ETKİN çözünürlüğü — beyan değil ÖLÇÜM.
    art_dpi = []

    def inner(page_no):
        """Tek sayfada iç kenar SAĞDA mı SOLDA mı — gutter tarafı değişir."""
        return GUTTER if page_no % 2 == 1 else OUTER

    def new_page():
        state["page"] += 1
        if c and state["page"] > 1:
            c.showPage()
        return state["page"]

    def text_block(x, y, w, txt, size, leading, font=FONT):
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

    def wrap_lines(txt, font, size, w):
        """Salt sarma — çizmez, satır listesi döner."""
        words, line, out = (txt or "").split(), "", []
        for word in words:
            t = (line + " " + word).strip()
            if pdfmetrics.stringWidth(t, font, size) <= w:
                line = t
            else:
                out.append(line)
                line = word
        if line:
            out.append(line)
        return out

    def measure_block(w, txt, size, leading, font=FONT):
        """`text_block`'un ÇİZMEYEN ikizi — yalnızca yükseklik döner.

        Levha kutusunu büyütebilmek için altında ne kadar yer
        gerektiğini ÖNCEDEN bilmek gerekiyor. Tahmin edilmez: aynı
        sarma mantığıyla ölçülür."""
        if not txt:
            return 0
        words, line, n = txt.split(), "", 0
        for word in words:
            t = (line + " " + word).strip()
            if pdfmetrics.stringWidth(t, font, size) <= w:
                line = t
            else:
                n += 1
                line = word
        if line:
            n += 1
        return n * leading

    def asset_box(x, y, w, h, aid, label):
        """Görsel yerleşimi. final/ varsa GERÇEK varlık, yoksa YER TUTUCU.

        ⭑ ÖLÇEK YUKARI ÇEKMEK ÇÖZÜNÜRLÜK ÜRETMEZ ⭑

        İlk hâl her görseli kutusuna DOLDURUYORDU. Kutu, varlığın
        şartnamedeki fiziksel boyundan büyük olduğunda görsel yukarı
        ölçekleniyor ve etkin çözünürlük düşüyordu. `pdfimages -list`
        ölçtü: 158 görselin 72'si **122–149 ppi** basılıyordu.

            825 × 1050 px  →  şartname 5,50 × 7,00 in @150 dpi
                              basılan  6,20 × 7,89 in @133 dpi

        Aynı anda `PROOF_HANDOFF.md` şunu yazıyordu: "158 iç blok
        görselinin HEPSİ 150 dpi etkin çözünürlükte". Ölçüm bunu
        yalanladı — beyan ile gerçeğin ayrışması bu projede birinci
        sınıf kusurdur (K41).

            Bir görselin fiziksel boyu şartnamede YAZILIDIR.
            Dizgi onu icat edemez.

        Bu yüzden ölçek `72/ART_DPI_FLOOR` ile sınırlanır: görsel
        kutusundan küçük kalabilir ama şartnamedeki boyunu AŞAMAZ.
        Kutu yine aynı yeri ayırır; görsel ortalanır."""
        a = assets.get(aid)
        fp = os.path.join(FINAL_DIR, a["filename"]) if a else None
        if c:
            if fp and os.path.isfile(fp):
                ir = ImageReader(fp)
                pw, phx = ir.getSize()
                s_fit = min(w / float(pw), h / float(phx))
                s_max = 72.0 / ART_DPI_FLOOR          # 1 px = 0,48 pt
                s_use = min(s_fit, s_max)
                dw, dh = pw * s_use, phx * s_use
                art_dpi.append((aid, round(72.0 / s_use, 1)))
                c.drawImage(ir, x + (w - dw) / 2.0, y - h + (h - dh) / 2.0,
                            width=dw, height=dh, mask="auto")
            else:
                c.setDash(3, 3)
                c.rect(x, y - h, w, h)
                c.setDash()
                c.setFont(FONT_I, 7)
                c.drawCentredString(x + w / 2, y - h / 2, label[:70])
        return h

    def para_block(x, y, w, txt, size, leading, font=FONT, gap=0.55):
        """Paragrafları ve satır sonlarını KORUYARAK dizer.

        ⭑ İLK HÂL `\\n\\n`'i İKİ BOŞLUKLA DEĞİŞTİRİYORDU ⭑

        Sonuç kitabın BİRİNCİ SAYFASINDA görüldü: başlık, alt başlık ve
        yayınevi tek bir gövde paragrafına eriyordu —

            THE MYTH HUNTER'S FIELD BOOK A Screen-Free Quest Through
            22 Cultures 120 Puzzles, Maps, Codes and Challenges for
            Ages 8-12 <imprint>      ← üçü tek paragrafa erimiş

        Kaynak DOĞRUYDU: manuscript satır yapısını `\\n\\n` ile taşıyor.
        Onu düzleştiren dizgiydi.

            Bir kaynağın taşıdığı yapıyı silen dizgi,
            kaynağı düzeltmekle onarılamaz.
        """
        total = 0.0
        for para in (txt or "").split("\n\n"):
            for line in para.split("\n"):
                used = text_block(x, y - total, w, line.strip(), size, leading,
                                  font)
                total += used or leading
            total += leading * gap
        return total

    def measure_para(x_w, txt, size, leading, font=FONT, gap=0.55):
        """`para_block`'un ÇİZMEYEN ikizi — bir paragrafın yüksekliği.

        Ön maddeyi akıtabilmek için bir paragrafın sayfaya SIĞIP
        sığmadığını çizmeden bilmek gerekir."""
        total = 0
        for para in (txt or "").split("\n\n"):
            for line in para.split("\n"):
                total += measure_block(x_w, line.strip(), size, leading,
                                       font) or leading
            total += leading * gap
        return total

    # ── ÖN MADDE ───────────────────────────────────────────────────────────
    #
    # ⚠ `heading` BİR İÇ KİMLİKTİR, HER SAYFADA BASILAMAZ.
    # İlk hâl onu koşulsuz basıyordu ve kapak içi sayfada okur
    # **"Title Page"** başlığını görüyordu. Künye sayfası ve başlık
    # sayfası kendi tipografilerini ister.
    SILENT_HEADINGS = {"title-page"}

    def front_section(s):
        """Bir ön madde bölümünü AKITIR — TEKRAR ETMEZ.

        ⭑ İLK HÂL BÖLÜMÜ `pages` KADAR TEKRAR BASIYORDU ⭑

            for _ in range(s.get("pages", 1)):     # ← kusur

        `pages` bir SAYFA BÜTÇESİDİR: "bu bölüm iki sayfa tutar".
        Döngü onu bir TEKRAR SAYISI gibi okudu ve `how-a-page-works`
        bölümünün 1593 karakterlik gövdesi ile levhası **sayfa 4 ve
        sayfa 5'e birebir aynı** basıldı. `pdftotext` ölçtü: iki
        sayfanın metni 1601 karakter ve özdeş.

            Bir bütçe, bir tekrar sayısı değildir.
            "İki sayfa tutar" ile "iki kez basılır" aynı cümle değildir.

        Bu, Faz 6'nın arka bölümde 7 sayfayı iki kez basmasıyla AYNI
        sınıftır ve `flow()` orada zaten doğru çözümü taşıyordu —
        ön madde onu kullanmıyordu.

        Levha yalnızca SON metin sayfasına konur; oraya sığmazsa
        kendi sayfasına geçer. Boş sayfa üretmez."""
        paras = [pp for pp in (s.get("bodyText") or "").split("\n\n")
                 if pp.strip()]
        used, first, i = 0, True, 0
        fig_h = 150
        while True:
            p = new_page()
            used += 1
            x, w, y = inner(p), TRIM_W - GUTTER - OUTER, TRIM_H - TOP
            if c and s["id"] not in SILENT_HEADINGS:
                c.setFont(FONT_B, 15)
                c.drawString(x, y, s.get("heading", "")
                             + ("" if first else " (continued)"))
            y -= 26
            first = False
            while i < len(paras):
                need = measure_para(w, paras[i], 10.5, 14.5)
                if y - need < BOTTOM and y < TRIM_H - TOP - 26:
                    break
                y -= para_block(x, y, w, paras[i], 10.5, 14.5)
                i += 1
            if i < len(paras):
                continue
            if s.get("visualNeed"):
                if y - fig_h - 20 < BOTTOM:
                    p = new_page()
                    used += 1
                    x, w, y = inner(p), TRIM_W - GUTTER - OUTER, TRIM_H - TOP
                    if c:
                        c.setFont(FONT_B, 15)
                        c.drawString(x, y, s.get("heading", "") + " (continued)")
                    y -= 26
                y -= asset_box(x, y - 8, w, fig_h, "front-%s" % s["id"],
                               "[ %s ]" % s["id"]) + 12
            if y < BOTTOM:
                state["overflow"].append("front:%s" % s["id"])
            state.setdefault("frontPages", {})[s["id"]] = used
            return used

    def title_page(s):
        """⭑ BAŞLIK SAYFASI — kitabın ilk izlenimi ⭑

        Satırlar manuscript'ten gelir; hiyerarşi burada kurulur. Bu
        sayfa akıtılmaz: tek sayfadır ve kendi tipografisini ister."""
        p = new_page()
        x, w = inner(p), TRIM_W - GUTTER - OUTER
        parts = [ln.strip() for ln in (s.get("bodyText") or "").split("\n")
                 if ln.strip()]
        title = parts[0] if parts else book.get("meta", {}).get("title", "")
        subs = parts[1:-1] if len(parts) > 2 else []
        imprint = parts[-1] if len(parts) > 1 else ""
        yy = TRIM_H * 0.70
        for ln in wrap_lines(title, FONT_B, 26, w):
            if c:
                c.setFont(FONT_B, 26)
                c.drawCentredString(x + w / 2, yy, ln)
            yy -= 32
        yy -= 14
        for sline in subs:
            for ln in wrap_lines(sline, FONT_I, 12.5, w * 0.86):
                if c:
                    c.setFont(FONT_I, 12.5)
                    c.drawCentredString(x + w / 2, yy, ln)
                yy -= 17
            yy -= 4
        if c and imprint:
            c.setFont(FONT, 11)
            c.drawCentredString(x + w / 2, BOTTOM + 46, imprint)
        state.setdefault("frontPages", {})[s["id"]] = 1

    for s in (book.get("frontMatter") or {}).get("sections", []):
        if s["id"] in SILENT_HEADINGS:
            title_page(s)
        else:
            front_section(s)

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
            c.setFont(FONT_B, 19)
            c.drawString(x, y, op.get("heading", rname.get(rid, rid)))
            c.setFont(FONT_I, 10)
            c.drawString(x, y - 20, (op.get("terrainLine") or "")[:110])
        if op:
            text_block(x, y - 46, w, op.get("openingText", ""), 10.5, 15)

        # aktivite sayfaları
        for a in pool:
            p = new_page()
            x, w = inner(p), TRIM_W - GUTTER - OUTER
            y = TRIM_H - TOP
            # ① görev satırı  ② zorluk
            #
            # ⭑ GÖREV SATIRI SARILMIYORDU — VE TAŞIYORDU ⭑
            #
            # `drawString` sarma yapmaz: sütundan uzun bir görev satırı
            # sağ kenardan TAŞAR. KDP Previewer bunu sayfa 47'de
            # "This text is outside the margins" olarak bildirdi.
            #
            # Ölçüm: `egyptian-nile-map`'in görev satırı 7,918 inç ve
            # sütun 7,626 inçti — 0,29 inç dışarı taşıyordu. Ölçülen dış
            # kenar 0,2200 in (asgari 0,2500).
            #
            #     Sarılmayan bir satır, uzun bir cümle yazıldığı gün
            #     sayfanın dışına çıkar.
            #
            # Ve yıldızlar sağa dayalı basıldığı için satırın onlara
            # ÇARPMAMASI da gerekir: sütun genişliğinden yıldız payı
            # düşülür.
            d = design.get(a["activityId"], {}).get("difficulty", 1)
            stars = "★" * int(d or 1)
            star_w = pdfmetrics.stringWidth(stars, FONT, 12) + 10
            plines = wrap_lines(a.get("prompt", ""), FONT_B, 12, w - star_w)
            if c:
                c.setFont(FONT_B, 12)
                for i, ln in enumerate(plines):
                    c.drawString(x, y - i * 15, ln)
                c.setFont(FONT, 12)
                c.drawRightString(x + w, y, stars)
            y -= 22 + max(0, len(plines) - 1) * 15
            # ③ levha — visualSpec ölçüsünde
            #
            # ⭑ MOBİLYA ROLÜ LEVHANIN BOYUNU DA DEĞİŞTİRİR ⭑
            #
            # Mobilya çiftlemesi giderildiğinde (dizgi artık levhanın
            # bastığını basmıyor) sayfanın alt yarısı BOŞ kaldı — 75
            # sayfada dört inçe yakın ölü alan. Boş alan yalnızca çirkin
            # değil: o sayfalarda ÇOCUĞUN YAZDIĞI SATIRLAR levhanın
            # içindedir ve levha küçük kalırsa satırlar da küçük kalır.
            #
            #     Ölü alan, küçültülmüş bir yazma alanıdır.
            #
            # Bu yüzden levha, altında GERÇEKTEN gereken yer ölçüldükten
            # sonra kalan yüksekliği alır. Tavan hâlâ vardır (sayfanın
            # %72'si): levha sayfayı tamamen yutmamalı.
            vs = a.get("visualSpec") or {}
            tpx = vs.get("targetPx") or [1650, 1200]
            box_w = w
            furn_pre = a.get("furniture") or {}
            # ⚠ REZERV HESABI İLK YAZILDIĞINDA YANLIŞTI VE KAPI YAKALADI.
            #
            # İlk hâl field note'u ayrıca ölçüp yazma bloğunun payına da
            # ekliyordu; oysa yazma bloğu kendi içinde field note ve
            # ebeveyn notu için 58 pt'lik SABİT bir pay zaten düşüyor.
            # Sonuç: levha 25 sayfada yazma satırlarının yerini yedi ve
            # satır yüksekliği 7 mm ölçütünün altına indi.
            #
            #     Kapı, levhayı büyütme hevesini 25 sayfada durdurdu —
            #     ve durdurduğu şey ÇOCUĞUN YAZMA ALANIYDI.
            #
            # Doğrusu: dizgi yazma satırı çiziyorsa rezerv
            # `satır × 7 mm + 58`; çizmiyorsa field note ayrıca ölçülür.
            need = 0.0
            for i, st in enumerate(a.get("steps") or [], 1):
                need += measure_block(w - 90, "%d. %s" % (i, st), 10, 13.5)
            if a.get("sealSlot") and furn_pre.get("starBox", "typeset") != "plate":
                need += 26
            typeset_lines = (0 if furn_pre.get("writingLines") == "plate"
                             else (a.get("writingSpaceLines") or 0))
            if typeset_lines:
                need += typeset_lines * WRITING_LINE + 58
            else:
                need += measure_block(w, "Field note: " + (a.get("fieldNote") or ""),
                                      9, 12)
                if a.get("parentNote"):
                    need += measure_block(w, a["parentNote"], 8, 11) + 8
            avail = (y - BOTTOM) - need - 22        # 22 pt nefes payı
            box_h = min(box_w * (tpx[1] / tpx[0]), max(avail, TRIM_H * 0.30),
                        TRIM_H * 0.72)
            y -= asset_box(x, y, box_w, box_h, vs.get("assetId", ""),
                           "[ %s ]" % vs.get("assetId", "?")) + 14
            # ④ adımlar
            if c:
                c.setFont(FONT, 10)
            for i, st in enumerate(a.get("steps") or [], 1):
                y -= text_block(x, y, w - 90, "%d. %s" % (i, st), 10, 13.5)
            y -= 6
            # ⭑ MOBİLYA BEYAN EDİLMİŞ ROLE GÖRE ÇİZİLİR ⭑
            #
            # `pagePrints` iki muhataba yazılmış tek bir listeydi ve
            # ayrım yazılı değildi: levha da mobilyayı çizdi, dizgi de.
            # Ölçüldü — yıldızlı kutu 37/37 sayfada, yazma alanı
            # 75/120 sayfada İKİ KEZ basılıyordu.
            #
            #     Levha bir mobilyayı zaten basıyorsa, DİZGİ onu basmaz.
            #
            # Rol prozadan her koşuda yeniden çıkarılmaz; bir kez
            # ölçülüp `furniture` alanına DONDURULMUŞTUR
            # (`04_BUILD/furniture_roles.py`). Beyan yoksa eski davranış
            # sürer — sessiz bir değişiklik yapılmaz.
            furn = a.get("furniture") or {}

            # ⑧ yıldızlı kutu
            if a.get("sealSlot") and furn.get("starBox", "typeset") != "plate":
                n = len(a.get("sealStarWord") or "")
                bw = 15
                if c:
                    for i in range(n):
                        c.rect(x + i * bw, y - 17, bw, 17)
                    c.setFont(FONT, 7.5)
                    c.drawString(x + n * bw + 8, y - 12,
                                 "★%d → seal slot %d" % (a.get("sealStarIndex", 1),
                                                         a["sealSlot"]))
                y -= 26
            # ⑦ yazma alanı — ÖLÇÜLEN KAPI
            lines = (0 if furn.get("writingLines") == "plate"
                     else (a.get("writingSpaceLines") or 0))
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
                c.setFont(FONT_I, 7.5)
                c.drawString(x, BOTTOM + 8, "For an adult: " + a["parentNote"][:120])
            if y - fn_h < BOTTOM:
                state["overflow"].append(a["activityId"])
            # sayfa numarası
            if c:
                c.setFont(FONT, 8)
                c.drawRightString(TRIM_W - inner(p), BOTTOM - 12, str(p))

        # bölge mühür sayfası
        p = new_page()
        x, y = inner(p), TRIM_H - TOP
        if c:
            c.setFont(FONT_B, 15)
            c.drawString(x, y, "%s — Seal" % rname.get(rid, rid))
        slots = sorted({a["sealSlot"] for a in pool if a.get("sealSlot")})
        if c:
            for i, sl in enumerate(slots):
                c.rect(x + i * 34, y - 74, 30, 30)
                c.setFont(FONT, 7.5)
                c.drawCentredString(x + i * 34 + 15, y - 86, "slot %d" % sl)
        asset_box(x, y - 110, 120, 120, "seal-%s" % rid, "[ seal-%s ]" % rid)

    # ═══════════════════════════════════════════════════════════════════════
    # FİNAL GÖREV — ⭑ TALİMAT DEĞİL, APARAT ⭑
    # ═══════════════════════════════════════════════════════════════════════
    #
    # ⭑ KİTABIN SON BEŞ SAYFASI KULLANILAMAZ HÂLDEYDİ ⭑
    #
    # İlk hâl başlığı, görev satırını, adımları ve saha notunu basıyor,
    # sonra duruyordu. Oysa adımlar sayfada BASILI OLMAYAN şeylere işaret
    # ediyordu:
    #
    #     "Write each region's name in its box on the route map."
    #                                    ↑ kutu yok   ↑ harita yok
    #     "Write your name on the certificate line."
    #                              ↑ sertifika yok, çizgi yok
    #
    # Sayfanın ortası boştu. Çocuk kitabın FİNALİNE varıyor ve yapacak
    # bir şey bulamıyordu.
    #
    #     Bir sayfanın ne basacağı `pagePrints`te YAZILIDIR.
    #     Basılmadıysa sayfa bir talimat listesidir, bir sayfa değil.
    #
    # Bu, arka maddede bir kez düzeltilmiş kusurun (§ ARKA MADDE ②) aynısı
    # ve düzeltme final göreve HİÇ UĞRAMAMIŞTI. Aparat artık `pagePrints`
    # ve ÖLÇÜLMÜŞ veriden (bölge sırası, kültür dizini, mühür kaydı)
    # kurulur — elle çizilmez.
    #
    # ⚠ K10: mühür SÖZCÜKLERİ ve notch HARFLERİ cevaptır ve BASILMAZ.
    # Yalnızca `pagePrints`in açıkça istediği notch NUMARASI basılır —
    # o bir veridir, cevap değil: harfi veren şey sözcüktür ve sözcük
    # çocuğun kendi topladığı mühürdedir.
    fq = book.get("finalQuest") or {}
    route = [r for r in sorted(regions, key=lambda z: z.get("order", 99))]
    seal_doc = jload(os.path.join(ROOT, "01_SOURCE", "answers",
                                  "seal_key.json"), {}) or {}
    notch = {sl.get("region"): sl.get("notchPosition")
             for sl in (seal_doc.get("seals") or [])}

    def fq_route(x, y, w):
        """Altı numaralı durak, noktalı yol, ad kutusu ve mühür halkası."""
        top = y
        cols, cw = 3, w / 3.0
        for i, r in enumerate(route[:6]):
            cx = x + (i % cols) * cw + cw / 2.0
            cy = top - (i // cols) * 150
            if c:
                c.circle(cx, cy - 10, 9, stroke=1, fill=0)
                c.setFont(FONT_B, 9)
                c.drawCentredString(cx, cy - 13, str(i + 1))
                c.rect(cx - cw / 2.0 + 12, cy - 52, cw - 24, 22)
                c.circle(cx, cy - 82, 17, stroke=1, fill=0)
                c.setFont(FONT, 6.5)
                c.drawCentredString(cx, cy - 104, "seal %d" % (i + 1))
        if c:                                   # duraklar arası noktalı yol
            c.setDash(2, 3)
            for i in range(5):
                a_c = x + (i % cols) * cw + cw / 2.0
                b_c = x + ((i + 1) % cols) * cw + cw / 2.0
                ay = top - (i // cols) * 150 - 10
                by = top - ((i + 1) // cols) * 150 - 10
                if (i // cols) == ((i + 1) // cols):
                    c.line(a_c + 10, ay, b_c - 10, by)
                else:
                    c.line(a_c, ay - 112, b_c, by + 12)
            c.setDash()
        return 150 * 2 + 6, 6          # altı ad kutusu = altı yazma yeri

    def fq_notch(x, y, w):
        """Altı mühür taslağı · kenarında çentik · numarası · iki kutu."""
        top, cols, cw = y, 3, w / 3.0
        for i, r in enumerate(route[:6]):
            cx = x + (i % cols) * cw + cw / 2.0
            cy = top - (i // cols) * 158
            n = notch.get(r["id"])
            if c:
                c.circle(cx - 22, cy - 26, 22, stroke=1, fill=0)
                c.setLineWidth(2)               # çentik: kenarda tek kesik
                c.line(cx - 22, cy - 4, cx - 22, cy - 12)
                c.setLineWidth(1)
                if n:
                    c.setFont(FONT_B, 10)
                    c.drawString(cx + 6, cy - 30, str(n))
                c.setFont(FONT, 6.5)
                c.drawCentredString(cx, cy - 58, rname.get(r["id"], r["id"])[:22])
                c.rect(cx - cw / 2.0 + 14, cy - 86, (cw - 34) / 2.0, 20)
                c.rect(cx + 2, cy - 86, (cw - 34) / 2.0, 20)
                c.setFont(FONT, 5.8)
                c.drawString(cx - cw / 2.0 + 14, cy - 95, "notch number")
                c.drawString(cx + 2, cy - 95, "letters in the word")
        return 158 * 2 + 4, 12        # altı mühür × iki kutu = on iki yer

    def fq_key_build(x, y, w):
        """Altı büyük boş harf karesi · üstünde bölge · altında numara."""
        sq, gap = 52, (w - 6 * 52) / 5.0
        for i, r in enumerate(route[:6]):
            bx = x + i * (sq + gap)
            if c:
                c.setFont(FONT, 5.6)
                c.drawCentredString(bx + sq / 2.0, y - 8,
                                    rname.get(r["id"], r["id"])[:20])
                c.setLineWidth(1.4)
                c.rect(bx, y - 20 - sq, sq, sq)
                c.setLineWidth(1)
                c.setFont(FONT_B, 9)
                c.drawCentredString(bx + sq / 2.0, y - 34 - sq, str(i + 1))
        if c:                                   # altına uzun yazma çizgisi
            c.line(x, y - 62 - sq, x + w, y - 62 - sq)
            c.rect(x + w / 2.0 - 60, y - 150 - sq, 120, 62)
            c.setFont(FONT, 6.5)
            c.drawCentredString(x + w / 2.0, y - 162 - sq,
                                "the cartographer's seal")
        return 176 + sq, 1            # kareler altındaki uzun çizgi

    def fq_sorting(x, y, w):
        """Yirmi iki kültür × altı motif · her hücrede boş kutu."""
        motifs = ["a writing", "a journey", "the year", "a named", "a counting",
                  "a message"]
        motifs2 = ["system", "by water", "turning", "real place", "system",
                   "that travels"]
        names = []
        for r in route:
            for cu in sorted({design.get(a["activityId"], {}).get("culture")
                              for a in by_region.get(r["id"], [])} - {None}):
                if cu not in names:
                    names.append(cu)
        lab_w, cell = w * 0.30, (w * 0.70) / 6.0
        rh = 14.6
        if c:
            c.setFont(FONT_B, 5.9)
            for j in range(6):
                cx = x + lab_w + j * cell
                c.drawCentredString(cx + cell / 2.0, y - 6, motifs[j])
                c.drawCentredString(cx + cell / 2.0, y - 13, motifs2[j])
        yy = y - 20
        for i, cu in enumerate(names[:22]):
            if c:
                c.setFont(FONT, 7.2)
                c.drawString(x, yy - rh + 4, cu.replace("-", " ").title()[:26])
                for j in range(6):
                    c.rect(x + lab_w + j * cell + cell / 2.0 - 7,
                           yy - rh + 2, 14, 11)
            yy -= rh
        if c:                                   # toplam satırı
            c.setFont(FONT_B, 7.2)
            c.drawString(x, yy - rh + 4, "total")
            for j in range(6):
                c.rect(x + lab_w + j * cell + cell / 2.0 - 13, yy - rh - 2,
                       26, 13)
        return (y - (yy - rh)) + 22, 0

    def fq_certificate(x, y, w):
        """Çerçeveli sertifika · ad · tarih · bölge kutusu · altı halka."""
        h = 214
        if c:
            c.setLineWidth(1.6)
            c.rect(x + 10, y - h, w - 20, h)
            c.setLineWidth(0.6)
            c.rect(x + 16, y - h + 6, w - 32, h - 12)
            c.setLineWidth(1)
            c.setFont(FONT_B, 15)
            c.drawCentredString(x + w / 2.0, y - 34, "FIELD RESEARCHER")
            c.setFont(FONT, 8)
            c.drawString(x + 40, y - 76, "name")
            c.line(x + 76, y - 78, x + w - 190, y - 78)
            c.drawString(x + 40, y - 106, "date")
            c.line(x + 76, y - 108, x + w - 190, y - 108)
            c.drawCentredString(x + w - 79, y - 62, "regions completed")
            c.rect(x + w - 110, y - 118, 62, 44)
            for i in range(6):                  # alt kenarda altı halka
                c.circle(x + w / 2.0 - 100 + i * 40, y - h + 34, 13,
                         stroke=1, fill=0)
        return h + 8, 3               # ad çizgisi · tarih çizgisi · kutu

    FQ_APPARATUS = {"map-trace": fq_route, "data-table": None,
                    "key-build": fq_key_build, "make-frame": fq_certificate}
    FQ_BY_ID = {"The Notch": fq_notch, "The Great Sorting Table": fq_sorting}

    for q in fq.get("quest", []):
        p = new_page()
        x, w, y = inner(p), TRIM_W - GUTTER - OUTER, TRIM_H - TOP
        if c:
            c.setFont(FONT_B, 14)
            c.drawString(x, y, q.get("heading", ""))
            c.setFont(FONT, 11)
        y -= 24
        y -= text_block(x, y, w, q.get("prompt", ""), 11, 14) + 6
        for i, st in enumerate(q.get("steps") or [], 1):
            y -= text_block(x, y, w, "%d. %s" % (i, st), 10, 13.5)
        y -= 10

        draw = FQ_BY_ID.get(q.get("heading")) or FQ_APPARATUS.get(q.get("layout"))
        provided = 0
        if draw:
            used_h, provided = draw(x, y, w)
            y -= used_h
        else:
            state["overflow"].append("finalQuest:%s" % q.get("heading"))

        # `pagePrints`in şerit/altlık satırları — sayfanın kendi sözü
        strips = [t for t in (q.get("pagePrints") or [])
                  if re.match(r"^(a caption strip|a footer|a rule strip|"
                              r"a self-check strip|a closing line|"
                              r"a worked example)", t)]
        for t in strips:
            body = t.split(":", 1)[1].strip() if ":" in t else t
            if y - 24 < BOTTOM + 46:
                break
            y -= text_block(x, y, w, body[:1].upper() + body[1:], 8, 11) + 3

        # ⭑ APARAT YAZMA YERİNİ ZATEN TAŞIYORSA ÇİZGİ TEKRARLANMAZ ⭑
        #
        # `The Notch` on iki satır BEYAN ediyor ve aparatı zaten on iki
        # kutu basıyor. İkisi birden basılınca satır başına 6,8 mm
        # kalıyordu ve çocuk eli kapısı (≥7 mm) KIRMIZI yandı — doğru
        # yandı: sayfa aynı yazma yerini iki kez istiyordu.
        #
        #     Bir kutu da bir yazma yeridir.
        #     Mobilya iki kez basılmaz (K45).
        lines = max(0, (q.get("writingSpaceLines") or 0) - provided)
        if lines:
            # ⚠ Aktivite sayfası çizgileri kalan boşluğa YAYAR; final görev
            # sayfasında kalan boşluk büyük olduğu için aynı davranış
            # çizgileri sayfaya dağıtıyor ve kazara çizilmiş gibi
            # gösteriyordu. Burada adım SABİTTİR ve aparatın hemen altına
            # oturur.
            avail = y - (BOTTOM + 46)
            per = max(WRITING_LINE, 9.0 * MM)
            if avail < lines * WRITING_LINE:
                state["thin"].append("finalQuest:%s (%.1f mm × %d satır)"
                                     % (q.get("heading"),
                                        (avail / lines) / MM, lines))
            if c:
                for i in range(lines):
                    yy = y - (i + 1) * per
                    if yy > BOTTOM + 46:
                        c.line(x, yy, x + w, yy)
            y -= min(avail, lines * per)

        text_block(x, BOTTOM + 40, w, "Field note: " + (q.get("fieldNote") or ""),
                   9, 12)
        if c:
            c.setFont(FONT, 8)
            c.drawRightString(TRIM_W - inner(p), BOTTOM - 12, str(p))
        if y < BOTTOM:
            state["overflow"].append("finalQuest:%s" % q.get("heading"))

    # ── ARKA MADDE ─────────────────────────────────────────────────────────
    # ═══════════════════════════════════════════════════════════════════════
    # ARKA MADDE — ⭑ ŞARTNAME DEĞİL, İÇERİK ⭑
    # ═══════════════════════════════════════════════════════════════════════
    #
    # İlk hâl iki ayrı kusuru birden taşıyordu ve ikisi de basılı sayfada
    # görülüyordu:
    #
    #  ① AYNI SAYFA N KEZ BASILIYORDU. `pages: 4` bir SAYFA BÜTÇESİDİR
    #     ("bu bölüm dört sayfa tutar"), bir TEKRAR TALİMATI değil. Döngü
    #     onu tekrar sanıyordu: sözlük dört özdeş sayfa, cevap anahtarı
    #     dört özdeş sayfa. On üç arka madde sayfasının yedisi BİREBİR
    #     kopyaydı.
    #
    #  ② BASILAN ŞEY İÇERİK DEĞİL ŞARTNAMEYDİ. `prints` alanı sayfanın NE
    #     BASACAĞINI tarif eder — *"twenty-two entries, one per culture,
    #     in route order"*. Bu bir sözlük değil, bir sözlüğün TARİFİDİR.
    #     Gerçek yirmi iki girdi, gerçek yüz yirmi cevap ve gerçek kurum
    #     listesi hiç dizilmemişti.
    #
    #     Arka kapak *"the back of the book says which ones"* diye söz
    #     veriyor ve kitabın arkası hangileri olduğunu SÖYLEMİYORDU.
    #
    # Veri zaten ÖLÇÜLMÜŞ hâlde duruyor: `culture_index` yirmi iki kültür,
    # `answers/answer_key.json` yüz yirmi cevap, `research/*-revalidation`
    # kurumlar. Arka madde artık ONLARDAN TÜRETİLİR ve sayfalara AKAR.
    def flow(section, rows, size=9.2, leading=12.4, head_size=14):
        """Satırları gerektiği kadar sayfaya AKITIR — tekrar etmez."""
        pages_used = 0
        i = 0
        first = True
        while i < len(rows) or first:
            p = new_page()
            pages_used += 1
            x, w, y = inner(p), TRIM_W - GUTTER - OUTER, TRIM_H - TOP
            if c:
                c.setFont(FONT_B, head_size)
                c.drawString(x, y, section.get("heading", "")
                             + ("" if first else " (continued)"))
            y -= 22
            first = False
            while i < len(rows):
                kind, text = rows[i]
                f = FONT_B if kind == "b" else (FONT_I if kind == "i" else FONT)
                if has_cjk(text) and rep.facts.get("cjkFont"):
                    f = FONT_CJK
                text, drop = renderable(text, [f])
                if drop:
                    state["droppedGlyphs"] = state.get("droppedGlyphs", 0) + drop
                sz = size + (0.8 if kind == "b" else 0)
                need = measure_block(w, text, sz, leading, f) or leading
                if y - need < BOTTOM:
                    break
                y -= text_block(x, y, w, text, sz, leading, f)
                if kind == "b":
                    y -= 2
                if kind == "p":                 # düzyazı paragrafı: nefes payı
                    y -= leading * 0.55
                i += 1
            if i >= len(rows):
                break
        return pages_used

    cultures_doc = jload(os.path.join(ROOT, "01_SOURCE", "culture_index.json"), {})
    akey = jload(os.path.join(ROOT, "01_SOURCE", "answers", "answer_key.json"), {})
    rorder2 = {r["id"]: r.get("order", 99) for r in regions}

    def glossary_rows():
        """⚠ `culture_index.writingSystem` TÜRKÇEDİR VE BASILAMAZ.

        İlk hâl onu doğrudan bastı ve sözlüğün yarısı Türkçe çıktı —
        *"Fince ünlü uyumu ve bileşik sözcük yapısı"* — İngilizce bir
        kitabın arkasında. `qa_language` ticari dili İngilizce olarak
        kilitliyor (K21) ve Türkçe bir sayfa nihai çıktıya KARIŞAMAZ.
        Alanın İngilizce karşılığı YOKTUR; uydurulmaz.

            Bir alanın çevirisi yoksa, o alan basılmaz —
            yerine ÖLÇÜLEBİLEN bir şey basılır.

        Sözlük bu yüzden yalnızca İngilizce ve ölçülmüş veriden kurulur:
        ad · bölge · kitapta kaç sayfa · yaşayan gelenek mi."""
        per = {}
        for a in acts:
            cu = design.get(a["activityId"], {}).get("culture")
            per[cu] = per.get(cu, 0) + 1
        cs = sorted(cultures_doc.get("cultures", []),
                    key=lambda x: (rorder2.get(x.get("region"), 99), x["name"]))
        rows = [("i", "Twenty-two peoples, in the order the route meets them. "
                      "The marks over and under the letters are part of the "
                      "names and are printed as they are written.")]
        last = None
        for cu in cs:
            if cu.get("region") != last:
                last = cu.get("region")
                rows.append(("b", rname.get(last, last)))
            n = per.get(cu["id"], 0)
            rows.append(("n", "%s — %d page%s in this book. %s" % (
                cu["name"], n, "" if n == 1 else "s",
                "Still spoken or practised today."
                if cu.get("livingTradition") else
                "Known from written and excavated record.")))
        return rows

    def answer_rows():
        rows = [("i", "One entry per activity page, in page order. Draw-and-write "
                      "pages give what a finished page must show, not a single "
                      "right answer. The six seal words are not printed here: "
                      "they check themselves, and printing them would remove "
                      "the only self-check in the book. Korean place names "
                      "are given in their romanised form here; the hangul "
                      "itself is printed on the activity page.")]
        for e in sorted(akey.get("entries", []), key=lambda x: x.get("pageOrder", 0)):
            body = (e.get("answer") if not e.get("openEnded")
                    else "a finished page shows: " + (e.get("whatAFinishedPageShows") or ""))
            rows.append(("n", "%d.  %s" % (e.get("pageOrder", 0), body)))
        return rows

    def source_rows():
        import glob as _glob
        import re as _re
        rows = [("i", "Every answer in this book was checked against at least "
                      "two independent published sources. Three claims could "
                      "not be checked twice; those pages were redesigned. If "
                      "you find a mistake, the record of where the fact came "
                      "from is printed here so you can prove it.")]
        for f in sorted(_glob.glob(os.path.join(ROOT, "01_SOURCE", "research",
                                                "*-revalidation.json"))):
            rid = os.path.basename(f).replace("-revalidation.json", "")
            doc = jload(f, {})
            names = set()

            def walk(o):
                if isinstance(o, dict):
                    if isinstance(o.get("ref"), str):
                        names.add(_re.split(r"\s+[—–-]\s+|\s*\(", o["ref"])[0].strip())
                    for v in o.values():
                        walk(v)
                elif isinstance(o, list):
                    for v in o:
                        walk(v)
            walk(doc)
            good = sorted(n for n in names if 3 < len(n) < 70)
            if not good:
                continue
            rows.append(("b", rname.get(rid, rid)))
            rows.append(("n", " · ".join(good)))
        return rows

    BUILDERS = {"glossary": glossary_rows, "answer-key": answer_rows,
                "sources": source_rows}

    def prose_rows(s):
        """⭑ `prints` BİR ŞARTNAMEDİR VE BASILAMAZ ⭑

        Üç arka madde sayfası (`how-to-use`, `hint-rule`,
        `world-myths-bridge`) hiçbir üreticiye bağlı değildi ve yedek
        yol `prints` alanını madde madde BASIYORDU:

            · a short opening line: this book is written to be worked
              alone, and a child who is stuck has met a page, not a limit

        Bu bir sayfa değil, bir sayfanın TARİFİDİR — ve basılı kitapta
        okurun gördüğü şey buydu. § ARKA MADDE ② bu kusuru bir kez
        kapatmıştı ama yalnızca veriden türeyen üç bölüm için; düzyazı
        bölümleri yedek yolda kalmıştı.

            Bir kusur sınıfı kapatılırken örneği değil SINIFI kapatılır.

        Metin artık `bodyText`ten gelir. `bodyText` yoksa sayfa
        ŞARTNAME basmaz — taşma olarak bildirilir ve kapı KIRMIZI yanar."""
        txt = s.get("bodyText")
        if not txt:
            state["overflow"].append("backMatter:%s (bodyText yok)" % s["id"])
            return []
        rows = []
        for para in txt.split("\n\n"):
            para = para.strip()
            if para:
                rows.append(("p", para))
        return rows

    for s in (book.get("backMatter") or {}).get("sections", []):
        build_rows = BUILDERS.get(s["id"])
        rows = build_rows() if build_rows else prose_rows(s)
        used = flow(s, rows)
        state.setdefault("backMatterPages", {})[s["id"]] = used

    # ── FORMA HİZASI ───────────────────────────────────────────────────────
    # ⭑ FORMA DOLGUSU BOŞ SAYFA DEĞİL, KULLANILABİLİR SAYFA OLMALI ⭑
    #
    # Ciltsiz baskı sayfa sayısını dörde tamamlar. İlk hâl bunu GERÇEKTEN
    # BOŞ sayfalarla yapıyordu ve ön uçuş denetimi sayfa 156'yı "kaza
    # eseri boş sayfa" olarak yakaladı — haklı olarak: bir okur boş bir
    # sayfayı bir BASIM HATASI sanar.
    #
    #     Üzerine yazılan bir kitapta boş bir sayfa israftır:
    #     çocuğun zaten yazacak yere ihtiyacı var.
    #
    # Dolgu sayfaları artık cetvelli birer NOT sayfasıdır.
    raw_pages = state["page"]
    padded = raw_pages + (-raw_pages) % 4
    for _ in range(padded - raw_pages):
        pg = new_page()
        if c:
            xx = inner(pg)
            ww = TRIM_W - GUTTER - OUTER
            c.setFont(FONT_B, 14)
            c.drawString(xx, TRIM_H - TOP, "Field Notes")
            c.setFont(FONT_I, 9.5)
            c.drawString(xx, TRIM_H - TOP - 18,
                         "Anything you worked out on the way, and anything "
                         "you want to look up later.")
            yy = TRIM_H - TOP - 46
            while yy > BOTTOM + WRITING_LINE:
                c.line(xx, yy, xx + ww, yy)
                yy -= WRITING_LINE * 1.35
    state["padPages"] = padded - raw_pages
    if c:
        c.showPage()
        c.save()

    # ⭑ ETKİN ÇÖZÜNÜRLÜK BEYAN EDİLMEZ, ÖLÇÜLÜR ⭑
    # `PROOF_HANDOFF.md` "hepsi 150 dpi" yazıyordu; `pdfimages` 122 ppi
    # ölçtü. Artık sayı buradan gelir ve belgeler onu KOPYALAR.
    dpis = [d for _, d in art_dpi]
    rep.facts.update({
        "typesetPagesRaw": raw_pages,
        "typesetPagesSignatureAligned": padded,
        "overflowPages": state["overflow"],
        "thinWritingLines": state["thin"],
        "artPlacements": len(art_dpi),
        "artDpiFloor": ART_DPI_FLOOR,
        "artDpiMin": round(min(dpis), 1) if dpis else None,
        "artDpiMax": round(max(dpis), 1) if dpis else None,
        "artBelowFloor": sorted({a for a, d in art_dpi
                                 if d < ART_DPI_FLOOR - 0.5}),
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

    # ⭑ İÇ KENAR ↔ SAYFA SAYISI YAKINSAMASI ⭑
    #
    # İç kenar sayfa sayısına, sayfa sayısı dizgiye bağlı. Döngüyü
    # kırmanın yolu tahmin etmek değil, YAKINSAMAK: bir kademeyle diz,
    # gerçek sayfa sayısını ölç, kademe değiştiyse yeniden diz.
    #
    #     Bir sayının kendi sonucuna bağlı olması onu tahmin edilebilir
    #     yapmaz — ölçülebilir yapar.
    #
    # Kademe sınırı 150/151'dir ve kitap oraya yakın olabilir; bu yüzden
    # yakınsama SESSİZ DEĞİL, kayıtlıdır ve yakınsamazsa KIRMIZI yanar.
    global GUTTER
    seed = (jload(CONFIG, {}) or {}).get("scope", {}).get("pageTarget", 156)
    history, pages = [], None
    for attempt in range(4):
        GUTTER = (kdp_gutter_inches(seed) + GUTTER_SAFETY) * 72.0
        pages = build(rep, write=not args.measure_only)
        if pages is None:
            break
        history.append({"attempt": attempt + 1, "assumedPages": seed,
                        "gutterInches": round(GUTTER / 72.0, 4),
                        "measuredPages": pages})
        if kdp_gutter_inches(pages) == kdp_gutter_inches(seed):
            break
        seed = pages
    rep.facts["gutterConvergence"] = history
    rep.facts["gutterInches"] = round(GUTTER / 72.0, 4)
    rep.facts["gutterKdpMinimum"] = kdp_gutter_inches(pages or 156)
    rep.facts["gutterSafetyInches"] = GUTTER_SAFETY
    rep.facts["gutterTierPages"] = pages
    if pages is not None:
        rep.check((kdp_gutter_inches(pages) + GUTTER_SAFETY) * 72.0 == GUTTER,
                  "iç kenar ölçülen sayfa sayısıyla YAKINSADI "
                  "(%d sayfa → %.3f in)" % (pages, GUTTER / 72.0))
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

    # ── ⑥ YAZI TİPİ GÖMÜLÜ MÜ — KDP ZORUNLULUĞU ──────────────────────────
    #
    # Faz 6 bu denetimi hiç yapmadı ve iç blok sıfır gömülü yazı tipiyle
    # "teslime hazır" ilan edildi. Gömülmemiş bir yazı tipi iki şey
    # yapar: basımevi kendi ikamesini kullanır (satır sonları kayar) ve
    # WinAnsi dışındaki her işaret DÜŞER — `M■ori` tam olarak buydu.
    print("\n── ⑥ yazı tipi ──")
    rep.check(bool(rep.facts.get("fontsEmbedded")),
              "bütün yazı tipleri GÖMÜLEBİLİR TTF (%s)"
              % (rep.facts.get("fontDir") or "BULUNAMADI"))

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
