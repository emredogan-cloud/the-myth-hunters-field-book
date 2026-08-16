# YAZI TİPLERİ — gömülür, depoya girmez

`.ttf` dosyaları `.gitignore § ④` ile dışlanır; bu dizinde depoda
yalnızca bu README ve `.gitkeep` durur.

## Hangi yazı tipi ve NEDEN

| Dosya | Nerede |
|---|---|
| `DejaVuSans.ttf` | iç blok gövde · levha dizgisi |
| `DejaVuSans-Bold.ttf` | başlık · görev satırı |
| `DejaVuSans-Oblique.ttf` | field note · künye |
| `DejaVuSerif.ttf` · `-Bold.ttf` | kapak tipografisi |

## ⭑ NEDEN BASE-14 DEĞİL ⭑

Faz 6 iç bloğu `Helvetica` ile dizdi. Ölçüldü ve iki ayrı kusur çıktı:

```
pdffonts interior.pdf
  Helvetica       Type 1   WinAnsi   emb=no
  Helvetica-Bold  Type 1   WinAnsi   emb=no
  ZapfDingbats    Type 1   ...       emb=no
```

**① Hiçbir yazı tipi GÖMÜLÜ DEĞİLDİ.** KDP ciltsiz iç bloğu bütün yazı
tiplerinin gömülü olmasını ister. Gömülmemiş bir yazı tipi, basımevinin
kendi ikamesiyle basılır ve sayfa kayabilir.

**② WinAnsi kodlaması kitabın kendi imlâsını TAŞIYAMIYORDU.** Faz 5'in
`A13` düzeltmesi on dört ad geçişine işaret ekledi — `Yorùbá`,
`Òṣun-Òṣogbo`, `Skíðblaðnir`, `Mjölnir`, `Cú Chulainn`, `Whangārei`.
Bu kod noktaları WinAnsi'de **yoktur** ve dizgide düştü:

```
basılan:  M■ori          ← ön maddede, imlâ kuralını ÖĞRETEN sayfada
```

> ### Bir kitabın *"işaretler önemlidir"* diyen sayfası, işareti basamıyordu.

DejaVu Sans Latin Genişletilmiş Ek'i (U+1E00–U+1EFF) ve `★` (U+2605)
kapsar; `qa_pdf § ②` artık her koşuda gömülülüğü ölçer.

## Lisans

DejaVu Fonts — Bitstream Vera lisansı türevi, serbest dağıtım ve
gömme izinli. Kaynak: `fonts-dejavu-core` (Debian/Ubuntu).
