# Connector Expansion

PAM Continuum is intentionally source-agnostic. A new connector should make one surface more legible without turning the repository into a credential store.

## Connector contract

Each adapter should define:

1. `source_id` matching `config/sources.json`.
2. Authentication method and required secret names, documented without secret values.
3. A mission-scoped capture method.
4. A completeness check and a content classification.
5. Stable evidence IDs and raw capture paths.
6. Rate limits, retry behavior, and failure categories.
7. A freshness guarantee that the dashboard can explain.

## Planned expansion order

1. GitHub and local workspace inventory, because they are already available and directly actionable.
2. Public web and official-source research, scoped by active mission.
3. The additional AI accounts the user makes available.
4. Operations sources such as calendar and email, with explicit privacy boundaries.
5. Specialist sources selected by domain gaps rather than by novelty.

The system should not connect a source merely to increase the count. A source earns a place when it adds coverage, perspective, primary evidence, or a useful failure signal.

