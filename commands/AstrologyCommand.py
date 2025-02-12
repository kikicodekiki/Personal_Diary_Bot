from telebot import types
from commands.base import Command
from RapidAPIHoroscope import RapidAPIHoroscope
from commands.GetNumerologyCommand import GetNumerologyCommand
from commands.GetDailyHoroscopeCommand import GetDailyHoroscopeCommand
from commands.GetCompatabilityCommand import GetCompatabilityCommand

class AstrologyCommand(Command):
    """Handles the retrieval of the zodiac sign and delegates to the other command classes."""
    def execute(self, bot, db, message):
        """Asks for the person's zodiac sign."""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # display each zodiac sign so that the user can choose theirs
        for sign in RapidAPIHoroscope.signs:
            markup.add(types.KeyboardButton(text=sign))
        bot.send_message(message.chat.id, "Please, select your zodiac sign: ", reply_markup=markup)
        bot.register_next_step_handler(message, self.save_zodiac, bot, db)

    def save_zodiac(self, message, bot, db):
        """Saves the zodiac sign and prompts the user to choose an astrology feature."""
        zodiac_sign = message.text.lower()
        user = message.from_user.first_name
        db.update_user(user, "zodiac_sign", zodiac_sign) # updates the database
        # display the next functionalities
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton(text="Get Horoscope for Today"))
        markup.add(types.KeyboardButton(text="Check Compatability"),
                   types.KeyboardButton(text="Numerology Reading"))
        bot.send_message(message.chat.id, "Please, choose a command:", reply_markup=markup)
        bot.register_next_step_handler(message, self.delegate_command, bot, db, zodiac_sign)

    def delegate_command(self, message, bot, db, zodiac_sign):
        """Delegates the request to the appropriate command."""
        commands = {
            "Get Horoscope for Today": GetDailyHoroscopeCommand(),
            "Check Compatibility": GetCompatabilityCommand(),
            "Numerology Reading": GetNumerologyCommand(),
        }
        command = commands.get(message.text)
        if command:
            command.execute(bot, db, message, zodiac_sign)