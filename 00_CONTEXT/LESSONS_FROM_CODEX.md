# CODEX PROJELERİNDEN DERSLER — bu projeye taşınanlar

> Bu proje diğer projelerden **izoledir**. Ortak dosya, ortak build çıktısı,
> ortak `.gate`, ortak rapor yoktur. Kod taşınmadı; **disiplin** taşındı.
>
> World Myths'ten **veri** devralınır — ama bu ayrı bir mekanizmadır ve
> [`INHERITANCE_ARCHITECTURE.md`](INHERITANCE_ARCHITECTURE.md) içinde tanımlıdır.

---

## 1 · Taşınan mekanizmalar

| # | Mekanizma | Nereden | Bu projede |
|---|---|---|---|
| 1 | `.gate` faz kapısı | ikisi de | `phase0…release` |
| 2 | Tek doğruluk kaynağı | World Myths | Gömülü sabit değer CI'ı kırmızı yakar |
| 3 | **Kapıların kendi testi** | World Myths | Dokuz kusurlu kurgu; devralma kilidi dahil |
| 4 | İki hatlı sızıntı koruması | Bestiarium D8/D29 | `.gitignore` + içerik taraması |
| 5 | Ölü muafiyet yasağı | Bestiarium D28 · WM K14 | Muafiyetler iki kez denetlenir |
| 6 | `run_optional` sözleşmesi | World Myths | Çıkış 2 = ATLANDI |
| 7 | **Yaş politikası kapısı** | World Myths `qa_age.py` | **Aktivite biçimine yeniden yazıldı** |
| 8 | İki ebeveyn okuması | World Myths H8 | Kanıt cinsi açıkça kaydedilir |

---

## 2 · Taşınan dersler

### D1 · Yazar adı üç betikte gömülüydü
World Myths Faz 6'da kapak ile metadata **farklı yazar** taşıyordu.
→ `project_config.json § founder` tek kaynak; `check_embedded` tarar.

### D2 · Yer tutucu metin KDP tarafından reddedildi
`[AUTHOR BIO — founder copy pending]` şablon metni sayıldı ve **reddedildi**.
→ `founder.authorBio` null iken Faz 6 kırmızıdır.

### D3 · `--fix` kapıyı sessizce düşürüyordu
→ Kapı yalnızca açıkça verilirse değişir.

### D4 · Muafiyetler sessizce ölüyordu
World Myths'te `.gitignore` sırası yüzünden manuscript politikasını
**anlatan** README hiç depoya girmedi.
→ Muafiyetler dosyanın sonunda; `selftest § ④` hepsini denetler.

### D5 · Bir kapının varlığı, koştuğu anlamına gelmiyordu
`calibrate_pages.py` yazılmıştı ama çağrılmıyordu — **ölü betik** (K18).
→ `qa_all.sh` Faz 1–5'te doğacak kapıların satırlarını şimdiden taşır.

### D6 · Yanlış nesneye bağlanmış kusursuz görsel bütün kapılardan geçer
→ `asset_inventory.py` ölçümden **önce** koşar. Bu kitapta risk daha büyüktür:
**yanlış aktiviteye bağlanmış bir görsel, aktiviteyi çözülemez yapar.**

### D7 · Yaş kapısı, doğru çalıştığı kanıtlanmadan kullanılamaz
World Myths'te `qa_age.py` 45 hikâyeyi otomatik reddetme yetkisine sahipti
ve `selftest.py` o yetkinin doğru çalıştığını kanıtlıyordu.
→ Burada aynı disiplin **devralma kilidi** için de geçerlidir:
`selftest § ②(f)` ve `§ ②(i)` onu iki farklı yönden test eder.

---

## 3 · Taşınmayanlar

| Taşınmadı | Neden |
|---|---|
| World Myths'in anlatı ses kapıları (`qa_voice` mit tonu) | Bu kitap anlatı değil **talimat** yazar |
| Bestiarium'un `kin_map` akrabalık sistemi | Burada tasnif ekseni **bölge × aktivite tipi** |
| Ortak Python kütüphanesi | Bkz. `DECISIONS.md § K1` |

---

## 4 · Bu projenin kendi dersi (peşinen)

> **Devralma bir kısayol değil, bir sözleşmedir.**

World Myths'in araştırması bu kitabın maliyet avantajının tamamıdır —
ve tam da bu yüzden en büyük riskidir. "Orada yazıyordu" bir doğrulama
değildir. `IMPORT_MANIFEST.json` bu cümleyi mekanizmaya çevirir.
