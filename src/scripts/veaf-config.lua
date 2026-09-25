---------------------------------------------------------------------------------------------------------------------------------------------
-- Généré par veaf-tools build depuis mission.yaml
-- Ne pas éditer manuellement.
-- Relancez 'veaf-tools build' ou 'veaf-tools generate-config' pour régénérer.
---------------------------------------------------------------------------------------------------------------------------------------------

-- ── Mission identity ─────────────────────────────────────────────────────────
veaf.config.MISSION_NAME = "VEAF_OpenTraining_GermanyCW_ICAO_ETAR"
veaf.config.era = veaf.ERA.MODERN
veaf.silenceAtcOnAllAirbases()
veaf.HideNamesFromSpawnedGroups = false

veaf.config.language = "fr"

-- ── Security ─────────────────────────────────────────────────────────────────
veaf.SecurityDisabled = true

-- ── Global log level ─────────────────────────────────────────────────────────
veaf.ForcedLogLevel = "debug"

-- ── CTLD 2 ───────────────────────────────────────────────────────────────────
-- Configuration lives in ctld-config.yaml (edit it with ctld-tools); this only starts it.
if ctld then
    veaf.ctld_initialize()
end

-- ── Module configuration + initialization ────────────────────────────────────

-- ── Core ──

if veafSecurity then
    veafSecurity.initialize()
end

if veafRadio then
    veafRadio.initialize(true)
end

if veafShortcuts then
    veafShortcuts.initialize()
end

if veafNamedPoints then
    veafNamedPoints.initialize({})
end

if veafSpawn then
    veafSpawn.initialize()
end

-- ── Combat ──

veaf.setConfig("CARRIER", "enable", false)

if veafCasMission then
    veafCasMission.initialize()
end

if veafTransportMission then
    veafTransportMission.initialize()
end

if veafCombatMission then
    veafCombatMission.initialize()
    veafCombatMission.addCapMission("CAP MiG-29S - Stendal - FL200", "CAP MiG-29S - Stendal - FL200", "Paire de MiG-29S armés Fox 3 : combat au-delà de la portée visuelle, puis dogfight. Hippodrome au FL200 centré sur BULLSEYE 051/64, à 31 nm du front au plus près.", false, true)
    veafCombatMission.addCapMission("CAP Su-27 - Brandenburg - FL280", "CAP Su-27 - Brandenburg - FL280", "Paire de Su-27 armés Fox 1 (missiles à guidage radar semi-actif). Hippodrome au FL280 centré sur BULLSEYE 071/82, à 59 nm du front au plus près.", false, true)
    veafCombatMission.addCapMission("CAP MiG-31 - Neuruppin - FL400", "CAP MiG-31 - Neuruppin - FL400", "Paire de MiG-31 : intercepteur haut et rapide. Hippodrome au FL400 centré sur BULLSEYE 060/106, à 73 nm du front au plus près.", false, true)
    veafCombatMission.addCapMission("Bombardier Tu-22M3 - Rostock - FL250", "Bombardier Tu-22M3 - Rostock - FL250", "Deux Tu-22M3 en attente : cible de bombardier à intercepter. Hippodrome au FL250 centré sur BULLSEYE 039/140, à 52 nm du front au plus près.", false, true)
    veafCombatMission.addCapMission("CAP F-16C - Hanovre - FL250", "CAP F-16C - Hanovre - FL250", "Paire de F-16C armés Fox 3 : opposition pour les joueurs rouges. Hippodrome au FL250 centré sur BULLSEYE 332/45, à 34 nm du front au plus près.", false, true)
    veafCombatMission.addCapMission("CAP F-15C - Kassel - FL300", "CAP F-15C - Kassel - FL300", "Paire de F-15C armés Fox 3 : opposition pour les joueurs rouges. Hippodrome au FL300 centré sur BULLSEYE 246/56, à 24 nm du front au plus près.", false, true)
end

