#!/usr/bin/env python3
"""Générateur du site statique bilingue (FR à la racine, EN sous /en/).
- Articles : content/*.md (front matter + markdown), champ lang: fr ou en (fr par défaut)
- Actus du web : data/news.json (rempli par fetch_feeds.py), liens vers les sites d'origine
- Sortie : docs/ (servi par GitHub Pages)
Usage : python3 build.py
"""
import json, math, re, shutil, html, unicodedata, datetime as dt
from pathlib import Path
from email.utils import format_datetime

ROOT = Path(__file__).parent
CFG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
BASE = CFG["base_url"].rstrip("/")
PREFIX = re.sub(r"^https?://[^/]+", "", BASE)
CATS = {c["slug"]: c for c in CFG["categories"]}
OUT = ROOT / "docs"
PER_PAGE = 24
LANGS = ["fr", "en"]
NOW = dt.datetime.now(dt.timezone.utc)

T = {
  "fr": dict(home="Accueil", cat="categorie", news="actus", sitemap="plan-du-site", legal="mentions-legales",
             news_t="Actus du web", news_d="Les dernières actualités des grands sites d'information, mises à jour plusieurs fois par jour.",
             latest="Derniers articles", cats="Catégories", read="min de lecture", pub="Publié le", toc="Sommaire",
             also="À lire aussi en", all="Tous les articles", page="page", soon="Les premiers articles arrivent très bientôt.",
             sitemap_t="Plan du site", legal_t="Mentions légales", all_news="Toutes les actus", more_news="Plus d'actus",
             cat_t="tous nos articles", nf="Page introuvable", nf_d="Cette page n'existe pas ou a été déplacée.", back="Retour à l'accueil",
             ago_min="il y a {} min", ago_h="il y a {} h", ago_d="il y a {} j", ext="Lien externe vers",
             submit="proposer-un-article", submit_t="Proposer un article", by="Par", author_site="Le site de l'auteur"),
  "en": dict(home="Home", cat="category", news="news", sitemap="sitemap", legal="legal",
             news_t="News from the web", news_d="The latest headlines from major news sites, updated several times a day.",
             latest="Latest articles", cats="Categories", read="min read", pub="Published on", toc="Contents",
             also="More in", all="All articles", page="page", soon="The first articles are coming very soon.",
             sitemap_t="Sitemap", legal_t="Legal notice", all_news="All news", more_news="More news",
             cat_t="all our articles", nf="Page not found", nf_d="This page does not exist or has moved.", back="Back to home",
             ago_min="{} min ago", ago_h="{}h ago", ago_d="{}d ago", ext="External link to",
             submit="submit-an-article", submit_t="Submit an article", by="By", author_site="Author's website"),
}
MOIS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]

esc = lambda s: html.escape(str(s), quote=True)
def lp(lang, p=""):  # chemin relatif au site pour une langue
    return (p if lang == "fr" else "en/" + p)
def url(p=""): return (PREFIX + "/" + p).replace("//", "/")
def abs_url(p=""): return BASE + "/" + p
def fdate(d, lang): return f"{d.day} {MOIS[d.month-1]} {d.year}" if lang == "fr" else f"{MONTHS[d.month-1]} {d.day}, {d.year}"
def rtime(w): return max(1, round(w / 220))
def cname(c, lang): return c["name"] if lang == "fr" else c["name_en"]
def cdesc(c, lang): return c["description"] if lang == "fr" else c["description_en"]
def g(key, lang): return CFG[key] if lang == "fr" else CFG[key + "_en"]
def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

# ---------- Markdown minimal ----------
def inline(t, rel="noopener"):
    t = esc(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*(?!\*)(.+?)\*", r"<em>\1</em>", t)
    def link(m):
        txt, href = m.group(1), html.unescape(m.group(2))
        ext = href.startswith("http") and not href.startswith(BASE)
        if href.startswith("/"): href = url(href.lstrip("/"))
        return f'<a href="{esc(href)}"' + (f' rel="{rel}" target="_blank"' if ext else "") + f">{txt}</a>"
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, t)

def md_to_html(md, rel="noopener"):
    il = lambda x: inline(x, rel)
    out, toc, para, lst, tag = [], [], [], [], None
    def flush():
        nonlocal para, lst
        if para: out.append("<p>" + il(" ".join(para)) + "</p>"); para = []
        if lst: out.append(f"<{tag}>" + "".join(f"<li>{il(i)}</li>" for i in lst) + f"</{tag}>"); lst = []
    for line in md.splitlines():
        s = line.strip()
        if not s: flush(); continue
        m = re.match(r"^(#{2,4})\s+(.*)", s)
        if m:
            flush(); lvl, txt = len(m.group(1)), m.group(2); hid = slugify(txt)
            if lvl == 2: toc.append((hid, txt))
            out.append(f'<h{lvl} id="{hid}">{il(txt)}</h{lvl}>'); continue
        m = re.match(r"^[-*]\s+(.*)", s) or re.match(r"^\d+[.)]\s+(.*)", s)
        if m:
            t2 = "ol" if s[0].isdigit() else "ul"
            if para or (lst and t2 != tag): flush()
            tag = t2; lst.append(m.group(1)); continue
        if s.startswith(">"): flush(); out.append("<blockquote>" + il(s.lstrip("> ")) + "</blockquote>"); continue
        if lst: flush()
        para.append(s)
    flush()
    return "\n".join(out), toc

