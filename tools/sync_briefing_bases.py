"""Copy the base frequencies of src/presets.yaml into the DCS briefing texts (no hand-typed frequency).

Usage (from the mission folder): python tools/sync_briefing_bases.py
Rewrites every "<base> [(note)] <uhf> / <vhf>" pair of the description* strings of src/mission/mission with the
values of the channel 'Base-<base>' (collection 'bases', written by `veaf-tools content airfield-channels`).
Ends on one verdict line; fails if a base of the text has no channel.
"""

import re
import sys
import unicodedata

import yaml

from paths import ROOT  # noqa: E402

PAIR = re.compile(r"([A-ZÀ-Ý][\w\-éèüöäÉ ]+?)((?: \([^)]*\))? )(\d{3}\.\d+) / (\d{3}\.\d+)")
STRING = re.compile(r'(description\w* = ")((?:[^"\\]|\\.)*)(")', re.S)


def ascii_name(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def fmt(f):
    return f"{float(f):.3f}".rstrip("0").rstrip(".") if float(f) % 1 else f"{float(f):.1f}"


def main():
    bases = yaml.safe_load(open(ROOT / "src" / "presets.yaml", encoding="utf-8"))["channels_collection"]["bases"]
    path = ROOT / "src" / "mission" / "mission"
    text = open(path, encoding="utf-8", newline="").read()
    changed, missing = [], []

    def pair(m):
        name = m.group(1).strip()
        ch = bases.get("Base-" + ascii_name(name))
        if ch is None:
            missing.append(name)
            return m.group(0)
        new = f"{m.group(1)}{m.group(2)}{fmt(ch['freqs']['uhf'])} / {fmt(ch['freqs']['vhf'])}"
        if new != m.group(0):
            changed.append(f"{name}: {m.group(3)} / {m.group(4)} -> {fmt(ch['freqs']['uhf'])} / {fmt(ch['freqs']['vhf'])}")
        return new

    text = STRING.sub(lambda s: s.group(1) + PAIR.sub(pair, s.group(2)) + s.group(3), text)
    if missing:
        print("no channel Base-<name> for:", ", ".join(missing))
        print("VERDICT: FAILED, mission not written")
        return 1
    open(path, "w", encoding="utf-8", newline="").write(text)
    for c in changed:
        print(" ", c)
    print(f"VERDICT: OK, {len(changed)} pair(s) rewritten")
    return 0


if __name__ == "__main__":
    sys.exit(main())
