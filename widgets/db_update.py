import sqlite3

from features.component import Component
from utils.logger import log

DB_FILE = "app_data.db"


class DBUpdate(Component):
    def __init__(self):
        super().__init__("DBUpdate", "DBUpdate Widget", 50, 50)
        self.query_template = ""
        self.params = {}
        self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        self.conn.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT)")
        self.conn.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, message TEXT)")
        self.conn.commit()

    def set_query(self, query):
        self.query_template = query

    def execute(self, params):
        with self.mutex:
            try:
                self.conn.execute(self.query_template.format(**params))
                self.conn.commit()
                log(f"Executed query: {self.query_template.format(**params)}")
                self.notify(f"DB updated with {params}")
            except Exception as e:
                log(f"DB update error: {e}")