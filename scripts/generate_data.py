from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

RANDOM_SEED = 42
STORE_COUNT = 50
EMPLOYEE_COUNT = 5000
ORDER_COUNT = 12000

FIRST_NAMES = [
    "Aarav", "Aisha", "Alex", "Amara", "Andre", "Anika", "Ben", "Bianca", "Carlos",
    "Chloe", "Daniel", "Deja", "Elena", "Ethan", "Fatima", "Grace", "Hannah",
    "Isaiah", "Jalen", "Jordan", "Kai", "Layla", "Liam", "Maya", "Mia", "Noah",
    "Olivia", "Priya", "Ravi", "Sam", "Sarah", "Sofia", "Taylor", "Zoe",
]

LAST_NAMES = [
    "Anderson", "Baker", "Brooks", "Brown", "Carter", "Chen", "Davis", "Diaz",
    "Garcia", "Gupta", "Harris", "Johnson", "Jones", "Kim", "Lee", "Lopez",
    "Martinez", "Miller", "Nguyen", "Patel", "Robinson", "Shah", "Singh",
    "Smith", "Thomas", "Walker", "Williams", "Wilson", "Young",
]

CITIES = [
    ("Austin", "TX"), ("Dallas", "TX"), ("Houston", "TX"), ("San Antonio", "TX"),
    ("Fort Worth", "TX"), ("Oklahoma City", "OK"), ("Tulsa", "OK"), ("Kansas City", "MO"),
    ("St. Louis", "MO"), ("Little Rock", "AR"), ("Memphis", "TN"), ("Nashville", "TN"),
    ("Baton Rouge", "LA"), ("New Orleans", "LA"), ("Jackson", "MS"),
]

ROLES = ["picker", "stager", "dispenser"]
SHIFTS = ["morning", "midday", "evening"]


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def minutes_after(start: datetime, minutes: float) -> datetime:
    return start + timedelta(minutes=round(minutes, 2))


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_stores() -> list[dict]:
    stores = []
    for index in range(1, STORE_COUNT + 1):
        city, state = random.choice(CITIES)
        store_number = 1000 + index
        stores.append(
            {
                "store_id": f"store_{index:03d}",
                "store_number": store_number,
                "city": city,
                "state": state,
                "market": "South Central Digital",
                "sla_target_minutes": random.choice([90, 105, 120]),
                "daily_order_capacity": random.randint(180, 420),
                "performance_bias": round(random.uniform(0.82, 1.18), 3),
            }
        )
    return stores


def build_employees(stores: list[dict]) -> list[dict]:
    employees = []
    for index in range(1, EMPLOYEE_COUNT + 1):
        store = random.choice(stores)
        role = random.choices(ROLES, weights=[0.55, 0.22, 0.23], k=1)[0]
        skill = clamp(random.gauss(1.0, 0.16), 0.58, 1.42)
        employees.append(
            {
                "employee_id": f"emp_{index:05d}",
                "store_id": store["store_id"],
                "name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
                "role": role,
                "shift": random.choice(SHIFTS),
                "hire_date": (
                    datetime(2021, 1, 1) + timedelta(days=random.randint(0, 1700))
                ).date().isoformat(),
                "skill_factor": round(skill, 3),
            }
        )
    return employees


def choose_employee(pool: dict[tuple[str, str], list[dict]], store_id: str, role: str) -> dict:
    candidates = pool.get((store_id, role), [])
    if not candidates:
        candidates = [employee for (candidate_store, candidate_role), employees in pool.items() for employee in employees if candidate_role == role]
    return random.choice(candidates)


