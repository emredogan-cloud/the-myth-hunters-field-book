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

# ═══════════════════════════════════════════════════════════════════════════
# FAZ 6+ · NİHAİ KDP VARLIKLARI — kapak · A+ · iki eksik levha
# ═══════════════════════════════════════════════════════════════════════════
#
# ⭑ BU BÖLÜM SONA EKLENİR VE ÖNCEKİ HİÇBİR ŞEYİ SİLMEZ ⭑
#
# Kütüphanenin § 1–8'i iç bloğun şartname katmanıdır ve Faz 5'te
# donduruldu. Yükleme öncesi geçiş üç yeni varlık sınıfı istiyor ve
# üçü de iç blok DEĞİLDİR:
#
#     KAPAK   → renkli · 300 dpi · tek PDF · sarmal (arka+sırt+ön)
#     A+      → renkli · pazarlama · Amazon modül ölçüleri
#     EKSİK   → iç blok · gri tonlama · 150 dpi (K39) · iki levha
#
# Üçünün ORTAK kuralı tektir ve § 4'ün aynısıdır:
#
#     GÖRSELE METİN GÖMÜLMEZ. Tipografi dizgi katmanında basılır.
#
# Kapakta bu kural bir üslup tercihi değil bir ZORUNLULUKTUR: bir
# üretecin yazdığı başlık düzeltilemez, KDP metadata'sıyla harfi harfine
# eşleşmez ve gömülü bir yazım hatası kapağı yeniden ürettirir.

# Kapak sanatı — iki seçenek. Metin YOK; tipografi CLI katmanında.
COVER_OPTIONS = [
    {
        "id": "kdp-cover-option-01",
        "title": "SEÇENEK 1 — “SAHA MASASI”",
        "purpose": ("Kitabı bir OYUN kitabı gibi değil, bir SAHA ARACI gibi "
                    "gösterir. Alıcı ebeveyn/öğretmen; sinyal: ciddi, "
                    "araştırmaya dayalı, ekransız."),
        "concept": (
            "A premium editorial illustration for the wrap-around cover of an "
            "illustrated non-fiction activity book for children aged 8 to 12.\n\n"
            "SUBJECT — an open field notebook resting on a working map table, "
            "viewed from slightly above. Arranged around it as a researcher "
            "would leave them at the end of a day: a folded regional map "
            "carrying faint pencil routes; a hand-inked compass rose on loose "
            "paper; a coastline study on tracing paper; small observation "
            "objects grouped as natural-history specimens (a shell, a seed "
            "head, a stone with a worn mark, a length of knotted cord); and a "
            "row of small EMPTY wax seal impressions pressed along one edge of "
            "the table.\n\n"
            "The notebook pages are ruled and gridded surfaces with pencil "
            "shading and measuring marks — but they carry NO readable writing "
            "and NO letterforms of any kind.\n\n"
            "STYLE — premium illustrated publishing art. Classic expedition "
            "field journal crossed with modern museum education design. Hand-"
            "drawn ink linework over flat painted colour. Not fantasy art, not "
            "cartoon, not anime, not photorealistic, not a games-box "
            "illustration.\n\n"
            "COLOUR — rich but restrained and natural: parchment, warm ochre, "
            "deep indigo blue, muted forest green, stone grey, iron-gall ink "
            "accents. No neon, no plastic toy palette, no heavy gradients.\n\n"
            "LIGHT — soft editorial studio light from the upper left, gentle "
            "contact shadows, no dramatic rim light and no glow.\n\n"
            "COMPOSITION — one strong focal object (the open notebook) with a "
            "clear silhouette that reads at thumbnail size. Detail density "
            "falls off toward the edges so the wrap survives cropping."),
        "cultureNote": (
            "Cultural material must be SPECIFIC and restrained. Objects may "
            "suggest observation and craft — a measuring cord, a plain woven "
            "mat edge, a carved wooden rule. They may NOT be sacred, "
            "ceremonial or restricted objects, and they may NOT be blended "
            "into a generic ‘exotic’ ornamental pattern. Invented scripts, "
            "invented symbols and invented ‘tribal’ motifs are forbidden."),
    },
    {
        "id": "kdp-cover-option-02",
        "title": "SEÇENEK 2 — “MİT HARİTASI PANOSU”",
        "purpose": ("Kitabın kapsamını tek bakışta verir: altı bölge, bir "
                    "dünya. Sinyal: keşif, rota, kapsam."),
        "concept": (
            "A premium cinematic illustration for the wrap-around cover of an "
            "illustrated non-fiction activity book for children aged 8 to 12.\n\n"
            "SUBJECT — a large hand-drawn explorer's field board: a single "
            "continuous map-like landscape that links six distinct geographic "
            "zones across one surface — sea ice and low winter light; a warm "
            "inland sea with terraced coast; open savanna with high grass and "
            "a broad river; mountain ridges under monsoon cloud; open ocean "
            "with island chains and a star-path; and high cloud forest above "
            "terraced slopes.\n\n"
            "Pinned and tucked across the board: route threads between zones, "
            "small blank observation cards, a knotted measuring cord, a "
            "sounding line, pale coastline overlays on tracing paper, and six "
            "small EMPTY seal impressions marking the six zones.\n\n"
            "The board carries pencil marks, route lines and measuring ticks — "
            "but NO readable writing, NO letterforms, NO numerals and NO "
            "invented script anywhere.\n\n"
            "STYLE — premium illustrated publishing art plus modern museum "
            "education plus classic expedition cartography. Ink linework over "
            "flat painted colour, visible paper texture.\n\n"
            "COLOUR — parchment ground with deep indigo sea, muted green, warm "
            "ochre, stone and iron-gall ink. Restrained and natural.\n\n"
            "COMPOSITION — readable at thumbnail size; the six zones must be "
            "distinguishable as separate places, not as one blended texture. "
            "Full-bleed wrap composition with the visual weight held toward "
            "the centre of each panel."),
        "cultureNote": (
            "Cultural references must be specific, restrained, educational and "
            "respectful. No sacred or ceremonial object. No stereotyped "
            "‘tribal’ world. No skulls, no weapons, no treasure chests, no "
            "glowing mystical symbols, no fake writing systems, no generic "
            "pirate treasure map."),
    },
]

