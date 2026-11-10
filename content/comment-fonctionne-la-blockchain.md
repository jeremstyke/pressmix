---
title: Comment fonctionne la blockchain ? L'explication simple
seo_title: Comment fonctionne la blockchain : explication simple
description: Blocs, minage, validation, décentralisation : on vous explique simplement comment fonctionne la blockchain, la technologie derrière le bitcoin et les cryptos.
category: crypto
lang: fr
date: 2026-11-10T08:45:00+01:00
tags: blockchain, bitcoin, cryptomonnaies, minage, décentralisation
---
Une blockchain est un **registre numérique partagé** entre des milliers d'ordinateurs, dans lequel les transactions sont regroupées en **blocs** reliés les uns aux autres de façon sécurisée. Comme chaque bloc dépend du précédent et que des copies existent partout, il est **extrêmement difficile de modifier l'historique**. C'est la technologie qui permet au bitcoin et aux autres cryptomonnaies de fonctionner sans banque centrale.

## Un grand livre de comptes partagé

Imaginez un cahier de comptes où chaque opération est inscrite à la suite. Au lieu d'être gardé par une seule banque, ce cahier est **copié chez tous les participants** du réseau, appelés les **nœuds**. Quand une nouvelle opération est ajoutée, toutes les copies sont mises à jour.

Personne ne peut tricher seul : si quelqu'un modifiait sa copie, elle ne correspondrait plus à celles des autres et serait rejetée.

## Des blocs enchaînés

Les transactions ne sont pas ajoutées une par une, mais regroupées en **blocs**. Chaque bloc contient :

- une liste de transactions ;
- la date ;
- une **empreinte numérique** (un « hash ») du bloc précédent.

Le hash est une sorte de signature calculée à partir du contenu. Si on modifie la moindre virgule d'un bloc, son hash change complètement. Comme chaque bloc contient le hash du précédent, modifier un ancien bloc casserait **toute la chaîne** qui suit. D'où le nom : **chaîne de blocs**.

## Qui valide les transactions ?

Sans autorité centrale, il faut un moyen de se mettre d'accord sur le prochain bloc à ajouter. C'est le rôle du **mécanisme de consensus**. Les deux plus connus :

### La preuve de travail

Utilisée notamment par le bitcoin. Des participants, les **mineurs**, font tourner des ordinateurs pour résoudre un problème mathématique difficile. Le premier qui trouve la solution propose le bloc suivant et reçoit une récompense. Ce système est très sûr mais **consomme beaucoup d'énergie**.

### La preuve d'enjeu

Utilisée notamment par Ethereum depuis 2022. Les **validateurs** immobilisent une partie de leurs cryptos en garantie. Ils sont choisis pour proposer et vérifier les blocs, et risquent de perdre une partie de leur mise s'ils trichent. Ce système consomme beaucoup moins d'énergie.

## Une transaction pas à pas

1. Vous envoyez des cryptos depuis votre portefeuille, en signant l'opération avec votre clé privée. Pour mieux comprendre cette étape, lisez [qu'est-ce qu'un wallet crypto](/qu-est-ce-qu-un-wallet-crypto/).
2. La transaction est diffusée au réseau et attend d'être intégrée.
3. Les mineurs ou validateurs vérifient qu'elle est valide (vous avez bien les fonds, la signature est correcte).
4. Elle est intégrée dans un bloc, qui est ajouté à la chaîne.
5. Chaque nouveau bloc ajouté ensuite renforce sa **confirmation**.

## Publique ou privée ?

- **Blockchains publiques** : tout le monde peut consulter les transactions et participer, comme sur Bitcoin ou Ethereum. Les adresses ne portent pas de nom, mais l'historique est visible par tous.
- **Blockchains privées** : réservées à un groupe d'acteurs, utilisées par certaines entreprises.

## Au-delà des cryptomonnaies

La blockchain sert aussi à exécuter des **smart contracts**, des programmes qui s'exécutent automatiquement quand certaines conditions sont réunies, à créer des jetons numériques ou à assurer la traçabilité de produits.

## Les limites à connaître

- **Lenteur et frais** variables selon l'encombrement du réseau.
- **Consommation d'énergie** élevée pour la preuve de travail.
- **Irréversibilité** : une erreur d'adresse ne peut pas être annulée.
- **Volatilité** des cryptomonnaies associées : n'investissez que ce que vous pouvez vous permettre de perdre, après avoir constitué une [épargne de précaution](/comment-constituer-une-epargne-de-precaution/).

## En résumé

- La blockchain est un **registre partagé** copié sur de nombreux ordinateurs.
- Les transactions sont regroupées en **blocs reliés par leur empreinte**, ce qui rend l'historique très difficile à falsifier.
- Un **mécanisme de consensus** (preuve de travail ou d'enjeu) remplace l'autorité centrale.
- Elle permet les cryptos, mais aussi les smart contracts et la traçabilité.
