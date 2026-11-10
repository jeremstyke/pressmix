# Consignes de rédaction (tâche quotidienne)

Chaque jour : 15 à 20 articles en français et 15 à 20 articles en anglais, sur des sujets précis et détaillés.

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

## Règles SEO et qualité

### Des sujets pointus, pas généralistes
- Une question précise par article, comme une vraie recherche Google de longue traîne. Exemples : pas « comment économiser de l'argent » mais « comment résilier son assurance emprunteur avec la loi Lemoine » ; pas « bien dormir » mais « se réveiller à 3 h du matin chaque nuit : causes et solutions » ; pas « choisir un smartphone » mais « iPhone qui chauffe en charge : que faire ».
- Jamais deux articles sur la même requête : vérifier les slugs existants avant d'écrire.
- Varier les catégories chaque jour pour couvrir les 15 catégories.

### Des articles détaillés
- 900 à 1 300 mots. Répondre à la question dès l'introduction, puis aller dans le détail.
- Du concret partout : étapes numérotées précises (menus, réglages, démarches), exemples chiffrés, cas particuliers, erreurs fréquentes, ce qui change selon la situation, prix ou délais réels.
- Quand c'est utile : un tableau comparatif (en liste si besoin), une section FAQ « Questions fréquentes » avec 3 à 5 questions, un encadré conseil en citation (>).
- Vérifier par une recherche web les faits qui changent (prix, lois, montants d'aides, dates, versions de logiciels) et ne garder que ce qui est confirmé par une source fiable (site officiel, service-public.fr, éditeur...). Jamais de chiffre inventé.
- En santé, argent et droit : rester exact et nuancé, et conseiller un professionnel quand c'est pertinent.
- 4 à 8 sections `##`, sous-sections `###`, listes, **gras** sur les points clés, section « En résumé » (« Summary » en anglais) à la fin.
- 2 à 4 liens internes vers des articles existants du site : `[texte](/slug-de-l-article/)` (anglais : `/en/slug/`). Un lien externe vers une source officielle est bienvenu.
- Anglais : écrire nativement pour un public international, avec des requêtes anglaises propres (pas une traduction mot à mot).
- Ne rien copier d'autres sites. Jamais de tiret cadratin (—) : tirets courts, deux-points ou virgules.

## Étaler la publication

Les articles dont la `date` est dans le futur ne sont pas publiés. Le site est regénéré toutes les 3 heures : pour étaler la publication dans la journée, donner aux articles des heures différentes (ex. de 06:00 à 23:00).
