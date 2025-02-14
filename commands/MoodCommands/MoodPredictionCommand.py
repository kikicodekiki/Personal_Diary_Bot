from commands.base import Command
from utils.RapidAPIHoroscope import RapidAPIHoroscope
from datetime import datetime
from telebot import types
from utils.Database import Database
import numpy as np

class MoodPredictionCommand(Command):
    """Predicts the user's mood based on their current menstrual cycle phase and daily horoscope."""
    def execute(self, bot, db, message):
        """Fetches the daily horoscope and determines the user's menstrual cycle phase."""
        user_first_name = message.from_user.first_name
        user_id = message.chat.id
        zodiac_sign = db.get_user_field(user_first_name, 'zodiac_sign')
        if not zodiac_sign:
            bot.send_message(user_id, "Zodiac sign not in Database. Add it before proceeding.")
            return self.return_to_main_menu(bot, db)
        if isinstance(zodiac_sign, tuple):
            zodiac_sign = zodiac_sign[0] # because it is returning a tuple for some reason??
        if not isinstance(zodiac_sign, str):  # ✅ Ensure it's a string
            bot.send_message(user_id, "Error retrieving zodiac sign. Please set it again.")
            return self.return_to_main_menu(bot, message)
        # get the horoscope for today
        horoscope_instance = RapidAPIHoroscope(sign=zodiac_sign)
        horoscope_text = horoscope_instance.get_horoscope()
        #get the last period date
        last_period_date = db.get_last_period_date(user_id)
        if not last_period_date:
            bot.send_message(user_id, "Couldn't find your period history. Please log your period first.")
            return self.return_to_main_menu(bot, message)
        # get the date today
        today = datetime.today().date() # to calculate the menstrual cycle phase
        last_period_date = last_period_date.date()
        days_since_last_period = (today - last_period_date).days
        # determine the cycle phase
        cycle_phase = self.determine_cycle_phase(user_id, db, days_since_last_period)
        # generate the response
        response = (
            f"🌙 **Mood Prediction for Today** 🌙\n"
            f"🔮 **Horoscope for {zodiac_sign.capitalize()}**:\n"
            f"_{horoscope_text}_\n\n"
            f"🩸 **Menstrual Cycle Phase**: {cycle_phase['name']}\n"
            f"💡 **Mood Description**: {cycle_phase['description']}"
        )
        bot.send_message(user_id, response, parse_mode="Markdown")
        return self.return_to_main_menu(bot, message)

    def determine_cycle_phase(self,user_id, db, days_since_last_period):
        """Fetches the average cycle length and checks in which category it falls."""
        average_cycle_len = int(np.mean(db.get_period_history_for_user(user_id)))
        # devide into 4 phases dynamically
        menstrual_phase = average_cycle_len * 0.25 # ~25%
        follicular_phase = average_cycle_len * 0.50
        ovulatory_phase = average_cycle_len * 0.75
        luteal_phase = average_cycle_len
        # find the correct phase and send the proper description
        if days_since_last_period <= menstrual_phase:
            return {"name": "Menstrual Phase", "description": "Inward focus, reflection, and restful energy."}
        elif days_since_last_period <= follicular_phase:
            return {"name": "Follicular Phase", "description": "Outward focus, curiosity, and rising energy."}
        elif days_since_last_period <= ovulatory_phase:
            return {"name": "Ovulatory Phase", "description": "Outward focus, achievement, and peak energy."}
        elif days_since_last_period <= luteal_phase:
            return {"name": "Luteal Phase", "description": "Inward focus, completion, and waning energy."}
        else:
            return {"name": "Unknown Phase", "description": "Cycle data might be inaccurate, please log your period."}

