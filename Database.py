import sqlite3
from datetime import datetime # using for the menstrual cycle logs

class Database:
    """A class that handles the Database operations and table."""
    def __init__(self, database_name = 'diary.db'):
        self.database_name = database_name
        # use context managers in order to refrain from opening the connection in the __init__ func
        self.create_tables()

    def create_tables(self):
        """Creates two tables:
           - One for users and their zodiac signs.
           - One for menstrual cycle logs."""
        # Using 'with' to ensure the connection is properly closed
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            # Table for users
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    zodiac_sign TEXT
                );
            """)  # removed extra comma after "zodiac_sign TEXT"

            # table for menstrual cycle logs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS menstrual_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    start_date TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                );
            """)

            conn.commit()  # Save changes

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

    def log_period(self, user_id, start_date):
        """Create a historical record of the logs for each user."""
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO menstrual_logs (user_id, start_date) VALUES(?, ?)",
                    (user_id, start_date)
                )
                conn.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}")

    def get_period_history_for_user(self, user_id):
        """Fetches the start days of each logged cycle and calculates their length."""
        """Converting the string dates into python datetime objects."""
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT start_date FROM menstrual_logs WHERE user_id=? ORDER BY start_date ASC",
                (user_id, ),
            )
            data = cursor.fetchall()
        dates = [datetime.strptime(row[0], '%Y-%m-%d') for row in data]
        cycle_lengths = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
        return cycle_lengths
