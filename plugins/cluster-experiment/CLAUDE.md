## Cluster Experiment Plugin

MCP server for creating A/B test experiments on Shopify stores via the Cluster platform.

### Available Skills

- `/create-experiment`  - Create an A/B test from a pasted recommendation
- `/get-landing-page-data` - Pull ad-impact opportunities and recommend the top one to test

### Tools (7)

| Tool | Purpose | ReadOnly |
|------|---------|----------|
| `list_connected_stores` | List all Shopify stores connected to this API key across orgs | Yes |
| `get_experiment_info` | List existing tests for a store (curated, no variant content) | Yes |
| `get_landing_page_data` | Fetch ad-impact opportunities ranked by spend, cross-referenced with existing experiments | Yes |
| `get_page_structure` | Get visible elements on a page with CSS selectors | Yes |
| `create_experiment` | Create test + control/treatment variants, with dedup check | No |
| `write_variant_content` | Add DOM patches to a variant incrementally | No |
| `get_screenshot` | Screenshot the variant preview via Playwright | Yes |

### Workflow

1. `get_landing_page_data` -> find highest-spend opportunity without an active experiment
2. `get_experiment_info` -> check what exists
3. `get_page_structure` -> discover visible elements and their selectors
4. `create_experiment` -> set up test + variants
5. `write_variant_content` (call multiple times) -> build up changes using selectors from step 3
6. `get_screenshot` (after every 2-3 writes) -> verify visually

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
