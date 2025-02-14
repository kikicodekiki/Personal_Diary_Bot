from commands.MenstrualCycleCommands.PeriodCommand import PeriodCommand
from datetime import datetime
from telebot import types
from utils.Database import Database

class PredictNextPeriodCommand(PeriodCommand):
    """Command that tells the user when their period might start."""
    def execute(self, bot, db, message):
        """Sends the user a message about when they can expect their period to start."""
        user_id = message.chat.id
        prediction = self.db.predict_next_period(user_id)
        if isinstance(prediction, str):
            bot.send_message(message.chat.id, prediction)
        else:
            prediction = self.db.predict_next_period(user_id)
            next_date, lower_bound, upper_bound = prediction
            bot.send_message(message.chat.id, f"""
                            Predicted next period is: {next_date}\nUncertainty: {lower_bound} - {upper_bound}\n
            Keep tracking for better predictions!""")
        self.return_to_main_menu(bot, message)

    def return_to_main_menu(self, bot, message):
        """Returns the user to the main menu."""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        markup.add(types.KeyboardButton(text="Get Astrology Reading"))
        markup.add(types.KeyboardButton(text="Menstrual Cycle Stats"))  # include the menstrual cycle button
        bot.send_message(message.chat.id, "Would you like to do something else?", reply_markup=markup)