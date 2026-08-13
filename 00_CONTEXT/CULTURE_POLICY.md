# KÜLTÜR POLİTİKASI — hangi kültür hangi biçimde aktiviteye girer

> Bu belge Faz 1'de doğdu ve bu projenin **ikinci en özgün parçasıdır**
> (birincisi devralma mimarisi).
>
> Sürüm 1.0 · 13 Ağustos 2026 · `01_SOURCE/culture_index.json` bunu uygular
> · `qa_age.py` ve `validate_research.py` mekanik olarak denetler

---

## 1 · Sorulan soru

World Myths 22 kültürü **anlatı için** taradı ve kilitledi. O tarama orada
doğrudur ve burada **yeniden yapılmaz**.

Ama burada başka bir soru sorulur:

> ### Bir geleneği anlatmak ile onu yaptırmak aynı şey değildir.

Bir yetişkin referans cildinde bir gelenek **anlatılır**. Bir çocuk aktivite
kitabında aynı gelenek **yaptırılır**: çizdirilir, çözdürülür, deftere
yazdırılır, bazen taklit ettirilir.

Yaşayan bir topluluğun kutsal anlatısını bir bulmacaya çevirmek, onu
anlatmaktan **kategorik olarak farklıdır**. Bu yüzden Field Book'un eşiği
kaynak projeninkinden **daha serttir** ve tarama burada **yeniden** yapılır —
ama aynı sorularla değil.

---

## 2 · Kültür düşürülmez, biçim daralır

`22` alt başlıkta yazan **doğrulanabilir bir vaattir**. Bir kültürü düşürmek
alt başlığı değiştirir ve bu bir kurucu kararıdır.

Bu yüzden kısıt bulunduğunda **daralma sırası** şudur:

```
① forbiddenForms büyür      → o biçim kapanır, kültür kalır
② allowedTypes daralır      → o aktivite tipi kapanır
③ activityQuota düşer       → kültür daha az aktivite taşır
④ hikâye aktivite DIŞI kalır → kültür başka hikâyesiyle temsil edilir
⑤ kültür düşer              → SON ÇARE · kurucu kararı · alt başlık değişir
```

Faz 1'de ①–④ kullanıldı. **⑤ hiç kullanılmadı.**

---

## 3 · Üç kademe

Kademe, kaynak projenin üç alanından **mekanik olarak türetilir** ve elle
yazılmaz — `04_BUILD/import_from_world_myths.py § activity_usage_for_culture`:

| Girdi | Nereden |
|---|---|
| `restrictionRisk` | World Myths kısıt taraması |
| `livingTradition` | World Myths kültür kaydı |
| `restrictionAssessment` | World Myths kısıt taraması |

```
restrictionRisk == high                              → KADEME C
restrictionRisk == medium  veya
  (livingTradition ve restrictionAssessment==partial) → KADEME B
livingTradition                                       → KADEME A · atıf zorunlu
aksi hâlde                                            → KADEME A
```

### Kademe A — beş tip açık
Yaşayan gelenekte **atıf zorunludur**; kültürün adı sayfada geçer.

**13 kültür:** Yunan · İskandinav · İrlanda · Fin · Mısır · Mezopotamya ·
Kore · Çin · Türk · Fars · Akan · Vietnam · Zulu

### Kademe B — beş tip açık, kutsal katman cevap olamaz
Atıf zorunlu. Ritüel veya kehanet katmanı bir bulmacanın **cevabı** olamaz.

**5 kültür:** Japon · Maya · Aztek · And · Yoruba

### Kademe C — biçim kısıtlı
`observe` · `map` · `sort` · `make` açık.
`cipher` **yalnızca** kamuya açık yazı sistemi ve imlâ üzerinden
(Inuktitut hecelemesi · Devanagari · makron · ʻokina) — kutsal ad veya
ritüel sözcük üzerinden **asla**.
Her aktivite atıf **ve** ebeveyn notu taşır.

**4 kültür:** İnuit · Māori · Hawaii · Hindu

> **Kademe C bir dışlama değildir.** Bu dört kültür kitapta vardır, adıyla
> anılır ve toplam **14 aktivite** taşır. Kısıtlanan **kültür** değil,
> ondan türetilebilecek **görev biçimidir**.

---

## 4 · Şifreler neden gerçek yazı sistemleridir

Karar K4 bir üslup kuralı değil bir **kapsam kuralıdır**: bulmaca içerikten
türer, süslenmez. Bunun kültürel güvenlikte doğrudan bir karşılığı vardır:

