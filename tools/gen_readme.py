"""Render briefing_data.json into the mission README (the pilots' briefing) and the maps (via gen_map.py).

Run gather.py first: every value comes from the mission folder, nothing is typed by hand.
"""

import json
import os

S = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(S, "briefing_data.json"), encoding="utf-8"))
from paths import ROOT as _ROOT  # noqa: E402

ROOT = str(_ROOT)

# ── maps: docs/carte.jpg, the zooms of docs/cartes/ and the DCS briefing pictures ────────────
import gen_map  # noqa: E402

gen_map.render()
bu = D["bullseye"]
# zone numbers, in the same order gen_map draws them
zone_num = {z["key"]: i for i, z in enumerate([z for z in D["zones"] if not z["training"]], 1)}


# ── markdown ─────────────────────────────────────────────────────────────────
def c(v):
    return f"`{v}`"


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    out += ["| " + " | ".join(str(x).replace("|", "/") for x in r) + " |" for r in rows]
    return "\n".join(out)


side = {"blue": "Bleu", "red": "Rouge"}
ad_by = {a["name"]: a for a in D["ad"]}
ADL = {"-avenger_squad": "Avenger", "-nasams": "NASAMS", "-sa15": "SA-15", "-sa11": "SA-11", "-patriot": "Patriot", "-blue_ewr": "Radar d'alerte"}
date, start = D["date"], D["start"]
md = []
w = md.append
w("# VEAF Open Training — GermanyCW (moderne)")
w("")
w("Mission d'entraînement ouverte des serveurs VEAF, sur la carte **Germany Cold War** de DCS, dans un "
  "scénario moderne fictif. Ce document est le briefing complet : bases, soutien, zones, QRA, CAP, radio, météo. "
  "Les positions sont données en coordonnées (degrés, minutes décimales) et en cap/distance depuis le bullseye "
  "(cap vrai, nautiques).")
w("")
w(table(["Mission", "Date", "Heure de base", "Bullseye (bleu et rouge)", "Météo réelle", "ATC"],
        [[c(D["name"]), f'{date["Day"]:02d}/{date["Month"]:02d}/{date["Year"]}', f'{start // 3600:02d}:{start % 3600 // 60:02d} (heure de la carte, UTC+2)',
          f'Brocken · {c(bu["ddm"])}', "ETAR (Ramstein)", "coupé sur tous les aérodromes"]]))
w("")
w("**Sommaire** : [Situation](#situation) · [Carte](#carte) · [Bases](#bases) · [Ravitailleurs et AWACS](#ravitailleurs-et-awacs) · "
  "[Porte-avions](#porte-avions) · [Drones laser](#drones-laser) · [Entraînement](#entraînement) · [Zones de combat](#zones-de-combat) · "
  "[QRA](#qra) · [CAP à la demande](#cap-à-la-demande) · [Combat entre joueurs](#combat-entre-joueurs) · "
  "[Défense aérienne](#défense-aérienne) · [Plan radio](#plan-radio) · [Météo et heures](#météo-et-heures) · "
  "[Commandes utiles](#commandes-utiles) · [Pour les créateurs de mission](#pour-les-créateurs-de-mission)")
w("")
w("## Situation")
w("")
w("Une crise OTAN–Russie fige les deux camps sur la ligne de l'ancienne frontière interallemande, de la baie de Lübeck "
  "à la frontière tchèque (environ 300 nm). L'OTAN tient l'Ouest ; la Russie tient l'Est et Berlin. Danemark, Suède et "
  "Pologne restent neutres.")
w("")
w("Zones de combat, missions CAP et soutien se pilotent par le menu radio F10 (*Zones de combat*, *MISSIONS*, *ASSETS*).")
w("")
ZOOM = {s: (f"docs/cartes/carte_{i:02d}_{s}.jpg", t) for i, (s, t, _) in enumerate(gen_map.ZOOMS, 1)}