def build_orders(stores: list[dict], employees: list[dict]) -> list[dict]:
    employee_pool: dict[tuple[str, str], list[dict]] = {}
    for employee in employees:
        key = (employee["store_id"], employee["role"])
        employee_pool.setdefault(key, []).append(employee)

    stores_by_id = {store["store_id"]: store for store in stores}
    start_date = datetime(2026, 5, 1, 6, 0)
    orders = []

    for index in range(1, ORDER_COUNT + 1):
        store = random.choices(stores, weights=[store["daily_order_capacity"] for store in stores], k=1)[0]
        store_bias = float(store["performance_bias"])

        picker = choose_employee(employee_pool, store["store_id"], "picker")
        stager = choose_employee(employee_pool, store["store_id"], "stager")
        dispenser = choose_employee(employee_pool, store["store_id"], "dispenser")

        day_offset = random.randint(0, 24)
        hour = random.choices(
            population=list(range(6, 22)),
            weights=[3, 4, 5, 6, 7, 8, 9, 8, 7, 7, 8, 10, 12, 11, 8, 4],
            k=1,
        )[0]
        created_at = start_date + timedelta(days=day_offset, hours=hour - 6, minutes=random.randint(0, 59))

        item_count = max(1, int(random.lognormvariate(2.6, 0.75)))
        order_type = random.choices(["pickup", "delivery"], weights=[0.72, 0.28], k=1)[0]
        peak_multiplier = 1.2 if hour in {16, 17, 18, 19} else 1.0

        pick_rate_per_hour = 62 * float(picker["skill_factor"]) * store_bias / peak_multiplier
        picking_minutes = clamp((item_count / pick_rate_per_hour) * 60 + random.uniform(2, 10), 4, 95)
        staging_minutes = clamp(random.gauss(8, 3.2) / store_bias * peak_multiplier, 2, 35)
        queue_minutes = clamp(random.gauss(12, 9) * peak_multiplier / store_bias, 0, 55)
        dispense_minutes = clamp(random.gauss(6, 2.3) / float(dispenser["skill_factor"]), 1.5, 24)
        delivery_minutes = clamp(random.gauss(28, 12), 12, 70) if order_type == "delivery" else 0

        picking_started_at = minutes_after(created_at, random.uniform(2, 18))
        picking_completed_at = minutes_after(picking_started_at, picking_minutes)
        staging_started_at = minutes_after(picking_completed_at, random.uniform(0, 4))
        staging_completed_at = minutes_after(staging_started_at, staging_minutes)
        dispensing_started_at = minutes_after(staging_completed_at, queue_minutes)
        dispensing_completed_at = minutes_after(dispensing_started_at, dispense_minutes)
        delivery_completed_at = minutes_after(dispensing_completed_at, delivery_minutes)

        substitution_probability = clamp(0.055 + (item_count / 900), 0.02, 0.18)
        substituted_items = sum(1 for _ in range(item_count) if random.random() < substitution_probability)

        fulfillment_minutes = (delivery_completed_at - created_at).total_seconds() / 60
        sla_hit = fulfillment_minutes <= int(stores_by_id[store["store_id"]]["sla_target_minutes"])
        rating_base = 4.7 if sla_hit else 3.7
        customer_rating = clamp(random.gauss(rating_base - substituted_items * 0.03, 0.38), 1.0, 5.0)

        orders.append(
            {
                "order_id": f"ord_{index:06d}",
                "store_id": store["store_id"],
                "created_at": created_at.isoformat(timespec="minutes"),
                "picking_started_at": picking_started_at.isoformat(timespec="minutes"),
                "picking_completed_at": picking_completed_at.isoformat(timespec="minutes"),
                "staging_started_at": staging_started_at.isoformat(timespec="minutes"),
                "staging_completed_at": staging_completed_at.isoformat(timespec="minutes"),
                "dispensing_started_at": dispensing_started_at.isoformat(timespec="minutes"),
                "dispensing_completed_at": dispensing_completed_at.isoformat(timespec="minutes"),
                "delivery_completed_at": delivery_completed_at.isoformat(timespec="minutes"),
                "item_count": item_count,
                "substituted_items": substituted_items,
                "order_type": order_type,
                "customer_rating": round(customer_rating, 2),
                "picker_id": picker["employee_id"],
                "stager_id": stager["employee_id"],
                "dispenser_id": dispenser["employee_id"],
            }
        )

    return orders


def main() -> None:
    random.seed(RANDOM_SEED)
    DATA_DIR.mkdir(exist_ok=True)

    stores = build_stores()
    employees = build_employees(stores)
    orders = build_orders(stores, employees)

    write_csv(DATA_DIR / "stores.csv", stores)
    write_csv(DATA_DIR / "employees.csv", employees)
    write_csv(DATA_DIR / "orders.csv", orders)

    print(f"Generated {len(stores)} stores")
    print(f"Generated {len(employees)} employees")
    print(f"Generated {len(orders)} orders")
    print(f"Wrote files to {DATA_DIR}")


if __name__ == "__main__":
    main()

