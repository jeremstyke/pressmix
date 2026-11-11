---
title: Wi-Fi connecté mais pas d'internet sur Windows : 9 solutions qui marchent
seo_title: Wi-Fi connecté mais pas d'internet sur Windows : solutions
description: « Connecté, pas d'internet » sur Windows ? Box, DNS, adresse IP, pilote, réinitialisation : 9 solutions à tester dans l'ordre, de la plus simple à la plus avancée.
category: tech
lang: fr
translation: wifi-connected-but-no-internet-windows
date: 2026-11-11T09:00:00+01:00
tags: Windows, Wi-Fi, pas d'internet, DNS, réseau
---
Quand Windows affiche « **Connecté, pas d'accès à internet** », votre PC parle bien à la box, mais quelque chose bloque entre la box et internet, ou entre Windows et la box. Dans la majorité des cas, le problème se règle en **redémarrant la box**, en **renouvelant l'adresse IP** ou en **changeant de serveur DNS**. Voici les solutions à tester dans l'ordre, de la plus rapide à la plus poussée.

## Étape 0 : savoir d'où vient la panne

Avant de toucher aux réglages, faites un test simple : **les autres appareils** (téléphone, tablette, télé) ont-ils internet sur le même Wi-Fi ?

- **Aucun appareil n'a internet** : le problème vient de la **box ou de la ligne**. Commencez par la solution 1, puis contactez votre opérateur si rien ne change.
- **Seul le PC n'a pas internet** : le problème vient de **Windows**. Passez directement aux solutions 2 à 9.

Ce diagnostic évite de perdre une heure à réinitialiser un ordinateur alors que c'est la ligne qui est coupée.

## Les solutions rapides (moins de 5 minutes)

### 1. Redémarrer la box et le PC

Débranchez la box **30 secondes**, rebranchez-la et attendez que tous les voyants soient stables, ce qui prend souvent 2 à 5 minutes. Redémarrez ensuite le PC (un vrai redémarrage, pas une mise en veille).

Pendant ce temps, consultez la page d'incidents de votre opérateur ou son application : une panne locale est peut-être déjà signalée.

### 2. Oublier le réseau et s'y reconnecter

1. Ouvrez **Paramètres** > **Réseau et Internet** > **Wi-Fi**.
2. Cliquez sur **Gérer les réseaux connus**.
3. Sélectionnez votre réseau puis **Oublier**.
4. Reconnectez-vous en saisissant à nouveau la clé Wi-Fi.

Cette manipulation efface un profil réseau corrompu, fréquent après une mise à jour de la box.

### 3. Lancer l'utilitaire de résolution des problèmes

Faites un clic droit sur l'icône réseau dans la barre des tâches, puis **Diagnostiquer les problèmes de réseau** (ou via **Paramètres** > **Système** > **Résolution des problèmes**). L'outil corrige seul certains blocages, notamment un adaptateur désactivé.

## Les solutions intermédiaires

### 4. Renouveler l'adresse IP et vider le cache DNS

Ouvrez le **Terminal** ou l'**Invite de commandes** en administrateur (clic droit sur le menu Démarrer > Terminal (administrateur)), puis tapez une à une :

```
ipconfig /release
ipconfig /renew
ipconfig /flushdns
```

Si `ipconfig` affiche une adresse commençant par **169.254**, votre PC n'a pas reçu d'adresse de la box : c'est la cause du problème. Le renouvellement règle souvent la question, sinon redémarrez la box.

### 5. Changer de serveur DNS

Le DNS traduit les noms de sites (exemple.fr) en adresses. Si celui de votre opérateur ne répond plus, les sites ne s'affichent pas alors que la connexion fonctionne.

1. **Paramètres** > **Réseau et Internet** > **Wi-Fi** > cliquez sur votre réseau (propriétés).
2. À la ligne **Attribution du serveur DNS**, cliquez sur **Modifier**.
3. Passez de **Automatique (DHCP)** à **Manuel**, activez **IPv4**.
4. Saisissez par exemple **1.1.1.1** (Cloudflare) en DNS préféré et **8.8.8.8** (Google) en DNS auxiliaire.
5. Enregistrez.

