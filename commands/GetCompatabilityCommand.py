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
        bot.send_message(message.chat.id, "Please select the other person's zodiac sign:", reply_markup=markup)
        bot.register_next_step_handler(message, self.get_compatibility, bot, zodiac_sign)

    def get_compatibility(self, message, bot, zodiac_sign):
        """Retrieves and sends the compatability data."""
        second_sign = message.text.lower()
        instance = RapidAPIHoroscope(sign=zodiac_sign)
        compatability = instance.get_compatability(second_sign)
        bot.send_message(message.chat.id, compatability)