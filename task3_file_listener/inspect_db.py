import pandas as pd

# Path to your SQLite database (absolute path)
DB_PATH = r"E:\data-analyst-assignment\task3_file_listener\uploads.db"

# Connect and query
try:
    df = pd.read_sql("SELECT * FROM uploads", f"sqlite:///{DB_PATH}")
    print(df.head())
except Exception as e:
    print(f"Error reading database: {e}")
