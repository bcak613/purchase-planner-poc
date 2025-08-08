import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

BASE_PATH = Path(__file__).parent


def generate_dim_product(n: int = 1000):
    """Generate n rows for dim_product.csv and return list of SKUs."""
    header = ["sku", "fruit", "variety", "size", "label", "grade", "origin"]
    fruits = {
        "Apple": ["Gala", "Fuji", "Honeycrisp"],
        "Orange": ["Navel", "Valencia", "Blood"],
        "Banana": ["Cavendish"],
        "Pear": ["Bosc", "Anjou"],
        "Grape": ["Red", "Green"],
        "Berry": ["Strawberry", "Blueberry", "Raspberry"],
        "Peach": ["Yellow", "White"],
        "Mango": ["Kent", "Ataulfo"],
        "Melon": ["Cantaloupe", "Honeydew"],
    }
    sizes = ["Small", "Medium", "Large"]
    labels = ["FarmCo", "FreshFarms", "OrganicLtd"]
    grades = ["A", "B", "C"]
    origins = ["USA", "Mexico", "Canada", "Brazil", "Chile", "Peru", "Spain"]

    rows = [["APPL001", "Apple", "Gala", "Medium", "FarmCo", "A", "USA"]]
    sku_counter = 2
    while len(rows) < n:
        fruit = random.choice(list(fruits.keys()))
        variety = random.choice(fruits[fruit])
        size = random.choice(sizes)
        label = random.choice(labels)
        grade = random.choice(grades)
        origin = random.choice(origins)
        sku = f"{fruit[:4].upper()}{sku_counter:03d}"
        rows.append([sku, fruit, variety, size, label, grade, origin])
        sku_counter += 1

    with open(BASE_PATH / "dim_product.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    return [row[0] for row in rows]


def _random_date(start: datetime, end: datetime) -> datetime:
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


def generate_sales(skus, n: int = 1000):
    header = ["txn_date", "sku", "qty_kg", "revenue", "channel"]
    channels = ["Wholesale", "Retail", "Online"]
    start = datetime(2024, 1, 1)
    end = datetime(2024, 12, 31)

    rows = [["2024-01-15", "APPL001", 100, 2000, "Wholesale"]]
    for _ in range(n - 1):
        date = _random_date(start, end).strftime("%Y-%m-%d")
        sku = random.choice(skus)
        qty = random.randint(10, 500)
        price = random.uniform(5, 40)
        revenue = round(qty * price, 2)
        channel = random.choice(channels)
        rows.append([date, sku, qty, revenue, channel])

    with open(BASE_PATH / "sales_2024.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def generate_purchase(skus, n: int = 1000):
    header = ["po_date", "grn_date", "sku", "supplier", "qty_kg", "unit_cost"]
    suppliers = ["SupplierCo", "FreshSources", "AgriGlobal", "LocalFarm"]
    start_po = datetime(2023, 12, 1)
    end_po = datetime(2024, 12, 31)

    rows = [["2023-12-20", "2024-01-05", "APPL001", "SupplierCo", 120, "10.50"]]
    for _ in range(n - 1):
        po_date = _random_date(start_po, end_po)
        grn_date = po_date + timedelta(days=random.randint(1, 14))
        sku = random.choice(skus)
        qty = random.randint(50, 600)
        unit_cost = round(random.uniform(2, 20), 2)
        supplier = random.choice(suppliers)
        rows.append([
            po_date.strftime("%Y-%m-%d"),
            grn_date.strftime("%Y-%m-%d"),
            sku,
            supplier,
            qty,
            f"{unit_cost:.2f}",
        ])

    with open(BASE_PATH / "purchase_2024.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def generate_inventory(skus, n: int = 1000):
    header = ["snap_date", "sku", "on_hand_kg", "in_transit_kg"]
    start = datetime(2024, 1, 1)
    end = datetime(2024, 12, 31)

    rows = [["2024-01-31", "APPL001", 80, 20]]
    for _ in range(n - 1):
        date = _random_date(start, end).strftime("%Y-%m-%d")
        sku = random.choice(skus)
        on_hand = random.randint(0, 1000)
        in_transit = random.randint(0, 300)
        rows.append([date, sku, on_hand, in_transit])

    with open(BASE_PATH / "inventory_2024.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def main():
    random.seed(0)
    skus = generate_dim_product()
    generate_sales(skus)
    generate_purchase(skus)
    generate_inventory(skus)


if __name__ == "__main__":
    main()
