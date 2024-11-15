import sqlite3
from features.component import Component


class DBQuery(Component):
    def __init__(self):
        super().__init__("DBQuery", "Database Query", 50, 50)
        self.env['query'] = None
        self.results = []

    def refresh(self):
        if self.env['query']:
            connection = sqlite3.connect("dashboard.db")
            cursor = connection.cursor()
            cursor.execute(self.env['query'])
            self.results = cursor.fetchall()
            print(self.results)
            connection.close()
        else:
            print("No query defined in DBQuery.")

    def view(self):
        if self.results:
            results_as_strings = [str(row) for row in self.results]
            return f"DB Query Results: {', '.join(results_as_strings)}"
        else:
            return "No query results."
