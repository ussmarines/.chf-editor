<!-- BEGIN brain.md -->
## Project Brain

This project keeps a **Project Brain**: a persistent memory layer of its durable decisions, requirements, and constraints. Read `./BRAIN.md` for the full read/write contract.

Maintain the brain as part of normal coding work — not as a separate task. While discussing or implementing features:
- **Start of a task:** load relevant context with the `brain` CLI (`list-pages`, `read-page`, `read-root`). Prefer a narrow read over scanning everything.
- **When a decision, requirement, constraint, or durable insight settles** (in chat or while coding): capture it immediately via the `brain` CLI. Do not wait to be asked and do not batch it for later.
- **Pure implementation with no new decision:** do not write to the brain.
- **When overturning a prior conclusion:** update the page (`update-truth` and/or `append-timeline` with `kind: reversal`, or `archive-page`).
- Only store what will still matter in six months and is hard to reconstruct from the code alone.
- All reads and writes go through the `brain` CLI — never hand-edit brain files.

The brain skills (`brain-setup`, `brain-page`, `brain-ingest`, `brain-bootstrap`) are installed in your global skills directory. Prefer `brain init` to scaffold a new project.
<!-- END brain.md -->

## Projet CHF

- Travailler sur une branche `codex/`; ne pas modifier `main`, fusionner ni toucher au dossier du jeu sans instruction explicite. La publication d'une branche de préparation publique est autorisée pour la tâche de préparation publique.
- Garder les `.chf` privés, vidéos, captures, `Data.p4k`, `Game2.dcb` et assets extraits sous `outputs/` ou hors dépôt. Ne jamais les ajouter à Git.
- Préserver les originaux octet pour octet. Un export doit passer taille 4096, CRC32C, limites Zstandard, structure v7/v8, préservation des zones opaques, diff logique attendu et relecture indépendante.
- Séparer dans le rapport : structure valide, chargement en jeu, sauvegarde par le jeu et effet visuel. Aucun de ces états ne découle d'un autre.
- Donner une source et un niveau de preuve à tout mapping. Les noms issus de StarBreaker/StarChar ou de `Game2.dcb` ne suffisent pas à prouver un effet anatomique ni la compatibilité d'une substitution.
- Utiliser StarBreaker `08302fbdd3a1cc704a0bc0977fb1841927a637bf` et StarChar `2c4bace845a4004c78b50a7ed902a725545aa5e7` comme révisions de source documentées. Mentionner séparément la version d'un binaire utilisé.
- La phase 1 est la compréhension et la validation contrôlée des paramètres. Ne démarrer le créateur intégralement hors jeu qu'après sa validation explicite par l'utilisateur.
- Exécuter les tests ciblés sur les deux nouveaux presets femme/homme. Les scripts historiques sous `research/space-shooter/` sont une archive, pas le writer principal.
- Pour une question sur une bibliothèque, API ou CLI, consulter Context7 d'abord conformément aux instructions de la session. Graphify peut aider à naviguer le code local ; ne pas installer de hook ou watcher sans besoin explicite.
