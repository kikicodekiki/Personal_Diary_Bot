from commands.base import Command
from telebot import types
from RapidAPIHoroscope import RapidAPIHoroscope

class GetNumerologyCommand(Command):
    """Handles numerology readings."""
    def execute(self, bot, db, message, zodiac_sign):
        """Asks for the person's life path number."""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range (1,10):
            markup.add(types.KeyboardButton(text=str(i)))
        markup.add(types.KeyboardButton(text="Go Back")) # add a go back button
        bot.send_message(message.chat.id,
                         "Please select your life path number.\n"
                         "You can find it by adding up all the digits from your birth date until you get a single digit number.\n",
                         reply_markup=markup
        )
        bot.register_next_step_handler(message, self.get_numerology, bot, db)

    def get_numerology(self, message, bot, db):
        """Fetches and sends the numerology results."""
        if message.text == "Go Back":
            from commands.AstrologyCommands.AstrologyCommand import AstrologyCommand # use lazy imports to prevent circular import
            return AstrologyCommand().execute(bot, db, message)
        if not message.text.isdigit():
            bot.send_message(message.chat.id, "Invalid input. Please try again.")
            self.execute(bot, db, message, None)
            return
        numerology_number = int(message.text)
        instance = RapidAPIHoroscope(numerology_number=numerology_number)
        numerology = instance.get_numerology()
        bot.send_message(message.chat.id, f"Your life path reading:\n\n{numerology}")
        # return to main menu
        self.return_to_main_menu(bot, message)

    def return_to_main_menu(self, bot, message):
        """Returns the user to the main menu."""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        markup.add(types.KeyboardButton(text="Get Astrology Reading"))
        markup.add(types.KeyboardButton(text="Menstrual Cycle Stats")) # include menstrual cycle funcs
        bot.send_message(message.chat.id, "Would you like to do anything else?", reply_markup=markup)

