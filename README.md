<div align="center">

# 📰 PressMix

**L'actualité et les guides pratiques du quotidien, en français et en anglais.**
*News and everyday guides, in French and English.*

[🇫🇷 Lire PressMix](https://jeremstyke.github.io/pressmix/) · [🇬🇧 Read in English](https://jeremstyke.github.io/pressmix/en/) · [✍️ Proposer un article](https://jeremstyke.github.io/pressmix/proposer-un-article/)

</div>

---

## Qu'est-ce que PressMix ?

PressMix est un site d'actualité et de conseils pratiques mis à jour tout au long de la journée. On y trouve au même endroit :

- **📰 Les actus du web** : les derniers titres des grands médias (Le Monde, France 24, BBC, Numerama, TechCrunch, CoinDesk...), rafraîchis toutes les 3 heures. Chaque titre renvoie vers l'article original sur le site de sa source.
- **📝 Les articles PressMix** : des dizaines de nouveaux guides chaque jour, clairs et directs, qui répondent aux questions que tout le monde se pose (budget, smartphone, cuisine, démarches, santé, voyage...).
- **✍️ Les articles des lecteurs** : chacun peut proposer gratuitement son article. Chaque proposition est relue avant publication.

## 15 rubriques

| | | |
|---|---|---|
| 💰 Argent | 💻 Tech | 🪙 Crypto |
| 💼 Business | 🩺 Santé | 🏡 Maison |
| 🍳 Cuisine | ✈️ Voyage | ⚽ Sport |
| 🎮 Jeux vidéo | 👨‍👩‍👧 Famille | 🚗 Auto |
| 🐾 Animaux | 📄 Emploi | 📋 Démarches |

## Ce qui rend PressMix agréable à lire

- ⚡ **Rapide** : des pages légères, sans cookies de suivi.
- 📱 **Pensé pour le mobile** : lisible sur n'importe quel écran.
- 🌍 **Bilingue** : chaque rubrique existe en français et en anglais.
- 🧭 **Facile à parcourir** : sommaire dans chaque article, articles liés, plan du site et flux RSS.

## Publier sur PressMix

Vous avez une expertise à partager ? Proposez votre article gratuitement :

- 🇫🇷 [Proposer un article](https://jeremstyke.github.io/pressmix/proposer-un-article/)
- 🇬🇧 [Submit an article](https://jeremstyke.github.io/pressmix/en/submit-an-article/)

Article original de 600 mots minimum, utile et bien structuré, avec un lien vers votre site.

## Suivre PressMix

- 📡 Flux RSS : [français](https://jeremstyke.github.io/pressmix/rss.xml) · [anglais](https://jeremstyke.github.io/pressmix/en/rss.xml)
- 💬 Contact : [Telegram](https://t.me/jeremstyke?direct)

---

<details>
<summary>🛠️ Fonctionnement technique</summary>

Site statique généré en Python.

- `content/` : les articles (markdown + front matter), voir `REDACTION.md`
- `feeds.json` : les flux RSS des actus du web
- `config.json` : nom du site, adresse, rubriques
- `build.py` : génère le site dans `docs/`
- `fetch_feeds.py` : récupère les actus dans `data/news.json`
- `fetch_submissions.py` : récupère les articles de lecteurs validés
- `.github/workflows/` : toutes les 3 heures et à chaque nouvel article, mise à jour des actus, génération et publication du site

</details>

<div align="center"><sub>© PressMix · by <a href="https://t.me/jeremstyke">@jeremstyke</a></sub></div>
