"""Defines the interface for the Command Design Pattern."""
from abc import ABC, abstractmethod # import needed modules for the creation of an abstract class
from telebot import types

class Command(ABC):
    """Abstract base class for all bot commands."""
    @abstractmethod
    def execute(self, bot, db, message):
        raise NotImplementedError('You must implement this method.')

    def return_to_main_menu(self, bot, message):
        """Returns to the main menu."""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        markup.add(types.KeyboardButton(text="Get Astrology Reading"))
        markup.add(types.KeyboardButton(text="Menstrual Cycle Stats"))  # include the menstrual cycle funcs
        markup.add(types.KeyboardButton(text="Get Mood Prediction for Today"))
        bot.send_message(message.chat.id, "Would you like to do something else?", reply_markup=markup)
