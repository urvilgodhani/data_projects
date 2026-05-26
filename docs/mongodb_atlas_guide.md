# MongoDB Atlas Guide

MongoDB Atlas is the cloud database layer for this project.

## What Goes Into MongoDB

Recommended collections:

- `stores`
- `employees`
- `orders`
- `orders_enriched`
- `store_rankings`
- `employee_scorecards`
- `stage_bottlenecks`
- `returns_exceptions`
- `market_summary`
- `manager_overrides`

## Setup Steps

1. Create a free MongoDB Atlas account.
2. Create a free shared cluster.
3. Create a database user.
4. Add your current IP address to Network Access.
5. Copy the Python connection string.
6. Create a local `.env` file from `.env.example`.
7. Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

8. Export your connection values:

```bash
export MONGODB_URI="mongodb+srv://username:password@cluster-name.mongodb.net/"
export MONGODB_DATABASE="digital_fulfillment_ops"
```

9. Load the data:

```bash
python3 scripts/load_to_mongodb.py
```

## Why MongoDB Fits This Project

The order lifecycle has nested, event-style data in the real world. MongoDB works well for flexible operational records such as:

- Order timestamps
- Stage events
- Exception records
- Manager action logs
- Store-level operational snapshots

For this portfolio version, CSV files are the local source of truth and MongoDB Atlas is the cloud serving layer.

## Power BI Note

Power BI can start from the CSV files first. That is simpler and completely acceptable for the first dashboard.

After the dashboard is polished, MongoDB can become the cloud data source through one of these approaches:

- MongoDB BI Connector
- Exported Atlas data files
- A small API layer
- Scheduled CSV refresh from MongoDB
