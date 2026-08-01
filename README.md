# PAM Continuum

**An evergreen intelligence workspace for one persistent P.A.M.-style assistant.**

PAM Continuum is the new system being built for Codex: a living workspace that gathers evidence through browser and desktop-app sessions, preserves uncertainty, connects related signals, turns observations into missions, and presents the whole system through a visual command center.

The name is deliberately new. `pam-continuum` is not a replacement for the existing Orchestra repository and does not modify it. Orchestra contributes durable principles—provenance, preserved disagreement, falsifiers, append-only history, and explicit context—while PAM Continuum adds a broader personal operating layer: missions, workspace awareness, build queues, source health, relation mapping, and a daily visual pulse.

## Current state

This repository starts in **bootstrap mode**. The structure, contracts, dashboard, and GitHub Pages workflows are ready. Until source accounts and connectors are added, the daily workflow records a heartbeat and clearly reports that no world data was collected. A heartbeat is not disguised as fresh intelligence.

## Live command center

Open the [PAM Continuum dashboard](https://jaronkbragg7337.github.io/pam-continuum/) to view the current system map, mission queue, signal watch, activity stream, and source-health state.

## What it is designed to become

- A growing source network: AI systems, public web research, code repositories, local projects, connected accounts, and future adapters.
- Browser-first AI collection through existing signed-in sessions; AI API collection is intentionally disabled.
- An append-only evidence archive with prompts, captures, timestamps, source identity, model/version metadata, and failure states.
- A relation graph that makes cross-domain connections visible instead of leaving them buried in separate notes.
- A mission engine that turns findings into buildable or solvable next actions.
- A visual command center showing freshness, source health, active missions, signals, connections, and recent activity.
- A daily GitHub Pages site generated from the repository's versioned data.

## Quick start

```powershell
python scripts/validate_data.py
python scripts/refresh_snapshot.py --heartbeat-only
python scripts/validate_data.py
python scripts/build_site.py
python -m http.server 8000 --directory site
```

Open `http://localhost:8000` to view the command center.

## Design rules

1. **Evidence before narrative.** Every important claim points back to an attributable artifact.
2. **Uncertainty stays visible.** Confidence, freshness, disagreement, refusal, and missing coverage are data.
3. **Connections are explicit.** A relationship is recorded as a relationship, not implied by prose alone.
4. **Nothing important disappears.** Raw captures and lifecycle events are append-only; corrections are additive.
5. **The system distinguishes activity from progress.** A successful heartbeat does not equal a successful world refresh.
6. **Actions are verified.** A build, fix, or external operation is not marked complete until its result is checked.
7. **Credentials never enter Git.** Secrets belong in local environment variables or GitHub Actions secrets.

## Repository map

```text
pam-continuum/
├── .github/workflows/       daily pulse and GitHub Pages deployment
├── config/                  source and domain registries
├── data/                    versioned state, missions, signals, and relationships
├── dashboard/               source files for the visual command center
├── docs/                    operating procedures and roadmap
├── schemas/                 machine-readable data contracts
└── scripts/                 validation, snapshot, and static-site build tools
```

## Daily page

The GitHub Pages workflow publishes the `dashboard/` view from the latest committed data. The scheduled pulse runs once per day and can also be started manually. When live connectors are configured, the same pipeline can be extended to collect and classify fresh evidence before the page is published.

## License

MIT. See [LICENSE](LICENSE).
