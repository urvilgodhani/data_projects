# Beacons Portfolio Showcase

Use this page as copy-ready content for a Beacons portfolio page. The goal is to make the project feel clear, serious, and easy to understand for recruiters, professors, classmates, and hiring managers.

## Page Title

Digital Fulfillment Command Center

## Short Tagline

A live retail operations analytics dashboard that simulates online order fulfillment across a 50-store market.

## Hero Section

I built a retail digital fulfillment command center that tracks online grocery orders from creation to picking, staging, dispensing, delivery, returns, and exceptions.

The project simulates a real operations environment: 50 stores, thousands of associates, order lifecycle timestamps, performance KPIs, store rankings, bottleneck alerts, manager overrides, MongoDB storage, live API updates, and a public GitHub Pages dashboard.

This is not just a chart project. It is a full analytics product: data generation, data modeling, KPI design, operational logic, backend simulation, cloud database loading, dashboard UI, and portfolio documentation.

## Primary Links

Use these as Beacons buttons.

- Live Dashboard: `https://urvilgodhani.github.io/data_projects/`
- GitHub Repository: `https://github.com/urvilgodhani/data_projects`
- Data Model: `https://github.com/urvilgodhani/data_projects/blob/main/docs/data_model.md`
- Power BI Guide: `https://github.com/urvilgodhani/data_projects/blob/main/docs/power_bi_guide.md`
- MongoDB Guide: `https://github.com/urvilgodhani/data_projects/blob/main/docs/mongodb_atlas_guide.md`

## Project Snapshot

| Area | What I Built |
|---|---|
| Business Domain | Retail online grocery fulfillment operations |
| Scale | 50 stores, 5,000 employees, 12,000+ orders |
| Data Source | Synthetic but realistic operational data |
| Backend | Python, FastAPI, MongoDB Atlas |
| Frontend | HTML, CSS, JavaScript command center |
| BI Layer | Power BI-ready CSV tables |
| Live Mode | Python service updates about 10% of stores each minute |
| Portfolio Value | Data analytics, data engineering, dashboard design, cloud deployment |

## Business Problem

Market Managers do not manage one store. They manage performance across many stores at once.

They need fast answers:

- Which stores are falling behind SLA?
- Is the bottleneck picking, staging, or dispensing?
- Are customers waiting too long?
- Which associates are top performers?
- Which stores need coaching, labor reallocation, or escalation?
- Are returns, refunds, and complaints increasing?
- Can leadership take action without changing the live numbers?

This project answers those questions with a command center built around the actual order lifecycle.

## Solution

The dashboard tracks every order through the fulfillment flow:

```text
Order Created -> Picking -> Staging -> Dispensing -> Delivery / Return
```

Every stage has timestamps. Those timestamps power the KPIs:

- Pick rate
- Staging time
- Customer wait time
- Fulfillment time
- SLA compliance
- Substitution rate
- Return rate
- Associate performance score
- Store efficiency score
- Bottleneck stage

## Dashboard Pages

### Market Cockpit

The main page acts like a Market Manager home screen. It shows live status, current bottleneck, priority queue, operational pods, and market-level KPIs.

Best screenshot to use:

```text
assets/home-screen.png
```

### Picking

Tracks active pickers, pick queue, pick rate, item-found rate, picker leaderboard, bottom performers, fatigue risk, missed item pressure, order-size impact, and shift comparison.

Best screenshot:

```text
assets/picking-page.png
```

### Staging

Tracks staging capacity, stage time, retrieval time, zone balance, misplaced orders, cold-chain compliance, handoff delay, and staging congestion.

Best screenshot:

```text
assets/staging-page.png
```

### Dispensing

Tracks customer wait time, curbside occupancy, dispenser performance, queue length, customer ratings, no-shows, slot utilization, and SLA violation risk.

Best screenshot:

```text
assets/dispensing-page.png
```

### Returns and Exceptions

Tracks returns, cancellations, failed deliveries, complaints, refund exposure, resolution rate, exception types, fraud-risk signals, and unresolved cases.

Best screenshot:

```text
assets/returns-page.png
```

### Store Drill-Down

Lets a Market Manager select a specific store and inspect store-level performance across picking, staging, dispensing, delivery, employee performance, trends, alerts, and recommended action plans.

Best screenshot:

```text
assets/store-drilldown.png
```

## Live Data Architecture

The live version is designed so the public dashboard visibly changes over time without exposing database credentials.

```text
Python Live Simulator
        |
        | updates about 10% of stores every minute
        v
MongoDB Atlas
        |
        | read-only FastAPI endpoint
        v
GitHub Pages Dashboard
```

GitHub Pages is only the frontend. It cannot run Python, so the backend simulator runs separately and exposes safe read-only dashboard data.

## Data Model

The project uses analytics tables and MongoDB collections for:

- `stores`
- `employees`
- `orders`
- `orders_enriched`
- `store_rankings`
- `employee_scorecards`
- `stage_bottlenecks`
- `market_summary`
- `returns_exceptions`
- `manager_overrides`
- Live store status
- Live snapshots
- Live events

The most important design choice is timestamp-based analytics. Instead of manually inventing numbers, the project calculates metrics from lifecycle timestamps.

## Manager Override Rule

