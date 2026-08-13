#!/usr/bin/env python3
"""
KAPILARIN KENDİ TESTİ — bu hattın EN ÖNEMLİ testi
================================================================================
Metin yokken yeşil kalan bir hat, KUSUR GELDİĞİNDE DE YEŞİL KALABİLİR.

Bu test o riski kapatır: her kapı için TAM BİR KUSUR taşıyan kurgu bir veri
seti çalıştırılır ve kapının o kusuru YAKALADIĞI kanıtlanır.

Bu projede özellikle kritiktir çünkü iki kapı otomatik reddetme yetkisine
sahiptir ve ikisi de doğru çalıştığı KANITLANMADAN kullanılamaz:

  · `validate_spec.py`        — kapsam vaadini (120 aktivite · 22 kültür)
  · `validate_inheritance.py` — DOĞRULANMAMIŞ devralmaya dayanan aktiviteyi

İkincisi bu projenin bel kemiğidir: devralınan veri sessizce doğrulanmış
sayılırsa, World Myths'in anlatı için yeterli olan bir iddiası burada bir
BULMACA CEVABI hâline gelir ve yanlışsa çocuk kendini suçlar.

On dört bölüm:
  ①  temiz kurgu BÜTÜN kapılardan geçer          (yanlış pozitif yok)
  ②  her kusurlu kurgu İLGİLİ kapıda yakalanır   (körlük yok)
  ③  kapı seviyeleri gerçekten kilitliyor        (kapsam kapıları)
  ④  her muafiyet en az bir kez DEVREYE GİRİYOR  (ölü kural yok)
  ⑤  YAŞ VE GÜVENLİK kapısı ısırıyor mu          (Faz 1'de doğdu)
  ⑥  MATRİS VE MÜHÜR kapısı ısırıyor mu          (Faz 1'de doğdu)
  ⑦  ARAŞTIRMA ZİNCİRİ kapısı ısırıyor mu        (Faz 1'de doğdu)
  ⑧  SAYFA BÜTÇESİ kapısı ısırıyor mu            (Faz 1'de doğdu)
  ⑨  OKUNABİLİRLİK kapısı ısırıyor mu            (Faz 1'de doğdu)
  ⑩–⑬ TEK CEVAP · TALİMAT · DİL · MÜHÜR          (Faz 2'de doğdu)
  ⑭  KURUCU FAZ AŞMASI bir KİLİT mi              (Faz 3'te doğdu)
  ⑮  TEKRAR (qa_echo) kapısı ısırıyor mu         (Faz 3'te doğdu)
  ⑯  TASARIM DİZGESİ kapısı ısırıyor mu          (Faz 3'te doğdu)

④ doğrudan Bestiarium'un üç ölü kuralına ve World Myths'in K14 kararına
cevaptır: takip edilmeyen bir dosya için yazılmış muafiyet ÖLÜ MUAFİYETTİR
ve sessizce yanlış güven verir.

⑤–⑨ Faz 1'de eklendi. Gerekçe World Myths'in D7 dersidir:

    Bir yaş kapısı, doğru çalıştığı KANITLANMADAN kullanılamaz.

`qa_age.py` bir çocuk ürününde otomatik REDDETME yetkisine sahiptir ve
o yetki ancak her karar dalının ısırdığı gösterildiğinde meşrudur.
⑤(i) ayrıca belge ile kodu bağlar: `AGE_POLICY.md`'deki malzeme listesi
ile `qa_age.py`'deki küme AYRILIRSA kapı kırmızı yanar — çünkü ayrıldığı
an belge yalan söylemeye başlar.

⑤–⑧ GERÇEK VERİYİ temel alır (⑨ kendi sentetik pilotunu taşır,
çünkü gerçek pilot depoda durmaz ve CI'da yoktur): temiz kurgu depodaki asıl dizinlerdir.
Böylece hem "gerçek veri geçiyor" hem de "bozulmuş veri yakalanıyor"
aynı testte kanıtlanır.

Çıkış kodları:  0 = geçti   1 = KÖRLÜK BULUNDU
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUILD = os.path.join(ROOT, "04_BUILD")

VALIDATE_SPEC = os.path.join(BUILD, "validate_spec.py")
VALIDATE_INHERITANCE = os.path.join(BUILD, "validate_inheritance.py")
VALIDATE_STRUCTURE = os.path.join(BUILD, "validate_structure.py")
CONFIG = os.path.join(ROOT, "project_config.json")


# ---------------------------------------------------------------------------
# Kurgu üreteci — GERÇEK envanterden bağımsız, tam kontrollü veri
# ---------------------------------------------------------------------------
def clean_config() -> dict:
    with open(CONFIG, encoding="utf-8") as fh:
        return json.load(fh)


def clean_games(cfg: dict, n: int = 180, status: str = "candidate") -> dict:
    """Şemaya uyan, kusursuz kurgu envanter.

    ⚠ MATRİS DOLDURULUR: 6 bölge × 5 tip hücrelerinin HER BİRİ minimum
    sayıyı sağlayacak biçimde üretilir. Aksi hâlde temiz kurgu bile
    matris kapısında takılır ve § ① anlamsızlaşır."""
    types = cfg["scope"]["activityTypes"]
    regions = [r["id"] for r in cfg["scope"]["regionsHypothesis"]]
    acts = []
    i = 0
    # Önce her hücreyi minimumun iki katıyla doldur.
    for r in regions:
        for t in types:
            for _ in range(t.get("perRegionMin", 1) * 2):
                acts.append({
                    "activityId": "fixture-%03d" % i,
                    "title": "Fixture Activity %03d" % i,
                    "culture": "culture-%02d" % (i % 22),
                    "region": r,
                    "type": t["id"],
                    "status": status,
                    "inheritanceStatus": "inherited-verified",
                    "restrictionStatus": "open",
                })
                i += 1
    # Kalanı serpiştir.
    while len(acts) < n:
        r = regions[i % len(regions)]
        t = types[i % len(types)]
        acts.append({
            "activityId": "fixture-%03d" % i,
            "title": "Fixture Activity %03d" % i,
            "culture": "culture-%02d" % (i % 22),
            "region": r,
            "type": t["id"],
            "status": status,
            "inheritanceStatus": "inherited-verified",
            "restrictionStatus": "open",
        })
        i += 1
    return {"activities": acts}


def run(script: str, *extra: str, gate: str | None = None,
        index: str | None = None) -> tuple[int, str]:
    cmd = [sys.executable, script, *extra]
    if gate:
        cmd += ["--gate", gate]
    env = dict(os.environ)
    if index:
        env["WORLDGAMES_GAME_INDEX"] = index
    out = subprocess.run(cmd, capture_output=True, text=True, env=env,
                         timeout=120, cwd=ROOT)
    return out.returncode, out.stdout + out.stderr


_RUN_SEQ = [0]


def run_spec_with(cfg: dict, games: dict | None, gate: str,
                  tmp: str) -> tuple[int, str]:
    """validate_spec'i kurgu dosyalarla koşturur.

    Betik yolları sabit okuduğu için kurgu bir PROJE KÖKÜ kurulur:
    gerçek depo asla değiştirilmez.

    ⚠ HER KOŞU KENDİ KÖKÜNÜ ALIR. Tek bir kök paylaşılırsa önceki testin
    yazdığı game_index.json sonraki testte HÂLÂ ORADA olur ve
    "envantersiz phase1 kırmızı yanmalı" testi sessizce anlamsızlaşır —
    yani testin kendisi kör olur. Bu kusur selftest'in ilk koşusunda
    yakalandı ve bu satır onun düzeltmesidir."""
    _RUN_SEQ[0] += 1
    fake_root = os.path.join(tmp, "root-%03d" % _RUN_SEQ[0])
    os.makedirs(os.path.join(fake_root, "01_SOURCE"), exist_ok=True)
    os.makedirs(os.path.join(fake_root, "04_BUILD"), exist_ok=True)

    with open(os.path.join(fake_root, "project_config.json"), "w",
              encoding="utf-8") as fh:
        json.dump(cfg, fh, ensure_ascii=False)
    if games is not None:
        with open(os.path.join(fake_root, "01_SOURCE", "activity_index.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(games, fh, ensure_ascii=False)
    with open(os.path.join(fake_root, ".gate"), "w", encoding="utf-8") as fh:
        fh.write(gate)

    # Betiği kurgu köke kopyala: ROOT'u kendi konumundan türetiyor.
    import shutil
    shutil.copy2(VALIDATE_SPEC, os.path.join(fake_root, "04_BUILD",
                                             "validate_spec.py"))
    out = subprocess.run(
        [sys.executable, os.path.join(fake_root, "04_BUILD", "validate_spec.py"),
         "--gate", gate],
        capture_output=True, text=True, timeout=120)
    return out.returncode, out.stdout + out.stderr


class Report:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.failed: list[str] = []
        self.passed = 0

    def check(self, ok: bool, label: str, detail: str = "") -> None:
        if ok:
            self.passed += 1
            if self.verbose:
                print("  ✓ %s" % label)
        else:
            self.failed.append(label)
            print("  ✗ %s" % label)
            if detail:
                print("      %s" % detail.strip()[:400])


# ---------------------------------------------------------------------------
def part1_clean_passes(rep: Report, tmp: str) -> None:
    print("\n① temiz kurgu bütün kapılardan geçer (yanlış pozitif yok)")
    cfg = clean_config()
    games = clean_games(cfg)
    code, out = run_spec_with(cfg, games, "phase1", tmp)
    rep.check(code == 0, "temiz kurgu + phase1 → geçer", out)


def part2_flaws_caught(rep: Report, tmp: str) -> None:
    print("\n② her kusurlu kurgu ilgili kapıda yakalanır (körlük yok)")

    base = clean_config()

    # (a) yinelenen aktivite kimliği
    cfg = copy.deepcopy(base)
    g = clean_games(cfg)
    g["activities"][7]["activityId"] = g["activities"][3]["activityId"]
    code, out = run_spec_with(cfg, g, "phase1", tmp)
    rep.check(code != 0, "yinelenen activityId YAKALANIR", out)

    # (b) tanımsız aktivite tipi
    cfg = copy.deepcopy(base)
    g = clean_games(cfg)
    g["activities"][11]["type"] = "uydurma-tip"
    code, out = run_spec_with(cfg, g, "phase1", tmp)
    rep.check(code != 0, "tanımsız aktivite tipi YAKALANIR", out)

    # (c) tanımsız bölge
    cfg = copy.deepcopy(base)
    g = clean_games(cfg)
    g["activities"][13]["region"] = "uydurma-bolge"
    code, out = run_spec_with(cfg, g, "phase1", tmp)
    rep.check(code != 0, "tanımsız bölge YAKALANIR", out)

    # (d) kısıt taraması yapılmamış
    cfg = copy.deepcopy(base)
    g = clean_games(cfg)
    del g["activities"][20]["restrictionStatus"]
    code, out = run_spec_with(cfg, g, "phase1", tmp)
    rep.check(code != 0, "TARANMAMIŞ kısıt durumu YAKALANIR", out)

    # (e) devralma durumu eksik
    cfg = copy.deepcopy(base)
    g = clean_games(cfg)
    del g["activities"][9]["inheritanceStatus"]
    code, out = run_spec_with(cfg, g, "phase1", tmp)
    rep.check(code != 0, "EKSİK devralma durumu YAKALANIR", out)

    # (f) ⭑ BU PROJENİN EN ÖNEMLİ KAPISI ⭑
    #     DOĞRULANMAMIŞ devralmaya dayanan LOCKED aktivite
    cfg = copy.deepcopy(base)
    g = clean_games(cfg, status="written")
    g["activities"][4]["inheritanceStatus"] = "inherited-provisional"
    code, out = run_spec_with(cfg, g, "phase2", tmp)
    rep.check(code != 0,
              "⭑ DOĞRULANMAMIŞ devralmaya dayanan LOCKED aktivite YAKALANIR", out)

    # (g) matris deliği: bir hücre boş
    cfg = copy.deepcopy(base)
    g = clean_games(cfg)
    victim_region = cfg["scope"]["regionsHypothesis"][0]["id"]
    victim_type = cfg["scope"]["activityTypes"][0]["id"]
    g["activities"] = [a for a in g["activities"]
                       if not (a["region"] == victim_region
                               and a["type"] == victim_type)]
    code, out = run_spec_with(cfg, g, "phase1", tmp)
    rep.check(code != 0, "MATRİS DELİĞİ YAKALANIR (%s×%s boş)"
              % (victim_region, victim_type), out)

    # (h) ekonomik olarak imkânsız fiyat → negatif telif
    cfg = copy.deepcopy(base)
    for ed in cfg["production"]["editionsHypothesis"]:
        if ed["id"] == "paperback":
            ed["list"] = 2.99          # 144 sayfa büyük trim: baskı 3,45 $
    code, out = run_spec_with(cfg, clean_games(base), "phase1", tmp)
    rep.check(code != 0, "NEGATİF TELİF yakalanır (fiyat < baskı maliyeti)", out)

    # (i) devralma sözleşmesi gevşetilmiş: provisional kilide izinli
    cfg = copy.deepcopy(base)
    cfg["inheritance"]["lockRequiresStatus"] = ["inherited-provisional"]
    code, out = run_spec_with(cfg, clean_games(base), "phase1", tmp)
    rep.check(code != 0,
              "DEVRALMA SÖZLEŞMESİNİN GEVŞETİLMESİ YAKALANIR", out)


def without_override(cfg: dict) -> dict:
    """Kurucu faz aşmasını SÖKÜLMÜŞ bir config.

    ③ kapı seviyelerini sınar, aşmayı değil. Gerçek config'te etkin bir
    aşma varken (K27 · tavan `phase1`) `phase2`/`phase4` kurguları aşma
    tavanına takılır ve ③ yanlış sebeple kırmızı yanar — yani test
    ölçtüğünü sandığı şeyi ölçmez. Aşmanın kendi testi ⑭'tür."""
    c = copy.deepcopy(cfg)
    c.get("founder", {}).pop("phaseOverride", None)
    return c


