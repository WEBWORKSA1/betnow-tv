"""Build every static page of BetNow.tv.  Run: python3 scripts/build.py"""
import os, sys, datetime, json
sys.path.insert(0, os.path.dirname(__file__))
from layout import page, hero, DOMAIN, INQUIRY  # noqa
from blocks import LEAD_QUIZ, video_grid, form, NAME_EMAIL, CHANNELS
from articles import ARTICLES

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TODAY = datetime.date.today().isoformat()
PAGES = []


def w(path, html, prio="0.7"):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(html)
    PAGES.append((path, prio))


def learn_cards(p="", n=None):
    items = ARTICLES[:n] if n else ARTICLES
    return '<div class="grid g3" id="learnGrid">' + "".join(
        f'<article class="card"><span class="tag lime">{a["tag"]}</span><h3 class="mt"><a href="{p}learn/{a["slug"]}.html" style="color:var(--text)">{a["title"]}</a></h3><p>{a["desc"]}</p><span class="muted" style="font-size:.85rem">{a["min"]} min read</span></article>'
        for a in items) + "</div>"


FAQ = [
    ("Is BetNow.tv a betting site?", "No. BetNow.tv is a free sports information, education and entertainment site. We never accept wagers, never process bets and never link to sportsbooks or gambling operators."),
    ("Where do the predictions come from?", "Our models use public fixture and league-table data, refreshed automatically every day. Soccer uses a Poisson goals model; US sports use a rating-based model with home advantage. Methodology is published on the Predictions page."),
    ("Are the contests really free?", "Yes. Every contest is free to enter, no purchase necessary. Prizes are funded by sponsors and community supporters. Entrants must be 18+ and contests are void where prohibited."),
    ("How do I advertise or sponsor?", "Visit Advertise & Sponsor and send the form, or use the inquiry link at the top of every page."),
    ("How is the site funded?", "Through display advertising, sponsorships and voluntary community support. Supporters fund data feeds, prizes, creators and hiring."),
]


def faq_html():
    return "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)


# ------------------------------------------------------------------ HOME
home = f"""
<section class="hero"><div class="container hero-grid">
 <div>
  <span class="eyebrow">⚡ Free · Data-driven · No wagering</span>
  <h1>Predict smarter. <span class="grad">Watch more.</span> Learn the math behind every game.</h1>
  <p class="lead">BetNow.tv is the free sports prediction hub: daily model probabilities for soccer, NFL, NBA, NHL and MLB, pro-grade calculators, official highlight channels, and free weekly contests with real prizes.</p>
  <div class="cta-row"><a class="btn btn-primary" href="predictions.html">See today's predictions →</a><a class="btn btn-ghost" href="#lead">Get the free Edge Report</a></div>
  <div class="stats"><div><b>5</b><span>major leagues tracked</span></div><div><b>6</b><span>free analytics tools</span></div><div><b>Daily</b><span>auto-updated data</span></div><div><b>$0</b><span>to play contests</span></div></div>
 </div>
 <div class="card"><h3>🎯 Daily trivia — keep your streak</h3><div id="trivia"></div>
  <p class="muted" style="font-size:.85rem">Your picks so far: <b data-pickcount>0</b> · Contest closes in <b id="countdown">—</b></p>
  <a class="btn btn-ghost btn-sm" href="contests.html">Enter this week's free contest</a></div>
</div></section>

<section><div class="container">
 <div class="section-head"><div><span class="tag lime">Updated <span id="fxUpdated">daily</span></span><h2 class="mt">Today's model predictions</h2><p>Tap a team to save your pick — then enter your picks in the free weekly contest.</p></div><a class="btn btn-ghost btn-sm" href="predictions.html">All predictions →</a></div>
 <div class="grid g3" id="fixtures" data-limit="6"><p class="muted">Loading predictions…</p></div>
</div></section>

<section><div class="container">{LEAD_QUIZ}</div></section>

<section><div class="container">
 <div class="section-head"><div><h2>Pro-grade tools. Free forever.</h2><p>Understand any price in seconds. Built for learning probability — not for placing wagers.</p></div><a class="btn btn-ghost btn-sm" href="tools.html">Open all tools →</a></div>
 <div class="grid g3">
  <a class="card" href="tools.html#odds" style="color:inherit"><div class="icon">🔁</div><h3>Odds converter</h3><p>Decimal ↔ American ↔ fractional, plus implied probability.</p></a>
  <a class="card" href="tools.html#margin" style="color:inherit"><div class="icon">⚖️</div><h3>Margin & fair price</h3><p>Strip the margin out of any market to reveal fair probabilities.</p></a>
  <a class="card" href="tools.html#poisson" style="color:inherit"><div class="icon">⚽</div><h3>Poisson score predictor</h3><p>Expected goals in, scoreline and result probabilities out.</p></a>
  <a class="card" href="tools.html#ev" style="color:inherit"><div class="icon">📐</div><h3>Expected value</h3><p>Compare your probability against a price, the analyst's way.</p></a>
  <a class="card" href="tools.html#elo" style="color:inherit"><div class="icon">🏆</div><h3>Elo win probability</h3><p>Turn rating gaps into win chances, with home advantage.</p></a>
  <a class="card" href="tools.html#bankroll" style="color:inherit"><div class="icon">📈</div><h3>Growth simulator</h3><p>See how small percentages compound over time.</p></a>
 </div></div></section>

<section><div class="container">
 <div class="section-head"><div><h2>Watch: latest from official channels</h2><p>Highlights and analysis from the leagues themselves, embedded with YouTube's privacy-enhanced player.</p></div><a class="btn btn-ghost btn-sm" href="videos.html">Video hub →</a></div>
 {video_grid(3)}
</div></section>

<section><div class="container">
 <div class="section-head"><div><h2>Learn the edge</h2><p>Original guides on odds, models and data — written for fans who want to think like analysts.</p></div><a class="btn btn-ghost btn-sm" href="learn.html">All guides →</a></div>
 {learn_cards(n=6)}
</div></section>

<section><div class="container">
 <div class="section-head"><div><h2>Latest sports headlines</h2><p>Auto-curated from major sports outlets every few hours.</p></div><a class="btn btn-ghost btn-sm" href="news.html">More news →</a></div>
 <div class="grid g3" id="news" data-limit="6"><p class="muted">Loading headlines…</p></div>
</div></section>

<section><div class="container grid g3">
 <div class="card"><div class="icon">🏅</div><h3>Free weekly contests</h3><p>Pick'em, trivia streaks and creator challenges. Free entry, real prizes from sponsors.</p><a class="btn btn-primary btn-sm" href="contests.html">Play free</a></div>
 <div class="card"><div class="icon">❤️</div><h3>Support independent analysis</h3><p>Fund data feeds, prizes and new creators. Every contribution keeps BetNow.tv free.</p><a class="btn btn-pink btn-sm" href="support.html">Support us</a></div>
 <div class="card"><div class="icon">🤝</div><h3>Sponsor & advertise</h3><p>Reach engaged, analytical sports fans with brand-safe placements and contest sponsorships.</p><a class="btn btn-ghost btn-sm" href="advertise.html">Media kit</a></div>
</div></section>

<section><div class="container" style="max-width:860px"><h2 class="center mb">Frequently asked questions</h2>{faq_html()}</div></section>
"""
faq_ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebSite", "name": "BetNow.tv", "url": DOMAIN + "/", "description": "Free sports predictions, odds education, videos and free-to-play contests."},
    {"@type": "Organization", "name": "BetNow.tv", "url": DOMAIN + "/", "logo": DOMAIN + "/assets/img/favicon.svg"},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}
