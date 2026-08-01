# Data Directory

These JSON files are the current, human-readable materialized state of PAM Continuum.

- `state.json` — runtime, freshness, and top-level metrics.
- `missions.json` — objectives and verified next actions.
- `signals.json` — tracked claims, hypotheses, and system observations.
- `connections.json` — explicit entities and relationships for the visual graph.
- `sources.json` — safe source-health projection with no credentials.
- `activity.json` — append-only visible activity feed.
- `heartbeat.json` — scheduler result, including whether actual world data was collected.

Raw evidence should be added in dated, append-only paths as connectors come online. Derived views may be rebuilt; evidence should not be silently rewritten or deleted.

