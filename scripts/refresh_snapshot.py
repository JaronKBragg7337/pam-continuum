from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CONFIG = ROOT / "config"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def env_ready(source_id: str) -> bool:
    return os.getenv(f"PAM_SOURCE_{source_id.upper().replace('-', '_')}_READY", "false").lower() == "true"


def main() -> None:
    parser = argparse.ArgumentParser(description="Record a transparent PAM Continuum pulse.")
    parser.add_argument("--heartbeat-only", action="store_true", help="Do not claim live world data was collected.")
    args = parser.parse_args()

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    source_config = read_json(CONFIG / "sources.json")
    live_sources = [source for source in source_config if env_ready(source["id"])]
    heartbeat_only = args.heartbeat_only or not live_sources
    run_status = "heartbeat-only" if heartbeat_only else "connector-ready"
    world_data_updated = False if heartbeat_only else True

    source_snapshot = []
    for source in source_config:
        ready = source["id"] in {item["id"] for item in live_sources}
        session_state = source.get("session_state")
        availability = source.get("availability")
        if ready:
            status = "connected"
            freshness = "awaiting-capture"
            note = "Connector is marked ready; source-specific capture must be verified before synthesis."
        elif availability == "quota-exhausted-until-2026-08-02":
            status = "ui-limited"
            freshness = "quota-exhausted"
            note = "Signed-in session observed; source quota is exhausted until 2026-08-02."
        elif session_state == "computer-observed-signed-in":
            status = "ui-ready"
            freshness = "session-observed"
            note = "Signed-in browser or desktop session observed; no capture has run yet."
        elif session_state == "user-reported-signed-in":
            status = "session-reported"
            freshness = "session-reported"
            note = "User reports a signed-in browser session; verify at capture time."
        elif source["status"] == "ready":
            status = "available"
            freshness = "available"
            note = "Surface is available for a mission-scoped read."
        else:
            status = "not-connected"
            freshness = "unknown"
            note = "Awaiting account, credential, or connector setup."
        source_snapshot.append({
            "id": source["id"],
            "label": source["label"],
            "kind": source["kind"],
            "status": status,
            "freshness": freshness,
            "note": note,
            "checked_at": now,
        })

    heartbeat = {
        "schema_version": 1,
        "run_status": run_status,
        "last_run": now,
        "world_data_updated": world_data_updated,
        "live_sources_checked": len(live_sources),
        "message": (
            "Scheduler is healthy; no world data was collected."
            if heartbeat_only
            else "At least one connector is ready for a verified capture pass."
        ),
        "checks": [
            "source registry loaded",
            "credential values were not written to disk",
            "dashboard data contracts remain machine-readable",
        ],
    }

    state = read_json(DATA / "state.json")
    state["generated_at"] = now
    state["mode"] = "heartbeat-only" if heartbeat_only else "connector-ready"
    state["runtime"].update({
        "status": "healthy",
        "heartbeat_status": "healthy",
        "world_refresh_status": "not-collected" if heartbeat_only else "capture-pending",
        "last_heartbeat": now,
        "live_sources_connected": len(live_sources),
        "connector_health": "awaiting-capture" if live_sources else "not-configured",
    })
    state["metrics"]["heartbeat_runs"] = int(state["metrics"].get("heartbeat_runs", 0)) + 1

    activity = read_json(DATA / "activity.json")
    activity.insert(0, {
        "id": f"PULSE-{now.replace('-', '').replace(':', '').replace('T', '')}",
        "timestamp": now,
        "type": "pulse",
        "title": "Daily pulse recorded",
        "detail": heartbeat["message"],
        "status": "verified",
    })
    activity = activity[:200]

    write_json(DATA / "heartbeat.json", heartbeat)
    write_json(DATA / "state.json", state)
    write_json(DATA / "sources.json", source_snapshot)
    write_json(DATA / "activity.json", activity)
    print(json.dumps({"run_status": run_status, "live_sources_checked": len(live_sources), "timestamp": now}, indent=2))


if __name__ == "__main__":
    main()
