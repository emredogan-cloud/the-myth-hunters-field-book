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

Dokuz bölüm:
  ①  temiz kurgu BÜTÜN kapılardan geçer          (yanlış pozitif yok)
  ②  her kusurlu kurgu İLGİLİ kapıda yakalanır   (körlük yok)
  ③  kapı seviyeleri gerçekten kilitliyor        (kapsam kapıları)
  ④  her muafiyet en az bir kez DEVREYE GİRİYOR  (ölü kural yok)
  ⑤  YAŞ VE GÜVENLİK kapısı ısırıyor mu          (Faz 1'de doğdu)
  ⑥  MATRİS VE MÜHÜR kapısı ısırıyor mu          (Faz 1'de doğdu)
  ⑦  ARAŞTIRMA ZİNCİRİ kapısı ısırıyor mu        (Faz 1'de doğdu)
  ⑧  SAYFA BÜTÇESİ kapısı ısırıyor mu            (Faz 1'de doğdu)
  ⑨  OKUNABİLİRLİK kapısı ısırıyor mu            (Faz 1'de doğdu)

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


def part3_gates_lock(rep: Report, tmp: str) -> None:
    print("\n③ kapı seviyeleri gerçekten kilitliyor")

    cfg = clean_config()

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
