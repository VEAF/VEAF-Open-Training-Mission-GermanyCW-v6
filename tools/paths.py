"""Where the mission folder and the VMCT Python code are, for every script of tools/.

VMCT_PY points at an export of VMCT develop's src/python/veaf-tools: the main VMCT checkout is shared with
other sessions working on other branches, so it is only the fallback.
"""

import os
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
VMCT_PY = os.environ.get("VMCT_PY", str(ROOT.parent / "VEAF-Mission-Creation-Tools" / "src" / "python" / "veaf-tools"))
BRIDGE_LUA = os.environ.get("BRIDGE_LUA", str(ROOT.parent / "VEAF-dcs-bridge" / "src" / "lua" / "dcs-bridge.lua"))

if VMCT_PY not in sys.path:
    sys.path.insert(0, VMCT_PY)
    print(f"[tools] VMCT code: {VMCT_PY}", file=sys.stderr)  # say which code built what the script prints
