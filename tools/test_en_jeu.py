"""In-game checks of the test mission, through dcs-bridge: one step per call, each ends on a VERDICT line.

Usage (from the mission folder, the test mission running in DCS, dcs-serve connected):
    python tools/test_en_jeu.py probe      # FIRST, before any zone: vehicles in forest/town/water (probe_scenery.py)
    python tools/test_en_jeu.py nesting    # each level spawns the levels it includes, one family at a time
    python tools/test_en_jeu.py activate   # every combat zone on, silently; then:
    python tools/test_en_jeu.py statics    # every static of the mission stands where the editor put it
    python tools/test_en_jeu.py ships      # ships alive, afloat, moving
    python tools/test_en_jeu.py convoys    # run twice, a minute or more apart: the convoys drive
    python tools/test_en_jeu.py cap        # every CAP on, a passive enemy fighter sent at each; then:
    python tools/test_en_jeu.py cap-result # a few minutes later: which CAP fired at its target

Order matters: `probe` measures the ground where no vehicle stands yet, so it runs at mission start
(docs/journal-v6.md, section 9.5). The later steps change the session; restart the mission to probe again.
"""

import json
import sys
import time
from collections import defaultdict

from paths import ROOT  # noqa: E402  (also puts VMCT on sys.path)
from probe_scenery import exec_lua  # noqa: E402
from veaf_mission_mcp.mission_folder import load_folder_mission  # noqa: E402

import yaml  # noqa: E402


def seq(v):
    return list(v.values()) if isinstance(v, dict) else list(v or [])


def mission():
    return load_folder_mission(ROOT).mission_content


def groups(m, cats):
    for side, co in m["coalition"].items():
        for c in seq(co.get("country")):
            for cat in cats:
                for g in seq((c.get(cat) or {}).get("group")):
                    yield side, cat, g


def lua_json(code):
    """Run Lua that returns a JSON string built with net.lua2json, and decode it."""
    return json.loads(exec_lua(f"local r = (function() {code} end)(); return '=' .. net.lua2json(r)")[1:])


def step_probe():
    import probe_scenery
    return probe_scenery.main()


def step_nesting():
    zones = yaml.safe_load(open(ROOT / "mission.yaml", encoding="utf-8"))["modules"]["COMBATZONE"]["combat_zones"]
    includes = {z["zone_name"]: z.get("includes") or [] for z in zones}

    def spawned_count(name):
        exec_lua(f'veafCombatZone.ActivateZone("{name}", true); return "=on"')
        time.sleep(15)  # VEAF spawns the zone's groups asynchronously
        n = lua_json(f"""
            local z = veafCombatZone.GetZone("{name}")
            local n = #(z.spawnedGroups or {{}})
            veafCombatZone.DesactivateZone("{name}", true)
            return {{n}}""")[0]
        return n

    # Compared by count, not by name: a group drawn through a `#command` carrier is named after the level that
    # spawned it, not after the level it belongs to (Borkenberge, 29/09). So a level must spawn strictly more
    # groups than each level it includes, alone.
    family = {z for name, inc in includes.items() if inc for z in [name, *inc]}
    count = {z: spawned_count(z) for z in sorted(family)}
    bad = 0
    for name, inc in includes.items():
        for i in inc:
            ok = count[name] > count[i]
            bad += not ok
            print(f"  {name}: {count[name]} groups, includes {i}: {count[i]}" + ("" if ok else "  <-- NOT MORE"))
    print(f"VERDICT: {bad} nested level(s) spawning no more than the level they include")


def step_activate():
    n = exec_lua("""local n = 0
        for name, _ in pairs(veafCombatZone.zonesDict) do pcall(veafCombatZone.ActivateZone, name, true); n = n + 1 end
        return "zones=" .. n""")
    print("VERDICT: activated", n)


