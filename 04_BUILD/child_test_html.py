#!/usr/bin/env python3
"""
ETKİLEŞİMLİ ÇOCUK TESTİ ÜRETECİ — The Myth Hunter's Field Book
================================================================================
`01_SOURCE/pilot_tr/interactive_child_test.html` **elle yazılmaz**;
`source-tr.json`'dan ÜRETİLİR (karar K17).

⭑ BU DOSYANIN NE OLDUĞU — VE NE OLMADIĞI ⭑

    Bu bir TEST ARACIDIR.
    Bir TEST SONUCU DEĞİLDİR.

Aracı üretmek, testi yapmak değildir. Faz 2 bu ayrımı bir kez kurdu ve
proje beş fazdır onu koruyor:

    PAKET ÜRETMEK, TEST YAPMAK DEĞİLDİR.  (DECISIONS § A10)

Bu betik `tester-pack-tr.txt`in ekran karşılığını üretir. Kâğıt paket
zaten vardı; bu, aynı on altı sayfayı bir çocuğun önüne **ekranda**
koyar ve yanına gözlemcinin kaydını alacağı bir panel ekler.

⭑ A10 NE ZAMAN KAPANIR ⭑

A10 bu dosya ÜRETİLDİĞİNDE kapanmaz. A10 şu olduğunda kapanır:

    gerçek bir çocuk  +  gerçek bir oturum  +  kaydedilmiş sonuç

Dosyanın kendisi bunu ekranda da söyler ve kapanış ekranı bir
**oturum kaydı** üretir: gözlemci onu indirir, kurucu projeye verir,
`CHILD_TEST_LOG.md` gerçek sayılarla dolar ve `externalValidation`
ancak o zaman değişir.

⚠ DOSYA DEPOYA GİRMEZ. Türkçedir (K21 · ticari dil değil), sayfa
prozası taşır (K11) ve CEVAP taşır (K10). `01_SOURCE/pilot_tr/`
`.gitignore § ①d` ile dışlanmıştır.

⚠ ÇOCUK CEVAPLARI GÖRMEZ. Cevaplar yalnızca gözlemci panelinde ve
yalnızca gözlemci "cevabı göster" dediğinde açılır.

  ./04_BUILD/child_test_html.py            üret
  ./04_BUILD/child_test_html.py --check    bayatsa KIRMIZI

TASARIM: yalnızca Python standart kütüphanesi (karar K7).

Çıkış kodları:  0 = güncel/yazıldı   1 = BAYAT   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SRC = os.path.join(ROOT, "01_SOURCE", "pilot_tr", "source-tr.json")
OUT = os.path.join(ROOT, "01_SOURCE", "pilot_tr", "interactive_child_test.html")
BANNER = "<!-- ÜRETİLMİŞTİR — 04_BUILD/child_test_html.py · ELLE DÜZENLEMEYİN -->"


def esc(s):
    return html.escape(str(s or ""), quote=True)


CSS = """
:root{--ink:#1d1b18;--paper:#fbf8f2;--rule:#ddd6c8;--muted:#6d6559;
      --warn:#8a3324;--ok:#2f5d3a;--chip:#f0eade;--accent:#2c4a6e}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
     font:17px/1.65 "Iowan Old Style",Georgia,serif}
.wrap{max-width:56rem;margin:0 auto;padding:1.5rem 1.1rem 5rem}
h1{font-size:1.6rem;margin:.2rem 0 .3rem}
h2{font-size:1.15rem;margin:1.6rem 0 .4rem}
.sub{color:var(--muted);font-size:.92rem;margin:0 0 1.2rem}
.stop{background:#fdf3f1;border-left:4px solid var(--warn);padding:.85rem 1rem;
      margin:1rem 0;font-size:.93rem}
.stop b{color:var(--warn)}
.note{background:var(--chip);border-left:4px solid var(--rule);
      padding:.8rem 1rem;margin:1rem 0;font-size:.92rem}
.card{background:#fff;border:1px solid var(--rule);border-radius:10px;
      padding:1.2rem 1.3rem;margin:1rem 0;box-shadow:0 1px 2px rgba(0,0,0,.04)}
.mission{font-weight:700;font-size:1.12rem;margin:0 0 .5rem}
ol.steps{margin:.4rem 0 .8rem 1.2rem;padding:0}
ol.steps li{margin:.35rem 0}
.plate{background:var(--chip);border:1px dashed var(--rule);border-radius:8px;
       padding:.85rem 1rem;margin:.7rem 0;font-size:.93rem}
