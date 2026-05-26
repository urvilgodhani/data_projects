# Digital Fulfillment Command Center

A portfolio-ready retail operations analytics project for monitoring online order fulfillment across a 50-store market.

The project simulates store, employee, order, return, and manager action data; calculates operational KPIs; and presents the results in a local command-center dashboard with Power BI-ready datasets and MongoDB Atlas loading support.

![Home screen](assets/home-screen.png)

## Business Problem

Market Managers need a fast way to understand whether digital fulfillment is running smoothly across many stores.

They need to know:

- Which stores are missing SLA?
- Where are bottlenecks happening: picking, staging, or dispensing?
- Which employees are top performers?
- Which stores need training, staffing, or escalation?
- Which returns and exceptions are creating customer pain?
- What operational actions should leadership take?

## Solution

This project builds a command center that tracks online orders through the fulfillment lifecycle:

```text
Order Created -> Picking -> Staging -> Dispensing -> Delivery / Return
```

Every stage has timestamps. Those timestamps power the analytics.

## Dashboard Pages

### Home

The home screen has 5 clickable command tiles:

- Picking
- Staging
- Dispensing
- Other / Returns
- Total Store

![Home screen](assets/home-screen.png)

### Picking

Tracks active pickers, orders being picked, average pick rate, queue depth, item-found rate, picker leaderboard, slow-picking alerts, shift comparison, fatigue risk, and pick-rate trends.

![Picking page](assets/picking-page.png)

### Staging

Tracks staging capacity, staged orders, average stage time, retrieval time, staging queue, zone balance, cold-chain compliance, misplaced orders, and staging bottlenecks.

![Staging page](assets/staging-page.png)

### Dispensing

Tracks active dispensers, curbside occupancy, average customer wait, queue length, customer ratings, no-shows, slot utilization, and SLA violation warnings.

![Dispensing page](assets/dispensing-page.png)

### Returns & Exceptions

Tracks returns, refund requests, cancellations, failed deliveries, complaints, return reasons, resolution time, refund exposure, and fraud-risk indicators.

![Returns page](assets/returns-page.png)

### Total Store Drill-Down

Lets a Market Manager select a store and view store-specific performance across picking, staging, dispensing, delivery, trends, employees, comparisons, and action plans.

![Store drill-down](assets/store-drilldown.png)

## Manager Override Rule

The Market Manager can override operational actions, but not live metrics.

Allowed actions:

- Reassign labor
- Prioritize queues
- Escalate stores
- Approve exceptions
- Open action plans

Not allowed:

- Editing SLA %
- Editing pick rate
- Editing wait time
- Editing customer ratings
- Editing timestamps

The dashboard models this through auditable action logs. Metrics remain read-only.

## Metrics

- Total orders
- SLA percentage
- Average pick rate
- Average staging time
- Average customer wait
- Fulfillment time
- Substitution rate
- Customer rating
- Store efficiency score
- Employee performance score
- Bottleneck stage
- Return rate
- Resolution rate

## Architecture

```text
Python data generator
        |
        v
CSV analytics tables
        |
        +--> Local HTML command center
        |
        +--> Power BI dashboard
        |
        +--> MongoDB Atlas collections
```

## Tech Stack

- Python
- CSV analytics tables
- MongoDB Atlas
- Power BI
- HTML, CSS, JavaScript
- GitHub

## Project Structure

```text
.
├── .env.example
├── .gitignore
├── assets/
│   ├── dispensing-page.png
│   ├── home-screen.png
│   ├── picking-page.png
│   ├── returns-page.png
│   ├── staging-page.png
│   └── store-drilldown.png
├── dashboard/
│   └── index.html
├── data/
│   ├── employee_scorecards.csv
│   ├── employees.csv
│   ├── manager_overrides.csv
│   ├── market_summary.csv
│   ├── orders.csv
│   ├── orders_enriched.csv
│   ├── returns_exceptions.csv
│   ├── stage_bottlenecks.csv
│   ├── store_rankings.csv
│   └── stores.csv
├── docs/
│   ├── data_model.md
│   ├── github_showcase.md
│   ├── mongodb_atlas_guide.md
│   ├── power_bi_guide.md
│   └── project_plan.md
├── scripts/
│   ├── analyze_operations.py
│   ├── generate_data.py
│   ├── load_to_mongodb.py
│   └── run_pipeline.py
├── requirements.txt
└── README.md
```

## Quick Start

Generate data:

```bash
python3 scripts/generate_data.py
```

Calculate analytics:

```bash
python3 scripts/analyze_operations.py
```

Or rebuild everything at once:

```bash
python3 scripts/run_pipeline.py
```

Start the local dashboard:

```bash
python3 -m http.server 8000
```

Then visit:

```text
http://127.0.0.1:8000/dashboard/
```

## MongoDB Atlas

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Set environment variables:

```bash
export MONGODB_URI="mongodb+srv://username:password@cluster-name.mongodb.net/"
export MONGODB_DATABASE="digital_fulfillment_ops"
```

Load data:

```bash
python3 scripts/load_to_mongodb.py
```

See [MongoDB Atlas guide](docs/mongodb_atlas_guide.md).

## Power BI

Use the CSV files in `data/` as the first Power BI data source.

Recommended pages:

- Home
- Picking
- Staging
- Dispensing
- Returns
- Store Dashboard

See [Power BI guide](docs/power_bi_guide.md).

## Portfolio Story

This project demonstrates:

- Data modeling
- Synthetic data generation
- Operational KPI design
- Analytics engineering
- Dashboard design
- MongoDB loading
- Power BI planning
- GitHub project documentation

## Documentation

- [Data model](docs/data_model.md)
- [MongoDB Atlas guide](docs/mongodb_atlas_guide.md)
- [Power BI guide](docs/power_bi_guide.md)
- [GitHub showcase guide](docs/github_showcase.md)
- [Project plan](docs/project_plan.md)
