# Connector Expansion

PAM Continuum is intentionally source-agnostic. A new connector should make one surface more legible without turning the repository into a credential store. For AI systems, the connector is a browser or desktop-app procedure, not an API client.

## Connector contract

Each adapter should define:

1. `source_id` matching `config/sources.json`.
2. Surface and session method, documented without passwords, tokens, or account identity.
3. A mission-scoped capture method.
4. A completeness check and a content classification.
5. Stable evidence IDs and raw capture paths.
6. Rate limits, retry behavior, and failure categories.
7. A freshness guarantee that the dashboard can explain.

## AI session rules

- Open the signed-in website or desktop app through computer control.
- Use a fresh conversation for each mission-scoped capture.
- Never automate password or OTP entry.
- Never silently fall back to an AI API.
- Do not send private workspace material unless the mission explicitly identifies the exact data and destination.
- Preserve refusals, unavailable sessions, truncation, and model/surface changes.

## Planned expansion order

1. GitHub and local workspace inventory, because they are already available and directly actionable.
2. Public web and official-source research, scoped by active mission.
3. The additional AI accounts the user makes available.
4. Operations sources such as calendar and email, with explicit privacy boundaries.
5. Specialist sources selected by domain gaps rather than by novelty.

The system should not connect a source merely to increase the count. A source earns a place when it adds coverage, perspective, primary evidence, or a useful failure signal.
