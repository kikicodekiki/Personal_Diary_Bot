from utils.Database import Database
from telebot import types


class PeriodCommand:
    """Parent class for the other period related commands."""
    def __init__(self, db: Database):
        self.db = db # keep an instance of the database

    def execute(self, bot, db, message):
        raise NotImplementedError("This command is not yet implemented.")

    def return_to_main_menu(self, bot,message):
        """Returns to the main menu."""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        markup.add(types.KeyboardButton(text="Get Astrology Reading"))
        markup.add(types.KeyboardButton(text="Menstrual Cycle Stats")) # include the menstrual cycle funcs
        bot.send_message(message.chat.id, "Would you like to do something else?", reply_markup=markup)


