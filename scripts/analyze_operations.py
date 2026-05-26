from __future__ import annotations

import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value)


def minutes_between(start: str, end: str) -> float:
    return (parse_time(end) - parse_time(start)).total_seconds() / 60


def pct(value: float) -> float:
    return round(value * 100, 2)


def average(values: list[float]) -> float:
    return round(mean(values), 2) if values else 0.0


def build_order_metrics(orders: list[dict], stores_by_id: dict[str, dict]) -> list[dict]:
    enriched = []
    for order in orders:
        item_count = int(order["item_count"])
        substituted_items = int(order["substituted_items"])
        picking_minutes = minutes_between(order["picking_started_at"], order["picking_completed_at"])
        staging_minutes = minutes_between(order["staging_started_at"], order["staging_completed_at"])
        wait_minutes = minutes_between(order["dispensing_started_at"], order["dispensing_completed_at"])
        fulfillment_minutes = minutes_between(order["created_at"], order["delivery_completed_at"])
        pick_rate = item_count / picking_minutes * 60
        sla_target = int(stores_by_id[order["store_id"]]["sla_target_minutes"])
        sla_hit = fulfillment_minutes <= sla_target
        substitution_rate = substituted_items / item_count if item_count else 0

        enriched.append(
            {
                **order,
                "picking_minutes": round(picking_minutes, 2),
                "staging_minutes": round(staging_minutes, 2),
                "customer_wait_minutes": round(wait_minutes, 2),
                "fulfillment_minutes": round(fulfillment_minutes, 2),
                "pick_rate_items_per_hour": round(pick_rate, 2),
                "sla_target_minutes": sla_target,
                "sla_hit": int(sla_hit),
                "substitution_rate": round(substitution_rate, 4),
            }
        )
    return enriched


