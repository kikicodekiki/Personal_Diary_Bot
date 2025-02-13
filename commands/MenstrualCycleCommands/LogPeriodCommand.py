from commands.MenstrualCycleCommands.PeriodCommand import PeriodCommand
from datetime import datetime


class LogPeriodCommand(PeriodCommand):
    """Command that handles the proper record of the user's menstrual cycle."""
    def execute(self, update, context):
        """Makes a connection with the database and logs in a new period entry."""
        user_id = update.message.chat_id
        if not context.args:
            update.message.reply_text("Please provide the start date (YYYY-MM-DD).")
            return
        try:
            start_date = datetime.strptime(context.args[0], "%Y-%m-%d").date()
            self.db.log_period(user_id, start_date)
            update.message.reply_text("Period logged in successfully.")
        except ValueError:
            update.message.reply_text("Please provide the start date (YYYY-MM-DD).")


from unittest.mock import MagicMock
import unittest
from Database import Database
import sqlite3

class TestLogPeriodDatabase(unittest.TestCase):
    def setUp(self):
        """Set up a test database before each test."""
        self.db = Database("test_diary.db")  # use a separate test database
        self.command = LogPeriodCommand(self.db)
        # ensure that the test table exists
        with sqlite3.connect("test_diary.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS menstrual_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    start_date TEXT NOT NULL
                );
            """)
            conn.commit()

    def test_period_log_insertion(self):
        """Check if a period entry is stored in the database."""
        user_id = 12345
        start_date = "2025-02-12"
        # log the period
        self.db.log_period(user_id, start_date)
        # check if the data was inserted
        with sqlite3.connect("test_diary.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, start_date FROM menstrual_logs WHERE user_id = ?", (user_id,))
            result = cursor.fetchall()
        #Expect one entry in the database
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (user_id, start_date))

    def tearDown(self):
        """Clean up the test database after each test."""
        with sqlite3.connect("test_diary.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM menstrual_logs")  # clear test data
            conn.commit()

if __name__ == "__main__":
    unittest.main()