"""Check that every place a pilot reads a frequency agrees with src/presets.yaml.

Usage (from the mission folder): python tools/check_frequencies.py [file.miz]
Without argument: the newest base .miz of the mission folder.

Compared, for every channel of the plan:
  1. src/presets.yaml (the reference);
  2. the radios injected into every player aircraft of the .miz: frequency, and the channel name shown in the
     cockpit, byte for byte (a UTF-8 name read as cp1252 becomes "NÃ¶rvenich");
  3. the DCS briefing (dictionary of the .miz): every "<base> <uhf> / <vhf>" pair;
  4. README.md: the bases table and the radio tables.
The kneeboard pages are pictures drawn from the same injected radios: check 2 covers their names and frequencies.
NOT checked: the channel NUMBERS (README 'canal 12', kneeboard CH column) against what the cockpit shows. On the
Mi-24P and the OH-58D they differ from the DCS slot (journal, section 13): read them in the cockpit.
Ends on one verdict line.
"""

import glob
import os
import re
import sys
import zipfile

import yaml

from paths import ROOT  # noqa: E402  (also puts VMCT on sys.path)
from mission_tools.miz_tools import read_miz  # noqa: E402


def seq(v):
    return list(v.values()) if isinstance(v, dict) else list(v or [])


def items(v):
    return sorted(v.items()) if isinstance(v, dict) else list(enumerate(v or [], 1))


def plan():
    """{title: {band: MHz}} and {MHz: title} from presets.yaml."""
    p = yaml.safe_load(open(ROOT / "src" / "presets.yaml", encoding="utf-8"))
    by_title, by_freq = {}, {}
    for coll in p["channels_collection"].values():
        for ch in coll.values():
            by_title[ch["title"]] = ch["freqs"]
            for f in ch["freqs"].values():
                by_freq.setdefault(round(float(f), 3), set()).add(ch["title"])
    return by_title, by_freq


def check_radios(m, by_title, by_freq, problems):
    seen = 0
    for side, co in m["coalition"].items():
        for c in seq(co.get("country")):
            for cat in ("plane", "helicopter"):
                for g in seq((c.get(cat) or {}).get("group")):
                    u = seq(g["units"])[0]
                    if u.get("skill") not in ("Client", "Player") and not g.get("dynSpawnTemplate"):
                        continue
                    for ri, r in items(u.get("Radio")):
                        # paired by slot number, not by position: either table may be a dict or have holes
                        names = dict(items(r.get("channelsNames")))
                        for slot, f in items(r.get("channels")):
                            name = names.get(slot)
                            if not name:
                                continue
                            seen += 1
                            where = f"{side} {u['type']} radio {ri} slot {slot}"
                            if name not in by_title:
                                problems.append(f"radio  {where}: name {name!r} is not a channel of the plan")
                            elif round(float(f), 3) not in {round(float(v), 3) for v in by_title[name].values()}:
                                problems.append(f"radio  {where}: {name} at {f}, plan says {by_title[name]}")
    return seen


PAIR = re.compile(r"([A-ZÀ-Ý][\w\-éèüöäÉ ]+?)(?: \([^)]*\))? (\d{3}\.\d) / (\d{3}\.\d)")


def check_text(label, text, by_title, problems):
    n = 0
    for name, uhf, vhf in PAIR.findall(text):
        name = name.strip()
        if name not in by_title:
            continue
        n += 1
        want = by_title[name]
        if float(uhf) != float(want.get("uhf", -1)) or float(vhf) != float(want.get("vhf", -1)):
            problems.append(f"{label}: {name} {uhf} / {vhf}, plan says {want}")
    return n


def check_readme(by_title, by_freq, problems):
    n = 0
    for line in open(ROOT / "README.md", encoding="utf-8"):
        cells = [c.strip().strip("*`") for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        # bases table: | **Base** | side | coords | bullseye | `uhf` | `vhf` | defence |
        if cells[0] in by_title and len(cells) >= 6 and re.fullmatch(r"\d{3}\.\d+", cells[4] or ""):
            n += 1
            want = by_title[cells[0]]
            if float(cells[4]) != float(want.get("uhf", -1)) or float(cells[5]) != float(want.get("vhf", -1)):
                problems.append(f"README bases: {cells[0]} {cells[4]} / {cells[5]}, plan says {want}")
        # radio tables: | radio | `channel` | name | `MHz` |
        if re.fullmatch(r"\d+(\.\d+)?", cells[-1] or "") and re.fullmatch(r"\d+", cells[1] or ""):
            f = round(float(cells[-1]), 3)
            n += 1
            if f not in by_freq:
                problems.append(f"README radio: {cells[2]} at {cells[-1]} MHz, not in the plan")
    return n


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else max(glob.glob(str(ROOT / "VEAF_OpenTraining_GermanyCW_ICAO_ETAR_*.miz")),
                                                     key=os.path.getmtime)
    by_title, by_freq = plan()
    problems = []
    raw = zipfile.ZipFile(path).read("mission")
    # "ö" is C3 B6 in UTF-8; read as cp1252 and written back as UTF-8 it becomes C3 83 C2 B6 ("Ã¶")
    mojibake = len(re.findall(rb"\xc3[\x82\x83]\xc2[\x80-\xbf]", raw))
    if mojibake:
        problems.append(f"mission: {mojibake} names encoded twice (UTF-8 read as cp1252, e.g. 'NÃ¶rvenich')")
    miz = read_miz(path)
    n_radio = check_radios(miz.mission_content, by_title, by_freq, problems)
    texts = [v for k, v in miz.mission_content.items() if k.startswith("description") and isinstance(v, str)]
    texts += [v for v in (miz.dictionary_content or {}).values() if isinstance(v, str)]
    n_brief = sum(check_text("briefing DCS", t, by_title, problems) for t in texts)
    n_readme = check_readme(by_title, by_freq, problems)
    print(f"{os.path.basename(path)}: {n_radio} injected channels, {n_brief} briefing pairs, {n_readme} README cells")
    grouped = {}
    for p in problems:
        grouped.setdefault(re.sub(r"^radio  .+? slot \d+: ", "radio: ", p), []).append(p)
    for k, v in grouped.items():
        print(f"  {k}" + (f"  (x{len(v)}, e.g. {v[0].split(':')[0]})" if len(v) > 1 else ""))
    print("VERDICT:", "OK, every frequency agrees with presets.yaml" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
