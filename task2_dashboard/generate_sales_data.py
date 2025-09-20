"""
generate_sales_data.py
Generates a synthetic sales_data.csv for the dashboard app.

Columns: OrderID, Date, Region, Product, Quantity, UnitPrice, Revenue
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sales_data.csv")

regions = ["North", "South", "East", "West"]
products = ["Widget A", "Widget B", "Widget C", "Gadget X", "Gadget Y"]

def generate(num_days=800, start_date="2023-01-01"):
    start = datetime.fromisoformat(start_date)
    rows = []
    order_id = 2000
    for i in range(num_days):
        date = start + timedelta(days=i)
        # for each day, random number of orders
        for _ in range(random.randint(1,6)):
            order_id += 1
            region = random.choice(regions)
            product = random.choices(products, weights=[40,30,15,10,5])[0]
            # product base price
            base_price = {
                "Widget A": 10.0,
                "Widget B": 18.0,
                "Widget C": 85.0,
                "Gadget X": 45.0,
                "Gadget Y": 60.0
            }[product]
            # vary price slightly
            unitprice = round(base_price * random.uniform(0.9, 1.2), 2)
            quantity = random.randint(1, 10)
            revenue = round(quantity * unitprice, 2)
            rows.append({
                "OrderID": order_id,
                "Date": date.strftime("%Y-%m-%d"),
                "Region": region,
                "Product": product,
                "Quantity": quantity,
                "UnitPrice": unitprice,
                "Revenue": revenue
            })
    df = pd.DataFrame(rows)
    df.to_csv(OUT, index=False)
    print(f"[generate] Created {OUT} with {len(df)} rows")

if __name__ == "__main__":
    generate()
