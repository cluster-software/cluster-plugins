# Workflow action configs

Use the config that matches the step's `action_type`. Resolve every referenced
campaign, table, column, and channel before creating the workflow.

## `add_to_campaign`

Required: `campaign_id`. Optional: `table_id`, `dedupe_campaigns`,
`linkedin_column`, `custom_variable_columns`, `standard_field_columns`, and
`row_selector`. Table mappings and row selection require `table_id`. A
custom-variable mapping has `source_column`, `variable_key`, and `label`;
standard mappings map a contact field to a source column. `row_selector` may
specify `workflow_run_column` and a table `condition` using the structure below.
A company-scope workflow must source campaign leads from a people table.

## `add_to_table`

Provide either `table_id` for an existing table or `new_table_name` plus
`columns`, where each column has signal-payload `field` and destination `name`.
Optional: `run_column_ids` and `dedupe_column`.

## `send_to_slack`

Required: `channel_id`. Optional: `channel_name` and `message_template`. The
template may use `workflow.id`, `workflow.name`, `workflow.match_count`,
`workflow.run_id`, and `workflow.run_url` in double braces.

## `agent`

Required: `prompt`. Optional: `model`, `max_turns`, and up to ten `variables`.
Each variable has a lowercase underscore `name`, type `string`, `number`, or
`boolean`, and a `description`. The agent runs unattended and cannot launch
campaigns or send prospect messages.

## `run_table_columns`

Required: `table_id` and non-empty `column_ids`. Optional `row_selector` accepts
`workflow_run_column` and a table `condition`. Every selected column must be a
runnable computed column.

### Row-selector conditions

`condition` is an object with `version: 1`, `enabled: true`, optional
`display_formula`, and `root`. A single root predicate is:

```json
{
  "type": "predicate",
  "column_id": "qualified-column-id",
  "operator": "equals",
  "value": true
}
```

To combine predicates, use a root group with `type: "group"`, `operator: "and"`
or `"or"`, and a non-empty `children` array of predicates. Predicate operators
are `is_empty`, `is_not_empty`, `equals`, `not_equals`, `contains`,
`not_contains`, `greater_than`, `greater_than_or_equal`, `less_than`, and
`less_than_or_equal`. Omit `value` for the two empty operators; otherwise it may
be text, number, boolean, or null.

## `aggregate_to_table`

Required: `source_table_id`, `destination_table_id`, non-empty `group_by`, and
non-empty `metrics`. A group mapping has `source_column` and
`destination_column`. A metric has `operation` (`count`, `count_distinct`,
`sum`, `average`, `min`, or `max`), `destination_column`, and `source_column`
except for `count`. Optional fields control uniqueness, ordering, limits, and
membership/run tracking: `unique_by_column`, `order_by_column`,
`order_direction`, `limit`, `destination_current_membership_column`,
`destination_run_id_column`, and `destination_first_seen_run_column`.

## `flatten_table_column`

Required: `source_table_id`, `destination_table_id`, `source_list_column`,
non-empty `field_mappings`, `dedupe_source_field`, and
`destination_dedupe_column`. A field mapping has `source_field` and
`destination_column`. Optional `source_column_mappings`, `row_selector`,
`dedupe_normalization`, `destination_source_row_column`,
`destination_current_membership_column`, `destination_run_id_column`, and
`destination_first_seen_run_column`. Each source-column mapping has
`source_column` and `destination_column`.
