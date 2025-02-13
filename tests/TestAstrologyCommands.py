import unittest
from unittest import TestCase
from unittest.mock import MagicMock
from telebot import TeleBot

from utils.Database import Database
from commands.AstrologyCommands.AstrologyCommand import AstrologyCommand
from commands.AstrologyCommands.GetDailyHoroscopeCommand import GetDailyHoroscopeCommand
from commands.AstrologyCommands.GetCompatibilityCommand import GetCompatibilityCommand
from commands.AstrologyCommands.GetNumerologyCommand import GetNumerologyCommand


class TestAstrologyCommands(TestCase):
    """Tests for the Command Pattern implementations for the astrology portion of the bot."""
    def setUp(self):
        """Set up a mocked bot and database before each test."""
        self.bot = MagicMock(spec=TeleBot) # ensure that the mock object behaves like an instance of TeleBot
        self.database = MagicMock(spec=Database)
        self.message = MagicMock() # simulate a Telegram message; not sure for this lol
        self.message.chat.id = 123456789 # mock the behavior of the message
        self.message.from_user.first_name = "TestUser1"

    def test_astrology_command_prompts_zodiac(self):
        """Test if AstrologyCommand prompts for zodiac sign selection."""
        command = AstrologyCommand()
        command.execute(self.bot, self.database, self.message)
        self.bot.send_message.assert_called_with(
            self.message.chat.id, "Please, select your zodiac sign: ",
            reply_markup=unittest.mock.ANY # accept any reply_markup
        ) # only checking if the correct message is sent to the right chat id

    def test_astrology_command_delegates_compatibility(self):
        """Test if AstrologyCommand properly delegates to GetCompatabilityCommand."""
        command = AstrologyCommand()
        self.message.text = "Check Compatibility"
        zodiac_sign = "virgo"
        command.delegate_command(self.message, self.bot, self.database, zodiac_sign)
        # since self.bot records all methods called to it
        self.bot.send_message.assert_called() # check if the send_message was called at least once during the test

    def test_get_compatibility_fetches_data(self):
        """Test if GetCompatibilityCommand properly fetches data."""
        # honestly, did not know what to test, lol
        command = GetCompatibilityCommand()
        command.execute(self.bot, self.database, self.message, "aries")
        self.bot.send_message.assert_called()

    def test_get_numerology_fetches_data(self):
        # again - did not know what to test lol
        command = GetNumerologyCommand()
        command.execute(self.bot, self.database, self.message, "virgo")
        self.bot.send_message.assert_called()

    def test_get_daily_horoscope_fetches_data(self):
        command = GetDailyHoroscopeCommand()
        command.execute(self.bot, self.database, self.message, "virgo")
        self.bot.send_message.assert_called()

if __name__ == '__main__':
    unittest.main()