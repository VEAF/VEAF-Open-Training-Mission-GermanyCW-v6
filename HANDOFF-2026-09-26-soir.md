# Passation — 2026-09-26 au soir

Écrite en fin de session, à 97 % du quota hebdomadaire. **Supprime ce fichier une fois le ticket 11
livré et mesuré en jeu.**

---

## 1. Où en est le code, exactement

**Tout est committé, arbres propres, 49 suites Lua vertes.** Rien n'est poussé ni mergé.

### VMCT — `D:\dev\_VEAF\VEAF-Mission-Creation-Tools`

Branche **`fix/settle-verifies-its-candidate`**, commit `01633c0e`, partie de `develop` @ `ae8076f9`.
Elle contient le diagnostic et la vérification par unité :

| fichier | contenu |
|---|---|
| `.backlog/…/tickets/11-settle-verifies-the-candidate-it-trusts.md` | le ticket, à jour : ce qui est fait, ce qui reste (le pré-calcul) |
| `.backlog/FIX-PLACEMENT-IGNORES-SCENERY/PRD.md` | lot rouvert, section « pourquoi trois rounds » |
| `src/python/…/known-limitations.yaml` + `docs/agents/dcs-runtime-traps.md` | l'entrée DCS sur `getSimpleZones` |
| `CHANGELOG.md` | entrée sous `[Unreleased]`, qui dit que c'est une étape et pas le correctif |
| `src/scripts/veaf/veafUnits.lua` | `isPointClearOfScenery`, `SETTLE_DRAWS`, `SETTLE_UNIT_PROBE`, `SETTLE_MAX_CANDIDATES_VERIFIED`, vérification par unité |
| `test/lua/test_veafUnits.lua` | mock fidèle + 2 tests neufs, vérifiés rouges sans le correctif |

**Le report d'une seconde a été écrit puis retiré avant le commit** — il n'est nulle part dans
l'historique. Ne pas le réintroduire sans lire le §2.

### Mission — `D:\dev\_VEAF\VEAF-Open-Training-Mission-GermanyCW-v6`

- `main` @ `d061236` (journal + ce fichier), arbre propre, non poussé.
- **Piège** : les exes déployés sont en **6.25.0.1** et contiennent **aussi le report retiré**, car
  ils ont été construits avant le nettoyage. **Redéployer avant toute mesure** :

  ```
  cd D:/dev/_VEAF/VEAF-Mission-Creation-Tools
  PYTHONUTF8=1 poetry run veaf-build build --version 6.25.0.2
  PYTHONUTF8=1 poetry run veaf-build publish-local "D:/dev/_VEAF/VEAF-Open-Training-Mission-GermanyCW-v6"
  ```

- `bridge/bridge-GermanyCW-OT.miz` régénérée à 15:28, donc elle aussi avec le report. À refaire
  après le redéploiement (voir §4 pour le script cassé et son contournement).

---

## 2. Ce que la session a établi — ne pas refaire ces mesures

### Le lot 10 (PR #1005, livré en 6.25.0) est inerte

Mesuré en jeu : 19 alertes de groupe et 66 unités bloquées, contre 16-18 et ~81 avant. Le ticket 11
(vérification des candidats) l'est aussi : 20 alertes, 75 unités. La seule promesse tenue dans les
deux cas est la formation, qui reste intacte.

### La cause : Disposition est aveugle dans la pile d'appel de `settleGroup`

Des **points témoins** à coordonnées fixes, sans rapport avec le groupe placé, vérité 9 bloqués
sur 15 :

| sondés depuis | réponse |
|---|---|
| l'intérieur de `settleGroup` | **0 / 15** |
| une seconde plus tard | 9 / 15 |

Les unités atterrissent exactement aux coordonnées examinées : déplacement maximal **0,0 m** sur 15.

**Hypothèses réfutées, toutes mesurées — ne pas y revenir :**