w("index.html", page("BetNow.tv — Free Sports Predictions, Odds Tools, Videos & Contests",
                     "Free daily sports predictions with model probabilities, odds and probability calculators, official highlight videos, and free weekly prize contests. No wagering.",
                     "index.html", home, schema=faq_ld), "1.0")

# ------------------------------------------------------------------ PREDICTIONS
pred = hero("Auto-updated daily", "Sports predictions & model probabilities",
            "Win/draw/loss probabilities for upcoming games across top leagues, refreshed automatically from public fixture and standings data. Save picks, then enter them in the free contest.",
            "Predictions") + f"""
<section style="padding-top:10px"><div class="container">
 <div class="section-head"><div id="fxFilters" class="filters"></div><div class="muted">Last update: <b id="fxUpdated">—</b> · Your picks: <b data-pickcount>0</b> · <a href="contests.html">Submit picks →</a></div></div>
 <div class="grid g3" id="fixtures"><p class="muted">Loading predictions…</p></div>
</div></section>
<section><div class="container article">
 <h2>Methodology</h2>
 <p><b>Soccer</b> forecasts use a Poisson goals model. Each club's attack and defence strength comes from current-season goals scored and conceded per game relative to the league average, with a home-advantage factor. We compute the full scoreline grid and sum home-win, draw and away-win probabilities. <a href="learn/poisson-soccer-predictions.html">How Poisson models work →</a></p>
 <p><b>NFL, NBA, NHL and MLB</b> forecasts use a rating model derived from current win percentage and point differential, converted to win probability with a logistic (Elo-style) curve plus a sport-specific home edge. <a href="learn/elo-ratings-explained.html">How Elo works →</a></p>
 <p><b>Fair odds</b> are simply 1 ÷ probability — the price at which the forecast would be break-even. They are shown for education only.</p>
 <div class="callout"><span class="badge-18">18+</span>Predictions are statistical estimates for entertainment and education. They are not advice to gamble. BetNow.tv does not take wagers or link to sportsbooks. <a href="responsible-gaming.html">Responsible gaming</a></div>
 <h2>Limitations</h2>
 <ul><li>Early-season tables are noisy; probabilities regress toward 50/50 when few games are played.</li><li>Models do not see late injury news, rotation or weather.</li><li>Ties in US sports are rare and treated as a split.</li></ul>
</div></section>
<section><div class="container">{LEAD_QUIZ}</div></section>"""
w("predictions.html", page("Free Sports Predictions Today — Model Probabilities | BetNow.tv",
                           "Daily auto-updated sports predictions with win, draw and loss probabilities for soccer, NFL, NBA, NHL and MLB. Free, transparent methodology.",
                           "predictions.html", pred), "0.9")

# ------------------------------------------------------------------ TOOLS
def tool(id_, icon, title, desc, inputs, out_id, learn):
    return f"""<article class="card tool" id="{id_}"><div class="icon">{icon}</div><h3>{title}</h3><p>{desc}</p>{inputs}
<div class="kv" id="{out_id}"></div><p class="mt" style="font-size:.85rem"><a href="learn/{learn}.html">Learn the math →</a></p></article>"""

