from commands.base import Command
from telebot import types
from RapidAPIHoroscope import RapidAPIHoroscope


class GetDailyHoroscopeCommand(Command):
    """Handles the retrieval of the daily horoscope."""

    def execute(self, bot, db, message, zodiac_sign):
        """Fetches the daily horoscope."""
        instance = RapidAPIHoroscope(sign=zodiac_sign)
        horoscope = instance.get_horoscope()
        bot.send_message(message.chat.id, f"Your horoscope for today:\n\n{horoscope}")
        self.return_to_main_menu(bot, message)

    def return_to_main_menu(self, bot,message):
        """Returns to the main menu."""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        markup.add(types.KeyboardButton(text="Get Astrology Reading"))
        bot.send_message(message.chat.id, "Would you like to do something else?", reply_markup=markup)