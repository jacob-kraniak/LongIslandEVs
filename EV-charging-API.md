# Project: Long Island EV Charging Station Update Feed

## Origin
- Grok conversation: [https://grok.com/c/77ece682-e8d6-44a2-befb-737abacab7ef?rid=121dc902-aebf-4813-a749-de47524fc6c8]
- Date conversation created: approx. 2025-12-15
- Date this summary generated: 2026-02-05
- Tags: #python #automation #ev-charging #discord #api-integration #rss-feed #nrel-afdc

## Problem / Goal
Keep the Long Island EV Community Discord server (independent, volunteer-run, supported by Drive Electric Long Island volunteers) informed about newly added or updated EV charging stations in Nassau and Suffolk counties. Manual monitoring of the Alternative Fuels Data Center (AFDC) is inefficient; automate detection and distribution to engage the community with timely, local infrastructure updates.

## Proposed Solution
Python script that:
1. Pulls full NY EV station dataset from NREL AFDC API daily/periodically.
2. Filters for stations in Long Island ZIP prefixes (110xx–119xx) with recent activity (open_date, date_last_confirmed, or updated_at within last 30 days).
3. Generates RSS feed for subscription in apps like Feeder.co.
4. Posts formatted updates via Discord webhook to a dedicated channel.
5. Saves filtered JSON as backup.

## Tech Stack (planned)
- Language(s): Python 3
- Core libraries / frameworks: requests, feedgen (RSS), datetime/timezone
- Deployment target / environment: Local machine initially; later cron/scheduled task, AWS Lambda, Replit, or small VPS
- Data sources / integrations (if any): NREL AFDC API (https://developer.nrel.gov/docs/transportation-infrastructure/alt-fuel-stations-v1/all/), Discord Webhooks

## Key Features / Scope
**Must-have:**
- Fetch and parse AFDC data with API key
- Robust date parsing and timezone-aware recency filter
- Long Island ZIP-based geographic filter
- RSS generation for Feeder.co
- Discord webhook notifications with formatted embeds

**Nice-to-have / future:**
- Configurable time window and ZIP list
- Email/SMS alerts fallback
- Station status change detection (not just new)
- Map link integration (Google Maps or AFDC)
- Hosted RSS with auto-update (GitHub Actions + Pages)

## Challenges & Open Questions
- AFDC lacks direct "updated_since" filter → full dataset pull + local diff required
- Rate limits (1k calls/day free tier) – mitigated by daily runs
- Public RSS hosting solution (GitHub Pages static? Dynamic endpoint needed?)
- Handling stations with missing/incomplete date fields
- Discord rate limits on bulk posts

## Next Steps
- [ ] Replace placeholder API key and Discord webhook URL in script
- [ ] Test full run: fetch → filter → RSS gen → Discord post
- [ ] Host RSS file publicly (GitHub Pages repo or static host)
- [ ] Add RSS URL to Feeder.co and verify feed updates
- [ ] Schedule script (cron, Task Scheduler, or cloud)
- [ ] Create dedicated repo (when POC is validated)

## Priority / Effort
- Priority: High (directly supports active community building for Long Island EV enthusiasts)
- Estimated effort to minimal POC: 5–10 hours (script already functional and tested locally)

## Updates / Log
- 2026-02-05: Initial brainstorm with Grok – core concept defined
- 2026-02-05: Working local script developed: API fetch, filtering, JSON output, progress logging
- 2026-02-05: Date parsing fixed (timezone issues resolved)
- 2026-02-05: Added RSS generation with feedgen + Discord webhook posting
- 2026-02-05: POC tested – successfully detects recent Long Island stations (e.g., Port Washington school locations) and formats output

## GitHub Tracking
- Issue: (create in repo and link here after commit, e.g. [#1](https://github.com/jacob-kraniak/Project-ideas/issues/1))
- Project board card: (add to Grok Ideas Pipeline board and link here)

## Current Status
POC script fully functional locally: pulls AFDC data, filters recent Long Island stations, saves JSON, generates RSS, and can post to Discord. Tested with real data showing new chargers (e.g., school locations in Port Washington area added/updated Nov–Dec 2025).

## Past Milestones
- 2026-02-05: Basic API fetch and print working
- 2026-02-05: Recency + ZIP filtering implemented
- 2026-02-05: Timezone-aware date parsing fixed
- 2026-02-05: RSS feed generation and Discord integration added

## Supplementary Code / Text
# Main Script: https://github.com/jacob-kraniak/LongIslandEVs/blob/main/AFDC_to_RSS_Discord.py
