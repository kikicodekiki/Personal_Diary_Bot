from telebot import types
from commands.base import Command
from RapidAPIHoroscope import RapidAPIHoroscope

class HoroscopeCommand(Command):
    """Handles the retrieval of the daily horoscope."""
    def execute(self, bot, db, message):
        """Asks for the person's zodiac sign."""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # display each zodiac sign so that the user can choose theirs
        for sign in RapidAPIHoroscope.signs:
            markup.add(types.KeyboardButton(text=sign))
        bot.send_message(message.chat.id, "Please, select your zodiac sign: ", reply_markup=markup)
        bot.register_next_step_handler(message, self.retrieve_horoscope_command, bot, db)

    def retrieve_horoscope_command(self, message, bot, db):
        """Get the horoscope for the given zodiac sign."""
        zodiac_sign = message.text.lower()
        user = message.from_user.username
        db.update_user(user, "zodiac_sign", zodiac_sign) # updates the database => was not sure how to implement this
        instance = RapidAPIHoroscope(sign=zodiac_sign)
        horoscope = instance.get_horoscope()
        bot.send_message(message.chat.id, f"Your horoscope for today:\n\n {horoscope}")
