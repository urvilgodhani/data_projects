from __future__ import annotations

import csv
import os
from pathlib import Path

import certifi
from pymongo import MongoClient


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

COLLECTION_FILES = {
    "stores": "stores.csv",
    "employees": "employees.csv",
    "orders": "orders.csv",
    "orders_enriched": "orders_enriched.csv",
    "store_rankings": "store_rankings.csv",
    "employee_scorecards": "employee_scorecards.csv",
    "stage_bottlenecks": "stage_bottlenecks.csv",
    "market_summary": "market_summary.csv",
    "returns_exceptions": "returns_exceptions.csv",
    "manager_overrides": "manager_overrides.csv",
}


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def load_collection(database, collection_name: str, file_name: str) -> int:
    rows = read_csv(DATA_DIR / file_name)
    collection = database[collection_name]
    collection.delete_many({})
    if rows:
        collection.insert_many(rows)
    return len(rows)


def main() -> None:
    uri = os.environ.get("MONGODB_URI")
    database_name = os.environ.get("MONGODB_DATABASE", "digital_fulfillment_ops")

    if not uri:
        raise SystemExit(
            "Set MONGODB_URI before running this script. "
            "Example: export MONGODB_URI='mongodb+srv://...'"
        )

    client = MongoClient(uri, tlsCAFile=certifi.where())
    database = client[database_name]

    for collection_name, file_name in COLLECTION_FILES.items():
        count = load_collection(database, collection_name, file_name)
        print(f"Loaded {count} rows into {database_name}.{collection_name}")

    client.close()


if __name__ == "__main__":
    main()