# Kapak için ORTAK olumsuz kısıtlar — iç blok listesinden AYRIDIR.
# İç blok gri tonlama ve çizgi sanatıdır; kapak renklidir. İki listeyi
# birleştirmek kapağı yanlışlıkla siyah-beyaz ürettirir.
COVER_NEGATIVE = [
    "NO TEXT of any kind anywhere in the image",
    "no title, no subtitle, no author name, no publisher name",
    "no badge wording, no sticker wording, no award wording",
    "no ISBN, no barcode, no price, no age-range block",
    "no typography, no lettering, no numerals, no calligraphy",
    "no invented script, no fake writing, no rune-like or glyph-like marks",
    "no logo, no watermark, no signature, no AI artefact mark",
    "no readable writing on any notebook page, card, map or label",
    "no sacred, ceremonial or restricted object",
    "no generic ‘tribal’ ornament and no blended pan-cultural pattern",
    "no weapon, no wound, no blood, no skull",
    "no photorealistic human face; no identifiable real person",
    "no modern branding, clothing, device or packaging",
    "no neon, no plastic toy palette, no lens flare, no bokeh",
    "no heavy vignette and no dark frame around the edges",
]

# A+ modül seti — pazarlama katmanı. İç blok kısıtları BURAYA UYGULANMAZ.
#
# ⚠ A+ GÖRSELİ BİR MANUSCRIPT SAYFASI DEĞİLDİR ve bu ayrım mekanik bir
# sonuç doğurur: A+ görselinde CEVAP, MÜHÜR SÖZCÜĞÜ ve ÇÖZÜM GÖSTERİLEMEZ.
# Bir pazarlama görselinde sızdırılan bir cevap, kitabın içindekinden
# DAHA GENİŞ yayılır: ürün sayfası herkese açıktır.
APLUS_MODULES = [
    {
        "id": "aplus-01-hero", "module": "Standard Image & Text Overlay",
        "name": "HERO / KİTAP FİKRİ", "shape": "banner", "count": 1,
        "purpose": ("Tek cümlelik vaat: bu bir mitoloji temalı bulmaca kitabı "
                    "değil, gerçek kültürlerden türetilmiş bir saha görevi."),
        "scene": (
            "A wide banner scene: the closed field book lying on a working "
            "desk beside a folded map, a pencil, a measuring cord and three "
            "small EMPTY seal impressions. Shot slightly from above, calm and "
            "premium, like a publisher's key visual."),
        "safeArea": ("Sol %45 SAKİN kalır — Amazon overlay metni oraya biner. "
                     "Odak nesne sağ %55'te durur."),
    },
    {
        "id": "aplus-02-what-children-do", "module": "Standard Three Image & Text",
        "name": "ÇOCUK NE YAPIYOR", "shape": "square", "count": 3,
        "purpose": ("Eylemi gösterir: çöz · çiz · yaz. Üç kare, üç FARKLI eylem; "
                    "aynı sahnenin üç açısı DEĞİL."),
        "scene": (
            "Three separate square scenes, one per image, each showing a "
            "child's hands only (no face) at a table:\n"
            "  (a) a pencil resting on an open ruled page mid-working;\n"
            "  (b) a pair of hands laying out small blank paper cards in a row;\n"
            "  (c) a hand pressing a small stamp beside a row of empty seal "
            "impressions.\n"
            "Same desk, same light, same palette across all three so they read "
            "as one set."),
        "safeArea": ("Kare görselin altına Amazon başlık+gövde metni gelir; "
                     "görselin kendi alt %15'i sakin kalır."),
    },
    {
        "id": "aplus-03-six-regions", "module": "Standard Image Header with Text",
        "name": "ALTI BÖLGE", "shape": "banner", "count": 1,
        "purpose": "Kapsamı gösterir: altı bölge, yirmi iki halk, tek görev.",
        "scene": (
            "A wide banner strip showing six distinct landscape vignettes in a "
            "single horizontal band, separated by thin ruled dividers: sea ice; "
            "warm inland sea coast; open savanna and river; monsoon mountain "
            "ridge; open ocean with island chain; high cloud-forest terraces. "
            "Each vignette carries one small EMPTY seal impression beneath it. "
            "Consistent palette and horizon line across all six."),
        "safeArea": ("Üst %30 sakin bir gökyüzü/parşömen bandı olarak boş "
                     "bırakılır — modül başlığı oraya biner."),
    },
    {
        "id": "aplus-04-real-cultures", "module": "Standard Single Image & Sidebar",
        "name": "GERÇEK KÜLTÜRLER / ARAŞTIRMA", "shape": "square", "count": 1,
        "purpose": ("Farklılaştırıcı: cevaplar müze, arşiv ve üniversite "
                    "kaynaklarıyla denetlendi. Sinyal: güvenilirlik."),
        "scene": (
            "A square still life of research materials on a desk: a stack of "
            "reference volumes seen edge-on with blank spines, an archive "
            "folder, a magnifier resting on a printed plate of abstract "
            "geometric marks (NOT letters), a card index box with blank cards, "
            "and a pair of cotton handling gloves. Quiet, scholarly, warm."),
        "safeArea": ("Sağ %35 sidebar metnine komşudur; kompozisyon SOLA "
                     "yaslanır ve sağ kenar sakin kalır."),
    },
    {
        "id": "aplus-05-screen-free", "module": "Standard Four Image & Text",
        "name": "EKRANSIZ DENEYİM", "shape": "square", "count": 4,
        "purpose": ("Satın alma gerekçesi: masa başı, ekransız, tek malzeme "
                    "bir kurşun kalem."),
        "scene": (
            "Four separate square scenes, one per image, all on the same table "
            "in the same light:\n"
            "  (a) the closed book and one sharpened pencil, nothing else;\n"
            "  (b) an open page with a partly ruled working area and a pencil "
            "laid across it;\n"
            "  (c) a small kit group: pencil, eraser, a short ruler, a length "
            "of plain cord;\n"
            "  (d) the book propped closed at the end of a session beside a "
            "cooling cup and a switched-off lamp.\n"
            "No screen, no phone, no tablet appears in any of the four."),
        "safeArea": "Her karenin alt %15'i metin için sakin kalır.",
    },
    {
        "id": "aplus-06-maps-and-codes", "module": "Standard Single Left Image",
        "name": "HARİTA · KOD · GÖZLEM", "shape": "square", "count": 1,
        "purpose": ("Aktivite TÜRLERİNİ gösterir: harita, şifre anahtarı, "
                    "gözlem levhası, sıralama kartları — cevap göstermeden."),
        "scene": (
            "A square overhead composition of four page-like sheets fanned "
            "across a desk, each representing one kind of work: an outline "
            "coast map with a pencil route; a ruled key panel whose cells are "
            "EMPTY; an observation plate of a plain object with blank pointer "
            "lines; and a set of blank rectangular cards each carrying an empty "
            "square number box. Every cell, line and box is EMPTY."),
        "safeArea": ("Görsel modülün SOL yarısında durur; sağ kenar metne "
                     "komşudur ve sakin kalır."),
    },
    {
        "id": "aplus-07-completion", "module": "Standard Image & Text Overlay",
        "name": "BİTİRME / SAHA YOLCULUĞU", "shape": "banner", "count": 1,
        "purpose": ("Tamamlama vaadi: altı mühür, bir sertifika, bitirilmiş "
                    "bir kitap. Sinyal: bu kitap BİTİRİLİR."),
        "scene": (
            "A wide banner: the finished book closed on a desk at the end of "
            "the journey, with a completed row of six pressed seal impressions "
            "beside it and a blank certificate card resting under one corner. "
            "The seals are pressed and textured but carry NO letters. Warm low "
            "evening light, a sense of an expedition completed."),
        "safeArea": ("Sağ %45 SAKİN kalır — overlay metni oraya biner. Odak "
                     "sol %55'te durur."),
    },
]

