# Data Contracts

The dashboard consumes JSON, but the files are treated as contracts rather than casual notes.

Required invariants:

- Every signal has an ID, claim, confidence, basis, falsifier, horizon, and status.
- Every connection names both endpoints, a relationship label, a confidence, and a mechanism or description in the node records.
- Every mission has a next action and a verification method.
- Runtime freshness distinguishes `heartbeat_status` from `world_refresh_status`.
- Source snapshots expose status and notes only; credentials and tokens are never serialized.
- Activity entries are append-only and carry a timestamp.

The first schemas are intentionally small. They will become stricter as live adapters are added, without invalidating historical records.

