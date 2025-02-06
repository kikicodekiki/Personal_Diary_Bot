import telebot
from telebot import types

bot = telebot.TeleBot(token='<KEY>')

"""Integrate the 'start' function which gets the bot running."""
@bot.message_handler(commands=['start'])
def start(message):
    """Create the buttons that will link up to the different functionalities of the bot."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    HoroscopeButton = types.KeyboardButton(text="Get Horocope")
    markup.add(HoroscopeButton)
    MoodTrackerButton = types.KeyboardButton(text="Mood Tracker")
    PeriodTrackerButton = types.KeyboardButton(text="Period Tracker")
    markup.add(MoodTrackerButton, PeriodTrackerButton)

    """Send the initial message."""
    to_send = """, and welcome to my Python project for the Introduction to programming with Python course. 
    \nThis bot is designed to represent a personal diary for women. 
    \nIt provides real-time insights into the Astrological realm, analyzing data from planetary positions,
     as well as tracking your period and your mood.

        <b>Features:</b> """
    bot.send_message(message.chat.id, f"<b>Hello, dear {message.from_user.first_name}</b>" + to_send,
                     parse_mode='html', reply_markup=markup)

    """Register the next steps after clicking on a given button."""
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == "Get Horocope":
        # give different options depending on the zodiac sign
        pass
    elif message.text == "Get MoodTracker":
        # give different options: log in mood, check progress
        pass
    elif message.text == "Get PeriodTracker":
        # give different options: log in period, check progress
        pass





"""Make the bot run constantly."""
bot.polling(none_stop=True)