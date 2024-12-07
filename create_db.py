import sqlite3

def create_database():
    conn = sqlite3.connect('users.db')  # Create the database file
    cursor = conn.cursor()

    # Create the users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Add a test user
    try:
        cursor.execute('''
            INSERT INTO users (username, password) 
            VALUES ('admin', 'admin123')
        ''')
        print("Test user added.")
    except sqlite3.IntegrityError:
        print("User already exists.")

    conn.commit()
    conn.close()
    print("Database setup complete.")

if __name__ == "__main__":
    create_database()
