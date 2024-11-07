from features.widget import Widget
import sqlite3


class DBQuery(Widget):
    def __init__(self, title="DB Query"):
        super().__init__(name="DBQuery", title=title)
        self.env['query'] = ""
        self.db_path = "example.db"
        self.events.append('refresh')

    def execute_query(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(self.env['query'])
                return cursor.fetchall()
        except Exception as e:
            return f"Query failed: {e}"

    def refresh(self):
        results = self.execute_query()
        return f"Query Results: {results}"