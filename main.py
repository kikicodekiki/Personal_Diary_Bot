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
        pass

    def log_mood(self, message):
        pass

    def log_period(self, message):
        pass

