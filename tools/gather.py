"""Collect every briefing fact from the mission folder itself (no hand-typed values)."""
import json, math
from paths import ROOT  # noqa: E402  (also puts VMCT on sys.path)
from pathlib import Path
import yaml
from veaf_libs import coordinates as C
from veaf_mission_mcp.mission_folder import load_folder_mission
F = ROOT
seq = lambda v: list(v.values()) if isinstance(v, dict) else list(v or [])
m = load_folder_mission(F).mission_content
Y = yaml.safe_load(open(F / "mission.yaml", encoding="utf-8"))
P = yaml.safe_load(open(F / "src/presets.yaml", encoding="utf-8"))
V = yaml.safe_load(open(F / "src/versions.yaml", encoding="utf-8"))
BULL = (m["coalition"]["blue"]["bullseye"]["x"], m["coalition"]["blue"]["bullseye"]["y"])

def ll(x, y):
    la, lo = C.xy_to_latlon("GermanyCW", x, y); return la, lo
def ddm(x, y):
    la, lo = ll(x, y)
    def f(v, p, n, w):
        # round the minutes first, then carry: 59.9996' must read 1° 00.000', never 60.000'
        deg, mins = int(abs(v)), round((abs(v) % 1) * 60, 3)
        if mins >= 60:
            deg, mins = deg + 1, mins - 60
        return f"{p if v >= 0 else n}{deg:0{w}d}°{mins:06.3f}'"
    return f(la, "N", "S", 2) + " " + f(lo, "E", "W", 3)
def be(x, y):
    dx, dy = x - BULL[0], y - BULL[1]
    if math.hypot(dx, dy) < 1852: return "sur le bullseye"
    return f"{round((math.degrees(math.atan2(dy, dx)) + 360) % 360) % 360:03d}/{round(math.hypot(dx, dy) / 1852)}"
def pt(x, y): return dict(x=round(x), y=round(y), ddm=ddm(x, y), be=be(x, y))

zones = {z["name"]: z for z in seq(m["triggers"]["zones"])}
groups = {}
for side, co in m["coalition"].items():
    for c in seq(co.get("country")):
        for cat in ("plane", "helicopter", "vehicle", "ship", "static"):
            for g in seq((c.get(cat) or {}).get("group")):
                groups[g["name"]] = (side, cat, g)

S = Path(__file__).parent
A = {a["name"]: a for a in json.load(open(S / "airfields.json"))}
chan = {}
for grp in P["channels_collection"].values():
    for k, v in grp.items(): chan[k] = v["freqs"]
out = dict(bullseye=pt(*BULL), name=Y["mission"]["name"], date=m["date"], start=m["start_time"])
disp = {"Buchel": "Büchel", "Norvenich": "Nörvenich"}
# bases
bases = []
for side, lst in (("blue", ["Ramstein", "Spangdahlem", "Buchel", "Norvenich", "Wiesbaden", "Nordholz", "Wunstorf", "Fassberg", "Fulda"]),
                  ("red", ["Laage", "Holzdorf", "Allstedt"])):
    for b in lst:
        a = A[b]; f = chan.get("Base-" + b, {})
        ad = [n for n in groups if n.startswith(f"AD-{b}-")]
        bases.append(dict(name=disp.get(b, b), side=side, uhf=f.get("uhf"), vhf=f.get("vhf"), ad=ad, **pt(a["x"], a["y"])))
out["bases"] = bases
# FARP
out["farps"] = [dict(name=n.replace("FARP-", "").replace("Goettingen", "Göttingen"), **pt(groups[n][2]["x"], groups[n][2]["y"])) for n in ("FARP-Baumholder", "FARP-Goettingen")]
# support
sup = []
for g in ("Texaco 1", "Arco 1", "Texaco 2", "Arco 2", "Shell 1", "Overlord 1", "Magic 1", "Tanker Rouge", "AWACS Rouge"):
    side, cat, gr = groups[g]; pts = seq(gr["route"]["points"]); u = seq(gr["units"])[0]
    tacan = None
    for t in seq(pts[0]["task"]["params"]["tasks"]):
        a = (t.get("params") or {}).get("action") or {}
        if a.get("id") == "ActivateBeacon": tacan = f'{a["params"]["channel"]}{a["params"]["modeChannel"]} {a["params"]["callsign"]}'
    sup.append(dict(name=g, side=side, type=u["type"], freq=gr["frequency"], tacan=tacan, fl=round(pts[0]["alt"] / 0.3048 / 100),
                    kt=round(pts[0]["speed"] * 1.943844), escort=(g + " escort") in groups,
                    a=pt(pts[0]["x"], pts[0]["y"]), b=pt(pts[1]["x"], pts[1]["y"]),
                    mid=pt((pts[0]["x"] + pts[1]["x"]) / 2, (pts[0]["y"] + pts[1]["y"]) / 2)))
