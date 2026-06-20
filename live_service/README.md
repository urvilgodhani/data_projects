# Live Data Service

This Python service simulates a moving digital fulfillment market.

Every minute it:

- Updates approximately 10% of stores
- Rotates active picker, stager, and dispenser counts
- Changes in-progress orders and queue pressure
- Recalculates SLA, ratings, wait time, and efficiency
- Writes store status, snapshots, and events to MongoDB Atlas
- Exposes a read-only API for the GitHub Pages dashboard

Run locally:

```bash
uvicorn live_service.app:app --reload
```

Required environment variables:

```text
MONGODB_URI
MONGODB_DATABASE=digital_fulfillment_ops
```

Optional environment variables:

```text
SIMULATION_INTERVAL_SECONDS=60
STORE_UPDATE_PERCENT=0.10
HISTORY_LIMIT=180
LIVE_RETENTION_HOURS=72
```

`live_store_status` is updated in place. Snapshot and event documents expire
automatically after the retention window, keeping the database footprint
bounded while preserving a rolling operational history.
