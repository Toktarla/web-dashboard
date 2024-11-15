import sqlite3


def create_db():
    conn = sqlite3.connect('dashboard.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        dashboard_id INTEGER
    )
    ''')
    conn.commit()
    conn.close()


def create_user(username, dashboard_id):
    conn = sqlite3.connect('dashboard.db')
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (username, dashboard_id) VALUES (?, ?)", (username, dashboard_id))
        conn.commit()
        print(f"User '{username}' attached to dashboard {dashboard_id}.")
    except sqlite3.IntegrityError:
        print(f"User '{username}' already exists.")

    conn.close()


def remove_user(username):
    conn = sqlite3.connect('dashboard.db')
    c = conn.cursor()

    c.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    print(f"User '{username}' removed from the system.")
    conn.close()
