## Pour les créateurs de mission

Construite de zéro avec VEAF Mission Creation Tools (`veaf-tools`) et le serveur MCP `veaf-mission-mcp`, en
s'inspirant de la v5 (`VEAF-Open-Training-Mission-GermanyCW`, 1980) sans la recopier. Trois ensembles sont repris de
l'Open Training Caucase v5 : l'arène « Air Quake » (emports et leurres), le groupe aéronaval du Stennis (tâches ATC,
Pedro, S-3B, slots de pont, entrepôt) et la zone hélicoptère « Mountain Hike » (balises et sons).

### Construire

```powershell
# configuration serveur : sécurité active, logs info, 20 variantes météo dans missions/
.\veaf-tools.exe mission build

# essais sur un poste : sécurité coupée, logs debug, noms de groupes lisibles, pas de variantes
.\veaf-tools.exe mission build --profile LOCAL_TEST
```

Contrôle avant build : `.\veaf-tools.exe validate` (ou l'action MCP `validate_mission`).

### Fichiers

| Fichier | Rôle |
|---|---|
| `mission.yaml` | Identité, sécurité, profil `LOCAL_TEST`, modules, zones (niveaux imbriqués par `includes:`), QRA, CAP, assets |
| `src/mission/` | La mission DCS éclatée (groupes, zones de déclenchement, aérodromes, dessins F10) |
| `src/presets.yaml` | Plan radio bleu et rouge |
| `src/versions.yaml` | Variantes météo et heure |
| `src/waypoints.yaml` | Points de navigation injectés dans les appareils joueurs |
| `src/warehouses.yaml` | Bases qui offrent des slots (`exclude_airports` pour les bases rouges sans slots), carburant et munitions illimités, appareils proposés sur le pont du porte-avions (`ships:`) |
| `src/dynamic-slot-templates.yaml` | Appareils proposés en slots dynamiques (WW2 retirés) |
| `src/mission/l10n/DEFAULT/*.ogg` | Sons des balises de la zone de sauvetage (MH01 à MH03, SOS), déclarés dans `mapResource` |
| `docs/carte.jpg`, `docs/cartes/` | La carte de ce briefing et ses zooms par zone (fond OpenStreetMap) ; les mêmes images sont dans `src/mission/l10n/DEFAULT/` pour le briefing DCS, listées côté bleu et neutre seulement (voir `tools/gen_map.py`, `declare_pictures`) |

Ce README est **généré depuis la mission** : après tout changement, relancer `gather.py` puis `gen_readme.py` (qui appelle `gen_map.py` pour la carte)
(dans `tools/`, voir `tools/README.md`), sans rien retaper à la main.

### Limites connues

Construite avec veaf-tools 6.25.0.1, construit depuis la branche `develop` de VMCT (`dd60e7a5`, 29/09/2026 : commandes F10 sécurisées « pour tous » posées dans le menu de chaque groupe, véhicules créés par script chauds dès le départ, panneau de zone qui compte les statiques). Plusieurs éléments n'ont pas d'action MCP dédiée et ont été
écrits par script sur la table de la mission : leurres et indicatifs des slots de l'arène, tâches ATC et slots de pont du
porte-avions, entrepôt du navire, balises radio de la zone de sauvetage, balises de tirage (`#spawngroup`,
`#spawncount`) des zones. Ils se relisent dans `src/mission/mission` comme le reste.

Vérifié en jeu les 28 et 29/09 (`tools/test_en_jeu.py`, journal §12 et §13) : TACAN, ICLS et Link 4 du Stennis,
points logistiques CTLD des FARP, destruction dans les sanctuaires, marquage laser des drones, tirages des zones,
imbrication des niveaux, statiques, navires, convois, engagement des CAP, fréquences de chaque appareil. Reste à
vérifier : les balises relevables au radiogoniomètre (il faut un hélicoptère sur la zone de sauvetage).
