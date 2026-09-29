"""Turn the static targets of a zone into one-vehicle ground groups, so they show warm on a targeting pod.

A static has no engine: on the 28/09 evening flight the static targets of Wahner Heide were cold on the A-10's
pod while the zone's groups were hot. A group keeps the static's type, place, heading and draw tag
(`#spawngroup` / `#spawncount`, on its first unit as the other drawn groups carry it), holds fire and does not
disperse: the easy levels promise inert targets.

Usage: python tools/statics_to_groups.py combatZone_WahnerHeide_Easy-cible combatZone_Baumholder_Easy-cible
Each argument is a static group name prefix. The script refuses to run twice (a group of that name already exists).
"""

import sys

import paths  # noqa: F401  (puts VMCT on sys.path)

from veaf_mission_mcp.mission_folder import load_folder_mission, save_folder_mission  # noqa: E402

ROE_WEAPON_HOLD = {"id": "WrappedAction", "number": 1, "auto": False, "enabled": True,
                   "params": {"action": {"id": "Option", "params": {"name": 0, "value": 4}}}}
# "Disperse under fire" unticked: the editor writes the option with no value (its value is a delay in seconds,
# me_action_db.lua; 0 would mean disperse at once)
NO_DISPERSAL = {"id": "WrappedAction", "number": 2, "auto": False, "enabled": True,
                "params": {"action": {"id": "Option", "params": {"name": 8}}}}


def countries(content):
    for side in content["coalition"].values():
        yield from side.get("country") or []


def groups(country, cat):
    return (country.get(cat) or {}).get("group") or []


def main(prefixes):
    mission = load_folder_mission(paths.ROOT)
    content = mission.mission_content
    every = [g for c in countries(content) for cat in ("vehicle", "static", "plane", "helicopter", "ship")
             for g in groups(c, cat)]
    next_gid = max(g["groupId"] for g in every) + 1
    next_uid = max(u["unitId"] for g in every for u in g["units"]) + 1
    vehicle_names = {g["name"] for c in countries(content) for g in groups(c, "vehicle")}
    done = 0
    for country in countries(content):
        statics = groups(country, "static")
        picked = [g for g in statics if g["name"].startswith(tuple(prefixes))]
        if not picked:
            continue
        clash = [g["name"] for g in picked if g["name"] in vehicle_names]
        if clash:
            sys.exit(f"{clash}: a group of that name already exists, nothing written")
        country["static"]["group"] = [g for g in statics if g not in picked]
        country.setdefault("vehicle", {}).setdefault("group", [])
        for sg in picked:
            su = sg["units"][0]
            x, y = su["x"], su["y"]
            country["vehicle"]["group"].append({
                "groupId": next_gid, "name": sg["name"], "task": "Ground Nothing", "hidden": False,
                "lateActivation": False, "start_time": 0, "taskSelected": True, "uncontrollable": False,
                "visible": False, "x": x, "y": y,
                "route": {"points": [{
                    "name": "", "type": "Turning Point", "action": "Off Road", "alt": 0, "alt_type": "BARO",
                    "ETA": 0, "ETA_locked": True, "formation_template": "", "speed": 0, "speed_locked": True,
                    "x": x, "y": y,
                    "task": {"id": "ComboTask", "params": {"tasks": [ROE_WEAPON_HOLD, NO_DISPERSAL]}},
                }]},
                "units": [{
                    "unitId": next_uid, "name": su["name"], "type": su["type"], "skill": "Average",
                    "coldAtStart": False, "heading": su.get("heading", 0), "playerCanDrive": True, "x": x, "y": y,
                }],
            })
            print(f"{sg['name']}: static {su['type']} -> group {next_gid}, unit {next_uid}")
            next_gid, next_uid, done = next_gid + 1, next_uid + 1, done + 1
    if not done:
        sys.exit("no static matched, nothing written")
    print(save_folder_mission(mission, paths.ROOT))


if __name__ == "__main__":
    main(sys.argv[1:])
