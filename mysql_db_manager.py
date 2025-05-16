import json
import mysql.connector
from mysql.connector import Error
from pathlib import Path

class MySqlDbManager:
    def __init__(self, config_file='db_config.json'):
        self.config = self.load_config(config_file)
        self.connection = None
        self.connect()

    def load_config(self, path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Could not load DB config: {e}")
            return {}

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.config.get('host'),
                user=self.config.get('user'),
                password=self.config.get('password'),
                database=self.config.get('database')
            )
            if self.connection.is_connected():
                print("[INFO] Connected to MySQL database")
        except Error as e:
            print(f"[ERROR] MySQL connection failed: {e}")
            self.connection = None

    def insert(self, table, fields, values):
        if not self.connection or not self.connection.is_connected():
            print("[ERROR] No active database connection.")
            return

        # 🔁 Ensure values are MySQL-safe (convert dicts to JSON)
        safe_values = []
        for v in values:
            if isinstance(v, (dict, list)):
                safe_values.append(json.dumps(v))
            else:
                safe_values.append(v)

        placeholders = ', '.join(['%s'] * len(safe_values))
        columns = ', '.join(fields)
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, safe_values)
            self.connection.commit()
            print(f"[INFO] Inserted into {table}: {fields} -> {safe_values}")
        except Error as e:
            print(f"[ERROR] Insert failed: {e}")
        finally:
            if cursor:
                cursor.close()

    def __del__(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("[INFO] MySQL connection closed.")