def build_store_rankings(enriched_orders: list[dict], stores_by_id: dict[str, dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for order in enriched_orders:
        grouped[order["store_id"]].append(order)

    rows = []
    for store_id, orders in grouped.items():
        sla_rate = mean(int(order["sla_hit"]) for order in orders)
        avg_pick_rate = average([float(order["pick_rate_items_per_hour"]) for order in orders])
        avg_wait = average([float(order["customer_wait_minutes"]) for order in orders])
        avg_rating = average([float(order["customer_rating"]) for order in orders])
        substitution_rate = sum(int(order["substituted_items"]) for order in orders) / sum(int(order["item_count"]) for order in orders)

        efficiency_score = (
            sla_rate * 45
            + min(avg_pick_rate / 75, 1.2) * 25
            + max(0, 1 - avg_wait / 30) * 15
            + (avg_rating / 5) * 15
        )

        store = stores_by_id[store_id]
        rows.append(
            {
                "store_id": store_id,
                "store_number": store["store_number"],
                "city": store["city"],
                "state": store["state"],
                "orders": len(orders),
                "sla_percent": pct(sla_rate),
                "avg_pick_rate": avg_pick_rate,
                "avg_staging_minutes": average([float(order["staging_minutes"]) for order in orders]),
                "avg_customer_wait_minutes": avg_wait,
                "substitution_percent": pct(substitution_rate),
                "avg_customer_rating": avg_rating,
                "efficiency_score": round(efficiency_score, 2),
            }
        )

    return sorted(rows, key=lambda row: row["efficiency_score"], reverse=True)


def build_employee_scorecards(enriched_orders: list[dict], employees_by_id: dict[str, dict]) -> list[dict]:
    role_fields = {
        "picker": ("picker_id", "pick_rate_items_per_hour"),
        "stager": ("stager_id", "staging_minutes"),
        "dispenser": ("dispenser_id", "customer_wait_minutes"),
    }

    performance: dict[str, list[float]] = defaultdict(list)
    order_counts: dict[str, int] = defaultdict(int)

    for order in enriched_orders:
        for role, (employee_field, metric_field) in role_fields.items():
            employee_id = order[employee_field]
            performance[employee_id].append(float(order[metric_field]))
            order_counts[employee_id] += 1

    rows = []
    for employee_id, values in performance.items():
        employee = employees_by_id[employee_id]
        role = employee["role"]
        avg_metric = average(values)
        if role == "picker":
            score = min(avg_metric / 80, 1.25) * 100
            metric_name = "items_per_hour"
        else:
            score = max(0, 1 - avg_metric / 30) * 100
            metric_name = "minutes_per_order"

        rows.append(
            {
                "employee_id": employee_id,
                "name": employee["name"],
                "store_id": employee["store_id"],
                "role": role,
                "shift": employee["shift"],
                "orders_handled": order_counts[employee_id],
                "primary_metric": metric_name,
                "average_value": avg_metric,
                "performance_score": round(score, 2),
            }
        )

    return sorted(rows, key=lambda row: row["performance_score"], reverse=True)


def build_bottlenecks(store_rankings: list[dict]) -> list[dict]:
    rows = []
    for store in store_rankings:
        stages = [
            ("picking", float(store["avg_pick_rate"]), "higher_is_better"),
            ("staging", float(store["avg_staging_minutes"]), "lower_is_better"),
            ("dispensing", float(store["avg_customer_wait_minutes"]), "lower_is_better"),
        ]

        normalized = {
            "picking": max(0, 1 - stages[0][1] / 70),
            "staging": min(stages[1][1] / 20, 1.5),
            "dispensing": min(stages[2][1] / 25, 1.5),
        }
        worst_stage = max(normalized, key=normalized.get)
        severity = "high" if normalized[worst_stage] >= 0.75 else "medium" if normalized[worst_stage] >= 0.45 else "low"

        rows.append(
            {
                "store_id": store["store_id"],
                "store_number": store["store_number"],
                "city": store["city"],
                "worst_stage": worst_stage,
                "severity": severity,
                "bottleneck_score": round(normalized[worst_stage] * 100, 2),
                "recommended_action": recommendation_for(worst_stage, severity),
            }
        )
    return sorted(rows, key=lambda row: row["bottleneck_score"], reverse=True)


def recommendation_for(stage: str, severity: str) -> str:
    if severity == "low":
        return "Monitor performance; no immediate action needed."
    if stage == "picking":
        return "Add picker coverage, review aisle routing, and coach low pick-rate associates."
    if stage == "staging":
        return "Audit staging layout, label quality, and handoff timing."
    return "Review arrival flow, parking bay coverage, and dispenser staffing."


def build_market_summary(enriched_orders: list[dict], store_rankings: list[dict]) -> list[dict]:
    total_items = sum(int(order["item_count"]) for order in enriched_orders)
    total_subs = sum(int(order["substituted_items"]) for order in enriched_orders)
    row = {
        "total_orders": len(enriched_orders),
        "total_items": total_items,
        "sla_percent": pct(mean(int(order["sla_hit"]) for order in enriched_orders)),
        "avg_pick_rate": average([float(order["pick_rate_items_per_hour"]) for order in enriched_orders]),
        "avg_staging_minutes": average([float(order["staging_minutes"]) for order in enriched_orders]),
        "avg_customer_wait_minutes": average([float(order["customer_wait_minutes"]) for order in enriched_orders]),
        "avg_fulfillment_minutes": average([float(order["fulfillment_minutes"]) for order in enriched_orders]),
        "substitution_percent": pct(total_subs / total_items),
        "avg_customer_rating": average([float(order["customer_rating"]) for order in enriched_orders]),
        "top_store": store_rankings[0]["store_number"],
        "bottom_store": store_rankings[-1]["store_number"],
    }
    return [row]


def build_returns_exceptions(enriched_orders: list[dict]) -> list[dict]:
    reasons = ["wrong_item", "damaged_item", "late_order", "missing_item", "customer_changed_mind"]
    categories = ["grocery", "fresh", "frozen", "household", "electronics", "apparel"]
    rows = []

    for index, order in enumerate(enriched_orders, start=1):
        substitution_rate = float(order["substitution_rate"])
        rating = float(order["customer_rating"])
        fulfillment_minutes = float(order["fulfillment_minutes"])
        should_return = (
            substitution_rate > 0.18
            or rating < 3.2
            or fulfillment_minutes > float(order["sla_target_minutes"]) + 35
            or index % 47 == 0
        )

        if not should_return:
            continue

        reason = reasons[index % len(reasons)]
        status = "resolved" if index % 6 else "pending"
        refund_amount = round(8 + (int(order["item_count"]) * 2.65) + (index % 80), 2)
        resolution_minutes = 18 + (index % 160)
        exception_type = "return"

        if reason == "late_order":
            exception_type = "complaint"
        elif index % 13 == 0:
            exception_type = "refund_request"
        elif index % 29 == 0:
            exception_type = "failed_delivery"
        elif index % 31 == 0:
            exception_type = "cancellation"

        rows.append(
            {
                "exception_id": f"ex_{index:06d}",
                "order_id": order["order_id"],
                "store_id": order["store_id"],
                "created_at": order["delivery_completed_at"],
                "exception_type": exception_type,
                "reason": reason,
                "category": categories[index % len(categories)],
                "status": status,
                "refund_amount": refund_amount,
                "resolution_minutes": resolution_minutes,
                "fraud_risk_score": round((index % 100) / 100, 2),
            }
        )

    return rows


def main() -> None:
    stores = read_csv(DATA_DIR / "stores.csv")
    employees = read_csv(DATA_DIR / "employees.csv")
    orders = read_csv(DATA_DIR / "orders.csv")

    stores_by_id = {store["store_id"]: store for store in stores}
    employees_by_id = {employee["employee_id"]: employee for employee in employees}

    enriched_orders = build_order_metrics(orders, stores_by_id)
    store_rankings = build_store_rankings(enriched_orders, stores_by_id)
    employee_scorecards = build_employee_scorecards(enriched_orders, employees_by_id)
    bottlenecks = build_bottlenecks(store_rankings)
    market_summary = build_market_summary(enriched_orders, store_rankings)
    returns_exceptions = build_returns_exceptions(enriched_orders)

    write_csv(DATA_DIR / "orders_enriched.csv", enriched_orders)
    write_csv(DATA_DIR / "store_rankings.csv", store_rankings)
    write_csv(DATA_DIR / "employee_scorecards.csv", employee_scorecards)
    write_csv(DATA_DIR / "stage_bottlenecks.csv", bottlenecks)
    write_csv(DATA_DIR / "market_summary.csv", market_summary)
    write_csv(DATA_DIR / "returns_exceptions.csv", returns_exceptions)

    print("Analytics complete")
    print(f"Market SLA: {market_summary[0]['sla_percent']}%")
    print(f"Top store: #{market_summary[0]['top_store']}")
    print(f"Most severe bottleneck: Store #{bottlenecks[0]['store_number']} - {bottlenecks[0]['worst_stage']}")


if __name__ == "__main__":
    main()
