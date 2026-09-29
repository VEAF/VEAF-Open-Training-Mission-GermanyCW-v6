"""Checks on the built .miz files (read with the VMCT reader, never by text search).

Usage (from the mission folder): python tools/verify.py [file.miz ...]
Without argument: the newest base .miz of the mission folder, then every weather variant of missions/.
"""

import collections
import glob
import os
import sys
import zipfile

from paths import ROOT, TOOLS  # noqa: E402  (also puts VMCT on sys.path)
from mission_tools.miz_tools import read_miz  # noqa: E402


def seq(v):
    return list(v.values()) if isinstance(v, dict) else list(v or [])


def groups(m):
    for side, co in m["coalition"].items():
        for c in seq(co.get("country")):
            for cat in ("plane", "helicopter", "vehicle", "ship", "static"):
                for g in seq((c.get(cat) or {}).get("group")):
                    yield side, c.get("name"), cat, g


def check(path, label):
    print(f"\n===== {label}: {path.split('/')[-1]}")
    miz = read_miz(path)
    m = miz.mission_content
    gnames, unames = collections.Counter(), collections.Counter()
    problems = []
    tanker_tasks = {}
    counts = collections.Counter()
    for side, country, cat, g in groups(m):
        gnames[g["name"]] += 1
        counts[(side, cat)] += 1
        for u in seq(g["units"]):
            unames[u["name"]] += 1
            if cat in ("plane", "helicopter") and not g.get("dynSpawnTemplate") and not g["name"].startswith("veafSpawn-"):
                on_deck = bool((seq(g["route"]["points"]) or [{}])[0].get("linkUnit"))  # carrier deck: alt 0 is right
                if (u.get("alt") or 0) <= 0 and not on_deck:
                    problems.append(f"alt<=0 {g['name']}")
                if not (u.get("payload") or {}).get("fuel"):
                    problems.append(f"no fuel {g['name']}")
            if cat == "static" and not u.get("category"):
                problems.append(f"static without category {g['name']} {u['type']}")
        if cat == "plane" and g["name"] in ("Texaco 1", "Arco 1", "Texaco 2", "Arco 2", "Shell 1", "Overlord 1", "Magic 1",
                                            "Tanker Rouge", "AWACS Rouge"):
            pts = seq(g["route"]["points"])
            ids = []
            for t in seq(pts[0]["task"]["params"]["tasks"]):
                ids.append(t["id"] if t["id"] != "WrappedAction" else t["params"]["action"]["id"])
            tanker_tasks[g["name"]] = ids
        if "convoi" in g["name"].lower() or "colonne" in g["name"].lower():
            pts = seq(g["route"]["points"])
            print("  convoy", g["name"], [p.get("action") for p in pts], len(seq(g["units"])), "units")
    gid, uid = collections.Counter(), collections.Counter()
    for _s, _c, _cat, _g in groups(m):
        gid[_g["groupId"]] += 1
        for _u in seq(_g["units"]):
            uid[_u["unitId"]] += 1
    print("  duplicate groupId:", sum(1 for c in gid.values() if c > 1), "| duplicate unitId:", sum(1 for c in uid.values() if c > 1))
    dup_g = [n for n, c in gnames.items() if c > 1]
    dup_u = [n for n, c in unames.items() if c > 1]
    print("  groups:", sum(gnames.values()), "| units:", sum(unames.values()), "| duplicate group names:", dup_g[:5],
          "| duplicate unit names:", dup_u[:5])
    print("  by side/category:", dict(counts))
    print("  support tasks:")
    for k, v in tanker_tasks.items():
        print("    ", k, v)
    print("  structural problems:", problems[:10], len(problems))
    wh = miz.warehouses_content
    dyn = []
    names = {}
    import json
    for a in json.load(open(TOOLS / "airfields.json")):
        names[a["id"]] = a["name"]
    for k, a in (wh.get("airports") or {}).items():
        if isinstance(a, dict) and a.get("dynamicSpawn"):
            dyn.append((names.get(int(k), k), a.get("coalition")))
    print("  dynamic slots on:", sorted(dyn))
    w = m["weather"]
    print("  weather: clouds.preset", w.get("clouds", {}).get("preset"), "| season.temperature", w.get("season", {}).get("temperature"),
          "| wind.atGround", w.get("wind", {}).get("atGround"), "| start_time", m.get("start_time"),
          f"({m.get('start_time', 0) // 3600:02d}:{m.get('start_time', 0) % 3600 // 60:02d})", "| date", m.get("date"))
    with zipfile.ZipFile(path) as z:
        cfg = [n for n in z.namelist() if n.endswith("veaf-config.lua")]
        txt = z.read(cfg[0]).decode("utf-8") if cfg else ""
    print("  veaf-config.lua:", cfg[:1], "| SecurityDisabled lines:", [l.strip() for l in txt.splitlines() if "SecurityDisabled" in l][:2],
          "| ForcedLogLevel:", [l.strip() for l in txt.splitlines() if "ForcedLogLevel" in l][:1],
          "| AddZone:", txt.count("veafCombatZone.AddZone"), "| VeafQRA:new:", txt.count("VeafQRA:new"), "| addCapMission:", txt.count("addCapMission("),
          "| HideNames:", [l.strip() for l in txt.splitlines() if "HideNames" in l][:1])
    return m


if __name__ == "__main__":
    paths = sys.argv[1:]
    if not paths:
        paths = [max(glob.glob(str(ROOT / "VEAF_OpenTraining_GermanyCW_ICAO_ETAR_*.miz")), key=os.path.getmtime)]
        paths += sorted(glob.glob(str(ROOT / "missions" / "*.miz")))
    for p in paths:
        check(p, "mission")