def zooms(*slugs):
    """The zoomed maps of a section, two per row, each opening full size when clicked (a single one, full width)."""
    if len(slugs) == 1:
        w(f"![{ZOOM[slugs[0]][1]}]({ZOOM[slugs[0]][0]})")
        w("")
        return
    cells = [f'<td width="50%"><a href="{ZOOM[s][0]}"><img src="{ZOOM[s][0]}" alt="{ZOOM[s][1]}"></a><br>'
             f'<sub>{ZOOM[s][1]}</sub></td>' for s in slugs]
    rows = ["<tr>" + "".join(cells[k:k + 2]) + "</tr>" for k in range(0, len(cells), 2)]
    w("<table>" + "".join(rows) + "</table>")
    w("")


w("## Carte")
w("")
w("![Carte de la mission](docs/carte.jpg)")
w("")
w("Cartes zoomées, reprises dans les sections qu'elles illustrent : "
  + " · ".join(f"[{t.split(' : ')[0]}]({f})" for f, t in ZOOM.values()) + ".")
w("")
w("Carrés : bases avec slots (bleu / rouge). Traits pleins : hippodromes des ravitailleurs et AWACS. Pointillés : CAP à la "
  "demande. Cercles : QRA. Pastilles vertes : entraînement (H hélicos, A attaque, S SEAD). Pastilles rouges numérotées : "
  "zones de combat (numéros de la liste plus bas). Tirets épais : sanctuaires. Navire : porte-avions. L'arène est hors du cadre, au nord (flèche). Fond de carte OpenStreetMap ; la ligne de front est approximative. "
  "Le briefing de la mission, dans DCS, montre cette carte puis les zooms (flèches sous l'image, molette pour grossir), "
  "et la carte F10 porte les mêmes dessins, chaque camp ne "
  "voyant que les siens.")
w("")
w("## Bases")
w("")
rows = []
for b in D["bases"]:
    ad = " + ".join(ADL.get(ad_by[n]["cmd"].split(",")[0], ad_by[n]["cmd"]) for n in b["ad"])
    rows.append([f'**{b["name"]}**' + (" (base mère)" if b["name"] == "Ramstein" else ""), side[b["side"]], c(b["ddm"]), c(b["be"]),
                 c(b["uhf"]), c(b["vhf"]), ad])
rows += [[f'**FARP {f["name"]}**', "Bleu", c(f["ddm"]), c(f["be"]), "—", "—", "posé au démarrage (`-farp`)"] for f in D["farps"]]
w(table(["Base", "Camp", "Position", "Bullseye", "UHF", "VHF", "Défense"], rows))
w("")
w("Slots dynamiques, démarrage moteur chaud, carburant et munitions illimités. Les 49 autres aérodromes de l'Est sont "
  "rouges, sans slots.")
w("")
zooms("nord_ouest", "hesse")
w("## Ravitailleurs et AWACS")
w("")
ROLE = {"Texaco 1": "perche · nord", "Arco 1": "panier · nord", "Texaco 2": "perche · sud", "Arco 2": "panier · sud",
        "Shell 1": "perche · arrière", "Overlord 1": "AWACS · nord", "Magic 1": "AWACS · sud", "Tanker Rouge": "ravitailleur",
        "AWACS Rouge": "AWACS"}
w(table(["Indicatif", "Camp", "Appareil", "Rôle", "MHz", "TACAN", "Niveau", "Vitesse", "Bullseye", "Hippodrome (extrémités)", "Escorte"],
        [[f'**{s["name"]}**', side[s["side"]], s["type"], ROLE[s["name"]], c(f'{s["freq"]:.1f}'), c(s["tacan"]) if s["tacan"] else "—",
          c(f'FL{s["fl"]}'), c(f'{s["kt"]} kt'), c(s["mid"]["be"]), f'{c(s["a"]["ddm"])}<br>{c(s["b"]["ddm"])}',
          "oui" if s["escort"] else "non"] for s in D["support"]]))
