import unittest
from unittest.mock import MagicMock, patch
import numpy as np
import os
from commands.MenstrualCycleCommands.PlotPeriodStatsCommand import PlotPeriodStatsCommand


class TestPlotPeriodStatsCommand(unittest.TestCase):
    def setUp(self):
        """Sets up the test environment before each test."""
        self.mock_bot = MagicMock()
        self.mock_db = MagicMock()
        self.command = PlotPeriodStatsCommand(self.mock_db)
        self.mock_message = MagicMock()
        self.mock_message.chat.id = 12345

    @patch("matplotlib.pyplot.savefig")
    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_plot_period_stats_creates_and_sends_image(self, mock_open, mock_savefig):
        """Test if the period stats are plotted and sent correctly."""
        cycle_lengths = [28, 30, 27, 29, 31]  # simulated data
        with patch("os.getcwd", return_value="/tmp"):  # Ensure compatibility with different OS
            self.command.plot_period_stats(self.mock_bot, 12345, cycle_lengths, self.mock_message)
        # check if savefig() was called (plot was generated)
        mock_savefig.assert_called_once()
        # ensure image is sent
        self.mock_bot.send_photo.assert_called_once()
        args, kwargs = self.mock_bot.send_photo.call_args
        self.assertEqual(args[0], 12345)  # user id check
        self.assertIn("period chart", kwargs["caption"])


if __name__ == "__main__":
    unittest.main()
