"""Shared helpers: bullseye bearing/distance and nearest tanker, from DCS x (north) / y (east)."""

import json
import math
import os

S = os.path.dirname(os.path.abspath(__file__))
BULL = json.load(open(os.path.join(S, "bullseye.json")))
SUP = json.load(open(os.path.join(S, "support.json")))
TANKERS = {"Texaco 1": "TACAN 51Y, 251.0", "Arco 1": "TACAN 52Y, 252.0", "Texaco 2": "TACAN 53Y, 253.0",
           "Arco 2": "TACAN 54Y, 254.0", "Shell 1": "TACAN 55Y, 255.0"}


def bullseye(x, y):
    """Bearing (true, grid) and distance (nm) FROM the bullseye TO the point: 'BULLSEYE 123/45'."""
    dx, dy = x - BULL["x"], y - BULL["y"]
    if math.hypot(dx, dy) < 1852:
        return "sur le BULLSEYE"
    brg = (math.degrees(math.atan2(dy, dx)) + 360) % 360
    return f"BULLSEYE {round(brg) % 360:03d}/{round(math.hypot(dx, dy) / 1852)}"


def _dseg(p, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    t = max(0, min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - ax - t * dx, p[1] - ay - t * dy)


def nearest_tanker(x, y):
    """Closest boom and closest drogue blue tanker racetracks (distance to the track segment), as text."""
    d = {k: round(_dseg((x, y), *SUP[k]) / 1852) for k in TANKERS}
    boom = min(("Texaco 1", "Texaco 2", "Shell 1"), key=d.get)
    drogue = min(("Arco 1", "Arco 2"), key=d.get)
    return (f"{boom} (perche, {TANKERS[boom]}) à {d[boom]} nm, "
            f"{drogue} (panier, {TANKERS[drogue]}) à {d[drogue]} nm")
