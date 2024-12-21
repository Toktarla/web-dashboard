import sqlite3


def create_db():
    conn = sqlite3.connect('app_data.db')
    c = conn.cursor()

    # Create the users table
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        dashboard_id INTEGER
    )
    ''')

    # Create the items table
    c.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER UNIQUE,
        name TEXT,
        description TEXT,
        quantity INTEGER,
        price REAL
    )
    ''')

    conn.commit()
    conn.close()

def add_item(item_id, name, description, quantity, price):
    conn = sqlite3.connect('app_data.db')
    c = conn.cursor()

    try:
        c.execute("INSERT INTO items (item_id, name, description, quantity, price) VALUES (?, ?, ?, ?, ?)",
                  (item_id, name, description, quantity, price))
        conn.commit()
        print(f"Item '{name}' added with ID {item_id}.")
    except sqlite3.IntegrityError:
        print(f"Item with ID '{item_id}' already exists.")

    conn.close()


# Remove item from the items table
def remove_item(item_id):
    conn = sqlite3.connect('app_data.db')
    c = conn.cursor()

    c.execute("DELETE FROM items WHERE item_id = ?", (item_id,))
    conn.commit()
    print(f"Item with ID {item_id} removed.")
    conn.close()


def list_items():
    conn = sqlite3.connect('app_data.db')
    c = conn.cursor()

    c.execute("SELECT * FROM items")
    items = c.fetchall()

    for item in items:
        print(f"ID: {item[0]}, Item ID: {item[1]}, Name: {item[2]}, Description: {item[3]}, Quantity: {item[4]}, Price: {item[5]}")

    conn.close()


def create_user(username, dashboard_id):
    conn = sqlite3.connect('app_data.db')
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (username, dashboard_id) VALUES (?, ?)", (username, dashboard_id))
        conn.commit()
        print(f"User '{username}' attached to dashboard {dashboard_id}.")
    except sqlite3.IntegrityError:
        print(f"User '{username}' already exists.")

    conn.close()


def remove_user(username):
    conn = sqlite3.connect('app_data.db')
    c = conn.cursor()

    c.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    print(f"User '{username}' removed from the system.")
    conn.close()
