# PAM Continuum Architecture

## System shape

```text
sources → capture → evidence ledger → relation graph → synthesis
                                      ↓              ↓
                                mission queue ← decision state
                                      ↓
                              verified computer action
                                      ↓
                             daily pulse + Git history
```

## Layers

### 1. Source layer

`config/sources.json` is the registry of possible inputs. A source can be an AI account, web surface, repository, local directory, connected application, or future adapter. Source configuration describes capability and connection state, never secrets.

### 2. Capture layer

Every collected artifact should carry source identity, timestamp, prompt or request version, model or surface version when available, completeness, content classification, and attempt history. Refusals, unavailable attempts, truncation, and empty responses are preserved as operating data.

### 3. Evidence layer

The `data/` directory is the current materialized view. Future raw captures will live in dated append-only paths. Every derived item must point back to one or more evidence IDs.

### 4. Relation layer

`data/connections.json` represents entities and edges explicitly. Edges include relationship type, mechanism, confidence, evidence IDs, and lifecycle state. The dashboard renders this graph; it does not invent relationships during rendering.

### 5. Mission layer

`data/missions.json` holds objectives, dependencies, expected value, status, next action, and verification criteria. A signal becomes a mission only when there is an actionable path or an explicit research question.

### 6. Action layer

Scripts, local tools, browser control, and connected applications are execution surfaces. Actions produce artifacts and verification notes. The action layer is not allowed to silently rewrite evidence.

### 7. Experience layer

`dashboard/` is a dependency-light static command center. It reads versioned JSON and displays freshness, source health, missions, signals, activity, and the relation graph. GitHub Pages publishes it from the current commit.

### 8. Scheduler layer

GitHub Actions runs the daily pulse. Initially it records a transparent heartbeat. As connectors are added, source-specific collection steps can be inserted before validation and deployment.

## State model

```text
planned → collecting → captured → synthesized → connected → missioned
                                               ↘ unresolved
```

Any state may also become `stale`, `invalidated`, `blocked`, or `archived`. State transitions are recorded as events rather than silently replacing history.

## Independence boundary

Collection should remain separate from synthesis. A synthesizer may read prior artifacts, but its context declaration is recorded. The comparison layer labels independent and informed agreement separately. The system never asks a model to decide that it agrees with itself.

