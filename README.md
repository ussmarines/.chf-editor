# Laboratoire local CHF

CLI Python pour inspecter, comparer et produire une variante contrôlée d'un preset Star Citizen `.chf` v7/v8 : **deux poids ADN équilibrés** dans une région, un flottant de matériau ou un canal RGBA. Le rendu de référence est celui du jeu ; ce programme ne visualise pas un personnage. Un contrôle structurel réussi ne prouve ni chargement ni effet visuel.

Ce dépôt public ne fournit aucun preset, fichier du jeu ou média de test. Les fichiers de personnages, captures, vidéos, extractions et manifestes de travail restent privés et ne doivent pas être publiés.

## Prérequis

- Windows et Python 3 ; Tkinter est requis pour l'interface graphique.
- Une bibliothèque native Zstandard compatible (`libzstd.dll`) à fournir localement aux commandes CLI.
- `pytest` pour exécuter les tests.

Clonez le dépôt et vérifiez la suite :

```powershell
git clone https://github.com/ussmarines/.chf-editor.git
cd .chf-editor
python -m pytest -q
python gui.py
```

Les commandes CLI nécessitent `--zstd-dll` avec le chemin vers votre propre DLL. Aucun profil Star Citizen ni asset de jeu n'est fourni.

## Démarrage

Python 3 et une bibliothèque native Zstandard (`libzstd.dll` sur Windows) sont nécessaires. Aucune donnée du jeu n'est incluse. Donner un chemin complet à `--zstd-dll` :

Sur cette machine, `python gui.py` ouvre l'interface locale et préremplit les chemins des deux nouveaux presets si présents. Les six onglets affichent le résumé, l'ADN, les ItemPorts, les matériaux, le diff et les preuves. L'onglet **Preuves** associe les régions ADN et champs matériels testés à leur contrôle, effet observé, build, référence SHA-256 et source ; il énumère les autres régions ADN et compte les occurrences matérielles inconnues. Une signature ADN ou une structure matérielle identique dans un autre preset est signalée comme **à vérifier sur ce fichier**. Deux formulaires permettent l'export de deux poids ADN compensés dans la même région ou d'une seule valeur brute de matériau déjà présente. L'export matériel vérifie aussi le SHA-256 de la source ouverte et le `name_hash` sélectionné ; il garde le même contrôle strict que la CLI.

```powershell
$py = 'python'
$dll = 'C:\chemin\vers\libzstd.dll'
& $py chf.py --zstd-dll $dll inspect 'C:\mes-presets\femme.chf'
& $py chf.py --zstd-dll $dll inspect 'C:\mes-presets\homme.chf'
& $py chf.py --zstd-dll $dll diff 'C:\mes-presets\avant.chf' 'C:\mes-presets\apres.chf'
& $py chf.py --zstd-dll $dll variant 'C:\mes-presets\femme.chf' 'outputs\essai.chf' --part Nose --slot 0 --balance-slot 1 --value 13531 --game-version 'LIVE build à relever' --control 'Nose slot 0 +1 et slot 1 -1 (exemple à adapter au preset)'
& $py chf.py --zstd-dll $dll variant-param 'C:\mes-presets\femme.chf' 'outputs\materiau-essai.chf' --expected-source-sha256 '<SHA-256 obtenu par inspect>' --material-index 0 --submaterial-index 0 --kind float --param-index 0 --name-hash '<hash obtenu par inspect>' --value 0.5 --game-version 'LIVE build à relever' --control 'paramètre brut sous essai'
```

`inspect` présente le conteneur, DNA, l'arbre ItemPort et les matériaux avec leurs valeurs brutes et positions dans le payload. `variant` accepte `value` dans `0..65535`, mais exige aussi `--balance-slot` : l'autre poids de la même région change de la quantité opposée, pour préserver la somme observée dans la source ; l'opération est refusée si l'autre poids ne peut absorber l'écart. Les `head_id` restent intacts. `variant-param` exige le SHA-256 de la source et le hash du paramètre choisi ; pour une couleur, ajouter `--kind color --channel R|G|B|A` et une valeur entière `0..255`. Les deux commandes refusent une sortie déjà présente. Elles écrivent le `.chf` et un manifeste `.experiment.json` contenant chemins, SHA-256, diff, version indiquée, contrôle, état du test en jeu et captures à compléter. Une variante ADN équilibrée n'est pas une reproduction du geste ni du rendu de BioCorp.

Le writer préserve les octets d'en-tête inconnus, les `head_id`, les champs opaques du payload et les octets du conteneur hors flux compressé. Il refuse un flux qui empiète sur ces derniers. Le relecteur vérifie taille fixe, CRC32C, tailles Zstandard, limites, structure v7/v8 et consommation complète. Il compare le diff logique attendu avant d'émettre la sortie, puis relit le fichier émis. La version actuelle ne modifie ni GUID ni `head_id` ; l'édition de matériau est expérimentale et ne prouve pas un effet dans le jeu.

Les `.chf`, manifestes d'expériences, `private/` et `outputs/` sont ignorés par Git. Ne pas publier les presets privés ni les captures sans instruction explicite. Déplacer une variante vers `CustomCharacters` uniquement après avoir sauvegardé la base et préparé le test ; consigner ensuite le build exact du jeu, le chargement, la sauvegarde éventuelle, des captures comparables et le verdict `effet confirmé`, `aucun effet visible`, `ambigu` ou `non testé`. Les variantes locales créées pendant la validation n'ont pas été copiées dans le dossier du jeu.

Voir [la base de connaissance](docs/KNOWLEDGE.md), [la procédure d'expérience](docs/EXPERIMENTS.md) et [le registre local des bugs candidats de BioCorp](docs/GAME_BUG_CANDIDATES.md). Ce registre distingue les défauts reproduits des observations encore ambiguës ; aucun rapport CIG n'a été envoyé.

Les [notes et scripts CHF historiques de SpaceShooter](research/README.md) sont archivés dans `research/space-shooter/` avec leur provenance locale. La [vidéo utilisateur](docs/VIDEO_OBSERVATIONS.md) et l'[inventaire des marqueurs bleus de BioCorp](docs/BIOCORP_MARKER_INVENTORY.md) sont documentés sans publier les médias privés.

La [recherche ciblée dans `Data.p4k` et `Game2.dcb`](docs/GAME_FILE_FINDINGS.md) fournit maintenant des noms source pour les paramètres et certains GUID. L'interface affiche ces étiquettes à côté des valeurs brutes ; elles ne garantissent pas l'effet visuel d'une modification. L'objectif de création complète sans démarrer le jeu est une phase ultérieure, après validation des paramètres et de la compatibilité.

Pour produire une correspondance contrôle → CHF, suivre [le protocole de paire contrôlée](docs/CONTROLLED_GAME_PAIR.md). Les instructions de contribution de l'agent sont dans [AGENTS.md](AGENTS.md) ; la mémoire de projet se lit via `BRAIN.md` et son CLI.

Les [essais en jeu du 27 septembre](docs/GAME_TEST_2026-09-27.md) consignent les paires sauvegardées par BioCorp, les variantes synthétiques testées et leurs limites de preuve. Les `.chf` et captures correspondants restent privés sous `outputs/`.
