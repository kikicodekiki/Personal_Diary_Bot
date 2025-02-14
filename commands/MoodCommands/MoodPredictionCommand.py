from commands.base import Command
from utils.RapidAPIHoroscope import RapidAPIHoroscope
from datetime import datetime
from telebot import types

class MoodPredictionCommand(Command):
    """Predicts the user's mood based on their current menstrual cycle phase and daily horoscope."""
    def execute(self, bot, db, message):
        """Fetches the daily horoscope and determines the user's menstrual cycle phase."""
        user_first_name = message.from_user.first_name
        user_id = message.chat.id
        zodiac_sign = db.get_user_field(user_first_name, 'zodiac_sign')
        if not zodiac_sign:
            bot.send_message(user_id, "Zodiac sign not in Database. Add it before proceeding.")

    def return_to_main_menu(self, bot, db, message):