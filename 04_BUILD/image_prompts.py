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


def build() -> str:
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

    by_layout = collections.Counter(vs["layout"] for _, _, _, vs, _ in specs)
    by_region = collections.Counter(r for _, r, _, _, _ in specs)

    L = ["<!doctype html>", '<html lang="tr">', "<head>", '<meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1">',
         "<title>Görsel Prompt Kütüphanesi — The Myth Hunter's Field Book</title>",
         BANNER, "<style>", CSS, "</style>", "</head>", "<body>", '<div class="wrap">']

    L += [
        "<h1>Görsel Prompt Kütüphanesi</h1>",
        '<p class="sub">The Myth Hunter\'s Field Book · <strong>Faz 3 · şartname katmanı</strong> · '
        "13 Ağustos 2026<br>%d sayfa için görsel şartnamesi · <strong>0 üretilmiş varlık</strong>. "
        "Varlık üretimi <strong>Faz 5</strong>'tir.</p>" % len(specs),

        '<div class="note stop">',
        "<strong>ŞARTNAME BİR VARLIK DEĞİLDİR.</strong><br>",
        "Bu belge %d görselin <em>ne olması gerektiğini</em> söyler. Hiçbiri "
        "üretilmedi ve bu belge üretildiklerini iddia etmez. "
        "<code>BOOK_STATS.md</code> ikisini ayrı satırlarda sayar: "
        "<em>görsel şartnamesi</em> ve <em>görsel varlık</em>." % len(specs),
        "</div>",

        '<div class="note stop">',
        "<strong>BU BELGE CEVAP TAŞIMAZ — VE TAŞIYAMAZ (karar K10).</strong><br>",
        "Her sayfanın basacağı şeylerin tam listesi (<code>pagePrints</code>) "
        "<em>cevabın kendisidir</em>: <em>“the chilli basket drawn empty”</em> bir "
        "şartnamedir <strong>ve aynı zamanda cevaptır</strong>. Bu yüzden promptlar "
        "<code>{PRINT_LIST}</code> yer tutucusuyla durur. Faz 5'te promptu üreten "
        "kişi yer tutucuyu <strong>elindeki manuscript'ten</strong> doldurur; "
        "public depo dolu hâlini hiçbir zaman görmez.",
        "</div>",

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
        L.append("<tr><td>%s <span class='tag'>%s</span></td><td>%d</td>"
                 "<td><strong>0</strong></td></tr>" % (esc(rname.get(rid, rid)), esc(rid), n))
    L.append("<tr><td><strong>toplam</strong></td><td><strong>%d</strong></td>"
             "<td><strong>0</strong></td></tr>" % len(specs))
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

    L += ["<h2>6 · Sayfa şartnameleri</h2>",
          "<p>Her satır bir varlıktır. <code>PRINT_LIST</code> sütunu bilerek "
          "<strong>boştur</strong>: içeriği manuscript'te durur ve depoya girmez.</p>",
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

    want = build()
    if args.check:
        cur = ""
        if os.path.isfile(OUT):
            with open(OUT, encoding="utf-8") as fh:
                cur = fh.read()
        print("=" * 74)
        print("  GÖRSEL PROMPT KÜTÜPHANESİ")
        print("=" * 74)
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
    print("yazıldı: %s" % os.path.relpath(OUT, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
