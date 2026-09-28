# Création assistée par un agent externe

Le projet peut être piloté par Codex, Claude ou un autre agent capable de lire des fichiers locaux et d'exécuter une commande. Aucune clé API ni fournisseur d'IA n'est nécessaire dans l'éditeur CHF. L'agent traite la description, l'image de référence et les captures du personnage ; le programme CHF fournit les champs éditables, les preuves et un writer contrôlé.

## Contrat local

1. Garder les `.chf`, images, captures et recettes sous `outputs/` ou hors dépôt. Préserver le preset source octet pour octet.
2. Présenter **féminin ou masculin** avant toute édition. Exécuter `python chf.py --zstd-dll CHEMIN_DLL agent-choices BASE_FEMME.chf BASE_HOMME.chf` pour obtenir deux options JSON. La sélection de l'utilisateur fixe la base de cette itération ; ne pas mélanger leurs exemples.
3. Exécuter `python chf.py --zstd-dll CHEMIN_DLL agent-context PRESET_CHOISI.chf`. La sortie JSON contient le SHA-256 source, les poids ADN, les champs de matériaux présents, les preuves disponibles et les exemples BioCorp dont la base a **la même signature et les mêmes régions ADN**. `baseline_match` indique si le fichier source est exactement la base de laboratoire ou si ses matériaux diffèrent. Le chemin local d'un exemple n'est fourni que si le fichier privé existe et correspond au SHA enregistré. Les noms et observations ne prouvent pas le rôle anatomique d'un poids isolé.
4. À partir d'une description ou d'images, proposer **une hypothèse** de changements avec justification et incertitude. Préparer une recette JSON `schema: 1` pour `compose`, en gardant le `source_sha256` exact. Ne modifier que des champs présents. Pour l'ADN, préférer un exemple BioCorp du même preset de base lorsque l'effet visé correspond à son observation ; sinon choisir deux slots distincts et une valeur équilibrable en signalant le caractère expérimental. Ne pas présenter l'image comme une mesure directe des poids CHF.
5. Exécuter `python chf.py --zstd-dll CHEMIN_DLL compose PRESET.chf SORTIE.chf --recipe RECETTE.json`. Lire le manifeste `.experiment.json`, le diff et le résultat de relecture. Une sortie structurellement valide n'est pas encore un personnage validé dans le jeu.
6. Si un résultat visuel est demandé, soumettre la sortie à un chargement dans BioCorp et comparer des captures au même angle, zoom, éclairage et coiffure. L'utilisateur peut effectuer cette étape dans le jeu. Consigner séparément : structure, chargement, sauvegarde par BioCorp, effet visible.
7. Faire une nouvelle recette depuis la source ou une variante explicitement choisie, avec son SHA-256 actuel. Conserver les itérations et leur provenance ; éviter d'écraser les anciens essais.

### Exemple de transfert contrôlé de régions

L'exemple suivant illustre la forme, sans chemins ni SHA réels. Prendre `source_sha256` dans la racine de `agent-context`, puis `baseline_sha256`, `reference_sha256` et `local_reference_path` dans chaque exemple proposé. Les régions doivent être distinctes ; les fichiers de référence restent privés sous `outputs/`.

```json
{
  "schema": 1,
  "source_sha256": "SHA de la base ouverte",
  "game_version": "LIVE 4.10.193.11644",
  "edits": [
    {
      "kind": "dna_region_from_reference",
      "regions": ["CheekLeft", "CheekRight"],
      "reference": "chemin local du fichier BioCorp pommettes",
      "reference_sha256": "SHA du fichier BioCorp pommettes",
      "baseline_sha256": "SHA de la base de laboratoire indiquée pour cet exemple",
      "control": "pommettes plus larges, transfert expérimental"
    },
    {
      "kind": "dna_region_from_reference",
      "regions": ["Jaw"],
      "reference": "chemin local du fichier BioCorp mâchoire",
      "reference_sha256": "SHA du fichier BioCorp mâchoire",
      "baseline_sha256": "SHA de la base de laboratoire indiquée pour cet exemple",
      "control": "mâchoire plus large, transfert expérimental"
    }
  ]
}
```

Le writer accepte seulement les exemples répertoriés dans `chflab/reference_exemplars.json`. Il vérifie les SHA, l'égalité de l'ADN complet et de la signature entre la source et la base de laboratoire, l'absence de changement dans les autres régions ADN du donneur, les offsets, le diff attendu et la relecture. Il copie les quatre paires poids/`head_id` de chaque région sélectionnée. Les autres changements du fichier BioCorp, notamment flags et couleurs annexes, ne sont pas copiés. Les profils d'origine et les bases de laboratoire ont le même ADN, mais des différences matérielles : le rendu visuel du transfert sur les profils d'origine et la compatibilité d'une combinaison exigent un essai dans le jeu.

## Limites actuelles

Les essais BioCorp relient plusieurs marqueurs à des **régions** CHF et décrivent des effets visuels. Ils ne relient pas chaque poids ou `head_id` à un axe anatomique précis. Un agent peut donc choisir des expériences prudentes, mais ne peut pas encore produire de manière fiable un visage ressemblant à une photo en une seule passe. Une boucle de retours visuels améliore le résultat. L'agent doit signaler clairement les réglages déduits et ceux effectivement observés.

L'image de référence et les captures restent sur la machine de l'utilisateur. Si un agent distant est utilisé, la transmission de ces fichiers dépend de l'outil choisi et doit être décidée séparément. Le programme ne téléverse rien.
