import unittest
from unittest.mock import MagicMock
from datetime import datetime
import telebot
from commands.MenstrualCycleCommands.LogPeriodCommand import LogPeriodCommand
from utils.Database import Database

class TestLogPeriodCommand(unittest.TestCase):
    def setUp(self):
        """Set up the mock environment for testing LogPeriodCommand."""
        self.mock_db = MagicMock(spec=Database)  # Mock the database
        self.mock_bot = MagicMock()
        self.command = LogPeriodCommand(self.mock_db)
        self.mock_message = MagicMock()
        self.mock_message.chat.id = 12345

    def test_log_period_valid_date(self):
        """Test logging a period with a valid date."""
        self.mock_message.text = "2025-02-12"  # simulating correct user input
        self.command.process_date(self.mock_bot, self.mock_db, self.mock_message)
        self.mock_db.log_period.assert_called_once_with(12345, datetime(2025, 2, 12).date())
        self.mock_bot.send_message.assert_any_call(12345, "Period logged in successfully.")

    def test_log_period_invalid_date(self):
        """Test when an invalid date format is provided."""
        self.mock_message.text = "invalid-date"
        self.command.process_date(self.mock_bot, self.mock_db, self.mock_message)
        self.mock_db.log_period.assert_not_called()
        self.mock_bot.send_message.assert_any_call(12345, "Invalid date. Please provide the start date (YYYY-MM-DD).")

    def test_execute_command(self):
        """Test executing the command to check if user is prompted correctly."""
        self.command.execute(self.mock_bot, self.mock_db, self.mock_message)
        self.mock_bot.send_message.assert_called_once_with(12345, "Please provide the start date (YYYY-MM-DD).",
                                                           reply_markup=unittest.mock.ANY) # so that the markup can pass

if __name__ == "__main__":
    unittest.main()

