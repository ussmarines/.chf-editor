# Laboratoire local CHF

Éditeur local et CLI Python pour inspecter des presets Star Citizen `.chf` v7/v8, comparer deux fichiers et produire des variantes contrôlées. Les modifications ADN équilibrées préservent la somme des poids de la région. Les modifications de matériaux sont limitées aux paramètres déjà présents dans le fichier.

Le programme ne rend pas de personnage en 3D. Une validation structurelle ne prouve ni le chargement par Star Citizen, ni une sauvegarde par BioCorp, ni un effet visuel.

## Confidentialité

Ce dépôt public ne contient aucun preset de personnage, fichier du jeu, capture ou vidéo. Les profils par défaut, personnages personnalisés, expériences et données extraites du jeu restent privés. Les sorties locales sont conservées sous `outputs/`, exclu de Git.

## Prérequis et démarrage

- Windows et Python 3 ; Tkinter pour l’interface graphique.
- Une bibliothèque native Zstandard compatible (`libzstd.dll`) pour les commandes CLI.
- `pytest` pour exécuter les tests.

```powershell
git clone https://github.com/ussmarines/.chf-editor.git
cd .chf-editor
python -m pytest -q
python gui.py
```

Dans l’interface, sélectionner la DLL Zstandard et ouvrir un preset local. L’application fournit sept onglets : résumé, ADN, ItemPorts, matériaux, diff, preuves et composition. Les sources et limites des mappings sont affichées dans l’onglet **Preuves**.

## CLI

Toutes les commandes prennent `--zstd-dll` avec le chemin de votre DLL. Exemples :

```powershell
$py = 'python'
$dll = 'C:\chemin\vers\libzstd.dll'
& $py chf.py --zstd-dll $dll inspect 'C:\presets\personnage.chf'
& $py chf.py --zstd-dll $dll diff 'C:\presets\avant.chf' 'C:\presets\apres.chf'
& $py chf.py --zstd-dll $dll agent-choices 'C:\presets\default_women.chf' 'C:\presets\Default_men.chf'
```

`variant` modifie deux poids ADN compensés dans une région. `variant-param` modifie une valeur matérielle déjà présente. `compose` applique une recette de changements distincts à une source dont le SHA-256 est fixé. Les commandes refusent d’écraser leurs sorties et créent un manifeste d’expérience.

Le lecteur vérifie la taille fixe, le CRC32C, les limites de décompression, la structure v7/v8 et la consommation du payload. L’export est relu et son diff logique contrôlé. Préserver séparément les fichiers originaux.

## Preuves et essais en jeu

Pour chaque résultat, distinguer la structure valide, le chargement en jeu, la sauvegarde par le jeu et l’effet visuel observé. Les noms de champs issus des sources et les correspondances observées sur un preset ne garantissent pas le même effet sur un autre personnage. Les essais demandant BioCorp restent à valider dans le jeu avec des captures comparables.

Voir [le protocole de paire contrôlée](docs/CONTROLLED_GAME_PAIR.md), [les expériences](docs/EXPERIMENTS.md), [le workflow agent](docs/AGENT_WORKFLOW.md) et [la politique de sécurité](SECURITY.md).

## Tests

```powershell
python -m unittest discover -s tests -v
```

Les tests du writer nécessitent un preset CHF local et une DLL Zstandard ; ces fichiers privés ne sont pas inclus dans le dépôt.

## Soutenir le projet

[Faire un don via PayPal](https://paypal.me/ussmarinesdot)
