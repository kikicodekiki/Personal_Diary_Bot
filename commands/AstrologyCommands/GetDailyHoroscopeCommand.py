from commands.base import Command
from telebot import types
from utils.RapidAPIHoroscope import RapidAPIHoroscope


class GetDailyHoroscopeCommand(Command):
    """Handles the retrieval of the daily horoscope."""

    def execute(self, bot, db, message, zodiac_sign):
        """Fetches the daily horoscope."""
        instance = RapidAPIHoroscope(sign=zodiac_sign)
        horoscope = instance.get_horoscope()
        bot.send_message(message.chat.id, f"Your horoscope for today:\n\n{horoscope}")
        self.return_to_main_menu(bot, message)