def part3_gates_lock(rep: Report, tmp: str) -> None:
    print("\n③ kapı seviyeleri gerçekten kilitliyor")

    cfg = without_override(clean_config())

    # phase0: envanter yokken geçmeli (Faz 1 henüz üretmedi)
    code, out = run_spec_with(cfg, None, "phase0", tmp)
    rep.check(code == 0, "phase0 envantersiz geçer", out)

    # phase1: envanter yoksa KIRMIZI
    code, out = run_spec_with(cfg, None, "phase1", tmp)
    rep.check(code != 0, "phase1 envantersiz KIRMIZI", out)

    # phase1: 160'ın altında aday → KIRMIZI
    small = clean_games(cfg)
    small["activities"] = small["activities"][:120]
    code, out = run_spec_with(cfg, small, "phase1", tmp)
    rep.check(code != 0, "phase1 yetersiz adayla KIRMIZI (120 < 160)", out)

    # phase2: 20 kilitli aktivite yoksa KIRMIZI
    code, out = run_spec_with(cfg, clean_games(cfg, status="candidate"),
                              "phase2", tmp)
    rep.check(code != 0, "phase2 kilitli aktivite olmadan KIRMIZI", out)

    # phase2: 20 yazılmış varsa geçer
    g = clean_games(cfg, status="candidate")
    for i in range(20):
        g["activities"][i]["status"] = "written"
    code, out = run_spec_with(cfg, g, "phase2", tmp)
    rep.check(code == 0, "phase2 20 yazılmış aktiviteyle geçer", out)

    # phase4: 120 yazılmış aktivite yoksa KIRMIZI
    code, out = run_spec_with(cfg, g, "phase4", tmp)
    rep.check(code != 0, "phase4 eksik manuscript ile KIRMIZI", out)


def part4_no_dead_exemptions(rep: Report) -> None:
    print("\n④ her muafiyet en az bir kez devreye giriyor (ölü kural yok)")

    sys.path.insert(0, BUILD)
    import validate_structure as vs   # noqa: E402

    # Sızıntı taraması muafiyetleri: muaf tutulan dosya GERÇEKTEN VAR OLMALI.
    # Var olmayan bir dosya için yazılmış muafiyet ÖLÜ MUAFİYETTİR ve
    # sessizce yanlış güven verir (World Myths K14 · Bestiarium D28).
    for rel in sorted(vs.LEAK_SCAN_SKIP):
        rep.check(os.path.isfile(os.path.join(ROOT, rel)),
                  "sızıntı muafiyeti canlı: %s" % rel)

    for rel in sorted(vs.EMBED_SCAN_SKIP):
        rep.check(os.path.isfile(os.path.join(ROOT, rel)),
                  "gömülü-değer muafiyeti canlı: %s" % rel)

    # ⑤ Cevap anahtarı taraması muafiyetleri de ölü olamaz.
    for rel in sorted(vs.ANSWER_SCAN_SKIP):
        rep.check(os.path.isfile(os.path.join(ROOT, rel)),
                  "cevap-taraması muafiyeti canlı: %s" % rel)

    # Muafiyet listesi gerçekten GEREKLİ mi: muaf dosya, muaf olmasaydı
    # yakalanacak mıydı? Değilse muafiyet gereksizdir ve kaldırılmalıdır.
    import re
    for rel in sorted(vs.LEAK_SCAN_SKIP):
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8") as fh:
            body = fh.read()
        hits = sum(1 for pat in vs.LEAK_MARKERS if re.search(pat, body))
        rep.check(hits >= vs.LEAK_MIN_HITS,
                  "muafiyet GEREKLİ (yoksa yakalanırdı): %s [%d işaret]"
                  % (rel, hits))


# ═══════════════════════════════════════════════════════════════════════════
# FAZ 1 KAPILARI · ⑤–⑧
# ═══════════════════════════════════════════════════════════════════════════
QA_AGE = os.path.join(BUILD, "qa_age.py")
QA_MATRIX = os.path.join(BUILD, "qa_matrix.py")
VALIDATE_RESEARCH = os.path.join(BUILD, "validate_research.py")
PAGE_BUDGET = os.path.join(BUILD, "page_budget.py")

SRC = os.path.join(ROOT, "01_SOURCE")
REAL = {
    "01_SOURCE/activity_index.json": os.path.join(SRC, "activity_index.json"),
    "01_SOURCE/culture_index.json": os.path.join(SRC, "culture_index.json"),
    "01_SOURCE/region_index.json": os.path.join(SRC, "region_index.json"),
    "01_SOURCE/inherited/IMPORT_MANIFEST.json":
        os.path.join(SRC, "inherited", "IMPORT_MANIFEST.json"),
}

# ⚠ FAZ 3'TE DÜZELTİLDİ — SABİT DOSYA ADI TESTİ BÖLGE BÖLGE KIRIYORDU.
#
# Faz 2 bu sözlüğe TEK bir doğrulama dosyası ELLE yazmıştı
# (`jaguar-condor-revalidation.json`) ve o gün doğruydu: bir bölge vardı.
# Faz 3 iki bölge daha yazınca yeni iddialar kurgu köke KOPYALANMADI,
# claimRef'ler boşa düştü ve "temiz veri geçer" testi kırmızı yandı —
# yani test, kusuru olmayan bir veriyi kusurlu gösterdi.
#
#     Bir testin kurgusu elle bakımı gerektiriyorsa,
#     o test er geç bakımsız kalır.
#
# Dizin artık TARANIYOR: bir sonraki bölge eklendiğinde burada
# değiştirilecek hiçbir satır yok.
_RESEARCH = os.path.join(SRC, "research")
if os.path.isdir(_RESEARCH):
    for _n in sorted(os.listdir(_RESEARCH)):
        if _n.endswith("-revalidation.json"):
            REAL["01_SOURCE/research/" + _n] = os.path.join(_RESEARCH, _n)


def real_data_available() -> bool:
    return all(os.path.isfile(p) for p in REAL.values())


def load_real() -> dict:
    """Gerçek dizinler — ⑤–⑧'in temiz kurgusu."""
    out = {}
    for rel, path in REAL.items():
        with open(path, encoding="utf-8") as fh:
            out[rel] = json.load(fh)
    return out


def run_gate(script: str, data: dict, tmp: str) -> tuple[int, str]:
    """Kurgu bir proje kökü kurar ve kapıyı orada koşturur.

    ⚠ HER KOŞU KENDİ KÖKÜNÜ ALIR (§ run_spec_with ile aynı gerekçe):
    paylaşılan bir kök, önceki testin dosyasını sonraki teste sızdırır
    ve testin kendisi körleşir."""
    import shutil
    _RUN_SEQ[0] += 1
    root = os.path.join(tmp, "gate-%03d" % _RUN_SEQ[0])
    os.makedirs(os.path.join(root, "01_SOURCE", "inherited"), exist_ok=True)
    os.makedirs(os.path.join(root, "04_BUILD"), exist_ok=True)
    os.makedirs(os.path.join(root, "06_REPORTS"), exist_ok=True)

    for rel, obj in data.items():
        p = os.path.join(root, *rel.split("/"))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, ensure_ascii=False)
    with open(os.path.join(root, ".gate"), "w", encoding="utf-8") as fh:
        fh.write("phase1")

    dest = os.path.join(root, "04_BUILD", os.path.basename(script))
    shutil.copy2(script, dest)
    out = subprocess.run([sys.executable, dest], capture_output=True,
                         text=True, timeout=120)
    return out.returncode, out.stdout + out.stderr


def with_config(real: dict) -> dict:
    d = dict(real)
    d["project_config.json"] = clean_config()
    return d


def mutate_activity(data: dict, pred, **fields) -> dict:
    """İlk eşleşen aktiviteyi bozar. Derin kopya üzerinde çalışır."""
    d = copy.deepcopy(data)
    for a in d["01_SOURCE/activity_index.json"]["activities"]:
        if pred(a):
            for k, v in fields.items():
                if v is _DELETE:
                    a.pop(k, None)
                else:
                    a[k] = v
            return d
    raise AssertionError("kurgu için uygun aktivite bulunamadı")


class _Delete:
    pass


_DELETE = _Delete()