w("")
w("Les ravitailleurs de secteur ne sont pas escortés : à vous de les défendre. Marqueurs F10 : `-tanker <nom>` amène un "
  "ravitailleur au marqueur ; `-tankerlow` et `-tankerhigh` mettent le plus proche au FL120 ou au FL220.")
w("")
cv = D["carrier"]
w("## Porte-avions")
w("")
w(table(["Navire", "Position de départ", "Bullseye", "TACAN", "ICLS", "Link 4", "Tour"],
        [[f'**{cv["name"]}** (groupe CSG-74, {cv["escorts"]} escorteurs)', c(cv["ddm"]), c(cv["be"]), c(cv["tacan"]), c(cv["icls"]),
          c(f'{cv["link4"]:.1f}'), c(f'{cv["tower"]:.1f}')]]))
w("")
deck = {}
for x in cv["deck"]:
    deck.setdefault(x["type"], [0, 0])[1 if x["hot"] else 0] += x["n"]
w("En mer du Nord, à l'ouest d'Helgoland. Slots sur le pont : " +
  ", ".join(f'{t.replace("FA-18C_hornet", "F/A-18C")} ({a} à froid, {h} moteur chaud)' for t, (a, h) in deck.items()) +
  " ; les slots dynamiques du pont proposent F/A-18C, F-14B, AV-8B, UH-1H et AH-64D. Le menu F10 *CARRIER OPS* met le "
  "porte-avions face au vent pour 45 ou 90 minutes, avec un ravitailleur S-3B et un hélicoptère de sauvetage.")
w("")
w("## Drones laser")
w("")
w(table(["Drone", "Appareil", "Au-dessus de", "Code laser", "Radio", "Hauteur", "Bullseye"],
        [[f'**{x["name"]}**', x["type"], x["where"], c(x["jtac"]), c(f'{x["freq"]} {x["mod"]}'), c(f'{x["agl"]:,} m sol'.replace(",", " ")), c(x["be"])] for x in D["drones"]]))
w("")
w("Un drone tourne au-dessus des zones d'entraînement hélicoptères et attaque, et désigne au laser ce qu'il voit ; le menu "
  "F10 *ASSETS* le remet en vol s'il a été abattu : au niveau difficile, l'AAA lourde de la zone le touche à cette hauteur "
  "(Reaper 2 abattu par un S-60 à Wahner Heide le 28/09). Il ne désigne que des véhicules, ce que sont aussi les cibles des niveaux "
  "faciles. Pas de drone sur la zone SEAD de Borkenberge : ses SAM portent plus loin "
  "que le laser, qui ne marque qu'à 10 km.")
w("")
w("## Entraînement")
w("")
w("Côté ouest, loin du front. Trois niveaux par famille, chacun comprenant ceux d'en dessous. **Activez un seul niveau par "
  "famille à la fois.**")
w("")
zooms("sud_ouest", "rhenanie")
for fam, label in (("Baumholder", "Hélicoptères"), ("WahnerHeide", "Attaque"), ("Borkenberge", "SEAD / DEAD")):
    lv = [z for z in D["zones"] if z["key"].startswith(f"combatZone_{fam}_")]
    z0 = lv[0]
    w(f'### {label} — {z0["name"].split(" - ")[0]}')
    w("")
    w(f'{c(z0["ddm"])} · bullseye {c(z0["be"])} · rayon {z0["radius_nm"]} nm · menu F10 « {z0["menu"]} »')
    w("")
    for z in lv:
        body = z["briefing"].split(". ", 1)[1].split(" Ravitailleur")[0]
        w(f'- **{z["name"].split(" - ")[1].capitalize()}** — {body}')
    w("")