out["support"] = sup
# combat zones
cz = []
for z in Y["modules"]["COMBATZONE"]["combat_zones"]:
    tz = zones[z["zone_name"]]
    cz.append(dict(key=z["zone_name"], name=z["friendly_name"], menu=z.get("radio_group_name"), training=z.get("training", False),
                   briefing=z.get("briefing"), includes=z.get("includes"), radius_nm=round(tz["radius"] / 1852, 1), **pt(tz["x"], tz["y"])))
out["zones"] = cz
# QRA
q = []
for d in Y["modules"]["QRA"]["definitions"]:
    tz = zones[d["trigger_zone"]]
    tiers = [dict(n=t["enemy_count"], pick=t.get("random_pick", 1), pool=[p.split(" - ", 1)[1] for p in t["groups"]]) for t in d.get("groups_by_enemy_count", [])]
    types = {}
    for t in d.get("groups_by_enemy_count", []):
        for gname in t["groups"]:
            u = seq(groups[gname][2]["units"]); types[gname.split(" - ", 1)[1]] = f'{len(u)} × {u[0]["type"]}'
    q.append(dict(name=d["name"], side=d["coalition"].lower(), base=d.get("airport_link"), radius_nm=round(tz["radius"] / 1852), tiers=tiers, types=types, **pt(tz["x"], tz["y"])))
out["qra"] = q
# CAP
caps = []
for c in Y.get("cap_missions", []):
    side, cat, g = groups["OnDemand-" + c["group_name"]]; pts = seq(g["route"]["points"]); u = seq(g["units"])
    caps.append(dict(name=c["group_name"], side=side, type=u[0]["type"], n=len(u), fl=round(pts[0]["alt"] / 0.3048 / 100), briefing=c.get("briefing"),
                     mid=pt((pts[0]["x"] + pts[1]["x"]) / 2, (pts[0]["y"] + pts[1]["y"]) / 2), a=pt(pts[0]["x"], pts[0]["y"]), b=pt(pts[1]["x"], pts[1]["y"])))
out["caps"] = caps
# permanent air defence
adl = []
for n, (side, cat, g) in groups.items():
    if n.startswith("AD-"):
        cmd = seq(g["units"])[0]["name"].split('"')[1] if '"' in seq(g["units"])[0]["name"] else ""
        adl.append(dict(name=n, side=side, cmd=cmd, **pt(g["x"], g["y"])))
out["ad"] = adl
# radio plan
out["radio"] = {side: {role: {str(k): (v if isinstance(v, str) else v.get("channel")) if not isinstance(v, (int, float)) else v for k, v in lst.items()}
                       for role, lst in roles.items()} for side, roles in P["channel_lists"].items()}
out["channels"] = chan
out["versions"] = [dict(name=v["name"], time=v.get("time"), kind="réel (METAR ETAR)" if v.get("airport_icao") else ("METAR fixe" if v.get("metar") else "manuel"),
                        metar=v.get("metar")) for v in V["versions"]]
# front (approx), from the Common drawing
for l in seq(m["drawings"]["layers"]):
    for o in seq(l.get("objects")):
        if o["name"] == "Front":
            out["front"] = [dict(x=o["mapX"] + p["x"], y=o["mapY"] + p["y"]) for p in seq(o["points"])]
# graticule
out["grid"] = {"lat": {la: [list(C.latlon_to_xy("GermanyCW", la, lo / 10)) for lo in range(55, 160)] for la in range(49, 56)},
               "lon": {lo: [list(C.latlon_to_xy("GermanyCW", la / 10, lo)) for la in range(488, 558)] for lo in range(6, 16)}}
# QRA timing and helicopters, from mission.yaml
out["qra_delay"] = sorted({d.get("delay_before_activating") for d in Y["modules"]["QRA"]["definitions"]})
out["qra_helos"] = sorted({bool(d.get("react_on_helicopters")) for d in Y["modules"]["QRA"]["definitions"]})
# arena: client groups named "Arène - <type> - <FOX> - <camp>", and its circle drawn on the Common layer
def acts(g):
    return [((t.get("params") or {}).get("action") or {}) for p in seq(g["route"]["points"])[:1] for t in seq(p["task"]["params"]["tasks"])]
arena = []
for n, (side, cat, g) in groups.items():
    if n.startswith("Arène - "):
        _, typ, fox, _ = n.split(" - ")
        arena.append(dict(side=side, type=typ, fox=fox, n=len(seq(g["units"])), freq=g["frequency"]))