def part5_age_gate(rep: Report, tmp: str, base: dict) -> None:
    print("\n⑤ YAŞ VE GÜVENLİK kapısı ısırıyor mu")

    code, out = run_gate(QA_AGE, base, tmp)
    rep.check(code == 0, "gerçek envanter yaş kapısından GEÇER", out)

    live = lambda a: a.get("status") != "dropped"

    # (a) yasak malzeme — beyan `safe` kalırsa çelişki yakalanmalı
    d = mutate_activity(base, live, materials=["book", "pencil", "scissors"])
    code, out = run_gate(QA_AGE, d, tmp)
    rep.check(code != 0, "⭑ YASAK MALZEME (scissors) YAKALANIR", out)

    # (b) KAPALI ARIZA — tanınmayan malzeme `safe` sayılamaz
    d = mutate_activity(base, live, materials=["book", "pencil", "quantum-ruler"])
    code, out = run_gate(QA_AGE, d, tmp)
    rep.check(code != 0, "⭑ TANINMAYAN MALZEME 'safe' SAYILMAZ (kapalı arıza)", out)

    # (c) malzemesiz aktivite de `safe` olamaz
    d = mutate_activity(base, live, materials=[])
    code, out = run_gate(QA_AGE, d, tmp)
    rep.check(code != 0, "MALZEMESİZ aktivite YAKALANIR", out)

    # (d) safe-with-adult ebeveyn notu olmadan
    d = mutate_activity(base,
                        lambda a: a.get("safetyClass") == "safe-with-adult",
                        parentNote=_DELETE)
    code, out = run_gate(QA_AGE, d, tmp)
    rep.check(code != 0, "EBEVEYN NOTSUZ safe-with-adult YAKALANIR", out)

    # (e) betimleme fiili × işaretli ad — "şiddeti çiz"
    d = mutate_activity(base, live,
                        objective="Reader draws the wounds of the hero in the box.")
    code, out = run_gate(QA_AGE, d, tmp)
    rep.check(code != 0, "⭑ ŞİDDETİN BETİMLENMESİNİ isteyen görev YAKALANIR", out)

    # (f) yasak çerçeve, incelenmemiş
    d = mutate_activity(base, lambda a: live(a) and not a.get("parentNote")
                        and not a.get("restrictionNote"),
                        objective="Light a match and hold it near the page.")
    code, out = run_gate(QA_AGE, d, tmp)
    rep.check(code != 0, "⭑ İNCELENMEMİŞ YASAK ÇERÇEVE YAKALANIR", out)

    # (g) kutsal ritüelin taklidi — çerçeve 1
    d = mutate_activity(base, lambda a: live(a) and not a.get("parentNote")
                        and not a.get("restrictionNote"),
                        objective="Reader performs the ceremony and chants the prayer.")
    code, out = run_gate(QA_AGE, d, tmp)
    rep.check(code != 0, "⭑ KUTSAL RİTÜEL TAKLİDİ YAKALANIR", out)

    # (h) do-not-use bir aktivite kitapta kalamaz
    d = copy.deepcopy(base)
    d["01_SOURCE/activity_index.json"]["activities"][0]["safetyClass"] = "do-not-use"
    code, out = run_gate(QA_AGE, d, tmp)
    rep.check(code != 0, "KİTAPTA KALAN do-not-use YAKALANIR", out)

    # (i) restricted bir aktivite kitapta kalamaz
    d = mutate_activity(base, live, restrictionStatus="restricted")
    code, out = run_gate(QA_AGE, d, tmp)
    rep.check(code != 0, "KİTAPTA KALAN restricted YAKALANIR", out)

    # (j) denetim yükü — yarısı yetişkin isterse ürün vaadi bozulur
    d = copy.deepcopy(base)
    for a in d["01_SOURCE/activity_index.json"]["activities"][:100]:
        a["materials"] = ["book", "pencil", "mirror"]
        a["safetyClass"] = "safe-with-adult"
        a["parentNote"] = "An adult hands over the mirror."
    code, out = run_gate(QA_AGE, d, tmp)
    rep.check(code != 0, "DENETİM YÜKÜ AŞIMI YAKALANIR (safe-with-adult > %10)", out)

    # (k) BELGE ↔ KOD BAĞI — üç yönlü.
    #
    # ⚠ BU DENETİMİN İLK HÂLİ YETERSİZDİ: malzeme adlarının belgede GEÇTİĞİNİ
    # doğruluyordu ama HANGİ KADEMEDE olduğunu değil. `ruler` kodda T0,
    # belgede T1 durduğu hâlde test yeşil yandı. Bir kapı "adı geçiyor mu"
    # diye sorarsa, o kapı yoktur. Şimdi KADEME KADEME karşılaştırıyor.
    import re as _re
    sys.path.insert(0, BUILD)
    import qa_age  # noqa: E402

    policy = os.path.join(ROOT, "00_CONTEXT", "AGE_POLICY.md")
    with open(policy, encoding="utf-8") as fh:
        body = fh.read()

    doc_tiers: dict[str, set] = {}
    for tier in ("T0", "T1", "TX"):
        m = _re.search(r"^\|\s*\*\*%s\*\*\s*\|(.+?)\|" % tier, body, _re.M)
        doc_tiers[tier] = set(_re.findall(r"`([a-z-]+)`", m.group(1))) if m else set()

    code_tiers = {"T0": qa_age.T0, "T1": qa_age.T1, "TX": qa_age.TX}
    for tier in ("T0", "T1", "TX"):
        rep.check(doc_tiers[tier] == code_tiers[tier],
                  "⭑ AGE_POLICY.md %s kademesi qa_age.py ile AYNI" % tier
                  + ("" if doc_tiers[tier] == code_tiers[tier] else
                     " — belge=%s kod=%s" % (sorted(doc_tiers[tier]),
                                             sorted(code_tiers[tier]))))

    # Şema da aynı beyaz listeyi taşımalıdır: bir aktivite şemadan geçip
    # kapıda takılıyorsa, ayrım yanlış yerdedir.
    with open(os.path.join(SRC, "activity.schema.json"), encoding="utf-8") as fh:
        schema = json.load(fh)
    schema_mats = set(schema["properties"]["materials"]["items"]["enum"])
    rep.check(schema_mats == (qa_age.T0 | qa_age.T1),
              "⭑ şema malzeme listesi T0 ∪ T1 ile AYNI"
              + ("" if schema_mats == (qa_age.T0 | qa_age.T1) else
                 " — şema=%s kod=%s" % (sorted(schema_mats),
                                        sorted(qa_age.T0 | qa_age.T1))))

    # TX şemada HİÇ TANIMLI OLMAMALIDIR: yasak malzeme adı geçmemelidir.
    leaked = sorted(schema_mats & qa_age.TX)
    rep.check(not leaked, "şema hiçbir TX malzemesini tanımlamıyor"
              + ("" if not leaked else " — SIZINTI: %s" % leaked))


def part5b_attribution(rep: Report, tmp: str, base: dict) -> None:
    """⭑ ATIF DENETİMİ — iç editoryal inceleme 16 sayfanın 11'inde ihlal buldu."""
    print("\n⑤b ATIF denetimi ısırıyor mu")

    ok = copy.deepcopy(BOOK_FIXTURE)
    code, out = run_text_gate(QA_AGE, base, tmp, ok)
    rep.check(code == 0, "kültür adı geçen sentetik proza GEÇER", out)

    # Kültür adı çocuğun gördüğü metinden ÇIKARILIRSA
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][0]["prompt"] = "Your mission: read the six numbers on the plate."
    d["activities"][0]["fieldNote"] = (
        "These numbers use three signs. A dot is one, a bar is five, "
        "and a shell means none at all.")
    code, out = run_text_gate(QA_AGE, base, tmp, d)
    rep.check(code != 0, "⭑ ATIFSIZ SAYFA YAKALANIR (kültür adı yok)", out)


def part6_matrix_gate(rep: Report, tmp: str, base: dict) -> None:
    print("\n⑥ MATRİS VE MÜHÜR kapısı ısırıyor mu")

    code, out = run_gate(QA_MATRIX, base, tmp)
    rep.check(code == 0, "gerçek envanter matris kapısından GEÇER", out)

    acts_key = "01_SOURCE/activity_index.json"

    # (a) matris deliği
    d = copy.deepcopy(base)
    victim = d[acts_key]["activities"][0]
    r, t = victim["region"], victim["type"]
    d[acts_key]["activities"] = [a for a in d[acts_key]["activities"]
                                 if not (a["region"] == r and a["type"] == t)]
    code, out = run_gate(QA_MATRIX, d, tmp)
    rep.check(code != 0, "⭑ MATRİS DELİĞİ YAKALANIR (%s×%s)" % (r, t), out)

    # (b) mühür yuvası boş
    d = mutate_activity(base, lambda a: a.get("sealSlot") == 1, sealSlot=_DELETE)
    code, out = run_gate(QA_MATRIX, d, tmp)
    rep.check(code != 0, "⭑ BOŞ MÜHÜR YUVASI YAKALANIR", out)

    # (c) aynı yuva iki kez dolu
    d = copy.deepcopy(base)
    donor = next(a for a in d[acts_key]["activities"] if a.get("sealSlot") == 1)
    twin = next(a for a in d[acts_key]["activities"]
                if a["region"] == donor["region"] and not a.get("sealSlot")
                and not a.get("openEnded"))
    twin["sealSlot"] = 1
    code, out = run_gate(QA_MATRIX, d, tmp)
    rep.check(code != 0, "⭑ ÇAKIŞAN MÜHÜR YUVASI YAKALANIR", out)

    # (d) açık uçlu aktivite mühür besleyemez
    d = copy.deepcopy(base)
    oe = next(a for a in d[acts_key]["activities"] if a.get("openEnded"))
    slot_owner = next(a for a in d[acts_key]["activities"]
                      if a["region"] == oe["region"] and a.get("sealSlot"))
    oe["sealSlot"] = slot_owner["sealSlot"]
    del slot_owner["sealSlot"]
    code, out = run_gate(QA_MATRIX, d, tmp)
    rep.check(code != 0, "⭑ AÇIK UÇLU AKTİVİTE MÜHÜR BESLEYEMEZ", out)

    # (e) bir kültür temsilsiz kalıyor
    d = copy.deepcopy(base)
    gone = d[acts_key]["activities"][0]["culture"]
    d[acts_key]["activities"] = [a for a in d[acts_key]["activities"]
                                 if a["culture"] != gone]
    code, out = run_gate(QA_MATRIX, d, tmp)
    rep.check(code != 0, "⭑ TEMSİLSİZ KÜLTÜR YAKALANIR (%s)" % gone, out)

    # (f) openEnded 'make' dışında bir tipte
    d = mutate_activity(base, lambda a: a["type"] == "sort", openEnded=True)
    code, out = run_gate(QA_MATRIX, d, tmp)
    rep.check(code != 0, "openEnded 'make' DIŞINDA YAKALANIR", out)

    # (g) kültürün izin vermediği tip
    d = copy.deepcopy(base)
    for c in d["01_SOURCE/culture_index.json"]["cultures"]:
        if c["id"] == "hindu":
            c["allowedTypes"] = ["observe"]
            break
    code, out = run_gate(QA_MATRIX, d, tmp)
    rep.check(code != 0, "⭑ KÜLTÜRÜN İZİN VERMEDİĞİ TİP YAKALANIR", out)

    # (h) kısıt gevşetme: attributed bir kültürde aktivite 'open' olamaz
    d = mutate_activity(base,
                        lambda a: a.get("restrictionStatus") == "attributed",
                        restrictionStatus="open")
    code, out = run_gate(QA_MATRIX, d, tmp)
    rep.check(code != 0, "⭑ KISIT GEVŞETMESİ YAKALANIR", out)

    # (i) zorluk profili beslenemiyor
    d = copy.deepcopy(base)
    for a in d[acts_key]["activities"]:
        if a["difficulty"] == 1:
            a["difficulty"] = 2
    code, out = run_gate(QA_MATRIX, d, tmp)
    rep.check(code != 0, "ZORLUK PROFİLİ AÇIĞI YAKALANIR (★ tükendi)", out)


def part7_research_gate(rep: Report, tmp: str, base: dict) -> None:
    print("\n⑦ ARAŞTIRMA ZİNCİRİ kapısı ısırıyor mu")

    code, out = run_gate(VALIDATE_RESEARCH, base, tmp)
    rep.check(code == 0, "gerçek envanter araştırma kapısından GEÇER", out)

    acts_key = "01_SOURCE/activity_index.json"

    # (a) manifestte olmayan bir hikâyeye bağlanmış aday
    d = mutate_activity(base, lambda a: a.get("sourceStory"),
                        sourceStory="story-does-not-exist")
    code, out = run_gate(VALIDATE_RESEARCH, d, tmp)
    rep.check(code != 0, "⭑ MANİFESTSİZ HİKÂYE REFERANSI YAKALANIR", out)

    # (b) aktivite dışı bırakılmış hikâyeden aday
    man = base["01_SOURCE/inherited/IMPORT_MANIFEST.json"]
    excluded = [r["recordId"] for r in man["records"]
                if r.get("activityExcludedReason")]
    if excluded:
        d = mutate_activity(base, lambda a: a.get("sourceStory"),
                            sourceStory=excluded[0])
        code, out = run_gate(VALIDATE_RESEARCH, d, tmp)
        rep.check(code != 0, "⭑ AKTİVİTE DIŞI HİKÂYEDEN ADAY YAKALANIR", out)
    else:
        rep.check(False, "manifest hiç 'aktivite dışı' kayıt taşımıyor — "
                         "editoryal dışlama katmanı KAYIP")

    # (c) doğrulama planı olmayan provisional aday
    d = mutate_activity(base,
                        lambda a: a.get("inheritanceStatus") == "inherited-provisional",
                        revalidationPlan=_DELETE)
    code, out = run_gate(VALIDATE_RESEARCH, d, tmp)
    rep.check(code != 0, "⭑ PLANSIZ inherited-provisional YAKALANIR", out)

    # (d) "sonra bakarız" bir plan değildir
    d = mutate_activity(base,
                        lambda a: a.get("inheritanceStatus") == "inherited-provisional",
                        revalidationPlan="sonra bakarız")
    code, out = run_gate(VALIDATE_RESEARCH, d, tmp)
    rep.check(code != 0, "ZAYIF doğrulama planı YAKALANIR", out)

    # (e) BEL KEMİĞİ: doğrulanmamış devralmaya dayanan locked aday
    d = mutate_activity(base,
                        lambda a: a.get("inheritanceStatus") == "inherited-provisional",
                        status="locked")
    code, out = run_gate(VALIDATE_RESEARCH, d, tmp)
    rep.check(code != 0,
              "⭑ DOĞRULANMAMIŞ DEVRALMAYA DAYANAN locked ADAY YAKALANIR", out)

    # (f) kademe gevşetmesi: kültür dizini manifestten ayrılırsa
    d = copy.deepcopy(base)
    for c in d["01_SOURCE/culture_index.json"]["cultures"]:
        if c["eligibilityTier"] == "C":
            c["eligibilityTier"] = "A"
            break
    code, out = run_gate(VALIDATE_RESEARCH, d, tmp)
    rep.check(code != 0, "⭑ KADEME GEVŞETMESİ YAKALANIR (C → A)", out)

    # (g) mühür besleyen aday, cevap üretemeyen bir kayda dayanamaz
    d = copy.deepcopy(base)
    for r in d["01_SOURCE/inherited/IMPORT_MANIFEST.json"]["records"]:
        if r.get("kind") == "story" and "answer-source" in (r.get("fieldbookUsage") or []):
            target = r["recordId"]
            r["fieldbookUsage"] = ["background"]
            break
    for a in d[acts_key]["activities"]:
        if a.get("sealSlot"):
            a["sourceStory"] = target
            break
    code, out = run_gate(VALIDATE_RESEARCH, d, tmp)
    rep.check(code != 0, "⭑ YETKİSİZ KAYDA DAYANAN MÜHÜR YAKALANIR", out)

    # (h) diakritik kaybı — çocuk bunu deftere yazacak
    d = copy.deepcopy(base)
    for c in d["01_SOURCE/culture_index.json"]["cultures"]:
        if c["id"] == "hawaiian":
            c["writingSystem"] = "Okina and kahako - two marks, two words"
            break
    code, out = run_gate(VALIDATE_RESEARCH, d, tmp)
    rep.check(code != 0, "⭑ DİAKRİTİK KAYBI YAKALANIR (ʻokina düştü)", out)

    # (i) kodlama bozulması (mojibake)
    d = copy.deepcopy(base)
    d["01_SOURCE/culture_index.json"]["cultures"][0]["fieldNoteAngle"] = \
        "BuÃ§uk bir baÅŸlÄ±k"
    code, out = run_gate(VALIDATE_RESEARCH, d, tmp)
    rep.check(code != 0, "MOJIBAKE YAKALANIR", out)

    # (j) gerekçesiz aday — "bu eğlenceli görünüyor" bir gerekçe değildir
    d = mutate_activity(base, lambda a: True, learningDimensions=[])
    code, out = run_gate(VALIDATE_RESEARCH, d, tmp)
    rep.check(code != 0, "⭑ ÖĞRENME BOYUTU OLMAYAN ADAY YAKALANIR", out)


