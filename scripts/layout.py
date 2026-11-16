"""Shared layout for BetNow.tv static pages (header, footer, head)."""
import json, datetime

DOMAIN = "https://betnow.tv"
ADS = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>'
INQUIRY = "https://web.works/contact"
NAV = [("index.html", "Home"), ("predictions.html", "Predictions"), ("tools.html", "Tools"),
       ("videos.html", "Videos"), ("news.html", "News"), ("learn.html", "Learn"),
       ("contests.html", "Contests"), ("edge.html", "Free Edge Report")]


def head(title, desc, path, p="", schema=None, ogtype="website"):
    url = f"{DOMAIN}/{path}".replace("/index.html", "/")
    ld = schema or {"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": url, "description": desc,
                    "isPartOf": {"@type": "WebSite", "name": "BetNow.tv", "url": DOMAIN + "/"}}
    return f"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#0a0f1e">
<meta property="og:type" content="{ogtype}"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}"><meta property="og:site_name" content="BetNow.tv"><meta property="og:image" content="{DOMAIN}/assets/img/og.svg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{p}assets/img/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="{p}manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}assets/css/style.css">
{ADS}
<script type="application/ld+json">{json.dumps(ld)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><a href="{INQUIRY}" target="_blank" rel="noopener">Contact, if you are interested in this website/domain name/Sponsorship/Advertisement/Partnership</a></div>
<header class="site-header"><div class="container nav">
  <a class="logo" href="{p}index.html" aria-label="BetNow.tv home"><span class="logo-mark">BN</span><span>BetNow<span class="grad">.tv</span><small>Predict · Watch · Learn</small></span></a>
  <ul class="menu" id="menu">{''.join(f'<li><a href="{p}{h}">{t}</a></li>' for h, t in NAV)}</ul>
  <div class="nav-actions"><a class="btn btn-primary btn-sm" href="{p}support.html">❤ Support</a>
  <button class="icon-btn" id="themeToggle" aria-label="Toggle light/dark theme">◐</button>
  <button class="icon-btn burger" id="burger" aria-label="Open menu">☰</button></div>
</div></header>
<div class="ticker" aria-hidden="true"><div class="ticker-track" id="ticker"><span><b>●</b> Free-to-play predictions, updated daily</span><span><b>●</b> No real-money wagering on this site</span><span><b>●</b> Weekly free Pick'em — prizes, no purchase necessary</span><span><b>●</b> Free-to-play predictions, updated daily</span><span><b>●</b> No real-money wagering on this site</span><span><b>●</b> Weekly free Pick'em — prizes, no purchase necessary</span></div></div>
<main id="main">
"""


def foot(p=""):
    return f"""</main>
<a class="btn btn-primary sticky-cta" href="{p}edge.html">📈 Get the free Edge Report</a>
<div class="modal" id="leadModal" role="dialog" aria-modal="true" aria-labelledby="mTitle"><div class="modal-box">
  <button class="modal-close" aria-label="Close">×</button>
  <span class="eyebrow">Free · Weekly</span>
  <h3 id="mTitle">Before you go — get the Sunday Edge Report</h3>
  <p class="muted">Model probabilities for the week's biggest games, one smart stat per match, and the Pick'em prize draw link. Free. Unsubscribe anytime.</p>
  <form class="js-form" data-subject="Exit-intent newsletter signup" data-success="You're in! Watch your inbox on Sunday.">
    <input class="hp" name="_honey" tabindex="-1" autocomplete="off">
    <input type="hidden" name="lead_type" value="Newsletter (exit intent)">
    <input name="name" placeholder="First name" required>
    <input type="email" name="email" placeholder="Email address" required>
    <label class="check"><input type="checkbox" name="consent" value="yes" required> I'm 18+ and agree to receive the free newsletter.</label>
    <button class="btn btn-primary btn-block" type="submit">Send me the Edge Report</button>
  </form></div></div>
<div class="cookie" id="cookie"><p>We use cookies for analytics and to serve ads through Google AdSense, which may personalize ads. See our <a href="{p}privacy.html">Privacy Policy</a>.</p>
  <div style="display:flex;gap:8px"><button class="btn btn-primary btn-sm" data-consent="all">Accept all</button><button class="btn btn-ghost btn-sm" data-consent="essential">Essential only</button></div></div>
<footer class="site-footer"><div class="container">
 <div class="foot-grid">
  <div><a class="logo" href="{p}index.html"><span class="logo-mark">BN</span><span>BetNow<span class="grad">.tv</span></span></a>
   <p class="muted mt">Free sports predictions, odds-math education, videos and free-to-play contests. We never take wagers and never link to sportsbooks.</p>
   <a class="btn btn-primary btn-sm" href="{p}edge.html">Get the free Edge Report</a></div>
  <div><h4>Explore</h4><ul><li><a href="{p}predictions.html">Predictions</a></li><li><a href="{p}tools.html">Calculators</a></li><li><a href="{p}videos.html">Videos</a></li><li><a href="{p}news.html">News</a></li><li><a href="{p}learn.html">Learn</a></li></ul></div>
  <div><h4>Community</h4><ul><li><a href="{p}contests.html">Free contests</a></li><li><a href="{p}support.html">Support us</a></li><li><a href="{p}careers.html">Careers</a></li><li><a href="{p}advertise.html">Advertise / Sponsor</a></li></ul></div>
  <div><h4>Company</h4><ul><li><a href="{p}about.html">About</a></li><li><a href="{p}contact.html">Contact</a></li><li><a href="{INQUIRY}" target="_blank" rel="noopener">Domain & partnership inquiries</a></li></ul></div>
  <div><h4>Legal</h4><ul><li><a href="{p}privacy.html">Privacy</a></li><li><a href="{p}terms.html">Terms</a></li><li><a href="{p}disclaimer.html">Trademark & Copyright</a></li><li><a href="{p}responsible-gaming.html">Responsible gaming</a></li></ul></div>
 </div>
 <div class="rg-bar"><span class="badge-18">18+</span>BetNow.tv is a free information & entertainment site. We do not accept wagers, process bets, or promote gambling operators. If gambling is causing you harm, call 1-800-GAMBLER (US), visit <a href="https://www.begambleaware.org" target="_blank" rel="noopener nofollow">BeGambleAware.org</a> (UK) or <a href="https://www.connexontario.ca" target="_blank" rel="noopener nofollow">ConnexOntario</a> (CA).</div>
 <div class="legal">© <span data-year></span> BetNow.tv. Independent publication — not affiliated with any sportsbook, gaming operator or company using the name "BetNow" or similar marks. Team and league names are trademarks of their respective owners, used for identification only. <a href="{p}disclaimer.html">Full disclosure</a>.</div>
</div></footer>
<script src="{p}assets/js/config.js"></script>
<script src="{p}assets/js/app.js" defer></script>
</body></html>
"""


def page(title, desc, path, body, p="", schema=None, ogtype="website"):
    return head(title, desc, path, p, schema, ogtype) + body + foot(p)


def hero(eyebrow, h1, lead, crumbs=None, p=""):
    bc = f'<div class="breadcrumb"><a href="{p}index.html">Home</a> / {crumbs}</div>' if crumbs else ""
    return f'<section class="page-hero"><div class="container">{bc}<span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p class="mt">{lead}</p></div></section>'