# ---------- Données ----------
def load_articles():
    arts = []
    for f in sorted((ROOT / "content").glob("*.md")):
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", f.read_text(encoding="utf-8"), re.S)
        if not m: print("ignoré (pas de front matter):", f.name); continue
        meta = {}
        for l in m.group(1).splitlines():
            if ":" in l: k, v = l.split(":", 1); meta[k.strip()] = v.strip().strip('"')
        if meta.get("category") not in CATS: print("ignoré (catégorie inconnue):", f.name); continue
        lang = meta.get("lang", "fr")
        if lang not in LANGS: print("ignoré (langue):", f.name); continue
        body, toc = md_to_html(m.group(2))
        date = dt.datetime.fromisoformat(meta["date"])
        if date.tzinfo is None: date = date.replace(tzinfo=dt.timezone.utc)
        if date > NOW: continue  # programmé pour plus tard
        upd = dt.datetime.fromisoformat(meta.get("updated", meta["date"]))
        if upd.tzinfo is None: upd = upd.replace(tzinfo=dt.timezone.utc)
        arts.append(dict(meta, lang=lang, slug=f.stem, body=body, toc=toc, date=date, updated=upd,
                         words=len(re.findall(r"\w+", m.group(2))),
                         tags=[t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
                         path=lp(lang, f.stem + "/")))
    # Articles proposés par les visiteurs et validés
    sp = ROOT / "data" / "submissions.json"
    for s in (json.loads(sp.read_text(encoding="utf-8")) if sp.exists() else []):
        if s.get("category") not in CATS or s.get("lang") not in LANGS: continue
        slug = slugify(s["title"])[:70].strip("-") + f"-{s['id']}"
        body, toc = md_to_html(s["content"], CFG.get("submission_link_rel", "noopener"))
        date = dt.datetime.fromisoformat(s["approved_at"].replace("Z", "+00:00"))
        plain = re.sub(r"\s+", " ", re.sub(r"[#*>\[\]]|\(https?://[^)]*\)", "", s["content"])).strip()
        arts.append(dict(title=s["title"], description=(s.get("description") or plain[:155].rsplit(" ", 1)[0] + "..."),
                         category=s["category"], lang=s["lang"], slug=slug, body=body, toc=toc, date=date, updated=date,
                         words=len(re.findall(r"\w+", s["content"])), tags=[], path=lp(s["lang"], slug + "/"),
                         author=s.get("name"), author_url=s.get("target_url"), anchor=s.get("anchor")))
    arts.sort(key=lambda a: a["date"], reverse=True)
    return arts

def load_news():
    p = ROOT / "data" / "news.json"
    news = json.loads(p.read_text(encoding="utf-8")) if p.exists() else []
    for n in news: n["dt"] = dt.datetime.fromisoformat(n["date"])
    return [n for n in news if n["dt"] <= NOW + dt.timedelta(hours=1)]

def ago(d, lang):
    s = max(0, (NOW - d).total_seconds())
    if s < 3600: return T[lang]["ago_min"].format(max(1, int(s // 60)))
    if s < 86400: return T[lang]["ago_h"].format(int(s // 3600))
    return T[lang]["ago_d"].format(int(s // 86400))

# ---------- Gabarit ----------
CSS = """:root{--ink:#17191e;--mut:#5f6570;--line:#e7e4dd;--bg:#fbfaf7;--card:#fff;--acc:#d9481f;--lnk:#1f4fd8;--soft:#f2eee6}
*{box-sizing:border-box;margin:0;padding:0}body{font:17px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink)}
a{color:inherit;text-decoration:none}.w{max-width:1100px;margin:0 auto;padding:0 18px}
header{border-bottom:1px solid var(--line)}.top{display:flex;align-items:center;justify-content:space-between;height:62px;gap:10px}
.logo{font:800 24px Georgia,serif;letter-spacing:-.5px;white-space:nowrap}.logo b{color:var(--acc)}
.tl{display:flex;gap:6px;align-items:center;font-size:14px}.tl a{padding:6px 10px;border-radius:8px;color:var(--mut)}.tl a:hover,.tl a.on{background:var(--soft);color:var(--ink)}
nav.cats{display:flex;gap:6px;overflow-x:auto;padding:10px 0 12px;scrollbar-width:none}nav.cats::-webkit-scrollbar{display:none}
nav.cats a{white-space:nowrap;padding:5px 13px;border:1px solid var(--line);border-radius:99px;font-size:14px;color:var(--mut);background:var(--card)}
nav.cats a:hover,nav.cats a.on{border-color:var(--ink);color:var(--ink)}
h1,h2,h3{font-family:Georgia,"Times New Roman",serif;line-height:1.2;letter-spacing:-.3px}
.hero{padding:36px 0 6px}.hero h1{font-size:clamp(28px,4.5vw,44px)}.hero p{color:var(--mut);margin-top:8px}
.sec{margin:34px 0 14px;font-size:24px;display:flex;justify-content:space-between;align-items:baseline;gap:10px}.sec a{font:600 14px sans-serif;color:var(--lnk)}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px;display:flex;flex-direction:column;gap:6px}
.card:hover{border-color:var(--ink)}.card h2,.card h3{font-size:19px}.card p{color:var(--mut);font-size:15px}
.tag{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:var(--acc)}
.meta{font-size:13px;color:var(--mut);margin-top:auto}
.news{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:6px 18px}
.news li{list-style:none;padding:11px 0;border-bottom:1px solid var(--line);display:flex;gap:10px;align-items:baseline}.news li:last-child{border:0}
.news a{font-weight:600;flex:1}.news a:hover{color:var(--lnk)}.news small{color:var(--mut);white-space:nowrap;font-size:13px}
.catgrid{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}.catgrid a{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;text-align:center;font-weight:600}
.catgrid a:hover{border-color:var(--ink)}.catgrid span{display:block;font-size:24px}
.crumbs{font-size:14px;color:var(--mut);margin:24px 0 8px}.crumbs a:hover{color:var(--ink)}
article{max-width:740px;margin:0 auto 20px}article h1{font-size:clamp(28px,4.5vw,42px);margin:6px 0 10px}
.lead{font-size:19px;color:var(--mut);margin-bottom:14px}
.toc{background:var(--soft);border-radius:12px;padding:16px 20px;margin:22px 0}.toc strong{display:block;margin-bottom:6px}.toc ol{padding-left:20px}.toc a{color:var(--lnk)}
.body h2{font-size:27px;margin:34px 0 12px}.body h3{font-size:21px;margin:24px 0 8px}.body p{margin:0 0 18px}.body ul,.body ol{margin:0 0 18px 22px}.body li{margin-bottom:6px}
.body a{color:var(--lnk);text-decoration:underline}.body blockquote{border-left:4px solid var(--acc);padding:4px 16px;margin:0 0 18px;color:var(--mut)}
.tags{margin:24px 0;display:flex;flex-wrap:wrap;gap:6px}.tags span{background:var(--soft);border-radius:6px;padding:2px 10px;font-size:13px;color:var(--mut)}
.pag{display:flex;gap:8px;justify-content:center;margin:30px 0}.pag a,.pag span{padding:8px 14px;border:1px solid var(--line);border-radius:8px;background:var(--card)}.pag span{background:var(--ink);color:#fff}
footer{border-top:1px solid var(--line);margin-top:50px;padding:26px 0;color:var(--mut);font-size:14px}footer .w{display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}footer a:hover{color:var(--ink)}
@media(max-width:560px){.tl .sub span{display:none}}
@media(max-width:820px){.grid{grid-template-columns:1fr}.catgrid{grid-template-columns:repeat(2,1fr)}.news li{flex-direction:column;gap:2px}}"""

def page(lang, title, desc, path, content, active=None, extra="", og="website", noindex=False, alt=None):
    t, site = T[lang], g("site_name", lang)
    full = title if site in title else f"{title} | {site}"
    nav = f'<a href="{url(lp(lang))}" class="{"on" if active is None else ""}">{t["home"]}</a>' + \
          f'<a href="{url(lp(lang, t["news"] + "/"))}" class="{"on" if active == "news" else ""}">📰 {t["news_t"]}</a>' + "".join(
          f'<a href="{url(lp(lang, t["cat"] + "/" + s + "/"))}" class="{"on" if active == s else ""}">{c["emoji"]} {esc(cname(c, lang))}</a>' for s, c in CATS.items())
    other = "en" if lang == "fr" else "fr"
    alt = alt or {}
    hreflang = "".join(f'<link rel="alternate" hreflang="{l}" href="{abs_url(p)}">' for l, p in alt.items())
    if "fr" in alt: hreflang += f'<link rel="alternate" hreflang="x-default" href="{abs_url(alt["fr"])}">'
    switch = url(alt.get(other, lp(other)))
    robots = "noindex,follow" if noindex else "index,follow,max-image-preview:large"
    gsc = f'<meta name="google-site-verification" content="{esc(CFG["google_verification"])}">' if CFG.get("google_verification") else ""
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(full)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{abs_url(path)}">
<meta name="robots" content="{robots}">{gsc}{hreflang}
<meta property="og:site_name" content="{esc(site)}"><meta property="og:locale" content="{'fr_FR' if lang == 'fr' else 'en_US'}">
<meta property="og:type" content="{og}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{abs_url(path)}">
<meta name="twitter:card" content="summary">
<link rel="alternate" type="application/rss+xml" title="{esc(site)}" href="{abs_url(lp(lang, 'rss.xml'))}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>📰</text></svg>">
<style>{CSS}</style>
{extra}
</head>
<body>
<header><div class="w"><div class="top"><a class="logo" href="{url(lp(lang))}">{g("logo_html", lang)}</a>
<div class="tl"><a href="{url(lp(lang, t['submit'] + '/'))}" class="sub {'on' if active == 'submit' else ''}" title="{t['submit_t']}">✍️ <span>{t['submit_t']}</span></a><a href="{url(path) if lang == 'fr' else switch}" class="{'on' if lang == 'fr' else ''}" hreflang="fr">FR</a><a href="{url(path) if lang == 'en' else switch}" class="{'on' if lang == 'en' else ''}" hreflang="en">EN</a></div></div>
<nav class="cats">{nav}</nav></div></header>
<main class="w">
{content}
</main>
<footer><div class="w"><div>© {NOW.year} {esc(site)}</div><div><a href="{url(lp(lang, t['submit'] + '/'))}">{t['submit_t']}</a> · <a href="{url(lp(lang, t['sitemap'] + '/'))}">{t['sitemap_t']}</a> · <a href="{url(lp(lang, t['legal'] + '/'))}">{t['legal_t']}</a> · <a href="{abs_url(lp(lang, 'rss.xml'))}">RSS</a></div></div></footer>
</body>
</html>"""

def card(a, h="h3"):
    c, t = CATS[a["category"]], T[a["lang"]]
    return f"""<a class="card" href="{url(a['path'])}"><span class="tag">{c['emoji']} {esc(cname(c, a['lang']))}</span>
<{h}>{esc(a['title'])}</{h}><p>{esc(a['description'])}</p><span class="meta">{fdate(a['date'], a['lang'])} · {rtime(a['words'])} {t['read']}</span></a>"""

def news_list(items, lang):
    t = T[lang]
    return '<ul class="news">' + "".join(
        f'<li><a href="{esc(n["url"])}" target="_blank" rel="nofollow noopener" title="{t["ext"]} {esc(n["source"])}">{esc(n["title"])}</a>'
        f'<small>{esc(n["source"])} · {ago(n["dt"], lang)}</small></li>' for n in items) + "</ul>"

def author_box(a, lang):
    if not a.get("author"): return ""
    link = ""
    if a.get("author_url"):
        rel = CFG.get("submission_link_rel", "noopener")
        link = f' · <a href="{esc(a["author_url"])}" target="_blank" rel="{rel}">{esc(a.get("anchor") or T[lang]["author_site"])}</a>'
    return f'<p class="meta" style="margin-top:26px;padding:14px;background:var(--soft);border-radius:10px">✍️ {T[lang]["by"]} <strong>{esc(a["author"])}</strong>{link}</p>'

ld = lambda o: '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False) + "</script>"

def write(path, content):
    p = OUT / path if path.endswith((".xml", ".html", ".txt")) else OUT / path / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

def pager(cur, total, base):
    if total <= 1: return ""
    link = lambda n: url(base + ("" if n == 1 else f"page/{n}/"))
    return '<nav class="pag">' + "".join(f"<span>{n}</span>" if n == cur else f'<a href="{link(n)}">{n}</a>'
        for n in range(1, total + 1) if n in (1, total) or abs(n - cur) <= 2) + "</nav>"

# ---------- Proposer un article ----------
SUBMIT_TXT = {
  "fr": dict(lead="Publiez gratuitement votre article sur Le Mag Utile. Chaque proposition est relue avant publication.",
    rules=["Article original, jamais publié ailleurs, en français", "600 mots minimum, utile et bien structuré", "Sous-titres avec ## et listes avec - (format markdown)",
           "Un lien vers votre site autorisé", "Refusés : contenu copié, adulte, jeux d'argent, arnaques, armes, contenu haineux"],
    name="Votre nom (affiché sous l'article)", email="Votre email (jamais affiché)", cat="Catégorie", choose="Choisir...", title="Titre de l'article",
    desc="Résumé en une phrase (facultatif)", content="Votre article", ph="Écrivez votre article ici.\n\n## Un sous-titre\n\nUn paragraphe...\n\n- une liste\n- de points",
    url="Votre site (facultatif)", anchor="Texte du lien vers votre site (facultatif)", words="mots", min="minimum 600 recommandé",
    send="Envoyer pour relecture", ok="✅ Merci ! Votre article a bien été reçu. Il sera publié après relecture.",
    err="Envoi impossible. Vérifiez que l'article fait au moins 1 500 caractères et que le lien commence par https://", free="100 % gratuit"),
  "en": dict(lead="Publish your article on The Useful Mag for free. Every submission is reviewed before publishing.",
    rules=["Original article, never published elsewhere, in English", "At least 600 words, useful and well structured", "Subheadings with ## and lists with - (markdown format)",
           "One link to your website allowed", "Rejected: copied, adult, gambling, scam, weapons or hateful content"],
    name="Your name (shown under the article)", email="Your email (never shown)", cat="Category", choose="Choose...", title="Article title",
    desc="One-sentence summary (optional)", content="Your article", ph="Write your article here.\n\n## A subheading\n\nA paragraph...\n\n- a list\n- of points",
    url="Your website (optional)", anchor="Link text to your website (optional)", words="words", min="600 minimum recommended",
    send="Send for review", ok="✅ Thank you! Your article was received. It will be published after review.",
    err="Could not send. Make sure the article has at least 1,500 characters and the link starts with https://", free="100% free"),
}

def submit_html(lang):
    s, t = SUBMIT_TXT[lang], T[lang]
    opts = "".join(f'<option value="{k}">{c["emoji"]} {esc(cname(c, lang))}</option>' for k, c in CATS.items())
    return f"""<p class="crumbs"><a href="{url(lp(lang))}">{t['home']}</a> › {t['submit_t']}</p>
<article><h1>✍️ {t['submit_t']}</h1><p class="lead">{s['lead']} <strong>{s['free']}</strong>.</p>
<div class="toc"><ul style="padding-left:18px">{"".join(f"<li>{r}</li>" for r in s['rules'])}</ul></div>
<form id="f" class="sf">
<label>{s['name']}<input name="name" required maxlength="100"></label>
<label>{s['email']}<input name="email" type="email" required maxlength="200"></label>
<label>{s['cat']}<select name="category" required><option value="">{s['choose']}</option>{opts}</select></label>
<label>{s['title']}<input name="title" required minlength="10" maxlength="200"></label>
<label>{s['desc']}<input name="description" maxlength="300"></label>
<label>{s['content']}<textarea name="content" required minlength="1500" maxlength="30000" rows="18" placeholder="{esc(s['ph'])}"></textarea></label>
<p class="meta"><span id="wc">0</span> {s['words']} · {s['min']}</p>
<label>{s['url']}<input name="target_url" type="url" placeholder="https://" maxlength="300"></label>
<label>{s['anchor']}<input name="anchor" maxlength="100"></label>
<input name="website" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
<button id="sb" type="submit">{s['send']}</button>
<div id="out"></div>
</form></article>
<style>.sf label{{display:block;font-weight:600;font-size:15px;margin:14px 0 0}}.sf input,.sf select,.sf textarea{{display:block;width:100%;margin-top:6px;padding:11px;border:1px solid var(--line);border-radius:10px;font:inherit;font-weight:400;background:#fff}}
.sf button{{margin-top:20px;background:var(--acc);color:#fff;border:0;border-radius:10px;padding:13px 22px;font:600 16px sans-serif;cursor:pointer}}.sf button:disabled{{opacity:.5}}
.msg{{margin-top:14px;padding:13px;border-radius:10px}}.ok{{background:#e6f5ea;color:#1d6b35}}.ko{{background:#fde8e4;color:#a3341a}}</style>
<script>
const f=document.getElementById('f'),sb=document.getElementById('sb'),out=document.getElementById('out');
f.content.addEventListener('input',()=>document.getElementById('wc').textContent=f.content.value.trim().split(/\\s+/).filter(Boolean).length);
f.addEventListener('submit',async e=>{{e.preventDefault();if(f.website.value)return;
const d=Object.fromEntries(new FormData(f));delete d.website;d.lang='{lang}';d.email=d.email.trim().toLowerCase();
for(const k of ['description','target_url','anchor'])d[k]=(d[k]||'').trim()||null;
sb.disabled=true;
try{{const r=await fetch('{CFG["supabase_url"]}/rest/v1/lp_submissions',{{method:'POST',headers:{{apikey:'{CFG["supabase_key"]}',Authorization:'Bearer {CFG["supabase_key"]}','Content-Type':'application/json',Prefer:'return=minimal'}},body:JSON.stringify(d)}});
if(!r.ok)throw 0;f.reset();out.innerHTML='<div class="msg ok">{s["ok"]}</div>';}}
catch(_){{out.innerHTML='<div class="msg ko">{esc(s["err"])}</div>';}}sb.disabled=false;}});
</script>"""

ADMIN_HTML = """<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Validation des articles</title>
<style>body{font:16px/1.6 -apple-system,Segoe UI,Roboto,sans-serif;margin:0;background:#fbfaf7;color:#17191e}.w{max-width:820px;margin:0 auto;padding:16px}
h1{font-size:22px}.tabs{display:flex;gap:6px;margin:12px 0}.tabs button{border:1px solid #ddd;background:#fff;border-radius:99px;padding:6px 14px;cursor:pointer}.tabs .on{background:#17191e;color:#fff}
.it{background:#fff;border:1px solid #e7e4dd;border-radius:12px;padding:14px;margin-bottom:12px}.it h2{font-size:18px;margin:0 0 4px}.m{color:#5f6570;font-size:14px}
pre{white-space:pre-wrap;font:15px/1.6 inherit;background:#f2eee6;padding:12px;border-radius:8px;max-height:420px;overflow:auto}
.b{display:flex;gap:8px;margin-top:10px}.b button{flex:1;border:0;border-radius:8px;padding:11px;font-weight:600;cursor:pointer;color:#fff}.ok{background:#1d8a45}.no{background:#c0392b}.re{background:#888}</style></head>
<body><div class="w"><h1>✍️ Articles proposés</h1><div class="tabs"><button data-s="pending" class="on">En attente</button><button data-s="approved">Publiés</button><button data-s="rejected">Refusés</button></div><div id="l">Chargement...</div></div>
<script>
const SB='__SB_URL__',K='__SB_KEY__',CATS=__CATS__;
let key=location.hash.slice(1);try{if(key)localStorage.setItem('mag_admin',key);else key=localStorage.getItem('mag_admin')||'';}catch(e){}
history.replaceState(null,'',location.pathname);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const rpc=(fn,b)=>fetch(SB+'/rest/v1/rpc/'+fn,{method:'POST',headers:{apikey:K,Authorization:'Bearer '+K,'Content-Type':'application/json'},body:JSON.stringify(b)}).then(r=>{if(!r.ok)throw r;return r.text()}).then(t=>t?JSON.parse(t):null);
let st='pending';
async function load(){const l=document.getElementById('l');l.textContent='Chargement...';
try{const rows=await rpc('lp_admin_list',{p_key:key,p_status:st});
l.innerHTML=rows.length?rows.map(r=>`<div class="it"><h2>${r.lang=='en'?'🇬🇧':'🇫🇷'} ${esc(r.title)}</h2>
<div class="m">${esc(CATS[r.category]||r.category)} · ${esc(r.name)} (${esc(r.email)}) · ${r.content.trim().split(/\\s+/).length} mots · ${new Date(r.created_at).toLocaleString('fr-FR')}</div>
${r.target_url?`<div class="m">Lien : <a href="${esc(r.target_url)}" target="_blank" rel="noopener">${esc(r.anchor||r.target_url)}</a> (${esc(r.target_url)})</div>`:''}
${r.description?`<p><em>${esc(r.description)}</em></p>`:''}<details><summary>Lire l'article</summary><pre>${esc(r.content)}</pre></details>
<div class="b">${st!='approved'?`<button class="ok" onclick="setS(${r.id},'approved')">✅ Valider</button>`:''}${st!='rejected'?`<button class="no" onclick="setS(${r.id},'rejected')">❌ Refuser</button>`:''}${st!='pending'?`<button class="re" onclick="setS(${r.id},'pending')">↩️ En attente</button>`:''}</div></div>`).join(''):'<p class="m">Rien ici.</p>';}
catch(e){l.innerHTML='<p>Accès refusé. Ouvre le lien admin complet (avec la clé après le #).</p>';}}
async function setS(id,s){await rpc('lp_admin_set',{p_key:key,p_id:id,p_status:s});load();}
document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{document.querySelectorAll('.tabs button').forEach(x=>x.classList.remove('on'));b.classList.add('on');st=b.dataset.s;load();});
load();
</script></body></html>"""

# ---------- Build ----------
def build():
    all_arts, all_news = load_articles(), load_news()
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / ".nojekyll").write_text("")
    if CFG.get("custom_domain"): (OUT / "CNAME").write_text(CFG["custom_domain"])
    sitemap = []
    by_slug = {a["slug"]: a for a in all_arts}
    both = lambda f: {l: f(l) for l in LANGS}  # chemins alternés FR/EN

    for lang in LANGS:
        t, site = T[lang], g("site_name", lang)
        arts = [a for a in all_arts if a["lang"] == lang]
        news = [n for n in all_news if n["lang"] == lang]
        org = {"@type": "Organization", "name": site, "url": abs_url(lp(lang))}

        # Articles
        for a in arts:
            c = CATS[a["category"]]
            same = [x for x in arts if x["category"] == a["category"] and x["slug"] != a["slug"]]
            rel = sorted(same, key=lambda x: (-len(set(x["tags"]) & set(a["tags"])), -x["date"].timestamp()))[:6]
            alt = {lang: a["path"]}
            tr = by_slug.get(a.get("translation", ""))
            if tr and tr["lang"] != lang: alt[tr["lang"]] = tr["path"]
            toc = ('<nav class="toc"><strong>' + t["toc"] + "</strong><ol>" + "".join(f'<li><a href="#{i}">{inline(x)}</a></li>' for i, x in a["toc"]) + "</ol></nav>") if len(a["toc"]) >= 3 else ""
            cat_path = lp(lang, t["cat"] + "/" + a["category"] + "/")
            schema = ld({"@context": "https://schema.org", "@graph": [
                {"@type": "Article", "headline": a["title"], "description": a["description"], "datePublished": a["date"].isoformat(),
                 "dateModified": a["updated"].isoformat(), "author": ({"@type": "Person", "name": a["author"]} if a.get("author") else org), "publisher": org, "mainEntityOfPage": abs_url(a["path"]),
                 "articleSection": cname(c, lang), "keywords": ", ".join(a["tags"]), "wordCount": a["words"], "inLanguage": lang},
                {"@type": "BreadcrumbList", "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": t["home"], "item": abs_url(lp(lang))},
                    {"@type": "ListItem", "position": 2, "name": cname(c, lang), "item": abs_url(cat_path)},
                    {"@type": "ListItem", "position": 3, "name": a["title"]}]}]})
            extra = schema + f'<meta property="article:published_time" content="{a["date"].isoformat()}">'
            cat_news = [n for n in news if n.get("category") == a["category"]][:5]
            body = f"""<p class="crumbs"><a href="{url(lp(lang))}">{t['home']}</a> › <a href="{url(cat_path)}">{esc(cname(c, lang))}</a></p>
<article><span class="tag">{c['emoji']} {esc(cname(c, lang))}</span><h1>{esc(a['title'])}</h1><p class="lead">{esc(a['description'])}</p>
<p class="meta">{(t['by'] + ' ' + esc(a['author']) + ' · ') if a.get('author') else ''}{t['pub']} <time datetime="{a['date'].date()}">{fdate(a['date'], lang)}</time> · {rtime(a['words'])} {t['read']}</p>
{toc}<div class="body">{a['body']}{author_box(a, lang)}</div>
{('<div class="tags">' + "".join(f"<span>{esc(x)}</span>" for x in a["tags"]) + "</div>") if a["tags"] else ""}</article>
{(f'<h2 class="sec">{t["also"]} {esc(cname(c, lang))}</h2><div class="grid">' + "".join(card(x) for x in rel) + "</div>") if rel else ""}
{(f'<h2 class="sec">{t["news_t"]}</h2>' + news_list(cat_news, lang)) if cat_news else ""}"""
            write(a["path"], page(lang, a.get("seo_title") or a["title"], a["description"], a["path"], body, a["category"], extra, "article", alt=alt))
            sitemap.append((abs_url(a["path"]), a["updated"], alt))

        # Catégories
        for s, c in CATS.items():
            lst = [a for a in arts if a["category"] == s]
            cnews = [n for n in news if n.get("category") == s][:8]
            pages = max(1, math.ceil(len(lst) / PER_PAGE))
            for n in range(1, pages + 1):
                chunk = lst[(n - 1) * PER_PAGE: n * PER_PAGE]
                base = lp(lang, t["cat"] + "/" + s + "/")
                p = base + ("" if n == 1 else f"page/{n}/")
                alt = both(lambda l: lp(l, T[l]["cat"] + "/" + s + "/")) if n == 1 else {lang: p}
                body = f"""<p class="crumbs"><a href="{url(lp(lang))}">{t['home']}</a> › {esc(cname(c, lang))}</p>
<section class="hero"><h1>{c['emoji']} {esc(cname(c, lang))}</h1><p>{esc(cdesc(c, lang))}</p></section>
{('<div class="grid" style="margin-top:22px">' + "".join(card(a, "h2") for a in chunk) + "</div>") if chunk else f'<p style="color:var(--mut);margin:24px 0">{t["soon"]}</p>'}
{pager(n, pages, base)}
{(f'<h2 class="sec">{t["news_t"]} : {esc(cname(c, lang))}</h2>' + news_list(cnews, lang)) if cnews and n == 1 else ""}"""
                title = f"{cname(c, lang)} : {t['cat_t']}" + ("" if n == 1 else f" ({t['page']} {n})")
                indexable = bool(chunk)
                write(p, page(lang, title, cdesc(c, lang), p, body, s, noindex=not indexable, alt=alt))
                if indexable: sitemap.append((abs_url(p), chunk[0]["updated"], alt))

        # Actus du web
        npath = lp(lang, t["news"] + "/")
        pages = max(1, math.ceil(len(news) / 60))
        for n in range(1, pages + 1):
            p = npath + ("" if n == 1 else f"page/{n}/")
            body = f"""<p class="crumbs"><a href="{url(lp(lang))}">{t['home']}</a> › {t['news_t']}</p>
<section class="hero"><h1>📰 {t['news_t']}</h1><p>{t['news_d']}</p></section><div style="margin-top:22px">{news_list(news[(n-1)*60:n*60], lang)}</div>{pager(n, pages, npath)}"""
            write(p, page(lang, t["news_t"] + ("" if n == 1 else f" ({t['page']} {n})"), t["news_d"], p, body, "news",
                          noindex=n > 1, alt=both(lambda l: lp(l, T[l]["news"] + "/")) if n == 1 else {lang: p}))
        sitemap.append((abs_url(npath), NOW, both(lambda l: lp(l, T[l]["news"] + "/"))))

        # Accueil
        pages = max(1, math.ceil(len(arts) / PER_PAGE))
        for n in range(1, pages + 1):
            chunk = arts[(n - 1) * PER_PAGE: n * PER_PAGE]
            p = lp(lang, "" if n == 1 else f"page/{n}/")
            top = ""
            if n == 1:
                top = f"""<section class="hero"><h1>{esc(g('tagline', lang))}</h1><p>{esc(g('description', lang))}</p></section>
{(f'<h2 class="sec">{t["news_t"]}<a href="{url(npath)}">{t["all_news"]} →</a></h2>' + news_list(news[:10], lang)) if news else ""}
<h2 class="sec">{t['cats']}</h2><div class="catgrid">{"".join(f'<a href="{url(lp(lang, t["cat"] + "/" + s + "/"))}"><span>{c["emoji"]}</span>{esc(cname(c, lang))}</a>' for s, c in CATS.items())}</div>
<h2 class="sec">{t['latest']}</h2>"""
            body = top + ('<div class="grid">' + "".join(card(a) for a in chunk) + "</div>" if chunk else f'<p style="color:var(--mut)">{t["soon"]}</p>') + pager(n, pages, lp(lang))
            ws = ld({"@context": "https://schema.org", "@type": "WebSite", "name": site, "url": abs_url(lp(lang)), "inLanguage": lang}) if n == 1 else ""
            write(p or ".", page(lang, f"{site} : {g('tagline', lang)}" if n == 1 else f"{t['all']} ({t['page']} {n})", g("description", lang), p, body,
                                 None, ws, alt=both(lambda l: lp(l)) if n == 1 else {lang: p}))
        sitemap.append((abs_url(lp(lang)), arts[0]["updated"] if arts else NOW, both(lambda l: lp(l))))

        # Plan du site
        sp = lp(lang, t["sitemap"] + "/")
        sm = f'<p class="crumbs"><a href="{url(lp(lang))}">{t["home"]}</a> › {t["sitemap_t"]}</p><h1 style="margin:10px 0 10px">{t["sitemap_t"]}</h1>'
        for s, c in CATS.items():
            lst = [a for a in arts if a["category"] == s]
            if lst:
                sm += f'<h2 class="sec">{c["emoji"]} <a href="{url(lp(lang, t["cat"] + "/" + s + "/"))}" style="font:inherit;color:inherit">{esc(cname(c, lang))}</a></h2><ul style="margin-left:20px">' + \
                      "".join(f'<li><a href="{url(a["path"])}">{esc(a["title"])}</a></li>' for a in lst) + "</ul>"
        write(sp, page(lang, t["sitemap_t"], t["sitemap_t"] + " : " + site, sp, sm, alt=both(lambda l: lp(l, T[l]["sitemap"] + "/"))))

        # Mentions légales
        lg = lp(lang, t["legal"] + "/")
        if lang == "fr":
            txt = f"""<p><strong>Éditeur :</strong> {esc(CFG['publisher'])}</p><p><strong>Contact :</strong> <a href="{esc(CFG['contact_url'])}">{esc(CFG['contact_url'])}</a></p>
<p><strong>Hébergement :</strong> GitHub Pages, GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.</p>
<p>Les articles sont fournis à titre informatif et ne remplacent pas l'avis d'un professionnel (médecin, conseiller financier, avocat).</p>
<p>La rubrique « Actus du web » affiche uniquement les titres publiés dans les flux RSS publics des sites cités ; chaque lien renvoie vers l'article original sur le site de sa source.</p>
<p>Ce site n'utilise pas de cookies de suivi.</p>"""
        else:
            txt = f"""<p><strong>Publisher:</strong> {esc(CFG['publisher'])}</p><p><strong>Contact:</strong> <a href="{esc(CFG['contact_url'])}">{esc(CFG['contact_url'])}</a></p>
<p><strong>Hosting:</strong> GitHub Pages, GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA.</p>
<p>Articles are for information only and are not a substitute for professional advice (doctor, financial adviser, lawyer).</p>
<p>The "News from the web" section only shows headlines from the public RSS feeds of the listed sites; every link leads to the original article on its source site.</p>
<p>This site does not use tracking cookies.</p>"""
        write(lg, page(lang, t["legal_t"], t["legal_t"] + " : " + site, lg, f'<article><h1 style="margin:30px 0 16px">{t["legal_t"]}</h1><div class="body">{txt}</div></article>', noindex=True))

        # RSS
        items = "".join(f"""<item><title>{esc(a['title'])}</title><link>{abs_url(a['path'])}</link><guid>{abs_url(a['path'])}</guid><pubDate>{format_datetime(a['date'])}</pubDate><category>{esc(cname(CATS[a['category']], lang))}</category><description>{esc(a['description'])}</description></item>\n""" for a in arts[:50])
        write(lp(lang, "rss.xml"), f"""<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>{esc(site)}</title><link>{abs_url(lp(lang))}</link><description>{esc(g('description', lang))}</description><language>{lang}</language>\n{items}</channel></rss>\n""")

        # Proposer un article
        sub = lp(lang, t["submit"] + "/")
        write(sub, page(lang, t["submit_t"], SUBMIT_TXT[lang]["lead"], sub, submit_html(lang), "submit",
                        alt=both(lambda l: lp(l, T[l]["submit"] + "/"))))
        sitemap.append((abs_url(sub), NOW, both(lambda l: lp(l, T[l]["submit"] + "/"))))

    # Admin (validation des articles proposés)
    write("admin/index.html", ADMIN_HTML.replace("__SB_URL__", CFG["supabase_url"]).replace("__SB_KEY__", CFG["supabase_key"])
          .replace("__CATS__", json.dumps({s: c["name"] for s, c in CATS.items()}, ensure_ascii=False)))

    # 404
    write("404.html", page("fr", T["fr"]["nf"], T["fr"]["nf_d"], "404.html",
        f'<section class="hero"><h1>{T["fr"]["nf"]}</h1><p>{T["fr"]["nf_d"]} <a href="{url()}" style="text-decoration:underline">{T["fr"]["back"]}</a></p></section>', noindex=True))

    # sitemap.xml + robots.txt
    sx = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    for u, d, alt in sitemap:
        links = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{esc(abs_url(p))}"/>' for l, p in alt.items()) if len(alt) > 1 else ""
        sx += f"<url><loc>{esc(u)}</loc><lastmod>{d.date()}</lastmod>{links}</url>\n"
    write("sitemap.xml", sx + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /admin/\n\nSitemap: {abs_url('sitemap.xml')}\n")
    print(f"OK : {sum(a['lang']=='fr' for a in all_arts)} articles FR, {sum(a['lang']=='en' for a in all_arts)} articles EN, {len(all_news)} actus, {len(sitemap)} URLs dans le sitemap")

if __name__ == "__main__":
    build()
