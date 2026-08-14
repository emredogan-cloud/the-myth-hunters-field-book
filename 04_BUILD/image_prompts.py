#!/usr/bin/env python3
"""
GÖRSEL PROMPT KÜTÜPHANESİ ÜRETECİ — The Myth Hunter's Field Book
================================================================================
`07_ASSETS/IMAGE_PROMPT_LIBRARY.html` **elle yazılmaz**. Manuscript'teki
`visualSpec` alanlarından ÜRETİLİR ve `--check` bayrağıyla bayatlığı
denetlenir (karar K17 · `update_docs.py` ile aynı gerekçe).

    Elle yazılan bir varlık listesi, bir sayfa değişince sessizce yalan
    söylemeye başlar — ve görsel hattı yanlış aktiviteye bağlanmış
    kusursuz bir görsel üretir. Faz 5'in en pahalı hatası budur.

⭑ BU DOSYANIN EN ÖNEMLİ KURALI — NE BASMADIĞI ⭑

Kütüphane **takip edilen** bir dosyadır ve karar K10 cevapların depoya
girmesini yasaklıyor. `pagePrints` listeleri cevabın KENDİSİNİ taşır:

    "<the one basket drawn empty, carrying the zero sign>"

Böyle bir cümle bir görsel şartnamesidir **ve aynı zamanda cevaptır**:
hangi sepetin boş çizileceğini söylemek, cevabı söylemektir. Faz 2 bu
yüzden şartname metnini kütüphaneye almadı, yalnızca sözleşmesini
anlattı. Faz 3 aynı sınırı korur ve mekanikleştirir:

    KÜTÜPHANEYE GİREN  → kimlik · sınıf · düzen · ölçü · kısıt · şablon
    KÜTÜPHANEYE GİRMEYEN → pagePrints · requiredLabels · yıldızlı sözcük

Prompt şablonları `{PRINT_LIST}` yer tutucusu taşır. Faz 5'te promptu
üreten kişi o yer tutucuyu **elindeki manuscript'ten** doldurur; public
depo hiçbir zaman dolu hâlini görmez.

  ./04_BUILD/image_prompts.py            kütüphaneyi tazele
  ./04_BUILD/image_prompts.py --check    bayatsa KIRMIZI

TASARIM: yalnızca Python standart kütüphanesi (karar K7).

Çıkış kodları:  0 = güncel/yazıldı   1 = BAYAT   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import collections
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

BOOK = os.path.join(ROOT, "02_MANUSCRIPT", "book.json")
ACTS = os.path.join(ROOT, "01_SOURCE", "activity_index.json")
CULTURES = os.path.join(ROOT, "01_SOURCE", "culture_index.json")
REGIONS = os.path.join(ROOT, "01_SOURCE", "region_index.json")
CONFIG = os.path.join(ROOT, "project_config.json")
OUT = os.path.join(ROOT, "07_ASSETS", "IMAGE_PROMPT_LIBRARY.html")

BANNER = "<!-- ÜRETİLMİŞTİR — 04_BUILD/image_prompts.py · ELLE DÜZENLEMEYİN -->"
OUT_LOCAL = os.path.join(ROOT, "07_ASSETS", "IMAGE_PROMPT_LIBRARY.local.html")

# ── Düzen başına prompt şablonu ────────────────────────────────────────────
# Şablonlar SINIF düzeyindedir ve sayfaya özel hiçbir şey taşımaz.
# {PRINT_LIST} yer tutucusu Faz 5'te manuscript'ten doldurulur.
TEMPLATES = {
    "key-decode": (
        "Black ink line drawing on white, technical field-guide style, no shading. "
        "A decoding plate for a children's activity book. Left: a boxed KEY PANEL "
        "listing each sign beside its value, ruled and evenly spaced. Right: the "
        "items to be decoded, printed large with clear space beneath each one for "
        "a handwritten answer. The key and the items must sit on the SAME spread — "
        "a child must never turn a page to reach the key.\n\nPRINT EXACTLY:\n{PRINT_LIST}"),
    "key-build": (
        "Black ink line drawing on white, technical field-guide style, no shading. "
        "An assembly plate: a PARTS BANK of separate signs along the top, and below "
        "it empty ruled frames the size of a finished unit. Frames must be large "
        "enough for a child's pencil to build inside them.\n\nPRINT EXACTLY:\n{PRINT_LIST}"),
    "sort-cards": (
        "Black ink line drawing on white, no shading. A set of rectangular CARDS "
        "scattered in a deliberately shuffled order, each card carrying one printed "
        "sentence and one empty square number box in its corner. Cards must not be "
        "arranged in any order that hints at the sequence.\n\nPRINT EXACTLY:\n{PRINT_LIST}"),
    "sort-columns": (
        "Black ink line drawing on white, no shading. Two columns of cards with a "
        "wide empty channel between them, sized for a child to rule a straight line "
        "across. The right column must be in a different order from the left.\n\n"
        "PRINT EXACTLY:\n{PRINT_LIST}"),
    "plate-label": (
        "Black ink line drawing on white, technical cutaway style, no shading. One "
        "subject drawn large and clearly, with numbered pointer lines running out to "
        "empty ruled label lines in the margin. Every part that must be labelled has "
        "to be visually DISTINCT from its neighbours.\n\nPRINT EXACTLY:\n{PRINT_LIST}"),
    "plate-compare": (
        "Black ink line drawing on white, no shading. Two or more subjects drawn at "
        "the SAME scale and in the SAME pose, side by side, so that a difference in "
        "the drawing is a real difference and not an artefact of the drawing. Empty "
        "circles printed over the plate where a difference can be marked.\n\n"
        "PRINT EXACTLY:\n{PRINT_LIST}"),
    "data-table": (
        "Black ink line drawing on white. A ruled TABLE with a clear head row, rows "
        "of the same height, and one empty column for the reader's own working. "
        "Figures right-aligned. No decorative border.\n\nPRINT EXACTLY:\n{PRINT_LIST}"),
    "map-trace": (
        "Black ink line drawing on white, outline map, no shading and no relief "
        "hatching. Coastlines and borders printed PALE so a child's pencil line "
        "reads on top of them. A scale bar and a north arrow in one corner. No more "
        "than four points to mark.\n\nPRINT EXACTLY:\n{PRINT_LIST}"),
    "map-overlay": (
        "Black ink line drawing on white. An outline map printed pale, and a separate "
        "outline shape printed beside it at the SAME scale, so the shape can be "
        "traced and laid over the map.\n\nPRINT EXACTLY:\n{PRINT_LIST}"),
    "make-frame": (
        "Black ink line drawing on white. One large empty FRAME carrying the page's "
        "constraint as part of the drawing (a rule line, a centre mark, a ruled "
        "guide), plus a small worked example in one corner at reduced size. The "
        "frame must be mostly empty: the child fills it.\n\nPRINT EXACTLY:\n{PRINT_LIST}"),
}

# ── Varlık sınıfı şablonları — aktivite DIŞI dört sınıf (Faz 5) ───────────
# Bunlar bir düzen değil bir SINIF taşır: vinyet bir levha değildir, damga
# bir illüstrasyon değildir. Şablonu düzenden değil sınıftan almaları bu
# yüzden zorunlu.
CLASS_TEMPLATES = {
    "culture-vignette": (
        "Black ink line drawing on white, technical field-guide style, no shading. "
        "A small CONTEXT vignette for one named culture in a children's field book. "
        "Draw two or three documented, everyday objects or landscape features that "
        "belong to this culture and to no other, arranged as a still group with "
        "clear white space around them. This is not a puzzle and carries no answer: "
        "nothing in it is counted, ordered or matched anywhere in the book.\n\n"
        "It must read as a place people LIVE, not as a ruin, a museum case or a "
        "costume. No people, no faces, no ceremony, no sacred object.\n\n"
        "PRINT EXACTLY ONE LABEL — the culture's own name:\n{PRINT_LIST}"),
    "seal-stamp": (
        "Black ink line drawing on white, no shading. A STAMP OUTLINE for the end "
        "of one region of a children's field book, drawn as an empty frame a child "
        "will write inside. The frame carries the region's own motif on its border "
        "and one NOTCH cut into the edge.\n\n"
        "⭑ THE STAMP CARRIES NO LETTERS AND NO WORDS. The letter slots are drawn "
        "EMPTY as plain ruled squares. The notch is drawn but NOT numbered — the "
        "number is set in type later. A letter printed here would destroy the only "
        "self-check in the book.\n\n{PRINT_LIST}"),
    "badge": (
        "Black ink line drawing on white, no shading. A small reusable INTERFACE "
        "mark for a children's activity book, drawn to read clearly at thumbnail "
        "size. Heavy even line weight, no fine detail, no culture-specific "
        "ornament: this mark appears on pages from every region and must belong to "
        "none of them.\n\n{PRINT_LIST}"),
    "front-matter": (
        "Black ink line drawing on white, technical diagram style, no shading. An "
        "instructional DIAGRAM for the opening pages of a children's field book. It "
        "explains how the book itself works.\n\n"
        "⭑ It must use a NEUTRAL demonstration subject and must NOT reproduce any "
        "real activity page from the book. It carries no seal word, no answer and "
        "no puzzle content.\n\n{PRINT_LIST}"),
}

NEGATIVE = [
    "no colour — the interior is printed black and white",
    "no greyscale washes or gradients; line and solid black only",
    "no photographic or realistic human faces",
    "no text baked into the image except the labels listed in PRINT EXACTLY",
    "no answer visible anywhere in the image",
    "no decorative borders, frames, corner flourishes or drop shadows",
    "no AI watermark, signature or logo",
    "no modern branding, clothing or objects in a historical scene",
    "no religious ritual shown as an action a reader could copy",
    "no weapon in use, no wound, no blood, no body",
]

TYPOGRAPHY = [
    ("Görselde metin", "YALNIZCA PRINT EXACTLY listesindeki etiketler. Başka hiçbir şey."),
    ("Yazı tipi", "Görsele metin GÖMÜLMEZ. Etiketler dizgi katmanında basılır (Faz 5)."),
    ("Neden", "Gömülü metin düzeltilemez, ölçeklenemez ve dil değişirse yeniden çizim ister."),
    ("Etiket yeri", "Şartnamedeki işaretçi konumları; görsel yalnızca YERİ ayırır."),
    ("Asgari punto", "Faz 5 ölçer. Bu belge yer ayırma kuralını taşır, punto değerini değil."),
]


def jload(p, default=None):
    if not os.path.isfile(p):
        return default
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def esc(s):
    return html.escape(str(s), quote=True)


def english_constraints(restrictions, culture_id, cmap):
    """Prompta giden kısıtları İNGİLİZCEYE çevirir.

    ⭑ NEDEN — VE BU BİR ÜSLUP MESELESİ DEĞİL ⭑

    `visualSpec.restrictions` içindeki kültürel kısıtlar Türkçedir çünkü
    `culture_index` proje dilindedir. Ama bu satırlar görseli ÜRETEN
    tarafa gider ve bir üreteç Türkçe bir emri güvenilir biçimde
    uygulamaz.

        Uygulanamayan bir kısıt, yazılmamış bir kısıttır.

    Ve tam olarak EN ÖNEMLİ kısıtlar bunlar: kültürel güvenlik.
    Eşleştirme sıraya göre yapılır — `forbiddenForms[i]` ↔
    `forbiddenFormsEn[i]` — ve iki liste aynı uzunlukta olmak
    zorundadır (qa_assets § ⑧b denetler).
    """
    STD = ("No answer may be visible", "No decorative text", "No photographic")
    c = (cmap or {}).get(culture_id or "") or {}
    tr = c.get("forbiddenForms") or []
    en = c.get("forbiddenFormsEn") or []
    def norm(x):
        """⚠ TÜRKÇE NOKTASIZ-I KATLAMASI — Faz 4 § 28 ④'ün aynı dersi.

        'CEVABI'.lower() Python'da 'cevabi' verir, 'cevabı' değil: nokta
        Türkçede anlamlıdır ama Unicode küçültmesi onu bilmez. Katlama
        yapılmazsa aynı kısıtın iki yazımı eşleşmez ve kültürel güvenlik
        kısıtı SESSİZCE çevrilmeden kalır.

        Faz 4 aynı kusuru üçüncü kez gördüğünde örneği değil SINIFI
        kapatmıştı; burada da liste büyütülmüyor, KATLAMA yapılıyor."""
        x = (x or "").replace("İ", "i").replace("I", "ı")
        x = x.lower().replace("ı", "i")
        return re.sub(r"[^a-zçğöşü ]", "", x).strip()

    pairs = list(zip(tr, en)) if len(tr) == len(en) else []
    out = []
    for r in restrictions:
        if r.startswith(STD):
            continue
        if r.startswith("culture_index §"):
            # Faz 4 kimi sayfada kısıtı SAYFAYA GÖRE yeniden yazdı ve
            # sonuna İngilizce bir emir ekledi:
            #   "... yasak biçim: X — no mystical glow or aura."
            # Bu hâl kanonik dizeyle birebir eşleşmez. Üç aşamalı
            # eşleştirme: birebir → gövde eşleşmesi → İngilizce kuyruk.
            body = r.split(":", 1)[1] if ":" in r else r
            tail = ""
            for dash in ("—", " - "):
                if dash in body:
                    body, tail = body.split(dash, 1)
                    break
            nb = norm(body)
            hit = ""
            for t, e in pairs:
                nt = norm(t)
                if nb and nt and (nb == nt or nb in nt or nt in nb):
                    hit = e
                    break
            if hit:
                out.append("CULTURAL SAFETY: " + hit
                           + (" " + tail.strip() if tail.strip() else ""))
                continue
            if tail.strip():
                # Kanonik karşılık yok ama sayfanın kendi İngilizce emri var.
                out.append("CULTURAL SAFETY: " + tail.strip())
                continue
            # Hiçbiri yoksa kısıt SESSİZCE DÜŞMEZ: düşerse prompt daha
            # temiz görünür ve daha az korur.
            out.append("CULTURAL SAFETY (project record, untranslated): " + r)
            continue
        if r.startswith("KAPALI KATMAN"):
            out.append("CLOSED LAYER: the forbidden layer of the source record "
                       "may not enter the drawing.")
            continue
        out.append(r)
    return out


def load_assets():
    """Tam envanteri okur (yerel), yoksa takip edileni.

    ⚠ Takip edilen envanter İÇERİK taşımaz (K10). Onunla üretilen bir
    kütüphane yalnızca yer tutucu sürümü verebilir — ve bunu SÖYLER."""
    local = os.path.join(ROOT, "07_ASSETS", "ASSET_MANIFEST.local.json")
    pub = os.path.join(ROOT, "07_ASSETS", "ASSET_MANIFEST.json")
    for path, full in ((local, True), (pub, False)):
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as fh:
                return json.load(fh), full
    return None, False


def build(populated: bool = False) -> str:
    book = jload(BOOK, {"activities": []}) or {"activities": []}
    acts_doc = jload(ACTS, {"activities": []}) or {"activities": []}
    design = {a["activityId"]: a for a in acts_doc.get("activities", [])}
    cultures = (jload(CULTURES, {}) or {}).get("cultures", [])
    regions = (jload(REGIONS, {}) or {}).get("regions", [])
    cfg = jload(CONFIG, {}) or {}
    rorder = {r["id"]: r.get("order", 99) for r in regions}
    rname = {r["id"]: r.get("en", r["id"]) for r in regions}

    specs = []
    for a in book.get("activities", []):
        vs = a.get("visualSpec")
        if not vs:
            continue
        d = design.get(a["activityId"], {})
        specs.append((rorder.get(d.get("region"), 99), d.get("region", "?"), a, vs, d))
    specs.sort(key=lambda x: (x[0], x[2].get("pageOrder", 0)))

    cmap = {c["id"]: c for c in cultures}
    inv, inv_full = load_assets()
    inv_assets = (inv or {}).get("assets", []) if inv else []
    by_id = {a.get("assetId"): a for a in inv_assets}
    # Aktivite dışı sınıflar: vinyet · damga · rozet · ön madde
    extra = [a for a in inv_assets if a.get("assetClass") != "activity"]
    rank = {"culture-vignette": 0, "seal-stamp": 1, "badge": 2, "front-matter": 3}
    extra.sort(key=lambda a: (rank.get(a.get("assetClass"), 9),
                              rorder.get(a.get("region") or "", 99),
                              a.get("assetId") or ""))

    by_layout = collections.Counter(vs["layout"] for _, _, _, vs, _ in specs)
    by_region = collections.Counter(r for _, r, _, _, _ in specs)

    L = ["<!doctype html>", '<html lang="tr">', "<head>", '<meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1">',
         "<title>Görsel Prompt Kütüphanesi — The Myth Hunter's Field Book</title>",
         BANNER, "<style>", CSS, "</style>", "</head>", "<body>", '<div class="wrap">']

    produced = sum(1 for a in inv_assets
                   if os.path.isfile(os.path.join(ROOT, a.get("processedLocation") or "")))
    L += [
        "<h1>Görsel Prompt Kütüphanesi</h1>",
        '<p class="sub">The Myth Hunter\'s Field Book · <strong>Faz 5 · %s</strong> · '
        "14 Ağustos 2026<br>%d varlık · %d aktivite şartnamesi · "
        "<strong>%d üretilmiş varlık</strong>.</p>"
        % ("ÜRETİM KATMANI · dolu promptlar" if populated
           else "şartname katmanı · yer tutuculu",
           len(inv_assets), len(specs), produced),
    ]

    if populated:
        L += [
            '<div class="note stop">',
            "<strong>BU DOSYA DEPOYA GİRMEZ.</strong><br>",
            "Promptlar <code>PRINT EXACTLY</code> listeleriyle <strong>DOLU</strong> "
            "ve o listeler cevabın kendisini taşır: "
            "<em>“the chilli basket drawn empty”</em> bir şartnamedir "
            "<strong>ve aynı zamanda cevaptır</strong> (karar K10). "
            "<code>.gitignore § ③d</code> bu dosyayı dışlar ve "
            "<code>validate_structure § ⑤b</code> depoya girmesini kırmızı yakar.",
            "</div>",
            '<div class="note">',
            "<strong>KULLANIM.</strong> Bir varlığın kutusundaki "
            "<em>promptu kopyala</em> düğmesine bas ve üretece yapıştır. Prompt "
            "şablonu, basılacak listeyi, ortak olumsuz kısıtları ve o sayfanın "
            "kültürel kısıtlarını <strong>birlikte</strong> taşır — dört parçayı "
            "elle birleştirmek gerekmez.",
            "</div>",
        ]
    else:
        L += [
            '<div class="note stop">',
            "<strong>ŞARTNAME BİR VARLIK DEĞİLDİR.</strong><br>",
            "Bu belge %d görselin <em>ne olması gerektiğini</em> söyler. "
            "<code>BOOK_STATS.md</code> ikisini ayrı satırlarda sayar: "
            "<em>görsel şartnamesi</em> ve <em>görsel varlık</em>."
            % len(inv_assets),
            "</div>",
            '<div class="note stop">',
            "<strong>BU BELGE CEVAP TAŞIMAZ — VE TAŞIYAMAZ (karar K10).</strong><br>",
            "Her sayfanın basacağı şeylerin tam listesi (<code>pagePrints</code>) "
            "<em>cevabın kendisidir</em>. Bu yüzden buradaki promptlar "
            "<code>{PRINT_LIST}</code> yer tutucusuyla durur.<br><br>"
            "<strong>Dolu sürüm:</strong> <code>./04_BUILD/image_prompts.py</code> "
            "koştuğunda <code>07_ASSETS/IMAGE_PROMPT_LIBRARY.local.html</code> "
            "dosyasını da yazar. O dosya <strong>depoya girmez</strong> ve "
            "kurucunun gerçek çalışma arayüzüdür.",
            "</div>",
        ]

    L += [
        "<h2>1 · Sözleşme: görsel metnin İHTİYACINDAN türer</h2>",
        "<p>Karar <strong>K25</strong>: <em>bir talimat “the X” derse, levha X'i "
        "basmak zorundadır.</em> Faz 2 bunu 16 sayfada ölçtü ve 11'inin "
        "çözülemez olduğunu buldu — sebeplerin çoğu görseldeydi. Zincir şudur "
        "ve tersi çalışmaz:</p>",
        '<div class="chain">talimat → <code>pagePrints</code> → '
        "<code>visualSpec</code> → prompt → varlık</div>",
        "<p>Görsel hiçbir zaman “bir şeyler çiz”den doğmaz. "
        "<code>qa_instruction § ⑨</code> göndermeyi, <code>qa_design § ⑤</code> "
        "şartnameyi denetler; ikisi de her koşuda çalışır.</p>",

        "<h2>2 · Envanter</h2>",
        "<p>%d şartname · %d bölge · %d düzen sınıfı.</p>"
        % (len(specs), len(by_region), len(by_layout)),
        '<div class="scroll"><table>',
        "<tr><th>Bölge</th><th>Şartname</th><th>Üretilmiş</th></tr>",
    ]
    for rid, n in sorted(by_region.items(), key=lambda kv: rorder.get(kv[0], 99)):
        made = sum(1 for _, r2, _, vs, _ in specs if r2 == rid and os.path.isfile(
            os.path.join(ROOT, "07_ASSETS", "processed", "interior", vs["filename"])))
        L.append("<tr><td>%s <span class='tag'>%s</span></td><td>%d</td>"
                 "<td><strong>%d</strong></td></tr>"
                 % (esc(rname.get(rid, rid)), esc(rid), n, made))
    L.append("<tr><td><strong>toplam</strong></td><td><strong>%d</strong></td>"
             "<td><strong>%d</strong></td></tr>" % (len(specs), produced))
    L.append("</table></div>")

    L += ["<h2>3 · Ortak olumsuz kısıtlar</h2>",
          "<p>Her promptun sonuna <strong>değişmeden</strong> eklenir.</p>",
          '<div class="prompt" id="neg">' + esc("NEGATIVE: " + "; ".join(NEGATIVE))
          + '<button class="copy" data-t="neg">kopyala</button></div>']

    L += ["<h2>4 · Tipografi politikası</h2>", '<div class="scroll"><table>']
    for k, v in TYPOGRAPHY:
        L.append("<tr><td><strong>%s</strong></td><td>%s</td></tr>" % (esc(k), esc(v)))
    L.append("</table></div>")

    L += ["<h2>5 · Düzen şablonları</h2>",
          "<p>Şablonlar <strong>sınıf düzeyindedir</strong> ve sayfaya özel hiçbir "
          "şey taşımaz. Her sayfa kendi şablonunu § 6'daki satırından bulur.</p>"]
    for i, (lay, tmpl) in enumerate(sorted(TEMPLATES.items())):
        if not by_layout.get(lay):
            continue
        L.append("<h3><code>%s</code> <span class='tag'>%d sayfa</span></h3>"
                 % (esc(lay), by_layout[lay]))
        L.append('<div class="prompt" id="t%d">%s<button class="copy" data-t="t%d">'
                 "kopyala</button></div>" % (i, esc(tmpl), i))

    # ── DOLU PROMPT KUTULARI — yalnızca yerel sürümde ─────────────────────
    if populated and inv_full:
        L += ["<h2>6 · Üretime hazır promptlar</h2>",
              "<p>Her kutu <strong>tek başına</strong> yeterlidir: şablon + "
              "basılacak liste + ortak olumsuz kısıtlar + o varlığın kendi "
              "kısıtları. Kopyala, yapıştır, üret.</p>"]
        # ⚠ Grup, tasarım kaydını da TAŞIMAK zorunda: kültür kimliği oradan
        # gelir ve o olmadan kültürel kısıtlar çevrilemez. İlk hâl yalnızca
        # aktiviteyi taşıyordu ve bütün kısıtlar sessizce "untranslated"
        # dalına düşüyordu — prompt DOLU görünüyor, koruma YOK.
        groups = []
        for rid in sorted(by_region, key=lambda r: rorder.get(r, 99)):
            groups.append((rname.get(rid, rid),
                           [(a, d) for _, r2, a, vs, d in specs if r2 == rid]))
        # aktivite promptları, bölge bölge
        pidx = 0
        for gname, acts in groups:
            if not acts:
                continue
            L.append("<h3>%s <span class='tag'>%d sayfa</span></h3>"
                     % (esc(gname), len(acts)))
            for a, d in acts:
                vs = a["visualSpec"]
                inv_a = by_id.get(vs["assetId"], {})
                pidx += 1
                tmpl = TEMPLATES.get(vs["layout"], "{PRINT_LIST}")
                plist = "\n".join("- " + p for p in (a.get("pagePrints") or []))
                labels = ", ".join(vs.get("requiredLabels") or []) or "(etiket yok)"
                extra_r = english_constraints(vs.get("restrictions") or [],
                                              d.get("culture"), cmap)
                body = (tmpl.replace("{PRINT_LIST}", plist)
                        + "\n\nEVERY LABEL BELOW MUST BE LEGIBLE AND SPELLED EXACTLY:\n"
                        + labels
                        + "\n\nCONSTRAINTS:\n"
                        + "\n".join("- " + r for r in extra_r)
                        + "\n\nNEGATIVE: " + "; ".join(NEGATIVE)
                        + "\n\nOUTPUT: PNG, %s, %d×%d px, %s, %d dpi minimum."
                        % (vs.get("colour", "grayscale"), vs["targetPx"][0],
                           vs["targetPx"][1], vs.get("aspect", ""),
                           vs.get("minDpi", 300)))
                L.append("<h4><code>%s</code></h4>" % esc(a["activityId"]))
                L.append("<p class='sub'><span class='tag'>%s</span>"
                         "<span class='tag'>%s</span><span class='tag'>%d×%d</span>"
                         "<span class='tag'>%s</span><span class='tag'>%d etiket</span>"
                         "<code>%s</code></p>"
                         % (esc(vs["visualClass"]), esc(vs["layout"]),
                            vs["targetPx"][0], vs["targetPx"][1],
                            esc(vs.get("aspect", "")),
                            len(vs.get("requiredLabels") or []),
                            esc(vs["filename"])))
                L.append('<div class="prompt" id="p%d">%s'
                         '<button class="copy" data-t="p%d">promptu kopyala</button>'
                         "</div>" % (pidx, esc(body), pidx))
        # aktivite dışı varlıklar
        for a in extra:
            pidx += 1
            tmpl = CLASS_TEMPLATES.get(a.get("assetClass"), "{PRINT_LIST}")
            if a.get("assetClass") == "culture-vignette":
                c = cmap.get(a.get("culture") or "", {})
                plist = ("- the culture's own name, printed once: %s"
                         % ", ".join(a.get("requiredLabels") or []))
            elif a.get("assetClass") == "seal-stamp":
                motif = ""
                for r in regions:
                    if r["id"] == a.get("region"):
                        motif = r.get("sealStampMotif", "")
                plist = ("MOTIF (from region_index, not to be printed as text): %s"
                         % motif) if motif else "PRINT NOTHING."
            else:
                plist = "PRINT NOTHING except what the constraints allow."
            extra_r = english_constraints(a.get("restrictions") or [],
                                          a.get("culture"), cmap)
            body = (tmpl.replace("{PRINT_LIST}", plist)
                    + "\n\nPURPOSE: " + (a.get("purpose") or "")
                    + "\n\nCONSTRAINTS:\n"
                    + "\n".join("- " + r for r in extra_r)
                    + "\n\nNEGATIVE: " + "; ".join(NEGATIVE)
                    + "\n\nOUTPUT: PNG, %s, %d×%d px, %s, %d dpi minimum."
                    % (a.get("colour", "grayscale"),
                       a["targetDimensions"][0], a["targetDimensions"][1],
                       a.get("aspectRatio", ""), a.get("minDpi", 300)))
            L.append("<h4><code>%s</code></h4>" % esc(a["assetId"]))
            L.append("<p class='sub'><span class='tag'>%s</span>"
                     "<span class='tag'>%d×%d</span><span class='tag'>%s</span>"
                     "<code>%s</code></p>"
                     % (esc(a.get("assetClass")), a["targetDimensions"][0],
                        a["targetDimensions"][1], esc(a.get("aspectRatio", "")),
                        esc(a["filename"])))
            L.append('<div class="prompt" id="p%d">%s'
                     '<button class="copy" data-t="p%d">promptu kopyala</button>'
                     "</div>" % (pidx, esc(body), pidx))

    L += ["<h2>%d · Varlık envanteri</h2>" % (7 if populated and inv_full else 6),
          "<p>Her satır bir varlıktır. Envanter <strong>hesaplanır</strong>, "
          "yol haritasının “~150” tahminine yuvarlanmaz.</p>",
          '<div class="scroll"><table>',
          "<tr><th>Sınıf</th><th>Adet</th><th>Kaynak</th></tr>",
          "<tr><td>aktivite görseli</td><td>%d</td><td><code>book.json § visualSpec</code></td></tr>" % len(specs),
          "<tr><td>kültür vinyeti</td><td>%d</td><td><code>culture_index.json</code></td></tr>"
          % sum(1 for a in inv_assets if a.get("assetClass") == "culture-vignette"),
          "<tr><td>mühür damgası</td><td>%d</td><td><code>region_index § sealStampMotif</code></td></tr>"
          % sum(1 for a in inv_assets if a.get("assetClass") == "seal-stamp"),
          "<tr><td>rozet</td><td>%d</td><td><code>DESIGN_SYSTEM § 1 · § 4 · § 7</code></td></tr>"
          % sum(1 for a in inv_assets if a.get("assetClass") == "badge"),
          "<tr><td>ön madde diyagramı</td><td>%d</td><td><code>book.json § frontMatter</code></td></tr>"
          % sum(1 for a in inv_assets if a.get("assetClass") == "front-matter"),
          "<tr><td><strong>toplam</strong></td><td><strong>%d</strong></td><td></td></tr>"
          % len(inv_assets),
          "</table></div>",
          '<div class="scroll"><table>',
          "<tr><th>#</th><th>activity_id</th><th>asset_id</th><th>sınıf / düzen</th>"
          "<th>yön · px · oran</th><th>dosya → hedef</th><th>durum</th></tr>"]
    for n, (_, rid, a, vs, d) in enumerate(specs, 1):
        L.append(
            "<tr><td>%d</td><td><code>%s</code><br><span class='tag'>%s</span></td>"
            "<td><code>%s</code></td><td>%s<br><code>%s</code></td>"
            "<td>%s · %d×%d · %s<br><span class='tag'>%s dpi</span>"
            "<span class='tag'>%s</span></td>"
            "<td><code>%s</code><br><code>%s</code></td>"
            "<td><span class='tag warnchip'>%s</span></td></tr>"
            % (n, esc(a["activityId"]), esc(rid), esc(vs["assetId"]),
               esc(vs["visualClass"]), esc(vs["layout"]),
               esc(vs["orientation"]), vs["targetPx"][0], vs["targetPx"][1],
               esc(vs["aspect"]), esc(vs.get("minDpi", 300)), esc(vs.get("colour", "grayscale")),
               esc(vs["filename"]), esc(vs["destination"]), esc(vs["status"])))
    L.append("</table></div>")

    L += ["<h2>7 · Kültür başına çizim kısıtları</h2>",
          "<p>Bunlar <code>01_SOURCE/culture_index.json § forbiddenForms</code> "
          "alanından gelir ve <strong>public</strong>tir. Bir promptun sonuna, "
          "o sayfanın kültürüne ait olanlar eklenir.</p>",
          '<div class="scroll"><table>',
          "<tr><th>Kültür</th><th>Kademe</th><th>Çizime giremeyecek olan</th></tr>"]
    used = {d.get("culture") for _, _, _, _, d in specs}
    for c in cultures:
        if c["id"] not in used:
            continue
        L.append("<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td></tr>"
                 % (esc(c["name"]), esc(c.get("eligibilityTier", "—")),
                    "<br>".join("· " + esc(f) for f in c.get("forbiddenForms", []))))
    L.append("</table></div>")

    L += ["<h2>8 · Faz 5'e devir</h2>",
          "<ol>",
          "<li>Bir satır seç ve düzen şablonunu kopyala.</li>",
          "<li><code>{PRINT_LIST}</code> yer tutucusunu <strong>manuscript'teki</strong> "
          "<code>pagePrints</code> ile doldur. Bu adım depo dışında yapılır.</li>",
          "<li>Ortak olumsuz kısıtları (§ 3) ekle.</li>",
          "<li>O kültürün çizim kısıtlarını (§ 7) ekle.</li>",
          "<li>Üret, <code>%s</code> hedefine <code>asset_id.png</code> adıyla yaz.</li>"
          % esc(cfg.get("design", {}).get("assetDestination", "07_ASSETS/processed/interior/")),
          "<li><code>asset_inventory.py</code> koştur — envanter ÖLÇÜMDEN ÖNCE koşar, "
          "çünkü yanlış aktiviteye bağlanmış kusursuz bir görsel aktiviteyi "
          "çözülemez yapar.</li>",
          "</ol>",
          '<div class="note stop"><strong>AJAN GÖRSEL ÜRETMEZ.</strong><br>'
          "Faz 3 şartname üretir. Varlık üretimi yol haritasında Faz 5'tir ve "
          "kurucu talimatı olmadan başlamaz.</div>",
          "</div>", SCRIPT, "</body>", "</html>", ""]
    return "\n".join(L)


CSS = """
  :root{ --ink:#1c1a17; --paper:#faf7f1; --rule:#d9d2c5; --muted:#6b6459;
         --warn:#8a3324; --ok:#2f5d3a; --chip:#efe9dc; }
  @media (prefers-color-scheme: dark){
    :root{ --ink:#ece7dd; --paper:#171614; --rule:#3a362f; --muted:#a09889;
           --warn:#e0836f; --ok:#8fc79b; --chip:#26241f; } }
  *{box-sizing:border-box}
  body{margin:0;background:var(--paper);color:var(--ink);
       font:16px/1.6 "Iowan Old Style",Georgia,"Times New Roman",serif;
       padding:2.5rem 1.25rem 6rem;}
  .wrap{max-width:64rem;margin:0 auto}
  h1{font-size:1.9rem;line-height:1.2;margin:0 0 .4rem;letter-spacing:-.01em}
  .sub{color:var(--muted);margin:0 0 2rem;font-size:.95rem}
  h2{font-size:1.25rem;margin:2.75rem 0 .5rem;padding-bottom:.35rem;
     border-bottom:2px solid var(--rule)}
  h3{font-size:1rem;margin:1.75rem 0 .35rem}
  p{margin:.6rem 0}
  .note{background:var(--chip);border-left:3px solid var(--rule);
        padding:.75rem 1rem;margin:1rem 0;font-size:.93rem}
  .stop{border-left-color:var(--warn)}
  .stop strong{color:var(--warn)}
  .chain{background:var(--chip);border:1px dashed var(--rule);border-radius:6px;
         padding:.7rem 1rem;margin:1rem 0;font:14px/1.6 ui-monospace,Menlo,monospace}
  table{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.88rem}
  th,td{text-align:left;padding:.45rem .6rem;border-bottom:1px solid var(--rule);
        vertical-align:top}
  th{font-size:.76rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
  .scroll{overflow-x:auto}
  .prompt{position:relative;background:var(--chip);border:1px solid var(--rule);
          border-radius:6px;padding:.9rem 2.5rem .9rem 1rem;margin:.6rem 0 1.4rem;
          font:13px/1.55 ui-monospace,"SF Mono",Menlo,Consolas,monospace;
          white-space:pre-wrap;word-break:break-word}
  .copy{position:absolute;top:.5rem;right:.5rem;border:1px solid var(--rule);
        background:var(--paper);color:var(--muted);border-radius:4px;
        font:11px/1 ui-monospace,monospace;padding:.35rem .55rem;cursor:pointer}
  .copy:hover{color:var(--ink)}
  .copy.done{color:var(--ok);border-color:var(--ok)}
  code{background:var(--chip);padding:.1rem .3rem;border-radius:3px;font-size:.86em}
  ol,ul{margin:.5rem 0 .5rem 1.2rem;padding:0}
  li{margin:.35rem 0}
  .tag{display:inline-block;background:var(--chip);border:1px solid var(--rule);
       border-radius:999px;padding:.1rem .55rem;font-size:.72rem;color:var(--muted);
       margin-right:.3rem}
  .warnchip{color:var(--warn);border-color:var(--warn)}
"""

SCRIPT = """<script>
document.querySelectorAll('.copy').forEach(function(b){
  b.addEventListener('click', function(){
    var box = document.getElementById(b.dataset.t);
    var text = box.innerText.replace(/kopyala$/, '').trim();
    navigator.clipboard.writeText(text).then(function(){
      b.textContent = 'kopyalandı'; b.classList.add('done');
      setTimeout(function(){ b.textContent = 'kopyala'; b.classList.remove('done'); }, 1600);
    });
  });
});
</script>"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    print("=" * 74)
    print("  GÖRSEL PROMPT KÜTÜPHANESİ")
    print("=" * 74)

    # ⚠ MANUSCRIPT DEPODA DURMAZ (K10) ve kütüphane ondan TÜRER.
    #
    # Manuscript yokken üreteç BOŞ bir kütüphane üretir ve o boş kütüphane
    # takip edilenle elbette tutmaz. Bu bir BAYATLIK değildir: kaynak
    # orada değildir. `asset_manifest.py` aynı gerekçeyle aynı şeyi yapar.
    #
    #     Bir bayatlık denetimi, kaynağın YOKLUĞUNU
    #     bir sürüklenme sanmamalıdır.
    if not os.path.isfile(BOOK):
        print("  ⊘ manuscript depoda yok (K10) — kütüphane üretilemedi, BOŞ KOŞTU")
        print("=" * 74)
        return 0

    want = build(populated=False)

    if args.check:
        # ⚠ YALNIZCA TAKİP EDİLEN SÜRÜM DENETLENİR.
        # Yerel sürüm depoda yoktur ve CI'da hiç üretilmez; onu bayatlık
        # denetimine sokmak, olmayan bir dosyayı KIRMIZI yakmak olurdu.
        cur = ""
        if os.path.isfile(OUT):
            with open(OUT, encoding="utf-8") as fh:
                cur = fh.read()
        if cur != want:
            print("  ✗ BAYAT: %s" % os.path.relpath(OUT, ROOT))
            print("\n  Tazele: ./04_BUILD/image_prompts.py")
            print("=" * 74)
            return 1
        print("  ✅ kütüphane güncel")
        print("=" * 74)
        return 0

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(want)
    print("  yazıldı: %s   (takip edilen · yer tutuculu)"
          % os.path.relpath(OUT, ROOT))

    inv, full = load_assets()
    if inv and full:
        with open(OUT_LOCAL, "w", encoding="utf-8") as fh:
            fh.write(build(populated=True))
        n = len(inv.get("assets", []))
        print("  yazıldı: %s   (yerel · %d DOLU prompt)"
              % (os.path.relpath(OUT_LOCAL, ROOT), n))
        print("\n  ⚠ Yerel sürüm CEVAP TAŞIR ve depoya GİRMEZ (.gitignore § ③d).")
    else:
        print("  ⊘ tam envanter yok — dolu sürüm üretilmedi")
        print("     ./04_BUILD/asset_manifest.py")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
