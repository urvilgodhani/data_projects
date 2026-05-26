# Power BI Guide

Use the generated CSV files in `data/` as the first version of the Power BI dataset.

## Recommended Tables

Import these files:

- `stores.csv`
- `employees.csv`
- `orders_enriched.csv`
- `store_rankings.csv`
- `employee_scorecards.csv`
- `stage_bottlenecks.csv`
- `market_summary.csv`
- `returns_exceptions.csv`

## Relationships

Create these relationships:

- `stores[store_id]` to `orders_enriched[store_id]`
- `stores[store_id]` to `employees[store_id]`
- `employees[employee_id]` to `orders_enriched[picker_id]`

For stager and dispenser analysis, duplicate the employees table or create inactive relationships:

- `employees[employee_id]` to `orders_enriched[stager_id]`
- `employees[employee_id]` to `orders_enriched[dispenser_id]`

## Suggested Dashboard Pages

### Market Overview

- KPI cards: total orders, SLA %, average pick rate, average wait, average rating
- Store ranking table
- Bottleneck alert table
- SLA by city or state

### Store Drilldown

- Store selector
- Order volume by hour
- SLA trend
- Stage timing breakdown
- Substitution rate

### Employee Performance

- Employee scorecard table
- Top pickers by items per hour
- Stagers by minutes per order
- Dispensers by wait time

### Operations Insights

- Bottleneck by stage
- Peak hour performance
- Order size vs fulfillment time
- Substitution rate vs rating

### Manager Overrides

Add an override/action-log visual, but keep KPI measures read-only.

Recommended override actions:

- Reassign labor
- Prioritize queue
- Escalate store
- Approve exception
- Open action plan

The important business rule: overrides should record manager decisions and reasons. They should not directly edit live operational metrics such as SLA %, pick rate, wait time, or ratings.
