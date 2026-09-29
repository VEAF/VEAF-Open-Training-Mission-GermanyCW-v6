"""Build the local test mission for David: LOCAL_TEST profile + game master + a non-dynamic A-10C II + dcs-bridge.

Dynamic slots only work in multiplayer, so a solo test needs a classic client slot (memory: mission-test-locale).
These slots go into the TEST COPY only, never into the mission sources: the server build must not gain them.

Usage (from the mission folder): python tools/make_test_mission.py
Output: bridge/bridge-GermanyCW-OT.miz

veaf-tools runs from the VMCT code named by VMCT_PY (tools/paths.py), in this Python, not from the mission's
veaf-tools.exe: the test copy must be built by the same code the checks read it with.
"""

import glob
import os
import shutil
import subprocess
import sys

from paths import BRIDGE_LUA, ROOT, VMCT_PY  # noqa: E402  (also puts VMCT on sys.path)
from mission_tools.miz_tools import read_miz, write_miz  # noqa: E402
from veaf_mission_mcp.actions import register_default_actions  # noqa: E402
from veaf_mission_mcp.catalog import ActionCatalog  # noqa: E402

OUT = ROOT / "bridge" / "bridge-GermanyCW-OT.miz"

VEAF_TOOLS = [sys.executable, "-c", "import sys; sys.path.insert(0, sys.argv.pop(1)); from veaf_tools.app import main; main()",
              VMCT_PY]

# the LOCAL_TEST build rewrites the versioned src/scripts/veaf-config.lua (security off, debug logs): keep the
# sources' copy and put it back, so a commit after a test never ships the test configuration
CONFIG = ROOT / "src" / "scripts" / "veaf-config.lua"
config_before = CONFIG.read_bytes()
try:
    subprocess.run([*VEAF_TOOLS, "mission", "build", "--profile", "LOCAL_TEST", "--no-pause"], cwd=ROOT, check=True,
                   stdout=subprocess.DEVNULL)
finally:
    CONFIG.write_bytes(config_before)
built = max(glob.glob(str(ROOT / "VEAF_OpenTraining_GermanyCW_ICAO_ETAR_*.miz")), key=os.path.getmtime)
OUT.parent.mkdir(exist_ok=True)
shutil.copy(built, OUT)

# game master, one per side
miz = read_miz(OUT)
miz.mission_content["groundControl"]["roles"]["instructor"] = {"blue": 1, "red": 1, "neutrals": 0}
write_miz(miz, OUT)

# A-10C II, cold start on Ramstein stand 4 (id 08) -- the stand the v5 mission used for its A-10C II
catalog = ActionCatalog()
register_default_actions(catalog)
print(catalog.run_action("add_player_slot", dict(
    target=str(OUT), coalition="blue", country_id=2, country_name="USA", name="TEST A-10C II Ramstein", unit_type="A-10C_2",
    position=dict(x=-498115, y=-935487), start="ground-cold", parking="4", parking_id="08", airdrome_id=165, frequency_mhz=251)))

# Mi-24P and OH-58D, hot on the ground at Ramstein, on the stands the v5 mission used for them: the two airframes
# whose channel list is shifted by one slot (channel-0 rotation, "M" head slot), so a pilot can read in the cockpit
# which number a preset really carries. Added after the build, so the presets injector never saw them: their radios
# are copied from the blue template of the same type, which it did fill.
HELOS = [("TEST Mi-24P Ramstein", "Mi-24P", -499135, -934277, "187", "125"),
         ("TEST OH-58D Ramstein", "OH58D", -499217, -933340, "138", "94")]
for name, unit_type, x, y, parking, parking_id in HELOS:
    print(catalog.run_action("add_player_slot", dict(
        target=str(OUT), coalition="blue", country_id=2, country_name="USA", name=name, unit_type=unit_type,
        position=dict(x=x, y=y), start="ground-hot", parking=parking, parking_id=parking_id, airdrome_id=165,
        frequency_mhz=251)))


def seq(v):
    return list(v.values()) if isinstance(v, dict) else list(v or [])


miz = read_miz(OUT)
blue = [(g, u) for c in seq(miz.mission_content["coalition"]["blue"].get("country"))
        for g in seq((c.get("helicopter") or {}).get("group")) for u in seq(g["units"])]
for name, unit_type, *_ in HELOS:
    template = next(u for g, u in blue if u["type"] == unit_type and u.get("Radio") and g["name"] != name)
    next(u for g, u in blue if g["name"] == name)["Radio"] = template["Radio"]
write_miz(miz, OUT)

subprocess.run([*VEAF_TOOLS, "dcs", "inject-bridge", "--bridge-lua", BRIDGE_LUA, str(OUT)], cwd=ROOT, check=True)
print("OK", OUT)
print("NOTE: the base .miz of the mission folder is now the LOCAL_TEST build; rebuild the server profile before publishing it")
