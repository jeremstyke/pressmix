# PressMix

Site statique bilingue (FR / EN) hébergé sur GitHub Pages.

- `content/` : les articles en markdown (voir `REDACTION.md`)
- `feeds.json` : les flux RSS des actus du web (titre + lien vers le site d'origine)
- `config.json` : nom du site, URL, catégories
- `build.py` : génère le site dans `docs/`
- `fetch_feeds.py` : met à jour `data/news.json` depuis les flux RSS
- `.github/workflows/build.yml` : toutes les 3 heures et à chaque push, récupère les actus, régénère et publie le site

Réglage GitHub Pages : Settings > Pages > Deploy from a branch > `main` / `/docs`.
