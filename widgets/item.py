import sqlite3
from features.component import Component
from utils.logger import log

DB_FILE = "app_data.db"


class Item(Component):
    def __init__(self, name):
        super().__init__("Item", "Item", "50", "50")
        self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        self.conn.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT)")
        self.conn.commit()

    def add_item(self, item_name):
        with self.mutex:
            self.conn.execute("INSERT INTO items (name) VALUES (?)", (item_name,))
            self.conn.commit()
            log(f"Item added: {item_name}")
            self.notify(f"Item added: {item_name}")

    def get_items(self):
        with self.mutex:
            cursor = self.conn.execute("SELECT * FROM items")
            items = cursor.fetchall()
            return items