from commands.MenstrualCycleCommands.PeriodCommand import PeriodCommand
from datetime import datetime
from telebot import types


class LogPeriodCommand(PeriodCommand):
    """Command that handles the proper record of the user's menstrual cycle."""
    def execute(self, bot, db, message):
        """Prompts the user to enter the period start date."""
        user_id = message.chat.id
        markup = types.ForceReply() # allows user input
        bot.send_message(user_id, "Please provide the start date (YYYY-MM-DD).", reply_markup=markup)
        bot.register_next_step_handler(message, lambda msg: self.process_date(bot, db, msg))

    def process_date(self, bot, db, message):
        """Handles the user input for the period start date and logs it."""
        user_id = message.chat.id
        date_text = message.text.strip() # extract user input
        try:
            start_date = datetime.strptime(date_text, "%Y-%m-%d").date()
            db.log_period(user_id, start_date)
            bot.send_message(user_id, "Period logged in successfully.")
            self.return_to_main_menu(bot, message)
        except ValueError:
            bot.send_message(user_id, "Invalid date. Please provide the start date (YYYY-MM-DD).")
            self.return_to_main_menu(bot, message)

    def return_to_main_menu(self, bot, message):
        """Returns the user to the main menu."""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        markup.add(types.KeyboardButton(text="Get Astrology Reading"))
        markup.add(types.KeyboardButton(text="Menstrual Cycle Stats")) # include the menstrual cycle button
        bot.send_message(message.chat.id,"Would you like to do something else?", reply_markup=markup)