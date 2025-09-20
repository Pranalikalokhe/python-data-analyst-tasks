"""
crud_csv.py
CRUD operations on a sales CSV file using pandas.

Usage examples (run in terminal from project root):
# create initial sample file
python task1_crud_csv/crud_csv.py init

# add a record (create)
python task1_crud_csv/crud_csv.py create --orderid 1006 --date 2025-09-18 --region West --product "Gadget X" --quantity 5 --unitprice 19.99

# read (all)
python task1_crud_csv/crud_csv.py read --all

# read by order id
python task1_crud_csv/crud_csv.py read --orderid 1001

# update a record
python task1_crud_csv/crud_csv.py update --orderid 1006 --quantity 7 --unitprice 18.50

# delete a record
python task1_crud_csv/crud_csv.py delete --orderid 1006
"""

import argparse
import pandas as pd
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "sales.csv")

SAMPLE_DATA = [
    {"OrderID": 1001, "Date": "2025-01-05", "Region": "North", "Product": "Widget A", "Quantity": 10, "UnitPrice": 9.99},
    {"OrderID": 1002, "Date": "2025-01-09", "Region": "South", "Product": "Widget B", "Quantity": 3, "UnitPrice": 19.99},
    {"OrderID": 1003, "Date": "2025-02-11", "Region": "East",  "Product": "Widget A", "Quantity": 7, "UnitPrice": 9.99},
    {"OrderID": 1004, "Date": "2025-03-01", "Region": "West",  "Product": "Gadget Y", "Quantity": 2, "UnitPrice": 49.99},
    {"OrderID": 1005, "Date": "2025-03-15", "Region": "North", "Product": "Widget C", "Quantity": 1, "UnitPrice": 99.99},
]

def init_dataset(force=False):
    """Create the sample CSV if not exists or if force=True."""
    if os.path.exists(CSV_PATH) and not force:
        print(f"[init] File already exists at {CSV_PATH}. Use force=True to overwrite.")
        return
    df = pd.DataFrame(SAMPLE_DATA)
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    df.to_csv(CSV_PATH, index=False)
    print(f"[init] Created sample dataset at: {CSV_PATH}")
    print(df.to_string(index=False))

def create_record(orderid, date, region, product, quantity, unitprice):
    df = pd.read_csv(CSV_PATH) if os.path.exists(CSV_PATH) else pd.DataFrame()
    new = {
        "OrderID": int(orderid),
        "Date": date,
        "Region": region,
        "Product": product,
        "Quantity": int(quantity),
        "UnitPrice": float(unitprice),
    }
    new["Revenue"] = new["Quantity"] * new["UnitPrice"]
    df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)
    print("[create] Added record:")
    print(pd.DataFrame([new]).to_string(index=False))

def read_records(orderid=None, all_records=False, filters=None):
    if not os.path.exists(CSV_PATH):
        print("[read] No dataset found. Run init first.")
        return
    df = pd.read_csv(CSV_PATH)
    if orderid is not None:
        subset = df[df["OrderID"] == int(orderid)]
        print(subset.to_string(index=False) if not subset.empty else f"[read] No record with OrderID={orderid}")
    elif filters:
        q = df
        for k, v in filters.items():
            q = q[q[k] == v]
        print(q.to_string(index=False) if not q.empty else "[read] No records match filters.")
    elif all_records:
        print(df.to_string(index=False))
    else:
        print("[read] No parameters provided. Use --all or --orderid.")

def update_record(orderid, **updates):
    if not os.path.exists(CSV_PATH):
        print("[update] No dataset found. Run init first.")
        return
    df = pd.read_csv(CSV_PATH)
    idx = df.index[df["OrderID"] == int(orderid)].tolist()
    if not idx:
        print(f"[update] No record with OrderID={orderid}")
        return
    i = idx[0]
    for k, v in updates.items():
        if v is None:
            continue
        if k in ["Quantity"]:
            df.at[i,k] = int(v)
        elif k in ["UnitPrice"]:
            df.at[i,k] = float(v)
        else:
            df.at[i,k] = v
    # recalc revenue
    df.at[i, "Revenue"] = df.at[i, "Quantity"] * df.at[i, "UnitPrice"]
    df.to_csv(CSV_PATH, index=False)
    print(f"[update] Updated OrderID={orderid}:")
    print(df.loc[i:i].to_string(index=False))

def delete_record(orderid):
    if not os.path.exists(CSV_PATH):
        print("[delete] No dataset found. Run init first.")
        return
    df = pd.read_csv(CSV_PATH)
    if int(orderid) not in df["OrderID"].values:
        print(f"[delete] No record with OrderID={orderid}")
        return
    df = df[df["OrderID"] != int(orderid)]
    df.to_csv(CSV_PATH, index=False)
    print(f"[delete] Deleted record OrderID={orderid}. Current dataset:")
    print(df.to_string(index=False))

def parse_args():
    parser = argparse.ArgumentParser(description="CRUD operations on sales.csv")
    sub = parser.add_subparsers(dest="cmd")

    sub_init = sub.add_parser("init")
    sub_init.add_argument("--force", action="store_true")

    sub_create = sub.add_parser("create")
    sub_create.add_argument("--orderid", required=True)
    sub_create.add_argument("--date", required=True)
    sub_create.add_argument("--region", required=True)
    sub_create.add_argument("--product", required=True)
    sub_create.add_argument("--quantity", required=True)
    sub_create.add_argument("--unitprice", required=True)

    sub_read = sub.add_parser("read")
    sub_read.add_argument("--orderid", type=int, help="OrderID to fetch")
    sub_read.add_argument("--all", dest="all", action="store_true")
    sub_read.add_argument("--region", help="Filter by region")
    sub_read.add_argument("--product", help="Filter by product")

    sub_update = sub.add_parser("update")
    sub_update.add_argument("--orderid", required=True)
    sub_update.add_argument("--date")
    sub_update.add_argument("--region")
    sub_update.add_argument("--product")
    sub_update.add_argument("--quantity")
    sub_update.add_argument("--unitprice")

    sub_delete = sub.add_parser("delete")
    sub_delete.add_argument("--orderid", required=True)

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    if args.cmd == "init":
        init_dataset(force=args.force)
    elif args.cmd == "create":
        create_record(args.orderid, args.date, args.region, args.product, args.quantity, args.unitprice)
    elif args.cmd == "read":
        filters = {}
        if args.region:
            filters["Region"] = args.region
        if args.product:
            filters["Product"] = args.product
        read_records(orderid=args.orderid, all_records=args.all, filters=filters if filters else None)
    elif args.cmd == "update":
        update_record(args.orderid, Date=args.date, Region=args.region, Product=args.product, Quantity=args.quantity, UnitPrice=args.unitprice)
    elif args.cmd == "delete":
        delete_record(args.orderid)
    else:
        print("No command given. Use --help for usage.")
