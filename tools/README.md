# Outils de la mission

Scripts Python qui lisent la mission et produisent ce qu'on ne tape pas à la main : le briefing, la mission de
test, les contrôles. Ils se lancent **depuis le dossier de la mission** :

```powershell
python tools/gather.py
```

Ils importent le code Python de VMCT : par défaut le dépôt voisin `../VEAF-Mission-Creation-Tools`, ou le dossier
désigné par la variable `VMCT_PY` (un export de `develop`, quand le dépôt VMCT est sur une autre branche) :

```powershell
$env:VMCT_PY = "D:\chemin\vers\veaf-tools"   # le dossier src/python/veaf-tools
```

| Script | Ce qu'il fait |
|---|---|
| `gather.py` | Relève dans la mission tout ce que le briefing affiche → `tools/briefing_data.json` |
| `gen_readme.py` | Écrit `README.md` (le briefing des pilotes) à partir de `briefing_data.json`, et les cartes via `gen_map.py` : la carte générale en tête, chaque zoom dans la section qu'il illustre |
| `gen_map.py` | Dessine sur un fond OpenStreetMap (tuiles mises en cache dans `tools/tiles/`) la carte générale `docs/carte.jpg` et les zooms `docs/cartes/` (liste `ZOOMS` : un titre et les objets à cadrer), copie les images dans `src/mission/l10n/DEFAULT/` et les déclare dans `mapResource` et les `pictureFileName*` de la mission |
| `check_frequencies.py` | Compare le plan radio `src/presets.yaml` aux radios injectées dans chaque appareil, au briefing DCS et au README ; finit sur une ligne `VERDICT` |
| `verify.py` | Contrôles du `.miz` construit : identifiants et noms en double, slots, météo, heure, configuration serveur |
| `make_test_mission.py` | Construit la mission de test locale : profil `LOCAL_TEST`, game master, A-10C II en slot classique, pont dcs-bridge → `bridge/bridge-GermanyCW-OT.miz` |
| `probe_scenery.py` | En jeu, par dcs-bridge : quels véhicules l'éditeur a posés dans les bois, en ville ou dans l'eau |
| `probe_gen.py` | En jeu : cherche la clairière la plus proche de chaque groupe, pour déplacer ceux qui sont dans les bois |
| `run_actions.py` | Exécute un lot d'actions `veaf-mission-mcp` décrit dans un fichier JSON |

Données d'entrée, relevées une fois sur la carte : `airfields.json` (aérodromes GermanyCW), `red_airfields.json`,
`ad_positions.json` (défense des bases bleues), `bullseye.json`, `support.json` (hippodromes des ravitailleurs et
AWACS).

**Après tout changement de la mission** : `gather.py` puis `gen_readme.py`, et `check_frequencies.py` sur le `.miz`
reconstruit.

**La sonde `probe_scenery.py` se lance au démarrage de la mission, avant d'activer la moindre zone.** Elle interroge
`Disposition.getSimpleZones`, qui répond « y a-t-il de la place ici » : un véhicule prend de la place, donc une
mesure faite après le spawn compte les véhicules, pas les arbres (journal, §9.5). Les statiques ne sont testées que
pour l'eau : un bâtiment bloque son propre test où qu'il soit (§9.4).
