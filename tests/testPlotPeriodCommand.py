import unittest
from unittest.mock import MagicMock, patch
import numpy as np
from commands.MenstrualCycleCommands.PlotPeriodStatsCommand import PlotPeriodStatsCommand


class TestPlotPeriodStatsCommand(unittest.TestCase):
    def setUp(self):
        """Sets up the test environment before each test."""
        self.mock_bot = MagicMock()  # Mock the Telegram bot
        self.mock_db = MagicMock()  # Mock the database
        self.command = PlotPeriodStatsCommand(self.mock_db)  # Instantiate command

        # Mock Telegram message object
        self.mock_message = MagicMock()
        self.mock_message.chat.id = 12345

    def test_execute_with_insufficient_data(self):
        """Test case where user has fewer than 2 cycle records."""
        self.mock_db.get_period_history_for_user.return_value = [28]  # Only one cycle length

        self.command.execute(self.mock_bot, self.mock_db, self.mock_message)

        # ✅ Ensure bot sends an error message
        self.mock_bot.send_message.assert_called_once_with(12345, "Not enough data found for this user.")

    @patch("matplotlib.pyplot.savefig")
    def test_plot_period_stats_creates_and_sends_image(self, mock_savefig):
        """Test if the period stats are plotted and sent correctly."""
        cycle_lengths = [28, 30, 27, 29, 31]  # Simulated data

        self.command.plot_period_stats(self.mock_bot, 12345, cycle_lengths, self.mock_message)

        # ✅ Check if `savefig()` was called (plot was generated)
        mock_savefig.assert_called_once_with("/mnt/data/period_stats.png")

        # ✅ Ensure image is sent
        self.mock_bot.send_photo.assert_called_once()
        args, kwargs = self.mock_bot.send_photo.call_args
        self.assertEqual(args[0], 12345)  # User ID check
        self.assertIn("period chart", kwargs["caption"])  # Caption check

    def test_return_to_main_menu(self):
        """Test if the bot returns to the Menstrual Cycle Stats menu."""
        self.command.return_to_main_menu(self.mock_bot, self.mock_message)

        # ✅ Ensure bot sends the correct menu
        self.mock_bot.send_message.assert_called_once_with(12345, "What would you like to do next?",
                                                           reply_markup=MagicMock())


if __name__ == "__main__":
    unittest.main()
