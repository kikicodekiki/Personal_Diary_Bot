from telebot import types
from commands.base import Command
from datetime import datetime


class LogPeriodCommand(Command):
    """Command that handles the proper record of the user's menstrual cycle."""
    def execute(self, bot, db, start_date):
        """Makes a connection with the database."""
