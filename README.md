# Digital Fulfillment Command Center

[![Live Dashboard](https://img.shields.io/badge/Live_Dashboard-Open-2dd4bf?style=for-the-badge)](https://urvilgodhani.github.io/data_projects/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Live_API-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=flat-square&logo=mongodb&logoColor=white)](https://www.mongodb.com/atlas)
[![Power BI Ready](https://img.shields.io/badge/Power_BI-Ready-F2C811?style=flat-square&logo=powerbi&logoColor=111)](docs/power_bi_guide.md)

A portfolio case study in retail operations analytics: synthetic order-lifecycle data, KPI engineering, a live simulation API, bounded MongoDB history, and an interactive command center for a 50-store market.

> All stores, employees, orders, and performance values are synthetic. This independent educational project is not affiliated with or endorsed by Walmart or any other retailer.

![Digital Fulfillment Command Center overview](assets/home-screen.png)

## Explore the Project

- [Open the live dashboard](https://urvilgodhani.github.io/data_projects/)
- [Read the data model](docs/data_model.md)
- [Review the live architecture](docs/live_data_deployment.md)
- [Build the Power BI version](docs/power_bi_guide.md)
- [See the portfolio case-study copy](docs/beacons_showcase.md)

## Executive Summary

Market Managers need to monitor fulfillment performance across many stores without digging through separate operational systems. This project turns the order lifecycle into one decision surface: it identifies struggling stores, stage bottlenecks, customer wait risks, employee performance patterns, and exceptions that need action.

The system models:

- **50 stores** across one synthetic market
- **5,000 employees** in picking, staging, and dispensing roles
- **12,000 orders** with complete lifecycle timestamps
- **10 analytics datasets** prepared for Power BI and MongoDB
- **6 interactive dashboard views** with drill-through navigation
- **Minute-level live simulation** that updates about 10% of stores per tick
- **72-hour rolling history** enforced with MongoDB TTL indexes

## Business Questions

The command center is designed to answer:

- Which stores are missing SLA right now?
- Is the constraint in picking, staging, or dispensing?
- Where are customer waits and curbside queues increasing?
- Which associates are leading, improving, or need coaching?
- Are returns, refunds, and complaints creating unusual risk?
- What action can a Market Manager take without changing the source metrics?

## Product Tour

### 1. Market Cockpit

The home screen summarizes market health, live connection status, the current bottleneck, the priority queue, stage-level operational pods, and leadership actions.

![Market Cockpit](assets/home-screen.png)

### 2. Picking Operations

Tracks active pickers, queue depth, item-found rate, pick speed, leaderboards, missed-item pressure, fatigue signals, order-size impact, and shift comparisons.

![Picking operations](assets/picking-page.png)

### 3. Staging Operations

Tracks staging capacity, stage time, retrieval time, zone balance, misplaced orders, cold-chain compliance, handoff delays, and congestion.

![Staging operations](assets/staging-page.png)

### 4. Dispensing Operations

Tracks customer wait, curbside occupancy, queue length, dispenser performance, customer ratings, no-shows, slot utilization, and SLA risk.

![Dispensing operations](assets/dispensing-page.png)

### 5. Returns and Exceptions

Tracks return reasons, refund exposure, cancellations, failed deliveries, complaints, resolution rate, unresolved cases, and fraud-risk signals.

![Returns and exceptions](assets/returns-page.png)

### 6. Store Drill-Down

Lets leadership select a store and compare its SLA, efficiency, stage performance, employee results, trends, issues, and recommended actions.

![Store drill-down](assets/store-drilldown.png)

## How It Works

```mermaid
flowchart LR
    A["Python synthetic data generator"] --> B["CSV analytics layer"]
    B --> C["Power BI-ready model"]
    B --> D["MongoDB Atlas"]
    D --> E["FastAPI live simulator"]
    E --> F["Read-only JSON API"]
    F --> G["GitHub Pages command center"]
    B --> G
```

The dashboard first attempts to read the hosted API. If the service is unavailable, it switches to a clearly labeled browser simulation so the public portfolio remains usable.

### Order Lifecycle

```text
Order Created -> Picking -> Staging -> Dispensing -> Delivery / Return
```

Every stage is timestamped. KPIs are calculated from those timestamps instead of being manually entered.

## Analytics Model

| KPI | Calculation | Decision Supported |
|---|---|---|
| Pick rate | Items / picking minutes x 60 | Labor coaching and workload balance |
| Staging time | Stage complete - stage start | Congestion and layout issues |
| Customer wait | Dispense complete - dispense start | Curbside experience risk |
| Fulfillment time | Completion - order creation | End-to-end speed |
| SLA compliance | On-time orders / total orders | Store accountability |
| Substitution rate | Substituted items / total items | Inventory availability pressure |
| Efficiency score | Weighted operational composite | Store comparison and prioritization |
| Return rate | Returned orders / total orders | Quality and customer experience |

See [the full data model](docs/data_model.md) for entities and fields.

## Live Data Design

The live service mutates approximately 10% of stores every 60 seconds. Each tick recalculates staffing, in-progress orders, queue pressure, SLA, wait time, rating, and efficiency.

MongoDB stores:

- `live_store_status`: one current-state document per store
- `live_market_snapshots`: market history for trend analysis
- `live_events`: stage-level change events

Snapshots and events receive an expiration timestamp. TTL indexes automatically remove records after 72 hours, keeping the Atlas footprint bounded while preserving a useful rolling changelog.

The public endpoint exposes read-only operational data. Database credentials are never sent to the browser.

## Manager Override Governance

The Market Manager can override operational decisions, but cannot rewrite performance data.

| Allowed leadership actions | Read-only source metrics |
|---|---|
| Reassign labor | SLA percentage |
| Prioritize a queue | Pick rate |
| Escalate a store | Customer wait |
| Approve an exception | Customer rating |
| Open an action plan | Lifecycle timestamps |

Every action is logged with scope, reason, timestamp, and an explicit `Metrics unchanged` marker. This separates authority from data integrity.

## Key Engineering Decisions

1. **Model the process, not random numbers.** Synthetic timestamps follow a valid lifecycle, which makes the derived metrics internally consistent.
2. **Separate current state from history.** Store status is updated in place; snapshots and events use rolling retention.
3. **Keep the frontend deployable anywhere.** The dashboard is plain HTML, CSS, and JavaScript hosted on GitHub Pages.
4. **Keep the backend portable.** FastAPI runs locally or on a Python host using environment-based configuration.
5. **Design for degraded service.** A labeled fallback keeps the portfolio interactive when a free hosted API sleeps or expires.
6. **Treat overrides as auditable commands.** Managers can act on the operation without editing the facts.

## Technology

| Layer | Tools |
|---|---|
| Data generation | Python, seeded synthetic logic, CSV |
| Analytics | Python, timestamp-derived KPIs |
| API | FastAPI, Uvicorn |
| Database | MongoDB Atlas, TTL indexes |
| Frontend | HTML, CSS, JavaScript |
| BI preparation | Power BI-ready fact and summary tables |
| Hosting | GitHub Pages; portable Python service configuration |
| Version control | Git, GitHub |

## Repository Structure

```text
.
├── assets/                 # Current portfolio screenshots
├── dashboard/index.html    # Interactive command center
├── data/                   # Generated and enriched CSV datasets
├── docs/                   # Architecture, BI, deployment, and case-study guides
├── live_service/app.py     # FastAPI simulator and read-only API
├── scripts/                # Generation, analytics, loading, and pipeline scripts
├── index.html              # GitHub Pages entry point
├── live-config.js          # Hosted API endpoint configuration
├── railway.toml            # Existing deployment configuration
├── requirements.txt
└── startup.sh              # Portable production start command
```

## Run Locally

### Static analytics dashboard

```bash
python3 scripts/run_pipeline.py
python3 -m http.server 8000
```

Open `http://127.0.0.1:8000/dashboard/`.

### Live API

```bash
python3 -m pip install -r requirements.txt
uvicorn live_service.app:app --reload
```

Without `MONGODB_URI`, the service runs in memory. To persist live state, set:

```bash
export MONGODB_URI="mongodb+srv://username:password@cluster-name.mongodb.net/"
export MONGODB_DATABASE="digital_fulfillment_ops"
export LIVE_RETENTION_HOURS="72"
```

Useful endpoints:

- `GET /health`
- `GET /api/live`

## Verification

The final release was checked with:

- Python compilation for the service and pipeline scripts
- Full synthetic data regeneration and analytics calculation
- API health and live-response checks
- Desktop and mobile browser layouts
- Navigation, drill-through, refresh, and override interactions
- Repository secret scan, link review, and clean Git diff validation

## What This Demonstrates

- Translating an operations problem into an analytics product
- Designing a timestamp-based fact model
- Building reproducible synthetic datasets
- Engineering decision-oriented KPIs
- Separating a static frontend from a live API
- Managing bounded retention in MongoDB
- Preparing clean tables for Power BI
- Designing an operational UI for scanning and repeated action
- Documenting technical tradeoffs for a portfolio audience

## Documentation

- [Data model](docs/data_model.md)
- [Live data deployment](docs/live_data_deployment.md)
- [MongoDB Atlas guide](docs/mongodb_atlas_guide.md)
- [Power BI guide](docs/power_bi_guide.md)
- [Azure App Service option](docs/azure_app_service_deployment.md)
- [Portfolio showcase copy](docs/beacons_showcase.md)
- [Project completion record](docs/project_plan.md)

## Author

**Urvil Godhani**

Data analytics and data science portfolio project