> Test rapide : dans le Terminal, tapez `ping 8.8.8.8`. Si vous obtenez des réponses mais que les sites ne s'ouvrent pas, c'est presque toujours un problème de **DNS**.

### 6. Désactiver le VPN, le proxy ou l'antivirus

Un **VPN** mal fermé, un **proxy** configuré par un logiciel ou un pare-feu tiers peuvent couper l'accès internet tout en laissant le Wi-Fi connecté.

- Déconnectez et quittez votre VPN.
- Vérifiez **Paramètres** > **Réseau et Internet** > **Proxy** : « Utiliser un serveur proxy » doit être désactivé, sauf réseau d'entreprise.
- Désactivez temporairement l'antivirus tiers pour tester.

## Les solutions avancées

### 7. Réinitialiser la pile réseau en ligne de commande

Toujours dans le Terminal administrateur :

```
netsh winsock reset
netsh int ip reset
```

Redémarrez ensuite le PC. Ces commandes remettent à zéro les composants réseau de Windows sans toucher à vos fichiers.

### 8. Mettre à jour ou réinstaller le pilote Wi-Fi

1. Clic droit sur Démarrer > **Gestionnaire de périphériques**.
2. Dépliez **Cartes réseau** et repérez votre carte Wi-Fi (Intel, Realtek, MediaTek...).
3. Clic droit > **Désinstaller l'appareil**, sans cocher la suppression du pilote.
4. Redémarrez : Windows réinstalle automatiquement le pilote.

Si le problème est apparu juste après une mise à jour Windows, essayez plutôt **Propriétés** > onglet **Pilote** > **Restaurer le pilote** quand l'option est disponible.

### 9. Réinitialisation du réseau Windows

C'est la solution de dernier recours, efficace mais plus lourde :

1. **Paramètres** > **Réseau et Internet** > **Paramètres réseau avancés**.
2. **Réinitialisation du réseau** > **Réinitialiser maintenant**.

Le PC redémarre et tous les adaptateurs sont réinstallés. **Vous devrez ressaisir vos mots de passe Wi-Fi** et reconfigurer un éventuel VPN.

## Cas particuliers

- **Wi-Fi public (hôtel, gare, train)** : le message apparaît souvent parce que la **page de connexion** ne s'est pas ouverte. Tapez une adresse en http simple dans le navigateur pour la faire apparaître.
- **Problème uniquement le soir** : saturation de la ligne ou du canal Wi-Fi. Rapprochez-vous de la box ou passez sur la bande 5 GHz. Nos conseils pour [réduire le ping en jeu](/comment-reduire-le-ping-en-jeu/) aident aussi à stabiliser la connexion.
- **PC qui rame en plus** : un disque plein ralentit tout, y compris le réseau. Voir [comment libérer de l'espace sur un PC Windows](/comment-liberer-de-l-espace-sur-un-pc-windows/).

## Erreurs fréquentes

- Réinitialiser la box en **mode usine** dès le début : vous perdez votre configuration alors qu'un simple redémarrage suffisait.
- Laisser des **DNS manuels** sur un PC portable utilisé ensuite au bureau ou à l'hôtel, ce qui peut bloquer certains réseaux. Repassez en automatique si besoin.
- Oublier de noter la **clé Wi-Fi** avant une réinitialisation réseau. Elle est indiquée sur l'étiquette de la box. Gardez-la dans un gestionnaire de mots de passe, comme expliqué dans notre guide du [mot de passe solide](/comment-creer-un-mot-de-passe-solide/).

## En résumé

- Testez d'abord un autre appareil : **box ou PC ?**
- Solutions rapides : redémarrage, oubli du réseau, dépanneur Windows.
- Solutions intermédiaires : `ipconfig /release` et `/renew`, **DNS 1.1.1.1**, couper VPN et proxy.
- En dernier recours : `netsh winsock reset`, pilote Wi-Fi, **réinitialisation du réseau**.