APLUS_NEGATIVE = [
    "NO TEXT of any kind baked into the image",
    "no headline, no body copy, no bullet text, no callout label",
    "no title, no author name, no publisher name, no imprint",
    "no badge, sticker, ribbon, star rating or award wording",
    "no price, no ISBN, no barcode, no age-range block",
    "no logo, no watermark, no signature",
    "no readable writing on any page, card, map, spine or label",
    "no invented script and no fake writing",
    "no puzzle solution, no answer, no completed working, no seal letter",
    "no screen, phone, tablet, laptop or television",
    "no identifiable child's face; hands only where a person appears",
    "no stock-photo look, no lens flare, no heavy bokeh",
    "no neon and no plastic toy palette",
]

# İki eksik iç blok levhası. Bunlar KAPAK/A+ değil, İÇ BLOKTUR:
# gri tonlama · çizgi sanatı · 150 dpi ölçütü (K39) · § 3'ün olumsuz listesi.
MISSING_ASSETS = [
    {
        "activityId": "yoruba-underdot-letters",
        "assetId": "fig-yoruba-underdot-letters",
        "why": (
            "Bu sayfanın bütün iddiası TEK BİR İŞARETTİR: harfin ALTINDAKİ "
            "nokta. Bir üretecin uydurduğu ya da kaydırdığı bir nokta, sayfayı "
            "çözülemez yapar VE bir yazı sistemi hakkında yanlış bilgi basar."),
        "typeset": (
            "⭑ GLİFLER ÜRETEÇTEN GELMEZ ⭑\n\n"
            "The Yorùbá letterforms are NOT generated by the image model. The "
            "model produces the PLATE ONLY: rules, boxes, cells, panels and "
            "writing lines. Every letter cell is left EMPTY and the CLI "
            "typography layer sets the real glyphs afterwards in an embedded "
            "font.\n\n"
            "Reason: an image model cannot be trusted to place a combining "
            "dot-below reliably, and on this page the dot IS the content. A "
            "hallucinated, shifted or missing dot does not make the plate "
            "slightly wrong — it makes the page unsolvable and the linguistic "
            "claim false."),
    },
    {
        "activityId": "korean-river-crossing-sort",
        "assetId": "fig-korean-river-crossing-sort",
        "why": (
            "Bu sayfanın cevabı bir SIRADIR. Levhaya eklenen dekoratif bir "
            "nesne yeni bir olası cevap üretir; suya konan tek bir hayvan ise "
            "cevabı doğrudan basar."),
        "typeset": (
            "⭑ KART METNİ ÜRETEÇTEN GELMEZ ⭑\n\n"
            "The card sentences are NOT generated by the image model. The model "
            "produces the PLATE ONLY: the river, the two banks, the empty card "
            "rectangles, the empty square number boxes and the writing line. "
            "Each card is left EMPTY and the CLI typography layer sets the "
            "card text afterwards in an embedded font.\n\n"
            "Reason: the order of the cards is the answer. Text placed by the "
            "generator cannot be guaranteed to sit in a shuffled order, and a "
            "card that lands in its own numbered position hands the answer to "
            "the reader."),
    },
]

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


