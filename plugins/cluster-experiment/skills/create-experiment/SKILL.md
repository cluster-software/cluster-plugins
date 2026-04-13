---
name: create-experiment
description: Create an A/B test experiment from a recommendation. Paste a test recommendation and this skill will create the experiment, write variant content, and open the preview.
---

# /create-experiment

Create an A/B test from a pasted recommendation. This skill guides you through creating an experiment, writing variant content incrementally, and verifying the result visually.

## Steps

### 1. Parse the recommendation

Extract from the pasted recommendation:
- **Page surface**: Homepage (1), PDP (2), Collection (3), Cart (4), or Landing Page (5)
- **Test name**: A concise name for the A/B test
- **Changes to make**: List of DOM changes (copy updates, new sections, layout changes, image swaps, etc.)
- **Recommendation ID** (if present): Look for a `**Recommendation ID:**` line — this is the unique ID of the ad-impact recommendation. Save it for step 1b.

### 1b. Ask about targeting (ad-impact recommendations only)

If the pasted recommendation includes a **Recommendation ID** (parsed in step 1), it comes from the ad-impact pipeline.

Use the `AskUserQuestion` tool to ask about targeting. Present two options:

- **All landing page visitors** — "Run for everyone who visits this page (more traffic, faster results)"
- **Ad audience only** — "Only target visitors arriving from the relevant Meta ads (precise, but slower to reach significance)"

If the user chooses **Ad audience only**, pass the **Recommendation ID** from step 1 as `ad_targeting_recommendation_id` when creating the experiment in step 3. The tool automatically fetches the relevant ads, creates a targeting segment (using fbadid), and attaches it to the test.

If no Recommendation ID is present (e.g., LP analysis, roadmap recommendations), skip this step entirely.

### 2. Check for existing experiments

Call `mcp__cluster-experiment__get_experiment_info`.

The store is resolved automatically from the API key.

Review the returned tests. If a test with the same name or very similar purpose exists, tell the user and ask whether to reuse it or create a new one.

### 3. Create the experiment

Call `mcp__cluster-experiment__create_experiment` with:
- `name` from step 1
- `description` summarizing what the test changes
- `test_surface_id` from step 1
- `ad_targeting_recommendation_id` — the recommendation's `id`, if the user chose "ad audience only" in step 1b

Save the returned `treatment_variant_id`  - this is what you'll write content to.

**Immediately** share the canvas URL with the user: "Open this URL now: {canvas_url}  - changes will appear in the canvas as I add them." Don't wait until content is written  - the user should have the canvas open before you start writing.

The `canvas_url` returned by the tool is a full URL (e.g. `https://dashboard.hello-cluster.com/variant/.../canvas`) — share it directly.

### 4. Write variant content incrementally

Break the changes into logical groups. For each group, call `mcp__cluster-experiment__write_variant_content` with:
- `variant_id`: the treatment_variant_id
- `patches`: array of DOM patches for this group
- `mode`: "append" (default) for new patches, "replace_by_selector" if correcting a previous patch

**Write one group at a time.** Examples of groups:
- Hero section headline + subheadline
- CTA button text + styling
- Social proof / trust badges
- Product description changes
- Image replacements

**Selector quality matters.** Always use selectors that target **visible** elements. Many themes have hidden accessibility duplicates (e.g., a bare `h1` that's `visually-hidden`). Prefer specific class-based selectors over generic tag selectors. Before writing patches, call `get_page_structure` to see which elements are visible and what selectors to use.

**JS selectors must be scoped — never broad.** When using the `js` parameter to manipulate links or elements, avoid page-wide attribute selectors like `a[href*="/products/foo"]`. These will match every link to that URL across the entire page — product cards, footer links, related products — not just your intended targets. Instead:
- **Scope to a container**: `document.querySelectorAll('.image-with-text a[href*="..."]')` limits changes to that section only
- **Match by button text**: filter results with `a.textContent.trim() === 'Shop Now'` to target only specific CTAs
- **Use both together** if needed for maximum precision: scope + text match

**JS is one block — keep it consolidated.** The `js` field in `write_variant_content` is a single accumulated script. If you call `replace_by_selector` mode with new JS, it **replaces the entire JS block**, silently wiping any previous JS operations (link swaps, text changes, etc.). Always consolidate all JS operations into a single block when updating. Never assume a previous JS snippet is still active after a `replace_by_selector` call.

**Mark all patched elements.** Always add `data-cluster-variant-patch="true"` to the root element of any HTML you write in patches. This allows the preview to highlight modified content with a blue bounding box.

Common patch patterns:
```json
// Replace text content  - note the data-cluster-variant-patch attribute
{ "action": "replaceContent", "selector": ".banner__heading span", "html": "<span data-cluster-variant-patch='true'>New Headline</span>" }

// Insert a new section after an element
{ "action": "insertAfter", "selector": ".hero-section", "html": "<div data-cluster-variant-patch='true' class='trust-bar'>...</div>" }

// Hide an element
{ "action": "hide", "selector": ".old-banner" }

// Replace an image
{ "action": "replaceUrl", "oldUrl": "https://cdn.shopify.com/old-image.jpg", "newUrl": "https://cdn.shopify.com/new-image.jpg" }
```

### 5. Verify with screenshot (Desktop AND Mobile)

After every 2-3 `write_variant_content` calls, call `mcp__cluster-experiment__get_screenshot` to visually verify:
- Are the patches applied correctly?
- Does the layout look right?
- Is text readable and properly styled?

The tool returns screenshots for both desktop and mobile.

If something looks off, use `write_variant_content` with `mode: "replace_by_selector"` to fix the specific patch.

### 6. Present result

Once all changes are written and verified:
1. Share the `canvas_url` with the user
2. Summarize what was changed (list of patches by section)
3. Ask if they want to make any adjustments before deploying

## Error Handling

- If `create_experiment` returns `reused: true`, a test with that name already exists. Ask the user if they want to write new content to the existing treatment variant.
- If `write_variant_content` fails, check the error message. Common issues: invalid CSS selector, variant_id is a control variant (write to treatment only).
- If `get_screenshot` fails (Playwright error), the preview URL is still returned in the error. Suggest the user open it manually.

## Guidelines

- Ensure designs look good on mobile and desktop.
