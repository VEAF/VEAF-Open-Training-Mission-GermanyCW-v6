# Open Training GermanyCW v6 — résumé du chantier (24-28/09/2026)

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
| Modules | CTLD, CSAR, AIEN, STTS, Skynet (réseau de spotters, vue F10 désactivée) |
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
2. ~~Outils de contrôle hors dépôt~~ : versionnés dans `tools/` le 29/09 (§13).
3. **Clé CheckWX en clair** dans le `configuration.json` de la v5 : à révoquer.
4. **Lot VMCT FIX-PLACEMENT-IGNORES-SCENERY** : tickets 01-03, 05-07, 09 et 10 livrés ; 10 mesuré
   inerte en jeu le 26/09 (§9.3) et repris par le **ticket 11**, en cours. Le ticket 04 (refuser un
   FARP dont l'escorte ne peut être placée) reste ouvert. À la livraison de 11 : rebuild, nouvelle
   sonde, et vérifier que les espacements n'ont pas bougé.
5. ~~La sonde et les statiques~~ : corrigée le 29/09 (§13) — véhicules seuls, positions de l'éditeur, avant tout spawn.
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
9. ~~Encore à vérifier en jeu~~ : fait le 29/09 (§13). Les portées des SAM sont retirées de la liste : le briefing n'en chiffre aucune, il n'y a rien à comparer.
10. **Reste à vérifier en jeu** : les balises MH01-03 et SOS relevables au radiogoniomètre (il faut un
    hélicoptère sur la zone de sauvetage). Le reste de la liste du 28/09 est vérifié (§12).
11. **Le preset VHF de l'OH-58D** n'a pas été lu dans le cockpit : le module a fait tomber DCS deux fois au
    chargement du cockpit (§13). La correction repose sur le code.

## 11. Finalisation selon le prompt du 28/09

Le prompt `new-open-training-mission` a gagné le 28/09 les règles tirées de l'Open Training Caucase v5
(commit VMCT `4fdb8ab6`). Appliquées à la mission :

- **Mesuré conforme sans rien changer** : aucune défense permanente à portée d'une base adverse avec slots
  (la plus proche, SA-11 d'Allstedt → Fulda, 84 nm ; NASAMS de Fulda → Allstedt, 85 nm), `requiredModules`
  vide, aucun mot de passe, chaque nom d'`ASSETS` désigne un groupe, `troopPickupAtFARP` ouvert.
- **Vue F10 des guetteurs** : `spotter_view: "off"` (ni dessin ni interrupteur radio).
- **FARP** : un statique `FARP Ammo Dump Coating` à 120 m de chacun. Celui que pose `-farp` apparaît en cours
  de partie, alors que CTLD ne cherche ses points logistiques qu'une fois, à son démarrage.
- **QRA** : `react_on_helicopters: false` écrit, vrai tirage à chaque niveau (les groupes A et B étaient des
  copies du même avion, et les niveaux 3 et 6 faisaient décoller tout ce qu'ils listaient). Délai de 60 s et
  hélicoptères ignorés dits au briefing.
- **Combat entre joueurs** : règle écrite au briefing ; sanctuaire bleu sur les arrières ouest, trois
  sanctuaires rouges de 8 nm autour de Laage, Holzdorf et Allstedt (aucune zone de combat dedans : Torgau, la
  plus proche, est à 15,6 nm de Holzdorf) ; arène au-dessus du Grand Belt, reprise de l'« Air Quake » v5
  (14 patrouilles de 4 slots en vol, emports v5, un AWACS par camp), plus 9 patrouilles rouges d'avions de l'Est
  (MiG-29S, J-11A et JF-17 en Fox 3 ; MiG-29A, Su-27, Su-33, J-11A, MiG-21bis et Mirage F1EE en Fox 1), emports du
  catalogue de démo VMCT et des modèles de slots rouges. Limites tracées sur la carte F10.
- **Porte-avions** : CSG-74 Stennis de la v5 en mer du Nord (tâches ATC, Pedro, S-3B, 6 slots de pont, module
  `CARRIER`), avec son entrepôt ; les slots dynamiques du pont limités aux appareils embarquables.
- **Drones laser** : un MQ-9 sur Baumholder (1688) et un sur Wahner Heide (1687), JTAC par `ASSETS`. Pas de drone sur
  Borkenberge : le JTAC ne marque qu'à 10 km, et tous les SAM de la zone portent plus loin (retiré sur décision de David).
- **Zone hélicoptère hors combat** : reprise de la « Mountain Hike » v5 dans le Hunsrück, trois balises FM et un
  SOS qui n'émettent que zone active ; sons v5 dans `src/mission/l10n/DEFAULT/`.
- **README** : reste le briefing, en français, généré par `gather.py` / `gen_readme.py` ; nouvelles sections
  porte-avions, drones, zone de sauvetage, combat entre joueurs et arène ; la carte montre sanctuaires et porte-avions,
  l'arène (hors cadre) par une flèche.
- **Sites variables** : `#spawngroup` / `#spawncount` sur 13 zones, dont les 5 d'entraînement qui ont plus d'un
  élément ; trois porteurs `#command` ajoutés à Borkenberge pour tirer la défense au sort.

## 12. Test en jeu du 28/09 au soir

Mission de test (game master, pont dcs-bridge), mesures par le pont et `dcs.log` :

- **Conforme** : aucune erreur de script ; sanctuaires construits (5 / 6 / 6 / 6 sommets, sommets
  détruits au démarrage) ; CARRIER OPS lit TACAN 10X, ICLS 10, Link 4 et tour du Stennis ; les FARP
  `-farp` s'enregistrent eux-mêmes comme points logistiques CTLD (les deux dépôts posés dans
  l'éditeur sont redondants) ; tirages justes (Baumholder 3 / 5, Borkenberge SA-6 + SA-15,
  Parchim 5 / 7) ; Reaper 1 désigne au laser le ZU-23 de Baumholder moyen ; slots de l'arène et du
  pont, dessins F10 vus par David.
- **Quatre objectifs n'existaient pas depuis le 24/09** : le poste de commandement de Wünsdorf et
  les trois `.Ammunition depot` (Torgau ×2, Wittenberg). DCS refuse un statique de ces types sans
  `shape_name` (« unknown static shape_name »). Corrigé avec les noms de la table de VEAF
  (`ComCenter`, `SkladC`).
- **Les drones volent à 3 000 m sol**, pas au FL150 écrit : CTLD les ré-oriente à
  `JTAC_droneAltitude` dès qu'il les prend comme JTAC. Briefing et README corrigés. Le JTAC ne
  désigne que des véhicules : rien aux niveaux faciles, faits de statiques.
- **Chaque zone s'initialise deux fois** (lignes de log et éléments doublés), sans double spawn.
  Signalé à VMCT.

### 12.1 Sur private1, le soir même

`dcs.log` du serveur relu entièrement (19:24 → 20:31, 10 567 lignes, plusieurs joueurs) :

- **Reaper 2 abattu** à 19:53 par un S-60 de 57 mm de Wahner Heide difficile (8 coups). À 3 000 m sol
  le drone est à portée de l'AAA lourde du niveau difficile. Décision de David : le dire au briefing,
  le menu ASSETS le relance.
- **CTLD attend `extract1`…`extract25` et `logistic1`…`logistic10`**, les listes d'exemple que
  `ctld-config.yaml` reprend des valeurs par défaut de CTLD ; aucun de ces noms n'existe : 35
  avertissements au démarrage. Listes vidées.
- **Le sanctuaire plante** sur une arme sans cible (CBU-105, AGM-88C : 25 fois) ou déjà disparue (un
  obus de 57 mm : 1 fois). Sans effet en jeu ; ticket VMCT.
- **Aucune ville pour GermanyCW** dans `veafNamedPoints`. Ticket VMCT.

## 13. Plan de fréquences, outils et test en jeu du 29/09

- **Le « Nörvenich pas juste » du 28/09 était un défaut d'encodage, pas de fréquence.** Les 1 931 canaux
  injectés, les 12 paires du briefing DCS et les 65 cellules radio du README donnent tous la fréquence du
  plan (`tools/check_frequencies.py`, vérifié avec un plan faussé pour témoin). Mais VMCT lisait
  `presets.yaml` en cp1252 (`open()` sans `encoding`) : 127 noms de canaux injectés et tous les kneeboards
  affichaient « NÃ¶rvenich », « BÃ¼chel ». Corrigé côté VMCT (branche `fix/presets-yaml-utf8`), avec un
  test qui refuse désormais toute ouverture de fichier texte sans encodage.
- **Le kneeboard du Mi-24P se trompait d'un cran** : il imprimait la case DCS (« 13 Nörvenich ») alors que
  le rotacteur de la R-863 lit **12** — lu par David dans le cockpit. Le README avait raison. Même défaut
  sur l'OH-58D (case « M » en tête).
- **L'OH-58D décalait toute sa VHF d'un cran** : sa case « M » est alimentée par l'entrée n°20, la liste
  VHF de la mission n'en a que 16, VMCT abandonnait la case et Nörvenich passait du preset 5 au 4. Corrigé
  dans VMCT (la case prend la dernière entrée), trouvé dans le code ; la lecture dans le cockpit n'a pas pu
  se faire (voir §10, point 11).
- **Le convoi de Ludwigslust était posé sur de l'eau pour DCS** (surface 3 sous les 9 véhicules, et sur
  240 m d'est en ouest au relevé du 29/09 ; le §8 y voyait un pont, rien ne le prouve ni ne l'exclut) ; VEAF le
  replaçait au hasard (« declared position … is on invalid terrain »). Reposé sur la route, 350 m au
  nord-est, espacé de 19 m ; VEAF valide maintenant sa position.
- **Mesuré conforme** par `tools/test_en_jeu.py` : imbrication des niveaux (chaque niveau fait apparaître
  plus de groupes que celui qu'il inclut), 32 statiques à moins d'1 m de leur place et tirages respectés,
  navires à flot, convois qui roulent, les 5 CAP qui tirent sur une cible envoyée devant elles.
- **La sonde des bois refaite** (`tools/probe_scenery.py`) selon §9.4-9.5 : positions de l'éditeur, véhicules
  seuls, au démarrage, un point couvert par une unité vivante n'étant pas jugé. 18 alertes, toutes connues
  (accessoires de FARP, porteurs `#command`, sommets de sanctuaire, SA-15 de Wittstock, zone de sauvetage).
- **Outils versionnés** dans `tools/` (chemins relatifs, `VMCT_PY` pour pointer un export de develop) ;
  voir `tools/README.md`.
- **Pièges de mesure de la journée**, tous dans mes détecteurs : un groupe tiré par `#command` porte le nom
  du niveau qui l'a lancé, pas du sien ; les groupes d'une zone sont renommés au spawn
  (`<zone> [r] <nom>#<id>`) ; `world.searchObjects` teste l'encombrement, un Il-76 déborde sur le point
  voisin ; une statique posée détruite n'est pas rendue par `getStaticObjects` ; VEAF enregistre chaque CAP
  en variantes `…/good/2`. Activer d'un coup tous les niveaux d'une famille fait tirer chaque niveau.
- **Le refus « secured command posted without a group »** vu par David venait de private1 (trois clics
  refusés le 29/09 à 11:19, 11:20 et 11:21 UTC, mission du 28/09). Cause, lue dans le code VMCT :
  `RadioMenuBuilder:_placeCommandOnMenu` pose une commande sécurisée déclarée `USAGE_ForAll` sans groupe
  (`_addDcsCommand(nil, …)`), sans l'avertissement que l'autre chemin écrit, et `_proxyMethod` refuse
  alors tout clic, sécurité active. Sont déclarées ainsi : activer / désactiver une zone et une mission
  CAP, « dispose » d'un asset, le brouillard, l'élingage CTLD, « skip » CAS et transport, le nettoyage
  des convois. Le log ne dit pas laquelle a été cliquée. Défaut VMCT, signalé à David, pas corrigé ici.


## 14. Cartes du briefing DCS, 29/09

- **La carte apparaissait deux fois** dans le briefing. Cause, lue dans `MissionEditor/modules/me_autobriefing.lua`
  de DCS : le camp du joueur n'est connu que si une unité a le niveau `Player` ; sinon (slot `Client`, dont
  celui de la mission de test, slot dynamique, spectateur) DCS affiche la liste rouge puis la liste bleue, et
  l'image était dans les deux. Le briefing en vol et en multijoueur passe par le moteur
  (`DCS.getPlayerBriefing`, `Scripts/UI/BriefingDialog.lua`), dont on ne voit pas la règle : ce qu'y voit un
  pilote rouge reste à confirmer. Les images sont
  maintenant listées côté bleu et neutre seulement ; la liste rouge est vide. Les seuls slots rouges classiques
  sont ceux de l'arène : c'est là, et seulement si DCS reconnaît le camp, qu'un pilote risque de n'avoir aucune
  carte.
- **Illisible parce que trop petite** : le panneau ajuste l'image à sa taille (la molette grossit, personne ne
  le sait). `tools/gen_map.py` dessine en plus 9 zooms titrés (liste `ZOOMS`, chacun nommé par les objets
  qu'il doit cadrer), à partir de tuiles OpenStreetMap du niveau le plus proche de leur résolution, avec les
  noms des zones de combat, la zone de sauvetage, le cercle de l'arène. Le briefing montre la carte générale
  puis les zooms. Le `.miz` passe de 7,1 à 11,2 Mo.
- **Au passage** : la zone 4 (Brocken) était cachée sous le bullseye, posé au même point ; le bullseye est
  maintenant un anneau autour d'elle. Les tirets des petits cercles (sanctuaires rouges) redémarraient à chaque
  segment et se dessinaient en trait plein.
- **Le README les reprend** : la carte générale en tête, chaque zoom dans la section qu'il illustre (bases, entraînement,
  zones de combat, arène), deux par ligne, cliquables.
