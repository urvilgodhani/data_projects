# Live Data Deployment

## Goal

The public GitHub Pages dashboard should visibly change every minute while a Python service simulates a moving retail market.

## Architecture

```text
Hosted Python service
        |
        | updates about 10% of stores every minute
        v
MongoDB Atlas
        |
        | read-only dashboard API
        v
GitHub Pages dashboard
```

GitHub Pages remains the public frontend. It cannot run Python because it is a static hosting service.

## What Changes Every Minute

- Approximately 5 of 50 stores
- Active picker, stager, and dispenser counts
- Orders in progress
- Picking queue
- Staging capacity
- Curbside occupancy
- Average pick rate
- Staging time
- Customer wait
- SLA
- Ratings
- Alerts

The service stores a 72-hour snapshot trail in MongoDB Atlas. MongoDB TTL
indexes automatically expire live snapshots and events after the retention
window. The current store-status collection is replaced in place, so it stays
at approximately 50 documents instead of growing every minute.

This creates a rolling changelog: after 72 hours, the oldest minute expires as
the newest minute is added.

## Run Locally

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Set environment variables:

```bash
export MONGODB_URI="mongodb+srv://..."
export MONGODB_DATABASE="digital_fulfillment_ops"
```

Start the service:

```bash
uvicorn live_service.app:app --reload
```

Test:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/api/live
```

## Deploy on Railway

Railway supports persistent services for long-running applications and background processes.

1. Create a Railway project.
2. Connect the GitHub repo:

```text
urvilgodhani/data_projects
```

3. Add variables:

```text
MONGODB_URI=mongodb+srv://...
MONGODB_DATABASE=digital_fulfillment_ops
SIMULATION_INTERVAL_SECONDS=60
STORE_UPDATE_PERCENT=0.10
LIVE_RETENTION_HOURS=72
```

4. Deploy the repo. Railway reads `railway.toml`.
5. Generate a public domain for the service.
6. Confirm:

```text
https://YOUR-RAILWAY-DOMAIN/health
```

7. Update `live-config.js`:

```js
window.LIVE_API_URL = "https://YOUR-RAILWAY-DOMAIN";
```

8. Push the change through GitHub Desktop.

## Demo Fallback

Before the hosted API URL is configured, the GitHub Pages dashboard runs a clearly labeled browser simulation. This makes the live behavior visible immediately without exposing database credentials.