tools = hero("Free calculators", "Odds & probability tools", "Six fast, free calculators that turn prices and ratings into probabilities. Built for learning, analysis and fantasy decisions.", "Tools") + f"""
<section style="padding-top:10px"><div class="container grid g2">
{tool("odds","🔁","Odds converter","Convert any format and see implied probability.",
 '<div class="row"><div><label for="oc-fmt">Format</label><select id="oc-fmt"><option value="dec">Decimal (2.50)</option><option value="us">American (+150 / -200)</option><option value="frac">Fractional (3/2)</option></select></div><div><label for="oc-in">Odds</label><input id="oc-in" value="2.50"></div></div>',"oc-out","how-sports-odds-work")}
{tool("margin","⚖️","Margin & fair probability","Enter 2 or 3 decimal prices for one market.",
 '<div class="row"><div><label for="mg-a">Outcome A</label><input id="mg-a" type="number" step="0.01" value="2.10"></div><div><label for="mg-b">Outcome B</label><input id="mg-b" type="number" step="0.01" value="3.40"></div></div><label for="mg-c">Outcome C (optional)</label><input id="mg-c" type="number" step="0.01" value="3.60">',"mg-out","implied-probability-and-margin")}
{tool("ev","📐","Expected value","Your probability vs a decimal price.",
 '<div class="row"><div><label for="ev-p">Your probability %</label><input id="ev-p" type="number" value="45"></div><div><label for="ev-o">Decimal price</label><input id="ev-o" type="number" step="0.01" value="2.40"></div></div>',"ev-out","expected-value-explained")}
{tool("poisson","⚽","Poisson score predictor","Expected goals for each side.",
 '<div class="row"><div><label for="po-h">Home expected goals</label><input id="po-h" type="number" step="0.1" value="1.6"></div><div><label for="po-a">Away expected goals</label><input id="po-a" type="number" step="0.1" value="1.1"></div></div>',"po-out","poisson-soccer-predictions")}
{tool("elo","🏆","Elo win probability","Ratings plus home advantage.",
 '<div class="row"><div><label for="el-a">Team A rating</label><input id="el-a" type="number" value="1600"></div><div><label for="el-b">Team B rating</label><input id="el-b" type="number" value="1500"></div></div><label for="el-h">Home advantage for A (points)</label><input id="el-h" type="number" value="65">',"el-out","elo-ratings-explained")}
{tool("bankroll","📈","Compounding simulator","See how a small % per period compounds — and how fast negative % erodes.",
 '<div class="row"><div><label for="br-s">Starting value</label><input id="br-s" type="number" value="1000"></div><div><label for="br-r">% change per period</label><input id="br-r" type="number" step="0.1" value="-2"></div></div><label for="br-n">Periods</label><input id="br-n" type="number" value="52">',"br-out","variance-and-sample-size")}
</div></section>
<section><div class="container">{LEAD_QUIZ}</div></section>"""
w("tools.html", page("Free Odds Converter & Probability Calculators | BetNow.tv",
                     "Free odds converter, margin calculator, expected value, Poisson score predictor and Elo win probability tools. Learn the math behind sports prices.",
                     "tools.html", tools), "0.9")

# ------------------------------------------------------------------ VIDEOS
vids = hero("Video hub", "Sports highlights & analysis", "Latest uploads from official league and broadcaster channels in one place. Videos load only when you press play.", "Videos") + f"""
<section style="padding-top:10px"><div class="container">{video_grid(6)}
<p class="muted mt" style="font-size:.85rem">Videos are embedded via YouTube's official player; all rights belong to the respective channel owners. BetNow.tv is not affiliated with these leagues or broadcasters.</p></div></section>
<section><div class="container card"><h2>Are you a sports creator?</h2><p class="muted">We feature independent analysts and highlight creators. Pitch your channel for a spotlight, a paid collaboration, or our creator contest.</p>
{form("Creator spotlight pitch", NAME_EMAIL + '<label>Channel URL</label><input name="channel" type="url" required><label>What do you cover?</label><textarea name="message" required></textarea>', "Pitch my channel", lead_type="Creator")}
</div></section>"""
w("videos.html", page("Sports Highlights Video Hub — NBA, NFL, Premier League, MLB, NHL | BetNow.tv",
                      "Watch the latest official highlights and analysis from NBA, NFL, Premier League, MLB, NHL and ESPN in one free video hub.",
                      "videos.html", vids), "0.8")

# ------------------------------------------------------------------ NEWS
news = hero("Auto-curated", "Sports news headlines", "Headlines from major sports outlets, refreshed automatically several times a day. Click through to read the full story at the source.", "News") + """
<section style="padding-top:10px"><div class="container"><div class="grid g3" id="news" data-limit="48"><p class="muted">Loading headlines…</p></div></div></section>"""
w("news.html", page("Latest Sports News Headlines — Auto-Updated | BetNow.tv",
                    "Auto-updated sports news headlines from leading outlets covering soccer, NFL, NBA, MLB and NHL.", "news.html", news), "0.8")

# ------------------------------------------------------------------ LEARN
learn = hero("Guides", "Learn sports analytics", "Original, plain-English guides to odds, probability, models and advanced stats.", "Learn") + f"""
<section style="padding-top:10px"><div class="container"><input id="learnSearch" placeholder="Search guides… (e.g. Poisson, xG, Elo)" aria-label="Search guides" style="max-width:480px">
{learn_cards()}</div></section>
<section><div class="container">{LEAD_QUIZ}</div></section>"""
w("learn.html", page("Learn Sports Analytics: Odds, Probability & Models | BetNow.tv",
                     "Free guides to sports odds, implied probability, expected value, Poisson and Elo models, and advanced stats like xG and EPA.", "learn.html", learn), "0.9")