.plate ul{margin:.3rem 0 0 1.1rem;padding:0}
.write{margin:.8rem 0}
.write input{width:100%;padding:.55rem .7rem;font:16px/1.4 inherit;
             border:1px solid var(--rule);border-radius:6px;background:#fff}
.starbox{display:flex;gap:.3rem;align-items:center;flex-wrap:wrap;margin:.6rem 0}
.starbox input{width:2.1rem;height:2.5rem;text-align:center;font-size:1.15rem;
               border:1px solid var(--ink);border-radius:5px;text-transform:uppercase}
.starbox .tag{font-size:.8rem;color:var(--muted);margin-left:.4rem}
.fn{border-top:1px solid var(--rule);margin-top:1rem;padding-top:.7rem;
    font-size:.9rem;color:var(--muted)}
.nav{display:flex;gap:.6rem;justify-content:space-between;margin:1.2rem 0}
button{font:15px/1 inherit;padding:.65rem 1.1rem;border-radius:7px;
       border:1px solid var(--rule);background:#fff;cursor:pointer}
button.primary{background:var(--accent);color:#fff;border-color:var(--accent)}
button:disabled{opacity:.4;cursor:not-allowed}
.obs{background:#f4f7fb;border:1px solid #c9d8ea;border-radius:10px;
     padding:1rem 1.15rem;margin:1.1rem 0}
.obs h3{margin:.1rem 0 .6rem;font-size:1rem;color:var(--accent)}
.obs label{display:block;margin:.55rem 0 .2rem;font-size:.88rem;font-weight:600}
.obs textarea{width:100%;min-height:3.2rem;padding:.5rem;font:14px/1.45 inherit;
              border:1px solid var(--rule);border-radius:6px}
.radio{display:flex;gap:1.1rem;flex-wrap:wrap;margin:.2rem 0}
.radio label{font-weight:400;font-size:.9rem;display:flex;gap:.35rem;
             align-items:center;margin:0}
.reveal{margin-top:.7rem;font-size:.9rem}
.reveal summary{cursor:pointer;color:var(--warn);font-weight:600}
.reveal .ans{background:#fdf3f1;border-radius:6px;padding:.6rem .8rem;
             margin-top:.4rem;font-family:ui-monospace,Menlo,monospace;font-size:.85rem}
.prog{height:5px;background:var(--rule);border-radius:3px;overflow:hidden;margin:.5rem 0 1rem}
.prog i{display:block;height:100%;background:var(--accent);width:0;transition:width .25s}
.pill{display:inline-block;background:var(--chip);border:1px solid var(--rule);
      border-radius:999px;padding:.1rem .6rem;font-size:.75rem;color:var(--muted)}
#done pre{background:var(--chip);padding:.9rem;border-radius:8px;overflow-x:auto;
          font-size:.78rem;white-space:pre-wrap}
@media print{.obs,.nav,button{display:none}}
"""


def build() -> str:
    with open(SRC, encoding="utf-8") as fh:
        d = json.load(fh)
    acts = d.get("activities", [])
    op = d.get("regionOpening", {})

    L = ["<!doctype html>", '<html lang="tr">', "<head>", '<meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1">',
         "<title>Saha Defteri — Çocuk Testi (Türkçe pilot)</title>",
         BANNER, "<style>", CSS, "</style>", "</head>", "<body>", '<div class="wrap">']

    L += [
        "<h1>Saha Defteri — çocuk testi</h1>",
        '<p class="sub">Türkçe pilot · <strong>%d sayfa</strong> · bölge: %s</p>'
        % (len(acts), esc(op.get("heading", ""))),

        '<div class="stop">',
        "<b>BU BİR TEST ARACIDIR, BİR TEST SONUCU DEĞİLDİR.</b><br>",
        "Bu dosyayı açmak bir test yapmaz. Test, <strong>gerçek bir çocuk</strong> "
        "on altı sayfayı <strong>tek başına</strong> denediğinde ve gözlemci ne "
        "olduğunu yazdığında yapılmış olur.",
        "</div>",

        '<div class="note">',
        "<strong>Gözlemciye — üç kural:</strong>",
        "<ol>",
        "<li><strong>Sayfada yazanı okumayın, açıklamayın.</strong> Çocuk yalnızca "
        "sayfadaki metni okur. Bir yetişkin “ne demek istediğini” anlatırsa o sayfa "
        "<em>geçersizdir</em> ve kayda “açıklandı” diye geçer.</li>",
        "<li><strong>Çocuk takılırsa bekleyin.</strong> Takılma bir sonuçtur, bir "
        "başarısızlık değil. Suç çocukta değil talimattadır.</li>",
        "<li><strong>Yanlış cevabı düzeltmeyin.</strong> Yanlış cevap, sayfanın "
        "nerede belirsiz olduğunu söyleyen en değerli veridir.</li>",
        "</ol>",
        "</div>",

        '<div class="card">',
        "<h2>%s</h2>" % esc(op.get("heading", "")),
        '<p class="sub">%s</p>' % esc(op.get("terrainLine", "")),
        "<p>%s</p>" % esc(op.get("openingText", "")),
        "</div>",

        '<div class="obs">',
        "<h3>Oturum bilgisi</h3>",
        '<label>Testçi kimliği (yalnızca <code>tester-01</code> biçiminde — GERÇEK AD YAZMAYIN)</label>',
        '<input id="tester" placeholder="tester-01" style="width:100%;padding:.5rem;'
        'border:1px solid var(--rule);border-radius:6px">',
        '<label>Yaş</label>',
        '<input id="age" type="number" min="6" max="14" placeholder="9" '
        'style="width:6rem;padding:.5rem;border:1px solid var(--rule);border-radius:6px">',
        '<label>Tarih</label>',
        '<input id="date" type="date" style="padding:.5rem;border:1px solid var(--rule);border-radius:6px">',
        "</div>",
        '<div class="prog"><i id="bar"></i></div>',
    ]

    for i, a in enumerate(acts, 1):
        aid = a.get("activityId", "")
        star_n = len(a.get("sealStarWord") or "")
        L += ['<section class="card act" data-i="%d" id="a%d">' % (i, i),
              '<span class="pill">sayfa %d / %d</span> '
              '<span class="pill">%s</span>' % (i, len(acts), esc(aid)),
              '<p class="mission">%s</p>' % esc(a.get("prompt"))]

        prints = a.get("pagePrints") or []
        if prints:
            L.append('<div class="plate"><strong>Sayfada basılı olanlar:</strong><ul>')
            for p in prints:
                L.append("<li>%s</li>" % esc(p))
            L.append("</ul></div>")
        else:
            L.append('<div class="plate"><em>Bu sayfanın levhası basılı '
                     'kâğıt pakettedir (<code>tester-pack-tr.txt</code>). '
                     'Ekranda yalnızca görev ve adımlar vardır.</em></div>')

        L.append("<ol class='steps'>")
        for st in a.get("steps") or []:
            L.append("<li>%s</li>" % esc(st))
        L.append("</ol>")

        lines = a.get("writingSpaceLines") or 3
        L.append('<div class="write">')
        for k in range(min(lines, 8)):
            L.append('<input class="ans" data-a="%s" placeholder="…">' % esc(aid))
        L.append("</div>")

        if star_n:
            L.append('<div class="starbox">')
            for k in range(star_n):
                L.append('<input maxlength="1" class="star" data-a="%s">' % esc(aid))
            L.append('<span class="tag">★%s → mühür yuvası %s</span>'
                     % (esc(a.get("sealStarIndex")), esc(a.get("sealSlot"))))
            L.append("</div>")

        if a.get("fieldNote"):
            L.append('<div class="fn"><strong>Saha notu:</strong> %s</div>'
                     % esc(a["fieldNote"]))

        # ── GÖZLEMCİ PANELİ — çocuk bunu doldurmaz ────────────────────────
        L += ['<div class="obs">',
              "<h3>Gözlemci — bu sayfa</h3>",
              "<label>Çocuk sayfayı <strong>yardımsız</strong> anladı mı?</label>",
              '<div class="radio">',
              '<label><input type="radio" name="u%d" value="evet"> evet</label>' % i,
              '<label><input type="radio" name="u%d" value="takildi"> takıldı, sonra çözdü</label>' % i,
              '<label><input type="radio" name="u%d" value="aciklandi"> açıklamak gerekti</label>' % i,
              '<label><input type="radio" name="u%d" value="birakti"> bıraktı</label>' % i,
              "</div>",
              "<label>Nerede takıldı, ne dedi? (birebir yazın)</label>",
              '<textarea data-obs="%d"></textarea>' % i,
              "</div>"]

        if a.get("answer"):
            L += ['<details class="reveal"><summary>Cevabı göster (yalnızca '
                  'gözlemci · çocuğa göstermeyin)</summary>',
                  '<div class="ans">%s</div></details>' % esc(a["answer"])]

        L.append("</section>")

    L += [
        '<section class="card" id="done">',
        "<h2>Oturumu bitir</h2>",
        "<p>Aşağıdaki düğme bir <strong>oturum kaydı</strong> üretir. Onu kurucuya "
        "verin: <code>CHILD_TEST_LOG.md</code> bu kayıtla dolar ve "
        "<code>externalValidation</code> ancak o zaman değişir.</p>",
        '<div class="stop"><b>Gerçek ad, okul, adres, fotoğraf veya ses '
        'yazmayın.</b> Kayda yalnızca <code>tester-01</code> biçiminde anonim '
        'kimlik, yaş ve sonuç girer.</div>',
        '<button class="primary" id="export">Oturum kaydını üret</button> ',
        '<button id="copy">Panoya kopyala</button>',
        "<pre id=\"out\" hidden></pre>",
        "</section>",
        "</div>",
        "<script>",
        "const N=%d;" % len(acts),
        "const IDS=%s;" % json.dumps([a.get("activityId") for a in acts],
                                     ensure_ascii=False),
        """
function prog(){
  let done=0;
  for(let i=1;i<=N;i++){ if(document.querySelector('input[name="u'+i+'"]:checked')) done++; }
  document.getElementById('bar').style.width=(done/N*100)+'%';
}
document.addEventListener('change',prog);
function record(){
  const rows=[];
  for(let i=1;i<=N;i++){
    const r=document.querySelector('input[name="u'+i+'"]:checked');
    const o=document.querySelector('textarea[data-obs="'+i+'"]');
    rows.push({page:i, activityId:IDS[i-1],
               unaided:r?r.value:null, note:o?o.value.trim():''});
  }
  const done=rows.filter(r=>r.unaided).length;
  const ok=rows.filter(r=>r.unaided==='evet').length;
  return {
    kind:'child-test-session',
    warning:'BU KAYIT GERCEK BIR OTURUMDAN GELMEDIYSE PROJEYE GIRMEZ.',
    tester:(document.getElementById('tester').value||'').trim(),
    age:(document.getElementById('age').value||'').trim(),
    date:(document.getElementById('date').value||'').trim(),
    language:'tr', material:'01_SOURCE/pilot_tr/source-tr.json',
    pagesTotal:N, pagesObserved:done, unaidedYes:ok,
    unaidedRate: done? Math.round(ok/done*100)+'%' : null,
    pages:rows
  };
}
document.getElementById('export').onclick=()=>{
  const el=document.getElementById('out');
  el.hidden=false; el.textContent=JSON.stringify(record(),null,2);
  el.scrollIntoView({behavior:'smooth'});
};
document.getElementById('copy').onclick=async()=>{
  await navigator.clipboard.writeText(JSON.stringify(record(),null,2));
  const b=document.getElementById('copy'); b.textContent='kopyalandı';
  setTimeout(()=>b.textContent='Panoya kopyala',1500);
};
""",
        "</script>", "</body>", "</html>", ""]
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    print("=" * 74)
    print("  ETKİLEŞİMLİ ÇOCUK TESTİ")
    print("=" * 74)

    if not os.path.isfile(SRC):
        # Türkçe pilot depoda durmaz (K21 · .gitignore § ①d).
        print("  ⊘ Türkçe pilot bu makinede yok — BOŞ KOŞTU")
        print("=" * 74)
        return 0

    want = build()
    if args.check:
        cur = ""
        if os.path.isfile(OUT):
            with open(OUT, encoding="utf-8") as fh:
                cur = fh.read()
        if cur != want:
            print("  ✗ BAYAT: %s" % os.path.relpath(OUT, ROOT))
            print("=" * 74)
            return 1
        print("  ✅ güncel")
        print("=" * 74)
        return 0

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(want)
    print("  yazıldı: %s" % os.path.relpath(OUT, ROOT))
    print()
    print("  ⚠ BU BİR TEST ARACIDIR, BİR TEST SONUCU DEĞİLDİR.")
    print("     A10 ancak GERÇEK bir çocuk GERÇEK bir oturumu bitirdiğinde")
    print("     ve kayıt CHILD_TEST_LOG.md'ye girdiğinde kapanır.")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