out["arena"] = sorted(arena, key=lambda a: (a["side"], a["fox"], a["type"]))
for l in seq(m["drawings"]["layers"]):
    for o in seq(l.get("objects")):
        if o["name"] == "Arène":
            out["arena_zone"] = dict(radius_nm=round(o["radius"] / 1852), **pt(o["mapX"], o["mapY"]))
out["arena_awacs"] = []
for g in ("Darkstar 1", "AWACS Arène Rouge"):
    side, cat, gr = groups[g]; pts = seq(gr["route"]["points"]); u = seq(gr["units"])[0]
    out["arena_awacs"].append(dict(name=g, side=side, type=u["type"], freq=gr["frequency"], fl=round(pts[0]["alt"] / 0.3048 / 100),
                                   mid=pt((pts[0]["x"] + pts[1]["x"]) / 2, (pts[0]["y"] + pts[1]["y"]) / 2)))
# carrier group: position, ATC from its first waypoint, deck slots
side, cat, cg = groups["CSG-74 Stennis"]
cv = next(u for u in seq(cg["units"]) if u["type"] == "Stennis")
atc = {}
for a in acts(cg):
    p = a.get("params") or {}
    if a.get("id") == "ActivateBeacon": atc["tacan"] = f'{p["channel"]}{p["modeChannel"]} {p["callsign"]}'
    if a.get("id") == "ActivateICLS": atc["icls"] = p["channel"]
    if a.get("id") == "ActivateLink4": atc["link4"] = p["frequency"] / 1e6
deck = []
for n, (sd, ct, g) in groups.items():
    if ct == "plane" and seq(g["route"]["points"])[0].get("linkUnit") == cv["unitId"]:
        deck.append(dict(name=n, type=seq(g["units"])[0]["type"], n=len(seq(g["units"])), hot="HOT" in n))
out["carrier"] = dict(name=cv["name"], type=cv["type"], tower=cv["frequency"] / 1e6, deck=sorted(deck, key=lambda d: d["name"]), escorts=len(seq(cg["units"])) - 1,
                      **atc, **pt(cv["x"], cv["y"]))
# laser drones: the ASSETS entries that carry a laser code. Their height is CTLD's, not the mission's: once
# CTLD takes a drone as a JTAC it re-routes it to JTAC_droneAltitude above the ground (measured in game 28/09)
CTLD_DRONE_AGL = yaml.safe_load(open(F / "ctld-config.yaml", encoding="utf-8"))["advanced"]["JTAC_droneAltitude"]
out["drones"] = []
for a in Y["modules"]["ASSETS"]["assets"]:
    if a.get("jtac"):
        side, cat, g = groups[a["name"]]; u = seq(g["units"])[0]
        out["drones"].append(dict(name=a["name"], type=u["type"], jtac=a["jtac"], freq=a.get("freq"), mod=a.get("mod"), where=a["description"].split(" - ")[-1],
                                  agl=CTLD_DRONE_AGL, **pt(u["x"], u["y"])))
# sanctuaries: polygon from their late-activated vertex units
unit_pos = {u["name"]: (u["x"], u["y"]) for n, (sd, ct, g) in groups.items() for u in seq(g["units"])}
out["sanctuaries"] = []
for z in Y["modules"]["SANCTUARY"]["sanctuary_zones"]:
    pts_ = [unit_pos[u] for u in z["polygon_units"]]
    cx, cy = sum(p[0] for p in pts_) / len(pts_), sum(p[1] for p in pts_) / len(pts_)
    out["sanctuaries"].append(dict(name=z["name"], side=z["coalition"].lower(), delay=z.get("delay_instant"), missiles=bool(z.get("protect_from_missiles")),
                                   poly=[dict(x=round(x), y=round(y)) for x, y in pts_], radius_nm=round(max(math.hypot(x - cx, y - cy) for x, y in pts_) / 1852, 1),
                                   **pt(cx, cy)))
# SAR zone: its radio beacons (frequency from their SetFrequency task) and the crash site
out["sar"] = []
for n, (sd, ct, g) in sorted(groups.items()):
    if n.startswith("combatZone_Hunsrueck_SAR-") and ct == "vehicle":
        f = next((a["params"]["frequency"] / 1e6 for a in acts(g) if a.get("id") == "SetFrequency"), None)
        u = seq(g["units"])[0]
        out["sar"].append(dict(name=n.split("-", 1)[1], freq=f, **pt(u["x"], u["y"])))
out["sit"] = m.get("descriptionText"); out["blue_task"] = m.get("descriptionBlueTask"); out["red_task"] = m.get("descriptionRedTask")
json.dump(out, open(S / "briefing_data.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(bases), len(sup), len(cz), len(q), len(caps), len(adl), out["bullseye"])
