/* Bet Tracker front end: plain JavaScript, no build step. */
"use strict";

const CFG = window.BT_CONFIG || {};
const $ = (s) => document.querySelector(s);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const fmt$ = (n) => (n < 0 ? "-$" : "$") + Math.abs(Number(n) || 0).toFixed(2);
const signed$ = (n) => (n > 0 ? "+" : "") + fmt$(n);

const SPORT_NAMES = { nba: "NBA", wnba: "WNBA", ncaab: "NCAAB", nfl: "NFL", ncaaf: "NCAAF", soccer: "Soccer", tennis: "Tennis", other: "Other", mixed: "Mixed" };
const TYPE_NAMES = { moneyline: "Moneyline", spread: "Spread", total: "Game total", team_total: "Team total", player_prop: "Player prop" };
const STATS = ["points", "rebounds", "assists", "threes", "pra", "pr", "pa", "ra", "steals", "blocks", "stocks", "turnovers",
  "passing_yards", "passing_tds", "completions", "pass_attempts", "interceptions", "rushing_yards", "rushing_attempts",
  "receiving_yards", "receptions", "rush_rec_yards", "touchdowns", "goals", "shots", "shots_on_target", "soccer_assists", "saves"];
const CHIP_TEXT = { won: "Won", lost: "Lost", push: "Push", void: "Void", winning: "Winning", losing: "Losing", tied: "Tied",
  live: "Live", pending: "Not started", unmatched: "Not found", unsupported: "Manual", error: "Retrying" };

const store = {
  get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch { return null; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* private mode: fine */ } },
  del(k) { try { localStorage.removeItem(k); } catch { /* ignore */ } },
};

let state = { slips: [], settings: { dailyGoal: 60, startingBankroll: 0 }, tab: "today", charts: {}, lastSync: null };

/* ------------------------------------------------------------------ auth (Cognito) */
const auth = {
  session: null, pendingEmail: null,
  async call(target, body) {
    const r = await fetch(`https://cognito-idp.${CFG.region}.amazonaws.com/`, {
      method: "POST",
      headers: { "Content-Type": "application/x-amz-json-1.1", "X-Amz-Target": `AWSCognitoIdentityProviderService.${target}` },
      body: JSON.stringify(body),
    });
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(friendlyAuthError(data));
    return data;
  },
  save(res) {
    const t = res.AuthenticationResult;
    const cur = store.get("bt_auth") || {};
    store.set("bt_auth", { id: t.IdToken, refresh: t.RefreshToken || cur.refresh, exp: Date.now() + (t.ExpiresIn - 60) * 1000 });
  },
  async signIn(email, password) {
    const res = await this.call("InitiateAuth", { AuthFlow: "USER_PASSWORD_AUTH", ClientId: CFG.clientId, AuthParameters: { USERNAME: email, PASSWORD: password } });
    if (res.ChallengeName === "NEW_PASSWORD_REQUIRED") { this.session = res.Session; this.pendingEmail = email; return "NEW_PASSWORD"; }
    this.save(res); return "OK";
  },
  async setNewPassword(pw) {
    const res = await this.call("RespondToAuthChallenge", { ChallengeName: "NEW_PASSWORD_REQUIRED", ClientId: CFG.clientId, Session: this.session,
      ChallengeResponses: { USERNAME: this.pendingEmail, NEW_PASSWORD: pw } });
    this.save(res);
  },
  async token() {
    const a = store.get("bt_auth");
    if (!a) return null;
    if (Date.now() < a.exp) return a.id;
    try {
      const res = await this.call("InitiateAuth", { AuthFlow: "REFRESH_TOKEN_AUTH", ClientId: CFG.clientId, AuthParameters: { REFRESH_TOKEN: a.refresh } });
      this.save(res); return store.get("bt_auth").id;
    } catch { store.del("bt_auth"); return null; }
  },
  signOut() { store.del("bt_auth"); location.reload(); },
};

function friendlyAuthError(d) {
  const t = (d.__type || "").split("#").pop();
  return ({
    NotAuthorizedException: "Wrong email or password.",
    UserNotFoundException: "Wrong email or password.",
    InvalidPasswordException: "Password needs at least 10 characters, including a number and a lowercase letter.",
    CodeMismatchException: "That code isn't right — check your email and try again.",
    ExpiredCodeException: "That code expired. Request a new one.",
    LimitExceededException: "Too many tries. Please wait a few minutes.",
    PasswordResetRequiredException: "Please reset your password with 'Forgot password?'.",
  })[t] || d.message || "Something went wrong. Please try again.";
}

