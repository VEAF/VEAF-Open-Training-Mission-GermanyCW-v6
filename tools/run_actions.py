"""Run a batch of veaf-mission-mcp actions in-process, through the same catalogue the server uses.

Usage: python run_actions.py batch.json  (a list of {"name": ..., "params": {...}})
Stops at the first error. Prints a one-line summary per action, plus any warnings.
"""

import json
import sys

import paths  # noqa: E402,F401  (puts VMCT on sys.path)

from veaf_mission_mcp.actions import register_default_actions  # noqa: E402
from veaf_mission_mcp.catalog import ActionCatalog  # noqa: E402

catalog = ActionCatalog()
register_default_actions(catalog)

batch = json.load(open(sys.argv[1], encoding="utf-8"))
for i, item in enumerate(batch, 1):
    try:
        res = catalog.run_action(item["name"], item["params"])
    except Exception as exc:  # report and stop: a half-applied batch must be visible
        print(f"[{i}] {item['name']} FAILED: {exc!r}")
        sys.exit(1)
    summary = {k: v for k, v in (res or {}).items() if k not in ("route", "units", "groups")} if isinstance(res, dict) else res
    text = json.dumps(summary, ensure_ascii=False, default=str)
    print(f"[{i}] {item['name']}: {text[:300]}")
