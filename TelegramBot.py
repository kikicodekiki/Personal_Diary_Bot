import telebot
from telebot import types
from Database import Database
from commands.AstrologyCommand import AstrologyCommand


class TelegramBot:
    """""Wrapper class for the Telegram Bot interactions and delegates tasks to commands."""
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.db = Database()
        # Command registry
        self.commands = {
            # got this idea from my dear friend, the chat bot, still have yet to implement other commands
            "Get Astrology Reading": AstrologyCommand(), # store instances of the command
        }
        self.register_handlers()

    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            """Implements the start command."""
            self.db.add_user(message.from_user.first_name) # add the user to the database
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for command in self.commands.keys():
                markup.add(types.KeyboardButton(text=command))
            (self.bot.send_message(message.chat.id, f"Hello {message.from_user.first_name}!", reply_markup=markup))

        @self.bot.message_handler(func=lambda message: message.text in self.commands)
        def handle_commands(message):
            """Delegates to the appropriate command."""
            command = self.commands.get(message.text)
            if command:
                command.execute(self.bot, self.db, message)

    def run(self):
        self.bot.polling(none_stop=True)


instance = TelegramBot("MY_KEY")
instance.run()