def part8_page_budget(rep: Report, tmp: str, base: dict) -> None:
    print("\n⑧ SAYFA BÜTÇESİ kapısı ısırıyor mu")

    code, out = run_gate(PAGE_BUDGET, base, tmp)
    rep.check(code == 0, "gerçek model sayfa bütçesinden GEÇER", out)

    # (a) kapsam şişerse sayfa bandı aşılır
    d = copy.deepcopy(base)
    for r in d["01_SOURCE/region_index.json"]["regions"]:
        r["activityQuota"] = r["activityQuota"] * 2
    code, out = run_gate(PAGE_BUDGET, d, tmp)
    rep.check(code != 0, "⭑ SAYFA BANDI AŞIMI YAKALANIR (kota iki katı)", out)

    # (b) fiyat baskı maliyetinin altına düşerse telif negatif olur
    d = copy.deepcopy(base)
    d["project_config.json"] = copy.deepcopy(base["project_config.json"])
    for ed in d["project_config.json"]["production"]["editionsHypothesis"]:
        if ed["id"] == "paperback":
            ed["list"] = 2.99
    code, out = run_gate(PAGE_BUDGET, d, tmp)
    rep.check(code != 0, "⭑ NEGATİF TELİF YAKALANIR", out)

    # (c) kapsam çökerse band alttan da kırılır
    d = copy.deepcopy(base)
    for r in d["01_SOURCE/region_index.json"]["regions"]:
        r["activityQuota"] = 2
    code, out = run_gate(PAGE_BUDGET, d, tmp)
    rep.check(code != 0, "SAYFA BANDI ALT SINIRI YAKALANIR (kapsam çöktü)", out)


QA_READABILITY = os.path.join(BUILD, "qa_readability.py")

# ⚠ SENTETİK PİLOT. Gerçek pilot 02_MANUSCRIPT altındadır ve DEPOYA GİRMEZ,
# yani CI'da yoktur. Bu test gerçek dosyaya bağlanamaz — kendi metnini
# taşır. Böylece kapı, manuscript olmayan bir makinede de KANITLANIR.
PILOT_FIXTURE = {
    "activities": [
        {
            "activityId": "fixture-cipher",
            "prompt": "Your mission: read the three names cut into the stones.",
            "fieldNote": "This script was cut along the edge of standing stones "
                         "about sixteen hundred years ago. Each letter is a group "
                         "of notches.",
            "steps": ["Start at the bottom of each edge.",
                      "Match every notch group to a letter.",
                      "Write each name in the box."],
            "hints": ["Turn the page so the edge runs up and down.",
                      "The first stone has four notches, then two."],
        },
        {
            "activityId": "fixture-observe",
            "prompt": "Your mission: match each carved stone to the print it makes.",
            "fieldNote": "A cylinder seal is a small carved stone rolled across "
                         "wet clay. It prints a whole scene and works as a signature.",
            "steps": ["Look at the carving on each cylinder.",
                      "Find the print that matches it."],
            "hints": ["A rolled print is the mirror of the carving."],
        },
    ]
}


def run_readability(pilot: dict, tmp: str) -> tuple[int, str]:
    import shutil
    _RUN_SEQ[0] += 1
    root = os.path.join(tmp, "read-%03d" % _RUN_SEQ[0])
    os.makedirs(os.path.join(root, "02_MANUSCRIPT", "pilot"), exist_ok=True)
    os.makedirs(os.path.join(root, "04_BUILD"), exist_ok=True)
    with open(os.path.join(root, "project_config.json"), "w", encoding="utf-8") as fh:
        json.dump(clean_config(), fh, ensure_ascii=False)
    with open(os.path.join(root, "02_MANUSCRIPT", "pilot", "pilot.json"), "w",
              encoding="utf-8") as fh:
        json.dump(pilot, fh, ensure_ascii=False)
    dest = os.path.join(root, "04_BUILD", "qa_readability.py")
    shutil.copy2(QA_READABILITY, dest)
    out = subprocess.run([sys.executable, dest], capture_output=True,
                         text=True, timeout=120)
    return out.returncode, out.stdout + out.stderr


def part9_readability(rep: Report, tmp: str) -> None:
    print("\n⑨ OKUNABİLİRLİK kapısı ısırıyor mu")

    code, out = run_readability(PILOT_FIXTURE, tmp)
    rep.check(code == 0, "kalibre edilmiş sentetik pilot GEÇER", out)

    # (a) metin yokken kapı yeşil ve BOŞ koşar — kabul edilmiş düzen
    code, out = run_readability({"activities": []}, tmp)
    rep.check(code == 0, "metin yokken kapı boş koşar (manuscript depoda yok)", out)

    # (b) çok uzun talimat cümlesi
    d = copy.deepcopy(PILOT_FIXTURE)
    d["activities"][0]["steps"][0] = (
        "Start at the very bottom of each carved edge and then work your way "
        "slowly upward until you reach the top of the stone.")
    code, out = run_readability(d, tmp)
    rep.check(code != 0, "⭑ AŞIRI UZUN TALİMAT CÜMLESİ YAKALANIR", out)

    # (c) DEĞİŞMEZ ihlali: talimat, tanıttığı içerikten ZOR
    d = copy.deepcopy(PILOT_FIXTURE)
    for a in d["activities"]:
        a["fieldNote"] = "A stone. It is old. Look at it. It is here."
    code, out = run_readability(d, tmp)
    rep.check(code != 0,
              "⭑ TALİMAT İÇERİKTEN ZOR OLURSA YAKALANIR (değişmez ihlali)", out)

    # (d) küçümseyen ton
    d = copy.deepcopy(PILOT_FIXTURE)
    d["activities"][0]["prompt"] = ("Your mission, little explorer: read the "
                                    "three names cut into the stones.")
    code, out = run_readability(d, tmp)
    rep.check(code != 0, "⭑ KÜÇÜMSEYEN HİTAP YAKALANIR", out)

    # (e) yasak kalıp
    d = copy.deepcopy(PILOT_FIXTURE)
    d["activities"][1]["prompt"] = ("Your mission: dive into the world of "
                                    "carved stones and find the print.")
    code, out = run_readability(d, tmp)
    rep.check(code != 0, "YASAK KALIP YAKALANIR", out)

    # (f) field note bandı: kültürel bilgi kutusu bir paragrafa dönüşürse
    d = copy.deepcopy(PILOT_FIXTURE)
    d["activities"][0]["fieldNote"] = " ".join(["This stone is very old."] * 12)
    code, out = run_readability(d, tmp)
    rep.check(code != 0, "AŞIRI UZUN FIELD NOTE YAKALANIR", out)



# ═══════════════════════════════════════════════════════════════════════════
# FAZ 2 KAPILARI · ⑩–⑬
#
# Her yeni kapı için TAM BİR KUSUR TAŞIYAN kurgu koşturulur ve kapının o
# kusuru yakaladığı KANITLANIR. Gerekçe World Myths'in D7 dersi:
#
#     Bir kapı, doğru çalıştığı KANITLANMADAN kullanılamaz.
#
# Bu bölümlerin kurgusu gerçek dizinler + SENTETİK bir manuscript'tir.
# Gerçek manuscript depoda yoktur ve testler ona BAĞLI OLAMAZ.
# ═══════════════════════════════════════════════════════════════════════════
QA_SOLVABLE = os.path.join(BUILD, "qa_solvable.py")
QA_INSTRUCTION = os.path.join(BUILD, "qa_instruction.py")
QA_LANGUAGE = os.path.join(BUILD, "qa_language.py")
QA_PROGRESSION = os.path.join(BUILD, "qa_progression.py")
CHILD_PACK = os.path.join(BUILD, "child_test_pack.py")

# Sentetik pilot: iki mühür besleyen sayfa + bir açık uçlu sayfa.
# Yıldızlı sözcükler MUT ve OKAY; harfleri M ve O — sentetik bölge
# sözcüğü "MO" DEĞİL, sentetik anahtar aşağıda kurulur.
BOOK_FIXTURE = {
    "meta": {"kind": "selftest", "language": "en"},
    "activities": [
        {
            "activityId": "maya-bar-dot-numbers",
            "prompt": "Your mission: read the six numbers on the market plate.",
            "fieldNote": "The Maya wrote numbers with three signs. A dot is one, "
                         "a bar is five, and a shell means none at all.",
            "steps": ["Count the dots and bars beside each basket.",
                      "Write the name on the shell basket in the star box."],
            "answer": "cacao 12 · maize 15 · chilli 0",
            "hints": ["One sign is not a dot and not a bar.",
                      "The shell basket has nothing in it."],
            "sealSlot": 1, "sealStarWord": "chilli", "sealStarIndex": 1,
            "sealContribution": "C", "writingSpaceLines": 4,
            "pagePrints": ["key panel: dot = 1, bar = 5, shell = 0",
                           "baskets labelled cacao, maize, chilli",
                           "star box with six letter squares"],
        },
        {
            "activityId": "aztec-chinampa-plate",
            "prompt": "Your mission: label the lake garden and find what holds it.",
            "fieldNote": "These Aztec lake gardens do not float, though people often "
                         "say they do. Willow trees called ahuejote grow along every edge.",
            "steps": ["Write the four labels from the word bank.",
                      "Write the name of the tree in the star box."],
            "answer": "posts · woven fence · lake mud · ahuejote willow",
            "hints": ["Look at the edges, not the middle.",
                      "Only one label names a living thing."],
            "sealSlot": 2, "sealStarWord": "ahuejote", "sealStarIndex": 6,
            "sealContribution": "O", "writingSpaceLines": 4,
            "pagePrints": ["cutaway of one plot with posts and a woven fence",
                           "word bank with ahuejote as a single-word entry",
                           "four label lines"],
        },
        {
            "activityId": "maya-number-make",
            "prompt": "Your mission: write your own age in dots and bars.",
            "fieldNote": "The Maya wrote numbers with dots and bars. Writing a number "
                         "you already know is the fastest way to learn them.",
            "steps": ["Draw your age with dots and bars.",
                      "Draw the number of doors in your home below it."],
            "openEnded": True,
            "expectedResult": "Each number is drawn with four or fewer dots above "
                              "each bar, and the bars are stacked flat.",
            "hints": ["Four dots is the most you will ever need.",
                      "Bars lie flat, one above the other."],
            "writingSpaceLines": 8,
            "pagePrints": ["key panel: dot = 1, bar = 5",
                           "two ruled frames"],
        },
    ],
}


