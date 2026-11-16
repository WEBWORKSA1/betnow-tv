"""Original long-form guides for the Learn hub. Each: slug, title, desc, tag, minutes, html."""

ARTICLES = [
{"slug": "how-sports-odds-work", "title": "How Sports Odds Work: Decimal, American and Fractional Explained", "tag": "Basics", "min": 7,
 "desc": "A plain-English guide to the three odds formats, how to convert between them, and what each number really says about probability.",
 "html": """
<p>Every sports price is a probability wearing a costume. Once you can see through the costume, previews, pundit takes and prediction models all become easier to judge. This guide walks through the three formats you will meet — decimal, American and fractional — and shows how each one converts into the only number that matters: the chance of an outcome happening.</p>
<h2>Decimal odds</h2>
<p>Decimal odds are common in Europe, Canada, Australia and India. The number is the total return per 1 unit staked, including the stake itself. Odds of <b>2.50</b> mean a 1-unit stake returns 2.50 units (1.50 profit plus the original 1). The implied probability is simply <b>1 ÷ decimal odds</b>: 1 ÷ 2.50 = 0.40, or 40%.</p>
<p>That relationship is why analysts like decimal odds: they map onto probability with a single division. A favourite at 1.25 implies 80%; an outsider at 6.00 implies about 16.7%.</p>
<h2>American (moneyline) odds</h2>
<p>American odds pivot around 100. A <b>positive</b> number shows the profit on a 100 stake: +150 means 150 profit on 100. A <b>negative</b> number shows how much you must stake to make 100 profit: −200 means staking 200 to win 100.</p>
<ul><li>Positive odds → probability = 100 ÷ (odds + 100). For +150: 100 ÷ 250 = 40%.</li>
<li>Negative odds → probability = |odds| ÷ (|odds| + 100). For −200: 200 ÷ 300 = 66.7%.</li></ul>
<p>Note that +150 and 2.50 decimal describe exactly the same price — 40%.</p>
<h2>Fractional odds</h2>
<p>Traditional in the UK and Ireland, fractional odds show profit relative to stake. 3/2 means 3 profit for every 2 staked. Convert to decimal by dividing and adding one: 3 ÷ 2 + 1 = 2.50. Again: 40%.</p>
<div class="callout"><b>Shortcut:</b> convert anything to decimal first, then take 1 ÷ decimal to get probability. Our free <a href="../tools.html">odds converter</a> does this instantly.</div>
<h2>Why the probabilities add up to more than 100%</h2>
<p>If you convert every outcome of a market — home, draw, away — and add the implied probabilities, you will usually get something like 104–108%. The excess is the bookmaker's margin (also called overround or "vig"). It is how a price-maker earns regardless of the result. Removing it gives the <i>fair</i> probabilities, which is what we compare our models against. We explain the method in <a href="implied-probability-and-margin.html">Implied Probability and Margin</a>.</p>
<h2>Odds are opinions, not facts</h2>
<p>A price is a market's estimate, shaped by information, public sentiment and risk management. It can be wrong. That is exactly why independent, transparent models are interesting: they let you compare a data-driven estimate to the crowd's estimate and ask <i>why</i> they differ — injuries, schedule fatigue, travel, weather or simple popularity bias.</p>
<h2>Key takeaways</h2>
<ul><li>All three formats describe the same thing: probability.</li><li>Decimal → probability is 1 ÷ odds.</li><li>Market probabilities include a margin; strip it out for a fair view.</li><li>Use odds as a lens for understanding games — BetNow.tv is a free, no-wagering site, and our tools are for learning and analysis.</li></ul>
"""},
{"slug": "implied-probability-and-margin", "title": "Implied Probability and Margin: Finding the Fair Price", "tag": "Math", "min": 6,
 "desc": "Learn how to calculate the margin built into a market and remove it to reveal fair probabilities — with worked examples.",
 "html": """
<p>Implied probability is the chance of an outcome according to a price. Margin is the extra percentage built into a full market. Together they let you translate any line into a clean, fair forecast you can compare with a model.</p>
<h2>Step 1 — convert each outcome</h2>
<p>Take a soccer match priced at Home 2.10, Draw 3.40, Away 3.60. Implied probabilities are 1/2.10 = 47.6%, 1/3.40 = 29.4%, 1/3.60 = 27.8%.</p>
<h2>Step 2 — add them up</h2>
<p>47.6 + 29.4 + 27.8 = 104.8%. The margin is the amount above 100%: <b>4.8%</b>. The "payout rate" is 100 ÷ 104.8 = 95.4%, meaning that in the long run only 95.4% of money staked on this market would be returned across all outcomes.</p>
<h2>Step 3 — normalise to remove the margin</h2>
<p>The simplest approach (proportional normalisation) divides each implied probability by the total:</p>
<ul><li>Home: 47.6 ÷ 1.048 = 45.4%</li><li>Draw: 29.4 ÷ 1.048 = 28.1%</li><li>Away: 27.8 ÷ 1.048 = 26.5%</li></ul>
<p>These now sum to 100% and represent the market's fair view.</p>
<div class="callout">Try it yourself with the <a href="../tools.html#margin">margin calculator</a> — enter two or three prices and see the margin and fair probabilities update live.</div>
<h2>Better normalisation methods</h2>
<p>Proportional normalisation assumes the margin is spread evenly. In reality, longshots often carry more of it — the well-documented <b>favourite–longshot bias</b>. Analysts therefore use alternatives such as the "power" method (raising probabilities to an exponent until they sum to 1) or Shin's method, which models a share of informed money. For two-outcome markets the differences are small; for multi-runner markets (golf, racing, outrights) they can be large.</p>
<h2>Why this matters for prediction</h2>
<p>A prediction model is only interesting relative to a benchmark. If our model says the home side wins 52% and the fair market says 45%, that seven-point gap is a hypothesis worth investigating: is the model missing an injury, or is the market overreacting to a recent loss? Learning to compute fair probability is the first step in thinking like an analyst rather than a fan.</p>
<h2>Common mistakes</h2>
<ul><li>Comparing a model to raw (margin-included) probabilities — this makes every outcome look overpriced.</li><li>Ignoring the draw in soccer — two-way thinking in a three-way sport distorts every number.</li><li>Treating a single price as truth — prices move as information arrives.</li></ul>
"""},
{"slug": "expected-value-explained", "title": "Expected Value (EV) Explained for Sports Fans", "tag": "Math", "min": 6,
 "desc": "What expected value means, how to calculate it, and why positive EV still loses in the short run — a core concept in probability.",
 "html": """
<p>Expected value is the average result of a decision if you could repeat it thousands of times. It is the most important idea in any game of uncertainty, from poker theory to insurance pricing to fantasy sports roster decisions.</p>
<h2>The formula</h2>
<p>For a simple win/lose proposition at decimal odds <i>d</i> with your estimated probability <i>p</i>:</p>
<p class="callout"><b>EV per unit = p × (d − 1) − (1 − p)</b></p>
<p>Example: you believe an outcome happens 45% of the time and it is priced at 2.40. EV = 0.45 × 1.40 − 0.55 = 0.63 − 0.55 = <b>+0.08</b> per unit. On paper, that is a positive-expectation proposition.</p>
<h2>Break-even probability</h2>
<p>The break-even probability is just 1 ÷ d. At 2.40 it is 41.7%. If your honest estimate is above that, EV is positive; below, it is negative. The difference between your estimate and break-even is your "edge" in percentage points.</p>
<h2>The catch: your probability must be right</h2>
<p>EV is only as good as the probability you feed it. Most people overestimate their accuracy, especially on teams they support. That is why we publish model probabilities openly and track them — calibration (does a 60% forecast happen about 60% of the time?) is the honest test of any forecaster.</p>
<h2>Variance: why good decisions still lose</h2>
<p>A +8% EV proposition still loses 55% of the time in our example. Over 20 trials you can easily be behind. Over 2,000 trials, the average converges toward the expectation. This gap between short-run results and long-run expectation is called variance, and misunderstanding it is the root of most bad reasoning in sport — from "hot hands" to sacking a coach after three unlucky losses. Read more in <a href="variance-and-sample-size.html">Variance and Sample Size</a>.</p>
<h2>EV beyond wagering</h2>
<p>EV thinking applies to free Pick'em contests, fantasy drafts (is the third running back worth more than the second receiver?), coaching decisions (fourth-down attempts in the NFL are a famous EV debate) and business. BetNow.tv is a no-wagering site: we teach EV as a thinking tool. Try our <a href="../tools.html#ev">EV calculator</a>.</p>
<div class="callout"><span class="badge-18">18+</span>If you choose to gamble elsewhere, remember that market margins make long-run positive EV extremely rare. See our <a href="../responsible-gaming.html">responsible gaming</a> page.</div>
"""},
{"slug": "poisson-soccer-predictions", "title": "How Poisson Models Predict Soccer Scores", "tag": "Models", "min": 8,
 "desc": "A step-by-step guide to the Poisson distribution for soccer: expected goals, scoreline probabilities and its known weaknesses.",
 "html": """
<p>Goals in soccer are rare, roughly independent events — which makes them a natural fit for the Poisson distribution. With just two numbers, each team's expected goals, a Poisson model produces a probability for every possible scoreline, and from those, win/draw/loss and over/under figures.</p>
<h2>Step 1 — estimate expected goals (λ)</h2>
<p>A simple approach uses attack and defence strength relative to league average:</p>
<ul><li><b>Home attack strength</b> = home team's home goals per game ÷ league average home goals.</li>
<li><b>Away defence strength</b> = away team's goals conceded away ÷ league average away goals conceded.</li>
<li><b>Home λ</b> = home attack × away defence × league average home goals.</li></ul>
<p>Repeat in reverse for the away side. Modern analysts often replace raw goals with xG (expected goals from shot quality), which is more stable over small samples.</p>
<h2>Step 2 — scoreline probabilities</h2>
<p>The probability a team scores exactly <i>k</i> goals is e<sup>−λ</sup> λ<sup>k</sup> ÷ k!. Multiply the home and away probabilities for each pair to get a grid of scorelines — 0–0, 1–0, 1–1 and so on.</p>
<h2>Step 3 — aggregate</h2>
<p>Sum cells where home goals exceed away goals for a home win, the diagonal for a draw, and the rest for an away win. Sum cells where total goals exceed 2 for "over 2.5". Our <a href="../tools.html#poisson">Poisson predictor</a> does all of this live.</p>
<div class="callout"><b>Worked example:</b> Home λ = 1.6, Away λ = 1.1 gives roughly Home 49%, Draw 25%, Away 26%, with 1–1 the single likeliest score and 1–0 close behind.</div>
<h2>Known weaknesses</h2>
<ul><li><b>Draws are underestimated.</b> Low scores are slightly correlated (game states, tactics). The Dixon–Coles adjustment (1997) corrects low-score cells.</li>
<li><b>Team strength changes.</b> Weighting recent matches more heavily (time decay) helps.</li>
<li><b>Context is missing.</b> Injuries, rotation, motivation and weather are not in the raw numbers.</li></ul>
<h2>Why it is still useful</h2>
<p>Poisson models are transparent, fast and surprisingly competitive as a baseline. They are a superb learning tool: every assumption is visible, so you can see exactly why a model disagrees with consensus. Our daily soccer predictions on the <a href="../predictions.html">Predictions</a> page use a Poisson-style approach built from current league tables.</p>
"""},
{"slug": "elo-ratings-explained", "title": "Elo Ratings Explained: From Chess to the NBA", "tag": "Models", "min": 6,
 "desc": "How Elo ratings work, how to convert rating gaps into win probabilities, and how sports analysts adapt Elo for home advantage and margin.",
 "html": """
<p>Arpad Elo designed his rating system for chess in the 1960s. Today variants power rankings in soccer, American football, basketball, esports and more, because the core idea is elegant: every result moves ratings by an amount proportional to how surprising it was.</p>
<h2>The win-probability formula</h2>
<p>For teams A and B with ratings R<sub>A</sub> and R<sub>B</sub>:</p>
<p class="callout"><b>P(A wins) = 1 ÷ (1 + 10<sup>(R<sub>B</sub> − R<sub>A</sub>) / 400</sup>)</b></p>
<p>A 100-point gap gives the stronger side about 64%; 200 points ≈ 76%; 400 points ≈ 91%.</p>
<h2>Updating after a game</h2>
<p>New rating = old rating + K × (actual result − expected result), where the result is 1 for a win, 0.5 for a draw and 0 for a loss. K controls how fast ratings react: high K for short seasons (NFL), lower K for long ones (NBA, MLB).</p>
<h2>Sports-specific tweaks</h2>
<ul><li><b>Home advantage:</b> add a fixed bonus to the home side's rating before computing probability (often 50–100 points depending on sport).</li>
<li><b>Margin of victory:</b> scale K by a function of the score margin so blowouts count more, with an autocorrelation adjustment so favourites are not over-rewarded.</li>
<li><b>Season reversion:</b> pull ratings partway toward the mean between seasons to reflect roster turnover.</li></ul>
<p>Try it with our <a href="../tools.html#elo">Elo probability calculator</a>, including a home-advantage input.</p>
<h2>Strengths and limits</h2>
<p>Elo needs only results, so it works in any sport with a schedule. It self-corrects and is easy to explain. Its limits: it does not know about injuries or trades until results arrive, and it treats every game as equally informative unless you adjust K. Good analysts combine Elo with player-level data for a fuller picture.</p>
"""},
{"slug": "home-advantage-by-sport", "title": "Home Advantage: How Much Is It Worth in Each Sport?", "tag": "Data", "min": 5,
 "desc": "What research says about home advantage across soccer, the NFL, NBA, NHL and MLB — and what changed when crowds disappeared in 2020.",
 "html": """
<p>Home advantage is one of the most studied effects in sport. It is real, it differs by sport, and it has been shrinking for decades. Here is what the evidence shows and how models use it.</p>
<h2>Approximate home win rates</h2>
<table><thead><tr><th>Sport</th><th>Typical home win share (historical)</th></tr></thead><tbody>
<tr><td>Soccer (top European leagues)</td><td>~45% wins, ~26% draws</td></tr>
<tr><td>NBA</td><td>~57–60%</td></tr><tr><td>NFL</td><td>~55–57%</td></tr>
<tr><td>NHL</td><td>~54–55%</td></tr><tr><td>MLB</td><td>~53–54%</td></tr></tbody></table>
<p class="muted" style="font-size:.88rem">Ranges summarise long-run historical figures widely reported in sports-analytics literature; exact values vary by season and league.</p>
<h2>Where does it come from?</h2>
<ul><li><b>Officiating bias:</b> studies of soccer referees suggest crowd noise nudges marginal decisions (fouls, added time).</li>
<li><b>Travel and fatigue:</b> especially in the NBA and NHL with back-to-back games and time-zone changes.</li>
<li><b>Familiarity:</b> MLB parks differ physically; altitude matters in Denver for several sports.</li></ul>
<h2>The empty-stadium natural experiment</h2>
<p>When games were played without fans in 2020, several studies of European soccer found home advantage dropped noticeably, with referee foul and card counts becoming more balanced — strong evidence that crowds drive a meaningful share of the effect.</p>
<h2>How models use it</h2>
<p>Elo models add a rating bonus to the home side; Poisson models use separate home and away scoring rates. Our <a href="../predictions.html">predictions</a> include a sport-specific home factor. Good practice is to re-estimate it every season, because the long-term trend has been a gradual decline.</p>
"""},
{"slug": "variance-and-sample-size", "title": "Variance and Sample Size: Why Short-Term Results Lie", "tag": "Mindset", "min": 6,
 "desc": "Why streaks, small samples and luck mislead fans and pundits — and how to judge forecasts and teams more honestly.",
 "html": """
<p>Ten games is not a trend. Neither is a five-game streak. Understanding variance protects you from the most common analytical mistakes in sport — and from poor decisions with money.</p>
<h2>A simple simulation</h2>
<p>Imagine a forecaster who is genuinely right 55% of the time. Over 20 predictions, the chance they go 50% or worse is roughly one in three. Over 100 predictions it is about one in six. Only over several hundred does skill reliably separate from noise. The same maths applies to teams: a true 0.550 baseball team can easily post a .450 month.</p>
<h2>Regression to the mean</h2>
<p>Extreme results tend to be followed by less extreme ones, because extremes usually involve some luck. A striker converting 30% of shots will usually fall back toward the league norm; a goalkeeper saving everything usually cools down. Metrics like xG, shot quality and point differential are "stickier" than wins and goals, which is why analysts lean on them.</p>
<h2>How to judge forecasts</h2>
<ul><li><b>Calibration:</b> do 70% predictions come true about 70% of the time?</li>
<li><b>Brier score / log loss:</b> scoring rules that reward confident correct forecasts and punish confident wrong ones.</li>
<li><b>Sample size:</b> demand hundreds of forecasts before believing anyone's record — including ours.</li></ul>
<h2>The human side</h2>
<p>Our brains are pattern detectors and hate randomness. We remember the dramatic win and forget the quiet losses. This is why chasing losses and "due" thinking are dangerous: past independent results do not make the next one more likely. If you ever feel the urge to recover losses, step away — see our <a href="../responsible-gaming.html">responsible gaming resources</a>.</p>
<div class="callout"><b>Rule of thumb:</b> before reacting to any streak, ask "how many games, and what would luck alone produce?"</div>
"""},
{"slug": "reading-advanced-stats", "title": "Reading Advanced Stats: xG, EPA, Net Rating and Corsi", "tag": "Data", "min": 7,
 "desc": "A beginner-friendly tour of the advanced metrics analysts use in soccer, the NFL, NBA and NHL — what they measure and when to trust them.",
 "html": """
<p>Advanced stats exist because traditional box scores mix skill with luck. Each sport has developed metrics that isolate the repeatable parts of performance. Here are the essentials.</p>
<h2>Soccer: expected goals (xG)</h2>
<p>xG assigns each shot a probability of scoring based on historical shots with similar location, angle, body part and assist type. A penalty is roughly 0.76 xG; a long-range strike might be 0.03. Summing a team's xG shows the quality of chances it created, regardless of finishing luck. Over a season, xG difference predicts future results better than actual goal difference.</p>
<h2>NFL: expected points added (EPA)</h2>
<p>Every down-distance-field position has an expected point value. EPA measures how much a play changed it. A 15-yard completion on 3rd-and-10 adds a lot; a 3-yard run on 3rd-and-10 subtracts. EPA per play is the standard efficiency metric for offences and quarterbacks, often paired with success rate.</p>
<h2>NBA: net rating and true shooting</h2>
<ul><li><b>Offensive / defensive rating:</b> points scored or allowed per 100 possessions, removing pace.</li>
<li><b>Net rating:</b> the difference — the best single number for team quality.</li>
<li><b>True shooting %:</b> scoring efficiency including threes and free throws.</li></ul>
<h2>NHL: Corsi, Fenwick and xGF%</h2>
<p>Corsi counts all shot attempts for minus against while a team or player is on ice; Fenwick excludes blocked shots. Expected goals for percentage (xGF%) weights attempts by quality. These possession proxies are far more stable than goals in a low-scoring sport.</p>
<h2>MLB: wOBA, FIP and run differential</h2>
<p>wOBA weights each offensive outcome by its run value; FIP judges pitchers on strikeouts, walks and home runs — outcomes they control most. Pythagorean expectation turns run differential into an expected win percentage.</p>
<h2>When to trust them</h2>
<p>Advanced metrics still need sample size, and they have blind spots (defensive positioning, game state). Use them to ask better questions, not to end debates. Our <a href="../predictions.html">predictions</a> and <a href="../tools.html">tools</a> are built on these ideas.</p>
"""},
{"slug": "pickem-contest-strategy", "title": "Free Pick'em Contest Strategy: How to Win More Often", "tag": "Contests", "min": 5,
 "desc": "Data-driven strategy for free prediction contests: when to follow the favourite, when to be contrarian, and how pool size changes everything.",
 "html": """
<p>Free Pick'em contests reward getting results right, but winning a contest is different from maximising correct picks. Strategy depends on scoring rules and how many people you compete against.</p>
<h2>Small pools: maximise accuracy</h2>
<p>With a handful of rivals, the player with the most correct picks usually wins. Pick the side with the higher probability in every game — our <a href="../predictions.html">model probabilities</a> are a good starting point.</p>
<h2>Large pools: differentiate</h2>
<p>With thousands of entrants, many people pick the same favourites, so matching the crowd guarantees you will tie with hundreds. To finish first you need correct picks others missed. The smart approach is selective contrarianism: choose a few close games (45–55% on the model) where the public heavily favours one side, and take the other.</p>
<h2>Confidence-point formats</h2>
<p>When you rank games by confidence, assign your highest points to the largest probability gaps, not your favourite team. Avoid putting top points on coin flips.</p>
<h2>Track your calibration</h2>
<p>Write down a probability for each pick. After a season, check how often your 60% picks came true. This is the fastest way to improve — and it is how professional forecasters train.</p>
<div class="callout">Ready to practise? Make your picks on the <a href="../predictions.html">Predictions</a> page, then enter them in this week's <a href="../contests.html">free contest</a>. No purchase necessary.</div>
"""},
]