if veafCombatZone then
    veafCombatZone.RadioMenuName = "Zones de combat"
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Baumholder_Easy")
        :setFriendlyName("Baumholder - facile")
        :setRadioGroupName("Entraînement hélicoptères")
        :setBriefing([[Entraînement cibles pour hélicoptères à Baumholder (BULLSEYE 233/180), niveau facile. Cibles statiques inertes (blindés et camions), aucune défense. Ravitailleur le plus proche : Shell 1 (TACAN 55Y, 255.0) à 16 nm. Un seul niveau de cette famille à la fois.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Baumholder_Medium")
        :setFriendlyName("Baumholder - moyen")
        :setRadioGroupName("Entraînement hélicoptères")
        :setBriefing([[Entraînement cibles pour hélicoptères à Baumholder (BULLSEYE 233/180), niveau moyen. Ajoute de l'AAA légère (ZU-23 et Shilka), en plus du niveau facile. Ravitailleur le plus proche : Shell 1 (TACAN 55Y, 255.0) à 16 nm. Un seul niveau de cette famille à la fois.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Baumholder_Hard")
        :setFriendlyName("Baumholder - difficile")
        :setRadioGroupName("Entraînement hélicoptères")
        :setBriefing([[Entraînement cibles pour hélicoptères à Baumholder (BULLSEYE 233/180), niveau difficile. Ajoute une défense courte portée (batterie VEAF de niveau 3 : missiles IR et AAA) et des MANPADS, en plus du niveau moyen. Ravitailleur le plus proche : Shell 1 (TACAN 55Y, 255.0) à 16 nm. Un seul niveau de cette famille à la fois.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_WahnerHeide_Easy")
        :setFriendlyName("Wahner Heide - facile")
        :setRadioGroupName("Entraînement attaque")
        :setBriefing([[Entraînement cibles pour avions d'attaque à Wahner Heide (BULLSEYE 257/144), niveau facile. Cibles statiques inertes (chars, VCI, camions). Ravitailleur le plus proche : Arco 2 (TACAN 54Y, 254.0) à 57 nm. Un seul niveau de cette famille à la fois.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_WahnerHeide_Medium")
        :setFriendlyName("Wahner Heide - moyen")
        :setRadioGroupName("Entraînement attaque")
        :setBriefing([[Entraînement cibles pour avions d'attaque à Wahner Heide (BULLSEYE 257/144), niveau moyen. Ajoute un peloton blindé actif et de l'AAA légère, en plus du niveau facile. Ravitailleur le plus proche : Arco 2 (TACAN 54Y, 254.0) à 57 nm. Un seul niveau de cette famille à la fois.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_WahnerHeide_Hard")
        :setFriendlyName("Wahner Heide - difficile")
        :setRadioGroupName("Entraînement attaque")
        :setBriefing([[Entraînement cibles pour avions d'attaque à Wahner Heide (BULLSEYE 257/144), niveau difficile. Ajoute un groupe blindé VEAF avec sa défense et une batterie courte portée (niveau 3), en plus du niveau moyen. Ravitailleur le plus proche : Arco 2 (TACAN 54Y, 254.0) à 57 nm. Un seul niveau de cette famille à la fois.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Borkenberge_Easy")
        :setFriendlyName("Borkenberge - facile")
        :setRadioGroupName("Entraînement SEAD")
        :setBriefing([[Entraînement site SEAD/DEAD à Borkenberge (BULLSEYE 279/125), niveau facile. Une batterie SA-6 seule (moyenne portée). Ravitailleur le plus proche : Arco 2 (TACAN 54Y, 254.0) à 79 nm. Un seul niveau de cette famille à la fois.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Borkenberge_Medium")
        :setFriendlyName("Borkenberge - moyen")
        :setRadioGroupName("Entraînement SEAD")
        :setBriefing([[Entraînement site SEAD/DEAD à Borkenberge (BULLSEYE 279/125), niveau moyen. Ajoute un SA-15 (courte portée), en plus du niveau facile. Ravitailleur le plus proche : Arco 2 (TACAN 54Y, 254.0) à 79 nm. Un seul niveau de cette famille à la fois.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Borkenberge_Hard")
        :setFriendlyName("Borkenberge - difficile")
        :setRadioGroupName("Entraînement SEAD")
        :setBriefing([[Entraînement site SEAD/DEAD à Borkenberge (BULLSEYE 279/125), niveau difficile. Ajoute un SA-10 (longue portée), un SA-11 et un radar d'alerte 55G6, en réseau Skynet, en plus du niveau moyen. Ravitailleur le plus proche : Arco 2 (TACAN 54Y, 254.0) à 79 nm. Un seul niveau de cette famille à la fois.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Luebtheen")
        :setFriendlyName("Lübtheen")
        :setRadioGroupName("Front")
        :setBriefing([[Lübtheen (BULLSEYE 021/92) : un bataillon blindé en position de départ sur le terrain d'exercice de Lübtheen. À détruire : les chars, les VCI et la batterie d'artillerie. Défense : batterie VEAF de niveau 4 (SA-8 ou Tor, missiles IR, AAA) et un SA-19 Tunguska. Hors couverture QRA rouge. Ravitailleurs les plus proches : Texaco 1 (perche, TACAN 51Y, 251.0) à 66 nm, Arco 1 (panier, TACAN 52Y, 252.0) à 77 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Letzlingen")
        :setFriendlyName("Letzlingen (Altmark)")
        :setRadioGroupName("Front")
        :setBriefing([[Letzlingen (Altmark) (BULLSEYE 051/53) : une brigade mécanisée sur le terrain d'exercice de l'Altmark, face au front. À détruire : les blindés et les véhicules de commandement. Défense : SA-15 Tor et SA-19 Tunguska, plus la défense propre du groupe blindé. Hors couverture QRA rouge. Ravitailleurs les plus proches : Texaco 1 (perche, TACAN 51Y, 251.0) à 81 nm, Arco 1 (panier, TACAN 52Y, 252.0) à 92 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Ohrdruf")
        :setFriendlyName("Ohrdruf")
        :setRadioGroupName("Front")
        :setBriefing([[Ohrdruf (BULLSEYE 184/59) : des positions d'artillerie et de lance-roquettes sur le terrain d'Ohrdruf. À détruire : les lance-roquettes Smerch, les obusiers Msta et leur ravitaillement. Défense : batterie VEAF de niveau 4 (SA-8 ou Tor, missiles IR, AAA). Hors couverture QRA rouge. Ravitailleurs les plus proches : Texaco 2 (perche, TACAN 53Y, 253.0) à 70 nm, Arco 2 (panier, TACAN 54Y, 254.0) à 82 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Brocken")
        :setFriendlyName("Brocken")
        :setRadioGroupName("SEAD")
        :setBriefing([[Brocken (sur le BULLSEYE) : le site radar du Brocken, au sommet du Harz, avec une batterie SA-11. À détruire : le radar d'alerte 55G6 et la batterie SA-11. Défense : SA-11 Buk et MANPADS SA-18, en réseau Skynet. Hors couverture QRA rouge. Ravitailleurs les plus proches : Texaco 1 (perche, TACAN 51Y, 251.0) à 72 nm, Arco 1 (panier, TACAN 52Y, 252.0) à 79 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Wittstock")
        :setFriendlyName("Kyritz-Ruppiner Heide")
        :setRadioGroupName("SEAD")
        :setBriefing([[Kyritz-Ruppiner Heide (BULLSEYE 052/105) : une batterie SA-10 isolée sur l'ancien champ de tir de la Kyritz-Ruppiner Heide, au sud de Wittstock. À détruire : la batterie SA-10 (radars et lanceurs). Défense : SA-10 et un SA-15 Tor en défense rapprochée, en réseau Skynet. Hors couverture QRA rouge. Ravitailleurs les plus proches : Texaco 1 (perche, TACAN 51Y, 251.0) à 117 nm, Arco 1 (panier, TACAN 52Y, 252.0) à 128 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_ConvoiA2")
        :setFriendlyName("Convoi A2")
        :setRadioGroupName("Convois")
        :setBriefing([[Convoi A2 (BULLSEYE 070/81) : un convoi logistique qui roule vers l'ouest sur l'axe Brandenburg - Genthin - Burg (A2 / B1), vers Magdeburg. À détruire : le convoi (camions, citernes, escorte). Défense : sa propre défense : un Shilka et un SA-13 roulent avec lui. Sous la couverture de la QRA Berlin. Ravitailleurs les plus proches : Texaco 1 (perche, TACAN 51Y, 251.0) à 116 nm, Arco 1 (panier, TACAN 52Y, 252.0) à 127 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_ConvoiA9")
        :setFriendlyName("Convoi A9")
        :setRadioGroupName("Convois")
        :setBriefing([[Convoi A9 (BULLSEYE 119/64) : un convoi de ravitaillement qui remonte l'A9 du Schkeuditzer Kreuz vers Bitterfeld et Dessau. À détruire : le convoi (camions et escorte). Défense : sa propre défense : un SA-19 Tunguska roule avec lui. Sous la couverture de la QRA Leipzig. Ravitailleurs les plus proches : Texaco 1 (perche, TACAN 51Y, 251.0) à 130 nm, Arco 1 (panier, TACAN 52Y, 252.0) à 139 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_ConvoiA24")
        :setFriendlyName("Convoi Ludwigslust")
        :setRadioGroupName("Convois")
        :setBriefing([[Convoi Ludwigslust (BULLSEYE 028/103) : une colonne blindée de renfort qui roule de Neustadt-Glewe vers Ludwigslust puis Hagenow, vers le front. À détruire : les chars et VCI de la colonne. Défense : sa propre défense : un SA-13 roule avec elle. Hors couverture QRA rouge. Ravitailleurs les plus proches : Texaco 1 (perche, TACAN 51Y, 251.0) à 81 nm, Arco 1 (panier, TACAN 52Y, 252.0) à 92 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Wuensdorf")
        :setFriendlyName("Wünsdorf")
        :setRadioGroupName("Frappe profonde")
        :setBriefing([[Wünsdorf (BULLSEYE 085/109) : l'état-major de théâtre installé dans les bunkers de Wünsdorf. À détruire : le poste de commandement, les bunkers et la tour de transmissions. Défense : SA-22 Pantsir et SA-15 Tor. Sous la couverture de la QRA Berlin. Ravitailleurs les plus proches : Texaco 1 (perche, TACAN 51Y, 251.0) à 153 nm, Arco 1 (panier, TACAN 52Y, 252.0) à 163 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Altengrabow")
        :setFriendlyName("Altengrabow")
        :setRadioGroupName("Frappe profonde")
        :setBriefing([[Altengrabow (BULLSEYE 075/63) : une batterie de missiles sol-sol Iskander déployée sur le terrain d'Altengrabow. À détruire : les trois lanceurs Iskander et leurs véhicules. Défense : SA-15 Tor et SA-19 Tunguska. Hors couverture QRA rouge. Ravitailleurs les plus proches : Texaco 1 (perche, TACAN 51Y, 251.0) à 106 nm, Arco 1 (panier, TACAN 52Y, 252.0) à 117 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Wittenberg")
        :setFriendlyName("Wittenberg")
        :setRadioGroupName("Frappe profonde")
        :setBriefing([[Wittenberg (BULLSEYE 095/76) : le nœud logistique du franchissement de l'Elbe à Wittenberg (B2). À détruire : le dépôt de munitions, l'entrepôt, les réservoirs et les camions. Défense : SA-19 Tunguska et ZU-23. Hors couverture QRA rouge. Ravitailleurs les plus proches : Texaco 1 (perche, TACAN 51Y, 251.0) à 130 nm, Arco 1 (panier, TACAN 52Y, 252.0) à 140 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Torgau")
        :setFriendlyName("Torgau")
        :setRadioGroupName("Frappe profonde")
        :setBriefing([[Torgau (BULLSEYE 107/91) : le dépôt de munitions et de carburant de Torgau, sur l'Elbe. À détruire : les dépôts de munitions, les entrepôts et le réservoir. Défense : batterie VEAF de niveau 4 (SA-8 ou Tor, missiles IR, AAA). Hors couverture QRA rouge. Ravitailleurs les plus proches : Texaco 1 (perche, TACAN 51Y, 251.0) à 151 nm, Arco 1 (panier, TACAN 52Y, 252.0) à 160 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Parchim")
        :setFriendlyName("Base aérienne de Parchim")
        :setRadioGroupName("Bases aériennes")
        :setBriefing([[Base aérienne de Parchim (BULLSEYE 031/107) : la base aérienne de Parchim, où stationnent des MiG-29S et des Su-27. À détruire : les avions au parking et le réservoir de carburant. Défense : SA-15 Tor et SA-11 Buk. Hors couverture QRA rouge. Ravitailleurs les plus proches : Texaco 1 (perche, TACAN 51Y, 251.0) à 88 nm, Arco 1 (panier, TACAN 52Y, 252.0) à 99 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Werneuchen")
        :setFriendlyName("Base aérienne de Werneuchen")
        :setRadioGroupName("Bases aériennes")
        :setBriefing([[Base aérienne de Werneuchen (BULLSEYE 074/127) : la base aérienne de Werneuchen, à l'est de Berlin, avec des Su-30, des MiG-31 et un Il-76. À détruire : les avions au parking. Défense : SA-22 Pantsir et SA-11 Buk ; la base est sous le parapluie du SA-10 de Berlin. Sous la couverture de la QRA Berlin. Ravitailleurs les plus proches : Texaco 1 (perche, TACAN 51Y, 251.0) à 158 nm, Arco 1 (panier, TACAN 52Y, 252.0) à 169 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Rostock")
        :setFriendlyName("Rade de Rostock")
        :setRadioGroupName("Antinavire")
        :setBriefing([[Rade de Rostock (BULLSEYE 028/156) : des cargos et un pétrolier au mouillage devant Warnemünde, à l'entrée du port de Rostock, escortés par une corvette. À détruire : les cargos, le pétrolier et la corvette. Défense : la corvette Molniya ; la rade est sous le parapluie du SA-10 de Rostock. Sous la couverture de la QRA Laage. Ravitailleurs les plus proches : Texaco 1 (perche, TACAN 51Y, 251.0) à 115 nm, Arco 1 (panier, TACAN 52Y, 252.0) à 124 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Mukran")
        :setFriendlyName("Prorer Wiek (Mukran)")
        :setRadioGroupName("Antinavire")
        :setBriefing([[Prorer Wiek (Mukran) (BULLSEYE 042/195) : un groupe naval au mouillage dans la baie de Prorer Wiek, devant le port de Mukran (Rügen). À détruire : la frégate, le patrouilleur et le cargo. Défense : la frégate Rezky et le patrouilleur du projet 22160. Hors couverture QRA rouge. Ravitailleurs les plus proches : Texaco 1 (perche, TACAN 51Y, 251.0) à 170 nm, Arco 1 (panier, TACAN 52Y, 252.0) à 180 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.GetZone("combatZone_Baumholder_Medium"):addZoneElementsFromZoneNamed("combatZone_Baumholder_Easy")
    veafCombatZone.GetZone("combatZone_Baumholder_Hard"):addZoneElementsFromZoneNamed("combatZone_Baumholder_Medium")
    veafCombatZone.GetZone("combatZone_Baumholder_Hard"):addZoneElementsFromZoneNamed("combatZone_Baumholder_Easy")
    veafCombatZone.GetZone("combatZone_WahnerHeide_Medium"):addZoneElementsFromZoneNamed("combatZone_WahnerHeide_Easy")
    veafCombatZone.GetZone("combatZone_WahnerHeide_Hard"):addZoneElementsFromZoneNamed("combatZone_WahnerHeide_Medium")
    veafCombatZone.GetZone("combatZone_WahnerHeide_Hard"):addZoneElementsFromZoneNamed("combatZone_WahnerHeide_Easy")
    veafCombatZone.GetZone("combatZone_Borkenberge_Medium"):addZoneElementsFromZoneNamed("combatZone_Borkenberge_Easy")
    veafCombatZone.GetZone("combatZone_Borkenberge_Hard"):addZoneElementsFromZoneNamed("combatZone_Borkenberge_Medium")
    veafCombatZone.GetZone("combatZone_Borkenberge_Hard"):addZoneElementsFromZoneNamed("combatZone_Borkenberge_Easy")
    veafCombatZone.initialize()
end

if veafQraManager then
    veafQraManager.initialize()
    VeafQRA.ToggleAllSilence(false)
    local QRA_Berlin = VeafQRA:new()
        :setName("QRA Berlin")
        :setCoalition(coalition.side.RED)
        :addEnnemyCoalition(coalition.side.BLUE)
        :setTriggerZone("QRA-Berlin")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA Berlin - MiG-29S A", "QRA Berlin - MiG-29S B"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA Berlin - Su-27", "QRA Berlin - MiG-29S A"}, 2)
        :setRandomGroupsToDeployByEnemyQuantity(6, {"QRA Berlin - Su-30", "QRA Berlin - Su-27", "QRA Berlin - MiG-29S B"}, 3)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(60)
        :setAirportLink("Schonefeld")
        :start()
    local QRA_Laage = VeafQRA:new()
        :setName("QRA Laage")
        :setCoalition(coalition.side.RED)
        :addEnnemyCoalition(coalition.side.BLUE)
        :setTriggerZone("QRA-Laage")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA Laage - MiG-29S A", "QRA Laage - MiG-29S B"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA Laage - Su-27", "QRA Laage - MiG-29S A"}, 2)
        :setRandomGroupsToDeployByEnemyQuantity(6, {"QRA Laage - Su-30", "QRA Laage - Su-27", "QRA Laage - MiG-29S B"}, 3)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(60)
        :setAirportLink("Laage")
        :start()
    local QRA_Leipzig = VeafQRA:new()
        :setName("QRA Leipzig")
        :setCoalition(coalition.side.RED)
        :addEnnemyCoalition(coalition.side.BLUE)
        :setTriggerZone("QRA-Leipzig")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA Leipzig - MiG-29S A", "QRA Leipzig - MiG-29S B"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA Leipzig - Su-27", "QRA Leipzig - MiG-29S A"}, 2)
        :setRandomGroupsToDeployByEnemyQuantity(6, {"QRA Leipzig - Su-30", "QRA Leipzig - Su-27", "QRA Leipzig - MiG-29S B"}, 3)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(60)
        :setAirportLink("Schkeuditz")
        :start()
    local QRA_Celle = VeafQRA:new()
        :setName("QRA Celle")
        :setCoalition(coalition.side.BLUE)
        :addEnnemyCoalition(coalition.side.RED)
        :setTriggerZone("QRA-Celle")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA Celle - F-16C A", "QRA Celle - F-16C B"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA Celle - F-15C", "QRA Celle - F-16C A"}, 2)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(60)
        :setAirportLink("Wunstorf")
        :start()
    local QRA_Francfort = VeafQRA:new()
        :setName("QRA Francfort")
        :setCoalition(coalition.side.BLUE)
        :addEnnemyCoalition(coalition.side.RED)
        :setTriggerZone("QRA-Francfort")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA Francfort - F-16C A", "QRA Francfort - F-16C B"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA Francfort - F-15C", "QRA Francfort - F-16C A"}, 2)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(60)
        :setAirportLink("Wiesbaden")
        :start()
end

-- ── Features ──

if veafGrass then
    veafGrass.initialize()
end

if veafAssets then
    veafAssets.Assets = {
        {sort = 1, name = "Texaco 1", description = "Texaco 1 (KC-135, perche) - nord", information = [[TACAN 51Y
U251.0 - FL220]]},
        {sort = 2, name = "Arco 1", description = "Arco 1 (KC-135MPRS, panier) - nord", information = [[TACAN 52Y
U252.0 - FL180]]},
        {sort = 3, name = "Texaco 2", description = "Texaco 2 (KC-135, perche) - sud", information = [[TACAN 53Y
U253.0 - FL240]]},
        {sort = 4, name = "Arco 2", description = "Arco 2 (KC-135MPRS, panier) - sud", information = [[TACAN 54Y
U254.0 - FL160]]},
        {sort = 5, name = "Shell 1", description = "Shell 1 (KC-135, perche) - arrière, Ramstein", information = [[TACAN 55Y
U255.0 - FL200]]},
        {sort = 6, name = "Overlord 1", description = "Overlord 1 (E-3A) - nord", information = "U265.0 - FL300"},
        {sort = 7, name = "Magic 1", description = "Magic 1 (E-3A) - sud", information = "U266.0 - FL310"},
        {sort = 8, name = "Tanker Rouge", description = "Tanker Rouge (Il-78M)", information = "U261.0 - FL200"},
        {sort = 9, name = "AWACS Rouge", description = "AWACS Rouge (A-50)", information = "U260.0 - FL300"},
    }
    veafAssets.initialize()
end

if veafMove then
    veafMove.initialize()
end

if veafWeather then
    veafWeather.initialize()
end

if veafRemote then
    veafRemote.initialize()
end

if veafAirbases then
    veafAirbases.initialize()
end

-- ── Infrastructure ──

if veafMarkers then
    veafMarkers.initialize()
end

if veafTime then
    veafTime.initialize()
end

if veafUnits then
    veafUnits.initialize()
end

if veafCacheManager then
    veafCacheManager.initialize()
end

if veafEventHandler then
    veafEventHandler.initialize()
end

-- ── Core ──

if veafGroundAI then
    veafGroundAI.initialize()
end

-- ── Infrastructure ──

if veafCommands then
    veafCommands.initialize()
end

-- ── Features ──

if veafInterpreter then
    veafInterpreter.initialize()
end

-- ── Community scripts disabled (VEAF leaves their globals alone) ──────────────
veaf.setConfig("tum", "enable", false)

-- ── Skynet-IADS ──────────────────────────────────────────────────────────────
if veafSkynet then
    veafSkynet.SpotterNetwork = true
    veafSkynet.SpotterView = "radio"
    veafSkynet.initialize(false, false, false, false)
end

-- ── CSAR configuration ───────────────────────────────────────────────────────
-- Note: CSAR.lua must be loaded by mission-script.lua before this block.
if csar then
    csar.initialize()
end