def cover_geometry():
    """Kapak ölçüsünü ÖLÇÜLMÜŞ metadata'dan okur — elle yazmaz.

    ⭑ SIRT GENİŞLİĞİ BU DOSYADA HESAPLANMAZ ⭑

    `metadata.py` sırtı sayfa sayısından türetiyor ve `COVER_SPEC.md`'yi
    o yazıyor. Aynı sayıyı burada ikinci kez hesaplamak, bir gün
    ikisinin ayrışması demektir — ve ayrıştığı gün kapak YANLIŞ SIRTLA
    basılır. Tek kaynak: `06_REPORTS/tracked/metadata.json`.
    """
    md = jload(os.path.join(ROOT, "06_REPORTS", "tracked", "metadata.json"))
    if not md:
        return None
    cv, ed = md.get("cover") or {}, md.get("edition") or {}
    try:
        tw, th = (float(x) for x in re.findall(r"[\d.]+", ed.get("trim", ""))[:2])
    except ValueError:
        return None
    bleed = cv["bleedInches"]
    g = {
        "pages": ed.get("pages"),
        "trimW": tw, "trimH": th,
        "spine": cv["spineInches"],
        "fullW": cv["fullCoverWidthInches"],
        "fullH": cv["fullCoverHeightInches"],
        "bleed": bleed,
        "safe": cv["safeMarginInches"],
        "spineText": cv.get("spineTextAllowed"),
        # Panel eni = trim + DIŞ kenar bleed'i. İç kenar sırta bakar ve
        # bleed almaz: orada kâğıt kesilmez, katlanır.
        "panelW": round(tw + bleed, 4),
        "panelH": round(th + 2 * bleed, 4),
    }
    # ⭑ PANELLER TOPLAMI SARMALA BİREBİR EŞİT OLMAK ZORUNDA ⭑
    #
    # Her ölçüyü ayrı ayrı yuvarlamak 1 px açık bırakıyordu:
    #     2588 + 108 + 2588 = 5284   ama sarmal 5283
    # Bir piksel bir hata gibi görünmez — ta ki birleştirici üç paneli yan
    # yana koyup tuvalin dışına taşana kadar. Panel enleri bu yüzden
    # HESAPLANMAZ, sarmaldan ÇIKARILIR: toplam her zaman tutar.
    g["fullPx"] = int(round(g["fullW"] * 300))
    g["fullPxH"] = int(round(g["fullH"] * 300))
    g["panelPxH"] = g["fullPxH"]
    g["spinePx"] = int(round(g["spine"] * 300))
    g["backPx"] = (g["fullPx"] - g["spinePx"]) // 2
    g["frontPx"] = g["fullPx"] - g["spinePx"] - g["backPx"]
    g["panelPx"] = g["frontPx"]
    assert g["backPx"] + g["spinePx"] + g["frontPx"] == g["fullPx"]
    return g


def missing_prompt_body(spec, book_act, populated):
    """İki eksik levhanın promptu.

    ⚠ TAKİP EDİLEN SÜRÜM `pagePrints` VE `requiredLabels` TAŞIMAZ (K10).
    § 6'nın yaptığı ayrımın aynısı: yer tutucu takip edilene, dolu hâl
    yalnızca yerele girer. Bu iki sayfada kural DAHA da bağlayıcı —
    yoruba'nın etiket listesi cevabın kendisidir."""
    vs = (book_act or {}).get("visualSpec") or {}
    if populated and book_act:
        plist = "\n".join("- " + p for p in (book_act.get("pagePrints") or []))
        labels = ", ".join(vs.get("requiredLabels") or []) or "(etiket yok)"
    else:
        plist = "{PRINT_LIST}"
        labels = "{REQUIRED_LABELS}"
    return (
        "Black ink line drawing on white, technical field-guide style, no "
        "shading, no colour. A PLATE for one page of a children's activity "
        "book.\n\n"
        + spec["typeset"] + "\n\n"
        "THE PLATE MUST PRINT THE FOLLOWING FURNITURE, AND NOTHING ELSE:\n"
        + plist + "\n\n"
        "EVERY CELL LISTED BELOW IS RESERVED AS AN EMPTY, CORRECTLY SIZED BOX. "
        "The generator leaves it blank; the typography layer fills it:\n"
        + labels)