def run_text_gate(script: str, data: dict, tmp: str,
                  book: dict | None, key: dict | None = None) -> tuple[int, str]:
    """Kurgu kök + sentetik manuscript (+ istenirse sentetik mühür anahtarı)."""
    import shutil
    _RUN_SEQ[0] += 1
    root = os.path.join(tmp, "text-%03d" % _RUN_SEQ[0])
    for d in ("01_SOURCE/inherited", "01_SOURCE/answers", "02_MANUSCRIPT",
              "03_EDITORIAL", "04_BUILD", "06_REPORTS"):
        os.makedirs(os.path.join(root, *d.split("/")), exist_ok=True)
    for rel, obj in data.items():
        p = os.path.join(root, *rel.split("/"))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, ensure_ascii=False)
    if book is not None:
        with open(os.path.join(root, "02_MANUSCRIPT", "book.json"),
                  "w", encoding="utf-8") as fh:
            json.dump(book, fh, ensure_ascii=False)
    if key is not None:
        with open(os.path.join(root, "01_SOURCE", "answers", "seal_key.json"),
                  "w", encoding="utf-8") as fh:
            json.dump(key, fh, ensure_ascii=False)
    with open(os.path.join(root, ".gate"), "w", encoding="utf-8") as fh:
        fh.write("phase1")
    dest = os.path.join(root, "04_BUILD", os.path.basename(script))
    shutil.copy2(script, dest)
    out = subprocess.run([sys.executable, dest], capture_output=True,
                         text=True, timeout=120)
    return out.returncode, out.stdout + out.stderr


def part10_solvable(rep: Report, tmp: str, base: dict) -> None:
    print("\n⑩ TEK CEVAPLILIK kapısı ısırıyor mu")

    code, out = run_text_gate(QA_SOLVABLE, base, tmp, BOOK_FIXTURE)
    rep.check(code == 0, "temiz sentetik pilot GEÇER", out)

    code, out = run_text_gate(QA_SOLVABLE, base, tmp, None)
    rep.check(code == 0, "manuscript yokken kapı boş koşar", out)

    # (a) cevapsız bir sayfa
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][0]["answer"] = ""
    code, out = run_text_gate(QA_SOLVABLE, base, tmp, d)
    rep.check(code != 0, "⭑ CEVAPSIZ SAYFA YAKALANIR", out)

    # (b) çift cevap: "or"
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][0]["answer"] = "cacao 12 or maize 15"
    code, out = run_text_gate(QA_SOLVABLE, base, tmp, d)
    rep.check(code != 0, "⭑ ÇİFT CEVAPLI SAYFA YAKALANIR", out)

    # (c) "answers may vary" — kaçış kapısının en yaygın hâli
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][0]["answer"] = "answers may vary between readers"
    code, out = run_text_gate(QA_SOLVABLE, base, tmp, d)
    rep.check(code != 0, "'answers may vary' YAKALANIR", out)

    # (d) açık uçlu ama ölçütsüz
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][2].pop("expectedResult")
    code, out = run_text_gate(QA_SOLVABLE, base, tmp, d)
    rep.check(code != 0, "ÖLÇÜTSÜZ AÇIK UÇLU SAYFA YAKALANIR", out)

    # (e) muğlak ölçüt — "be creative" bir ölçüt değildir
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][2]["expectedResult"] = "Anything creative works."
    code, out = run_text_gate(QA_SOLVABLE, base, tmp, d)
    rep.check(code != 0, "MUĞLAK ÖLÇÜT YAKALANIR", out)

    # (f) ipucu cevabı söylüyor
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][1]["hints"] = ["The answer is ahuejote willow."]
    code, out = run_text_gate(QA_SOLVABLE, base, tmp, d)
    rep.check(code != 0, "⭑ CEVABI SIZDIRAN İPUCU YAKALANIR", out)

    # (g) mühür harfi elle DEĞİŞTİRİLMİŞ — hesapla uyuşmuyor
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][0]["sealContribution"] = "Z"
    code, out = run_text_gate(QA_SOLVABLE, base, tmp, d)
    rep.check(code != 0, "⭑ ELLE YAZILMIŞ MÜHÜR HARFİ YAKALANIR", out)

    # (h) yıldız sayısı sözcüğün dışında
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][0]["sealStarIndex"] = 99
    code, out = run_text_gate(QA_SOLVABLE, base, tmp, d)
    rep.check(code != 0, "SÖZCÜK DIŞI YILDIZ SAYISI YAKALANIR", out)

    # (i) yıldızlı sözcük sayfada basılı değil
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][0]["sealStarWord"] = "kumquat"
    code, out = run_text_gate(QA_SOLVABLE, base, tmp, d)
    rep.check(code != 0, "SAYFADA BASILI OLMAYAN YILDIZ SÖZCÜĞÜ YAKALANIR", out)

    # (k) ⭑ FIELD NOTE CEVABI SÖYLÜYOR ⭑
    #     İç editoryal inceleme bunu pilotun BEŞ sayfasında buldu.
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][1]["fieldNote"] = (
        "These lake gardens rest on posts in the lake bed, inside a woven "
        "fence, and the ahuejote willow holds them where they are.")
    code, out = run_text_gate(QA_SOLVABLE, base, tmp, d)
    rep.check(code != 0, "⭑ CEVABI SÖYLEYEN FIELD NOTE YAKALANIR", out)

    # (j) açık uçlu bir sayfa mühür besliyor
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][2]["sealSlot"] = 3
    d["activities"][2]["sealStarWord"] = "dots"
    d["activities"][2]["sealStarIndex"] = 1
    code, out = run_text_gate(QA_SOLVABLE, base, tmp, d)
    rep.check(code != 0, "⭑ AÇIK UÇLU SAYFA MÜHÜR BESLEYEMEZ", out)


def part11_instruction(rep: Report, tmp: str, base: dict) -> None:
    print("\n⑪ TALİMAT NETLİĞİ kapısı ısırıyor mu")

    code, out = run_text_gate(QA_INSTRUCTION, base, tmp, BOOK_FIXTURE)
    rep.check(code == 0, "temiz sentetik pilot GEÇER", out)

    # (a) adım bir fiille başlamıyor — bir BEYAN, talimat değil
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][0]["steps"][0] = "Two baskets are empty in this row."
    code, out = run_text_gate(QA_INSTRUCTION, base, tmp, d)
    rep.check(code != 0, "⭑ TALİMAT DEĞİL BEYAN OLAN ADIM YAKALANIR", out)

    # (b) görev satırı kalıbı bozuk
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][0]["prompt"] = "Read the six numbers on the plate."
    code, out = run_text_gate(QA_INSTRUCTION, base, tmp, d)
    rep.check(code != 0, "GÖREV SATIRI KALIBI DIŞI SAYFA YAKALANIR", out)

    # (c) ⭑ EDİLGEN SÜRÜKLENME — talimat çocuğa seslenmeyi bırakıyor
    #     Bu kurgu bir kapı kusurunu da kayda geçirir: denetimin İLK hâli
    #     "metinde 'you' var mı" diye soruyordu ve 'Your mission:' kalıbı
    #     yüzünden HİÇBİR KOŞULDA yanamıyordu. Ölü kapı burada öldü.
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][0]["prompt"] = "Your mission: the numbers must be read."
    code, out = run_text_gate(QA_INSTRUCTION, base, tmp, d)
    rep.check(code != 0, "⭑ EDİLGEN TALİMAT YAKALANIR", out)

    # (c2) üçüncü şahıs: "the reader counts…"
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][0]["steps"][0] = "Count what the reader sees in each basket."
    code, out = run_text_gate(QA_INSTRUCTION, base, tmp, d)
    rep.check(code != 0, "ÜÇÜNCÜ ŞAHIS HİTABI YAKALANIR", out)

    # (d) bir adım iki iş birden istiyor
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][0]["steps"][1] = ("Write the name in the star box and then "
                                      "count the bars again.")
    code, out = run_text_gate(QA_INSTRUCTION, base, tmp, d)
    rep.check(code != 0, "⭑ İKİ İŞİ TEK ADIMA SIKIŞTIRAN ADIM YAKALANIR", out)

    # (e) öncülsüz zamir
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][0]["steps"][1] = "Them you write in the star box."
    code, out = run_text_gate(QA_INSTRUCTION, base, tmp, d)
    rep.check(code != 0, "ÖNCÜLSÜZ ZAMİRLE BAŞLAYAN ADIM YAKALANIR", out)

    # (f) yazdırıyor ama yazacak yer yok
    #     ⚠ Alanı SİLMEK yetmez: kapı tasarım katmanıyla birleştirir ve
    #     activity_index.json onu geri getirir. Sıfır AÇIKÇA yazılmalı —
    #     ve bu, birleştirmenin gerçekten çalıştığının da kanıtıdır.
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][0]["writingSpaceLines"] = 0
    code, out = run_text_gate(QA_INSTRUCTION, base, tmp, d)
    rep.check(code != 0, "⭑ YAZMA ALANI OLMAYAN YAZDIRAN SAYFA YAKALANIR", out)

    # (g) ★ sayfası iki adımı aşıyor  (gerçek envanterde ★1)
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][0]["steps"] = ["Count the dots beside each basket.",
                                   "Write the name in the star box.",
                                   "Check your work once more."]
    code, out = run_text_gate(QA_INSTRUCTION, base, tmp, d)
    rep.check(code != 0, "★ SAYFASINDA ÜÇÜNCÜ ADIM YAKALANIR", out)


    # (h) ⭑ SAYFADA OLMAYAN BİR ŞEYE GÖNDERME ⭑
    #     "Colour them the way the key shows" — sayfada anahtar YOK.
    #     Bütün biçim kapıları bu cümleyi GEÇİRİR; çocuk yine de takılır.
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][0]["steps"][1] = "Copy the colours from the wall chart."
    code, out = run_text_gate(QA_INSTRUCTION, base, tmp, d)
    rep.check(code != 0, "⭑ SAYFADA BASILI OLMAYAN GÖNDERME YAKALANIR", out)

    # (i) pagePrints hiç yoksa — görsel şartname olmadan sayfa denetlenemez
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][0].pop("pagePrints")
    code, out = run_text_gate(QA_INSTRUCTION, base, tmp, d)
    rep.check(code != 0, "GÖRSEL ŞARTNAMESİZ SAYFA YAKALANIR", out)


