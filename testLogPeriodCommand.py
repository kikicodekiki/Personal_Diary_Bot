from unittest.mock import MagicMock
import unittest
from datetime import datetime
from commands.MenstrualCycleCommands.LogPeriodCommand import LogPeriodCommand

class TestLogPeriodCommand(unittest.TestCase):
    """Tests only that the data that is passed and processed is correct.
            Have different tests to make sure that the data is in the db.
            """
    def setUp(self):
        """Mocks the database instance and the update and context."""
        self.mock_db = MagicMock()
        self.mock_update = MagicMock()
        self.mock_context = MagicMock()
        self.command = LogPeriodCommand(self.mock_db) # create the command that will be tested
        self.mock_update.message.chat_id = 123456
        self.mock_update.reply_text = MagicMock() # capture responses

    def test_log_period_invalid_date_format(self):
        """Test if a return massage is being passed down."""
        self.mock_context.args = ["90-40-35"]
        self.command.execute(self.mock_update, self.mock_context) # execute the command
        self.mock_update.message.reply_text.assert_called_once_with("Please provide the start date (YYYY-MM-DD).")
        self.mock_db.log_period.assert_not_called() # should not be called with the invalid date

    def test_log_period_valid_date(self):
        """Test if a valid date is logged successfully."""
        self.mock_context.args = ["2025-02-15"]
        self.command.execute(self.mock_update, self.mock_context)
        self.mock_db.log_period.assert_called_once_with(123456, datetime(2025,2,15).date())
        self.mock_update.message.reply_text.assert_called_once_with("Period logged in successfully.")

if __name__ == '__main__':
    unittest.main()