for i, a in enumerate(ARTICLES):
    nxt = ARTICLES[(i + 1) % len(ARTICLES)]
    body = f"""<section class="page-hero"><div class="container article">
<div class="breadcrumb"><a href="../index.html">Home</a> / <a href="../learn.html">Learn</a> / {a["tag"]}</div>
<span class="tag lime">{a["tag"]}</span><h1 class="mt">{a["title"]}</h1>
<p class="meta">By the BetNow.tv Analytics Desk · {a["min"]} min read · Updated {TODAY}</p>
{a["html"]}
<div class="card mt"><h3>Keep learning</h3><p>Next: <a href="{nxt["slug"]}.html">{nxt["title"]}</a></p>
<p class="muted">Get one 3-minute lesson every Sunday in the free Edge Report.</p><a class="btn btn-primary btn-sm" href="../edge.html">Get the Edge Report</a></div>
</div></section>"""
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"],
          "author": {"@type": "Organization", "name": "BetNow.tv Analytics Desk"}, "publisher": {"@type": "Organization", "name": "BetNow.tv"},
          "dateModified": TODAY, "mainEntityOfPage": f"{DOMAIN}/learn/{a['slug']}.html"}
    w(f"learn/{a['slug']}.html", page(a["title"] + " | BetNow.tv", a["desc"], f"learn/{a['slug']}.html", body, p="../", schema=ld, ogtype="article"), "0.8")

# ------------------------------------------------------------------ CONTESTS
contests = hero("Free to enter · No purchase necessary", "Free weekly contests & prizes", "Pick'em, trivia streaks and creator challenges. Prizes are funded by sponsors and supporters — entry is always free.", "Contests") + f"""
<section style="padding-top:10px"><div class="container grid g3">
 <div class="card"><span class="tag lime">Weekly</span><h3 class="mt">🏈 Free Pick'em</h3><p>Pick winners on the <a href="predictions.html">Predictions</a> page, then submit below. Most correct picks wins; ties broken by random draw.</p><p>Closes in <b id="countdown">—</b> · Your picks: <b data-pickcount>0</b></p></div>
 <div class="card"><span class="tag amber">Daily</span><h3 class="mt">🧠 Trivia streak</h3><div id="trivia"></div></div>
 <div class="card"><span class="tag pink">Monthly</span><h3 class="mt">🎬 Creator challenge</h3><p>Make the best 60-second explainer of a sports-analytics concept. Winner gets featured and a cash or gear prize from that month's sponsor.</p><a class="btn btn-ghost btn-sm" href="videos.html#">Pitch your entry</a></div>
</div></section>
<section><div class="container grid g2">
 <div>{form("Pick'em contest entry", NAME_EMAIL + '<input type="hidden" name="picks"><label>Display name for leaderboard</label><input name="nickname" required maxlength="24"><label>Tiebreaker: total points in the week\'s headline game</label><input name="tiebreak" type="number" required><label class="check"><input type="checkbox" name="rules" value="accepted" required> I am 18+ and accept the Official Rules. No purchase necessary.</label>', "Submit my picks", success="Entry received! Winners are announced every Monday.", lead_type="Contest entry")}</div>
 <div class="card"><h3>🏆 Leaderboard</h3><p class="muted">Weekly results are posted here every Monday after entries are verified.</p><ul class="lb"><li><span>This week</span><b>Entries open</b></li><li><span>Prize pool</span><b>Sponsor-funded</b></li><li><span>Entry fee</span><b style="color:var(--lime)">Free</b></li></ul>
 <h3 class="mt">Want to sponsor a prize?</h3><p class="muted">Brands get logo placement, a newsletter feature and all contest impressions.</p><a class="btn btn-primary btn-sm" href="advertise.html">Sponsor a contest</a></div>
</div></section>
<section><div class="container article"><h2>Official rules (summary)</h2>
<ol><li><b>No purchase or payment necessary</b> to enter or win. A purchase or donation does not improve chances of winning.</li>
<li>Open to individuals 18+ (or age of majority) where legal; void where prohibited. One entry per person per contest.</li>
<li>Contests are games of skill/knowledge with no entry fee. No wagering is involved.</li>
<li>Winners are determined by the scoring rules stated for each contest; ties are broken by tiebreaker, then random draw.</li>
<li>Winners are contacted by email and must respond within 7 days. Prizes are non-transferable; sponsor substitutions of equal value may apply.</li>
<li>Residents of jurisdictions where skill contests are restricted (e.g., Quebec residents may need to answer a skill-testing question) must satisfy local requirements.</li>
<li>BetNow.tv may modify or cancel a contest in case of fraud or technical failure. See <a href="terms.html">Terms</a> and <a href="privacy.html">Privacy</a>.</li></ol></div></section>"""
w("contests.html", page("Free Sports Contests & Pick'em Prizes — No Purchase Necessary | BetNow.tv",
                        "Enter free weekly sports Pick'em contests, daily trivia streaks and creator challenges. Sponsor-funded prizes, no entry fee.", "contests.html", contests), "0.9")

