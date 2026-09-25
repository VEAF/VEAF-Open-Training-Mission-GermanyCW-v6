# Open Training GermanyCW v6 — résumé du chantier (24-25/09/2026)

## 1. Point de départ et choix

- Mission créée **à partir d'un dossier vide** avec le prompt `VEAF-Mission-Creation-Tools/.prompts/new-open-training-mission.fr.md`. La v5 (`VEAF-Open-Training-Mission-GermanyCW`) a servi de référence, sans contrainte de la reprendre.
- Choix de David :
  - époque **moderne** ;
  - gabarit **standard** ;
  - **pas d'escorte** sur les ravitailleurs de secteur ;
  - sécurité **active, sans mot de passe**.
- Dossier : `D:\dev\_VEAF\VEAF-Open-Training-Mission-GermanyCW-v6`.
- Dépôt Git : https://github.com/VEAF/VEAF-Open-Training-Mission-GermanyCW-v6. Il est privé, sur la branche `main`, avec un premier commit `0d31188`.

## 2. Contenu de la mission

| Domaine | Contenu |
|---|---|
| Nom | `VEAF_OpenTraining_GermanyCW_ICAO_ETAR`, en français, ATC muet |
| Bases | 61 aérodromes attribués : 9 bleus et 3 rouges avec slots, 49 rouges sans slot (`exclude_airports`) |
| Soutien | Texaco 1/2, Arco 1/2, Shell 1, Overlord 1, Magic 1, Tanker rouge, AWACS rouge, plus des escortes pour Shell, Overlord, Magic et les deux rouges |
| Défense aérienne | 35 groupes `AD-*`, FARP Baumholder et Göttingen |
| Zones de combat | 25 zones ; les niveaux Medium et Hard incluent le niveau inférieur (`includes:`) |
| QRA / CAP | 5 QRA (menu radio public retiré) ; 6 CAP (tâches : engager d'abord, puis orbite) |
| Modules | CTLD, CSAR, AIEN, STTS, Skynet (réseau de spotters, vue radio) |
| Radio | Plan refait. Bleu : 20 canaux UHF, patrouilles en 360.x. Bases en 270.x / 130.x. Ravitailleurs 251-255, AWACS 265/266, rouges 260/261 |
| Variantes | 20 variantes : nuit, aube (`sunrise`), matin, jour, soir (`sunset-45*60`) × réel (METAR ETAR), dégagé, épars, pluie. Fuseau `Europe/Berlin`, date 14/06/2025 |
| Divers | Bullseye sur le Brocken ; 11 points de navigation, 4 plans de vol ; 38 dessins F10 ; avions WW2 retirés des modèles de slots dynamiques (102 gardés) |
| Profil `LOCAL_TEST` | debug, sécurité désactivée, noms visibles, pas de météo réelle |

## 3. Outils VMCT : défauts trouvés et corrigés

- Défauts rencontrés avec la version 6.24.0 :
  - météo des variantes jamais lue par DCS ;
  - données avwx absentes de l'exe ;
  - presets radio injectés dans 0 avion ;
  - collisions d'ids ;
  - lever du soleil calculé en UTC ;
  - pas d'imbrication de zones ;
  - slots dynamiques forcés sur toutes les bases.
- Suite donnée :
  - Tous ces points sont remontés dans le lot VMCT **FIX-SCRATCH-MISSION-FINDINGS**, rouvert dans une session VMCT (tickets 15-22, #1000).
  - Les 5 contournements provisoires ont été retirés ; ils sont gardés dans `.veaf-backups/contournements-6.24.0/`.
  - Le rebuild avec develop est **validé** : 0 doublon, 12 bases à slots, météo différente par variante, aube à 05:23, presets sur 62 des 102 modèles, includes générés.
- Exes reconstruits depuis develop (`veaf-tools`, `veaf-logs`, updater) et déployés dans la mission (6.24.0.2).

## 4. Mes erreurs, corrigées

- Navires espacés de 20 m : réespacés à 600 m.
- CAP sans tâche d'engagement : tâches remises dans l'ordre.
- Menu radio QRA ouvert à tous : retiré.
- Canaux radio hors plage ou au-delà de 20 : corrigés.
- Coordonnées affichant « 60.000' » : retenue des minutes corrigée.
- J'avais listé des défauts VMCT déjà corrigés : recadré par David.
- Mission de test livrée avec seulement des slots dynamiques, **inutilisables en solo** : ajout d'un slot A-10 classique.
- Email de David envoyé par erreur dans un en-tête HTTP à overpass-api.de : à ne jamais refaire.

## 5. Briefing

- **Le README est le briefing pilotes** : c'est le point d'entrée (règle de David). La carte est dans `docs/carte.svg`.
- Il est généré par `gather.py` puis `gen_readme.py`, depuis les données de la mission, sans aucune valeur tapée à la main.
- L'ancien `briefing.html` et l'artifact claude.ai sont périmés. Copies dans `.veaf-backups/ancien-briefing/`.

## 6. Mission de test locale

- `python .veaf-backups/outils-controle/make_test_mission.py` produit `bridge/bridge-GermanyCW-OT.miz` :
  - build `LOCAL_TEST` ;
  - **game master** bleu et rouge ;
  - **A-10C II en slot classique**, démarrage à froid à Ramstein, parking 4 ;
  - trigger dcs-bridge.
- Règles (en mémoire) :
  - les slots dynamiques ne marchent qu'en multijoueur ;
  - les slots de test vont dans la copie de test, jamais dans les sources ;
  - **c'est Claude qui lance `dcs-serve`**, David ne s'occupe que de DCS et du slot.

## 7. Audit « unités dans les bois »

- **Déclencheur** : David a signalé que la zone de Wahner Heide (32U LB 679 393) est dans les bois.
- **Méthode** : sonde lancée dans DCS via dcs-bridge avec `Disposition.getSimpleZones`, l'API que VEAF utilise déjà pour éviter le décor. Attention, elle renvoie ses candidats en `{x, y}` et non `{x, z}`.
- **Premier passage**, sur les points de l'éditeur : 29 groupes déplacés par `apply_forest_moves.py`.
  - **Wahner Heide** : toute la zone décalée de 2,2 km vers l'ouest.
  - **Torgau** : cibles sorties de l'Elbe.
  - **SAM de Ramstein** : Avenger à 3 km, NASAMS à 6 km.
  - **Autres** : Lübtheen, Brocken, Baumholder, EWR Centre rouge.
  - **Wittstock** laissé en forêt : aucune clairière à 6 km.
  - Seconde sonde : 42 unités OK sur les nouveaux points.
- **Second passage**, avec les 25 zones activées en jeu : **53 objets sur 184** sont encore sous les arbres ou dans l'eau.
  - Calibration : Letzlingen, à découvert, donne 0 alerte, donc les unités ne faussent pas le test.
  - J'avais d'abord écarté ces alertes à tort.
- **Cause racine, côté VMCT** (log `dcs.log` fourni par David) :
  1. `findSpawnPoint` exige 100 m de dégagement, puis retombe sur un tirage aléatoire sans regarder le décor. Ça arrive 38 fois sur 106 commandes, même en rase campagne.
  2. Les unités d'une batterie sont posées sans aucun test de décor ; seule l'eau est refusée.
  3. Une unité refusée disparaît en silence (Torgau : Strela-1, Strela-10 et Ural perdus), et le message s'affiche aux joueurs même en activation silencieuse.
- **Suite** : une session VMCT (Fable) rouvre le lot **FIX-PLACEMENT-IGNORES-SCENERY** avec ces constats.
  - Recette : `outils-controle/probe_units_in_scenery.lua`.
  - Question laissée à David : pour le contenu de l'éditeur, revenir à la position déclarée plutôt que tirer un point au hasard ?

## 8. Ce que j'ai appris en route

### DCS
- Coordonnées de mission : `x` = nord, `y` = est. Dans le Lua de DCS, un vec3 met l'altitude en `y` et l'est en `z`.
- Conversion : `veaf_libs.coordinates.latlon_to_xy` / `xy_to_latlon('GermanyCW', …)`. L'horloge de la mission GermanyCW est à UTC+2.
- `land.getSurfaceType` : 1 = terre, 2 = eau peu profonde, 3 = eau, 4 = route, 5 = piste. Un barrage est vu comme une piste, et un pont peut donner « eau » (convoi A24).
- **`Disposition.getSimpleZones(point, rayon, dégagement, n)`** :
  - candidats rendus en `{x, y}` et non `{x, z}` ;
  - au plus une dizaine de candidats ;
  - le rayon ne borne pas vraiment les réponses ;
  - il ignore l'eau : il propose des points libres sur un lac.
- **Mesurer avec `getSimpleZones`** :
  - la distance au candidat le plus proche est un mauvais indicateur, puisque les candidats sont peu nombreux et tirés au hasard ;
  - le bon test : rayon de 20 à 60 m autour du point exact ; 0 candidat veut dire bois ou bâtiments ;
  - les unités posées ne faussent pas ce test (calibré sur Letzlingen) ;
  - une clairière de 100 à 250 m est rare en Allemagne.
- Les slots dynamiques ne fonctionnent qu'en multijoueur.

### VEAF en jeu
- Au démarrage, les groupes des zones de combat sont retirés. Pour les faire apparaître : `veafCombatZone.ActivateZone(nom, true)`. Les noms de zones sont en minuscules dans `veafCombatZone.zonesDict`.
- Les SAM `#veafInterpreter` sont recréés sous un autre nom (`[b]-NASAMS C battery#10297`) : on les retrouve par leur position, pas par le nom de l'éditeur.
- Le contenu de l'éditeur et les alias de rayon 0 ne sont jamais écartés du décor (règle du 27/08). Les éléments de zone et les batteries repassent en revanche par `findSpawnPoint`, avec les défauts décrits en section 7.
- Sans `exclude_airports`, le build met `dynamicSpawn = true` sur tous les aérodromes d'un camp déclaré.

### dcs-bridge
- `dcs-serve.exe` : HTTP sur 127.0.0.1:8080, TCP sur 7777. L'API est `/api/exec`, avec un jeton `Bearer`.
- Côté MCP : `capabilities` puis `exec_lua`, qui demande le rôle superuser.
- La mission doit contenir le trigger du pont (`veaf-tools dcs inject-bridge`), et `MissionScripting.lua` doit être désanitisé.
- Pour éviter de renvoyer de gros scripts, déclarer une fonction globale une seule fois (`_G.__probe`), puis l'appeler.
- Le terrain se sonde sans recharger la mission : la mission chargée ne change rien.

### Outils et machine
- Le catalogue MCP s'appelle directement en Python (`run_actions.py`). Il n'a **pas** d'action de déplacement de groupe : j'ai modifié le fichier de mission par script (`load_folder_mission` / `save_folder_mission`, qui fait sa propre sauvegarde).
- VMCT n'a pas de données de parking pour GermanyCW : le parking de l'A-10 est repris de la v5.
- `veaf-logs.exe` ouvert empêche de reconstruire l'exe.
- Sous Windows, lancer Python avec `PYTHONUTF8=1`.
- Le venv poetry de VMCT a déjà eu `python-dateutil` cassé (réinstallé).
- Un `"\n"` dans une chaîne Python qui contient du Lua devient un vrai retour à la ligne : le Lua casse.

### Méthode
- **Ne jamais écarter une alerte sur une hypothèse sans témoin.** J'ai rejeté les alertes SAM avec « les unités se gênent entre elles » ; il a suffi d'une calibration pour montrer qu'elles étaient réelles.
- **Tester le point d'ancrage ne suffit pas.** Ce qui compte, c'est où les unités apparaissent réellement : activer les zones et sonder les unités en place.
- Le log fourni par David a désigné la cause racine plus vite que mes sondes : lire le `dcs.log` tôt.

## 9. Points ouverts

1. **NASAMS à 6 km de Ramstein** : acceptable, ou le rapprocher en acceptant une lisière ?
2. **Outils de contrôle hors dépôt** (`.veaf-backups/outils-controle/` : générateur du README, mission de test, sondes). Proposition : les déplacer dans un dossier `tools/` versionné.
3. **Clé CheckWX en clair** dans le `configuration.json` de la v5 : à révoquer.
4. **Session VMCT FIX-PLACEMENT-IGNORES-SCENERY** : en cours. À la livraison, rebuild et nouvelle sonde.
5. **Encore à vérifier en jeu** : statiques, navires, convois, FARP, imbrication des zones, engagement des CAP, portées des SAM.
6. Les 25 zones sont restées actives dans la partie de test en cours.
