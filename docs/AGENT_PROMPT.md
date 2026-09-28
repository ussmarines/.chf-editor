# Consigne à remettre à un agent local

Tu travailles dans le dépôt `.chf-editor` pour aider à créer un personnage Star Citizen à partir de ma description et, si je les fournis, d'images de référence et de captures de BioCorp. Lis `AGENTS.md`, `BRAIN.md` via son CLI, puis `docs/AGENT_WORKFLOW.md`. Ne téléverse aucun `.chf`, image ou capture et ne modifie pas les fichiers originaux.

1. Propose le choix entre les deux profils d'origine `default_women.chf` et `Default_men.chf`. Demande uniquement les informations encore nécessaires : profil choisi, description du personnage ou image de référence, et changements prioritaires. Si elles sont déjà dans la conversation, utilise-les.
2. Exécute `agent-choices` sur les deux profils, puis `agent-context` sur le preset choisi avec la DLL Zstandard disponible localement. Utilise seulement les exemples BioCorp proposés pour cette base et lis `baseline_match` ; les matériaux de la base de laboratoire peuvent différer de ceux du profil d'origine. Distingue ce qui est observé en jeu de ce qui est seulement déduit de l'image ou des noms de paramètres.
3. Propose une première itération courte et motivée, avec incertitudes. Prépare une recette `compose` dans `outputs/`, puis exporte un nouveau `.chf` sous `outputs/`. Consulte le manifeste, le diff et la relecture. Ne remplace jamais une sortie existante.
4. Rapporte séparément : structure valide, chargement en jeu, sauvegarde par BioCorp et effet visuel. Si l'itération exige BioCorp, donne-moi les actions précises à faire ; attends mon retour et les captures avant d'affirmer une ressemblance.
5. Conserve les SHA et la provenance de chaque itération. Arrête-toi au prochain geste que seul l'utilisateur peut faire dans le jeu, ou quand la description/image de référence manque réellement.

Le writer prend en charge des transferts de régions ADN cataloguées et des changements bruts équilibrés ou matériels. Il ne calcule pas les paramètres CHF exacts à partir d'une image et ne produit pas encore d'aperçu 3D fidèle.
