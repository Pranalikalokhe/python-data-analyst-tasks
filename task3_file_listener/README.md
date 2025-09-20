Task 3: File Listener and Database Upload
-----------------------------------------
File: file_listener.py

Dependencies:
- pandas, watchdog, sqlalchemy

Run:
python file_listener.py

python task3_file_listener\inspect_db.py


Then copy CSV files to the 'incoming' folder. The script will detect new CSV files and import rows into uploads.db (SQLite) table 'uploads'.

<img width="691" height="194" alt="image" src="https://github.com/user-attachments/assets/6e4a599b-a6ef-4009-9757-75b7d80849a3" />

Notes:
- The table schema is created from CSV headers.
- Errors during import will be printed to console. You can modify the handler to move files on success/failure.
