from __future__ import annotations

import asyncio
import os
import random
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta
from statistics import mean
from typing import Any

import certifi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient, ReplaceOne
from pymongo.errors import PyMongoError


DATABASE_NAME = os.environ.get("MONGODB_DATABASE", "digital_fulfillment_ops")
MONGODB_URI = os.environ.get("MONGODB_URI")
SIMULATION_INTERVAL_SECONDS = int(os.environ.get("SIMULATION_INTERVAL_SECONDS", "60"))
STORE_UPDATE_PERCENT = float(os.environ.get("STORE_UPDATE_PERCENT", "0.10"))
HISTORY_LIMIT = int(os.environ.get("HISTORY_LIMIT", "180"))
LIVE_RETENTION_HOURS = int(os.environ.get("LIVE_RETENTION_HOURS", "24"))

random.seed()

mongo_client: MongoClient | None = None
database = None
simulation_task: asyncio.Task | None = None
memory_store_status: dict[str, dict[str, Any]] = {}
memory_snapshots: list[dict[str, Any]] = []
memory_events: list[dict[str, Any]] = []


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def read_documents(collection_name: str, limit: int | None = None) -> list[dict[str, Any]]:
    if database is None:
        return []
    cursor = database[collection_name].find({}, {"_id": 0})
    if limit:
        cursor = cursor.limit(limit)
    return list(cursor)


def build_seed_statuses() -> list[dict[str, Any]]:
    rankings = read_documents("store_rankings")
    if not rankings:
        rankings = [
            {
                "store_id": f"store_{index:03d}",
                "store_number": str(1000 + index),
                "city": "Demo City",
                "state": "TX",
                "sla_percent": "91",
                "avg_pick_rate": "42",
                "avg_staging_minutes": "8",
                "avg_customer_wait_minutes": "6",
                "avg_customer_rating": "4.5",
                "efficiency_score": "78",
            }
            for index in range(1, 51)
        ]

    statuses = []
    for store in rankings:
        statuses.append(
            {
                "store_id": store["store_id"],
                "store_number": str(store["store_number"]),
                "city": store["city"],
                "state": store["state"],
                "sla_percent": float(store["sla_percent"]),
                "pick_rate": float(store["avg_pick_rate"]),
                "staging_minutes": float(store["avg_staging_minutes"]),
                "customer_wait_minutes": float(store["avg_customer_wait_minutes"]),
                "customer_rating": float(store["avg_customer_rating"]),
                "efficiency_score": float(store["efficiency_score"]),
                "active_pickers": random.randint(22, 54),
                "active_stagers": random.randint(8, 22),
                "active_dispensers": random.randint(8, 20),
                "orders_in_progress": random.randint(18, 64),
                "picking_queue": random.randint(4, 30),
                "staging_capacity_percent": random.randint(38, 88),
                "curbside_occupancy_percent": random.randint(25, 86),
                "returns_open": random.randint(0, 12),
                "alerts": random.randint(0, 5),
                "updated_at": now_iso(),
            }
        )
    return statuses


def save_store_statuses(statuses: list[dict[str, Any]]) -> None:
    global memory_store_status
    memory_store_status = {status["store_id"]: status for status in statuses}
    if database is None:
        return
    collection = database["live_store_status"]
    if statuses:
        collection.bulk_write(
            [ReplaceOne({"store_id": status["store_id"]}, status, upsert=True) for status in statuses]
        )
        collection.delete_many({"store_id": {"$nin": list(memory_store_status)}})


def load_store_statuses() -> list[dict[str, Any]]:
    if database is None:
        return list(memory_store_status.values())
    rows = read_documents("live_store_status")
    return rows or list(memory_store_status.values())


