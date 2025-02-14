import unittest
from unittest.mock import MagicMock
import sqlite3
from utils.Database import Database
from datetime import datetime, timedelta
import numpy as np


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
        self.assertEqual(cycle_lengths, expected_lengths)

    def test_add_user(self):
        """Test adding a user to the database."""
        self.db.add_user("new_user", "Aries")
        result = self.db.get_user_field("new_user", "zodiac_sign")
        self.assertEqual(result[0], "Aries")

    def test_update_user(self):
        """Test updating a user field."""
        self.db.update_user("test_user", "zodiac_sign", "Virgo")
        result = self.db.get_user_field("test_user", "zodiac_sign")
        self.assertEqual(result[0], "Virgo", "User update failed")

    def test_get_last_period_date(self):
        """Test retrieving the last period date."""
        self.db.log_period(self.user_id, "2025-03-01")
        last_date = self.db.get_last_period_date(self.user_id)
        self.assertEqual(last_date, datetime.strptime("2025-03-01", "%Y-%m-%d"))

    def test_predict_next_period(self):
        """Test predicting the next period start date."""
        dates = ["2025-01-01", "2025-01-30", "2025-02-28"]
        for date in dates:
            self.db.log_period(self.user_id, date)
        prediction = self.db.predict_next_period(self.user_id)
        self.assertIsInstance(prediction, tuple, "Prediction should return a tuple")
        self.assertEqual(len(prediction), 3, "Prediction tuple should have three elements")

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
