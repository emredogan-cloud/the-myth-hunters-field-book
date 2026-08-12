#!/usr/bin/env python3
"""
DEVRALMA BÜTÜNLÜĞÜ KAPISI — The Myth Hunter's Field Book
================================================================================
Bu kapı bu projeye ÖZGÜDÜR ve tek bir şeyi engellemek için vardır:

    DEVRALINAN VERİNİN SESSİZCE DOĞRULANMIŞ SAYILMASI.

Bu kitap `THE-GREAT-BOOK-OF-WORLD-MYTHS`'in 22 kültürlük kilitli araştırma
tabanından besleniyor ve bu, projenin maliyet avantajının TAMAMI. Ama:

    Bir hikâye anlatmak ile bir aktivite tasarlamak AYNI İDDİA DEĞİLDİR.

World Myths'te *"bu mitte X olur"* cümlesi anlatı için yeterlidir. Burada
aynı cümle bir BULMACA CEVABIDIR — yanlışsa çocuk kendini suçlar.

Bu yüzden devralma bir KOPYALAMA + KÖKEN KAYDIdır, canlı bağımlılık değil:

  · Devralınan her kayıt sha256 ile manifestoya yazılır
  · Kaynağın nereden geldiği (depo + yol) kayıtlıdır
  · Üç durumdan birini taşır ve `inherited-provisional` olan bir kayda
    dayanan aktivite LOCKED OLAMAZ

⚠ Bu betik World Myths deposunun VARLIĞINI GEREKTİRMEZ. Kardeş dizinde
bulunması zorunlu değildir; manifest kendi kendine yeterlidir. Depo varsa
sha256'lar ayrıca KARŞILAŞTIRILIR (--cross-check).

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CONFIG = os.path.join(ROOT, "project_config.json")
MANIFEST = os.path.join(ROOT, "01_SOURCE", "inherited", "IMPORT_MANIFEST.json")
ACTIVITY_INDEX = os.path.join(ROOT, "01_SOURCE", "activity_index.json")

VALID_STATUS = ["inherited-provisional", "inherited-verified", "new-researched"]
SHA256_HEX = 64


class Report:
    def __init__(self, verbose):
        self.verbose = verbose
        self.errors = []
        self.warnings = []
        self.checks = 0
        self.facts = {}

    def check(self, cond, label):
        self.checks += 1
        if cond:
            if self.verbose:
                print("  ✓ %s" % label)
        else:
            self.errors.append(label)
            print("  ✗ %s" % label)
        return cond

    def warn(self, label):
        self.warnings.append(label)
        print("  ! %s" % label)


def load_json(path, rep, required=True):
    if not os.path.exists(path):
        if required:
            rep.check(False, "dosya yok: %s" % os.path.relpath(path, ROOT))
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        rep.check(False, "JSON bozuk: %s — %s" % (os.path.relpath(path, ROOT), exc))
        return None


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def check_manifest(cfg, man, rep, cross_check):
    print("\n── devralma manifestosu ──")

    if man is None:
        rep.warn("IMPORT_MANIFEST.json yok — Faz 1 teslimatı; devralma "
                 "denetimi boş koşuyor")
        rep.facts["records"] = 0
        return

    records = man.get("records", []) if isinstance(man, dict) else man
    rep.facts["records"] = len(records)
    rep.check(isinstance(records, list), "manifest bir kayıt listesi taşıyor")

    src = man.get("sourceProject") if isinstance(man, dict) else None
    expected = cfg.get("project", {}).get("inheritsFrom", {}).get("project")
    rep.check(src == expected,
              "manifest kaynak projeyi doğru bildiriyor (%s)" % expected)

    require_sha = cfg.get("inheritance", {}).get("requireSha256", True)
    require_repo = cfg.get("inheritance", {}).get("requireSourceRepo", True)

    missing_sha, missing_repo, bad_status, bad_path = [], [], [], []
    for r in records:
        rid = r.get("recordId", "<kimliksiz>")
        sha = r.get("sourceSha256", "")
        if require_sha and (not isinstance(sha, str) or len(sha) != SHA256_HEX):
            missing_sha.append(rid)
        if require_repo and not r.get("sourceRepo"):
            missing_repo.append(rid)
        if r.get("status") not in VALID_STATUS:
            bad_status.append(rid)
        if not r.get("sourcePath"):
            bad_path.append(rid)

    rep.check(not missing_sha, "her kayıt sha256 taşıyor" +
              ("" if not missing_sha else " — EKSİK: %s" % missing_sha[:5]))
    rep.check(not missing_repo, "her kayıt kaynak deposunu bildiriyor" +
              ("" if not missing_repo else " — EKSİK: %s" % missing_repo[:5]))
    rep.check(not bad_path, "her kayıt kaynak yolunu bildiriyor" +
              ("" if not bad_path else " — EKSİK: %s" % bad_path[:5]))
    rep.check(not bad_status, "devralma durumları geçerli" +
              ("" if not bad_status else " — GEÇERSİZ: %s" % bad_status[:5]))

    ids = [r.get("recordId") for r in records]
    rep.check(len(ids) == len(set(ids)), "kayıt kimlikleri tekil")

    for st in VALID_STATUS:
        rep.facts["status_%s" % st] = sum(1 for r in records if r.get("status") == st)

    # Doğrulama oranı — Faz 1 PASS ölçütü (%80)
    if records:
        verified = rep.facts.get("status_inherited-verified", 0) \
                   + rep.facts.get("status_new-researched", 0)
        ratio = verified / len(records)
        rep.facts["verified_ratio"] = round(ratio, 3)
        print("  · doğrulanmış oran: %.1f%% (%d/%d)"
              % (ratio * 100, verified, len(records)))

    # ÇAPRAZ DENETİM — yalnızca kaynak depo GERÇEKTEN varsa
    if cross_check:
        base = man.get("sourceRoot") if isinstance(man, dict) else None
        if not base:
            rep.warn("--cross-check istendi ama manifest sourceRoot taşımıyor")
            return
        base_abs = os.path.normpath(os.path.join(ROOT, base))
        if not os.path.isdir(base_abs):
            rep.warn("kaynak depo bu makinede yok (%s) — çapraz denetim ATLANDI. "
                     "Bu bir kusur DEĞİLDİR: proje kaynak deposu olmadan da "
                     "build alır." % base)
            return
        drifted = []
        for r in records:
            p = os.path.join(base_abs, r.get("sourcePath", ""))
            if not os.path.isfile(p):
                drifted.append("%s (kaynak dosya yok)" % r.get("recordId"))
                continue
            if sha256_of(p) != r.get("sourceSha256"):
                drifted.append("%s (sha256 DEĞİŞMİŞ)" % r.get("recordId"))
        rep.check(not drifted, "kaynak dosyalar manifestteki sha256 ile aynı" +
                  ("" if not drifted else " — SÜRÜKLENME: %s" % drifted[:5]))


def check_lock_rule(cfg, man, acts, rep):
    print("\n── devralma kilidi ──")
    if acts is None or man is None:
        rep.warn("envanter veya manifest yok — kilit denetimi boş koşuyor")
        return

    records = man.get("records", []) if isinstance(man, dict) else man
    by_id = {r.get("recordId"): r for r in records}
    entries = acts.get("activities", []) if isinstance(acts, dict) else acts
    lock_ok = set(cfg["inheritance"]["lockRequiresStatus"])

    violators = []
    for a in entries:
        if a.get("status") not in ("locked", "written"):
            continue
        for rid in a.get("inheritedRecords", []) or []:
            rec = by_id.get(rid)
            if rec is None:
                violators.append("%s → manifestte olmayan kayıt %s"
                                 % (a.get("activityId"), rid))
            elif rec.get("status") not in lock_ok:
                violators.append("%s → %s (%s)"
                                 % (a.get("activityId"), rid, rec.get("status")))

    rep.check(not violators,
              "DOĞRULANMAMIŞ kayda dayanan locked aktivite yok" +
              ("" if not violators else " — İHLAL: %s" % violators[:5]))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--cross-check", action="store_true",
                    help="kaynak depo varsa sha256'ları karşılaştır")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    print("=" * 74)
    print("  DEVRALMA BÜTÜNLÜĞÜ")
    print("=" * 74)

    rep = Report(args.verbose)
    cfg = load_json(CONFIG, rep)
    if cfg is None:
        return 1

    man = load_json(MANIFEST, rep, required=False)
    acts = load_json(ACTIVITY_INDEX, rep, required=False)

    check_manifest(cfg, man, rep, args.cross_check)
    check_lock_rule(cfg, man, acts, rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil" % rep.checks)
        status = "pass"
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": status, "checks": rep.checks,
                       "errors": rep.errors, "warnings": rep.warnings,
                       "facts": rep.facts}, fh, ensure_ascii=False, indent=2)
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