# ------------------------------------------------------------------ EDGE (dedicated lead generation)
edge = hero("Free weekly report", "The Sunday Edge Report", "Join fans who get model probabilities, one sharp stat per game and a 3-minute analytics lesson every Sunday. Free forever.", "Edge Report") + f"""
<section style="padding-top:10px"><div class="container">{LEAD_QUIZ}</div></section>
<section><div class="container grid g3">
 <div class="card"><div class="icon">📊</div><h3>Probabilities, not hype</h3><p>Every big game with home/draw/away percentages and fair prices.</p></div>
 <div class="card"><div class="icon">🎓</div><h3>Learn in 3 minutes</h3><p>One concept per week: margin, xG, EPA, variance, Elo…</p></div>
 <div class="card"><div class="icon">🎁</div><h3>Prize access</h3><p>First access to free contests and sponsor giveaways.</p></div>
</div></section>
<section><div class="container grid g2">
 <div><h2>For businesses: partner leads</h2><p class="muted">Brands, media buyers, data providers and fantasy apps — tell us what you need and we'll reply within 1 business day.</p>
 {form("Business partnership lead", NAME_EMAIL + '<div class="row"><div><label>Company</label><input name="company" required></div><div><label>Budget range</label><select name="budget"><option>Under $1k</option><option>$1k–$5k</option><option>$5k–$25k</option><option>$25k+</option></select></div></div><label>Interest</label><select name="interest"><option>Display / native advertising</option><option>Contest sponsorship</option><option>Newsletter sponsorship</option><option>Data / content partnership</option><option>Domain / website acquisition</option></select><label>Message</label><textarea name="message"></textarea>', "Request a proposal", lead_type="B2B partner")}</div>
 <div><h2>Request a custom model</h2><p class="muted">Creators, podcasters and leagues: get a custom probability widget, power ranking or data story for your audience.</p>
 {form("Custom model request", NAME_EMAIL + '<label>Sport / league</label><input name="sport" required><label>What do you need?</label><textarea name="message" required></textarea>', "Request a quote", lead_type="Custom model")}</div>
</div></section>"""
w("edge.html", page("Free Sunday Edge Report — Weekly Sports Probabilities | BetNow.tv",
                    "Get the free weekly Edge Report: model probabilities, data-backed angles and a 3-minute analytics lesson. Plus partner and custom-model requests.", "edge.html", edge), "0.9")

# ------------------------------------------------------------------ SUPPORT
support = hero("Community-funded", "Support BetNow.tv", "Your support pays for data feeds, servers, contest prizes, marketing and new contributors — and keeps everything free.", "Support") + f"""
<section style="padding-top:10px"><div class="container">
 <div class="card mb"><h3>Season goal</h3><div class="progress"><i id="goalBar" style="width:2%"></i></div><p class="muted mt" id="goalTxt"></p></div>
 <div class="grid g4">
  <div class="card tier"><h3>Fan</h3><div class="amt">$5</div><p>Covers a day of data feeds.</p><a class="btn btn-ghost btn-block" data-amount="5" data-donate="buymeacoffee" href="#pledge">Give $5</a></div>
  <div class="card tier featured"><h3>Analyst</h3><div class="amt">$15</div><p>Funds a weekly contest prize.</p><a class="btn btn-primary btn-block" data-amount="15" data-donate="paypal" href="#pledge">Give $15</a></div>
  <div class="card tier"><h3>Pro</h3><div class="amt">$50</div><p>Pays a creator for an explainer.</p><a class="btn btn-ghost btn-block" data-amount="50" data-donate="stripe" href="#pledge">Give $50</a></div>
  <div class="card tier"><h3>Club</h3><div class="amt">Monthly</div><p>Recurring support + supporter badge.</p><a class="btn btn-ghost btn-block" data-amount="monthly" data-donate="patreon" href="#pledge">Join monthly</a></div>
 </div></div></section>
<section><div class="container grid g2">
 <div class="card"><h2>Where your money goes</h2><table><tbody><tr><td>⚙️ Operations — data feeds, hosting, tools</td><td><b>35%</b></td></tr><tr><td>🏆 Contests & prizes</td><td><b>25%</b></td></tr><tr><td>🧑‍💻 Hiring writers, analysts, editors</td><td><b>25%</b></td></tr><tr><td>📣 Promotion & marketing</td><td><b>15%</b></td></tr></tbody></table>
 <p class="muted mt">Support is a voluntary contribution, not a purchase, and does not affect contest eligibility or odds. Not tax-deductible.</p></div>
 <div id="pledge"><h2>Pledge or ask about other ways to give</h2><p class="muted">Prefer bank transfer, crypto, in-kind prizes or corporate matching? Send a pledge and we'll reply with secure payment details.</p>
 {form("Donation pledge", NAME_EMAIL + '<div class="row"><div><label>Amount (USD)</label><input id="pledgeAmount" name="amount" required></div><div><label>Support type</label><select name="type"><option>One-time</option><option>Monthly</option><option>Prize sponsorship</option><option>In-kind (gear, tickets, software)</option></select></div></div><label>Message (optional)</label><textarea name="message"></textarea><label class="check"><input type="checkbox" name="public" value="yes"> Thank me publicly on the supporters wall</label>', "Send my pledge", success="Thank you! We'll email secure payment details shortly.", lead_type="Donation pledge")}</div>
</div></section>"""
w("support.html", page("Support BetNow.tv — Donate to Keep Sports Analytics Free",
                       "Support BetNow.tv with a one-time or monthly contribution. Funds data, prizes, hiring and promotion — and keeps every tool free.", "support.html", support), "0.7")

