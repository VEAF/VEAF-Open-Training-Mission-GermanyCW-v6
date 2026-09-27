# Open Training GermanyCW v6 — résumé du chantier (24-26/09/2026)

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

## 9. La suite du chantier « unités dans les bois » (25-26/09)

### 9.1 Une seule régression causait trois symptômes

`settlePosition` perdait le champ `hdg`, d'où un `math.deg(nil)` qui tuait la fonction planifiée en
silence. Conséquences : 6 zones sur 25 vides, 11 groupes perdus, **et toute la défense aérienne
absente** — 0 batterie générée au lieu de 9, Skynet se rabattant sur les gabarits de l'éditeur et en
rejetant 15 avec un message à l'écran. Corrigé par la PR VMCT #1003.

### 9.2 Déplacer unité par unité ne peut pas marcher

`settlePosition` n'a jamais déplacé quoi que ce soit : sur 20 unités bloquées, 25 candidats rendus,
25 valides sur le terrain, **0 accepté**. Elle bornait l'acceptation par le rayon demandé à DCS, or
**DCS ne respecte pas ce rayon** — on demande 50 m, il répond entre 52 et 171 m, médiane 130.

Et même corrigée, l'approche est condamnée : l'espacement naturel d'un groupe est de 20 à 27 m pour
un SAM, le point le plus proche que DCS propose est à 52 m. Tout déplacement à l'unité disloque la
formation d'un facteur 2 à 5. D'où la translation rigide du groupe (PR #1005, livrée en 6.25.0).

Aucune retouche des sources ne peut s'y substituer : `veafUnits` tire la disposition interne au
hasard **à chaque spawn**. Les ancres atterrissent exactement où on les vise (écart 4 à 22 m) et les
unités retombent quand même sous les arbres au tirage suivant. Seul le moment du spawn connaît la
disposition réelle.

À noter, parce que c'est le piège qui a coûté un aller-retour : **le rayon nul est une valeur par
défaut, pas une intention**. 100 des 118 commandes de spawn passent `radius 0`. Toute exemption
fondée dessus rend le correctif inerte. D'où le drapeau explicite `honouringDeclaredPosition`.

### 9.3 L'essai en jeu du 26/09 : la translation rigide est inerte elle aussi

Mission chargée, 25 zones activées, 102 groupes et 593 unités en place.

| mesure | avant #1005 | attendu | **mesuré** |
|---|---|---|---|
| alertes sur des groupes | 16-18 | ~0 | **19** |
| unités bloquées | ~81 | quelques-unes | **66** |
| espacements internes | intacts | intacts | **intacts** |

> **Ces chiffres sont faux, et le §9.5 dit pourquoi.** Ils sont relevés après le spawn, et le
> critère employé compte les **véhicules** autant que les arbres : une batterie serrée échoue au
> test où qu'elle soit. Le tableau est conservé parce que la conclusion qu'on en a tirée — la
> translation rigide ne suffit pas — tient sur le critère correct aussi, mais **aucun de ces
> nombres ne doit être cité**.

La seule promesse tenue est la formation. Ce qui est acquis sans réserve, c'est que **ce n'est pas
proche de zéro**.

Le diagnostic, étape par étape, parce qu'aucun des suspects évidents n'est coupable :

1. **Le correctif tourne** — `settleGroup` présente en jeu, `settlePosition` disparue. 55 groupes
   translatés (118 à 278 m), 11 en échec. *Le hash de version affiché (`6.24.0.5+f4211271`)
   désignait le commit de #1004 et induit en erreur : c'est la présence des fonctions qui tranche.*
2. **DCS obéit au mètre** — `settleGroup` instrumentée, une zone recyclée, positions relues :
   **0 m d'écart** entre le barycentre commandé et le réel.
3. **Le groupe atterrit quand même dans les bois** — le S-300 de Wittstock, translaté de 217 m, a
   **6 de ses 14 unités bloquées**. Son point d'arrivée est bloqué dans **12 directions sur 12 à
   10 m**, et ne se dégage qu'à 183 m.
4. **`Disposition.getSimpleZones` n'est pas déterministe** — cinq appels consécutifs identiques :
   candidat le plus proche à 1335, 1476, 1404, 1355, 1293 m. Un sixième en a trouvé un à 153 m.

C'est la même erreur que celle que #1005 corrigeait, déplacée d'un paramètre à l'autre : #1005 avait
établi que DCS n'honore pas le **rayon de recherche**, puis a supposé qu'il honore le **dégagement**,
et l'a écrit en commentaire sans le mesurer.

**Suite** : ticket 11 du lot VMCT FIX-PLACEMENT-IGNORES-SCENERY — le singleton propose, le code
vérifie. Chaque candidat est testé unité par unité avec le critère de la sonde, et plusieurs tirages
sont fusionnés.

### 9.4 Pièges de mesure, à relire avant toute nouvelle sonde

- **La sonde ne vaut rien pour les statiques.** Elle demande « 5 m de libre dans un rayon de 20 m » ;
  un bâtiment de 47×52 m bloque forcément son propre test. Les statiques signalées ont un voisinage
  dégagé à 60 m dans 1 à 3 directions sur 4 : elles ne sont pas en forêt. 11 déplacements décidés sur
  ce signal faussé ont été annulés. **Restreindre la sonde aux véhicules.**
- **La sonde est déterministe, elle** : 12 essais sur les mêmes points, 0/12 contre 12/12, comptes de
  candidats identiques. Le bruit ne vient jamais de là. C'est l'usage à grand rayon de dégagement qui
  est aléatoire (§9.3, point 4).
- **`getSimpleZones` rend `{course, x, y}` où `y` est l'est**, sans champ `z`. Calculer une distance
  sur le candidat brut donne des valeurs absurdes.
- **Les horodatages de `dcs.log` sont en UTC**, l'heure locale est UTC+2.
- **`dcs.log.old` peut contenir plusieurs runs.** Découper sur `loading mission` avant de compter :
  un total brut a déjà produit un « 18 batteries attendues » qui en valait 9.
- **Ne pas comparer deux nombres d'alertes** sans vérifier que le parc est le même, ni sans séparer
  groupes et statiques.
- **Et surtout : ne rien mesurer après le spawn.** Voir §9.5, qui invalide la moitié des chiffres
  de ce chapitre.

### 9.5 La sonde compte les véhicules — ce qui invalide la moitié des chiffres ci-dessus

Trouvé le 26/09 au soir, après deux jours de mesures bâties dessus.

`Disposition.getSimpleZones` — la seule API DCS qui connaisse les forêts, et donc le socle de toute
la métrique « unités dans les arbres » — ne répond pas à la question « suis-je sous un arbre ». Elle
répond à « y a-t-il de la place libre ici », et **un blindé occupe de la place**.

La preuve, mêmes points, même session, quelques secondes d'écart, la seule différence étant que le
groupe se tenait dessus ou non :

| groupe | avec ses véhicules | groupe détruit |
|---|---|---|
| `combatZone_Brocken` EWR, 3 véhicules | **3 / 3 bloquées** | **0 / 3** |
| `combatZone_Borkenberge_Hard` S-300, 14 véhicules | **12 / 14 bloquées** | **0 / 14** |

Quinze véhicules sur dix-sept signalés « dans les arbres » n'étaient gênés que par leurs propres
voisins. Une batterie SAM serrée ne peut pas passer ce test, où qu'on la mette.

**Conséquence :** les nombres `~81`, `76` et `66` de ce chapitre, et les `69` qui ont suivi, sont
en grande partie un décompte de groupes qui se bloquent eux-mêmes.

**Conséquence heureuse :** ça explique la « cécité de `Disposition` dans la pile d'appel de
`settleGroup` », qui a coûté une journée et qu'on n'a jamais expliquée. `settleGroup` sonde **avant
que les unités existent** — pas de véhicules, donc « dégagé » ; la mesure de contrôle sondait
**après** le spawn. Deux questions différentes, pas un singleton qui ment.

**La bonne façon de mesurer :** sonder là où aucun véhicule du groupe n'existe encore, c'est-à-dire
exactement là où `veafUnits` sonde déjà. Relevé ainsi le 26/09 au soir, après le ticket 11 et après
le déplacement de 11 groupes : **22 véhicules réellement sous les arbres à l'arrivée du spawn**, et
**4** une fois `settleGroup` passé — contre 22 et 17 avant. C'est consigné côté VMCT dans
`known-limitations.yaml` et dans la docstring de `isPointClearOfScenery`.

### 9.6 Règles de travail

- **C'est Claude qui lance `dcs-serve`**, pas David ; lui ne s'occupe que de DCS et du slot. Prendre
  la configuration de `VEAF-dcs-bridge`, **pas** celle de VMCT : les clés diffèrent et l'erreur se
  manifeste par un 401 peu parlant.
- **Vérifier le travail d'un agent avant de le relayer.** #1005 a été rendue « tout vert » alors
  qu'elle était inerte sur la mission réelle : sa CI passait un rayon non nul, la mission n'en passe
  jamais.

## 10. Points ouverts

1. **NASAMS à 6 km de Ramstein** : acceptable, ou le rapprocher en acceptant une lisière ?
2. **Outils de contrôle hors dépôt** (`.veaf-backups/outils-controle/` : générateur du README, mission de test, sondes). Proposition : les déplacer dans un dossier `tools/` versionné.
3. **Clé CheckWX en clair** dans le `configuration.json` de la v5 : à révoquer.
4. **Lot VMCT FIX-PLACEMENT-IGNORES-SCENERY** : tickets 01-03, 05-07, 09 et 10 livrés ; 10 mesuré
   inerte en jeu le 26/09 (§9.3) et repris par le **ticket 11**, en cours. Le ticket 04 (refuser un
   FARP dont l'escorte ne peut être placée) reste ouvert. À la livraison de 11 : rebuild, nouvelle
   sonde, et vérifier que les espacements n'ont pas bougé.
5. **La sonde et les statiques** (§9.4, premier point) : à corriger avant le prochain passage.
6. **Le Shilka aveugle**, en pause, aucun ticket ouvert. Sur 11 ZSU-23-4, 3 ne déclarent aucun
   capteur à DCS (`getSensors()` rend `nil`) ; 2 sont l'unique radar de leur site, qui n'apporte donc
   rien à la détection Skynet. Éliminés : le type (`getDesc` identique au caractère près), le pays,
   l'état de l'unité, le gabarit seul, le retard après spawn (stable à 190 s et à 576 s). **Ce n'est
   pas une régression** : 2 alertes par run avant comme après. Décision en attente : ouvrir un ticket
   VMCT pour ne pas le perdre, ou abandonner.
7. **`combatZone_Wittstock [r] SA15`** : 2 unités, aucune issue à 720 m — vérifié le 26/09 au soir
   en retirant toute marge, la forêt est réellement fermée. Le seul cas sans solution. Son voisin le
   S-300, longtemps rangé ici aussi, **en a une** : un balayage à la sonde lui a trouvé une clairière
   à 200 m là où `getSimpleZones` ne proposait rien à aucun rayon. Il a été déplacé, avec dix autres
   groupes.
8. **Les FARP** : 4 accessoires dans les bois à Baumholder et Göttingen, volontairement non traités.
   Ils partagent leur groupe avec l'hélisurface, et les déplacer bougerait le point d'atterrissage
   pour un gain cosmétique.
9. **Encore à vérifier en jeu** : statiques, navires, convois, FARP, imbrication des zones, engagement des CAP, portées des SAM.