def kdp_final_section(populated, book, cmap, inv_by_id):
    """§ 9 — NİHAİ KDP: kapak · A+ · iki eksik levha.

    Bölüm kütüphanenin SONUNA eklenir. § 1–8 iç bloğun donmuş şartname
    katmanıdır ve bu geçiş onlara dokunmaz."""
    g = cover_geometry()
    acts = {a["activityId"]: a for a in (book or {}).get("activities", [])}
    L, pid = [], 900

    L += ["<h2>9 · NİHAİ KDP — KAPAK · A+ · EKSİK VARLIK PROMPTLARI</h2>",
          '<div class="note stop">',
          "<strong>BU BÖLÜM SONA EKLENDİ VE ÜSTÜNDEKİ HİÇBİR ŞEYİ SİLMEDİ.</strong><br>",
          "§ 1–8 iç bloğun <strong>donmuş</strong> şartname katmanıdır. Bu bölüm "
          "yükleme öncesi geçişte doğdu ve üç yeni varlık sınıfı taşır: "
          "<strong>kapak sanatı</strong>, <strong>A+ pazarlama görselleri</strong> "
          "ve <strong>iki eksik iç blok levhası</strong>.",
          "</div>",
          '<div class="note stop">',
          "<strong>ÜÇÜNÜN DE ORTAK KURALI: GÖRSELDE METİN YOK.</strong><br>",
          "Başlık, yazar adı, alt başlık, rozet yazısı, ISBN, barkod, fiyat, "
          "yaş bandı ve <em>her türlü harf</em> görselin DIŞINDADIR. Tipografi "
          "CLI katmanında, gömülü yazı tipiyle basılır.<br><br>"
          "Gerekçe § 4'ün aynısıdır ve kapakta daha da bağlayıcıdır: "
          "<strong>bir üretecin yazdığı başlık düzeltilemez, KDP "
          "metadata'sıyla harfi harfine eşleşmez ve gömülü bir yazım hatası "
          "bütün kapağı yeniden ürettirir.</strong>",
          "</div>"]

    # ── 9.1 kapak geometrisi ──────────────────────────────────────────────
    L += ["<h3>9.1 · Kapak geometrisi — <em>ölçümden türetilir, elle yazılmaz</em></h3>"]
    if not g:
        L += ['<div class="note stop"><strong>KAPAK GEOMETRİSİ OKUNAMADI.</strong><br>'
              "<code>06_REPORTS/tracked/metadata.json</code> yok. "
              "<code>./04_BUILD/metadata.py</code> koşturun.</div>"]
    else:
        L += ["<p>Bütün ölçüler <code>metadata.json § cover</code>'dan gelir ve o "
              "da <strong>ölçülen sayfa sayısından</strong> türer. Sayfa sayısı "
              "değişirse bu tablo kendiliğinden değişir — sırt hiçbir yerde "
              "elle yazılmaz.</p>",
              '<div class="scroll"><table>',
              "<tr><th>Ölçü</th><th>inç</th><th>piksel @300 dpi</th></tr>",
              "<tr><td><strong>Tam sarmal</strong> (arka+sırt+ön, bleed dâhil)</td>"
              "<td>%.4f × %.4f</td><td><strong>%d × %d</strong></td></tr>"
              % (g["fullW"], g["fullH"], g["fullPx"], g["fullPxH"]),
              "<tr><td>Arka panel (bleed dâhil) — <em>soldaki</em></td>"
              "<td>%.4f × %.4f</td><td>%d × %d</td></tr>"
              % (g["panelW"], g["panelH"], g["backPx"], g["panelPxH"]),
              "<tr><td><strong>Sırt</strong> (%s sayfa)</td><td>%.4f × %.4f</td>"
              "<td>%d × %d</td></tr>"
              % (g["pages"], g["spine"], g["panelH"], g["spinePx"], g["panelPxH"]),
              "<tr><td>Ön panel (bleed dâhil) — <em>sağdaki</em></td>"
              "<td>%.4f × %.4f</td><td>%d × %d</td></tr>"
              % (g["panelW"], g["panelH"], g["frontPx"], g["panelPxH"]),
              "<tr><td><em>toplam denetimi</em></td><td>—</td>"
              "<td><em>%d + %d + %d = %d</em> ✓</td></tr>"
              % (g["backPx"], g["spinePx"], g["frontPx"], g["fullPx"]),
              "<tr><td>Trim</td><td>%.2f × %.2f</td><td>—</td></tr>"
              % (g["trimW"], g["trimH"]),
              "<tr><td>Bleed · güvenli kenar</td><td>%.3f · %.2f</td><td>—</td></tr>"
              % (g["bleed"], g["safe"]),
              "<tr><td>Sırta yazı basılabilir mi</td><td colspan='2'>%s</td></tr>"
              % ("EVET" if g["spineText"] else "HAYIR"),
              "</table></div>",
              '<div class="note stop">',
              "<strong>BU TABLO BİR TEYİT DEĞİL, BİR BAŞLANGIÇTIR.</strong><br>",
              "Nihai geometri <strong>KDP kapak şablonundan</strong> alınır: "
              "kurucu son sayfa sayısıyla şablonu indirir, CLI barkod kutusunu "
              "ve katlama payını <em>şablondan okur</em>. Hiçbir koordinat elle "
              "yazılmaz.<br><br>"
              "⚠ Sayfa sayısı yeniden üretimde değişirse <strong>sırt da "
              "değişir</strong> ve kapak yeniden dizilir.",
              "</div>"]

    # ── 9.2 · kapak promptları ────────────────────────────────────────────
    for i, co in enumerate(COVER_OPTIONS, 1):
        pid += 1
        px = ("%d × %d px" % (g["fullPx"], g["fullPxH"])) if g else "(geometri yok)"
        inch = ("%.4f × %.4f in" % (g["fullW"], g["fullH"])) if g else "—"
        ratio = ("%.4f : 1" % (g["fullW"] / g["fullH"])) if g else "—"
        L += ["<h3>9.2.%d · KAPAK SANATI — %s</h3>" % (i, esc(co["title"])),
              '<div class="scroll"><table>',
              "<tr><td><strong>Amaç</strong></td><td>%s</td></tr>" % esc(co["purpose"]),
              "<tr><td><strong>Varlık kimliği</strong></td><td><code>%s</code></td></tr>"
              % esc(co["id"]),
              "<tr><td><strong>Dosya adı</strong></td><td><code>%s.png</code></td></tr>"
              % esc(co["id"]),
              "<tr><td><strong>HAM konum</strong></td>"
              "<td><code>07_ASSETS/raw/%s.png</code> · <em>teslimden sonra "
              "DEĞİŞTİRİLMEZ</em></td></tr>" % esc(co["id"]),
              "<tr><td><strong>Nihai hedef</strong></td>"
              "<td><code>08_OUTPUT/PAPERBACK/cover.pdf</code> — tek PDF: "
              "arka + sırt + ön</td></tr>",
              "<tr><td><strong>Hedef ölçü</strong></td><td>%s &nbsp;(%s)</td></tr>"
              % (px, inch),
              "<tr><td><strong>En-boy oranı</strong></td><td>%s · yatay sarmal</td></tr>"
              % ratio,
              "<tr><td><strong>Renk · çözünürlük</strong></td>"
              "<td>RGB renkli · <strong>gerçek 300 dpi</strong> "
              "(iç bloğun 150 dpi ölçütü kapağa UYGULANMAZ)</td></tr>",
              "<tr><td><strong>CLI sonradan basacak</strong></td>"
              "<td>ön: başlık + yazar · sırt: başlık + yazar · arka: tanıtım "
              "metni, yaş bandı, ekransız sinyali, yazar biyografisi · "
              "barkod alanı BOŞ</td></tr>",
              "</table></div>"]
        body = (co["concept"]
                + "\n\nCULTURAL CONSTRAINT:\n" + co["cultureNote"]
                + "\n\nTYPOGRAPHY RESERVE — leave these zones visually calm and "
                  "uncluttered so type can be set over them later, but place NO "
                  "text in them:\n"
                  "- FRONT PANEL upper third: title zone\n"
                  "- FRONT PANEL lower sixth: author zone\n"
                  "- SPINE band, full height: title and author zone\n"
                  "- BACK PANEL centre: blurb zone\n"
                  "- BACK PANEL lower outer corner: a clear 2.0 × 1.2 in "
                  "barcode block, light and empty\n"
                + "\n\nNEGATIVE: " + "; ".join(COVER_NEGATIVE)
                + ("\n\nOUTPUT: PNG, RGB colour, %d × %d px, %s, full-bleed "
                   "wrap, 300 dpi at %.4f × %.4f in."
                   % (g["fullPx"], g["fullPxH"], ratio, g["fullW"], g["fullH"])
                   if g else "\n\nOUTPUT: PNG, RGB colour, highest native "
                             "resolution available."))
        L += ['<div class="prompt" id="p%d">%s'
              '<button class="copy" data-t="p%d">promptu kopyala</button></div>'
              % (pid, esc(body), pid)]

    L += ['<div class="note stop">',
          "<strong>TEK BİR ÜRETEÇ 300 dpi SARMALI ÜRETEMEZ — VE BU GİZLENMEZ."
          "</strong><br>",
          "%s piksel, yaygın üreteçlerin tek karede verdiğinin çok üstündedir. "
          "İki dürüst yol vardır:<br>"
          "① <strong>Panel panel üretim:</strong> ön ve arka panel AYRI "
          "üretilir (her biri %s px), sırt CLI'da düz renk/doku olarak "
          "kurulur; CLI üçünü tek tuvalde birleştirir.<br>"
          "② <strong>Yerel yeniden çizim:</strong> üreteç maksimum kendi "
          "çözünürlüğünde üretir, CLI onu 300 dpi tuvale <em>gerçek</em> "
          "büyütmeyle taşır ve <strong>kaynak dpi'ı rapora yazar</strong>.<br><br>"
          "⛔ <strong>Yapılmayacak olan:</strong> pikseli değiştirmeden yalnızca "
          "DPI etiketini 300 yazmak. Etiket çözünürlük değildir."
          % (("%d × %d" % (g["fullPx"], g["fullPxH"])) if g else "Gereken",
             ("%d × %d" % (g["panelPx"], g["panelPxH"])) if g else "panel ölçüsü"),
          "</div>"]

    # ── 9.3 · A+ modül seti ───────────────────────────────────────────────
    total_imgs = sum(m["count"] for m in APLUS_MODULES)
    L += ["<h3>9.3 · A+ İÇERİK MODÜL SETİ — %d modül · %d görsel</h3>"
          % (len(APLUS_MODULES), total_imgs),
          '<div class="note stop">',
          "<strong>A+ GÖRSELİ BİR MANUSCRIPT SAYFASI DEĞİLDİR.</strong><br>",
          "Ürün sayfası herkese açıktır: burada sızdırılan bir cevap, kitabın "
          "içindekinden <strong>daha geniş</strong> yayılır. Hiçbir A+ görseli "
          "cevap, çözülmüş bir sayfa, mühür harfi veya yıldız sözcüğü "
          "gösteremez. Bütün hücreler, kutular ve mühürler <strong>BOŞ</strong> "
          "çizilir.",
          "</div>",
          '<div class="note">',
          "<strong>METİN AMAZON'DA, GÖRSELDE DEĞİL.</strong><br>",
          "Amazon <em>Image &amp; Text Overlay</em> modüllerinde arka plan "
          "görseline metin eklenmemesini açıkça tavsiye ediyor: metin modülün "
          "kendi alanına girer, böylece dil ve kopya görsel yeniden "
          "üretilmeden değiştirilebilir. Her modülün <strong>metin-güvenli "
          "alanı</strong> aşağıda ayrıca yazılıdır.",
          "</div>",
          '<div class="scroll"><table>',
          "<tr><th>#</th><th>Modül</th><th>Amaç</th><th>Görsel</th>"
          "<th>Ölçü</th><th>Dosya</th></tr>"]
    for n, m in enumerate(APLUS_MODULES, 1):
        if m["shape"] == "banner":
            dim, note = "1940 × 600 px", "min kabul alanı 970 × 300"
        else:
            dim, note = "600 × 600 px", "kare · min 220 × 220"
        names = (("%s.png" % m["id"]) if m["count"] == 1
                 else "%s-01…%02d.png" % (m["id"], m["count"]))
        L.append("<tr><td>%d</td><td><strong>%s</strong><br>"
                 "<span class='tag'>%s</span></td><td>%s</td>"
                 "<td>%d</td><td>%s<br><span class='tag'>%s</span></td>"
                 "<td><code>%s</code></td></tr>"
                 % (n, esc(m["name"]), esc(m["module"]), esc(m["purpose"]),
                    m["count"], dim, esc(note), esc(names)))
    L += ["</table></div>",
          '<div class="note">',
          "<strong>HAM konum:</strong> <code>07_ASSETS/raw/aplus/</code> · "
          "<strong>nihai hedef:</strong> <code>08_OUTPUT/APLUS/</code> · "
          "<strong>dosya boyutu:</strong> her nihai görsel <strong>&lt; 3 MB</strong>."
          "<br>⚠ KDP paneli bir A+ belgesine eklenebilecek modül sayısını "
          "sınırlar. Kurucu paneldeki güncel sınırı görür ve bu setten "
          "yukarıdan aşağıya seçer; sıralama <strong>öncelik sırasıdır</strong>.",
          "</div>"]

    for m in APLUS_MODULES:
        pid += 1
        if m["shape"] == "banner":
            w, h, ar = 1940, 600, "97:30 (geniş banner)"
            minarea = "970 × 300 px kabul edilen asgari görsel alan"
        else:
            w, h, ar = 600, 600, "1:1 (kare)"
            minarea = "220 × 220 px kabul edilen asgari görsel alan"
        L += ["<h4><code>%s</code> — %s</h4>" % (esc(m["id"]), esc(m["name"])),
              "<p class='sub'><span class='tag'>%s</span>"
              "<span class='tag'>%d × %d</span><span class='tag'>%s</span>"
              "<span class='tag'>%d görsel</span></p>"
              % (esc(m["module"]), w, h, esc(ar), m["count"])]
        body = (
            "A premium marketing image for the Amazon A+ Content page of an "
            "illustrated non-fiction activity book for children aged 8 to 12.\n\n"
            "⭑ THIS IMAGE MUST CONTAIN NO TEXT. The copy is supplied separately "
            "through the Amazon module overlay.\n\n"
            "MODULE: " + m["module"] + "\n"
            "PURPOSE: " + m["purpose"] + "\n\n"
            "SCENE:\n" + m["scene"] + "\n\n"
            "TEXT-SAFE AREA (leave visually calm, but place NO text there):\n"
            + m["safeArea"] + "\n\n"
            "VISUAL SYSTEM — all A+ images share one look so the page reads as "
            "a single product presentation: warm parchment and desk-wood "
            "ground, deep indigo and muted green accents, soft editorial studio "
            "light from the upper left, shallow contact shadows, matte paper "
            "texture. Photographic-illustrative hybrid, premium publishing "
            "quality. No two modules repeat the same composition.\n\n"
            "VISUAL HIERARCHY — one dominant object, one supporting group, one "
            "quiet ground. Nothing competes with the reserved text area.\n\n"
            "BACKGROUND — even, low-contrast and uncluttered behind the "
            "reserved text zone; detail is concentrated in the focal area.\n\n"
            "NEGATIVE: " + "; ".join(APLUS_NEGATIVE) + "\n\n"
            "OUTPUT: PNG or JPEG, RGB colour, %d × %d px (%s), %s, final file "
            "under 3 MB." % (w, h, ar, minarea))
        L += ['<div class="prompt" id="p%d">%s'
              '<button class="copy" data-t="p%d">promptu kopyala</button></div>'
              % (pid, esc(body), pid)]

    # ── 9.4 · iki eksik levha ─────────────────────────────────────────────
    L += ["<h3>9.4 · EKSİK İÇ BLOK VARLIKLARI — iki levha</h3>",
          '<div class="note stop">',
          "<strong>BU İKİSİ BASIMA GİREMEZ.</strong><br>",
          "Şu an iki sayfada <em>çapraz taramalı</em>, üzerinde "
          "<code>art not supplied — do not print</code> yazan dürüst yer "
          "tutucular duruyor. Yer tutucu sanat değildir ve öyle olduğunu "
          "iddia etmiyor — ama <strong>basıma girerse kitabı bozar</strong>.",
          "</div>",
          '<div class="note stop">',
          "<strong>BU İKİSİ KAPAK VE A+ DEĞİL, İÇ BLOKTUR.</strong><br>",
          "Kural takımı § 3'ün olumsuz listesi + § 7'nin kültürel kısıtlarıdır: "
          "<strong>gri tonlama · siyah çizgi · gölgesiz · 150 dpi ölçütü "
          "(K39)</strong>. Kapağın renkli/300 dpi kuralı buraya "
          "<em>uygulanmaz</em>.",
          "</div>"]
    for spec in MISSING_ASSETS:
        pid += 1
        a = acts.get(spec["activityId"])
        vs = (a or {}).get("visualSpec") or {}
        inv = inv_by_id.get(spec["assetId"], {})
        tpx = vs.get("targetPx") or inv.get("targetDimensions") or [0, 0]
        dpi = vs.get("minDpi", inv.get("minDpi", 150))
        phys = ("%.2f × %.2f in" % (tpx[0] / dpi, tpx[1] / dpi)) if dpi else "—"
        L += ["<h4><code>%s</code></h4>" % esc(spec["activityId"]),
              '<div class="scroll"><table>',
              "<tr><td><strong>Amaç</strong></td><td>%s</td></tr>"
              % esc(vs.get("purpose") or inv.get("purpose") or "—"),
              "<tr><td><strong>Neden bu sayfa hassas</strong></td><td>%s</td></tr>"
              % esc(spec["why"]),
              "<tr><td><strong>Varlık kimliği</strong></td><td><code>%s</code></td></tr>"
              % esc(spec["assetId"]),
              "<tr><td><strong>Dosya adı</strong></td><td><code>%s</code></td></tr>"
              % esc(vs.get("filename") or inv.get("filename") or "—"),
              "<tr><td><strong>HAM konum</strong></td><td><code>%s</code><br>"
              "<em>⚠ şu an YER TUTUCU duruyor; hat onu "
              "<code>07_ASSETS/rejected/</code> altına arşivler, ÜZERİNE "
              "YAZMAZ</em></td></tr>" % esc(inv.get("rawLocation") or "—"),
              "<tr><td><strong>Nihai hedef</strong></td><td><code>%s</code></td></tr>"
              % esc(inv.get("finalLocation") or "—"),
              "<tr><td><strong>Hedef ölçü</strong></td>"
              "<td>%d × %d px · %s @ %s dpi</td></tr>"
              % (tpx[0], tpx[1], phys, dpi),
              "<tr><td><strong>En-boy oranı · yön</strong></td><td>%s · %s</td></tr>"
              % (esc(vs.get("aspect") or inv.get("aspectRatio") or "—"),
                 esc(vs.get("orientation") or inv.get("orientation") or "—")),
              "<tr><td><strong>Renk · düzen</strong></td>"
              "<td>%s · <code>%s</code></td></tr>"
              % (esc(vs.get("colour", "grayscale")), esc(vs.get("layout") or "—")),
              "<tr><td><strong>CLI sonradan basacak</strong></td>"
              "<td>bütün glifler / kart metni / etiketler — gömülü yazı "
              "tipiyle, üreteçten DEĞİL</td></tr>",
              "</table></div>"]
        extra_r = english_constraints(
            vs.get("restrictions") or inv.get("restrictions") or [],
            (jload(ACTS, {}) or {}).get("activities") and next(
                (d.get("culture") for d in (jload(ACTS, {}) or {})
                 .get("activities", []) if d.get("activityId")
                 == spec["activityId"]), None), cmap)
        body = (missing_prompt_body(spec, a, populated)
                + "\n\nCONSTRAINTS:\n"
                + "\n".join("- " + r for r in extra_r)
                + "\n\nNEGATIVE: " + "; ".join(NEGATIVE)
                + "\n\nOUTPUT: PNG, %s, %d × %d px, %s, %s dpi minimum."
                % (vs.get("colour", "grayscale"), tpx[0], tpx[1],
                   vs.get("aspect", ""), dpi))
        L += ['<div class="prompt" id="p%d">%s'
              '<button class="copy" data-t="p%d">promptu kopyala</button></div>'
              % (pid, esc(body), pid)]

    if not populated:
        L += ['<div class="note stop">',
              "<strong>YUKARIDAKİ İKİ PROMPT YER TUTUCULUDUR (K10).</strong><br>",
              "<code>{PRINT_LIST}</code> ve <code>{REQUIRED_LABELS}</code> "
              "cevabın kendisini taşır — <code>yoruba</code>'nın etiket listesi "
              "<em>tam olarak</em> çocuğun yazacağı şeydir. Dolu hâl yalnızca "
              "<code>IMAGE_PROMPT_LIBRARY.local.html</code> dosyasındadır ve o "
              "dosya depoya girmez.",
              "</div>"]

    # ── 9.5 · teslim tablosu ──────────────────────────────────────────────
    L += ["<h3>9.5 · Kurucunun üreteceği dosyalar — tam liste</h3>",
          "<p>Ayrıntılı teslim sözleşmesi: "
          "<code>07_ASSETS/FOUNDER_ASSET_DELIVERY.md</code>.</p>",
          '<div class="scroll"><table>',
          "<tr><th>Sınıf</th><th>Dosya</th><th>Ölçü</th><th>HAM konum</th>"
          "<th>Nihai hedef</th></tr>"]
    for co in COVER_OPTIONS:
        L.append("<tr><td>kapak</td><td><code>%s.png</code></td><td>%s</td>"
                 "<td><code>07_ASSETS/raw/</code></td>"
                 "<td><code>08_OUTPUT/PAPERBACK/cover.pdf</code></td></tr>"
                 % (esc(co["id"]),
                    ("%d × %d" % (g["fullPx"], g["fullPxH"])) if g else "—"))
    for m in APLUS_MODULES:
        dim = "1940 × 600" if m["shape"] == "banner" else "600 × 600"
        names = (("%s.png" % m["id"]) if m["count"] == 1
                 else "%s-01…%02d.png" % (m["id"], m["count"]))
        L.append("<tr><td>A+</td><td><code>%s</code></td><td>%s</td>"
                 "<td><code>07_ASSETS/raw/aplus/</code></td>"
                 "<td><code>08_OUTPUT/APLUS/</code></td></tr>"
                 % (esc(names), dim))
    for spec in MISSING_ASSETS:
        inv = inv_by_id.get(spec["assetId"], {})
        vs = (acts.get(spec["activityId"]) or {}).get("visualSpec") or {}
        tpx = vs.get("targetPx") or inv.get("targetDimensions") or [0, 0]
        L.append("<tr><td>iç blok</td><td><code>%s</code></td><td>%d × %d</td>"
                 "<td><code>07_ASSETS/raw/</code></td><td><code>%s</code></td></tr>"
                 % (esc(inv.get("filename") or spec["assetId"] + ".png"),
                    tpx[0], tpx[1], esc(inv.get("finalLocation") or "—")))
    L += ["</table></div>",
          '<div class="note stop">',
          "<strong>AJAN GÖRSEL ÜRETMEZ — VE BU BÖLÜM DE ÜRETMEZ.</strong><br>",
          "Bu bölüm yalnızca <em>ne üretileceğini</em> ve <em>nereye "
          "konacağını</em> yazar. Ham üretim kurucuya aittir. Hat, kurucu "
          "<strong>DEVAM</strong> diyene kadar çalıştırılmaz.",
          "</div>"]
    return L


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
          "kurucu talimatı olmadan başlamaz.</div>"]

    # ── § 9 — YÜKLEME ÖNCESİ GEÇİŞ · SONA EKLENİR ─────────────────────────
    # Bölüm en sona girer ve § 1–8'e dokunmaz: iç bloğun şartname katmanı
    # Faz 5'te donduruldu, bu geçiş onun ÜSTÜNE yazar, YERİNE değil.
    L += kdp_final_section(populated, book, cmap, by_id)

    L += ["</div>", SCRIPT, "</body>", "</html>", ""]
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