# ------------------------------------------------------------------ ADVERTISE
adv = hero("Media kit", "Advertise & sponsor on BetNow.tv", "Reach analytical, high-intent sports fans across predictions, tools, video and newsletter — in a brand-safe, no-gambling-operator environment.", "Advertise") + f"""
<section style="padding-top:10px"><div class="container grid g4">
 <div class="card"><div class="icon">🖼</div><h3>Display & native</h3><p>Premium placements on predictions and tools pages.</p></div>
 <div class="card"><div class="icon">✉️</div><h3>Newsletter</h3><p>Presenting sponsor of the Sunday Edge Report.</p></div>
 <div class="card"><div class="icon">🏆</div><h3>Contest sponsor</h3><p>Name a weekly contest, fund prizes, collect opted-in leads.</p></div>
 <div class="card"><div class="icon">🎬</div><h3>Video & creators</h3><p>Branded explainers with our creator network.</p></div>
</div></section>
<section><div class="container grid g2">
 <div class="card"><h2>Audience</h2><ul class="lb"><li><span>Interests</span><b>Sports, fantasy, data, tech</b></li><li><span>Age</span><b>18+ only</b></li><li><span>Markets</span><b>US · CA · UK · IN · AU</b></li><li><span>Brand safety</span><b>No gambling operator ads sold</b></li></ul>
 <p class="muted mt">Category policy: we accept sports apparel, streaming, tech, fantasy (free-to-play), fitness, food & beverage, travel and education advertisers. We do not sell placements to sportsbooks or casinos.</p></div>
 {form("Advertising / sponsorship inquiry", NAME_EMAIL + '<div class="row"><div><label>Company</label><input name="company" required></div><div><label>Website</label><input name="website" type="url"></div></div><label>Package</label><select name="package"><option>Display & native</option><option>Newsletter sponsor</option><option>Contest sponsor</option><option>Video / creator</option><option>Custom / all of the above</option></select><label>Goals & timing</label><textarea name="message" required></textarea>', "Request media kit & pricing", lead_type="Advertiser")}
</div></section>
<section><div class="container card center"><h2>Interested in acquiring this website or domain?</h2><p class="muted">Domain, full-site acquisition and strategic partnerships are handled through our inquiry desk.</p><a class="btn btn-primary" href="{INQUIRY}" target="_blank" rel="noopener">Make an inquiry →</a></div></section>"""
w("advertise.html", page("Advertise & Sponsor — Media Kit | BetNow.tv",
                         "Advertise to engaged sports fans on BetNow.tv: display, newsletter, contest sponsorships and creator video. Brand-safe, 18+ audience.", "advertise.html", adv), "0.7")

# ------------------------------------------------------------------ CAREERS
roles = [("Sports Data Analyst", "Remote · Part-time", "Build and validate prediction models (Python, R). Experience with xG, Elo or EPA a plus."),
         ("Sports Writer / Editor", "Remote · Freelance", "Write evergreen analytics guides and weekly previews. Clear, data-literate writing."),
         ("Video Creator", "Remote · Per project", "Produce 60-second explainers and highlight breakdowns for YouTube Shorts, TikTok and Reels."),
         ("Front-end Developer", "Remote · Contract", "Ship fast, accessible features in vanilla JS and static-site tooling."),
         ("Partnerships Manager", "Remote · Commission", "Sell sponsorships, newsletter and contest packages to non-gambling brands."),
         ("Community Moderator", "Remote · Volunteer / paid", "Run contests, verify entries and keep our community welcoming.")]
careers = hero("We're hiring", "Careers at BetNow.tv", "Help build the most trusted free sports-analytics hub. Remote-first, flexible, results-focused.", "Careers") + \
    '<section style="padding-top:10px"><div class="container grid g3">' + "".join(
        f'<div class="card"><span class="tag">{loc}</span><h3 class="mt">{t}</h3><p>{d}</p></div>' for t, loc, d in roles) + \
    f"""</div></section><section><div class="container" style="max-width:760px"><h2>Apply</h2>
{form("Job application", NAME_EMAIL + '<label>Role</label><select name="role">' + "".join(f"<option>{t}</option>" for t, _, _ in roles) + '<option>Other / open application</option></select><label>Portfolio, LinkedIn or GitHub URL</label><input name="portfolio" type="url" required><label>Why you? (short)</label><textarea name="message" required></textarea>', "Submit application", success="Application received — thank you! We review every application.", lead_type="Job applicant")}</div></section>"""
w("careers.html", page("Careers — Sports Analysts, Writers, Creators | BetNow.tv",
                       "Join BetNow.tv: remote roles for sports data analysts, writers, video creators, developers and partnerships managers.", "careers.html", careers), "0.6")

# ------------------------------------------------------------------ ABOUT / CONTACT
about = hero("About", "About BetNow.tv", "An independent, free sports-analytics publication.", "About") + """
<section style="padding-top:10px"><div class="container article">
<p>BetNow.tv exists to make sports probability understandable. Fans see numbers everywhere — prices, power rankings, win probabilities — but rarely get an honest explanation of what they mean. We publish transparent model forecasts, free calculators and plain-English guides so anyone can think like an analyst.</p>
<h2>What we believe</h2><ul><li><b>Transparency:</b> methods are published; limitations are stated.</li><li><b>No wagering:</b> we never take bets or promote gambling operators. Our contests are free.</li><li><b>Education first:</b> every tool links to a guide explaining the math.</li><li><b>Fan-funded independence:</b> advertising, sponsorship and supporters fund the site.</li></ul>
<h2>How the site stays fresh</h2><p>Fixtures, predictions and headlines are refreshed automatically several times a day from public data sources. Our editorial team writes and reviews all guides.</p>
<h2>Editorial standards</h2><p>Guides are written by the BetNow.tv Analytics Desk and reviewed for accuracy. Spot an error? <a href="contact.html">Tell us</a> — corrections are made promptly.</p></div></section>"""
w("about.html", page("About BetNow.tv — Independent Sports Analytics", "About BetNow.tv: an independent, free sports predictions and analytics education site. No wagering, transparent methods.", "about.html", about), "0.5")

