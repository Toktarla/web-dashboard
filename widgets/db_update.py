from features.component import Component
import sqlite3

class DBUpdate(Component):
    def __init__(self):
        super().__init__("DBUpdate", "Database Update", 50, 50)
        self.env['query'] = None
        self.events.append('submit')
        self.result = None
        
    def submit(self, params):
        if self.env['query']:
            try:
                formatted_query = self.env['query'].format(**params)
                connection = sqlite3.connect("dashboard.db")
                cursor = connection.cursor()
                cursor.execute(formatted_query)
                connection.commit()
                self.result = "Query executed successfully"
            except Exception as e:
                self.result = f"Error executing query: {str(e)}"
            finally:
                connection.close()
        else:
            self.result = "No query defined"
            
    def view(self):
        return f"DB Update Result: {self.result if self.result else 'No query executed'}"