def mutate_store(status: dict[str, Any]) -> dict[str, Any]:
    next_status = dict(status)
    pick_delta = random.uniform(-4.2, 4.2)
    stage_delta = random.uniform(-1.1, 1.1)
    wait_delta = random.uniform(-1.4, 1.4)
    volume_delta = random.randint(-7, 10)

    next_status["pick_rate"] = round(clamp(float(status["pick_rate"]) + pick_delta, 24, 78), 2)
    next_status["staging_minutes"] = round(clamp(float(status["staging_minutes"]) + stage_delta, 2, 24), 2)
    next_status["customer_wait_minutes"] = round(clamp(float(status["customer_wait_minutes"]) + wait_delta, 1, 28), 2)
    next_status["active_pickers"] = int(clamp(int(status["active_pickers"]) + random.randint(-4, 5), 12, 72))
    next_status["active_stagers"] = int(clamp(int(status["active_stagers"]) + random.randint(-2, 3), 4, 32))
    next_status["active_dispensers"] = int(clamp(int(status["active_dispensers"]) + random.randint(-2, 3), 4, 28))
    next_status["orders_in_progress"] = int(clamp(int(status["orders_in_progress"]) + volume_delta, 8, 110))
    next_status["picking_queue"] = int(clamp(int(status["picking_queue"]) + random.randint(-5, 7), 0, 56))
    next_status["staging_capacity_percent"] = int(clamp(int(status["staging_capacity_percent"]) + random.randint(-7, 8), 18, 98))
    next_status["curbside_occupancy_percent"] = int(clamp(int(status["curbside_occupancy_percent"]) + random.randint(-8, 9), 8, 100))
    next_status["returns_open"] = int(clamp(int(status["returns_open"]) + random.choice([-1, 0, 0, 1]), 0, 28))

    next_status["sla_percent"] = round(
        clamp(
            100
            - max(0, next_status["customer_wait_minutes"] - 5) * 0.9
            - max(0, next_status["staging_minutes"] - 8) * 0.55
            - max(0, 42 - next_status["pick_rate"]) * 0.45,
            68,
            99.8,
        ),
        2,
    )
    next_status["customer_rating"] = round(
        clamp(4.86 - max(0, next_status["customer_wait_minutes"] - 4) * 0.055 + random.uniform(-0.08, 0.08), 2.8, 5),
        2,
    )
    next_status["efficiency_score"] = round(
        clamp(
            next_status["sla_percent"] * 0.45
            + min(next_status["pick_rate"] / 75, 1) * 25
            + max(0, 1 - next_status["customer_wait_minutes"] / 30) * 15
            + next_status["customer_rating"] / 5 * 15,
            0,
            100,
        ),
        2,
    )
    next_status["alerts"] = sum(
        [
            next_status["sla_percent"] < 90,
            next_status["customer_wait_minutes"] > 15,
            next_status["staging_capacity_percent"] > 90,
            next_status["picking_queue"] > 38,
            next_status["curbside_occupancy_percent"] > 94,
        ]
    )
    next_status["updated_at"] = now_iso()
    return next_status


def build_event(status: dict[str, Any]) -> dict[str, Any]:
    choices = [
        ("picking", f"Pick rate changed to {status['pick_rate']} items/hr"),
        ("staging", f"Staging capacity moved to {status['staging_capacity_percent']}%"),
        ("dispensing", f"Customer wait moved to {status['customer_wait_minutes']} minutes"),
        ("orders", f"{status['orders_in_progress']} orders are in progress"),
    ]
    stage, message = random.choice(choices)
    return {
        "event_id": f"evt_{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}_{status['store_id']}",
        "store_id": status["store_id"],
        "store_number": status["store_number"],
        "stage": stage,
        "message": message,
        "created_at": now_iso(),
    }


def build_market_snapshot(statuses: list[dict[str, Any]], changed_count: int) -> dict[str, Any]:
    total_active = sum(status["active_pickers"] + status["active_stagers"] + status["active_dispensers"] for status in statuses)
    total_orders = sum(status["orders_in_progress"] for status in statuses)
    return {
        "generated_at": now_iso(),
        "store_count": len(statuses),
        "active_employee_count": total_active,
        "orders_in_progress": total_orders,
        "active_pickers": sum(status["active_pickers"] for status in statuses),
        "active_stagers": sum(status["active_stagers"] for status in statuses),
        "active_dispensers": sum(status["active_dispensers"] for status in statuses),
        "picking_queue": sum(status["picking_queue"] for status in statuses),
        "returns_open": sum(status["returns_open"] for status in statuses),
        "avg_pick_rate": round(mean(status["pick_rate"] for status in statuses), 2),
        "avg_staging_minutes": round(mean(status["staging_minutes"] for status in statuses), 2),
        "avg_customer_wait_minutes": round(mean(status["customer_wait_minutes"] for status in statuses), 2),
        "avg_customer_rating": round(mean(status["customer_rating"] for status in statuses), 2),
        "sla_percent": round(mean(status["sla_percent"] for status in statuses), 2),
        "staging_capacity_percent": round(mean(status["staging_capacity_percent"] for status in statuses), 2),
        "curbside_occupancy_percent": round(mean(status["curbside_occupancy_percent"] for status in statuses), 2),
        "alert_count": sum(status["alerts"] for status in statuses),
        "stores_updated_this_tick": changed_count,
        "update_percent": round(changed_count / max(len(statuses), 1) * 100, 1),
    }


