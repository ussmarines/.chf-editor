# Première paire contrôlée à produire dans Star Citizen

But : relier **un contrôle visible** à son diff CHF sur le build LIVE `4.10.193.11644`, sans déduire un effet d'un nom de hash. Les deux `default_*.chf` reçus restent des références intactes.

## Opérations dans le jeu

1. Copier `default_women.chf` vers un dossier de sauvegarde **hors du jeu** et relever son SHA-256. Laisser l'original intact.
2. Dans le créateur BioCorp, charger ce personnage. Sans changer de contrôle, enregistrer une nouvelle copie nommée `lab_woman_00_baseline.chf`.
3. Choisir **un seul** curseur au nom lisible, de préférence `Freckles Amount` si l'interface le propose. Noter son onglet, sa valeur avant et sa valeur après. Déplacer ce seul curseur vers une valeur nettement différente, sans changer coiffure, couleur, ADN ou autre option. Enregistrer une seconde copie `lab_woman_01_one_control.chf`.
4. Faire deux captures comparables : même angle, même zoom, même éclairage, une de chaque état. Noter si les deux fichiers se rechargent et si la sauvegarde reste possible.
5. Fournir les chemins des deux `.chf`, les captures et le nom/valeurs du contrôle. Les fichiers n'ont pas à être placés dans Git ; un dossier local privé suffit.

## Ce que le laboratoire fera ensuite

`chf.py diff` contrôlera CRC, Zstandard, structure v8 et toutes les différences logiques. Si la sauvegarde du jeu modifie aussi d'autres champs (normalisation, timestamps, équipement), la paire restera **ambiguë** et une répétition sera nécessaire. Un effet visible et un diff simple permettront de promouvoir le mapping au niveau « confirmé pour ce build ». Le même protocole sera ensuite répété sur le personnage masculin et les autres familles de contrôles.

La vidéo précédente prouve les options et effets qu'elle montre à l'écran ; elle ne contient pas ces deux sauvegardes isolées. Les variantes `+1` de `outputs/` passent seulement le contrôle structurel, pas le gate de chargement.
