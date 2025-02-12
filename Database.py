import sqlite3


class Database:
    """A class that handles the Database operations and table."""
    def __init__(self, database_name = 'diary.db'):
        self.database_name = database_name
        # use context managers in order to refrain from opening the connection in the __init__ func
        self.create_tables()

    def create_tables(self):
        """Creates two tables =>
            one that keeps users and their zodiac signs and
            another that keeps their menstrual cycle logs."""
        # use the "with - as conn" structure to ensure that there are no multiple connections that stay open at the same time
        with (sqlite3.connect(self.database_name) as conn):
            cursor = conn.cursor()
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        zodiac_sign TEXT,
                    );
                """) # table for the users and their zodiac signs -> keeping this so as to not refactor code
            # create the table for the menstrual cycle
            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS menstrual_logs (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            start_date TEXT NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                            );
            """) # make sure that when a user gets deleted => their data also gets deleted
            conn.commit()

    def add_user(self, username, zodiac_sign=None):
        """Adds a new user to the database if not already present."""
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT OR IGNORE INTO users (username, zodiac_sign) VALUES (?, ?)",
                    (username, zodiac_sign),
                )
                conn.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}")

    def update_user(self, username, field, value):
        # modify logic to use context managers so as to ensure proper file management
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(f'UPDATE users SET {field}=? WHERE username=?', (value, username))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}")

    def get_user_field(self, username, field):
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(f'SELECT {field} FROM users WHERE username=?', (username,))
                return cursor.fetchone()
            except sqlite3.Error as e:
                print(f"Database error: {e}")

    # def close(self):
    #     self.connection.close() => no need for this function anymore since we are working with context managers