- `gen_map.py` écrit lui-même `mapResource` et les `pictureFileName*` de la mission : la liste suit ce qui est
  dessiné, un zoom retiré ne reste pas dans le `.miz`.

## 15. Cibles des niveaux faciles : de statiques à groupes, 29/09

- **Constat** : au vol du 28/09 au soir (Wahner Heide difficile, qui inclut le moyen et le facile), des
  véhicules étaient froids au pod de l'A-10, d'autres chauds. Les groupes des niveaux moyen et difficile
  étaient chauds ; les froids étaient les cibles du niveau facile, des statiques. Un statique n'a pas de
  moteur, aucun script ne le réchauffe (ticket VMCT `FIX-COMBATZONE-DEAD-UNIT-HAS-NO-GROUP` n°02).
- **Fait** : `tools/statics_to_groups.py` a changé les 12 cibles faciles (Wahner Heide 7, Baumholder 5)
  en groupes d'un véhicule : même type, même place, même nom d'unité (donc même tirage `#spawngroup` /
  `#spawncount`), `coldAtStart = false`, tir interdit et pas de dispersion sous le feu, pour rester les
  cibles inertes que promet le briefing. Comparaison de la table avant/après : rien d'autre ne change.
- **Effet attendu** : le drone laser, qui ne désigne que des véhicules (§12), désigne aussi ces cibles.
- **L'option « dispersion sous le feu »** (`name = 8`) prend un délai en secondes (`me_action_db.lua` de
  DCS, 600 par défaut) : décochée, l'éditeur l'écrit sans valeur, forme reprise ici (une valeur 0 aurait
  voulu dire « se disperser tout de suite »).
