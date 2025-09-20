Task 1: CRUD Operations on Sales Dataset (CSV)
---------------------------------------------
File: crud_csv.py

Dependencies:
- pandas

Commands:
- Initialize dataset:
  python crud_csv.py init
- Create:
  python crud_csv.py create --orderid 1006 --date 2025-09-18 --region West --product "Gadget Z" --quantity 5 --unitprice 29.5
- Read all:
  python crud_csv.py read --all
- Read by OrderID:
  python crud_csv.py read --orderid 1001
- Update:
  python crud_csv.py update --orderid 1006 --quantity 7 --unitprice 28.0
- Delete:
  python crud_csv.py delete --orderid 1006

Notes:
- Revenue is automatically calculated.
- CSV path: sales.csv in this folder.
