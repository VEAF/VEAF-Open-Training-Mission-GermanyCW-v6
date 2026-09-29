"""Ask DCS whether the mission's ground vehicles stand in forest, town or water, where the editor put them.

Usage (from the mission folder, the test mission running in DCS with dcs-serve connected):
    python tools/probe_scenery.py            # probe, print one line per group in trouble, then a verdict
    python tools/probe_scenery.py --lua-only # write the Lua chunks to tools/probe_chunks.json, send nothing

What it measures, and why this way (docs/journal-v6.md, sections 9.4 and 9.5):
- DCS's own `Disposition.getSimpleZones` is the only API that knows forests, and it answers "is there free room
  here", not "is this under a tree": a vehicle takes room. So the probe runs on the **editor positions**, at
  mission start, **before any zone is activated**: combat zone groups do not exist yet, nothing blocks the test
  but the scenery. A point that a live unit covers anyway (a group alive from the start) is reported as
  "occupied" and not judged: that answer would be the unit, not the ground.
- Statics are not probed: a 50 m building blocks its own 20 m test wherever it stands. They are counted, and
  only checked for water.
- Test per vehicle: at least one free 5 m spot within 20 m (the calibration of 25/09: open ground, 0 alert).
- `getSimpleZones` returns candidates as {x, y}, with y the easting: the probe only counts them.

The bridge address and key are read from ../VEAF-dcs-bridge/dcs-client.yaml (DCS_CLIENT_YAML to override);
the key is sent in a header, never printed.
"""

import json
import os
import sys
import urllib.request
from collections import defaultdict

import yaml

from paths import ROOT, TOOLS  # noqa: E402  (also puts VMCT on sys.path)
from veaf_mission_mcp.mission_folder import load_folder_mission  # noqa: E402

CHUNK = 60
CLIENT_YAML = os.environ.get("DCS_CLIENT_YAML", str(ROOT.parent / "VEAF-dcs-bridge" / "dcs-client.yaml"))

LUA = """local pts = %s
local out = {}
local function occupied(p)
  local found = false
  world.searchObjects(Object.Category.UNIT, {id = world.VolumeType.SPHERE, params = {point = p, radius = 25}},
    function() found = true; return false end)
  return found
end
for _, q in ipairs(pts) do
  local p = {x = q[2], y = land.getHeight({x = q[2], y = q[3]}), z = q[3]}
  local verdict
  if land.getSurfaceType({x = p.x, y = p.z}) == 3 then verdict = "water"
  elseif occupied(p) then verdict = "occupied"
  else
    local ok, c = pcall(Disposition.getSimpleZones, p, 20, 5, 10)
    verdict = (ok and type(c) == "table" and #c > 0) and "clear" or "blocked"
  end
  out[#out + 1] = q[1] .. "=" .. verdict
end
return table.concat(out, ";")"""


def seq(v):
    return list(v.values()) if isinstance(v, dict) else list(v or [])


def collect():
    """Every vehicle unit (id, group, x, z) and every static (group, x, z) of the mission folder."""
    m = load_folder_mission(ROOT).mission_content
    vehicles, statics = [], []
    for co in m["coalition"].values():
        for c in seq(co.get("country")):
            for g in seq((c.get("vehicle") or {}).get("group")):
                for u in seq(g["units"]):
                    vehicles.append((len(vehicles) + 1, g["name"], round(u["x"]), round(u["y"])))
            for g in seq((c.get("static") or {}).get("group")):
                u = seq(g["units"])[0]
                statics.append((len(statics) + 1, g["name"], round(u["x"]), round(u["y"])))
    return vehicles, statics


def chunks(points):
    for i in range(0, len(points), CHUNK):
        part = points[i:i + CHUNK]
        yield LUA % ("{" + ",".join("{%d,%d,%d}" % (n, x, z) for n, _g, x, z in part) + "}")


def exec_lua(code):
    cfg = yaml.safe_load(open(CLIENT_YAML, encoding="utf-8"))
    req = urllib.request.Request(f"http://{cfg['host']}:{cfg['port']}/api/exec", data=json.dumps({"code": code, "timeout": 60}).encode(),
                                 headers={"Authorization": f"Bearer {cfg['api_key']}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as r:
        body = json.loads(r.read().decode("utf-8"))
    result = body.get("result", body)
    if not isinstance(result, str) or "=" not in result:
        raise RuntimeError(f"unexpected answer from DCS: {str(body)[:300]}")
    return result


def main():
    vehicles, statics = collect()
    if "--lua-only" in sys.argv:
        lua = list(chunks(vehicles)) + list(chunks(statics))
        json.dump(lua, open(TOOLS / "probe_chunks.json", "w", encoding="utf-8"), ensure_ascii=False)
        print(len(vehicles), "vehicles,", len(statics), "statics,", len(lua), "chunks -> tools/probe_chunks.json")
        return 0
    verdict = {}
    for code in chunks(vehicles):
        verdict.update(kv.split("=") for kv in exec_lua(code).split(";"))
    per_group = defaultdict(lambda: defaultdict(int))
    for n, g, _x, _z in vehicles:
        per_group[g][verdict.get(str(n), "missing")] += 1
    water_statics = []
    for code in chunks(statics):
        for kv in exec_lua(code).split(";"):
            n, v = kv.split("=")
            if v == "water":
                water_statics.append(statics[int(n) - 1][1])
    totals = defaultdict(int)
    for g, c in sorted(per_group.items()):
        for k, v in c.items():
            totals[k] += v
        if c.get("blocked") or c.get("water") or c.get("missing"):
            print(f"  {g}: " + ", ".join(f"{k} {v}" for k, v in sorted(c.items())))
    for s in water_statics:
        print(f"  static {s}: water")
    occ = sorted(g for g, c in per_group.items() if c["occupied"])
    print(f"  occupied by a live unit, not judged: {totals['occupied']} vehicles in {len(occ)} groups ({', '.join(occ[:6])}"
          f"{', ...' if len(occ) > 6 else ''})")
    print(f"VERDICT: {len(vehicles)} vehicles in {len(per_group)} groups -- clear {totals['clear']}, blocked {totals['blocked']}, "
          f"water {totals['water']}, occupied {totals['occupied']}, missing {totals['missing']}; "
          f"{len(statics)} statics, {len(water_statics)} in water")
    return 0


if __name__ == "__main__":
    sys.exit(main())