contact = hero("Contact", "Contact us", "Questions, corrections, partnerships or press — we reply within 1–2 business days.", "Contact") + f"""
<section style="padding-top:10px"><div class="container grid g2">
{form("General contact", NAME_EMAIL + '<label>Topic</label><select name="topic"><option>General question</option><option>Correction / feedback</option><option>Advertising & sponsorship</option><option>Contest question</option><option>Press</option><option>Website / domain acquisition</option><option>Privacy request</option></select><label>Message</label><textarea name="message" required></textarea>', "Send message", lead_type="Contact")}
<div class="card"><h3>Other ways to reach us</h3><ul class="lb"><li><span>Advertising</span><a href="advertise.html">Media kit →</a></li><li><span>Jobs</span><a href="careers.html">Careers →</a></li><li><span>Support</span><a href="support.html">Donate →</a></li><li><span>Domain / partnership</span><a href="{INQUIRY}" target="_blank" rel="noopener">Inquiry desk →</a></li></ul>
<p class="muted mt">For privacy, our team inbox is not published. Every message sent through this form reaches us directly.</p></div>
</div></section>"""
w("contact.html", page("Contact BetNow.tv", "Contact BetNow.tv for questions, corrections, advertising, contests, press or partnerships.", "contact.html", contact), "0.5")

# ------------------------------------------------------------------ LEGAL
def legal(slug, title, desc, html, prio="0.3"):
    w(slug, page(title + " | BetNow.tv", desc, slug, hero("Legal", title, f"Last updated {TODAY}.", title) + f'<section style="padding-top:10px"><div class="container article">{html}</div></section>'), prio)

legal("privacy.html", "Privacy Policy", "How BetNow.tv collects, uses and protects information, including cookies and Google AdSense advertising.", """
<p>This policy explains what information BetNow.tv ("we") collects and how it is used.</p>
<h2>Information you give us</h2><p>When you submit a form (newsletter, contest entry, pledge, application or contact), we receive the details you enter, such as name, email and message. Form submissions are delivered through a third-party form-processing service (FormSubmit) to our private inbox. We use this data only to respond, deliver the newsletter, run contests or process your request. We do not sell personal data.</p>
<h2>Information stored on your device</h2><p>Your picks, trivia streak, theme and cookie choice are stored in your browser's local storage and never leave your device unless you submit a form.</p>
<h2>Advertising and cookies</h2><p>We use Google AdSense to display ads. Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this and other websites. Google's use of advertising cookies enables it and its partners to serve ads based on your visits to this site and/or other sites on the Internet. You may opt out of personalised advertising by visiting <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">Google Ads Settings</a> or <a href="https://www.aboutads.info/choices" target="_blank" rel="noopener">aboutads.info</a>. Learn more in <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">How Google uses data from partner sites</a>. Visitors in the EEA, UK and Switzerland are shown a consent message before personalised ads are served.</p>
<h2>Embedded content</h2><p>Videos use YouTube's privacy-enhanced mode and load only after you click play. Fonts are served by Google Fonts. These providers may collect technical data under their own policies.</p>
<h2>Children</h2><p>BetNow.tv is intended for adults 18+. We do not knowingly collect information from minors.</p>
<h2>Your rights</h2><p>You may request access, correction or deletion of your data (GDPR, UK GDPR, CCPA/CPRA, PIPEDA) via the <a href="contact.html">contact form</a> (topic: Privacy request). Newsletter emails include an unsubscribe option.</p>
<h2>Retention & security</h2><p>We keep form data only as long as needed for its purpose, then delete it. The site is served over HTTPS.</p>
<h2>Changes</h2><p>We may update this policy; the date above shows the latest revision.</p>""")

legal("terms.html", "Terms of Use", "Terms governing use of BetNow.tv predictions, tools, contests and content.", """
<h2>1. Nature of the service</h2><p>BetNow.tv provides sports information, statistical predictions, educational content, calculators and free-to-play contests for entertainment and educational purposes. <b>We do not accept, process or facilitate wagers of any kind</b>, and nothing on this site is financial, legal or gambling advice.</p>
<h2>2. Eligibility</h2><p>You must be 18 or older (or the age of majority where you live) to use the site and enter contests.</p>
<h2>3. No guarantees</h2><p>Predictions are probabilistic estimates generated from public data and may be wrong or outdated. Content is provided "as is" without warranties. You are solely responsible for decisions you make.</p>
<h2>4. Contests</h2><p>Contests are free; no purchase necessary. Each contest is governed by its Official Rules on the <a href="contests.html">Contests</a> page. Void where prohibited.</p>
<h2>5. Donations</h2><p>Contributions are voluntary, non-refundable except where required by law, and do not confer any goods, services or contest advantages.</p>
<h2>6. Intellectual property</h2><p>Original text, design, code and models are © BetNow.tv. Third-party trademarks and embedded content belong to their owners — see <a href="disclaimer.html">Trademark & Copyright</a>.</p>
<h2>7. Acceptable use</h2><p>No scraping that burdens the site, no automated contest entries, no unlawful use.</p>
<h2>8. Limitation of liability</h2><p>To the extent permitted by law, BetNow.tv is not liable for indirect or consequential losses arising from use of the site.</p>
<h2>9. Changes</h2><p>We may update these terms at any time; continued use means acceptance.</p>""")

