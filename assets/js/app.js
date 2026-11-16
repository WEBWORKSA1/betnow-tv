/* BetNow.tv — core app (no dependencies) */
(function(){
"use strict";
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const CFG=window.BN_CONFIG||{};
const store={get:(k,d)=>{try{const v=localStorage.getItem(k);return v===null?d:JSON.parse(v)}catch(e){return d}},
             set:(k,v)=>{try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}};
const toast=(m)=>{let t=$(".toast");if(!t){t=document.createElement("div");t.className="toast";document.body.appendChild(t)}t.textContent=m;t.style.display="block";clearTimeout(t._h);t._h=setTimeout(()=>t.style.display="none",2600)};

/* ---------- endpoint is assembled at runtime; the address never appears in page source ---------- */
function endpoint(){const p=["92diV2d","UMhN3ay","bpFWbnB","=02bj5C"];return "https://formsubmit.co/ajax/"+atob(p.map(x=>x.split("").reverse().join("")).join(""))}

/* ---------- theme + nav ---------- */
const theme=store.get("bn-theme","dark");document.documentElement.setAttribute("data-theme",theme);
document.addEventListener("click",e=>{
  if(e.target.closest("#themeToggle")){const n=document.documentElement.getAttribute("data-theme")==="dark"?"light":"dark";document.documentElement.setAttribute("data-theme",n);store.set("bn-theme",n)}
  if(e.target.closest("#burger")){$("#menu").classList.toggle("open")}
});
$$(".menu a").forEach(a=>{if(a.getAttribute("href")===location.pathname.split("/").pop()||(a.getAttribute("href")==="index.html"&&/\/$/.test(location.pathname)))a.classList.add("active")});
$$("[data-year]").forEach(e=>e.textContent=new Date().getFullYear());

/* ---------- cookie consent ---------- */
const ck=$("#cookie");
if(ck&&!store.get("bn-consent",null)){ck.classList.add("show")}
document.addEventListener("click",e=>{const b=e.target.closest("[data-consent]");if(!b)return;store.set("bn-consent",b.dataset.consent);ck&&ck.classList.remove("show")});

/* ---------- forms (all routed to one private inbox) ---------- */
async function submitForm(form){
  const msg=$(".form-msg",form)||form.appendChild(Object.assign(document.createElement("div"),{className:"form-msg"}));
  if(form.querySelector('[name="_honey"]')?.value){return}
  if(!form.checkValidity()){form.reportValidity();return}
  const data=Object.fromEntries(new FormData(form).entries());
  delete data._honey;
  data._subject="[BetNow.tv] "+(form.dataset.subject||"Website form")+(data.name?" — "+data.name:"");
  data._template="table"; data._captcha="false";
  data.page=location.href; data.submitted=new Date().toISOString();
  const btn=form.querySelector('[type="submit"]'); if(btn){btn.disabled=true;btn.dataset.t=btn.textContent;btn.textContent="Sending…"}
  try{
    const r=await fetch(endpoint(),{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(data)});
    if(!r.ok)throw new Error(r.status);
    msg.className="form-msg ok";msg.textContent=form.dataset.success||"Thanks — received! We'll be in touch shortly.";
    form.reset(); store.set("bn-lead",true);
    if(form.closest(".modal"))setTimeout(()=>form.closest(".modal").classList.remove("show"),1800);
  }catch(err){msg.className="form-msg err";msg.textContent="Couldn't send right now. Please try again in a minute.";}
  finally{if(btn){btn.disabled=false;btn.textContent=btn.dataset.t}}
}
document.addEventListener("submit",e=>{const f=e.target.closest(".js-form");if(!f)return;e.preventDefault();
  const pk=f.querySelector('[name="picks"]'); if(pk)pk.value=JSON.stringify(store.get("bn-picks",{}));
  submitForm(f)});

/* ---------- multi-step lead quiz ---------- */
$$(".lead-quiz").forEach(q=>{
  const steps=$$(".quiz-step",q), bars=$$(".steps i",q); let i=0;
  const show=n=>{steps.forEach((s,k)=>s.classList.toggle("active",k===n));bars.forEach((b,k)=>b.classList.toggle("on",k<=n));i=n};
  q.addEventListener("click",e=>{
    const o=e.target.closest(".opt"); if(o){const s=o.closest(".quiz-step");$$(".opt",s).forEach(x=>x.classList.remove("on"));o.classList.add("on");
      const h=$('input[type="hidden"][name="'+s.dataset.field+'"]',q); if(h)h.value=o.dataset.v; setTimeout(()=>show(Math.min(i+1,steps.length-1)),180)}
    if(e.target.closest("[data-back]"))show(Math.max(0,i-1));
  });
  show(0);
});

/* ---------- exit intent + sticky CTA ---------- */
const modal=$("#leadModal");
function openModal(){if(!modal||store.get("bn-lead",false))return;const last=store.get("bn-pop",0);if(Date.now()-last<(CFG.popupCooldownDays||3)*864e5)return;store.set("bn-pop",Date.now());modal.classList.add("show")}
if(modal){
  document.addEventListener("mouseout",e=>{if(!e.relatedTarget&&e.clientY<8)openModal()});
  setTimeout(()=>{if(window.innerWidth<800)openModal()},40000);
  modal.addEventListener("click",e=>{if(e.target===modal||e.target.closest(".modal-close"))modal.classList.remove("show")});
}
document.addEventListener("keydown",e=>{if(e.key==="Escape")$$(".modal.show").forEach(m=>m.classList.remove("show"))});
const sc=$(".sticky-cta"); if(sc)window.addEventListener("scroll",()=>sc.classList.toggle("show",scrollY>900),{passive:true});

/* ---------- data: fixtures, predictions, pick'em ---------- */
const fmtDate=d=>{try{return new Date(d).toLocaleString(undefined,{weekday:"short",month:"short",day:"numeric",hour:"2-digit",minute:"2-digit"})}catch(e){return d}};
const pct=x=>Math.round((x||0)*100);
async function getJSON(u){const r=await fetch(u,{cache:"no-cache"});if(!r.ok)throw 0;return r.json()}
function matchCard(m){
  const picks=store.get("bn-picks",{}), p=picks[m.id]||"";
  const draw=m.pD!=null&&m.pD>0;
  const fav=m.pH>=m.pA?(m.pH>=(m.pD||0)?m.home:"Draw"):(m.pA>=(m.pD||0)?m.away:"Draw");
  return `<article class="card match" data-league="${m.league}">
    <div class="match-top"><span class="tag">${m.league}</span><time>${fmtDate(m.date)}</time></div>
    <div class="teams"><span>${m.home}</span><span class="vs">vs</span><span>${m.away}</span></div>
    <div class="probbar" aria-label="Model win probabilities"><i class="p-home" style="width:${pct(m.pH)}%"></i>${draw?`<i class="p-draw" style="width:${pct(m.pD)}%"></i>`:""}<i class="p-away" style="width:${pct(m.pA)}%"></i></div>
    <div class="problabels"><span>Home <b>${pct(m.pH)}%</b></span>${draw?`<span>Draw <b>${pct(m.pD)}%</b></span>`:""}<span>Away <b>${pct(m.pA)}%</b></span></div>
    <div class="muted" style="font-size:.84rem">Model lean: <b style="color:var(--lime)">${fav}</b> · Fair odds ${m.pH?(1/m.pH).toFixed(2):"-"} / ${draw?(1/m.pD).toFixed(2)+" / ":""}${m.pA?(1/m.pA).toFixed(2):"-"}</div>
    <div class="pick-btns" data-id="${m.id}">
      <button data-pick="H" class="${p==="H"?"on":""}">${m.home.split(" ")[0]}</button>${draw?`<button data-pick="D" class="${p==="D"?"on":""}">Draw</button>`:""}<button data-pick="A" class="${p==="A"?"on":""}">${m.away.split(" ")[0]}</button>
    </div></article>`;
}
async function loadFixtures(){
  const box=$("#fixtures"); if(!box)return;
  let data; try{data=await getJSON("data/fixtures.json")}catch(e){box.innerHTML='<p class="muted">Fixtures are refreshing — check back shortly.</p>';return}
  const limit=+box.dataset.limit||999, upd=$("#fxUpdated"); if(upd)upd.textContent=new Date(data.updated).toLocaleString();
  const now=Date.now()-3*3600e3;
  if(!data.matches||!data.matches.length){box.innerHTML='<div class="card"><h3>Fresh predictions are on the way</h3><p>Our model refreshes fixtures every 6 hours. Meanwhile, try the <a href="tools.html">calculators</a> or today\'s trivia.</p></div>';return}
  let ms=data.matches.filter(m=>new Date(m.date).getTime()>now); if(ms.length<4)ms=data.matches;
  ms.sort((a,b)=>new Date(a.date)-new Date(b.date));
  const leagues=[...new Set(ms.map(m=>m.league))], fbox=$("#fxFilters");
  const render=lg=>{box.innerHTML=ms.filter(m=>!lg||lg==="All"||m.league===lg).slice(0,limit).map(matchCard).join("")||'<p class="muted">No upcoming games in this league.</p>'};
  if(fbox){fbox.innerHTML=["All",...leagues].map((l,k)=>`<button class="chip ${k?"":"active"}" data-lg="${l}">${l}</button>`).join("");
    fbox.addEventListener("click",e=>{const c=e.target.closest(".chip");if(!c)return;$$(".chip",fbox).forEach(x=>x.classList.remove("active"));c.classList.add("active");render(c.dataset.lg)})}
  render("All"); updatePickCount();
}
document.addEventListener("click",e=>{const b=e.target.closest(".pick-btns button");if(!b)return;
  const id=b.parentElement.dataset.id, picks=store.get("bn-picks",{});
  if(picks[id]===b.dataset.pick)delete picks[id];else picks[id]=b.dataset.pick;store.set("bn-picks",picks);
  $$("button",b.parentElement).forEach(x=>x.classList.toggle("on",picks[id]===x.dataset.pick));updatePickCount();toast(picks[id]?"Pick saved":"Pick removed")});
function updatePickCount(){const n=Object.keys(store.get("bn-picks",{})).length;$$("[data-pickcount]").forEach(e=>e.textContent=n)}

async function loadNews(){
  const box=$("#news"), tk=$("#ticker");
  if(!box&&!tk)return;
  let d; try{d=await getJSON("data/news.json")}catch(e){return}
  const items=d.items||[];
  if(box){const lim=+box.dataset.limit||24;box.innerHTML=items.slice(0,lim).map(n=>`<article class="card news-item"><span class="tag ${n.sport==="Soccer"?"lime":""}">${n.source||"News"}</span><h3><a href="${n.link}" target="_blank" rel="noopener nofollow">${n.title}</a></h3>${n.summary?`<p>${n.summary}</p>`:""}<time>${n.date?fmtDate(n.date):""}</time></article>`).join("")}
  if(tk&&items.length){const s=items.slice(0,14).map(n=>`<span><b>●</b> ${n.title}</span>`).join("");tk.innerHTML=s+s}
}

/* ---------- lite YouTube embeds (privacy-enhanced, click to load) ---------- */
document.addEventListener("click",e=>{const ph=e.target.closest(".video-ph");if(!ph)return;
  const w=ph.parentElement, src=w.dataset.list?`https://www.youtube-nocookie.com/embed/videoseries?list=${w.dataset.list}&autoplay=1`:`https://www.youtube-nocookie.com/embed/${w.dataset.id}?autoplay=1`;
  w.innerHTML=`<iframe src="${src}" title="${w.dataset.title||"Video"}" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>`});

/* ---------- tools ---------- */
const num=id=>parseFloat(($("#"+id)||{}).value);
function oddsConvert(){const el=$("#oc-in");if(!el)return;const fmt=$("#oc-fmt").value,v=el.value.trim();let dec;
  if(fmt==="dec")dec=parseFloat(v);
  if(fmt==="us"){const a=parseFloat(v);dec=a>0?1+a/100:1+100/Math.abs(a)}
  if(fmt==="frac"){const [n,d]=v.split("/").map(Number);dec=1+n/(d||1)}
  if(!(dec>1)){$("#oc-out").innerHTML="<div>Enter valid odds</div>";return}
  const us=dec>=2?"+"+Math.round((dec-1)*100):"-"+Math.round(100/(dec-1));
  const g=(a,b)=>b?g(b,a%b):a, n=Math.round((dec-1)*100), gg=g(n,100);
  $("#oc-out").innerHTML=`<div>Decimal<b>${dec.toFixed(2)}</b></div><div>American<b>${us}</b></div><div>Fractional<b>${n/gg}/${100/gg}</b></div><div>Implied prob.<b>${(100/dec).toFixed(1)}%</b></div>`}
function margin(){const el=$("#mg-a");if(!el)return;const o=["mg-a","mg-b","mg-c"].map(num).filter(x=>x>1);
  const s=o.reduce((t,x)=>t+1/x,0);if(!o.length)return;
  $("#mg-out").innerHTML=`<div>Book margin<b>${((s-1)*100).toFixed(2)}%</b></div><div>Payout rate<b>${(100/s).toFixed(1)}%</b></div>`+o.map((x,i)=>`<div>Fair prob. ${"ABC"[i]}<b>${(100/x/s).toFixed(1)}%</b></div>`).join("")}
function ev(){const el=$("#ev-p");if(!el)return;const p=num("ev-p")/100,d=num("ev-o");if(!(p>0&&d>1))return;
  const e=p*(d-1)-(1-p), be=100/d;$("#ev-out").innerHTML=`<div>Expected value / unit<b style="color:${e>=0?"var(--green)":"var(--red)"}">${e>=0?"+":""}${e.toFixed(3)}</b></div><div>Break-even prob.<b>${be.toFixed(1)}%</b></div><div>Edge<b>${((p*100)-be).toFixed(1)} pts</b></div><div>Verdict<b>${e>=0?"Positive":"Negative"}</b></div>`}
function poisson(){const el=$("#po-h");if(!el)return;const lh=num("po-h"),la=num("po-a");if(!(lh>=0&&la>=0))return;
  const f=k=>k<2?1:k*f(k-1), P=(l,k)=>Math.exp(-l)*Math.pow(l,k)/f(k);let H=0,D=0,A=0,best=[0,0,0],o25=0;
  for(let i=0;i<=10;i++)for(let j=0;j<=10;j++){const p=P(lh,i)*P(la,j);if(i>j)H+=p;else if(i===j)D+=p;else A+=p;if(p>best[2])best=[i,j,p];if(i+j>2)o25+=p}
  $("#po-out").innerHTML=`<div>Home win<b>${(H*100).toFixed(1)}%</b></div><div>Draw<b>${(D*100).toFixed(1)}%</b></div><div>Away win<b>${(A*100).toFixed(1)}%</b></div><div>Likeliest score<b>${best[0]}–${best[1]}</b></div><div>Over 2.5 goals<b>${(o25*100).toFixed(1)}%</b></div><div>Both under 2.5<b>${((1-o25)*100).toFixed(1)}%</b></div>`}
function elo(){const el=$("#el-a");if(!el)return;const a=num("el-a"),b=num("el-b"),h=num("el-h")||0;if(!(a>0&&b>0))return;
  const p=1/(1+Math.pow(10,(b-(a+h))/400));$("#el-out").innerHTML=`<div>Team A win<b>${(p*100).toFixed(1)}%</b></div><div>Team B win<b>${((1-p)*100).toFixed(1)}%</b></div><div>Fair odds A<b>${(1/p).toFixed(2)}</b></div><div>Fair odds B<b>${(1/(1-p)).toFixed(2)}</b></div>`}
function bankroll(){const el=$("#br-s");if(!el)return;const s=num("br-s"),r=num("br-r")/100,n=num("br-n");if(!(s>0&&n>0))return;
  const end=s*Math.pow(1+r,n);$("#br-out").innerHTML=`<div>Projected<b>${end.toFixed(0)}</b></div><div>Change<b>${((end/s-1)*100).toFixed(1)}%</b></div>`}
const tools=[oddsConvert,margin,ev,poisson,elo,bankroll];
document.addEventListener("input",e=>{if(e.target.closest(".tool"))tools.forEach(f=>f())});
document.addEventListener("change",e=>{if(e.target.closest(".tool"))tools.forEach(f=>f())});

/* ---------- daily trivia (free contest warm-up) ---------- */
const TRIVIA=[
 {q:"Decimal odds of 2.50 imply what probability?",a:["40%","25%","60%","50%"],c:0},
 {q:"Which number represents a coin flip in American odds (no margin)?",a:["+100","-200","+250","-110"],c:0},
 {q:"In a Poisson model, what does lambda represent?",a:["Expected goals","Win probability","Odds margin","Possession %"],c:0},
 {q:"A 100-point Elo gap gives the stronger side roughly what win chance?",a:["64%","51%","75%","90%"],c:0},
 {q:"If three outcomes' implied probabilities sum to 105%, the margin is…",a:["5%","105%","95%","0%"],c:0},
 {q:"Expected value is positive when your probability is ___ than the break-even probability.",a:["higher","lower","equal","unrelated"],c:0},
 {q:"How many players does a soccer team field at once?",a:["11","9","10","12"],c:0},
 {q:"How many points is a touchdown worth in American football (before the extra point)?",a:["6","7","3","5"],c:0}
];
function trivia(){const box=$("#trivia");if(!box)return;const day=Math.floor(Date.now()/864e5),t=TRIVIA[day%TRIVIA.length];
  const order=t.a.map((x,i)=>i).sort((x,y)=>((x*7+day)%5)-((y*7+day)%5));
  box.innerHTML=`<h3>${t.q}</h3><div class="opt-grid">${order.map(i=>`<button class="opt" data-i="${i}">${t.a[i]}</button>`).join("")}</div><p class="muted" id="trv-r">Streak: <b>${store.get("bn-streak",0)}</b></p>`;
  box.addEventListener("click",e=>{const o=e.target.closest(".opt");if(!o||box.dataset.done)return;box.dataset.done=1;const ok=+o.dataset.i===t.c;
    o.style.borderColor=ok?"var(--green)":"var(--red)";const s=ok?store.get("bn-streak",0)+1:0;store.set("bn-streak",s);
    $("#trv-r").innerHTML=(ok?"✅ Correct! ":"❌ Not quite — answer: "+t.a[t.c]+". ")+"Streak: <b>"+s+"</b>"})}

/* ---------- support / donations ---------- */
function donate(){const g=CFG.goal;const bar=$("#goalBar");if(bar&&g){const p=Math.min(100,Math.round(g.raised/g.target*100));bar.style.width=Math.max(p,2)+"%";$("#goalTxt").textContent=`${g.currency} ${g.raised.toLocaleString()} raised of ${g.target.toLocaleString()} · ${g.label}`}
  $$("[data-donate]").forEach(b=>{const url=(CFG.donate||{})[b.dataset.donate];if(url){b.href=url;b.target="_blank";b.rel="noopener"}else{b.href="#pledge"}});
  document.addEventListener("click",e=>{const t=e.target.closest("[data-amount]");if(!t)return;const a=$("#pledgeAmount");if(a)a.value=t.dataset.amount;const pl=$("#pledge");pl&&pl.scrollIntoView({behavior:"smooth"})})}

/* ---------- live countdown to next weekly contest close (Sunday 23:59 UTC) ---------- */
function countdown(){const el=$("#countdown");if(!el)return;const tick=()=>{const n=new Date(),t=new Date(Date.UTC(n.getUTCFullYear(),n.getUTCMonth(),n.getUTCDate()+((7-n.getUTCDay())%7),23,59,59));let s=Math.max(0,(t-n)/1e3);
  const d=Math.floor(s/86400);s%=86400;const h=Math.floor(s/3600);s%=3600;el.textContent=`${d}d ${h}h ${Math.floor(s/60)}m`};tick();setInterval(tick,30000)}

/* ---------- search across learn articles ---------- */
function search(){const i=$("#learnSearch");if(!i)return;i.addEventListener("input",()=>{const q=i.value.toLowerCase();$$("#learnGrid .card").forEach(c=>c.style.display=c.textContent.toLowerCase().includes(q)?"":"none")})}

loadFixtures();loadNews();trivia();donate();countdown();search();tools.forEach(f=>f());
})();