- **À vérifier en jeu** : cibles chaudes au pod, immobiles et muettes sous le feu, désignées par le Reaper ;
  et leurs 12 places, que `probe_scenery.py` n'a testées que pour l'eau tant qu'elles étaient statiques
  (§9.4) : un véhicule posé dans les bois est replacé au hasard par VEAF, comme le convoi de Ludwigslust.

## 16. Outils reconstruits depuis VMCT develop `dd60e7a5`, 29/09

- Apporte #1028 (une commande F10 sécurisée « pour tous » est posée dans le menu de chaque groupe :
  le refus « secured command posted without a group » vu sur private1, §13) et #1030 (tout véhicule
  créé par script part avec `coldAtStart = false` ; le panneau d'information d'une zone compte ses statiques).
- Construits dans un worktree détaché, avec son propre environnement Poetry (`veaf-build build`, puis
  `publish-local`). Outils précédents dans `.veaf-backups/outils-e33ee057/`.
- `.miz` mesuré : aucun identifiant ni nom en double, aucune anomalie de structure, slots sur les 12 bases,
  sécurité active, `check_frequencies.py` conforme ; les scripts embarqués sont ceux de `dd60e7a5`.
- À vérifier en jeu, pour le ticket VMCT n°02 : les véhicules d'une zone qu'on vient d'activer sont
  chauds au pod.
