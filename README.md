# Claude-code-

## Expert Trader agent

One agent that holds all ten roles from the *Copilot Trading Agents* pack (Master + 9 Specialists), so the whole trading desk runs inside a single conversation:

| # | Role | What it does inside the agent |
|---|------|-------------------------------|
| 00 | Trading Commander | Makes the final call: **TRADE / WATCH / PASS / HIGH-RISK** |
| 01 | Stock Hunter | Stocks and ETFs, with a 100-point evidence score |
| 02 | Options Sniper | Checks the underlying first, then the contract; prefers defined risk |
| 03 | Crypto Scout | BTC/ETH regime, funding, open interest, 24/7 volatility |
| 04 | Memecoin Defense | Safety review *before* any upside talk |
| 05 | Forex Sentinel | Chart structure plus macro events (CPI, NFP, central banks) |
| 06 | Risk Guardian | Tries to disprove the trade and has **veto** power |
| 07 | Catalyst Watcher | 🟢 GREEN / 🟡 YELLOW / 🔴 RED event-risk check |
| 08 | Trade Reviewer | Judges your *process*, not just the P&L |
| 09 | Backtest Lab | Tests whether a strategy actually has evidence behind it |

How a trade idea flows through it:

```
Your idea → Specialist → Catalyst Watcher → Risk Guardian → Commander → ONE decision
                                                                 ↓
                                        (after it closes) Trade Reviewer → Backtest Lab
```

### Files

| File | Use it for |
|------|------------|
| [`.claude/agents/expert-trader.md`](.claude/agents/expert-trader.md) | The full agent for **Claude Code** |
| [`copilot/expert-trader-copilot.md`](copilot/expert-trader-copilot.md) | A copy-paste version for **Microsoft 365 Copilot Agent Builder** (fits the 8,000-character limit) |

### How to use it in Claude Code

**Option A: start a session that *is* the Expert Trader**

```bash
cd Claude-code-
claude --agent expert-trader
```

**Option B: ask for it inside any Claude Code session in this repo**

> Use the expert-trader agent to review this trade idea: …

Things you can ask it:

- "Scan NVDA, AMD and TSLA and rank only the setups that qualify."
- "Risk-audit this trade: entry 50.00, stop 49.40, target 51.20. Account $1,500, risk 1%."
- "Run a safety-first review of this memecoin: <contract address>."
- "Analyze EUR/USD. Is it safe to trade around this week's data?"
- "Review my closed trade without judging me by the P&L alone."
- "Teach me how risk/reward works, with a picture and a practice question."

Tell it your **account size**, **risk per trade** (beginners usually use 0.5–1%), **daily loss limit** and **daily goal**. It will size every position for you and show the math.

### The rules it will never break

- It never makes up prices, news or data. If it can't verify something, it says so.
- A daily profit goal is a goal, never a reason to force a trade.
- It never raises risk to "make it back."
- **PASS counts as a win** when the edge isn't clear.
- Confidence measures evidence quality. It is **not** a promise of profit.

> This is a research and decision-support tool, not financial advice. No agent can remove market risk or guarantee profits. You make every final decision.