sz = next(z for z in D["zones"] if z["key"] == "combatZone_Hunsrueck_SAR")
w("### Hélicoptères hors combat — Hunsrück")
w("")
w(f'{c(sz["ddm"])} · bullseye {c(sz["be"])} · menu F10 « {sz["menu"]} »')
w("")
w(sz["briefing"].split(". ", 1)[1])
w("")
w(table(["Balise", "FM", "Position", "Bullseye"], [[x["name"].replace("Balise ", ""), c(f'{x["freq"]:.1f}'), c(x["ddm"]), c(x["be"])] for x in D["sar"]]))
w("")
w("## Zones de combat")
w("")
w("Côté est. Les numéros renvoient à la carte. Chaque zone s'active par le menu F10 *Zones de combat*, qui redonne son "
  "briefing et sa position. La plupart des sites changent d'une activation à l'autre : une partie des cibles ou "
  "de la défense est tirée au sort, et la fiche dit laquelle.")
w("")
zooms("front_nord", "front_centre", "berlin", "baltique")
for menu in ("Front", "SEAD", "Convois", "Frappe profonde", "Bases aériennes", "Antinavire"):
    w(f"### {menu}")
    w("")
    for z in D["zones"]:
        if z["training"] or z["menu"] != menu:
            continue
        n = zone_num[z["key"]]
        body = z["briefing"].split(" : ", 1)[1] if " : " in z["briefing"] else z["briefing"]
        w(f'**{n}. {z["name"]}** — {c(z["ddm"])} · bullseye {c(z["be"])}')
        w("")
        w(body)
        w("")
w("## QRA")
w("")
rows = []
for q in D["qra"]:
    tiers = "<br>".join(f'dès {x["n"]} intrus : {x["pick"]} vol{"s" if x["pick"] > 1 else ""} parmi ' +
                        ", ".join(q["types"][p] for p in x["pool"]) for x in q["tiers"])
    rows.append([f'**{q["name"]}**', side[q["side"]], c(q["ddm"]), c(q["be"]), c(f'{q["radius_nm"]} nm'), q["base"], tiers])
w(table(["QRA", "Défend", "Centre", "Bullseye", "Rayon", "Base", "Réponse"], rows))
w("")
w(f"Les chasseurs décollent {D['qra_delay'][0]} s après l'entrée du premier intrus dans le cercle" + ("." if D["qra_helos"] == [True] else " ; les hélicoptères ne les déclenchent pas."))
w("")
w("Couloirs sans QRA rouge : le nord-ouest (Lübtheen, Parchim, Ludwigslust), le centre (Altmark, Magdeburg, Altengrabow) "
  "et la Thuringe (Ohrdruf, Brocken).")
w("")
w("## CAP à la demande")
w("")
w(table(["Mission", "Camp", "Appareils", "Niveau", "Bullseye", "Centre", "Description"],
        [[f'**{x["name"]}**', side[x["side"]], f'{x["n"]} × {x["type"]}', c(f'FL{x["fl"]:03d}'), c(x["mid"]["be"]), c(x["mid"]["ddm"]),
          x["briefing"].split(" Hippodrome")[0]] for x in D["caps"]]))
w("")
w("À lancer par le menu F10 *MISSIONS*.")
w("")
w("## Combat entre joueurs")
w("")
w("Des joueurs volent des deux côtés. Le combat entre joueurs est **permis partout, sauf dans les sanctuaires** : un pilote "
  "du camp adverse y est prévenu dès l'entrée, puis détruit au bout de 60 s, et les missiles tirés sur les défenseurs sont "
  "détruits. Les limites sont tracées sur la carte F10.")
w("")
w(table(["Sanctuaire", "Protège", "Étendue", "Destruction après"],
        [[f'**{z["name"]}**', side[z["side"]], "les arrières à l'ouest : Ramstein, Spangdahlem, Büchel, Nörvenich, Wiesbaden et les zones d'entraînement"
          if z["side"] == "blue" else f'{z["radius_nm"]:g} nm autour de la base (bullseye {c(z["be"])})', f'{z["delay"]} s'] for z in D["sanctuaries"]]))
