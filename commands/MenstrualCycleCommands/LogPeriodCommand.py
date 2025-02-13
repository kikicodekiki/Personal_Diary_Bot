from commands.MenstrualCycleCommands.PeriodCommand import PeriodCommand
from datetime import datetime
from telebot import types


class LogPeriodCommand(PeriodCommand):
    """Command that handles the proper record of the user's menstrual cycle."""
    def execute(self, bot, db, message):
        """Prompts the user to enter the period start date."""
        user_id = message.chat.id
        args = message.text.split()[1:] # extract arguments from message
        if not args:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=False)
            bot.send_message(user_id, "Please provide the start date (YYYY-MM-DD).", reply_markup=markup)
            return self.execute(bot, db, message)
        try:
            start_date = datetime.strptime(args[0], "%Y-%m-%d").date()
            db.log_period(user_id, start_date)
            bot.send_message(user_id, "Period logged in successfully.")
        except ValueError:
            bot.send_message(user_id, "Invalid date. Please provide the start date (YYYY-MM-DD).")