def save_snapshot(snapshot: dict[str, Any], events: list[dict[str, Any]]) -> None:
    memory_snapshots.insert(0, snapshot)
    del memory_snapshots[HISTORY_LIMIT:]
    memory_events[0:0] = events
    del memory_events[60:]

    if database is None:
        return
    expires_at = datetime.now(UTC) + timedelta(hours=LIVE_RETENTION_HOURS)
    database["live_market_snapshots"].insert_one({**snapshot, "expires_at": expires_at})
    database["live_events"].insert_many([{**event, "expires_at": expires_at} for event in events])
    cutoff = datetime.now(UTC) - timedelta(hours=LIVE_RETENTION_HOURS)
    database["live_market_snapshots"].delete_many({"generated_at": {"$lt": cutoff.isoformat(timespec="seconds")}})
    database["live_events"].delete_many({"created_at": {"$lt": cutoff.isoformat(timespec="seconds")}})


def ensure_retention_indexes() -> None:
    if database is None:
        return
    database["live_store_status"].create_index("store_id", unique=True)
    database["live_market_snapshots"].create_index("expires_at", expireAfterSeconds=0)
    database["live_events"].create_index("expires_at", expireAfterSeconds=0)


def simulate_tick() -> dict[str, Any]:
    statuses = load_store_statuses()
    if not statuses:
        statuses = build_seed_statuses()

    update_count = max(1, round(len(statuses) * STORE_UPDATE_PERCENT))
    selected_ids = {status["store_id"] for status in random.sample(statuses, update_count)}
    updated_statuses = [mutate_store(status) if status["store_id"] in selected_ids else status for status in statuses]
    changed = [status for status in updated_statuses if status["store_id"] in selected_ids]
    events = [build_event(status) for status in changed]

    save_store_statuses(updated_statuses)
    snapshot = build_market_snapshot(updated_statuses, len(changed))
    save_snapshot(snapshot, events)
    return snapshot


def latest_snapshot() -> dict[str, Any]:
    if database is not None:
        row = database["live_market_snapshots"].find_one({}, {"_id": 0}, sort=[("generated_at", -1)])
        if row:
            return row
    if memory_snapshots:
        return memory_snapshots[0]
    return simulate_tick()


async def simulation_loop() -> None:
    while True:
        simulate_tick()
        await asyncio.sleep(SIMULATION_INTERVAL_SECONDS)


@asynccontextmanager
async def lifespan(_: FastAPI):
    global mongo_client, database, simulation_task
    if MONGODB_URI:
        try:
            mongo_client = MongoClient(
                MONGODB_URI,
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
            )
            mongo_client.admin.command("ping")
            database = mongo_client[DATABASE_NAME]
            ensure_retention_indexes()
        except PyMongoError:
            if mongo_client:
                mongo_client.close()
            mongo_client = None
            database = None
    if not load_store_statuses():
        save_store_statuses(build_seed_statuses())
    simulate_tick()
    simulation_task = asyncio.create_task(simulation_loop())
    yield
    if simulation_task:
        simulation_task.cancel()
    if mongo_client:
        mongo_client.close()


app = FastAPI(title="Digital Fulfillment Live API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "digital-fulfillment-live-api", "status": "ok"}


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "database": DATABASE_NAME,
        "mongodb_connected": database is not None,
        "interval_seconds": SIMULATION_INTERVAL_SECONDS,
        "store_update_percent": STORE_UPDATE_PERCENT,
        "live_retention_hours": LIVE_RETENTION_HOURS,
    }


@app.get("/api/live")
def live_dashboard() -> dict[str, Any]:
    statuses = sorted(load_store_statuses(), key=lambda row: row["efficiency_score"], reverse=True)
    if database is not None:
        history = list(database["live_market_snapshots"].find({}, {"_id": 0}).sort("generated_at", -1).limit(30))
        events = list(database["live_events"].find({}, {"_id": 0}).sort("created_at", -1).limit(20))
    else:
        history = memory_snapshots[:30]
        events = memory_events[:20]
    return {
        "mode": "mongodb-live" if database is not None else "memory-live",
        "summary": latest_snapshot(),
        "stores": statuses,
        "history": history,
        "events": events,
    }
