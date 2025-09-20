"""
file_listener.py
Monitors the 'incoming' directory. When a new CSV is added, it reads it and uploads rows to a SQLite database table 'uploads'.

Run:
python task3_file_listener/file_listener.py

Then copy a CSV into task3_file_listener/incoming/ (the script will detect & import it).
"""


import time
import os
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from sqlalchemy import create_engine
import logging


BASE_DIR = os.path.dirname(__file__)
INCOMING = os.path.join(BASE_DIR, "incoming")
DB_PATH = os.path.join(BASE_DIR, "uploads.db")
os.makedirs(INCOMING, exist_ok=True)

# Setup logging
LOG_PATH = os.path.join(BASE_DIR, "listener.log")
logging.basicConfig(filename=LOG_PATH, level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)


class CSVHandler(FileSystemEventHandler):
    REQUIRED_COLUMNS = {"OrderID", "Date", "Region", "Product", "Quantity", "UnitPrice", "Revenue"}

    def on_created(self, event):
        if event.is_directory:
            return
        filepath = event.src_path
        if not filepath.lower().endswith(".csv"):
            msg = f"Ignored non-csv file: {filepath}"
            print(f"[listener] {msg}")
            logging.info(msg)
            return
        try:
            print(f"[listener] Detected new CSV: {filepath}")
            logging.info(f"Detected new CSV: {filepath}")
            df = pd.read_csv(filepath)
            if df.empty:
                msg = f"CSV is empty: {filepath}"
                print(f"[listener] {msg}")
                logging.warning(msg)
                return
            # sanitize columns: to lowercase, remove spaces
            df.columns = [c.strip().replace(" ", "_") for c in df.columns]
            # Validate columns
            if not self.REQUIRED_COLUMNS.issubset(set(df.columns)):
                msg = f"Missing required columns in {filepath}: {self.REQUIRED_COLUMNS - set(df.columns)}"
                print(f"[listener] {msg}")
                logging.error(msg)
                return
            # write to sqlite table 'uploads' - append
            df.to_sql("uploads", engine, if_exists="append", index=False)
            msg = f"Imported {len(df)} rows into uploads.db -> uploads table."
            print(f"[listener] {msg}")
            logging.info(msg)
        except Exception as e:
            msg = f"Error importing {filepath}: {e}"
            print(f"[listener] {msg}")
            logging.error(msg)


def start_listener():
    event_handler = CSVHandler()
    observer = Observer()
    observer.schedule(event_handler, INCOMING, recursive=False)
    observer.start()
    print(f"[listener] Monitoring directory: {INCOMING}")
    print(f"[listener] Database will be at: {DB_PATH}")
    print(f"[listener] Logging to: {LOG_PATH}")
    logging.info(f"Monitoring directory: {INCOMING}")
    logging.info(f"Database will be at: {DB_PATH}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[listener] Stopping listener...")
        logging.info("Stopping listener...")
        observer.stop()
    observer.join()

if __name__ == "__main__":
    # Let pandas.to_sql create the uploads table structure when the first CSV arrives.
    start_listener()