The Market Manager has authority to take action, but they cannot change live metrics.

Allowed:

- Reassign labor
- Prioritize queue
- Escalate store
- Approve exception
- Open action plan

Not allowed:

- Editing SLA %
- Editing pick rate
- Editing wait time
- Editing ratings
- Editing timestamps

This models real operational governance: leaders can make decisions, but metrics stay read-only and auditable.

## Difficulties and How I Solved Them

### 1. Making Fake Data Feel Real

Problem:
Random data looks fake if it does not follow business logic.

Solution:
I modeled the actual fulfillment lifecycle with timestamps. Picking starts after order creation, staging starts after picking, dispensing starts after staging, and delivery or return happens later. This made calculated KPIs feel realistic instead of random.

### 2. Creating KPIs That Mean Something

Problem:
A dashboard can look busy but still fail to answer business questions.

Solution:
I built metrics around operations decisions: SLA compliance, pick rate, staging capacity, customer wait, return rate, substitution pressure, employee performance, and bottleneck stage.

### 3. Handling Manager Override Authority

Problem:
The Market Manager should have power, but not the ability to edit live numbers.

Solution:
I separated operational actions from metrics. Metrics are read-only. Overrides create an auditable action log.

### 4. Making the Dashboard Live

Problem:
GitHub Pages is static and cannot run Python in the background.

Solution:
I separated frontend and backend. GitHub Pages hosts the dashboard, while a Python FastAPI service simulates live store updates and stores data in MongoDB Atlas.

### 5. Preventing MongoDB Storage Growth

Problem:
If a live simulator writes every minute forever, MongoDB storage will eventually fill up.

Solution:
I used a bounded retention design. Current store status stays small, and live snapshots/events expire automatically after a retention window. The database keeps a rolling history instead of growing forever.

### 6. Making the UI Look Like a Real Operations Tool

Problem:
The first design had too many cards and felt cluttered.

Solution:
I redesigned the home screen into a command cockpit: live brief, priority queue, compact operation pods, real navigation, better contrast, and clearer action buttons.

### 7. Preparing for Power BI

Problem:
Power BI needs clean tables, not messy nested app data.

Solution:
I exported Power BI-ready CSV tables: orders enriched with calculated fields, store rankings, employee scorecards, bottlenecks, returns, and market summary.

### 8. Cloud Deployment Tradeoffs

Problem:
Free hosting platforms have limits. Railway is useful, but the free trial is temporary. Azure can work, but setup has cost and billing considerations.

Solution:
I kept the architecture portable. The frontend works on GitHub Pages. The backend can run locally, on Railway, or later on Azure App Service using the included deployment guide.

## Skills Demonstrated

- Data modeling
- Synthetic data generation
- Timestamp-based analytics
- KPI design
- Python scripting
- FastAPI backend development
- MongoDB Atlas loading
- Live API design
- Frontend dashboard UI/UX
- Power BI data preparation
- GitHub documentation
- Deployment planning
- Business storytelling

## Resume Bullets

Use these for a resume or LinkedIn.

- Built a retail digital fulfillment analytics command center simulating 50 stores, 5,000 employees, and 12,000+ online orders.
- Designed timestamp-based order lifecycle data to calculate SLA compliance, pick rate, staging time, customer wait, fulfillment time, substitution rate, and return rate.
- Developed Python data pipelines to generate realistic synthetic operational data and export Power BI-ready analytics tables.
- Built a live FastAPI service that updates operational metrics and exposes read-only dashboard endpoints backed by MongoDB Atlas.
- Designed an interactive dashboard with market overview, picking, staging, dispensing, returns, and store drill-down pages.
- Modeled manager override authority as auditable actions while keeping live metrics read-only.

## Interview Explanation

Short version:

I built a retail operations analytics project that simulates online grocery fulfillment across 50 stores. It tracks orders through picking, staging, dispensing, delivery, and returns, calculates KPIs from timestamps, stores data in MongoDB, and visualizes everything in a live command-center dashboard.

Deeper version:

The core idea is that retail fulfillment is a time-based system. If I know when an order was created, when picking started and ended, when staging happened, and when the customer received the order, I can calculate the operational health of every store. I used that idea to create metrics like pick rate, SLA %, wait time, staging capacity, and bottleneck stage. Then I built a dashboard that helps a Market Manager decide where to send labor, which stores need coaching, and where customer experience is at risk.

## Beacons Layout Recommendation

Recommended Beacons block order:

1. Hero block
2. Live Dashboard button
3. GitHub Repository button
4. Screenshot gallery
5. Project Snapshot table
6. Business Problem
7. Solution / Architecture
8. Dashboard Pages
9. Difficulties and Solutions
10. Skills Demonstrated
11. Resume Bullets
12. Contact / LinkedIn / GitHub buttons

## Short Social Caption

I built a live retail digital fulfillment command center that simulates 50 stores, 5,000 employees, and 12,000+ online orders. It tracks picking, staging, dispensing, delivery, returns, bottlenecks, SLA, employee performance, and manager overrides using Python, MongoDB, FastAPI, Power BI-ready data, and a public dashboard.

## One-Line Pitch

A live analytics command center for retail online order fulfillment, built with Python, MongoDB, FastAPI, Power BI-ready data, and an interactive dashboard.
