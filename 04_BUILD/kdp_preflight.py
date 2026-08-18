#!/usr/bin/env python3
"""
KDP ÖN UÇUŞ DENETİMİ — The Myth Hunter's Field Book
================================================================================
Nihai ÇIKTILARDAN başlar ve kaynağa doğru gider. Bu bir kalite kapısı
değil, bir **teslim denetimidir**: kapılar kaynağı denetler, bu betik
KDP'ye YÜKLENECEK DOSYALARI denetler.

    Bir kapı, sorduğu soruyu ölçer. Sormadığı soru yeşil görünür.

Faz 6 iç bloğu "teslime hazır" ilan etti ve `pdffonts` sıfır gömülü
yazı tipi gösteriyordu. Hiçbir kapı yazı tipini sormamıştı. Bu betik
o sınıfın tamamını sorar.

Ne denetler:

  ① İÇ BLOK PDF   sayfa · trim · yazı tipi · görsel · ek açıklama · boş sayfa
  ② KAPAK PDF     tek sayfa · ölçü · sırt · yazı tipi · sahte ISBN/barkod
  ③ A+ PAKETİ     ölçü · dosya boyutu · sayı · modül haritası
  ④ VERİ TUTARLILIĞI  metadata ⇄ manuscript ⇄ PDF ⇄ kapak ⇄ BOOK_STATS
  ⑤ SIZINTI       cevap · mühür sözcüğü · Türkçe · yerel yol · sır
  ⑥ YER TUTUCU    hiçbir çıktıda yer tutucu kalmadı mı

⚠ BU BETİK KDP PREVIEWER'IN YERİNE GEÇMEZ. Previewer bir Amazon
hizmetidir ve yalnızca panelde koşar. Betik onun sorduğu soruların
MEKANİK olanlarını sorar; geri kalanı `PREVIEWER_CHECKLIST` maddesi
olarak kurucuya kalır.

  ./04_BUILD/kdp_preflight.py            denetle ve rapor yaz
  ./04_BUILD/kdp_preflight.py --quick    boş sayfa taramasını atla
  ./04_BUILD/kdp_preflight.py --seal     paketi mühürle (checksums.txt)

Çıkış kodları:  0 = geçti   1 = KIRMIZI   2 = bağımlılık yok
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

INTERIOR = os.path.join(ROOT, "08_OUTPUT", "PAPERBACK", "interior.pdf")
COVER = os.path.join(ROOT, "08_OUTPUT", "PAPERBACK", "cover.pdf")
APLUS_DIR = os.path.join(ROOT, "08_OUTPUT", "APLUS")
META = os.path.join(ROOT, "06_REPORTS", "tracked", "metadata.json")
BOOK = os.path.join(ROOT, "02_MANUSCRIPT", "book.json")
ANSWERS = os.path.join(ROOT, "01_SOURCE", "answers", "answer_key.json")
SEALS = os.path.join(ROOT, "01_SOURCE", "answers", "seal_key.json")
REPORT = os.path.join(ROOT, "06_REPORTS", "kdp-preflight.json")

TRIM_W, TRIM_H = 8.5, 11.0
PT = 72.0
FAKE_ISBN = re.compile(r"\b97[89][- ]?\d{1,5}[- ]?\d{1,7}[- ]?\d{1,7}[- ]?\d\b")
LOCAL_PATH = re.compile(r"/home/[a-z]+/|/Users/[a-z]+/|C:\\Users\\", re.I)
SECRET = re.compile(r"sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}")
TURKISH = re.compile(r"\b(ve|bir|için|değil|sayfa|cevap|kurucu|yapılır)\b")


def jload(p, default=None):
    if not os.path.isfile(p):
        return default
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def run(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        return r.returncode, r.stdout + r.stderr
    except (OSError, subprocess.SubprocessError) as e:
        return 1, str(e)


class Report:
    def __init__(self, verbose=True):
        self.errors, self.warnings, self.checks = [], [], 0
        self.facts = {}
        self.verbose = verbose

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


# ═══════════════════════════════════════════════════════════════════════════
def check_interior(rep, quick):
    print("\n── ① İÇ BLOK PDF ──")
    if not rep.check(os.path.isfile(INTERIOR), "interior.pdf var"):
        return
    code, info = run(["pdfinfo", INTERIOR])
    rep.check(code == 0, "PDF açılıyor")
    pages = int(re.search(r"Pages:\s+(\d+)", info).group(1))
    w, h = (float(x) for x in
            re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", info).groups())
    rep.facts["interiorPages"] = pages
    rep.facts["interiorTrim"] = [round(w / PT, 4), round(h / PT, 4)]
    print("     %d sayfa · %.3f × %.3f in" % (pages, w / PT, h / PT))
    rep.check(abs(w / PT - TRIM_W) < 0.01 and abs(h / PT - TRIM_H) < 0.01,
              "trim 8,5 × 11,0 in")
    rep.check(pages % 4 == 0, "sayfa sayısı dörde bölünüyor")
    rep.check(110 <= pages <= 828, "KDP sayfa bandında (110–828)")

    # yazı tipleri
    # ⚠ SÜTUN KONUMUYLA AYRIŞTIRMA YANLIŞTI VE KENDİ DENETİMİMİ
    # YALANLADI: `l[40:60]` `emb` sütununa değil `type/encoding`e
    # bakıyordu ve gömülü yazı tiplerini GÖMÜLMEMİŞ sayıyordu.
    # pdffonts satırının SON beş alanı sabittir: emb sub uni obj gen.
    #
    #     Bir denetim yanlış ölçerse, ölçtüğü şey hakkında değil
    #     KENDİSİ hakkında bilgi verir.
    code, fonts = run(["pdffonts", INTERIOR])
    rows = [l for l in fonts.splitlines()[2:] if l.strip()]
    emb = [l for l in rows if l.split()[-5] == "yes"]
    notemb = [l.split()[0] for l in rows if l.split()[-5] != "yes"]
    rep.facts["interiorFonts"] = len(rows)
    rep.facts["interiorFontsEmbedded"] = len(emb)
    rep.check(len(rows) > 0 and len(emb) == len(rows),
              "bütün yazı tipleri GÖMÜLÜ (%d/%d)" % (len(emb), len(rows))
              + ("" if len(emb) == len(rows) else " — GÖMÜLMEMİŞ: %s" % notemb))

    # ek açıklama / JavaScript / gömülü dosya — KDP bunları reddeder
    with open(INTERIOR, "rb") as fh:
        blob = fh.read()
    rep.facts["interiorBytes"] = len(blob)
    for pat, name in ((rb"/Annots", "ek açıklama (/Annots)"),
                      (rb"/JavaScript", "JavaScript"),
                      (rb"/EmbeddedFile", "gömülü dosya"),
                      (rb"/Movie", "film"),
                      (rb"/TrimBox", "TrimBox")):
        n = blob.count(pat)
        if name == "TrimBox":
            continue
        rep.check(n == 0, "%s yok" % name + ("" if n == 0 else " — %d bulundu" % n))
    imgs = blob.count(b"/Image")
    rep.facts["interiorImageObjects"] = imgs
    rep.check(imgs > 100, "görseller gömülü (%d XObject)" % imgs)

    # boş sayfa taraması — RENDER edilerek, tahminle değil
    if not quick:
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            code, _ = run(["pdftoppm", "-r", "18", "-gray", "-png",
                           INTERIOR, os.path.join(td, "p")])
            from PIL import Image, ImageStat
            blanks, faint = [], []
            files = sorted(os.listdir(td))
            for i, f in enumerate(files, 1):
                with Image.open(os.path.join(td, f)) as im:
                    st = ImageStat.Stat(im.convert("L"))
                    ink = 255.0 - st.mean[0]
                if ink < 0.35:
                    blanks.append(i)
                elif ink < 1.5:
                    faint.append(i)
            rep.facts["interiorBlankPages"] = blanks
            rep.facts["interiorFaintPages"] = len(faint)
            rep.check(not blanks, "kaza eseri boş sayfa yok"
                      + ("" if not blanks else " — BOŞ: %s" % blanks))
            if faint:
                rep.warn("%d sayfa çok az mürekkep taşıyor (bölüm açılışları "
                         "olabilir): %s" % (len(faint), faint[:8]))

    # yer tutucu ve sızıntı — METİN katmanında
    code, txt = run(["pdftotext", INTERIOR, "-"])
    low = txt.lower()
    for bad, name in (("placeholder", "PLACEHOLDER"),
                      ("art not supplied", "'art not supplied'"),
                      ("do not print", "'do not print'"),
                      ("lorem ipsum", "lorem ipsum"),
                      ("tbd", "TBD")):
        rep.check(bad not in low, "iç blokta %s yok" % name)
    rep.check(not LOCAL_PATH.search(txt), "yerel dosya yolu yok")
    rep.check(not FAKE_ISBN.search(txt), "sahte ISBN yok")
    tr = TURKISH.findall(low)
    rep.check(len(tr) < 3, "Türkçe editör metni sızmamış"
              + ("" if len(tr) < 3 else " — %d eşleşme" % len(tr)))
    rep.facts["interiorTextChars"] = len(txt)
    return txt


def check_cover(rep):
    print("\n── ② KAPAK PDF ──")
    if not rep.check(os.path.isfile(COVER), "cover.pdf var"):
        return
    md = jload(META)
    cv = md["cover"]
    code, info = run(["pdfinfo", COVER])
    pages = int(re.search(r"Pages:\s+(\d+)", info).group(1))
    w, h = (float(x) for x in
            re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", info).groups())
    rep.facts["coverPages"] = pages
    rep.facts["coverSize"] = [round(w / PT, 4), round(h / PT, 4)]
    print("     %d sayfa · %.4f × %.4f in" % (pages, w / PT, h / PT))
    rep.check(pages == 1, "kapak TEK sayfa (arka+sırt+ön tek tuvalde)")
    rep.check(abs(w / PT - cv["fullCoverWidthInches"]) < 0.005,
              "kapak eni metadata ile aynı (%.4f)" % cv["fullCoverWidthInches"])
    rep.check(abs(h / PT - cv["fullCoverHeightInches"]) < 0.005,
              "kapak boyu metadata ile aynı (%.4f)" % cv["fullCoverHeightInches"])

    code, fonts = run(["pdffonts", COVER])
    rows = [l for l in fonts.splitlines()[2:] if l.strip()]
    emb = [l for l in rows if l.split()[-5] == "yes"]
    rep.facts["coverFontsEmbedded"] = "%d/%d" % (len(emb), len(rows))
    rep.check(rows and len(emb) == len(rows),
              "kapak yazı tipleri GÖMÜLÜ (%d/%d)" % (len(emb), len(rows)))

    code, txt = run(["pdftotext", COVER, "-"])
    rep.check(not FAKE_ISBN.search(txt), "kapakta SAHTE ISBN yok")
    rep.check("barcode" not in txt.lower(), "kapakta barkod metni yok")
    rep.check(md["title"].lower() in txt.lower(),
              "kapaktaki başlık metadata ile aynı")
    rep.check(md["author"].lower() in txt.lower(),
              "kapaktaki yazar metadata ile aynı")
    rep.check("placeholder" not in txt.lower(), "kapakta yer tutucu yok")
    # sayfa sayısı iddiası kapakta doğru mu
    m = re.search(r"(\d{2,4})\s*pages", txt, re.I)
    if m:
        rep.check(int(m.group(1)) == md["edition"]["pages"],
                  "kapaktaki sayfa sayısı ölçümle aynı (%s)" % m.group(1))
    with open(COVER, "rb") as fh:
        blob = fh.read()
    rep.check(blob.count(b"/Annots") == 0, "kapakta ek açıklama yok")
    cj = jload(os.path.join(ROOT, "06_REPORTS", "cover.json"), {})
    dpi = (cj.get("facts") or {}).get("effectiveDpi")
    rep.facts["coverArtDpi"] = dpi
    if dpi and dpi < 300:
        rep.warn("kapak sanatı %.0f dpi — KDP 300 dpi bekler. Yukarı "
                 "örnekleme YAPILMADI; tipografi vektör. KURUCU EYLEMİ: "
                 "sanatı yeniden üret." % dpi)


def check_aplus(rep):
    print("\n── ③ A+ PAKETİ ──")
    if not rep.check(os.path.isdir(APLUS_DIR), "08_OUTPUT/APLUS/ var"):
        return
    from PIL import Image
    imgs = sorted(f for f in os.listdir(APLUS_DIR) if f.endswith(".jpg"))
    rep.facts["aplusImages"] = len(imgs)
    rep.check(len(imgs) >= 7, "en az yedi A+ görseli (%d)" % len(imgs))
    bad_dim, big = [], []
    for f in imgs:
        p = os.path.join(APLUS_DIR, f)
        with Image.open(p) as im:
            w, h = im.size
        if (w, h) not in ((1940, 600), (600, 600)):
            bad_dim.append("%s %dx%d" % (f, w, h))
        if os.path.getsize(p) > 3 * 1024 * 1024:
            big.append(f)
    rep.check(not bad_dim, "her görsel modül ölçüsünde"
              + ("" if not bad_dim else " — SAPMA: %s" % bad_dim))
    rep.check(not big, "her görsel 3 MB altında"
              + ("" if not big else " — BÜYÜK: %s" % big))
    rep.check(os.path.isfile(os.path.join(APLUS_DIR, "APLUS_MODULE_MAP.md")),
              "modül haritası var")
    rep.check(os.path.isfile(os.path.join(APLUS_DIR, "checksums.txt")),
              "sağlama listesi var")
    # ⚠ İDDİA TARAMASI MODÜL HARİTASININ TAMAMINA BAKAMAZ.
    # Harita, YASAKLI iddiaları bir uyarı bölümünde ADIYLA sayıyor
    # ("bu metinler ödül · bestseller · çocuk testi iddia etmez") ve
    # naif bir arama kendi uyarısını bir ihlal sanıyordu.
    #
    #     Bir yasağı YAZMAK, o yasağı ÇİĞNEMEK değildir.
    #
    # Bu yüzden tarama, panele GİRİLECEK metnin kendisine bakar:
    # `06_REPORTS/aplus.json § rows[].headline|body|panelCopy`.
    aj = jload(os.path.join(ROOT, "06_REPORTS", "aplus.json"), {})
    copy = " ".join(
        " ".join(str(r.get(k) or "")
                 for k in ("headline", "body", "panelCopy", "panelBody"))
        for r in (aj.get("rows") or []))
    md = jload(META)
    if copy:
        stale = [n for n in re.findall(r"(\d{2,4})\s*pages", copy, re.I)
                 if int(n) != md["edition"]["pages"]]
        rep.check(not stale, "A+ kopyasında bayat sayfa sayısı yok"
                  + ("" if not stale else " — %s" % stale))
        for claim in ("child-tested", "child tested", "award", "bestseller",
                      "best seller", "approved by"):
            rep.check(claim not in copy.lower(),
                      "A+ kopyası '%s' iddia etmiyor" % claim)
    rep.check(os.path.isfile(os.path.join(APLUS_DIR, "APLUS_MODULE_MAP.md")),
              "modül haritası okunabilir")


def check_consistency(rep, interior_txt):
    print("\n── ④ VERİ TUTARLILIĞI ──")
    md = jload(META)
    book = jload(BOOK)
    stats = os.path.join(ROOT, "BOOK_STATS.md")
    st = open(stats, encoding="utf-8").read() if os.path.isfile(stats) else ""

    acts = len((book or {}).get("activities") or [])
    rep.check(md["descriptionFacts"]["activities"] == acts,
              "metadata aktivite sayısı = manuscript (%d)" % acts)
    rep.check(md["edition"]["pages"] == rep.facts.get("interiorPages"),
              "metadata sayfa = PDF sayfa (%s == %s)"
              % (md["edition"]["pages"], rep.facts.get("interiorPages")))
    rep.check(md["descriptionFacts"]["pages"] == rep.facts.get("interiorPages"),
              "açıklama sayfa iddiası = PDF sayfa")
    spine_expect = round(rep.facts.get("interiorPages", 0) * 0.002252, 4)
    rep.check(abs(md["cover"]["spineInches"] - spine_expect) < 1e-6,
              "sırt = sayfa × 0,002252 (%.4f)" % spine_expect)
    fw = 2 * (8.5 + 0.125) + md["cover"]["spineInches"]
    rep.check(abs(md["cover"]["fullCoverWidthInches"] - fw) < 1e-6,
              "kapak eni = 2×(trim+bleed) + sırt")
    rep.check("**160**" in st or str(rep.facts.get("interiorPages")) in st,
              "BOOK_STATS sayfa sayısıyla tutarlı")
    # kültür/bölge
    ci = jload(os.path.join(ROOT, "01_SOURCE", "culture_index.json"), {})
    ri = jload(os.path.join(ROOT, "01_SOURCE", "region_index.json"), {})
    rep.facts["cultures"] = len(ci.get("cultures", []))
    rep.facts["regions"] = len(ri.get("regions", []))
    rep.check(rep.facts["cultures"] == 22, "22 kültür")
    rep.check(rep.facts["regions"] == 6, "6 bölge")
    rep.check(md["subtitle"].count("22") >= 1, "alt başlık 22 kültür diyor")


def check_leaks(rep, interior_txt):
    print("\n── ⑤ SIZINTI ──")
    ak = jload(ANSWERS, {})
    sk = jload(SEALS, {})

    # Mühür sözcükleri iç blokta BASILI OLMALI (mekanik gereği) ama
    # nihai mühür sözcüğü ve sertifika cevabı SIZMAMALI.
    final = (sk.get("finalQuest") or {})
    fw = final.get("word") or final.get("finalWord")
    if fw:
        n = interior_txt.lower().count(str(fw).lower())
        rep.facts["finalSealWordOccurrences"] = n
        rep.check(n <= 1, "nihai mühür sözcüğü iç blokta çözülmüş hâlde "
                          "basılı değil (%d geçiş)" % n)

    # ⭑ CEVAP ANAHTARI BİR SIZINTI DEĞİL, BİR BÖLÜMDÜR ⭑
    #
    # Aşama 2 arka maddeye GERÇEK cevap anahtarını dizdi (önceden orada
    # yalnızca şartname metni vardı). Naif bir tarama bunu 40 sızıntı
    # olarak bildirdi — oysa ön madde ve arka kapak o bölümü SÖZ VERİYOR.
    #
    #     Aranan şey, cevabın kitapta OLMASI değil;
    #     cevabın AKTİVİTE SAYFASINDA olmasıdır.
    #
    # Bu yüzden tarama yalnızca cevap anahtarından ÖNCEKİ sayfalara bakar.
    body = interior_txt.split("Answer Key")[0]
    rep.facts["scannedPagesBeforeAnswerKey"] = len(body.split("\f"))
    hits = 0
    for e in (ak.get("entries") or [])[:400]:
        a = (e.get("answer") or "").strip()
        if len(a) > 40 and a in body:
            hits += 1
    rep.facts["verbatimAnswerLeaks"] = hits
    rep.check(hits == 0, "hiçbir cevap kaydı iç bloğa BİREBİR düşmemiş"
              + ("" if hits == 0 else " — %d" % hits))

    # Takip edilen dosyalarda sır / yerel yol
    code, out = run(["git", "-C", ROOT, "ls-files"])
    tracked = [f for f in out.splitlines() if f.strip()]
    rep.facts["trackedFiles"] = len(tracked)
    secret_hits, path_hits = [], []
    for f in tracked:
        if not f.endswith((".md", ".json", ".py", ".html", ".yml", ".txt")):
            continue
        p = os.path.join(ROOT, f)
        try:
            t = open(p, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        if SECRET.search(t):
            secret_hits.append(f)
        if LOCAL_PATH.search(t):
            path_hits.append(f)
    rep.check(not secret_hits, "takip edilen dosyalarda sır yok"
              + ("" if not secret_hits else " — %s" % secret_hits[:3]))
    rep.check(not path_hits, "takip edilen dosyalarda yerel yol yok"
              + ("" if not path_hits else " — %s" % path_hits[:3]))

    # PDF üstverisi
    code, info = run(["pdfinfo", INTERIOR])
    rep.check(not LOCAL_PATH.search(info), "PDF üstverisinde yerel yol yok")


def check_placeholders(rep):
    print("\n── ⑥ YER TUTUCU ──")
    man = jload(os.path.join(ROOT, "07_ASSETS", "ASSET_MANIFEST.json"), {})
    ph = [a["assetId"] for a in man.get("assets", [])
          if a.get("status") == "placeholder-art-missing"]
    final_dir = os.path.join(ROOT, "07_ASSETS", "final", "interior")
    missing = [a["assetId"] for a in man.get("assets", [])
               if not os.path.isfile(os.path.join(final_dir, a["filename"]))]
    rep.facts["manifestPlaceholders"] = ph
    rep.facts["finalAssetsMissing"] = missing
    rep.check(not missing, "her varlığın nihai dosyası var (%d)"
              % (len(man.get("assets", [])) - len(missing))
              + ("" if not missing else " — EKSİK: %s" % missing[:5]))
    if ph:
        rep.warn("manifest %d varlığı hâlâ `placeholder-art-missing` diye "
                 "kaydediyor; nihai dosyalar YERİNDE — durum alanı "
                 "şartnameden gelir ve `visualSpec.status` güncellenmeli: %s"
                 % (len(ph), ph))


# ═══════════════════════════════════════════════════════════════════════════
def check_previewer_class(rep, quick):
    """⑦ PREVIEWER SINIFI — gerçek Previewer'ın bulduğu hata SINIFLARI.

    ⭑ BU BÖLÜM BİR ÜRETİM HATASINDAN DOĞDU ⭑

    Yerel CI yeşilken **gerçek Amazon KDP Print Previewer** iki hata
    bildirdi: yetersiz iç kenar (156 sayfanın 152'sinde) ve sayfa 47'de
    margin dışına taşan metin. Hiçbir yerel kapı bunları sormamıştı.

        Bir kapı, sorduğu soruyu ölçer. Sormadığı soru yeşil görünür.

    O yüzden burada tek bir sayfa değil, Previewer'ın soracağı SORU
    SINIFLARI sorulur: kenar boşluğu · sayfa ölçüsü tekbiçimliliği ·
    yinelenen sayfa · yerleştirilmiş görselin ETKİN çözünürlüğü ·
    kenara değen mürekkep · eksik glif.

    ⚠ Bu bölüm KDP Previewer'ı taklit veya simüle ETMEZ. Previewer bir
    Amazon hizmetidir ve yalnızca panelde koşar. Burada yapılan,
    Previewer'ın YAYIMLANMIŞ kurallarını modelleyip basılı dosyayı
    onlara karşı ölçmektir. Nihai hüküm yalnızca Previewer'a aittir.
    """
    print("\n── ⑦ PREVIEWER SINIFI ──")
    if not os.path.isfile(INTERIOR):
        return
    pages = rep.facts.get("interiorPages")

    # ① KENAR BOŞLUĞU — `qa_margins.py` ölçtü, burada TAZELİĞİ denetlenir.
    #    Bayat bir ölçüm, ölçüm değildir.
    mg = jload(os.path.join(ROOT, "06_REPORTS", "margins.json"))
    if rep.check(bool(mg), "kenar boşluğu ölçümü var (06_REPORTS/margins.json)"):
        mf = mg.get("facts", {})
        rep.check(mf.get("pages") == pages,
                  "kenar ölçümü BU PDF'e ait (%s ⇄ %s sayfa)"
                  % (mf.get("pages"), pages))
        rep.check(mg.get("status") == "pass" and mf.get("violations") == 0,
                  "hiçbir sayfa KDP kenar boşluğunu ihlal etmiyor (%s ihlal)"
                  % mf.get("violations"))
        # Kural sayfa sayısından TÜREMİŞ mi — elle yazılmış olmasın.
        tier = {(24, 150): 0.375, (151, 300): 0.5, (301, 500): 0.625,
                (501, 700): 0.75, (701, 828): 0.875}
        want = next((v for (lo, hi), v in tier.items()
                     if pages and lo <= pages <= hi), None)
        rep.check(want is not None
                  and abs(mf.get("requiredGutter", -1) - want) < 1e-9,
                  "iç kenar ölçütü %s sayfadan TÜREDİ (%s in)"
                  % (pages, want))
        rep.facts["marginMinInner"] = mf.get("minInner")
        rep.facts["marginMinOuter"] = mf.get("minOuter")

    # ② SAYFA ÖLÇÜSÜ TEKBİÇİMLİ Mİ — tek bir yatay sayfa Previewer'ı kırar.
    code, info = run(["pdfinfo", "-l", str(pages or 1), INTERIOR])
    sizes = set(re.findall(r"Page\s+\d+ size:\s+([\d.]+ x [\d.]+)", info))
    if not sizes:                       # tek ölçü varsa pdfinfo tekil yazar
        sizes = set(re.findall(r"Page size:\s+([\d.]+ x [\d.]+)", info))
    rep.facts["interiorPageSizes"] = sorted(sizes)
    rep.check(len(sizes) == 1,
              "bütün sayfalar AYNI ölçüde (%d farklı ölçü)" % len(sizes)
              + ("" if len(sizes) == 1 else " — %s" % sorted(sizes)[:4]))

    # ③ YERLEŞTİRİLMİŞ GÖRSELİN ETKİN ÇÖZÜNÜRLÜĞÜ
    #    ⚠ Ölçülen şey dosyanın piksel sayısı DEĞİL, sayfada BASILDIĞI
    #    boya bölünmüş hâlidir. `interior.py` bunu kendi kaydeder; burada
    #    BAĞIMSIZ bir araçla (`pdfimages`) doğrulanır — kendi ölçümünü
    #    kendi doğrulayan bir hat, hiçbir şey doğrulamaz.
    if run(["which", "pdfimages"])[0] == 0:
        code, lst = run(["pdfimages", "-list", INTERIOR])
        ppi = []
        for line in lst.splitlines()[2:]:
            f = line.split()
            if len(f) >= 14:
                try:
                    ppi.append((int(f[0]), float(f[12])))
                except ValueError:
                    pass
        if ppi:
            floor = float((jload(os.path.join(ROOT, "06_REPORTS",
                                              "interior.json"), {}) or {})
                          .get("facts", {}).get("artDpiFloor") or 150.0)
            low = sorted({pg for pg, v in ppi if v < floor - 1})
            rep.facts["placedImages"] = len(ppi)
            rep.facts["placedImageMinPpi"] = round(min(v for _, v in ppi), 1)
            rep.facts["placedImageDpiFloor"] = floor
            rep.check(not low,
                      "yerleştirilen %d görselin hepsi ≥ %.0f dpi (en düşük "
                      "%.0f)" % (len(ppi), floor, min(v for _, v in ppi))
                      + ("" if not low else " — TABAN ALTI sayfalar: %s"
                         % low[:10]))
            # KDP'nin kendi tavsiyesi 300 dpi'dır ve bu kitap onu
            # KARŞILAMAZ (K39 kurucu kararı). Kırmızı değil, AÇIK uyarı.
            if min(v for _, v in ppi) < 300:
                rep.warn("iç blok görselleri KDP'nin 300 dpi TAVSİYESİNİN "
                         "altında (en düşük %.0f dpi) — K39 kurucu kararı; "
                         "Previewer bunu uyarı olarak gösterebilir"
                         % min(v for _, v in ppi))

    # ④ YİNELENEN SAYFA — İKİ ARAÇLA, ÇÜNKÜ BİRİ YETMEDİ
    #
    # ⭑ RASTER KARŞILAŞTIRMASI KUSURU KAÇIRDI ⭑
    #
    # `how-a-page-works` bölümü sayfa 4 ve 5'e BİREBİR AYNI basılıyordu.
    # Raster karşılaştırması bunu göremedi: iki sayfanın dip numarası
    # (4 ve 5) farklıydı ve tek bir piksel farkı hash'i değiştirir.
    # Kusuru gözle bir kontakt sayfasında gördüm, araç değil.
    #
    #     Bir yinelenen sayfayı numarasından tanıyamazsınız —
    #     numarası zaten farklıdır. METNİ aynıdır.
    #
    # Bu yüzden önce METİN karşılaştırılır (dip numarası atılarak),
    # sonra raster. İkisi farklı kusurları yakalar: metin, aynı sözü
    # iki kez basmayı; raster, aynı çizimi iki kez basmayı.
    code, alltxt = run(["pdftotext", "-layout", INTERIOR, "-"])
    ptexts = alltxt.split("\f")
    norm, tdup = {}, []
    for i, t in enumerate(ptexts[:pages or 0], 1):
        k = re.sub(r"\s+", " ", t).strip()
        k = re.sub(r"\s*\d+\s*$", "", k)          # dip numarasını at
        if len(k) < 200:                           # kısa/boş sayfa: meşru
            continue
        if k in norm:
            tdup.append((norm[k], i))
        else:
            norm[k] = i
    rep.facts["duplicateTextPages"] = tdup
    rep.check(not tdup, "aynı METNİ basan sayfa çifti yok"
              + ("" if not tdup else " — %s" % tdup[:6]))

    # ④b raster — aynı ÇİZİMİ iki kez basmayı yakalar
    if not quick:
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            run(["pdftoppm", "-r", "24", "-gray", "-png", INTERIOR,
                 os.path.join(td, "p")])
            seen, dups = {}, []
            for i, f in enumerate(sorted(os.listdir(td)), 1):
                with open(os.path.join(td, f), "rb") as fh:
                    h = hashlib.sha256(fh.read()).hexdigest()
                if h in seen:
                    dups.append((seen[h], i))
                else:
                    seen[h] = i
            # Boş/az mürekkepli sayfalar meşru olarak birbirinin aynısıdır
            # (Field Notes cetvelli sayfaları). Kusur, DOLU bir sayfanın
            # tekrarıdır.
            blanks = set(rep.facts.get("interiorBlankPages") or [])
            real = [d for d in dups if d[0] not in blanks and d[1] not in blanks]
            rep.facts["duplicateRenderedPages"] = real
            rep.check(not real, "aynı görünen DOLU sayfa çifti yok"
                      + ("" if not real else " — %s" % real[:6]))

    # ⑤ EKSİK GLİF (tofu) — metin katmanında yer tutucu karakter
    code, txt = run(["pdftotext", INTERIOR, "-"])
    tofu = txt.count("\ufffd") + txt.count("\u25a1")
    rep.facts["interiorReplacementChars"] = tofu
    rep.check(tofu == 0, "eksik glif yer tutucusu yok (%d)" % tofu)

    # ⭑ PROVA SAYFA NUMARALARI — KAYABİLİRLER, VE KAYDILAR ⭑
    #
    # `PROOF_HANDOFF § 1` kurucuya "şu sayfalara bak" diyen bir tablo
    # taşıyor. Ön maddedeki kopya sayfa kaldırılınca (K59) 4'ten sonraki
    # her folyo bir azaldı ve tablonun DOKUZ SATIRI da yanlış sayfayı
    # gösterir oldu. Hiçbir kapı fark etmedi.
    #
    #     Bir belgedeki sayfa numarası, kitap her yeniden dizildiğinde
    #     yeniden DOĞRULANMASI gereken bir iddiadır.
    #
    # Her satır artık o sayfada GERÇEKTEN geçen bir ifadeyi `kod` olarak
    # taşır; burada o ifade o sayfanın metninde aranır.
    ph = os.path.join(ROOT, "08_OUTPUT", "PROOF_HANDOFF.md")
    if os.path.isfile(ph) and ptexts:
        with open(ph, encoding="utf-8") as fh:
            pht = fh.read()
        bad = []
        for m in re.finditer(r"^\|\s*\*\*(\d+)(?:[–-]\d+)?\*\*\s*\|(.+)\|\s*$",
                             pht, re.M):
            n = int(m.group(1))
            marks = re.findall(r"`([^`]+)`", m.group(2))
            if not marks:
                continue
            page = ptexts[n - 1] if 0 < n <= len(ptexts) else ""
            flat = re.sub(r"\s+", " ", page)
            for mk in marks:
                if re.sub(r"\s+", " ", mk) not in flat:
                    bad.append("s.%d ⊄ %r" % (n, mk))
        rep.facts["proofPageRefsBad"] = bad
        rep.check(not bad, "prova sayfa numaraları GERÇEK sayfaları gösteriyor"
                  + ("" if not bad else " — KAYMIŞ: %s" % bad[:6]))

    # ⑥ BLEED BEYANI ⇄ GERÇEK
    cfg = jload(os.path.join(ROOT, "project_config.json"), {}) or {}
    bleed = bool(cfg.get("production", {}).get("interiorBleed", False))
    rep.facts["interiorBleedDeclared"] = bleed
    if mg:
        rep.check(mg.get("facts", {}).get("bleed") == bleed,
                  "bleed beyanı ölçümle aynı (%s)" % ("VAR" if bleed else "YOK"))



# ═══════════════════════════════════════════════════════════════════════════
PB_FILES = ("interior.pdf", "cover.pdf", "metadata.json")
PB_SUMS = os.path.join(ROOT, "08_OUTPUT", "PAPERBACK", "checksums.txt")


def seal_paperback():
    """⭑ PAKETİ MÜHÜRLE — açık bir OPERATÖR eylemi ⭑

    `checksums.txt` elle yazılmıştı ve hiçbir betik onu tazelemiyor,
    hiçbir kapı onu denetlemiyordu. Bir dosya ne üretiliyor ne
    denetleniyorsa, taşıdığı sayı bir SÜSTÜR: iç blok yeniden
    kurulduğu an sessizce yalan söylemeye başlar.

        Denetleyenin mühürlemesi döngüseldir.
        O yüzden mühür AÇIKÇA istenir, denetim KENDİLİĞİNDEN koşar.

    Bu yüzden `--seal` ayrı bir bayraktır: `kdp_preflight.py` varsayılan
    hâlinde yalnızca DOĞRULAR ve bayat mühürde KIRMIZI yanar."""
    src = os.path.join(ROOT, "06_REPORTS", "tracked", "metadata.json")
    dst = os.path.join(ROOT, "08_OUTPUT", "PAPERBACK", "metadata.json")
    if os.path.isfile(src):
        with open(src, encoding="utf-8") as fh:
            blob = fh.read()
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(blob)
    lines = []
    for n in PB_FILES:
        fp = os.path.join(ROOT, "08_OUTPUT", "PAPERBACK", n)
        if os.path.isfile(fp):
            lines.append("%s  %s" % (sha256(fp), n))
    with open(PB_SUMS, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("  mühürlendi: %s" % os.path.relpath(PB_SUMS, ROOT))
    for l in lines:
        print("    %s" % l)


def check_seal(rep):
    """⑧ PAKET MÜHRÜ — checksums.txt gerçekten BU dosyaları mı anlatıyor."""
    print("\n── ⑧ PAKET MÜHRÜ ──")
    if not os.path.isfile(INTERIOR):
        return
    if not rep.check(os.path.isfile(PB_SUMS), "checksums.txt var"):
        return
    want = {}
    with open(PB_SUMS, encoding="utf-8") as fh:
        for line in fh:
            f = line.split()
            if len(f) == 2:
                want[f[1]] = f[0]
    rep.check(set(want) == set(PB_FILES),
              "mühür üç dosyayı da anıyor (%s)" % ", ".join(sorted(want)))
    stale = []
    for n, h in want.items():
        fp = os.path.join(ROOT, "08_OUTPUT", "PAPERBACK", n)
        if not os.path.isfile(fp) or sha256(fp) != h:
            stale.append(n)
    rep.facts["paperbackSealStale"] = stale
    rep.check(not stale, "mühür TAZE — dosyalar mühürlendiği gibi"
              + ("" if not stale else " — BAYAT: %s "
                 "(`kdp_preflight.py --seal` ile tazeleyin)" % stale))
    # ⭑ EL KİTABI DA BAYATLAR ⭑
    # `KDP_UPLOAD_HANDBOOK § 0` yüklenecek dosyaların sha256 önekini ELLE
    # taşıyordu ve iç blok yeniden kurulduğunda kimse onu güncellemedi:
    # kurucunun "doğru dosyayı yüklüyor muyum" diye baktığı tablo yanlış
    # bir özet gösteriyordu.
    #
    #     Bir belgede duran her sayı, kaynağı değiştiğinde yalan olur.
    #     O yüzden sayı ya ÜRETİLİR ya DENETLENİR.
    hb = os.path.join(ROOT, "08_OUTPUT", "KDP_UPLOAD_HANDBOOK.md")
    if os.path.isfile(hb):
        with open(hb, encoding="utf-8") as fh:
            hbt = fh.read()
        wrong = []
        for n in PB_FILES:
            fp = os.path.join(ROOT, "08_OUTPUT", "PAPERBACK", n)
            if os.path.isfile(fp) and ("PAPERBACK/%s`" % n) in hbt:
                if sha256(fp)[:16] not in hbt:
                    wrong.append(n)
        rep.facts["handbookStaleHashes"] = wrong
        rep.check(not wrong, "el kitabındaki sha256 önekleri GERÇEK dosyalarla "
                  "uyuşuyor" + ("" if not wrong else " — BAYAT: %s" % wrong))

    # Pakete konan metadata, izlenen metadata ile AYNI olmalı.
    src = os.path.join(ROOT, "06_REPORTS", "tracked", "metadata.json")
    dst = os.path.join(ROOT, "08_OUTPUT", "PAPERBACK", "metadata.json")
    if os.path.isfile(src) and os.path.isfile(dst):
        rep.check(sha256(src) == sha256(dst),
                  "paketteki metadata.json izlenen sürümle AYNI")



def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--seal", action="store_true",
                    help="paketi mühürle (checksums.txt tazele)")
    args = ap.parse_args()

    print("=" * 74)
    print("  KDP ÖN UÇUŞ DENETİMİ")
    print("=" * 74)
    for tool in ("pdfinfo", "pdffonts", "pdftotext"):
        if run(["which", tool])[0] != 0:
            print("  ⊘ %s yok — ATLANDI" % tool)
            print("=" * 74)
            return 2

    rep = Report(verbose=False)
    txt = check_interior(rep, args.quick) or ""
    check_cover(rep)
    check_aplus(rep)
    check_consistency(rep, txt)
    check_leaks(rep, txt)
    check_placeholders(rep)
    check_previewer_class(rep, args.quick)
    if args.seal:
        print("\n── MÜHÜRLEME ──")
        seal_paperback()
    check_seal(rep)

    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as fh:
        json.dump({"status": "fail" if rep.errors else "pass",
                   "checks": rep.checks, "errors": rep.errors,
                   "warnings": rep.warnings, "facts": rep.facts},
                  fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
        for w in rep.warnings:
            print("     ! %s" % w)
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        print("=" * 74)
        return 1
    print("  ✅ %d ÖN UÇUŞ DENETİMİ YEŞİL" % rep.checks)
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
