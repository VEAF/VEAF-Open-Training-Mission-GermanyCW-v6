# Rapport de validation des fréquences radio

Fichier presets : `src/presets.yaml`  
Mission : `VEAF_OpenTraining_GermanyCW_ICAO_ETAR`

## ℹ️ Hors plage — retirées de la radio injectée (DCS les stockerait mais les ignorerait)

*2 types d'appareil concernés.*

### M-2000C
Groupes : `Arène - M-2000C - FOX1 - bleu`, `M-2000C Template`, `Arène - M-2000C - FOX1 - rouge`, `M-2000C Template Red`  
Plages valides : 225.0–400.0 MHz (AM/FM), 118.0–140.0 MHz (AM/FM), 225.0–400.0 MHz (AM/FM)

| Canal | Titre | Fréquence (MHz) | Collection | Radio |
|---------|-------|-----------------|------------|-------|
| 6 | Nordholz | 142.9 |  | radio_2 |

**Rien à faire :** les canaux à portée restent sur les radios de cet avion ; DCS aurait ignoré ceux-ci. Ne passez pas le type à `none` — cela retire tous ses presets.

### TF-51D
Groupes : `TF-51D Template`, `TF-51D Template Red`  
Plages valides : 38.0–156.0 MHz (AM/FM), 100.0–200.0 MHz (AM/FM)

| Canal | Titre | Fréquence (MHz) | Collection | Radio |
|---------|-------|-----------------|------------|-------|
| 1 | Overlord 1 (AWACS) | 265.0 |  | radio_2 |
| 2 | Magic 1 (AWACS) | 266.0 |  | radio_2 |
| 3 | Texaco 1 / perche / 51Y | 271.0 |  | radio_2 |
| 4 | Arco 1 / panier / 52Y | 272.0 |  | radio_2 |
| 5 | Texaco 2 / perche / 53Y | 273.0 |  | radio_2 |
| 6 | Arco 2 / panier / 54Y | 274.0 |  | radio_2 |
| 7 | Shell 1 / perche / 55Y | 275.0 |  | radio_2 |
| 8 | Archer | 360.0 |  | radio_2 |
| 9 | Arctic | 360.1 |  | radio_2 |
| 10 | Ninja | 360.2 |  | radio_2 |
| 11 | Pinder | 360.3 |  | radio_2 |
| 12 | Bengal | 360.4 |  | radio_2 |
| 13 | Blade | 360.5 |  | radio_2 |
| 1 | AWACS Rouge (A-50) | 260.0 |  | radio_2 |
| 2 | Tanker Rouge (Il-78M) | 261.0 |  | radio_2 |
| 3 | Rouge-1 | 380.0 |  | radio_2 |
| 4 | Rouge-2 | 380.1 |  | radio_2 |
| 5 | Rouge-3 | 380.2 |  | radio_2 |
| 6 | Rouge-4 | 380.3 |  | radio_2 |

**Rien à faire :** les canaux à portée restent sur les radios de cet avion ; DCS aurait ignoré ceux-ci. Ne passez pas le type à `none` — cela retire tous ses presets.

## ⚠️ AWACS et ravitailleurs qu'aucun preset n'atteint — ajoutez leur canal dans src/presets.yaml

| Groupe | Tâche | Fréquence (MHz) | Coalition |
|--------|------|-----------------|-----------|
| `CVN-74 Stennis S3B-Tanker` | Refueling | 290.9 | blue |
| `Darkstar 1` | AWACS | 280.0 | blue |
| `AWACS Arène Rouge` | AWACS | 281.0 | red |
