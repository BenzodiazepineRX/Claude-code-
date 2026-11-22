/* Backup slip reader: runs entirely in the browser (Tesseract OCR + simple rules).
   Used only when the AWS AI reader is unavailable. Results are a best guess for the user to check. */
"use strict";

const OCR_LIB = "https://cdn.jsdelivr.net/npm/tesseract.js@5.1.1/dist/tesseract.min.js";

function loadScript(src) {
  return new Promise((res, rej) => {
    if (document.querySelector(`script[src="${src}"]`)) return res();
    const s = document.createElement("script"); s.src = src; s.onload = res; s.onerror = () => rej(new Error("Couldn't load the backup reader."));
    document.head.appendChild(s);
  });
}

async function ocrImage(dataUrl, onProgress) {
  await loadScript(OCR_LIB);
  const { data } = await window.Tesseract.recognize(dataUrl, "eng", {
    logger: (m) => { if (m.status === "recognizing text" && onProgress) onProgress(Math.round(m.progress * 100)); },
  });
  return data.text || "";
}

const STAT_WORDS = [
  [/pts\s*\+\s*reb\s*\+\s*ast|points\s*\+\s*rebounds\s*\+\s*assists|\bpra\b/i, "pra", "nba"],
  [/pts\s*\+\s*reb|points\s*\+\s*rebounds/i, "pr", "nba"], [/pts\s*\+\s*ast|points\s*\+\s*assists/i, "pa", "nba"],
  [/reb\s*\+\s*ast|rebounds\s*\+\s*assists/i, "ra", "nba"],
  [/3[-\s]?(pt|pointers?|point field goals)|threes|3pm/i, "threes", "nba"],
  [/passing\s+yds|passing\s+yards|pass\s+yds/i, "passing_yards", "nfl"], [/passing\s+(td|touchdowns)/i, "passing_tds", "nfl"],
  [/rush(ing)?\s*\+\s*rec(eiving)?\s+(yds|yards)/i, "rush_rec_yards", "nfl"],
  [/rushing\s+(yds|yards)|rush\s+yds/i, "rushing_yards", "nfl"], [/receiving\s+(yds|yards)|rec\s+yds/i, "receiving_yards", "nfl"],
  [/receptions/i, "receptions", "nfl"], [/completions/i, "completions", "nfl"], [/anytime\s+(td|touchdown)/i, "touchdowns", "nfl"],
  [/shots\s+on\s+(goal|target)|\bsot\b/i, "shots_on_target", "soccer"], [/\bshots\b/i, "shots", "soccer"],
  [/anytime\s+(goal|scorer)|\bgoals\b/i, "goals", "soccer"],
  [/rebounds|\breb\b/i, "rebounds", "nba"], [/assists|\bast\b/i, "assists", "nba"], [/steals/i, "steals", "nba"],
  [/blocks/i, "blocks", "nba"], [/points|\bpts\b/i, "points", "nba"],
];

const money = (s) => parseFloat(String(s).replace(/[,$\s]/g, ""));
const fixMinus = (s) => s.replace(/[−–—]/g, "-");

function guessSlip(rawText) {
  const text = fixMinus(rawText);
  const lines = text.split(/\n+/).map((l) => l.trim()).filter(Boolean);
  const draft = { legs: [] };

  const stake = text.match(/(?:wager|stake|risk|bet amount|entry|amount)[^\d$\n]{0,15}\$?\s?(\d[\d,]*(?:\.\d{1,2})?)/i);
  if (stake) draft.stake = money(stake[1]);
  const pay = text.match(/(?:to pay|payout|potential (?:payout|return)|total (?:payout|return)|returns?)[^\d$\n]{0,15}\$?\s?(\d[\d,]*(?:\.\d{1,2})?)/i);
  const toWin = text.match(/(?:to win|potential win(?:nings)?)[^\d$\n]{0,15}\$?\s?(\d[\d,]*(?:\.\d{1,2})?)/i);
  if (pay) draft.payout = money(pay[1]);
  else if (toWin && draft.stake) draft.payout = +(money(toWin[1]) + draft.stake).toFixed(2);
  for (const book of ["FanDuel", "DraftKings", "BetMGM", "Caesars", "PrizePicks", "Underdog", "ESPN BET", "Fanatics", "bet365", "Hard Rock"]) {
    if (new RegExp(book.replace(" ", "\\s*"), "i").test(text)) { draft.book = book; break; }
  }

  let matchup = null;
  lines.forEach((line, i) => {
    const mu = line.match(/^(.{3,40}?)\s+(?:@|at|vs\.?|v)\s+(.{3,40}?)$/i);
    if (mu && !/over|under/i.test(line)) { matchup = { a: mu[1].trim(), b: mu[2].trim() }; return; }

    const odds = (line.match(/(?:^|\s)([+-]\d{3,4})(?=\s|$)/) || [])[1] || "";
    const ou = line.match(/\b(over|under|o|u)\s*(\d+(?:\.\d)?)\b/i);
    if (ou) {
      const side = /^u/i.test(ou[1]) ? "under" : "over";
      const line_ = parseFloat(ou[2]);
      const context = `${line} ${lines[i + 1] || ""}`;
      const stat = STAT_WORDS.find(([re]) => re.test(context));
      if (stat) {
        // player name: words before "Over/Under" on this line, else the previous line
        let player = line.slice(0, ou.index).replace(/[^A-Za-z.' -]/g, "").trim();
        if (player.split(" ").length < 2) player = (lines[i - 1] || "").replace(/[^A-Za-z.' -]/g, "").trim();
        draft.legs.push({ selection: line, sport: stat[2], type: "player_prop", player, stat: stat[1], side, line: line_, odds,
          team: "", opponent: "" });
      } else {
        draft.legs.push({ selection: line, sport: "nba", type: "total", side, line: line_, odds,
          team: matchup?.a || "", opponent: matchup?.b || "" });
      }
      return;
    }
    const spread = line.match(/^([A-Z][A-Za-z .'&]{2,40}?)\s+([+-]\d{1,2}(?:\.5)?)(?:\s|$)/);
    if (spread && Math.abs(parseFloat(spread[2])) < 40) {
      draft.legs.push({ selection: line, sport: "nba", type: "spread", team: spread[1].trim(), line: parseFloat(spread[2]), odds,
        opponent: matchup ? (spread[1].includes(matchup.a) ? matchup.b : matchup.a) : "" });
      return;
    }
    if (/moneyline|\bml\b|to win/i.test(line)) {
      const team = line.replace(/moneyline|\bml\b|to win|[+-]\d{3,4}/gi, "").trim() || (lines[i - 1] || "");
      draft.legs.push({ selection: line, sport: "nba", type: "moneyline", team, odds, opponent: matchup?.b || "" });
    }
  });

  // fill team/opponent on legs from the nearest matchup if missing
  for (const l of draft.legs) {
    if (!l.team && matchup) { l.team = matchup.a; l.opponent = matchup.b; }
    if (/sets?|games?\b/i.test(text) && /tennis|atp|wta/i.test(text)) l.sport = "tennis";
    if (/\bnfl\b/i.test(text) && l.type !== "player_prop") l.sport = "nfl";
    if (/premier league|la ?liga|serie a|bundesliga|mls|champions league|soccer/i.test(text) && l.type !== "player_prop") l.sport = "soccer";
    l.gameDate = new Date().toISOString().slice(0, 10);
  }
  return draft;
}

window.backupReader = { ocrImage, guessSlip };
