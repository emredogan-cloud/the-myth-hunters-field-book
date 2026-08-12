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

Dört bölüm:
  ①  temiz kurgu BÜTÜN kapılardan geçer          (yanlış pozitif yok)
  ②  her kusurlu kurgu İLGİLİ kapıda yakalanır   (körlük yok)
  ③  kapı seviyeleri gerçekten kilitliyor        (kapsam kapıları)
  ④  her muafiyet en az bir kez DEVREYE GİRİYOR  (ölü kural yok)

④ doğrudan Bestiarium'un üç ölü kuralına ve World Myths'in K14 kararına
cevaptır: takip edilmeyen bir dosya için yazılmış muafiyet ÖLÜ MUAFİYETTİR
ve sessizce yanlış güven verir.

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