- rafale d'appels : 12 passes d'affilée au calme donnent 9, 9, 9… identiques ;
- réchauffement : 5 passes consécutives *dans* `settleGroup` donnent toutes 0 ;
- création d'un groupe, même dans la même frame : aucun effet ;
- destruction d'unités : aucun effet ;
- les unités qui se gêneraient : détruire le groupe ne change pas le compte (9 avant, 9 après) —
  les alertes sont bien des arbres ;
- forme de la table passée (`{x,y,z}`, champs en plus, sans `y`, `y=0`) : aucune différence ;
- gros appel préalable, rafale de gros appels, `veaf.findSpawnPoint` réel : aucun effet ;
- exception avalée et traduite en « dégagé » : non, les 15 appels **réussissent** et renvoient
  des candidats.

**La cause reste inconnue.** C'est acté, ce n'est pas un aveu provisoire.

### Le report d'une seconde a été essayé, et abandonné

Il fonctionne côté mesure (t+1 s dit la vérité, 16 groupes sur 16, en pleine rafale des 25 zones),
mais il casse la chaîne décrite au §1. Ne pas le reprendre sans traiter d'abord le bloc post-spawn.

---

## 3. La suite : le pré-calcul, et il est déjà validé

**Idée de David :** sortir le check du flux de spawn. Sonder le terrain dans une phase à part, au
calme, et n'utiliser au spawn qu'un résultat déjà calculé.

**Mesuré le 2026-09-26** en rejouant la sélection complète (vérification par unité + 3 tirages
fusionnés) depuis une frame calme, sur les 16 groupes en alerte :

- **9 résolus**, translations de 131 à 470 m, **tous les gros S-300 compris** (11/14, 12/15 et 9/14
  unités bloquées) ;
- **7 non résolus**, et jamais parce que la vérification refuse : **0 candidat proposé** à chaque
  fois. Trois sont des convois (footprint 400 m), exemptés de toute façon ; restent 4 irréductibles,
  dont `combatZone_Wittstock [r] SA15` déjà connu comme sans issue.

La voie est donc validée. Ce qui reste à concevoir : **où placer la phase de pré-calcul**. Piste la
plus simple — au moment où une zone s'active, une passe qui demande les clairières autour de la
zone, puis les spawns qui piochent dedans sans jamais réinterroger Disposition.

**Réserve à lever avant d'écrire du code :** la disposition interne d'un groupe est tirée au hasard
*au moment du spawn*, donc on ne sait pas d'avance où chaque véhicule tombera. Il faut vérifier
qu'une clairière pré-calculée assez large permet quand même de translater le groupe correctement.
La mesure ci-dessus le suggère fortement (elle part du footprint réel), mais elle a été faite sur
des groupes déjà spawnés.

**À réécrire en conséquence :** le ticket 11, l'entrée `known-limitations` et l'entrée de changelog
décrivent tous la bonne cause racine mais la mauvaise réponse (ils parlent de vérifier les candidats
au spawn ; il faut parler de pré-calculer hors spawn).

---

## 4. Contexte opératoire

- **C'est Claude qui lance `dcs-serve`** (`cd D:/dev/_VEAF/VEAF-dcs-bridge && ./dist/dcs-serve.exe
  --config dcs-serve.yaml`), avec la config de `VEAF-dcs-bridge`, **pas** celle de VMCT — sinon 401.
  David charge la mission et entre dans un slot.
- **`make_test_mission.py` est cassé** : le build `LOCAL_TEST` sort en code 1 sur un avertissement
  informatif (fréquences UHF hors plage du TF-51D) et le `check=True` fait tout échouer. Contourner
  en déroulant les étapes à la main — le build lui-même réussit. Vient de 6.25.0, à corriger à part.
- Le rapport `presets-validation-report.md` a des accents cassés (`BÃ¼chel`) : encodage, hors sujet.
- **Vérifier que le `.miz` embarque bien le correctif** avant toute mesure : chercher les nouvelles
  constantes dans `l10n/DEFAULT/veaf-scripts.lua`. Le hash de version affiché par `capabilities` ne
  le dit pas — il a désigné le commit de #1004 pour une build qui contenait #1005.
- Sous Windows, lancer Python avec `PYTHONUTF8=1`. L'outil Bash n'a ni `jq` ni `rg`.
