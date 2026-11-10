#!/usr/bin/env python3
"""Récupère les flux RSS/Atom listés dans feeds.json et met à jour data/news.json.
Seuls le titre, la source, la date et le lien sont gardés : le clic renvoie vers le site d'origine.
Usage : python3 fetch_feeds.py [fichier_ou_url_de_test...]
"""
import json, re, sys, html, urllib.request, datetime as dt, xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "news.json"
KEEP_DAYS, MAX_PER_FEED, MAX_TOTAL = 7, 25, 1500
UA = "Mozilla/5.0 (compatible; PressMixBot/1.0; +https://jeremstyke.github.io/pressmix/)"

def text(el, *names):
    for n in names:
        for child in el:
            tag = child.tag.split("}")[-1]
            if tag == n:
                if n == "link" and child.get("href"):
                    if child.get("rel", "alternate") == "alternate": return child.get("href").strip()
                    continue
                if child.text and child.text.strip(): return child.text.strip()
    return ""

def parse_date(s):
    if not s: return None
    try: d = parsedate_to_datetime(s)
    except Exception:
        try: d = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
        except Exception: return None
    return d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)

def clean(s):
    s = html.unescape(re.sub(r"<[^>]+>", "", s or ""))
    return re.sub(r"\s+", " ", s).strip()

def parse(raw):
    root = ET.fromstring(raw)
    items = [e for e in root.iter() if e.tag.split("}")[-1] in ("item", "entry")]
    out = []
    for it in items:
        title = clean(text(it, "title"))
        link = text(it, "link", "guid")
        date = parse_date(text(it, "pubDate", "published", "updated", "date"))
        if title and link.startswith("http"):
            out.append({"title": title[:200], "url": link, "date": (date or dt.datetime.now(dt.timezone.utc)).isoformat()})
    return out

def fetch(url):
    if not url.startswith("http"):
        return Path(url).read_bytes()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/xml, text/xml, */*"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()

def main():
    feeds = json.loads((ROOT / "feeds.json").read_text(encoding="utf-8"))
    old = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else []
    seen = {n["url"]: n for n in old}
    ok = 0
    for f in feeds:
        try:
            items = parse(fetch(f["url"]))[:MAX_PER_FEED]
            for i in items:
                if i["url"] not in seen:
                    seen[i["url"]] = dict(i, source=f["name"], lang=f["lang"], category=f.get("category"), follow=bool(f.get("follow")))
            ok += 1
            print(f"OK  {f['name']}: {len(items)} items")
        except Exception as e:
            print(f"ERR {f['name']}: {e}")
    limit = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=KEEP_DAYS)
    news = [n for n in seen.values() if dt.datetime.fromisoformat(n["date"]) > limit]
    news.sort(key=lambda n: n["date"], reverse=True)
    DATA.parent.mkdir(exist_ok=True)
    DATA.write_text(json.dumps(news[:MAX_TOTAL], ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"{ok}/{len(feeds)} flux OK, {len(news[:MAX_TOTAL])} actus gardées")

if __name__ == "__main__":
    main()