def part11b_test_pack(rep: Report, tmp: str, base: dict) -> None:
    """⭑ SAHTE TEST MATERYALİ ÜRETİLEBİLİYOR MU ⭑

    `child_test_pack.py` bir kapı değil bir araçtır — ama taşıdığı REDDETME
    bir güvenlik mekanizmasıdır ve test edilmeden kullanılamaz (D7).

        Sahte test materyali, sahte test kaydının bir adım öncesidir.

    İki ayrı reddetme yolu var ve ikisi de kanıtlanmalı:
      ① kurucu onayı yokken       → testçi yoksa materyal de olamaz
      ② kaynak dosyası yokken     → yazılmamış bir çeviri üretilmiş sayılamaz

    ② özellikle önemli: betiğin ilk hâli reddetme kapısını taşıyordu ama
    kapı AÇILDIĞINDA ne olacağı yazılmamıştı — İngilizce prozayı basıp
    üstüne 'tr' etiketi yapıştıracaktı.
    """
    print("\n⑪b TEST PAKETİ reddetme yolları ısırıyor mu")
    import shutil

    def run_pack(confirmed: bool, with_source: bool) -> tuple[int, str]:
        _RUN_SEQ[0] += 1
        root = os.path.join(tmp, "pack-%03d" % _RUN_SEQ[0])
        for d in ("01_SOURCE/pilot_tr", "02_MANUSCRIPT", "04_BUILD"):
            os.makedirs(os.path.join(root, *d.split("/")), exist_ok=True)
        cfg = copy.deepcopy(base["project_config.json"])
        cfg.setdefault("founder", {}).setdefault("childTesters", {})
        cfg["founder"]["childTesters"]["founderConfirmed"] = confirmed
        cfg["founder"]["childTesters"]["availableTesters"] = 2 if confirmed else 0
        cfg.setdefault("language", {}).setdefault("commercial", "en")
        cfg["language"].setdefault("testOnly", ["tr"])
        with open(os.path.join(root, "project_config.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(cfg, fh, ensure_ascii=False)
        with open(os.path.join(root, "01_SOURCE", "activity_index.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(base["01_SOURCE/activity_index.json"], fh, ensure_ascii=False)
        with open(os.path.join(root, "02_MANUSCRIPT", "book.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(BOOK_FIXTURE, fh, ensure_ascii=False)
        if with_source:
            with open(os.path.join(root, "01_SOURCE", "pilot_tr",
                                   "source-tr.json"), "w", encoding="utf-8") as fh:
                json.dump({"meta": {"language": "tr"},
                           "activities": [{"activityId": "x",
                                           "prompt": "Görevin: oku.",
                                           "steps": ["Say."],
                                           "writingSpaceLines": 2}]},
                          fh, ensure_ascii=False)
        dest = os.path.join(root, "04_BUILD", "child_test_pack.py")
        shutil.copy2(CHILD_PACK, dest)
        out = subprocess.run([sys.executable, dest, "--lang", "tr"],
                             capture_output=True, text=True, timeout=120)
        return out.returncode, out.stdout + out.stderr

    code, out = run_pack(confirmed=False, with_source=True)
    rep.check(code == 3, "⭑ ONAY YOKKEN TÜRKÇE MATERYAL REDDEDİLİR", out)

    code, out = run_pack(confirmed=True, with_source=False)
    rep.check(code == 3, "⭑ KAYNAK YOKKEN TÜRKÇE MATERYAL REDDEDİLİR "
                         "(İngilizce proza 'tr' etiketiyle BASILMAZ)", out)

    code, out = run_pack(confirmed=True, with_source=True)
    rep.check(code == 0, "onay + kaynak varken paket ÜRETİLİR", out)


def part12_language(rep: Report, tmp: str, base: dict) -> None:
    print("\n⑫ DİL AYRIMI kapısı ısırıyor mu")

    code, out = run_text_gate(QA_LANGUAGE, base, tmp, BOOK_FIXTURE)
    rep.check(code == 0, "İngilizce sentetik pilot GEÇER", out)

    # (a) ⭑ EN ÖNEMLİ KURGU ⭑ — Türkçe talimat ticari katmana sızmış
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][0]["prompt"] = "Göreviniz: levhadaki altı sayıyı okuyun."
    code, out = run_text_gate(QA_LANGUAGE, base, tmp, d)
    rep.check(code != 0, "⭑ TÜRKÇE TALİMAT TİCARİ KATMANDA YAKALANIR", out)

    # (b) Türkçe field note
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][1]["fieldNote"] = ("Bu göller üzerindeki bahçeler yüzmez. "
                                       "Söğüt kökleri onları yerinde tutar.")
    code, out = run_text_gate(QA_LANGUAGE, base, tmp, d)
    rep.check(code != 0, "TÜRKÇE FIELD NOTE YAKALANIR", out)

    # (c) Türkçe ipucu
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][0]["hints"] = ["Kenarlara bak, ortaya değil."]
    code, out = run_text_gate(QA_LANGUAGE, base, tmp, d)
    rep.check(code != 0, "TÜRKÇE İPUCU YAKALANIR", out)

    # (d) KÜLTÜREL AD YANLIŞLIKLA SUÇLANMAMALI — kapı ters yönde de doğru
    #     çalışmalı: Tenochtitlán ve Huarochirí Türkçe DEĞİLDİR.
    d = copy.deepcopy(BOOK_FIXTURE)
    d["activities"][0]["fieldNote"] = (
        "The city of Tenochtitlán sat on a lake. The Huarochirí account and "
        "Tonacatépetl both keep their own spelling on the page.")
    code, out = run_text_gate(QA_LANGUAGE, base, tmp, d)
    rep.check(code == 0, "⭑ KÜLTÜREL DİAKRİTİK TÜRKÇE SANILMAZ", out)

    # (e) ticari dil ile test dili aynı yapılırsa
    d = copy.deepcopy(base)
    cfg = copy.deepcopy(d["project_config.json"])
    cfg["language"]["testOnly"] = ["en"]
    cfg["language"]["commercial"] = "en"
    d["project_config.json"] = cfg
    code, out = run_text_gate(QA_LANGUAGE, d, tmp, BOOK_FIXTURE)
    rep.check(code != 0, "⭑ TİCARİ DİL = TEST DİLİ GEVŞETMESİ YAKALANIR", out)

    # (f) testçi yokken 'passed' beyanı
    d = copy.deepcopy(base)
    cfg = copy.deepcopy(d["project_config.json"])
    cfg["founder"]["childTesters"]["externalValidation"] = "passed"
    cfg["founder"]["childTesters"]["availableTesters"] = 0
    d["project_config.json"] = cfg
    code, out = run_text_gate(QA_LANGUAGE, d, tmp, BOOK_FIXTURE)
    rep.check(code != 0, "⭑ TESTÇİ YOKKEN 'PASSED' BEYANI YAKALANIR", out)


SEAL_KEY_FIXTURE = {
    "version": "selftest",
    "seals": [
        {"sealId": "seal-jaguar-condor", "region": "jaguar-condor",
         "word": "CONDOR", "letterCount": 6,
         "notchPosition": 3, "notchLetter": "N"},
    ],
    "finalQuest": {"id": "the-cartographers-seal", "word": "N", "letterCount": 1},
}


def part13_progression(rep: Report, tmp: str, base: dict) -> None:
    print("\n⑬ MÜHÜR VE KURTARMA kapısı ısırıyor mu")

    # Sentetik anahtar yalnızca TEK bölge taşır; diğer bölgeler yazılmamış
    # sayılır ve final sözcük tek harftir. Gerçek anahtar depoda YOKTUR.
    one_region = copy.deepcopy(base)
    idx = one_region["01_SOURCE/activity_index.json"]
    reg = one_region["01_SOURCE/region_index.json"]
    reg["regions"] = [r for r in reg["regions"] if r["id"] == "jaguar-condor"]
    idx["activities"] = [a for a in idx["activities"]
                         if a.get("region") == "jaguar-condor"]

    book = {"meta": {"language": "en"}, "activities": []}
    for a in idx["activities"]:
        if not a.get("sealSlot"):
            continue
        book["activities"].append({"activityId": a["activityId"]})
    # Yıldızlı sözcükleri CONDOR'u kuracak biçimde ver.
    letters = "CONDOR"
    for e in book["activities"]:
        slot = next(a["sealSlot"] for a in idx["activities"]
                    if a["activityId"] == e["activityId"])
        e["sealStarWord"] = letters[slot - 1].lower() + "word"
        e["sealStarIndex"] = 1
        e["sealContribution"] = letters[slot - 1]

    code, out = run_text_gate(QA_PROGRESSION, one_region, tmp, book,
                              SEAL_KEY_FIXTURE)
    rep.check(code == 0, "temiz mühür kurgusu GEÇER", out)

    # (a) anahtar yokken kapı ATLAR, kırmızı yanmaz (K10)
    code, out = run_text_gate(QA_PROGRESSION, one_region, tmp, book, None)
    rep.check(code == 0, "cevap anahtarı yokken kapı atlar", out)

    # (b) ⭑ BOŞ YUVA — çocuk bölgeyi bitiremez
    d = copy.deepcopy(one_region)
    for a in d["01_SOURCE/activity_index.json"]["activities"]:
        if a.get("sealSlot") == 4:
            a.pop("sealSlot")
            break
    code, out = run_text_gate(QA_PROGRESSION, d, tmp, book, SEAL_KEY_FIXTURE)
    rep.check(code != 0, "⭑ BOŞ MÜHÜR YUVASI YAKALANIR", out)

    # (c) ⭑ HASAR YARIÇAPI — bir aktivite iki yuva besliyor
    #     Tek bir hata İKİ harfi bozar ve çocuk hangi sayfaya döneceğini
    #     bulamaz. Bu, "felâket kapısı yok" ölçütünün ihlalidir.
    d = copy.deepcopy(one_region)
    acts = d["01_SOURCE/activity_index.json"]["activities"]
    donor = next(a for a in acts if a.get("sealSlot") == 6)
    taker = next(a for a in acts if a.get("sealSlot") == 5)
    donor.pop("sealSlot")
    taker["sealSlot"] = 5
    dup = copy.deepcopy(taker)
    dup["activityId"] = taker["activityId"]
    acts.append({**taker, "sealSlot": 6})
    code, out = run_text_gate(QA_PROGRESSION, d, tmp, book, SEAL_KEY_FIXTURE)
    rep.check(code != 0, "⭑ TEK AKTİVİTE İKİ YUVA BESLEYEMEZ (hasar yarıçapı 2)",
              out)

    # (d) türetilen harf bölge sözcüğüyle uyuşmuyor
    d = copy.deepcopy(book)
    d["activities"][0]["sealStarWord"] = "zebra"
    d["activities"][0]["sealStarIndex"] = 1
    code, out = run_text_gate(QA_PROGRESSION, one_region, tmp, d,
                              SEAL_KEY_FIXTURE)
    rep.check(code != 0, "⭑ YANLIŞ TÜRETİLEN MÜHÜR HARFİ YAKALANIR", out)

    # (e) çentik harfi sözcükle uyuşmuyor
    k = copy.deepcopy(SEAL_KEY_FIXTURE)
    k["seals"][0]["notchLetter"] = "Z"
    code, out = run_text_gate(QA_PROGRESSION, one_region, tmp, book, k)
    rep.check(code != 0, "YANLIŞ ÇENTİK HARFİ YAKALANIR", out)

    # (f) ⭑ ZİNCİRLEME SAYFA — tek hata çocuğu kilitler
    d = copy.deepcopy(book)
    d["activities"][1]["prompt"] = ("Your mission: use your answer from page 1 "
                                    "to label the garden.")
    d["activities"][1]["steps"] = ["Write the four labels from the word bank."]
    code, out = run_text_gate(QA_PROGRESSION, one_region, tmp, d,
                              SEAL_KEY_FIXTURE)
    rep.check(code != 0, "⭑ ZİNCİRLEME BAĞIMLILIK YAKALANIR "
                         "(bir hata kitabı kilitleyemez)", out)

    # (g) tek hatadan kurtarılamayacak kadar kısa mühür sözcüğü
    k = copy.deepcopy(SEAL_KEY_FIXTURE)
    k["seals"][0]["word"] = "CON"
    k["seals"][0]["letterCount"] = 3
    k["seals"][0]["notchPosition"] = 3
    k["seals"][0]["notchLetter"] = "N"
    code, out = run_text_gate(QA_PROGRESSION, one_region, tmp, book, k)
    rep.check(code != 0, "KURTARILAMAYACAK KADAR KISA MÜHÜR SÖZCÜĞÜ YAKALANIR",
              out)


# ═══════════════════════════════════════════════════════════════════════════
# FAZ 3 · ⑭ KURUCU FAZ AŞMASI BİR KİLİT MİDİR
#
# Bir aşma kaydı iki şeyden biri olabilir:
#
#     KİLİT   → aşmayı görünür tutar ve yan etkilerini engeller
#     KAÇIŞ   → "kurucu izin verdi" diyerek her kapıyı açar
#
# İkincisi bu projeyi bitirir: bir kez "kurucu izin verdi" bir gerekçe
# olarak kabul edilirse, çocuk testi de öyle atlanır.
#
# Bu bölüm aşmanın bir KİLİT olduğunu kanıtlar: aşma etkinken kapı
# yükselemez, dış doğrulama 'passed' olamaz, blokaj kapanamaz ve aşma
# belgeden düşemez.
# ═══════════════════════════════════════════════════════════════════════════
def run_spec_override(cfg: dict, gate: str, docs: dict, tmp: str) -> tuple[int, str]:
    """validate_spec'i kurgu kök + kurgu BELGELERLE koşturur.

    `run_spec_with` belge yazmaz; aşma denetiminin dördüncü kilidi
    (belgede anılıyor mu) belge olmadan sınanamaz."""
    import shutil
    _RUN_SEQ[0] += 1
    root = os.path.join(tmp, "ovr-%03d" % _RUN_SEQ[0])
    for d in ("01_SOURCE", "04_BUILD", "06_REPORTS"):
        os.makedirs(os.path.join(root, d), exist_ok=True)
    with open(os.path.join(root, "project_config.json"), "w", encoding="utf-8") as fh:
        json.dump(cfg, fh, ensure_ascii=False)
    with open(os.path.join(root, "01_SOURCE", "activity_index.json"),
              "w", encoding="utf-8") as fh:
        json.dump(clean_games(cfg), fh, ensure_ascii=False)
    with open(os.path.join(root, ".gate"), "w", encoding="utf-8") as fh:
        fh.write(gate)
    for rel, body in docs.items():
        p = os.path.join(root, *rel.split("/"))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(body)
    dest = os.path.join(root, "04_BUILD", "validate_spec.py")
    shutil.copy2(VALIDATE_SPEC, dest)
    out = subprocess.run([sys.executable, dest, "--gate", gate],
                         capture_output=True, text=True, timeout=120)
    return out.returncode, out.stdout + out.stderr


def part14_phase_override(rep: Report, tmp: str) -> None:
    print("\n⑭ KURUCU FAZ AŞMASI bir kilit mi (kaçış kapısı değil)")

    base = clean_config()
    if not (base.get("founder", {}).get("phaseOverride") or {}).get("active"):
        print("  ⊘ etkin aşma yok — bölüm atlandı")
        return

    ov = base["founder"]["phaseOverride"]
    good_docs = {rel: "aşma kaydı: %s · ertelenen blokaj: %s\n"
                      % (ov["decision"], ov["deferredBlocker"])
                 for rel in ov.get("documentedIn", [])}

    # temiz aşma: tavanda duran kapı + anılmış belgeler → GEÇER
    code, out = run_spec_override(base, ov["gateCeiling"], good_docs, tmp)
    rep.check(code == 0, "temiz aşma kaydı GEÇER", out)

    # (a) kapı tavanı — aşma kapıyı yükseltmek için KULLANILAMAZ
    order = ["phase0", "phase1", "phase2", "phase3", "phase4", "phase5", "release"]
    higher = order[min(order.index(ov["gateCeiling"]) + 1, len(order) - 1)]
    code, out = run_spec_override(base, higher, good_docs, tmp)
    rep.check(code != 0, "⭑ AŞMAYLA KAPI YÜKSELTME YAKALANIR (%s > %s)"
              % (higher, ov["gateCeiling"]), out)

    # (b) dış doğrulama 'passed' — aşma bir testi geçmiş saydıramaz
    d = copy.deepcopy(base)
    d["founder"]["childTesters"]["externalValidation"] = "passed"
    code, out = run_spec_override(d, ov["gateCeiling"], good_docs, tmp)
    rep.check(code != 0, "⭑ AŞMA ETKİNKEN 'passed' BEYANI YAKALANIR", out)

    # (c) ertelenen blokaj kapanmış GÖRÜNEMEZ
    d = copy.deepcopy(base)
    d["founder"]["phaseOverride"]["deferredBlockerStatus"] = "closed"
    code, out = run_spec_override(d, ov["gateCeiling"], good_docs, tmp)
    rep.check(code != 0, "⭑ ERTELENEN BLOKAJIN KAPATILMASI YAKALANIR", out)

    # (d) SESSİZ AŞMA — belgeden düşen bir aşma, unutulan bir aşmadır
    silent = dict(good_docs)
    first = next(iter(silent))
    silent[first] = "bu belge aşmadan hiç söz etmiyor\n"
    code, out = run_spec_override(base, ov["gateCeiling"], silent, tmp)
    rep.check(code != 0, "⭑ BELGEDE ANILMAYAN AŞMA YAKALANIR (%s)" % first, out)

    # (e) eksik alan — gerekçesiz bir aşma bir aşma değildir
    d = copy.deepcopy(base)
    d["founder"]["phaseOverride"]["reason"] = ""
    code, out = run_spec_override(d, ov["gateCeiling"], good_docs, tmp)
    rep.check(code != 0, "GEREKÇESİZ AŞMA YAKALANIR", out)

    # (f) aşma kapatılınca denetim boş koşar ve kapı normale döner
    d = without_override(base)
    code, out = run_spec_override(d, "phase1", {}, tmp)
    rep.check(code == 0, "aşma yokken denetim boş koşar", out)


# ═══════════════════════════════════════════════════════════════════════════
# FAZ 3 · ⑮ TEKRAR VE KÜLTÜREL DÜZLEŞME (qa_echo)
#
# Bu kapının iki ayrı yoldan yanlış olma ihtimali var ve ikisi de test
# edilmek zorunda:
#
#   ① kusuru KAÇIRIR   → altı bölge tek sesle okunur ve kimse görmez
#   ② kusursuzu SUÇLAR → yazar kültür adını silmeye başlar
#
# İkincisi daha tehlikelidir çünkü kapıyı susturmanın yolu ATIFI
# ZAYIFLATMAKTIR ve `qa_age § ⑨` tam tersini şart koşuyor. (h) maddesi
# bunu ayrıca kanıtlıyor: kültür adını ve yazı dizgesi terimini her
# sayfada tekrarlayan bir kurgu GEÇMEK ZORUNDADIR.
# ═══════════════════════════════════════════════════════════════════════════
QA_ECHO = os.path.join(BUILD, "qa_echo.py")

_ECHO_IDS = ["maya-bar-dot-numbers", "maya-ballcourt-plate", "maya-number-add",
             "aztec-chinampa-plate", "aztec-place-glyphs", "aztec-lake-city-map"]
_ECHO_NOTES = [
    "The Maya wrote numbers with three signs. A dot is one, a bar is five, and a shell means none.",
    "A ball court is cut into the ground between two stone walls. Players used their hips.",
    "Adding in this system needs a swap. Five loose dots become one bar and the count moves up.",
    "These Aztec lake gardens do not float, though people often say they do. Willows edge every plot.",
    "A place sign is built from small pictures. Read the pictures and the name comes out of them.",
    "Water decided where this city could grow. Causeways carried people over the lake in four directions.",
]
_ECHO_PROMPTS = [
    "Your mission: read the six numbers on the market plate.",
    "Your mission: label the parts of a ball court.",
    "Your mission: add two Maya numbers together.",
    "Your mission: find what holds a lake garden in place.",
    "Your mission: work out three place signs.",
    "Your mission: trace four causeways across the lake.",
]
_ECHO_STEPS = [
    ["Count the dots beside each basket.", "Write each total on its line."],
    ["Write each label on the line beside its part.", "Mark the sloping wall."],
    ["Swap five loose dots for one bar.", "Write the new total on the line."],
    ["Write the four labels from the word bank.", "Mark what holds the plot."],
    ["Read each small picture in the sign.", "Write the name on the line."],
    ["Trace each causeway to the shore.", "Mark where the water is fresh."],
]


def echo_fixture(n: int = 6) -> dict:
    return {"meta": {"kind": "selftest-echo", "language": "en"},
            "activities": [{"activityId": _ECHO_IDS[i],
                            "prompt": _ECHO_PROMPTS[i],
                            "fieldNote": _ECHO_NOTES[i],
                            "steps": list(_ECHO_STEPS[i]),
                            "answer": "field %d" % i,
                            "writingSpaceLines": 4,
                            "pagePrints": ["a plate"]} for i in range(n)]}


def part15_echo(rep: Report, tmp: str, base: dict) -> None:
    print("\n⑮ TEKRAR VE KÜLTÜREL DÜZLEŞME kapısı ısırıyor mu")

    code, out = run_text_gate(QA_ECHO, base, tmp, echo_fixture())
    rep.check(code == 0, "temiz sentetik kurgu GEÇER", out)

    code, out = run_text_gate(QA_ECHO, base, tmp, None)
    rep.check(code == 0, "manuscript yokken kapı boş koşar", out)

    # (a) AÇILIŞ KALIBI — dört sayfa, iki kültür, aynı iskelet
    d = echo_fixture()
    for i in range(4):
        d["activities"][i]["fieldNote"] = (
            "In this account the people of the valley kept a careful "
            "record of number %d and its meaning." % i)
    code, out = run_text_gate(QA_ECHO, base, tmp, d)
    rep.check(code != 0, "⭑ AYNI FIELD NOTE AÇILIŞI YAKALANIR", out)

    # (b) GÖREV KALIBI — beş sayfa aynı biçimle açılıyor
    d = echo_fixture()
    for i in range(5):
        d["activities"][i]["prompt"] = (
            "Your mission: work out the meaning of item %d." % i)
    code, out = run_text_gate(QA_ECHO, base, tmp, d)
    rep.check(code != 0, "⭑ AYNI GÖREV SATIRI KALIBI YAKALANIR", out)

    # (c) DÜZLEŞTİRİCİ DİL — tek bir cümle yeter
    d = echo_fixture()
    d["activities"][1]["fieldNote"] = (
        "These ancient peoples believed the ball court was a door. "
        "Their strange customs are still a mystery to us.")
    code, out = run_text_gate(QA_ECHO, base, tmp, d)
    rep.check(code != 0, "⭑ KÜLTÜREL DÜZLEŞTİRME YAKALANIR", out)

    # (d) SAYFA ÖRTÜŞMESİ — iki field note neredeyse aynı
    d = echo_fixture()
    d["activities"][4]["fieldNote"] = d["activities"][0]["fieldNote"].replace(
        "three signs", "three marks")
    code, out = run_text_gate(QA_ECHO, base, tmp, d)
    rep.check(code != 0, "⭑ NEREDEYSE AYNI FIELD NOTE YAKALANIR", out)

    # (e) BEYANSIZ NAKARAT — birebir aynı adım üç sayfada
    d = echo_fixture()
    for i in (0, 2, 4):
        d["activities"][i]["steps"][1] = "Write the finding in the record box."
    code, out = run_text_gate(QA_ECHO, base, tmp, d)
    rep.check(code != 0, "⭑ BEYAN EDİLMEMİŞ NAKARAT YAKALANIR", out)

    # (f) NAKARAT PAYI — beyan edilmiş bir kalıp kitabı ele geçiriyor
    d = echo_fixture()
    for i in range(5):
        d["activities"][i]["steps"][1] = "Copy the word into the star box."
    code, out = run_text_gate(QA_ECHO, base, tmp, d)
    rep.check(code != 0, "⭑ NAKARAT SAYFALARIN ÇOĞUNU KAPLARSA YAKALANIR", out)

    # (g) TEK KAYNAKLI KÜLTÜR — daha SIKI eşik gerçekten sıkı mı
    #     Genel eşiğin (0,55) altında ama tek kaynaklı eşiğin (0,40)
    #     üstünde kalan bir çift, YALNIZCA tek kaynaklı kültürde yanmalı.
    d = echo_fixture()
    d["activities"] = [
        {"activityId": "andean-khipu-knots",
         "prompt": "Your mission: read four knotted cords.",
         "fieldNote": "A cord counts in tens along its length. Knots sit in "
                      "places and the lowest place is nearest the end.",
         "steps": ["Count the knots in each place."], "answer": "a",
         "writingSpaceLines": 4, "pagePrints": ["cords"]},
        {"activityId": "andean-altitude-map",
         "prompt": "Your mission: sort four crops by height.",
         "fieldNote": "A cord counts in tens along its length. Knots sit in "
                      "bands and the lowest band is nearest the valley.",
         "steps": ["Count the bands on each side."], "answer": "b",
         "writingSpaceLines": 4, "pagePrints": ["bands"]},
    ]
    code, out = run_text_gate(QA_ECHO, base, tmp, d)
    rep.check(code != 0, "⭑ TEK KAYNAKLI KÜLTÜRDE TEKRAR YAKALANIR", out)

    # (h) ⭑ YANLIŞ POZİTİF YOK ⭑
    #     Kültür adını ve yazı dizgesi terimini HER sayfada tekrarlayan
    #     bir kurgu GEÇMEK ZORUNDADIR. qa_age § ⑨ atıfı şart koşuyor ve
    #     iki kapı birbirine ters çalışamaz.
    d = echo_fixture()
    for i, a in enumerate(d["activities"]):
        a["fieldNote"] = ("The Maya used bar and dot numerals here. "
                          + _ECHO_NOTES[i]) if i < 3 else (
                         "Aztec scribes used Nahuatl place glyphs here. "
                          + _ECHO_NOTES[i])
    code, out = run_text_gate(QA_ECHO, base, tmp, d)
    rep.check(code == 0,
              "⭑ ZORUNLU KÜLTÜREL TERİM TEKRARI CEZALANDIRILMAZ", out)



# ═══════════════════════════════════════════════════════════════════════════
# FAZ 3 · ⑯ TASARIM DİZGESİ VE GÖRSEL ŞARTNAMESİ (qa_design)
#
# Bu kapının koruduğu şey bir belge değil bir GERİLİMDİR:
#
#     yapı tutarlılığı  ⇄  kültürel çeşitlilik
#
# İki yönde de kırılabilir ve iki yön de sınanıyor:
#   · modül düşerse (mühür kutusu, açılış kuralı) → çocuk kuralı öğrenemez
#   · düzen tekleşirse                            → altı bölge tek şablon olur
#
# (g) maddesi ikincisini kanıtlıyor: beş TİPİ de dolu, bütün sayfaları
# aynı DÜZENDE olan bir bölge `qa_matrix`ten geçer ve buradan GEÇMEZ.
# ═══════════════════════════════════════════════════════════════════════════
QA_DESIGN = os.path.join(BUILD, "qa_design.py")

_DS_OPENING = {
    "regionId": "jaguar-condor",
    "heading": "Jaguar and Condor",
    "terrainLine": "Rainforest over pale rock in the north, thin cold air in the south.",
    "openingText": " ".join(["Two lands that never met lie side by side in this "
                             "region and the ground explains both of them."] * 6)
                   + " Six pages have a star box. Write the word in the box. "
                     "The number in the star says which letter to copy into the "
                     "seal slot with the same number.",
}


def _ds_page(aid, layout, seal=None, star=None, idx=None, labels=("alpha", "beta")):
    p = {"activityId": aid,
         "prompt": "Your mission: read the plate.",
         "fieldNote": "A field note that carries twenty words so the register "
                      "band is not the thing under test here at all.",
         "steps": ["Read each sign on the plate."],
         "answer": "alpha · beta",
         "layout": layout,
         "writingSpaceLines": 4,
         "pagePrints": ["a plate with a key: alpha, beta"],
         "visualSpec": {
             "assetId": "fig-" + aid, "visualClass": "diagram", "layout": layout,
             "purpose": "Print the plate.", "subject": "a plate",
             "requiredLabels": list(labels), "orientation": "portrait",
             "targetPx": [1950, 2550], "aspect": "13:17",
             "safeAreaMm": {"bleed": 3.2}, "restrictions": ["no answer", "no faces"],
             "format": "png", "filename": "fig-" + aid + ".png",
             "destination": "07_ASSETS/processed/interior/",
             "status": "specified-not-produced"},
         }
    if seal:
        p.update({"sealSlot": seal, "sealStarWord": star, "sealStarIndex": idx,
                  "sealContribution": star[idx - 1].upper()})
        p["answer"] = "alpha · beta · star box: " + star
        p["pagePrints"].append(
            "star box drawn as %d letter squares, square %d outlined, "
            "marked \u2605%d \u2192 seal slot %d" % (len(star), idx, seal, seal))
        p["pagePrints"].append("a label printed on the plate: " + star)
    return p


def design_fixture():
    """Gerçek jaguar-condor kimlikleriyle kurulmuş temiz bir tasarım kurgusu."""
    return {"meta": {"kind": "selftest-design", "language": "en"},
            "regionOpenings": [dict(_DS_OPENING)],
            "activities": [
                _ds_page("maya-bar-dot-numbers", "key-decode", 1, "chilli", 1),
                _ds_page("maya-ballcourt-plate", "plate-label"),
                _ds_page("maya-number-make", "make-frame", labels=()),
                _ds_page("maya-ballcourt-sort", "sort-cards", labels=()),
                _ds_page("aztec-lake-city-map", "map-trace"),
            ]}


def part16_design(rep: Report, tmp: str, base: dict) -> None:
    print("\n\u2470 TASARIM DİZGESİ kapısı ısırıyor mu")

    code, out = run_text_gate(QA_DESIGN, base, tmp, design_fixture())
    rep.check(code == 0, "temiz tasarım kurgusu GEÇER", out)

    code, out = run_text_gate(QA_DESIGN, base, tmp, None)
    rep.check(code == 0, "manuscript yokken kapı boş koşar", out)

    # (a) ⭑ MÜHÜR KURALI AÇILIŞTAN DÜŞERSE ⭑ — Faz 2'nin 1 numaralı
    #     bloklayıcısı buydu ve bir daha sessizce olamaz.
    d = design_fixture()
    d["regionOpenings"][0]["openingText"] = " ".join(
        ["Two lands that never met lie side by side in this region here."] * 12)
    code, out = run_text_gate(QA_DESIGN, base, tmp, d)
    rep.check(code != 0, "⭑ AÇILIŞTA BASILMAYAN MÜHÜR KURALI YAKALANIR", out)

    # (b) açılış bandı
    d = design_fixture()
    d["regionOpenings"][0]["openingText"] = ("Star box, seal slot, letter. "
                                             "That is the whole opening.")
    code, out = run_text_gate(QA_DESIGN, base, tmp, d)
    rep.check(code != 0, "BANT DIŞI BÖLGE AÇILIŞI YAKALANIR", out)

    # (c) yıldızlı kutu levhadan düştü
    d = design_fixture()
    d["activities"][0]["pagePrints"] = ["a plate with a key: alpha, beta",
                                        "a label printed on the plate: chilli"]
    code, out = run_text_gate(QA_DESIGN, base, tmp, d)
    rep.check(code != 0, "⭑ LEVHADA TARİF EDİLMEYEN YILDIZLI KUTU YAKALANIR", out)

    # (d) levhadaki yuva numarası kayıtla çelişiyor
    d = design_fixture()
    d["activities"][0]["pagePrints"][1] = (
        "star box drawn as 6 letter squares, square 1 outlined, "
        "marked \u26051 \u2192 seal slot 4")
    code, out = run_text_gate(QA_DESIGN, base, tmp, d)
    rep.check(code != 0, "⭑ LEVHA İLE KAYIT ARASINDAKİ YUVA ÇELİŞKİSİ YAKALANIR", out)

    # (e) ⭑ YILDIZLI SÖZCÜK LEVHADA BASILI DEĞİL ⭑
    #     Basılmayan bir sözcük kopyalanamaz, ÜRETİLİR — ve yanlış yazılır.
    d = design_fixture()
    d["activities"][0]["pagePrints"] = [x for x in d["activities"][0]["pagePrints"]
                                        if not x.startswith("a label printed")]
    code, out = run_text_gate(QA_DESIGN, base, tmp, d)
    rep.check(code != 0, "⭑ LEVHADA BASILMAYAN YILDIZLI SÖZCÜK YAKALANIR", out)

    # (f) düzen tipe izinli değil
    d = design_fixture()
    d["activities"][1]["layout"] = "key-decode"
    d["activities"][1]["visualSpec"]["layout"] = "key-decode"
    code, out = run_text_gate(QA_DESIGN, base, tmp, d)
    rep.check(code != 0, "⭑ TİPİNE İZİNSİZ DÜZEN YAKALANIR", out)

    # (g) ⭑ ŞABLONLAŞMA ⭑ — beş tipin hepsi dolu, düzen TEK.
    #     qa_matrix bunu göremez; tip ile düzen aynı şey değildir.
    d = design_fixture()
    for a in d["activities"]:
        a["layout"] = "make-frame"
        a["visualSpec"]["layout"] = "make-frame"
        a.pop("sealSlot", None)
    code, out = run_text_gate(QA_DESIGN, base, tmp, d)
    rep.check(code != 0, "⭑ TEK DÜZENE ÇÖKMÜŞ BÖLGE YAKALANIR", out)

    # (h) görsel şartnamesi eksik
    d = design_fixture()
    d["activities"][2].pop("visualSpec")
    code, out = run_text_gate(QA_DESIGN, base, tmp, d)
    rep.check(code != 0, "⭑ ŞARTNAMESİZ SAYFA YAKALANIR", out)

    # (i) şartname var ama alanları eksik
    d = design_fixture()
    d["activities"][2]["visualSpec"].pop("safeAreaMm")
    code, out = run_text_gate(QA_DESIGN, base, tmp, d)
    rep.check(code != 0, "EKSİK ALANLI ŞARTNAME YAKALANIR", out)

    # (j) etiket gerektiren bir düzen etiket saymıyor
    d = design_fixture()
    d["activities"][1]["visualSpec"]["requiredLabels"] = []
    code, out = run_text_gate(QA_DESIGN, base, tmp, d)
    rep.check(code != 0, "⭑ ETİKETSİZ LEVHA ŞARTNAMESİ YAKALANIR", out)

    # (k) assetId yinelendi
    d = design_fixture()
    d["activities"][1]["visualSpec"]["assetId"] = \
        d["activities"][0]["visualSpec"]["assetId"]
    code, out = run_text_gate(QA_DESIGN, base, tmp, d)
    rep.check(code != 0, "YİNELENEN assetId YAKALANIR", out)

    # (l) dosya adı sözleşme dışı
    d = design_fixture()
    d["activities"][1]["visualSpec"]["filename"] = "plate.png"
    code, out = run_text_gate(QA_DESIGN, base, tmp, d)
    rep.check(code != 0, "SÖZLEŞME DIŞI DOSYA ADI YAKALANIR", out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    print("=" * 74)
    print("  KAPILARIN KENDİ TESTİ · The Myth Hunter's Field Book")
    print("=" * 74)

    rep = Report(args.verbose)
    with tempfile.TemporaryDirectory() as tmp:
        part1_clean_passes(rep, tmp)
        part2_flaws_caught(rep, tmp)
        part3_gates_lock(rep, tmp)

        # ⑤–⑧ gerçek dizinleri temiz kurgu olarak kullanır. Dizinler
        # henüz üretilmediyse (Faz 0) bu bölümler ATLANIR — ama kapı
        # betikleri VARSA atlanamaz: var olan bir kapı test edilmeden
        # kullanılamaz (World Myths D7).
        gates = [("qa_age.py", QA_AGE), ("qa_matrix.py", QA_MATRIX),
                 ("validate_research.py", VALIDATE_RESEARCH),
                 ("page_budget.py", PAGE_BUDGET)]
        present = [n for n, p in gates if os.path.isfile(p)]
        if not real_data_available():
            if present:
                rep.check(False,
                          "Faz 1 kapıları var ama dizinler yok — TEST EDİLEMEYEN "
                          "KAPI: %s" % present)
            else:
                print("\n⑤–⑧ Faz 1 kapıları henüz doğmadı — ATLANDI")
        else:
            base = with_config(load_real())
            if os.path.isfile(QA_AGE):
                part5_age_gate(rep, tmp, base)
            if os.path.isfile(QA_MATRIX):
                part6_matrix_gate(rep, tmp, base)
            if os.path.isfile(VALIDATE_RESEARCH):
                part7_research_gate(rep, tmp, base)
            if os.path.isfile(PAGE_BUDGET):
                part8_page_budget(rep, tmp, base)
        if os.path.isfile(QA_READABILITY):
            part9_readability(rep, tmp)

        # ⑩–⑬ Faz 2 kapıları. Kapı VARSA test edilmek ZORUNDADIR:
        # test edilmemiş bir kapı yok sayılır (D7).
        p2 = [("qa_solvable.py", QA_SOLVABLE), ("qa_instruction.py", QA_INSTRUCTION),
              ("qa_language.py", QA_LANGUAGE), ("qa_progression.py", QA_PROGRESSION)]
        p2_present = [n for n, p in p2 if os.path.isfile(p)]
        if p2_present and not real_data_available():
            rep.check(False, "Faz 2 kapıları var ama dizinler yok — "
                             "TEST EDİLEMEYEN KAPI: %s" % p2_present)
        elif p2_present:
            base2 = with_config(load_real())
            if os.path.isfile(QA_SOLVABLE):
                part10_solvable(rep, tmp, base2)
            if os.path.isfile(QA_INSTRUCTION):
                part11_instruction(rep, tmp, base2)
            if os.path.isfile(CHILD_PACK):
                part11b_test_pack(rep, tmp, base2)
            if os.path.isfile(QA_LANGUAGE):
                part12_language(rep, tmp, base2)
            if os.path.isfile(QA_PROGRESSION):
                part13_progression(rep, tmp, base2)
            if os.path.isfile(QA_AGE):
                part5b_attribution(rep, tmp, base2)
        else:
            print("\n⑩–⑬ Faz 2 kapıları henüz doğmadı — ATLANDI")

        # ⑭–⑯ Faz 3 kapıları
        part14_phase_override(rep, tmp)
        p3 = [("qa_echo.py", QA_ECHO), ("qa_design.py", QA_DESIGN)]
        p3_present = [n for n, q in p3 if os.path.isfile(q)]
        if p3_present and not real_data_available():
            rep.check(False, "Faz 3 kapıları var ama dizinler yok — "
                             "TEST EDİLEMEYEN KAPI: %s" % p3_present)
        elif p3_present:
            base3 = with_config(load_real())
            if os.path.isfile(QA_ECHO):
                part15_echo(rep, tmp, base3)
            if os.path.isfile(QA_DESIGN):
                part16_design(rep, tmp, base3)

    part4_no_dead_exemptions(rep)

    print("\n" + "=" * 74)
    if rep.failed:
        print("  ⛔ %d KÖRLÜK BULUNDU (%d denetim geçti)"
              % (len(rep.failed), rep.passed))
        for f in rep.failed:
            print("     · %s" % f)
        print("=" * 74)
        print("\n  Bir kapı kusuru yakalamıyorsa, o kapı YOK demektir.")
        return 1
    print("  ✅ %d denetim yeşil — bütün kapılar ısırıyor" % rep.passed)
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