def step_statics():
    """Every static that spawned stands on its editor position, and each draw (#spawngroup) spawned #spawncount.

    Matched by name: a spawned static is named "<zone> [r] <editor name>#<id>". A search by position is useless
    here, it tests the object's bounding box and an Il-76 spills over a neighbour's point (29/09).
    Run `activate` first, and read the draws with one level per family: two levels of a family each draw
    their own copy of the included level.
    """
    import re
    editor = {}
    for _s, _c, g in groups(mission(), ("static",)):
        u = seq(g["units"])[0]
        m = re.search(r'#spawngroup="([^"]+)" #spawncount=(\d+)', u["name"])
        editor[g["name"]] = (u["x"], u["y"], m.group(1) if m else None, int(m.group(2)) if m else None)
    live = lua_json("""local o = {}
        for _, s in ipairs({1, 2}) do for _, st in ipairs(coalition.getStaticObjects(s)) do
          local p = st:getPoint(); o[#o + 1] = {n = st:getName(), x = p.x, z = p.z}
        end end
        return o""")
    drawn, moved, seen = defaultdict(set), [], set()
    for obj in live:
        # "<zone> [r] <editor name>[ #spawngroup=... #spawncount=N]#<id>[ #<n>]" -> "<editor name>"
        rest = re.sub(r"#\d+( #\d+)?$", "", obj["n"].split(" [r] ")[-1])
        key = re.sub(r" #spawngroup=.*$", "", rest).strip()
        if key not in editor:
            continue
        seen.add(key)
        x, y, sg, _n = editor[key]
        if (d := ((obj["x"] - x) ** 2 + (obj["z"] - y) ** 2) ** 0.5) > 1:
            moved.append(f"{key} {d:.0f} m")
        if sg:
            drawn[(obj["n"].split(" [r] ")[0], sg)].add(key)
    for m in moved:
        print(f"  moved: {m}")
    want = {sg: n for _x, _y, sg, n in editor.values() if sg}
    wrong = [f"{zone} {sg}: {len(keys)} of {want[sg]}" for (zone, sg), keys in sorted(drawn.items()) if len(keys) != want[sg]]
    for w in wrong:
        print(f"  draw: {w}")
    absent = [k for k, v in editor.items() if k not in seen and not v[2]]
    if absent:  # a static placed dead (a wreck) keeps its editor name but is not listed by getStaticObjects
        names = "{" + ",".join(json.dumps(a) for a in absent) + "}"
        absent = lua_json(f"local o = {{}} for _, n in ipairs({names}) do "
                          "if not StaticObject.getByName(n) then o[#o + 1] = n end end return o")
    for a in absent:
        print(f"  missing (not drawn): {a}")
    print(f"VERDICT: {len(seen)} statics spawned, {len(moved)} moved, {len(wrong)} draw(s) off, {len(absent)} missing")


def step_ships():
    names = [g["name"] for _s, _c, g in groups(mission(), ("ship",))]
    res = lua_json(f"""
        local out = {{}}
        for _, n in ipairs({{{",".join(json.dumps(n) for n in names)}}}) do
          local g = Group.getByName(n)
          if not g then -- a zone's ship group is renamed on spawn: "<zone> [r] <editor name>#<id>"
            for _, s in ipairs({{1, 2}}) do for _, c in ipairs(coalition.getGroups(s, Group.Category.SHIP)) do
              if c:getName():find(n, 1, true) then g = c end
            end end
          end
          local row = {{name = n, alive = 0, water = 0, speed = 0}}
          if g then
            for _, u in ipairs(g:getUnits()) do
              local p, v = u:getPoint(), u:getVelocity()
              row.alive = row.alive + 1
              if land.getSurfaceType({{x = p.x, y = p.z}}) == 3 then row.water = row.water + 1 end
              row.speed = math.max(row.speed, math.floor(math.sqrt(v.x * v.x + v.z * v.z) * 1.94384))
            end
          end
          out[#out + 1] = row
        end
        return out""")
    bad = 0
    for r in res:
        ok = r["alive"] > 0 and r["water"] == r["alive"]
        bad += not ok
        print(f"  {r['name']}: {r['alive']} alive, {r['water']} afloat, {r['speed']} kt" + ("" if ok else "  <-- PROBLEM"))
    print(f"VERDICT: {bad} ship group(s) missing or aground")


def step_convoys():
    res = lua_json("""
        local out, prev = {}, _G.__testConvoys or {}
        _G.__testConvoys = {}
        for _, side in ipairs({1, 2}) do
          for _, g in ipairs(coalition.getGroups(side, Group.Category.GROUND)) do
            local n = g:getName()
            if n:lower():find("convoi") or n:lower():find("colonne") then
              local u = g:getUnit(1)
              if u then
                local p = u:getPoint()
                local road = land.getSurfaceType({x = p.x, y = p.z}) == 4
                _G.__testConvoys[n] = {x = p.x, z = p.z, t = timer.getTime()}
                local o = prev[n]
                out[#out + 1] = {name = n, size = g:getSize(), road = road,
                  moved = o and math.floor(math.sqrt((p.x - o.x) ^ 2 + (p.z - o.z) ^ 2)) or -1,
                  dt = o and math.floor(timer.getTime() - o.t) or 0}
              end
            end
          end
        end
        return out""")
    if not res:
        print("VERDICT: no convoy group alive -- run `activate` first")
        return
    first = all(r["moved"] < 0 for r in res)
    for r in res:
        print(f"  {r['name']}: {r['size']} vehicles, lead on road: {r['road']}"
              + ("" if first else f", moved {r['moved']} m in {r['dt']} s"))
    if first:
        print("VERDICT: positions recorded -- run `convoys` again in a minute")
    else:
        still = [r["name"] for r in res if r["moved"] < 50]
        print(f"VERDICT: {len(res) - len(still)} of {len(res)} convoy groups drive" + (f" (stopped: {', '.join(still)})" if still else ""))


