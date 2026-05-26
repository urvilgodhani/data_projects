# Data Model

This project uses a simple analytics-friendly model built around an order lifecycle.

## Entities

### Stores

Each store belongs to one market and has operating targets.

Important fields:

- `store_id`
- `store_number`
- `city`
- `state`
- `market`
- `sla_target_minutes`

### Employees

Employees belong to a store and work in one fulfillment role.

Important fields:

- `employee_id`
- `store_id`
- `name`
- `role`
- `shift`
- `hire_date`

### Orders

Orders are the primary fact table. Each row represents one online order and contains lifecycle timestamps.

Important fields:

- `order_id`
- `store_id`
- `created_at`
- `picking_started_at`
- `picking_completed_at`
- `staging_started_at`
- `staging_completed_at`
- `dispensing_started_at`
- `dispensing_completed_at`
- `delivery_completed_at`
- `item_count`
- `substituted_items`
- `order_type`
- `customer_rating`
- `picker_id`
- `stager_id`
- `dispenser_id`

## Calculated Metrics

### Pick Rate

```text
item_count / picking_minutes * 60
```

Shows how many items a picker completes per hour.

### Staging Time

```text
staging_completed_at - staging_started_at
```

Shows whether orders are moving cleanly through the holding area.

### Customer Wait

```text
dispensing_completed_at - dispensing_started_at
```

Shows how long customers or drivers wait after arrival.

### Fulfillment Time

```text
delivery_completed_at - created_at
```

Shows total click-to-completion speed.

### SLA Hit

```text
fulfillment_minutes <= sla_target_minutes
```

Shows whether the order was completed within the store target.

### Substitution Rate

```text
substituted_items / item_count
```

Acts as a proxy for inventory quality and availability.

### Efficiency Score

A composite score that rewards SLA performance, pick speed, low wait time, and customer satisfaction.

## Manager Overrides

The Market Manager has authority to override operational decisions, but not live metrics.

Examples of allowed overrides:

- Reassign labor between picking, staging, and dispensing
- Prioritize a queue or urgent order group
- Escalate a store for leadership attention
- Approve a return or exception
- Open a store action plan

Examples of disallowed overrides:

- Editing live SLA %
- Editing pick rate
- Editing customer wait time
- Editing customer ratings
- Editing generated timestamps

This keeps the dashboard realistic: live numbers remain read-only and auditable, while managers can still take action based on what the numbers show.

Suggested fields:

- `override_id`
- `created_at`
- `manager_id`
- `scope`
- `store_id`
- `action`
- `reason`
- `metric_edit_allowed`
- `status`
