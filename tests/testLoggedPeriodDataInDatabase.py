import unittest
from commands.MenstrualCycleCommands.LogPeriodCommand import LogPeriodCommand
from utils.Database import Database
import sqlite3


class TestLoggedPeriodDataInDatabase(unittest.TestCase):
    """Testing to see if the data is being added to the database correctly."""
    def setUp(self):
        """Set up a test database before each test => will need to clean it up afterwards."""
        self.mock_database = Database("test_diary.db")
        self.command = LogPeriodCommand(self.mock_database)
        # ensure that the table exists
        with sqlite3.connect("test_diary.db") as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS menstrual_logs (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER NOT NULL,
                                start_date TEXT NOT NULL,
                                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                            );
                        """)
            connection.commit()

    def test_period_log_insertion_into_database(self):
        """Check if the period entry is stored in the database."""
        user_id = 12345
        start_date = "2023-10-01" # send string, not datetime object
        # log the period
        self.mock_database.log_period(user_id, start_date)
        with sqlite3.connect("test_diary.db") as connection:
            cursor = connection.cursor()
            cursor.execute("""
                    SELECT user_id, start_date FROM menstrual_logs WHERE user_id = ?""",
                           (user_id,))
            result = cursor.fetchall()
        self.assertEqual(result[0], (user_id, start_date))
        self.assertEqual(len(result), 1)

    def tearDown(self):
        """Clean up after test cases."""
        with sqlite3.connect("test_diary.db") as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM menstrual_logs")
            connection.commit()

if __name__ == '__main__':
    unittest.main()