def step_cap():
    # VEAF registers each CAP once per skill and size ("<name>/good/2"...): the radio menu's default is good, pair
    caps = [c["group_name"] + "/good/2" for c in yaml.safe_load(open(ROOT / "mission.yaml", encoding="utf-8"))["cap_missions"]
            if c["group_name"].startswith("CAP ")]  # the bombers are missions too, with nothing to fire at a fighter
    exec_lua("for _, n in ipairs({" + ",".join(json.dumps(c) for c in caps) + "}) do veafCombatMission.ActivateMission(n, true) end"
             " return '=on'")
    time.sleep(20)  # the CAP groups spawn asynchronously
    res = lua_json(f"""
        _G.__testCapShots = _G.__testCapShots or {{}}
        if not _G.__testCapHandler then
          _G.__testCapHandler = {{}}
          function _G.__testCapHandler:onEvent(e)
            if (e.id == world.event.S_EVENT_SHOT or e.id == world.event.S_EVENT_SHOOTING_START) and e.initiator
               and e.initiator.getGroup and e.initiator:getGroup() then
              local n = e.initiator:getGroup():getName()
              _G.__testCapShots[n] = (_G.__testCapShots[n] or 0) + 1
            end
          end
          world.addEventHandler(_G.__testCapHandler)
        end
        local out = {{}}
        for i, name in ipairs({{{",".join(json.dumps(c) for c in caps)}}}) do
          local m = veafCombatMission.GetMission(name)
          local g = m and m.spawnedGroups and m.spawnedGroups[1]
          local u = g and g:isExist() and g:getUnit(1)
          local row = {{cap = name, group = g and g:getName() or "none"}}
          if u then
            local p = u:getPoint()
            local red = g:getCoalition() == coalition.side.RED
            local sy = red and -40000 or 40000 -- the enemy comes from its own side of the front
            local tname = "TEST cible " .. i
            local anyEnemy = coalition.getGroups(red and coalition.side.BLUE or coalition.side.RED)[1]
            local enemy = anyEnemy and anyEnemy:getUnit(1) and anyEnemy:getUnit(1):getCountry()
              or (red and country.id.USA or country.id.RUSSIA)
            coalition.addGroup(enemy, Group.Category.AIRPLANE, {{
              name = tname, task = "CAP",
              units = {{{{name = tname, type = red and "F-16C_50" or "Su-27", skill = "Average",
                x = p.x, y = p.z + sy, alt = p.y, speed = 200, heading = red and math.pi / 2 or 3 * math.pi / 2,
                payload = {{fuel = 3000, flare = 0, chaff = 0, gun = 0, pylons = {{}}}}}}}},
              route = {{points = {{
                {{x = p.x, y = p.z + sy, alt = p.y, speed = 200, type = "Turning Point", action = "Turning Point",
                  task = {{id = "ComboTask", params = {{tasks = {{ -- ROE weapon hold: the target never fires back
                    {{id = "WrappedAction", number = 1, params = {{action = {{id = "Option", params = {{name = 0, value = 4}}}}}}}}}}}}}}}},
                {{x = p.x, y = p.z - sy, alt = p.y, speed = 200, type = "Turning Point", action = "Turning Point"}}}}}}
            }})
            row.target = tname
          end
          out[#out + 1] = row
        end
        return out""")
    for r in res:
        print(f"  {r['cap']}: CAP group {r['group']}, target {r.get('target', 'NOT SENT')}")
    print("VERDICT: targets sent (weapons hold) -- run `cap-result` in 3 to 5 minutes")


def step_cap_result():
    shots = lua_json("return _G.__testCapShots or {}")
    caps = [c["group_name"] for c in yaml.safe_load(open(ROOT / "mission.yaml", encoding="utf-8"))["cap_missions"]
            if c["group_name"].startswith("CAP ")]  # the Tu-22M3 is a bomber: it has nothing to fire at a fighter
    fired = defaultdict(int)
    for g, n in (shots or {}).items():
        for c in caps:
            if c.lower() in g.lower():
                fired[c] += n
    for c in caps:
        print(f"  {c}: {fired[c]} shot(s)")
    print(f"VERDICT: {sum(1 for c in caps if fired[c])} of {len(caps)} CAP engaged their target")


STEPS = {"probe": step_probe, "nesting": step_nesting, "activate": step_activate, "statics": step_statics,
         "ships": step_ships, "convoys": step_convoys, "cap": step_cap, "cap-result": step_cap_result}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in STEPS:
        print(__doc__)
        sys.exit(2)
    sys.exit(STEPS[sys.argv[1]]() or 0)
