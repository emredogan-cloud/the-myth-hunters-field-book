# YAŞ POLİTİKASI — aktivite biçimine uyarlanmış

> World Myths'in `AGE_POLICY.md` disiplini burada **kopyalanmadı, yeniden
> yazıldı**. Gerekçe: orada risk *okunan şiddetti*; burada risk
> **yapılan görev**.
>
> Sürüm 1.0 · Faz 1'de onaylanır · `qa_age.py` bu belgeyi uygular

---

## 1 · Temel fark

| | World Myths | Field Book |
|---|---|---|
| Çocuk ne yapıyor | **Okuyor** | **Yazıyor, çiziyor, çözüyor** |
| Risk | Sahnelenmiş şiddet | **Yapılması istenen eylem** |
| Kalıcılık | Sayfa kapanır | **Deftere yazılan kalır** |
| Başarısızlık | "Fazla karanlık" | "Çocuğum yapamadı / yanlış öğrendi" |

Bir çocuğa bir sahneyi *okutmak* ile bir görevi *yaptırmak* aynı şey değildir.

---

## 2 · Altı yasak çerçeve

Bir aktivite bunlardan birine giriyorsa **kitaba giremez**.
`qa_age.py` bunları mekanik olarak tarar.

| # | Yasak | Neden |
|---|---|---|
| 1 | **Kutsal ritüelin taklidi** | Bir ayini "oyun" hâline getirmek, o geleneği taşıyan aileyi rencide eder |
| 2 | **Kapalı bilginin "çözülmesi"** | Bazı bilgiler bir topluluğa aittir; onu bulmaca yapmak sahiplenmedir |
| 3 | **Gerçek kişi/topluluğun karikatürleştirilmesi** | Klişe, öğretmenin kitabı rafa koymamasına yeter |
| 4 | **Şiddetin sahnelenmesini gerektiren görev** | "Savaşı çiz" ≠ "kahramanı çiz" |
| 5 | **Çocuğun evden çıkmasını gerektiren görev** | Ebeveyn denetimi olmadan güvenli değil |
| 6 | **Kesici alet, ateş veya yiyecek gerektiren görev** | Aynı gerekçe; ayrıca alerji riski |

---

## 3 · Şiddet ve trajedi: saklanmaz, sahnelenmez

World Myths'in kuralı burada da geçerlidir ve **aynı cümleyle** durur:

> *Şiddet ve trajedi **saklanmaz** ama **sahnelenmez**: sonuç anlatılır,
> dehşet betimlenmez.*

Aktivite biçimindeki karşılığı:

| ✅ Olur | ❌ Olmaz |
|---|---|
| "Bu kahraman üç sınavdan geçti. Sınavları sırala." | "Kahramanın yaralarını çiz." |
| "Canavarın hangi kültürde ne ad aldığını eşleştir." | "Canavarın avını nasıl parçaladığını anlat." |
| "Yeraltına inen tanrıçanın yolunu bul." | "Ölüler diyarını betimle." |

---

## 4 · Zorluk merdiveni — 8 yaş da 12 yaş da kullanabilmeli

Her bölümde aktiviteler **★ → ★★★** sırasıyla dizilir.

| ★ | 8–9 yaş · tek adımlı · örnekli |
| ★★ | 10–11 yaş · iki adımlı · ipuçsuz çözülebilir |
| ★★★ | 12 yaş · çok adımlı · kademeli ipucu var |

Bir bölümde ★★★ oranı **%30'u aşamaz**. Aşarsa küçük çocuk kitabı bırakır.

---

## 5 · Talimat netliği bir yaş meselesidir

Çocuk takılıyorsa **suç çocukta değil talimattadır**.

| Ölçüt | Değer | Kapı |
|---|---|---|
| Talimat cümlesi azami | **18 kelime** | `qa_instruction` |
| Cümle ortalaması | 9–14 kelime | `qa_readability` |
| Okuma seviyesi | 3.–5. sınıf | `qa_readability` |
| Şahıs | ikinci tekil (`you`) | `qa_instruction` |
| Küçümseyen ton | **YASAK** | `qa_voice` |

**Faz 2'nin sert ölçütü:** çocuk testinde aktivitelerin **≥%80'i yardımsız
anlaşılmalıdır**. Bir yetişkin "ne demek istediğini" açıklarsa test geçersizdir.

---

## 6 · İki ebeveyn okuması

World Myths'in H8 disiplini burada da zorunludur ve `project_config.json §
safety.parentReadingsRequired = 2` içinde durur.

Kanıt cinsi **açıkça** kaydedilir: kurucu beyanı mı, imzalı okuyucu kaydı mı.
Uydurulmuş okuyucu adı, tarihi veya alıntısı **yasaktır**.

---

## 7 · Çocuk testçi mahremiyeti

Çocuk testçilerinin adları **hiçbir koşulda** depoya girmez.
Kayıtlar yalnızca anonim kimlik (`tester-01`), yaş ve sonuç taşır.

`validate_structure.py § check_child_privacy` bunu mekanik olarak denetler:
`tester` alanı `tester-\d{2}` biçiminde değilse **CI kırmızı yanar**.
