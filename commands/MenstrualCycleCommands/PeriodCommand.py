from commands.base import Command
from utils.Database import Database
from telegram import Update
from telegram.ext import CallbackContext

# if I had learned this a bot earlier I could have saved up on some nerves, haha
# Update -> everything about the incoming message from the user
# CallbackContext -> contains extra metadata and helps manage the bot's state

class PeriodCommand(Command):
    """Parent class for the other period related commands."""
    def __init__(self, db: Database):
        self.db = db # keeping the Database instance to make operation easier

    def execute(self, update: Update, context: CallbackContext):
        """This method is designed to be used as a Telegram command handler."""
        """Update -> provides the user's message data like chat id.
            CallBackContext -> provides command arguments, bot data and memory.
            context.args[]0 -> to get the first element."""
        raise NotImplementedError("This command is not yet implemented.")

