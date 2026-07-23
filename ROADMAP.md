# Master Build Roadmap — 3 Pathways
Last updated: 2026-07-23

---

## THE BIG PICTURE — 3 Pathways

```
PATHWAY 1 — Goofy Screener (live ✅)
  US/ASX/JPX stock screener · paper trading · ML signals
  → Audience: retail traders, quant-curious people globally

PATHWAY 2 — International Student Finance (building now 🔨)
  Super calculator · Tax estimator · Money transfer · Work rights
  → Audience: international students in Australia (Japanese-first)

PATHWAY 3 — JPX Gateway (planned, ~month 3+)
  Japanese stocks in full English · screener + fundamentals
  → Audience: non-Japanese speakers who want to invest in Japan
      (expats, English-speaking investors, students returning to Japan)
```

HOW THEY CONNECT:
  Pathway 2 user (Japanese student in AU) finishes degree
    → claims super using Pathway 2 tools
    → sends money home via Wise (Pathway 2 referral)
    → wants to invest in Japanese stocks
    → lands on Pathway 3 (JPX Gateway in English)
    → Pathway 3 uses Pathway 1's screener data as the engine

This is one ecosystem, built in 3 stages. Each pathway stands alone,
but they reinforce each other and share the same audience.

---

---

## PROJECT 1 — Goofy Screener Website
**What it is:** Live paper-trading screener. 313 stocks, US/ASX/JPX. 15 strategies tested on each.
Walk-forward backtest, market regime filter, XGBoost ML gate, Kelly sizing.
**Repo:** GoofyisDAWG/goofy-screener-website
**Status:** Live on Streamlit Cloud ✅

### Already Built ✅
- [x] Phase 10 — Walk-forward engine (R28-R33)
- [x] Phase 11 — ML gate + regime filter + Kelly sizing (R34-R36)
- [x] Live website with Home, Stock Chart, Screener, Portfolio, Closed Trades, Strategy Breakdown
- [x] Bilingual EN/JA
- [x] Mobile CSS
- [x] Visual "How it works" pipeline
- [x] Price data bug fix (TTL mismatch)

### Next Up 🔜
- [ ] **Phase 12 — Email waitlist / notify me**
      One text input on the home page. User enters email. Stored in a Google Sheet
      via st.secrets + gspread. Send a Mailchimp/Resend email when a new signal fires.
      Goal: first 100 subscribers. No money, just building an audience.

- [ ] **Phase 13 — New strategy research**
      Wait 4-6 weeks for R32-R36 data to accumulate.
      Run analysis: did the new strategies (tested in Phase 11) outperform old ones?
      Add any winner to the live screener.

- [ ] **Phase 14 — Subscription model**
      Stripe integration. Free tier = delayed signals (24h lag).
      Paid tier ($9/mo) = real-time signals + email alerts.
      Requires: ASIC disclaimer review + T&C page.

- [ ] **Phase 15 — JPX upgrade**
      Full Japanese stock universe expansion (currently ~80 JPX stocks → 300+).
      Japanese-language screener view.
      Partner or cross-link with Project 2.

---

## PROJECT 2 — International Student Finance Platform
**What it is:** Free bilingual tools for international students in Australia —
super calculator, tax estimator, money transfer guide, work rights.
Later: waitlist → premium tools → affiliate income.
**Repo:** GoofyisDAWG/intl-student-finance (create this)
**Status:** Building now 🔨

### The Problem (why this matters)
- 750,000+ international students in Australia
- Most leave without claiming $2k–$8k in superannuation
- Most overpay on money transfers (bank 3-5% vs Wise 0.5%)
- Most don't know their tax and work rights
- Zero good English+Japanese tools exist for this

### Stage 1 — Core Tools (NOW — weeks 1-4)
- [x] **Super Claim Calculator** — income → super owed → DASP after 35% tax → in JPY
      Steps to claim via ATO portal. DONE ✅
- [ ] **Tax Estimator** — income + residency status → estimated tax bill or refund
      Australian tax brackets, low income offset, Medicare levy exemption for students
      Link to ATO myTax. EN/JA bilingual.
- [ ] **Money Transfer Comparison** — AUD amount + destination country →
      side-by-side comparison: your bank vs Wise vs Revolut
      Show total received in JPY/CNY/KRW. Wise referral link = first income stream.
- [ ] **Work Rights Quick Check** — visa type selector → what you can/can't do
      Student visa 500: 48h/fortnight during study, unlimited in holidays
      Working Holiday 417/462: 6-month employer limit etc.
      Common underpayment traps. Link to Fair Work.

