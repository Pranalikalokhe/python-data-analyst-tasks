Task 3: File Listener and Database Upload
-----------------------------------------
File: file_listener.py

Dependencies:
- pandas, watchdog, sqlalchemy

Run:
python file_listener.py

Then copy CSV files to the 'incoming' folder. The script will detect new CSV files and import rows into uploads.db (SQLite) table 'uploads'.

Notes:
- The table schema is created from CSV headers.
- Errors during import will be printed to console. You can modify the handler to move files on success/failure.
