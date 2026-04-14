---
name: get-landing-page-data
description: Pull the latest ad-impact analysis and recommend the top landing page opportunity to test next.
---

# /get-landing-page-data

Fetch landing page opportunities from the ad-impact pipeline and recommend what to test next.

## Steps

### 1. Fetch opportunities

Call `mcp__cluster-experiment__get_landing_page_data`.

This returns all ad-impact opportunities ranked by ad spend, with cross-references to any existing experiments.

### 2. Find the top recommendation

From the returned opportunities, find the one with the **highest `spend`** that does **not** have `has_active_experiment: true`.

If every opportunity already has an active experiment, tell the user: "All top opportunities already have experiments running or in preview. Here's the full list:" and show a summary table.

### 3. Present the recommendation

Present the top opportunity clearly:

**Top Recommendation: {display_name}**
- **Landing Page:** {landing_page_url}
- **Ad Spend:** ${spend} (across {ad_count} ads)
- **Issue:** {reasoning}
- **Recommendation ID:** {id}

If `changes_markdown` is available, show it under a "Suggested Changes" heading.

If `rationale_markdown` is available, show it under a "Rationale" heading.

### 4. Offer next steps

Ask the user if they'd like to create an experiment for this opportunity. If yes, hand off to `/create-experiment` by telling the user to paste the recommendation or by directly proceeding with `create_experiment` using:
- The opportunity's `landing_page_url` as the `surface_path`
- Test surface = 5 (Landing Page)
- The opportunity's `id` as `ad_targeting_recommendation_id` (if the user wants ad audience targeting)
- The `changes_markdown` as the basis for variant content

### 5. Show remaining opportunities

After presenting the top pick, show a brief summary of the other opportunities:

| # | Landing Page | Issue | Spend | Already Testing? |
|---|-------------|-------|-------|-----------------|
| 1 | ... | ... | $... | Yes/No |

This gives the user the full picture so they can override your recommendation if needed.
