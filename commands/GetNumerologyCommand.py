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
        bot.send_message(message.chat.id,
                         "Please select your life path number.\n"
                         "You can find it by adding up all the digits from your birth date until you get a single digit number.\n"
                         )
        bot.register_next_step_hander(message, self.get_numerology, bot)

    def get_numerology(self, message, bot):
        """Fetches and sends the numerology results."""
        numerology_number = int(message.text)
        instance = RapidAPIHoroscope(numerology_number=numerology_number)
        numerology = instance.get_numerology()
        bot.send_message(message.chat.id, f"Your life path reading:\n\n{numerology}")