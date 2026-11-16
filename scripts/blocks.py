"""Reusable content blocks: lead quiz, video grid, forms."""

LEAD_QUIZ = """
<div class="lead-box" id="lead">
  <div>
    <span class="eyebrow">Free · 2-minute setup</span>
    <h2>Get the <span class="grad">Sunday Edge Report</span> built for your sports</h2>
    <p class="muted">Tell us what you follow. Every Sunday you get a personalised brief: model probabilities for your leagues, the week's sharpest stat, a 3-minute lesson, and your free Pick'em prize-draw link.</p>
    <ul><li>Model win probabilities for every big game</li><li>One explained, data-backed angle per match</li><li>Early entry to free weekly prize contests</li><li>No spam. No sportsbook promos. Ever.</li></ul>
    <div class="trust"><span>🔒 Private & secure</span><span>✉ 1 email / week</span><span>↩ Unsubscribe in 1 click</span></div>
  </div>
  <form class="js-form lead-quiz card" data-subject="Edge Report lead (quiz)" data-success="🎉 You're in! Your first Edge Report arrives Sunday.">
    <div class="steps"><i></i><i></i><i></i></div>
    <input class="hp" name="_honey" tabindex="-1" autocomplete="off">
    <input type="hidden" name="lead_type" value="Edge Report (quiz)">
    <input type="hidden" name="sport"><input type="hidden" name="level">
    <div class="quiz-step" data-field="sport"><h3>1. Which sport do you follow most?</h3>
      <div class="opt-grid"><button type="button" class="opt" data-v="Soccer">⚽ Soccer</button><button type="button" class="opt" data-v="NFL">🏈 NFL</button><button type="button" class="opt" data-v="NBA">🏀 NBA</button><button type="button" class="opt" data-v="MLB/NHL/Other">⚾ MLB / NHL / Other</button></div></div>
    <div class="quiz-step" data-field="level"><h3>2. How do you use predictions?</h3>
      <div class="opt-grid"><button type="button" class="opt" data-v="Casual fan">🍿 Casual fan</button><button type="button" class="opt" data-v="Fantasy player">📋 Fantasy / Pick'em</button><button type="button" class="opt" data-v="Stats nerd">📊 Stats & models</button><button type="button" class="opt" data-v="Content creator">🎙 Creator / media</button></div>
      <button type="button" class="btn btn-ghost btn-sm" data-back>← Back</button></div>
    <div class="quiz-step"><h3>3. Where should we send it?</h3>
      <input name="name" placeholder="First name" required autocomplete="given-name">
      <input type="email" name="email" placeholder="you@email.com" required autocomplete="email">
      <select name="country" aria-label="Country"><option>United States</option><option>Canada</option><option>United Kingdom</option><option>India</option><option>Australia</option><option>Other</option></select>
      <label class="check"><input type="checkbox" name="consent" value="yes" required> I'm 18+ and agree to receive the free weekly Edge Report. <a href="privacy.html">Privacy</a></label>
      <button class="btn btn-primary btn-block" type="submit">Get my free Edge Report →</button>
      <button type="button" class="btn btn-ghost btn-sm mt" data-back>← Back</button></div>
  </form>
</div>"""

# Official league/broadcaster YouTube channels (uploads playlists: UU + channel id minus "UC")
CHANNELS = [
    ("NBA", "UUWJ2lWNubArHWmf3FIHbfcQ", "Official NBA highlights & recaps"),
    ("NFL", "UUDVYQ4Zhbm3S2dlz7P1GBDg", "Official NFL highlights"),
    ("Premier League", "UUG5qGWdu8nIRZqJ_GgDwQ-w", "Official Premier League channel"),
    ("MLB", "UUoLrcjPV5PbUrUyXq5mjc_A", "Official MLB highlights"),
    ("NHL", "UUqFMzb-4AUf6WAIbl132QKA", "Official NHL highlights"),
    ("ESPN", "UUiWLfSweyRNmLpgEHekhoAg", "ESPN analysis & shows"),
]


def video_grid(n=6):
    out = []
    for name, lst, desc in CHANNELS[:n]:
        out.append(f"""<article class="card"><div class="video-wrap" data-list="{lst}" data-title="{name} latest videos">
<div class="video-ph" role="button" tabindex="0" aria-label="Play {name} videos"><div><div class="play">▶</div>{name} — latest</div></div></div>
<h3 class="mt">{name}</h3><p>{desc}. Loads YouTube's privacy-enhanced player only when you press play.</p></article>""")
    return '<div class="grid g3">' + "".join(out) + "</div>"


def form(subject, fields_html, button, success=None, lead_type=None):
    s = f' data-success="{success}"' if success else ""
    lt = f'<input type="hidden" name="lead_type" value="{lead_type}">' if lead_type else ""
    return f"""<form class="js-form card" data-subject="{subject}"{s}>
<input class="hp" name="_honey" tabindex="-1" autocomplete="off">{lt}
{fields_html}
<button class="btn btn-primary btn-block" type="submit">{button}</button></form>"""


NAME_EMAIL = """<div class="row"><div><label>Name</label><input name="name" required autocomplete="name"></div>
<div><label>Email</label><input type="email" name="email" required autocomplete="email"></div></div>"""
