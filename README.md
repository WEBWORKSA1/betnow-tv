# BetNow.tv — Predict · Watch · Learn

Free sports predictions, odds-math education, official highlight videos and free-to-play prize contests. No wagering.

**Live:** https://betnow.tv (GitHub Pages, free plan, `main` branch, custom domain via `CNAME`).

## How it works
- Pages are plain HTML on `main`. GitHub Pages renders them with one shared layout (`_layouts/default.html`) and the lead-capture block (`_includes/lead.html`), so no build workflow is needed.
- Fixtures, model predictions and headlines load live in the visitor's browser from ESPN's public scoreboard and news feeds, and refresh on every visit.
- All forms post to a private inbox via FormSubmit. The address is assembled at runtime and never appears in the page source.
- `scripts/` holds the generator used to author the pages (`python3 scripts/build.py`), plus an optional data snapshot updater. These are excluded from the published site.

## To-do
1. **FormSubmit:** the first form submission sends a one-time "Activate form" email to the inbox. Click it once.
2. **Donations:** paste PayPal / Buy Me a Coffee / Stripe / Patreon links into `assets/js/config.js`.
3. **AdSense:** add the site `betnow.tv` in AdSense (`ads.txt` is already in place), then submit `https://betnow.tv/sitemap.xml` in Search Console.

See `PROMPT.md` (phase-wise build prompt) and `RESEARCH.md` (idea selection and 35-site benchmark).

## Trademark & copyright
BetNow.tv is an independent publication. It is not affiliated with any sportsbook, gaming operator or company using the name "BetNow" or similar marks. League and team names belong to their owners. Original content © BetNow.tv.
