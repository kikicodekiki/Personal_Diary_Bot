from commands.base import Command
from telebot import types
from RapidAPIHoroscope import RapidAPIHoroscope

class GetCompatabilityCommand(Command):
    """Handles the fetching of the compatability data."""
    def execute(self, bot, db, message, zodiac_sign):
        """Asks for the second person's zodiac_sign."""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for sign in RapidAPIHoroscope.signs:
            markup.add(types.KeyboardButton(text=sign))
        markup.add(types.KeyboardButton(text="Go Back")) # add a return button
        bot.send_message(message.chat.id, "Please select the other person's zodiac sign:", reply_markup=markup)
        bot.register_next_step_handler(message, self.get_compatibility, bot, db, zodiac_sign)

    def get_compatibility(self, message, bot, db, zodiac_sign):
        """Retrieves and sends the compatability data."""
        if message.text == "Go Back":
            from commands.AstrologyCommand import AstrologyCommand
            return AstrologyCommand().execute(bot, db, message) # Go back to Astrology menu
        second_sign = message.text.lower()
        instance = RapidAPIHoroscope(sign=zodiac_sign)
        compatability = instance.get_compatability(second_sign)
        bot.send_message(message.chat.id, compatability)
        # self.return_to_main_menu(bot, message)

    def return_to_main_menu(self, bot, message):
        """Returns the user to the main menu."""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        markup.add(types.KeyboardButton(text="Back"))
        bot.send_message(message.chat.id,"Would you like to do something else?", markup=markup)