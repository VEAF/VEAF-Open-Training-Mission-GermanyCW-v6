# Rapport de validation des fréquences radio

Généré le : 2026-10-01  
Fichier presets : `D:\dev\_VEAF\VEAF-Open-Training-Mission-GermanyCW-v6\src\presets.yaml`  
Mission : `D:\dev\_VEAF\VEAF-Open-Training-Mission-GermanyCW-v6\VEAF_OpenTraining_GermanyCW_ICAO_ETAR_20261001.miz`

## ℹ️ Hors plage — retirées de la radio injectée (DCS les stockerait mais les ignorerait)

*2 types d'appareil concernés.*

### M-2000C
Groupes : `Arène - M-2000C - FOX1 - bleu`, `M-2000C Template`, `Arène - M-2000C - FOX1 - rouge`, `M-2000C Template Red`  
Plages valides : 225.0–400.0 MHz (AM/FM), 118.0–140.0 MHz (AM/FM), 225.0–400.0 MHz (AM/FM)

| Canal | Titre | Fréquence (MHz) | Collection | Radio |
|---------|-------|-----------------|------------|-------|
| 7 | Nordholz | 142.9 |  | radio_2 |

**Pour masquer :** ajouter dans `presets.yaml` :
```yaml
presets_assignments:
  blue:
    plane:
      M-2000C: none
```

### TF-51D
Groupes : `TF-51D Template`, `TF-51D Template Red`  
Plages valides : 38.0–156.0 MHz (AM/FM), 100.0–200.0 MHz (AM/FM)

| Canal | Titre | Fréquence (MHz) | Collection | Radio |
|---------|-------|-----------------|------------|-------|
| 1 | Guard | 243.0 |  | radio_2 |
| 2 | Overlord 1 (AWACS) | 265.0 |  | radio_2 |
| 3 | Magic 1 (AWACS) | 266.0 |  | radio_2 |
| 4 | Texaco 1 / perche / 51Y | 271.0 |  | radio_2 |
| 5 | Arco 1 / panier / 52Y | 272.0 |  | radio_2 |
| 6 | Texaco 2 / perche / 53Y | 273.0 |  | radio_2 |
| 7 | Arco 2 / panier / 54Y | 274.0 |  | radio_2 |
| 8 | Shell 1 / perche / 55Y | 275.0 |  | radio_2 |
| 9 | Ramstein / 81X | 251.95 |  | radio_2 |
| 10 | Spangdahlem / 32X | 251.8 |  | radio_2 |
| 11 | Büchel / 118X | 252.9 |  | radio_2 |
| 12 | Nörvenich / 77X | 365.0 |  | radio_2 |
| 13 | Wiesbaden / 88X | 252.25 |  | radio_2 |
| 14 | Nordholz | 315.7 |  | radio_2 |
| 15 | Wunstorf / 116X | 253.95 |  | radio_2 |
| 16 | Fassberg / 95X | 251.0 |  | radio_2 |
| 17 | Fulda | 252.0 |  | radio_2 |
| 18 | Archer | 360.0 |  | radio_2 |
| 19 | Arctic | 360.1 |  | radio_2 |
| 20 | Ninja | 360.2 |  | radio_2 |
| 2 | AWACS Rouge (A-50) | 260.0 |  | radio_2 |
| 3 | Tanker Rouge (Il-78M) | 261.0 |  | radio_2 |
| 4 | Laage | 252.7 |  | radio_2 |
| 5 | Holzdorf | 250.95 |  | radio_2 |
| 6 | Allstedt | 251.5 |  | radio_2 |
| 7 | Rouge-1 | 380.0 |  | radio_2 |
| 8 | Rouge-2 | 380.1 |  | radio_2 |
| 9 | Rouge-3 | 380.2 |  | radio_2 |
| 10 | Rouge-4 | 380.3 |  | radio_2 |

**Pour masquer :** ajouter dans `presets.yaml` :
```yaml
presets_assignments:
  blue:
    plane:
      TF-51D: none
```
