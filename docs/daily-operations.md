# Daily Operations

## Current behavior

The scheduled workflow runs once per day at 13:17 UTC and can be started manually. In bootstrap mode it records a heartbeat, checks the safe source registry, validates JSON, and commits only the generated snapshot changes. It does not claim that the world was refreshed.

## Live collection behavior

When a connector is implemented and marked ready, the daily pulse should:

1. Load the mission queue and identify the highest-value open questions.
2. Select sources based on coverage and independence, not just availability.
3. Open fresh sessions or use an authenticated API as appropriate.
4. Capture raw responses and mechanical metadata.
5. Classify completeness, refusal, unavailability, and truncation separately.
6. Validate evidence before synthesis.
7. Generate claims with basis, confidence, horizon, and falsifier.
8. Match claims to existing signals and append lifecycle events.
9. Generate a reading and update the dashboard.
10. Commit the complete cycle, including degraded results.

## What the dashboard must always show

- Last heartbeat time.
- Last actual world-data capture time, or an explicit absence marker.
- Connected and unavailable source counts.
- Active missions and blocked dependencies.
- New, resurfaced, unresolved, confirmed, and invalidated signals.
- Cross-domain connections with their confidence and evidence basis.
- Failed attempts and coverage gaps.

