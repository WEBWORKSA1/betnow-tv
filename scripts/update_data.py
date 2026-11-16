"""Self-updating data pipeline for BetNow.tv (runs in GitHub Actions every 6 hours).

- Fixtures: ESPN public scoreboard JSON (next 7 days) for EPL, LaLiga, UCL, NFL, NBA, NHL, MLB
- Predictions: Poisson goals model (soccer, from live standings) / log5 rating model (US sports, from records)
- News: public RSS feeds from major sports outlets
Writes data/fixtures.json and data/news.json. Never raises: on failure it keeps the previous file.
"""
import json, math, os, re, datetime, urllib.request, html
import xml.etree.ElementTree as ET

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "data")
UA = {"User-Agent": "Mozilla/5.0 (BetNow.tv data bot; +https://betnow.tv)"}
NOW = datetime.datetime.now(datetime.timezone.utc)

LEAGUES = [  # (label, espn sport path, kind, home edge)
    ("Premier League", "soccer/eng.1", "soccer", 0.0),
    ("LaLiga", "soccer/esp.1", "soccer", 0.0),
    ("Champions League", "soccer/uefa.champions", "soccer", 0.0),
    ("NFL", "football/nfl", "us", 0.030),
    ("NBA", "basketball/nba", "us", 0.035),
    ("NHL", "hockey/nhl", "us", 0.025),
    ("MLB", "baseball/mlb", "us", 0.020),
]
NEWS_FEEDS = [
    ("ESPN", "https://www.espn.com/espn/rss/news"),
    ("BBC Sport", "https://feeds.bbci.co.uk/sport/rss.xml"),
    ("CBS Sports", "https://www.cbssports.com/rss/headlines/"),
    ("Yahoo Sports", "https://sports.yahoo.com/rss/"),
    ("Sky Sports", "https://www.skysports.com/rss/12040"),
]


