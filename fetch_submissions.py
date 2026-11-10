#!/usr/bin/env python3
"""Récupère les articles proposés par les visiteurs et validés (status approved) -> data/submissions.json"""
import json, urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
CFG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
req = urllib.request.Request(CFG["supabase_url"] + "/rest/v1/rpc/lp_published_submissions", data=b"{}", method="POST",
    headers={"apikey": CFG["supabase_key"], "Authorization": "Bearer " + CFG["supabase_key"], "Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        rows = json.loads(r.read())
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "submissions.json").write_text(json.dumps(rows, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"{len(rows)} articles de visiteurs validés")
except Exception as e:
    print("ERR soumissions :", e, "(on garde le fichier précédent)")