legal("disclaimer.html", "Trademark & Copyright Disclosure", "BetNow.tv trademark, copyright and non-affiliation disclosure.", """
<h2>Non-affiliation</h2><p>BetNow.tv is an independent sports information and education publication. <b>BetNow.tv is not affiliated with, endorsed by, sponsored by or connected to any sportsbook, online casino, gaming operator, or any company or brand that uses the name "BetNow", "Bet Now" or any similar mark.</b> The domain name is used descriptively for a free, no-wagering site whose brand presentation ("BetNow<span>.tv</span>" with the "BN" mark, tagline "Predict · Watch · Learn") is distinct from any such business. If you believe any content infringes your rights, please contact us through the <a href="contact.html">contact form</a> and we will respond promptly.</p>
<h2>Third-party trademarks</h2><p>NBA, NFL, NHL, MLB, Premier League, ESPN, YouTube and all team and league names are trademarks of their respective owners. They are referenced only to identify sports events and content (nominative use) and imply no endorsement. We do not use official team or league logos.</p>
<h2>Copyright</h2><p>All original text, guides, designs, code, models and graphics on this site are © BetNow.tv, all rights reserved. Embedded videos are displayed via YouTube's official embed player under YouTube's Terms of Service; copyright remains with the uploading channel. News headlines link to and are credited to their original publishers; we display headlines and short descriptions only.</p>
<h2>Data</h2><p>Fixture and standings data are sourced from public sports-data APIs and feeds and may contain errors. Predictions are our own statistical estimates.</p>
<h2>DMCA / takedown</h2><p>Send notices via the <a href="contact.html">contact form</a> (topic: Press/Legal) with the URL, the work claimed and your contact details.</p>""")

legal("responsible-gaming.html", "Responsible Gaming", "Responsible gaming information and free help resources. BetNow.tv does not accept wagers.", """
<p><span class="badge-18">18+</span>BetNow.tv is a free, no-wagering site. We publish predictions and probability education because understanding probability helps people make informed, healthier decisions. If you gamble elsewhere, these principles and resources matter.</p>
<h2>Warning signs</h2><ul><li>Spending more time or money than intended</li><li>Chasing losses or feeling a result is "due"</li><li>Borrowing money or hiding activity from family</li><li>Feeling anxious or irritable when not gambling</li><li>Gambling to escape problems or low mood</li></ul>
<h2>Healthy habits</h2><ul><li>Treat any gambling as entertainment spending, never income.</li><li>Set time and money limits in advance and keep them.</li><li>Never gamble while upset, tired or under the influence.</li><li>Remember the maths: market margins mean most people lose over time (see <a href="learn/implied-probability-and-margin.html">margin explained</a>).</li></ul>
<h2>Free, confidential help</h2><ul>
<li>USA: 1-800-GAMBLER · <a href="https://www.ncpgambling.org" target="_blank" rel="noopener nofollow">National Council on Problem Gambling</a></li>
<li>Canada: <a href="https://www.connexontario.ca" target="_blank" rel="noopener nofollow">ConnexOntario</a> 1-866-531-2600 · <a href="https://www.responsiblegambling.org" target="_blank" rel="noopener nofollow">Responsible Gambling Council</a></li>
<li>UK: <a href="https://www.begambleaware.org" target="_blank" rel="noopener nofollow">BeGambleAware</a> · National Gambling Helpline 0808 8020 133 · <a href="https://www.gamstop.co.uk" target="_blank" rel="noopener nofollow">GAMSTOP</a> self-exclusion</li>
<li>Australia: <a href="https://www.gamblinghelponline.org.au" target="_blank" rel="noopener nofollow">Gambling Help Online</a> 1800 858 858</li>
<li>International: <a href="https://www.gamblersanonymous.org" target="_blank" rel="noopener nofollow">Gamblers Anonymous</a></li></ul>
<h2>Blocking tools</h2><p>Free tools such as Gamban, BetBlocker and device-level parental controls can block gambling sites and apps.</p>""", "0.5")

# ------------------------------------------------------------------ 404
w("404.html", page("Page not found | BetNow.tv", "The page you requested could not be found.", "404.html",
                   '<section class="page-hero"><div class="container center"><h1>404 — Off target</h1><p class="muted mt">That page went wide. Try the predictions or tools instead.</p><div class="cta-row" style="justify-content:center;display:flex;gap:10px;margin-top:20px"><a class="btn btn-primary" href="index.html">Home</a><a class="btn btn-ghost" href="predictions.html">Predictions</a></div></div></section>'), "0")

# ------------------------------------------------------------------ SITEMAP
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path, prio in PAGES:
    if path == "404.html":
        continue
    loc = f"{DOMAIN}/" + ("" if path == "index.html" else path)
    freq = "daily" if path in ("index.html", "predictions.html", "news.html") else "weekly"
    sm.append(f"<url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><changefreq>{freq}</changefreq><priority>{prio}</priority></url>")
sm.append("</urlset>")
open(os.path.join(ROOT, "sitemap.xml"), "w").write("\n".join(sm))
print(f"Built {len(PAGES)} pages")
