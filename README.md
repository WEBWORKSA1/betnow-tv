# BetNow.tv — Predict · Watch · Learn

Free sports predictions, odds-math education, official highlight videos and free-to-play prize contests. No wagering. Static site hosted on GitHub Pages (free plan, `main` branch), auto-built and auto-updated by GitHub Actions.

## How it works
- `scripts/build.py` generates all pages (layout in `scripts/layout.py`, blocks in `scripts/blocks.py`, guides in `scripts/articles.py`) plus `sitemap.xml`.
- `scripts/update_data.py` refreshes `data/fixtures.json` (fixtures + model probabilities) and `data/news.json` every 6 hours.
- `.github/workflows/update-data.yml` runs on every push and every 6 hours: fetch data → build → commit → deploy to Pages.
- All forms post to a private inbox via FormSubmit; the address is assembled at runtime and never appears in source.

## One-time setup
1. **Pages:** Settings → Pages → Source: **GitHub Actions** (the workflow tries to enable this automatically).
2. **FormSubmit activation:** the first form submission triggers a one-time "Activate form" email to the inbox. Click it once.
3. **Donation links:** paste PayPal / Buy Me a Coffee / Stripe / Patreon links into `assets/js/config.js`.
4. **Custom domain:** at the registrar add A records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` and `www` CNAME → `webworksa1.github.io`. Then Settings → Pages → Custom domain `betnow.tv` → Enforce HTTPS.
5. **AdSense:** add site `betnow.tv` in AdSense; `ads.txt` is already in place. Submit `https://betnow.tv/sitemap.xml` to Search Console.

## Edit content
Edit the files in `scripts/`, then push. The workflow rebuilds every page. Local build: `python3 scripts/build.py`.

See `PROMPT.md` (phase-wise build prompt) and `RESEARCH.md` (idea selection + 35-site benchmark).

## Trademark & copyright
BetNow.tv is an independent publication, not affiliated with any sportsbook, gaming operator or company using the name "BetNow" or similar marks. League and team names belong to their owners. Original content © BetNow.tv.
