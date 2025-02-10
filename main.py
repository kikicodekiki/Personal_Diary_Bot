import telebot
from telebot import types
from RapidAPIHoroscope import RapidAPIHoroscope
from Database import Database

class TelegramBot:
    """Wrapper class for the Telegram Bot itself."""
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.db = Database()
        self.register_handlers()

    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            """Implement the start command."""
            self.db.add_user(message.from_user.username)
            # generates the custom keyboard
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton(text='Get Horoscope'))
            markup.add(types.KeyboardButton(text='Mood Tracker'))
            markup.add(types.KeyboardButton(text='Period Tracker'))
            self.bot.send_message(message.chat.id,
                                  f"Hello {message.from_user.username}!",
                                  reply_markup=markup)

        @self.bot.message_handler(func = lambda message: True)
        def handle_commands(message):
            """Register all possible commands."""
            if message.text == 'Get Horoscope':
                self.ask_zodiac(message)
            if message.text == 'Mood Tracker':
                self.log_mood(message)
            if message.text == 'Period Tracker':
                self.log_period(message)

    def ask_zodiac(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # display each zodiac sign so that the user can choose theirs
        for sign in RapidAPIHoroscope.signs:
            markup.add(types.KeyboardButton(text = sign))
        self.bot.send_message(message.chat.id, "Please, select your zodiac sign: ", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.choose_horoscope_command)

    def choose_horoscope_command(self, message):
        """Showcases the different functionalities, related to astrology, that the bot supports."""
        zodiac_sign = message.text.lower()
        user = message.from_user.username
        self.db.update_user(user, "zodiac_sign", zodiac_sign)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton(text='Get Horoscope for Today'))
        markup.add(types.KeyboardButton(text='Check Compatability'))
        markup.add(types.KeyboardButton(text='Numerology Reading'))
        self.bot.send_message(message.chat.id, "Please, choose a command: ", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.handle_horoscope_command, zodiac_sign)

    def handle_horoscope_command(self, message, zodiac_sign):
        """Handles each command that the user may have picked."""
        if message.text == 'Get Horoscope for Today':
            """Give out the person's horoscope."""
            instance = RapidAPIHoroscope(sign=zodiac_sign)
            horoscope = instance.get_horoscope()
            self.bot.send_message(message.chat.id, f"Your horoscope for today:\n\n {horoscope}\n")
        elif message.text == 'Check Compatability':
            """Ask for the other person's zodiac sign.'"""
            self.ask_compatability_sign(message, zodiac_sign)
        elif message.text == 'Numerology Reading':
            self.ask_numerology_number(message)

    def ask_compatability_sign(self, message, zodiac_sign):
        """Fetch the other person's sign."""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for sign in RapidAPIHoroscope.signs:
            markup.add(types.KeyboardButton(text = sign))
        self.bot.send_message(message.chat.id, "Please, select your zodiac sign: ", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.fetch_compatability_sign, zodiac_sign)

    def fetch_compatability_sign(self, message, zodiac_sign):
        """Get the needed information through the instance."""
        second_sign = message.text.lower()
        instance = RapidAPIHoroscope(sign=zodiac_sign)
        compatability = instance.get_compatability(second_sign)
        self.bot.send_message(message.chat.id, f"Your compatability for {second_sign}:\n{compatability}")

    def ask_numerology_number(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(1, 10):
            markup.add(types.KeyboardButton(text = str(i)))
        self.bot.send_message(message.chat.id, """Please select your life path number: \n 
                                                You can find it by adding up all of the digits from your birth date.""")
        self.bot.register_next_step_handler(message, self.fetch_numerology)

    def fetch_numerology(self, message):
        """Gets the life path number and displays the info about it."""
        numerology_number = int(message.text)
        instance = RapidAPIHoroscope(numerology_number=numerology_number)
        numerology = instance.get_numerology()
        self.bot.send_message(message.chat.id, f"Your life path reading:\n\n {numerology}")

    def log_mood(self, message):
        pass

    def log_period(self, message):
        pass

    def run(self):
        self.bot.polling(none_stop=True)

if __name__ == '__main__':
    bot = TelegramBot(token="<KEY>")
    bot.run()
