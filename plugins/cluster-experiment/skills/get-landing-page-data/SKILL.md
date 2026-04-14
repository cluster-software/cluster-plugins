---
name: get-landing-page-data
description: Pull the latest ad-impact analysis and recommend the top landing page opportunity to test next.
---

# /get-landing-page-data

Fetch landing page opportunities from the ad-impact pipeline and recommend what to test next.

## Steps

### 1. Fetch opportunities

Call `mcp__cluster-experiment__get_landing_page_data`.

This returns all ad-impact opportunities ranked by ad spend, plus a list of existing experiments.

### 2. Find the top recommendation

Recommend the opportunity with the **highest `spend`** — this is always the top pick.

Only skip an opportunity if there is a **running** experiment (status = `"running"`) targeting the same landing page. Draft/preview experiments do NOT count as coverage — those haven't launched yet.

### 3. Present the recommendation

Present the top opportunity clearly:

**Top Recommendation: {display_name}**
- **Landing Page:** {landing_page_url}
- **Ad Spend:** ${spend} (across {ad_count} ads)
- **Issue:** {reasoning}
- **Recommendation ID:** {id}

If `changes_markdown` is available, show it under a "Suggested Changes" heading.

If `rationale_markdown` is available, show it under a "Rationale" heading.

### 3b. Mention draft experiments as an aside

If there are draft/preview experiments that target the same landing page as the top recommendation, mention them briefly as a note — e.g.:

> Note: I see you already have draft experiments for this page ({experiment names}). If those are ready to go, here are the next best opportunities: ...

Then briefly list the next 1-2 opportunities by spend as alternatives the user could pursue instead.

### 4. Offer next steps

Ask the user if they'd like to create an experiment for this opportunity. If yes, proceed with `create_experiment` using:
- The opportunity's `landing_page_url` as the `surface_path`
- Test surface = 5 (Landing Page)
- The opportunity's `id` as `ad_targeting_recommendation_id` (if the user wants ad audience targeting)
- The `changes_markdown` as the basis for variant content

### 5. Show remaining opportunities

After presenting the top pick, show a brief summary of the other opportunities:

| # | Landing Page | Issue | Spend | Running Experiment? |
|---|-------------|-------|-------|---------------------|
| 1 | ... | ... | $... | Yes/No |

This gives the user the full picture so they can override your recommendation if needed.