w("")
az = D["arena_zone"]
w("### Arène")
w("")
w(f'Au-dessus du Grand Belt, en territoire neutre, loin du front : {c(az["ddm"])} · bullseye {c(az["be"])} · rayon {az["radius_nm"]} nm. '
  "Slots en départ en vol au FL250, bleus à l'ouest, rouges à l'est, face à face à 57 nm.")
w("")
zooms("arene")
rows = []
for sd in ("blue", "red"):
    for fox in ("FOX3", "FOX1"):
        lst = [a for a in D["arena"] if a["side"] == sd and a["fox"] == fox]
        if lst:
            rows.append([side[sd], fox.replace("FOX", "Fox "), ", ".join(f'{a["type"].replace("FA-18C", "F/A-18C").replace("MiG-21Bis", "MiG-21bis")} ×{a["n"]}' for a in lst),
                         c(f'{lst[0]["freq"]:.1f}')])
w(table(["Camp", "Missiles", "Slots", "MHz"], rows))
w("")
w("AWACS de l'arène : " + " ; ".join(f'{x["name"]} ({x["type"]}, {side[x["side"]].lower()}) {x["freq"]:.1f}, FL{x["fl"]}' for x in D["arena_awacs"]) + ".")
w("")
w("## Défense aérienne")
w("")
w("**Rouge (renseignement)** : SA-10 permanents à Berlin, Rostock et Leipzig ; SA-15 et SA-11 sur les bases rouges avec "
  "slots (Laage, Holzdorf, Allstedt) ; trois radars d'alerte 55G6 en réseau et un réseau de guetteurs Skynet. Chaque zone "
  "de combat a sa propre défense, décrite dans sa fiche.")
w("")
w("**Bleu** :")
w("")
w(table(["Site", "Système", "Position", "Bullseye"],
        [[a["name"].replace("AD-", ""), ADL.get(a["cmd"].split(",")[0], a["cmd"].split(",")[0]), c(a["ddm"]), c(a["be"])]
         for a in D["ad"] if a["side"] == "blue"]))
w("")
w("## Plan radio")
w("")
for sd, label in (("blue", "Bleu"), ("red", "Rouge")):
    rows = []
    for role, title in (("primary_1", "Radio 1 (UHF)"), ("primary_2", "Radio 2 (VHF)")):
        for k, v in D["radio"][sd][role].items():
            f = D["channels"].get(v, {})
            rows.append([title, c(k), str(v).replace("Base-", "").replace("-", " "), c(f.get("uhf") if role == "primary_1" else f.get("vhf"))])
    w(f"### {label}")
    w("")
    w(table(["Radio", "Canal", "Nom", "MHz"], rows))
    w("")
w("Presets injectés dans les appareils à radio programmable ; les FC3, le Ka-50 et les Gazelle n'en reçoivent pas. "
  "FM : canaux 1 à 30 = 30 à 59 MHz.")
w("")
w("## Météo et heures")
w("")
w(table(["Variante", "Heure", "Météo", "METAR"], [[c(v["name"]), c(v["time"]), v["kind"], c(v["metar"]) if v["metar"] else "—"] for v in D["versions"]]))
w("")
w("Sur le serveur VEAF, la météo réelle de Ramstein est appliquée au lancement (RealWeather). Aube = lever du soleil, "
  "soir = 45 min avant le coucher.")
w("")
w("## Commandes utiles")
w("")
w("- `-tanker <nom>` : amène le ravitailleur nommé à la position du marqueur.")
w("- `-cas` : fait apparaître une cible CAS aléatoire au marqueur.")
w("- `-point <nom>` : nomme un point de la carte.")
w("- `-smoke`, `-light`, `-signal` : fumigène, éclairage, fusée.")
w("- `-jtac`, `-afac` : JTAC au sol, drone AFAC.")
w("")
w(open(os.path.join(S, "readme_makers.md"), encoding="utf-8").read())
open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
print("README.md", sum(len(x) for x in md), "docs/carte.jpg and docs/cartes/ ok")