### Stage 2 — Content + Growth (weeks 5-8)
- [ ] **Bank Account Guide** — which account for new arrivals? (no overseas history)
      Compare: CommBank, NAB, ING, Wise (debit). Fees, setup requirements.
- [ ] **HECS/FEE-HELP explainer** — international students can't get HECS, but
      some confuse it. Clear EN/JA guide on how tuition works.
- [ ] **Email waitlist** — capture early users before paid features exist
- [ ] **SEO landing page** — "superannuation for international students Japan"
      Deploy as static page or add st.experimental_query_params routing
- [ ] **Reddit + Discord distribution** — r/australia, r/japanlife, r/ausjapan

### Stage 3 — Monetization (weeks 9-16)
- [ ] **Wise affiliate** — apply for Wise affiliate programme
      Referral link already in app. Add CTA card on Money Transfer page.
      Target: 10 signups/month = ~$500–750 AUD/month passive
- [ ] **Premium tools (Stripe)** — free = calculator basics, paid = personalised
      PDF summary, email reminder before visa expiry, direct ATO pre-fill guide
- [ ] **Japanese community partnerships** — reach out to Japanese student associations
      at UQ, UNSW, Melbourne. Offer free tool + ask for share.

### Stage 4 — Expansion (month 4+)
- [ ] **Multi-country** — add South Korea, China, India student workflows
      (same super/tax tools, different money transfer destinations)
- [ ] **Mobile app** — if web traction is strong, React Native wrapper

---

## PATHWAY 3 — JPX Gateway
**What it is:** Japanese stock market in full English. Uses Pathway 1's screener
engine + adds fundamentals (P/E, revenue, sector) for each JPX-listed company.
**Audience:** Expats in Japan, international investors, students returning to Japan
**Repo:** GoofyisDAWG/jpx-gateway (create when ready)
**Status:** Planned — start after Pathway 2 Stage 2 complete

### Why this is a real gap
- Tokyo Stock Exchange is the 3rd largest in the world (~3,900 companies)
- Almost all analysis tools are in Japanese only
- English-speaking investors who want Japan exposure have basically nothing
- Pathway 1 already covers ~80 JPX stocks — expand to full 3,900

### Build order
- [ ] **Phase A — English data layer**
      Map TSE ticker → English company name + sector + brief description
      (use Wikipedia API + manual curation for top 500 by market cap)
- [ ] **Phase B — Screener integration**
      Pull signals from Pathway 1's engine for JPX stocks
      Add P/E, P/B, dividend yield, market cap columns
      EN/JA toggle (same T() pattern)
- [ ] **Phase C — Fundamentals deep-dive**
      Individual stock page: revenue trend, margins, sector peers
      Cross-link to Pathway 2 ("This company is hiring in Australia →")
- [ ] **Phase D — Alert system**
      Email alert when a JPX stock you're watching gets a signal
      Stripe: $5/mo for alerts
- [ ] **Phase E — Community**
      Submit your JPX watchlist. See what others are watching.
      Reddit-style discussion (could use Giscus / GitHub Discussions)

---

## Architecture Decision
```
/quant-research/
├── goofy-screener-website/   ← Project 1 (live)
│   └── app.py (5000+ lines)
└── intl-student-finance/     ← Project 2 (building now)
    ├── app.py
    └── ROADMAP.md (this file)
```

**Why separate:**
- Different audiences (traders vs international students)
- Different branding
- Each can be deployed as its own Streamlit app
- When ready: link them via nav footer or share a landing page domain
- Combining now = messy; combining later = easy

**Cross-link plan:**
- Project 1 footer: "Also check out our International Student Finance tools →"
- Project 2 footer: "Interested in Japanese stocks? →"

---

## Income Streams (realistic timeline)
| Stream | Project | When | Est. Monthly |
|--------|---------|------|-------------|
| Wise affiliate | P2 | Month 2 | $200–500 AUD |
| Stripe sub (P1) | P1 | Month 4 | $100–300 AUD |
| Stripe premium (P2) | P2 | Month 5 | $100–400 AUD |
| JPX data API | P1+P2 | Month 6+ | unknown |

---

## Current Sprint (this week)
1. [x] Super Claim Calculator — DONE
2. [ ] Tax Estimator — next
3. [ ] Money Transfer Comparison — after that
4. [ ] Work Rights Quick Check — after that
5. [ ] Create GitHub repo for Project 2 + deploy to Streamlit Cloud
