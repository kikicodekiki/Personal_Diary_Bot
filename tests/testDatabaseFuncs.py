import unittest
from unittest.mock import MagicMock
import sqlite3
from utils.Database import Database
from datetime import datetime

class testDatabaseFuncs(unittest.TestCase):
    def setUp(self):
        """Sets up a test database connection."""
        self.test_db = "test_diary.db"
        self.db = Database(self.test_db)
        self.user_id = None
        self._setup_test_user()

    def _setup_test_user(self):
        """Helper method to create a test user."""
        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, zodiac_sign) VALUES (?, ?)", ("test_user", "Leo"))
            conn.commit()
            self.user_id = cursor.lastrowid

    def test_log_period(self):
        """Test logging periods and retrieving cycle history."""
        dates = ["2025-01-01", "2025-01-30", "2025-02-28"]  # Example period start dates
        for date in dates:
            self.db.log_period(self.user_id, date)
        cycle_lengths = self.db.get_period_history_for_user(self.user_id)
        expected_lengths = [(datetime.strptime(dates[i], "%Y-%m-%d") - datetime.strptime(dates[i - 1], "%Y-%m-%d")).days
                            for i in range(1, len(dates))]
        self.assertEqual(cycle_lengths, expected_lengths, "Cycle lengths do not match expected values")

    def tearDown(self):
        """Clean up test database after each test."""
        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS users")
            cursor.execute("DROP TABLE IF EXISTS menstrual_logs")
            conn.commit()
            cursor.close()

if __name__ == "__main__":
    unittest.main()