import sqlite3


class Database:
    """A class that handles the Database operations and table."""
    def __init__(self, database_name = 'diary.db'):
        self.database_name = database_name
        self.connection = sqlite3.connect(database_name, check_same_thread=False)
        # check_same_thread = False => the connection may be accessed in multiple threads;
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            zodiac_sign TEXT,
                            period_start DATE,
                            period_end DATE,
                            mood TEXT,
                            )
                            ''')
        self.connection.commit()

    def add_user(self, username):
        self.cursor.execute('INSERT OR IGNORE INTO users (username) VALUES (?)', (username,))
        self.connection.commit()

    def update_user(self, username, field, value):
        self.cursor.execute(f'UPDATE users SET {field}=? WHERE username=?', (value, username))
        self.connection.commit()

    def get_user_field(self, username, field):
        self.cursor.execute(f'SELECT {field} FROM users WHERE username=?', (username,))
        return self.cursor.fetchone()

    def close(self):
        self.connection.close()