import sqlite3


class Database:
    """A class that handles the Database operations and table."""
    def __init__(self, database_name = 'diary.db'):
        self.database_name = database_name
        self.connection = sqlite3.connect(database_name, check_same_thread=False)
        # check_same_thread = False => the connection may be accessed in multiple threads;
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        """Creates two tables =>
            one that keeps users and their zodiac signs and
            another that keeps their menstrual cycle logs."""
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        zodiac_sign TEXT,
                    );
                """) # table for the users and their zodiac signs -> keeping this so as to not refactor code
        # create the table for the menstrual cycle
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS menstrual_logs (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            start_date TEXT NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                            );
        """) # make sure that when a user gets deleted => their data also gets deleted
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