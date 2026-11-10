# Consignes de rédaction (tâche quotidienne)

Chaque jour : 15 à 20 articles en français et 15 à 20 articles en anglais.

Chaque article = un fichier `content/<slug>.md`. Le slug = le nom du fichier, en minuscules, sans accents, mots séparés par des tirets, reprenant la requête visée (ex. `comment-detartrer-une-bouilloire`).

## Format

```
---
title: Titre H1 lisible (contient la requête principale)
seo_title: Titre pour Google, 50 à 60 caractères, requête au début
description: Meta description de 140 à 160 caractères qui donne envie de cliquer
category: <slug de catégorie dans config.json>
lang: fr            (ou en)
translation: <slug de l'article dans l'autre langue, si il existe>
date: 2026-11-11T08:00:00+01:00
tags: 3 à 6 mots-clés, séparés, par des virgules
---
Introduction de 2 à 3 phrases qui répond directement à la question.

## Sous-titre H2
...
## En résumé
```

## Règles SEO

- Une requête précise par article, réellement tapée par les gens (« comment… », « combien… », « pourquoi… », « meilleur… », « que faire si… »). Jamais deux articles sur la même requête : vérifier les slugs existants avant d'écrire.
- Environ 600 mots (550 à 700). Répondre à la question dès l'introduction, puis détailler.
- 4 à 8 sections `##`, sous-sections `###` si utile, listes à puces et étapes numérotées, **gras** sur les points clés, une section « En résumé » à la fin.
- 2 à 4 liens internes vers des articles existants du site, en markdown : `[texte](/slug-de-l-article/)` (pour l'anglais : `/en/slug/`).
- Contenu exact et utile : pas de chiffres inventés, pas de fausses citations. En santé, argent et droit, rester général et conseiller un professionnel quand c'est pertinent. Ne rien copier d'autres sites.
- Varier les catégories chaque jour pour couvrir les 15 catégories.
- Anglais : écrire nativement pour un public international (pas une traduction mot à mot), avec des requêtes anglaises propres.
- Jamais de tiret cadratin (—) : utiliser des tirets courts, deux-points ou virgules.

## Étaler la publication

Les articles dont la `date` est dans le futur ne sont pas publiés. Le site est regénéré toutes les 3 heures : pour étaler la publication dans la journée, donner aux articles des heures différentes (ex. de 06:00 à 23:00).
