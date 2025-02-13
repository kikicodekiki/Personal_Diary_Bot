import unittest
from unittest.mock import MagicMock
from datetime import datetime
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
        self.mock_message.text = "/log_period 2025-02-12"  # simulating correct user input

    def test_log_period_valid_date(self):
        """Test logging a period with a valid date."""
        self.command.execute(self.mock_bot, self.mock_db, self.mock_message)
        self.mock_db.log_period.assert_called_once_with(12345, datetime(2025, 2, 12).date())
        self.mock_bot.send_message.assert_called_once_with(12345, "Period logged in successfully.")

    def test_log_period_missing_date(self):
        """Test when no date is provided."""
        self.mock_message.text = "/log_period"  # No date provided
        self.command.execute(self.mock_bot, self.mock_db, self.mock_message)
        self.mock_db.log_period.assert_not_called()
        self.mock_bot.send_message.assert_called_once_with(12345, "Please provide the start date (YYYY-MM-DD).")

    def test_log_period_invalid_date(self):
        """Test when an invalid date format is provided."""
        self.mock_message.text = "/log_period invalid-date"  # Invalid format
        self.command.execute(self.mock_bot, self.mock_db, self.mock_message)
        self.mock_db.log_period.assert_not_called()
        self.mock_bot.send_message.assert_called_once_with(12345, "Please provide the start date (YYYY-MM-DD).")

if __name__ == "__main__":
    unittest.main()