def get(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def getjson(url):
    return json.loads(get(url).decode("utf-8", "replace"))


# ---------------------------------------------------------------- models
def pois(l, k):
    return math.exp(-l) * l ** k / math.factorial(k)


def poisson_probs(lh, la):
    h = d = a = 0.0
    for i in range(11):
        for j in range(11):
            p = pois(lh, i) * pois(la, j)
            if i > j: h += p
            elif i == j: d += p
            else: a += p
    # light Dixon-Coles style draw inflation (Poisson underestimates draws)
    d *= 1.06
    s = h + d + a
    return h / s, d / s, a / s


def log5(pa, pb):
    den = pa + pb - 2 * pa * pb
    return 0.5 if den == 0 else (pa - pa * pb) / den


def parse_record(summary):
    """'10-4' or '8-3-2' -> (wins, games). For soccer W-D-L treat draws as half wins."""
    try:
        parts = [int(x) for x in summary.split("-")]
    except Exception:
        return None
    if len(parts) == 2:
        return parts[0], sum(parts)
    if len(parts) == 3:
        return parts[0] + 0.5 * parts[1], sum(parts)
    return None


def soccer_table(path):
    """team -> (gf_pg, ga_pg) from ESPN standings."""
    out = {}
    try:
        js = getjson(f"https://site.api.espn.com/apis/v2/sports/{path}/standings")
        groups = js.get("children") or [js]
        for g in groups:
            for e in (g.get("standings") or {}).get("entries", []):
                st = {s.get("name"): s.get("value") for s in e.get("stats", [])}
                gp = st.get("gamesPlayed") or 0
                if gp:
                    out[e["team"]["displayName"]] = (st.get("pointsFor", 0) / gp, st.get("pointsAgainst", 0) / gp, gp)
    except Exception as ex:
        print("standings fail", path, ex)
    return out


def predict_soccer(home, away, table):
    avg_h, avg_a = 1.50, 1.18  # long-run top-flight averages (home, away goals)
    lg = sum(v[0] for v in table.values()) / len(table) if table else 1.35
    def strength(team):
        if team not in table:
            return 1.0, 1.0
        gf, ga, gp = table[team]
        w = gp / (gp + 6)  # shrink early-season samples toward average
        return (w * gf / lg + (1 - w)), (w * ga / lg + (1 - w))
    ah, dh = strength(home)
    aa, da = strength(away)
    return poisson_probs(avg_h * ah * da, avg_a * aa * dh)


def predict_us(rec_h, rec_a, edge):
    def wp(rec):
        if not rec:
            return 0.5
        w, g = rec
        return (w + 5 * 0.5) / (g + 10 * 0.5 + 0.0001) if g else 0.5  # regress toward .500
    p = log5(min(max(wp(rec_h), .05), .95), min(max(wp(rec_a), .05), .95)) + edge
    p = min(max(p, 0.03), 0.97)
    return p, 0.0, 1 - p


# ---------------------------------------------------------------- fixtures
def fixtures():
    start = NOW.strftime("%Y%m%d")
    end = (NOW + datetime.timedelta(days=7)).strftime("%Y%m%d")
    matches = []
    for label, path, kind, edge in LEAGUES:
        try:
            js = getjson(f"https://site.api.espn.com/apis/site/v2/sports/{path}/scoreboard?dates={start}-{end}&limit=200")
        except Exception as ex:
            print("scoreboard fail", label, ex)
            continue
        table = soccer_table(path) if kind == "soccer" else {}
        for ev in js.get("events", []):
            try:
                comp = ev["competitions"][0]
                if comp.get("status", {}).get("type", {}).get("completed"):
                    continue
                teams = {c["homeAway"]: c for c in comp["competitors"]}
                h, a = teams["home"], teams["away"]
                hn, an = h["team"]["displayName"], a["team"]["displayName"]
                if kind == "soccer":
                    pH, pD, pA = predict_soccer(hn, an, table)
                else:
                    rh = parse_record((h.get("records") or [{}])[0].get("summary", ""))
                    ra = parse_record((a.get("records") or [{}])[0].get("summary", ""))
                    pH, pD, pA = predict_us(rh, ra, edge)
                matches.append({"id": ev["id"], "league": label, "date": ev["date"], "home": hn, "away": an,
                                "pH": round(pH, 3), "pD": round(pD, 3) if pD else None, "pA": round(pA, 3)})
            except Exception as ex:
                print("event parse fail", label, ex)
        print(label, "ok")
    matches.sort(key=lambda m: m["date"])
    return matches[:240]


# ---------------------------------------------------------------- news
TAG = re.compile(r"<[^>]+>")


def clean(t, n=170):
    t = html.unescape(TAG.sub("", t or "")).strip()
    return (t[:n].rsplit(" ", 1)[0] + "…") if len(t) > n else t


def news():
    items, seen = [], set()
    for src, url in NEWS_FEEDS:
        try:
            root = ET.fromstring(get(url))
        except Exception as ex:
            print("feed fail", src, ex)
            continue
        for it in root.iter("item"):
            title = clean(it.findtext("title"), 140)
            link = (it.findtext("link") or "").strip()
            if not title or not link.startswith("http") or title.lower() in seen:
                continue
            seen.add(title.lower())
            date = it.findtext("pubDate") or ""
            try:
                iso = datetime.datetime.strptime(date[:25].strip(), "%a, %d %b %Y %H:%M:%S").replace(tzinfo=datetime.timezone.utc).isoformat()
            except Exception:
                iso = NOW.isoformat()
            items.append({"title": title, "link": link, "source": src, "summary": clean(it.findtext("description")), "date": iso})
    items.sort(key=lambda x: x["date"], reverse=True)
    return items[:80]


def save(name, payload, key):
    path = os.path.join(DATA, name)
    if not payload[key]:
        print(f"{name}: no fresh data, keeping previous file")
        return
    json.dump(payload, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{name}: {len(payload[key])} rows")


if __name__ == "__main__":
    os.makedirs(DATA, exist_ok=True)
    save("fixtures.json", {"updated": NOW.isoformat(), "matches": fixtures()}, "matches")
    save("news.json", {"updated": NOW.isoformat(), "items": news()}, "items")