/* ------------------------------------------------------------------ API */
async function api(method, path, body) {
  const tok = await auth.token();
  if (!tok) { showAuth(); throw new Error("Please sign in again."); }
  const r = await fetch(CFG.apiUrl + path, {
    method, headers: { Authorization: `Bearer ${tok}`, "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await r.json().catch(() => ({}));
  if (r.status === 401) { store.del("bt_auth"); showAuth(); throw new Error("Please sign in again."); }
  if (!r.ok) { const e = new Error(data.error || `Request failed (${r.status})`); e.data = data; throw e; }
  return data;
}

function toast(msg, ms = 2600) {
  const t = $("#toast"); t.textContent = msg; t.classList.remove("hidden");
  clearTimeout(toast.t); toast.t = setTimeout(() => t.classList.add("hidden"), ms);
}

/* ------------------------------------------------------------------ helpers */
const localDay = (iso) => { const d = new Date(iso); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`; };
const todayKey = () => localDay(new Date().toISOString());
const isSettled = (s) => s.status && s.status !== "open";
function slipSport(s) {
  const sp = [...new Set((s.legs || []).map((l) => l.sport || "other"))];
  return sp.length === 1 ? sp[0] : sp.length ? "mixed" : "other";
}
function legResult(l) {
  if (["won", "lost", "push", "void"].includes(l.manualResult)) return l.manualResult;
  const lv = l.live || {};
  if (["won", "lost"].includes(lv.status)) return lv.status;
  if (lv.status === "push" && lv.final) return "push";
  return null;
}
function legTitle(l) {
  const line = l.line === null || l.line === undefined || l.line === "" ? "" : Number(l.line);
  const ln = line === "" ? "" : (l.type === "spread" && line > 0 ? `+${line}` : `${line}`);
  switch (l.type) {
    case "player_prop": return `${l.player || "?"} ${l.side === "under" ? "Under" : "Over"} ${ln} ${l.stat ? l.stat.replace(/_/g, " ") : ""}`;
    case "spread": return `${l.team || "?"} ${ln}`;
    case "total": return `${l.side === "under" ? "Under" : "Over"} ${ln} — ${[l.team, l.opponent].filter(Boolean).join(" vs ")}`;
    case "team_total": return `${l.team || "?"} team total ${l.side === "under" ? "Under" : "Over"} ${ln}`;
    default: return `${l.team || l.selection || "?"} to win${l.opponent ? ` vs ${l.opponent}` : ""}`;
  }
}
function chip(status) { const s = status || "pending"; return `<span class="chip ${esc(s)}">${esc(CHIP_TEXT[s] || s)}</span>`; }
function slipStatusChip(s) {
  if (s.status && s.status !== "open") return chip(s.status);
  const ls = s.liveSummary || {};
  if (ls.missing) return chip("losing");
  if (ls.hitting) return chip("winning");
  return chip("live");
}

/* ------------------------------------------------------------------ rendering */
function slipCard(s, { actions = true } = {}) {
  const legs = (s.legs || []).map((l) => {
    const lv = l.live || {};
    const st = l.manualResult || lv.status || "pending";
    return `<div class="leg">${chip(st)}<div><div class="leg-title">${esc(legTitle(l))}</div>
      <div class="leg-detail">${esc(SPORT_NAMES[l.sport] || l.sport || "")}${l.odds ? ` · ${esc(l.odds)}` : ""}${lv.detail ? ` · ${esc(lv.detail)}` : ""}</div></div></div>`;
  }).join("");
  const settled = isSettled(s);
  const ls = s.liveSummary || {};
  const headline = settled ? "" : `<div class="headline">${ls.hitting || 0}/${ls.legs || (s.legs || []).length} legs hitting${ls.missing ? ` · ${ls.missing} behind` : ""}</div>`;
  const money = settled
    ? `<div class="${s.profit > 0 ? "pos" : s.profit < 0 ? "neg" : ""}">${signed$(s.profit)}</div>`
    : `<div>${fmt$(s.stake)} → ${fmt$(s.payout || 0)}</div>`;
  return `<div class="slip" data-id="${esc(s.slipId)}">
    <div class="slip-head"><div>${slipStatusChip(s)} <span class="meta">${esc(s.book || "")} · ${(s.legs || []).length}-leg · ${esc(localDay(s.placedAt || s.createdAt))}</span>${headline}</div>
      <div class="slip-money">${money}</div></div>
    ${legs}
    ${actions ? `<div class="slip-actions">
      <button class="btn small" data-act="edit">Edit</button>
      ${settled ? `<button class="btn small" data-act="reopen">Reopen</button>` : `<button class="btn small" data-act="won">Mark won</button><button class="btn small" data-act="lost">Mark lost</button>`}
      ${s.screenshotUrl ? `<a class="btn small" href="${esc(s.screenshotUrl)}" target="_blank" rel="noopener">Screenshot</a>` : ""}
      <button class="btn small danger" data-act="delete">Delete</button></div>` : ""}
  </div>`;
}

function renderList(el, list, emptyText) {
  el.innerHTML = list.length ? list.map((s) => slipCard(s)).join("") : `<div class="empty">${esc(emptyText)}</div>`;
}

function renderToday() {
  const tk = todayKey();
  const settledToday = state.slips.filter((s) => isSettled(s) && s.settledAt && localDay(s.settledAt) === tk);
  const profit = settledToday.reduce((a, s) => a + (s.profit || 0), 0);
  const goal = Number(state.settings.dailyGoal) || 0;
  $("#today-profit").textContent = signed$(profit);
  $("#today-profit").className = "big " + (profit > 0 ? "pos" : profit < 0 ? "neg" : "");
  $("#today-goal").textContent = fmt$(goal);
  const pct = goal > 0 ? Math.max(0, Math.min(100, (profit / goal) * 100)) : 0;
  const bar = $("#goal-bar"); bar.style.width = pct + "%"; bar.classList.toggle("done", goal > 0 && profit >= goal);
  const open = state.slips.filter((s) => !isSettled(s));
  const potential = open.reduce((a, s) => a + Math.max(0, (s.payout || 0) - (s.stake || 0)), 0);
  $("#goal-note").textContent = goal <= 0 ? "Set a daily goal in Settings." :
    profit >= goal ? "🎉 Goal reached for today. Nice work — protect it!" :
    `${fmt$(goal - profit)} to go.` + (open.length ? ` Open slips could add up to ${fmt$(potential)}.` : "");
  renderList($("#live-list"), open, "No live slips. Tap ➕ Add to upload a bet slip.");
  renderList($("#today-settled"), settledToday, "Nothing settled yet today.");
}

function renderHistory() {
  const st = $("#f-status").value, sp = $("#f-sport").value;
  const list = state.slips.filter((s) => (!st || (s.status || "open") === st) && (!sp || slipSport(s) === sp));
  renderList($("#history-list"), list, "No slips match.");
}

function table(rows, headers) {
  if (!rows.length) return `<div class="empty">No settled bets yet.</div>`;
  return `<table><tr>${headers.map((h, i) => `<th class="${i ? "num" : ""}">${esc(h)}</th>`).join("")}</tr>${
    rows.map((r) => `<tr>${r.map((c, i) => `<td class="${i ? "num" : ""}">${c}</td>`).join("")}</tr>`).join("")}</table>`;
}

function renderStats() {
  const settled = state.slips.filter(isSettled);
  const decided = settled.filter((s) => s.status === "won" || s.status === "lost");
  const profit = settled.reduce((a, s) => a + (s.profit || 0), 0);
  const staked = decided.reduce((a, s) => a + (s.stake || 0), 0);
  const wins = decided.filter((s) => s.status === "won").length;
  const legsAll = state.slips.flatMap((s) => (s.legs || []).map((l) => ({ ...l, result: legResult(l) }))).filter((l) => l.result === "won" || l.result === "lost");
  const legWins = legsAll.filter((l) => l.result === "won").length;
  $("#s-profit").textContent = signed$(profit); $("#s-profit").className = "mid " + (profit > 0 ? "pos" : profit < 0 ? "neg" : "");
  $("#s-winrate").textContent = decided.length ? `${Math.round((wins / decided.length) * 100)}% (${wins}-${decided.length - wins})` : "–";
  $("#s-roi").textContent = staked ? `${((profit / staked) * 100).toFixed(1)}%` : "–";
  $("#s-legrate").textContent = legsAll.length ? `${Math.round((legWins / legsAll.length) * 100)}% (${legWins}-${legsAll.length - legWins})` : "–";

  // by sport (slip profit by the slip's sport; leg record by leg sport)
  const bySport = {};
  for (const s of settled) { const k = slipSport(s); (bySport[k] ||= { p: 0, w: 0, l: 0, lw: 0, ll: 0 }).p += s.profit || 0; if (s.status === "won") bySport[k].w++; if (s.status === "lost") bySport[k].l++; }
  for (const l of legsAll) { const k = l.sport || "other"; (bySport[k] ||= { p: 0, w: 0, l: 0, lw: 0, ll: 0 }); l.result === "won" ? bySport[k].lw++ : bySport[k].ll++; }
  $("#by-sport").innerHTML = table(Object.entries(bySport).sort((a, b) => b[1].p - a[1].p).map(([k, v]) => [
    esc(SPORT_NAMES[k] || k), `${v.w}-${v.l}`, `${v.lw}-${v.ll}`, `<span class="${v.p > 0 ? "pos" : v.p < 0 ? "neg" : ""}">${signed$(v.p)}</span>`]),
    ["Sport", "Slips W-L", "Legs W-L", "Profit"]);

  const byType = {};
  for (const l of legsAll) { const k = l.type || "other"; (byType[k] ||= { w: 0, l: 0 }); l.result === "won" ? byType[k].w++ : byType[k].l++; }
  $("#by-type").innerHTML = table(Object.entries(byType).map(([k, v]) => [esc(TYPE_NAMES[k] || k), `${v.w}-${v.l}`, `${Math.round((v.w / (v.w + v.l)) * 100)}%`]),
    ["Bet type", "Legs W-L", "Hit rate"]);

  drawCharts(settled);
}

function cssVar(n) { return getComputedStyle(document.documentElement).getPropertyValue(n).trim(); }
function drawCharts(settled) {
  if (!window.Chart) return;
  const days = [];
  for (let i = 13; i >= 0; i--) { const d = new Date(); d.setDate(d.getDate() - i); days.push(localDay(d.toISOString())); }
  const perDay = Object.fromEntries(days.map((d) => [d, 0]));
  for (const s of settled) { const k = s.settledAt && localDay(s.settledAt); if (k in perDay) perDay[k] += s.profit || 0; }
  const goal = Number(state.settings.dailyGoal) || 0;
  const text = cssVar("--muted"), grid = cssVar("--line");
  const common = { responsive: true, maintainAspectRatio: false, animation: false, plugins: { legend: { labels: { color: text } } },
    scales: { x: { ticks: { color: text }, grid: { color: grid } }, y: { ticks: { color: text, callback: (v) => "$" + v }, grid: { color: grid } } } };
  state.charts.daily?.destroy();
  state.charts.daily = new Chart($("#c-daily"), {
    data: { labels: days.map((d) => d.slice(5)), datasets: [
      { type: "bar", label: "Profit", data: days.map((d) => +perDay[d].toFixed(2)),
        backgroundColor: days.map((d) => (perDay[d] >= goal && goal > 0 ? cssVar("--won") : perDay[d] < 0 ? cssVar("--lost") : cssVar("--accent"))) },
      { type: "line", label: "Goal", data: days.map(() => goal), borderColor: cssVar("--live"), borderDash: [6, 4], pointRadius: 0 }] },
    options: common,
  });
  const sorted = [...settled].sort((a, b) => (a.settledAt || "").localeCompare(b.settledAt || ""));
  let run = Number(state.settings.startingBankroll) || 0;
  const pts = [{ x: "start", y: run }, ...sorted.map((s) => ({ x: localDay(s.settledAt), y: +(run += s.profit || 0).toFixed(2) }))];
  state.charts.bank?.destroy();
  state.charts.bank = new Chart($("#c-bankroll"), {
    type: "line",
    data: { labels: pts.map((p) => p.x.slice(5)), datasets: [{ label: "Bankroll", data: pts.map((p) => p.y), borderColor: cssVar("--accent"), tension: .25, pointRadius: 2 }] },
    options: common,
  });
}

function render() {
  if (state.tab === "today") renderToday();
  if (state.tab === "history") renderHistory();
  if (state.tab === "stats") renderStats();
  $("#sync").textContent = state.lastSync ? `Updated ${state.lastSync.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" })}` : "—";
}

/* ------------------------------------------------------------------ data */
async function loadSlips() {
  const r = await api("GET", "/slips");
  state.slips = r.slips || []; state.lastSync = new Date(); render();
}
async function liveRefresh(manual) {
  if (!state.slips.some((s) => !isSettled(s))) { if (manual) toast("No live slips to check."); return; }
  const btn = $("#refresh-btn"); btn.disabled = true;
  try { await api("POST", "/refresh"); await loadSlips(); if (manual) toast("Live scores updated."); }
  catch (e) { if (manual) toast(e.message); }
  finally { btn.disabled = false; }
}

/* ------------------------------------------------------------------ slip form */
let draft = null;
function legEditor(l, i) {
  const opt = (vals, cur, names = {}) => vals.map((v) => `<option value="${esc(v)}" ${v === cur ? "selected" : ""}>${esc(names[v] || v.replace(/_/g, " "))}</option>`).join("");
  const isProp = l.type === "player_prop";
  return `<div class="leg-edit" data-i="${i}">
    <div class="row-between"><strong>Leg ${i + 1}</strong><button type="button" class="btn small danger" data-rm="${i}">Remove</button></div>
    ${l.selection ? `<p class="hint">On slip: “${esc(l.selection)}”</p>` : ""}
    <div class="grid2">
      <label>Sport <select data-f="sport">${opt(["nba", "nfl", "soccer", "tennis", "wnba", "ncaab", "ncaaf", "other"], l.sport, SPORT_NAMES)}</select></label>
      <label>Bet type <select data-f="type">${opt(Object.keys(TYPE_NAMES), l.type, TYPE_NAMES)}</select></label>
    </div>
    <div class="grid2 ${isProp ? "" : "hidden"}">
      <label>Player <input data-f="player" value="${esc(l.player)}"></label>
      <label>Stat <select data-f="stat">${opt(STATS, l.stat)}</select></label>
    </div>
    <div class="grid2">
      <label>${isProp ? "Player's team" : l.sport === "tennis" ? "Player you bet on" : "Team you bet on"} <input data-f="team" value="${esc(l.team)}" placeholder="${l.type === "moneyline" && l.sport === "soccer" ? "or Draw" : ""}"></label>
      <label>Opponent <input data-f="opponent" value="${esc(l.opponent)}"></label>
    </div>
    <div class="grid3">
      <label class="${["total", "team_total", "player_prop"].includes(l.type) ? "" : "hidden"}">Over/Under <select data-f="side">${opt(["over", "under"], l.side)}</select></label>
      <label class="${l.type === "moneyline" ? "hidden" : ""}">Line <input data-f="line" type="number" step="0.5" value="${l.line ?? ""}"></label>
      <label>Odds <input data-f="odds" value="${esc(l.odds)}" placeholder="-110"></label>
      <label>Game date <input data-f="gameDate" type="date" value="${esc(l.gameDate)}"></label>
    </div>
  </div>`;
}
function renderForm() {
  const f = $("#slip-form");
  f.innerHTML = `<h2>${draft.slipId ? "Edit slip" : "Check your slip"}</h2>
    <p class="hint">Make sure everything matches your screenshot. Teams and player names matter most for live tracking.</p>
    <div class="grid2">
      <label>Stake ($) <input name="stake" type="number" step="0.01" min="0" value="${draft.stake ?? ""}" required></label>
      <label>Total payout if it wins ($) <input name="payout" type="number" step="0.01" min="0" value="${draft.payout ?? ""}"></label>
      <label>Sportsbook <input name="book" value="${esc(draft.book)}"></label>
      <label>Overall odds <input name="odds" value="${esc(draft.odds)}" placeholder="+450"></label>
    </div>
    <div id="legs-edit">${(draft.legs || []).map(legEditor).join("")}</div>
    <button type="button" class="btn" id="add-leg">+ Add leg</button>
    <div class="form-actions"><button type="button" class="btn" id="cancel-slip">Cancel</button><button type="submit" class="btn primary">Save slip</button></div>`;
  f.classList.remove("hidden");
}
function readForm() {
  const f = $("#slip-form");
  for (const k of ["stake", "payout", "book", "odds"]) draft[k] = f.elements[k].value;
  f.querySelectorAll(".leg-edit").forEach((el) => {
    const l = draft.legs[+el.dataset.i];
    el.querySelectorAll("[data-f]").forEach((inp) => { l[inp.dataset.f] = inp.value; });
  });
}
function openForm(d) { draft = JSON.parse(JSON.stringify(d)); draft.legs ||= []; renderForm(); switchTab("add"); $("#slip-form").scrollIntoView({ behavior: "smooth" }); }
const blankLeg = () => ({ sport: "nba", type: "moneyline", side: "over", gameDate: todayKey() });

async function imageToDataUrl(file) {
  const img = await new Promise((res, rej) => { const i = new Image(); i.onload = () => res(i); i.onerror = rej; i.src = URL.createObjectURL(file); });
  const max = 1800, scale = Math.min(1, max / Math.max(img.width, img.height));
  const c = document.createElement("canvas"); c.width = Math.round(img.width * scale); c.height = Math.round(img.height * scale);
  c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
  return c.toDataURL("image/jpeg", 0.88);
}

/* ------------------------------------------------------------------ events */
function switchTab(tab) {
  state.tab = tab;
  document.querySelectorAll(".tab").forEach((t) => t.classList.toggle("hidden", t.id !== `tab-${tab}`));
  document.querySelectorAll(".tabs button").forEach((b) => b.classList.toggle("active", b.dataset.tab === tab));
  render(); window.scrollTo(0, 0);
}

function wire() {
  document.querySelectorAll(".tabs button").forEach((b) => b.addEventListener("click", () => switchTab(b.dataset.tab)));
  $("#refresh-btn").addEventListener("click", () => liveRefresh(true));
  $("#f-status").addEventListener("change", renderHistory);
  $("#f-sport").addEventListener("change", renderHistory);
  $("#signout").addEventListener("click", () => auth.signOut());

  $("#file").addEventListener("change", async (e) => {
    const file = e.target.files[0]; if (!file) return;
    const msg = $("#parse-status"); msg.textContent = "Reading your slip… (about 10 seconds)";
    try {
      const dataUrl = await imageToDataUrl(file);
      $("#preview").src = dataUrl; $("#preview").classList.remove("hidden");
      const r = await api("POST", "/parse", { image: dataUrl });
      msg.textContent = `Found ${r.draft.legs.length} leg(s). Check them below.`;
      openForm({ ...r.draft, placedAt: r.draft.placedAt || new Date().toISOString() });
    } catch (err) {
      msg.textContent = err.message;
      openForm({ legs: [blankLeg()], screenshotKey: err.data?.screenshotKey, placedAt: new Date().toISOString() });
    } finally { e.target.value = ""; }
  });
  $("#manual-btn").addEventListener("click", () => openForm({ legs: [blankLeg()], placedAt: new Date().toISOString() }));

  const form = $("#slip-form");
  form.addEventListener("change", (e) => { if (e.target.dataset.f === "type" || e.target.dataset.f === "sport") { readForm(); renderForm(); } });
  form.addEventListener("click", (e) => {
    if (e.target.id === "add-leg") { readForm(); draft.legs.push(blankLeg()); renderForm(); }
    if (e.target.dataset.rm !== undefined) { readForm(); draft.legs.splice(+e.target.dataset.rm, 1); renderForm(); }
    if (e.target.id === "cancel-slip") { form.classList.add("hidden"); $("#preview").classList.add("hidden"); $("#parse-status").textContent = ""; draft = null; }
  });
  form.addEventListener("submit", async (e) => {
    e.preventDefault(); readForm();
    if (!draft.legs.length) return toast("Add at least one leg.");
    const btn = form.querySelector("[type=submit]"); btn.disabled = true;
    try {
      if (draft.slipId) await api("PUT", `/slips/${encodeURIComponent(draft.slipId)}`, draft);
      else await api("POST", "/slips", draft);
      form.classList.add("hidden"); $("#preview").classList.add("hidden"); $("#parse-status").textContent = ""; draft = null;
      toast("Saved! Tracking it live now."); await loadSlips(); switchTab("today");
    } catch (err) { toast(err.message); } finally { btn.disabled = false; }
  });

  document.body.addEventListener("click", async (e) => {
    const act = e.target.dataset?.act; if (!act) return;
    const id = e.target.closest(".slip")?.dataset.id; const s = state.slips.find((x) => x.slipId === id); if (!s) return;
    try {
      if (act === "edit") return openForm(s);
      if (act === "delete") { if (!confirm("Delete this slip?")) return; await api("DELETE", `/slips/${encodeURIComponent(id)}`); }
      if (act === "won" || act === "lost") await api("PUT", `/slips/${encodeURIComponent(id)}`, { manualStatus: act });
      if (act === "reopen") await api("PUT", `/slips/${encodeURIComponent(id)}`, { manualStatus: "", legs: s.legs.map((l) => ({ ...l, manualResult: undefined, live: undefined })) });
      await loadSlips();
    } catch (err) { toast(err.message); }
  });

  $("#settings-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
      state.settings = await api("PUT", "/settings", { dailyGoal: $("#set-goal").value, startingBankroll: $("#set-bankroll").value });
      $("#settings-msg").textContent = "Saved ✓"; render();
    } catch (err) { $("#settings-msg").textContent = err.message; }
  });

  // auth screens
  const msg = (t) => { $("#auth-msg").textContent = t; };
  $("#login-form").addEventListener("submit", async (e) => {
    e.preventDefault(); msg("Signing in…");
    try {
      const r = await auth.signIn($("#login-email").value.trim(), $("#login-password").value);
      if (r === "NEW_PASSWORD") { $("#login-form").classList.add("hidden"); $("#newpw-form").classList.remove("hidden"); msg(""); }
      else start();
    } catch (err) { msg(err.message); }
  });
  $("#newpw-form").addEventListener("submit", async (e) => {
    e.preventDefault(); msg("Saving…");
    try { await auth.setNewPassword($("#newpw").value); start(); } catch (err) { msg(err.message); }
  });
  $("#forgot-link").addEventListener("click", () => { $("#login-form").classList.add("hidden"); $("#forgot-form").classList.remove("hidden"); $("#forgot-email").value = $("#login-email").value; msg(""); });
  $("#back-login").addEventListener("click", () => { $("#forgot-form").classList.add("hidden"); $("#login-form").classList.remove("hidden"); msg(""); });
  $("#send-code").addEventListener("click", async () => {
    try { await auth.call("ForgotPassword", { ClientId: CFG.clientId, Username: $("#forgot-email").value.trim() }); msg("If that email has an account, a code is on its way."); }
    catch (err) { msg(err.message); }
  });
  $("#forgot-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
      await auth.call("ConfirmForgotPassword", { ClientId: CFG.clientId, Username: $("#forgot-email").value.trim(), ConfirmationCode: $("#forgot-code").value.trim(), Password: $("#forgot-newpw").value });
      msg("Password reset. Sign in with your new password."); $("#back-login").click();
    } catch (err) { msg(err.message); }
  });
}

function showAuth() { $("#app").classList.add("hidden"); $("#auth").classList.remove("hidden"); }

let timers = [];
async function start() {
  $("#auth").classList.add("hidden"); $("#app").classList.remove("hidden");
  try {
    const [settings] = await Promise.all([api("GET", "/settings"), loadSlips()]);
    state.settings = { dailyGoal: 60, startingBankroll: 0, ...settings };
    $("#set-goal").value = state.settings.dailyGoal; $("#set-bankroll").value = state.settings.startingBankroll || "";
    render();
    liveRefresh(false);
  } catch (err) { toast(err.message); }
  timers.forEach(clearInterval);
  // While the page is open: re-read slips every 30s and ask for a fresh live check every 60s.
  timers = [
    setInterval(() => { if (!document.hidden) loadSlips().catch(() => {}); }, 30000),
    setInterval(() => { if (!document.hidden) liveRefresh(false); }, 60000),
  ];
}

document.addEventListener("DOMContentLoaded", async () => {
  wire();
  if (!CFG.apiUrl) { document.body.innerHTML = "<p style='padding:16px'>Missing config.js — deploy the site first.</p>"; return; }
  (await auth.token()) ? start() : showAuth();
});
