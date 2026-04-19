## Cluster Experiment Plugin

MCP server for analyzing landing pages and creating A/B test experiments on Shopify stores via the Cluster platform.

### Available Skills

- `/create-experiment`  - Create an A/B test from a pasted recommendation
- `/get-landing-page-data` - Pull ad-impact opportunities and recommend the top one to test
- `/analyse-landing-page-url` - Reuse or run a landing page analysis for a specific URL and return the dashboard link

### Tools (8)

| Tool | Purpose | ReadOnly |
|------|---------|----------|
| `list_connected_stores` | List all Shopify stores connected to this API key across orgs | Yes |
| `get_experiment_info` | List existing tests for a store (curated, no variant content) | Yes |
| `get_landing_page_data` | Fetch ad-impact opportunities ranked by spend, cross-referenced with existing experiments | Yes |
| `getLandingPageAnalysis` | Create or reuse a 24h-cached LP analysis for a URL and return the finished analysis, recommendations, and dashboard link | No |
| `get_page_structure` | Get visible elements on a page with CSS selectors | Yes |
| `create_experiment` | Create test + control/treatment variants, with dedup check | No |
| `write_variant_content` | Add DOM patches to a variant incrementally | No |
| `get_screenshot` | Screenshot the variant preview via Playwright | Yes |

### Workflow

For ad-impact-driven testing:

1. `get_landing_page_data` -> find highest-spend opportunity without an active experiment
2. `get_experiment_info` -> check what exists
3. `get_page_structure` -> discover visible elements and their selectors
4. `create_experiment` -> set up test + variants
5. `write_variant_content` (call multiple times) -> build up changes using selectors from step 3
6. `get_screenshot` (after every 2-3 writes) -> verify visually

For direct landing page analysis:

1. `getLandingPageAnalysis` -> create or reuse a recent LP analysis for a specific URL
2. Review the returned recommendations and choose what to test
3. Open the returned dashboard link if deeper inspection is helpful
4. `create_experiment` -> create the A/B test for the chosen idea
5. `write_variant_content` + `get_screenshot` -> implement and verify the treatment

### Content Model

Variants contain DOM patches applied client-side to a Shopify storefront. Each patch has:
- `action`: replaceContent, replaceElement, insertBefore, insertAfter, hide, addClass, removeClass, setAttribute, replaceUrl
- `selector`: CSS selector targeting the element
- Action-specific fields: `html`, `className`, `attribute`/`value`, `oldUrl`/`newUrl`

### Test Surfaces

1 = Homepage, 2 = PDP, 3 = Collection, 4 = Cart, 5 = Landing Page

### Setup

Install the plugin from the marketplace, or for local development:

```bash
cd apps/experiment-plugin
npm install
```

Set `CLUSTER_API_KEY` and `CLUSTER_API_URL` in `.claude/settings.local.json`, then:
```bash
claude --plugin-dir .
```
