"""Build the Lua probe asking DCS's own Disposition (the scenery-aware point finder VEAF already uses)
whether each editor-placed ground element stands clear of forests and buildings."""
import json
from paths import ROOT, TOOLS  # noqa: E402  (also puts VMCT on sys.path)
from veaf_mission_mcp.mission_folder import load_folder_mission
seq = lambda v: list(v.values()) if isinstance(v, dict) else list(v or [])
m = load_folder_mission(ROOT).mission_content
pts = []
for side, co in m["coalition"].items():
    for c in seq(co.get("country")):
        for cat in ("vehicle", "static"):
            for g in seq((c.get(cat) or {}).get("group")):
                us = seq(g["units"])
                pts.append({"n": g["name"], "x": round(us[0]["x"]), "z": round(us[0]["y"]), "len": len(us)})
chunks = [pts[i:i + 25] for i in range(0, len(pts), 25)]
LUA = """local pts = %s
local out = {}
for _, p in ipairs(pts) do
  local v = {x = p.x, y = land.getHeight({x = p.x, y = p.z}), z = p.z}
  local ok, cands = pcall(Disposition.getSimpleZones, v, 600, 40, 30)
  local best, bx, bz = nil, nil, nil
  if ok and type(cands) == "table" then
    for _, c in ipairs(cands) do
      local d = math.sqrt((c.x - p.x)^2 + (c.y - p.z)^2)
      if not best or d < best then best, bx, bz = d, c.x, c.y end
    end
  end
  out[#out + 1] = string.format("%%s|%%s|%%s|%%s|%%s", p.n, land.getSurfaceType({x = p.x, y = p.z}), best and math.floor(best) or -1, bx and math.floor(bx) or "", bz and math.floor(bz) or "")
end
return table.concat(out, ";")"""
def lua_tbl(ch):
    return "{" + ",".join('{n=%s,x=%d,z=%d}' % (json.dumps(p["n"]), p["x"], p["z"]) for p in ch) + "}"
json.dump([LUA % lua_tbl(ch) for ch in chunks], open(TOOLS / "probe_chunks.json", "w", encoding="utf-8"), ensure_ascii=False)
json.dump(pts, open(TOOLS / "probe_points.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(pts), "points,", len(chunks), "chunks")