| ❌ Kapalı bilgiyi "çözdürmek" | ✅ Kamuya açık yazıyı öğretmek |
|---|---|
| Ifá kehanet şekillerini bulmaca yapmak | Yoruba imlâsındaki alt noktayı öğretmek |
| Mantrayı şifre çözdürmek | Devanagari harflerini tanıtmak |
| Whakapapa'yı cevap yapmak | Makronun ünlü uzunluğunu göstermesi |
| Tonalpohualli'yi falcılık aracı yapmak | Nahuatl yer adı gliflerini okutmak |

Sağ sütun **okulda öğretilen**, yayımlanmış, topluluğun kendisinin de
öğrettiği malzemedir. Sol sütun bir topluluğa aittir ve **bulmaca olamaz**.

22 kültürün **hepsinin** sağ sütunda bir karşılığı vardır —
`culture_index.json § writingSystem`. Bu tesadüf değil, seçim ölçütüdür.

---

## 5 · Hikâye düzeyinde dışlama

Kısıt her zaman kültür düzeyinde değildir. İki hikâye **aktivite dışı**
bırakıldı; kültürleri kalmaya devam ediyor:

| Hikâye | Neden aktivite dışı |
|---|---|
| `story-egyptian-horus-seth` | Kaynak anlatı cinsel saldırı içeren bir bölüm taşıyor. Anlatı katmanında ele alınabilir; bir **görev** çocuğu kaynağa yönlendirir. |
| `story-hindu-ganesha-head` | Anlatının çekirdeği bir başın kesilmesi ve kaynakta yaş incelemesi `pending`. Bir çocuk aktivite kitabında bu, *"çocuğum için fazla karanlık"* yorumunun tarifidir. |

Her iki kültür de **iki kullanılabilir hikâyeyle** temsil edilmeye devam
ediyor. Vaat kırılmadı.

Ayrıca **20 hikâyede kapalı katman** işaretlendi: hikâye kalır, o bölüm
aktiviteye çevrilemez (`IMPORT_MANIFEST.json § forbiddenLayer`).

---

## 6 · Tek hikâyeli iki kültür — açık risk

| Kültür | Kullanılabilir hikâye | Kota | Risk |
|---|---|---|---|
| Zulu | 1 | 4 | Dört aktivite tek anlatıdan türerse **tekrar gibi okunur** |
| And | 1 | 3 | Aynı risk |

**Azaltma:** bu iki kültürün aktiviteleri hikâyeden değil, ağırlıklı olarak
**kültür kaydından** türetilir — dil (isiZulu şıklamaları), notasyon (khipu),
coğrafya (harita noktası). Hikâye yalnızca **bir** aktiviteye kaynaklık eder.

Bu, `qa_echo` (Faz 3) tarafından ayrıca ölçülecek bir risktir ve
`PHASE_1_REPORT.md § açık riskler` içinde kayıtlıdır.

---

## 7 · Aktiviteye çevrilemeyen altı şey

`AGE_POLICY.md § 2`'nin altı yasak çerçevesi kültürel tarafta şöyle okunur:

1. **Kutsal ritüelin taklidi** — hula, haka, gut, puja, jesa, harae, karakia
2. **Kapalı bilginin "çözülmesi"** — Ifá, I Ching, tonalpohualli, whakapapa
3. **Karikatürleştirme** — "kızılderili şefi", "Afrika kabilesi", "yerli büyücü"
4. **Şiddetin sahnelenmesi** — öldürme, parçalama, işkence sahnelerinin çizdirilmesi
5. **Evden çıkma** — bu kitap masada çözülür
6. **Kesici alet, ateş, yiyecek** — kalem ve silgi yeter

> Şüphe her zaman **daha sert olanın** lehine çözülür. 160 adaylık havuz
> tam olarak bunun içindir: bir aday düşerse yerine bir başkası geçer ve
> kapsam sarsılmaz.

---

## 8 · Bu politikanın bilmediği

| Bilinmeyen | Ne zaman öğrenilir |
|---|---|
| Kademe C'nin 14 aktivitesi yeterli temsil mi | **Faz 2 · ebeveyn okuması** |
| Zulu ve And tekrar gibi okunuyor mu | **Faz 3 · `qa_echo`** |
| Bir kültür temsilcisi itiraz eder mi | **yayından sonra** — bu belge o itirazın cevabıdır |
