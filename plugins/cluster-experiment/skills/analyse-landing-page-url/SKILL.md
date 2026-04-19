---
name: analyse-landing-page-url
description: Analyze a landing page URL, reuse a recent cached result when available, and return the dashboard link for deeper inspection.
---

# /analyse-landing-page-url

Analyze a landing page URL using the Cluster LP analysis pipeline. This skill automatically reuses a completed analysis from the last 24 hours when one already exists for the same normalized URL.

## Input

The user provides:
- A landing page URL

Optionally they can provide:
- Competitor URLs
- Extra context about brand voice, goals, or traffic

If the user does not provide a URL, ask for it.

## Steps

### 1. Call the LP analysis tool

Call `mcp__cluster-experiment__get_landing_page_analysis` with:
- `lp_url` - the landing page URL
- `competitor_urls` - if the user provided any
- `extra_context` - if the user provided any
- `include_meta_context` - `true`
- `include_google_context` - `true`

The tool returns:
- `analysis`
- `recommendations`
- `frontend_url`
- `cached`

### 2. Tell the user whether results were reused

If `cached` is `true`, say the analysis was reused from the last 24 hours.

If `cached` is `false`, say a fresh analysis was run.

### 3. Present the analysis

Summarize the result clearly:

- **Landing Page:** `{analysis.lp_url}`
- **Dashboard Link:** `{frontend_url}`

If `recommendations.themes` has items:
- summarize the top 2-3 highest-priority themes
- mention the strongest actions under each theme

If only `recommendations.ungrouped` has items:
- summarize the top recommendations by impact

If no recommendations are present:
- say the analysis completed but no recommendations were returned

## Output Style

Keep the response concise and action-oriented:
- mention whether the result was cached
- surface the most important findings
- include the dashboard link near the top
