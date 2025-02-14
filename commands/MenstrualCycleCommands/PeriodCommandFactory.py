from telebot import types
from commands.MenstrualCycleCommands.LogPeriodCommand import LogPeriodCommand
from commands.MenstrualCycleCommands.PlotPeriodStatsCommand import PlotPeriodStatsCommand
from commands.MenstrualCycleCommands.PredictNextPeriodCommand import PredictNextPeriodCommand

class PeriodCommandFactory:
    """Delegates to the other period commands."""

    def execute(self, bot, db, message):
        """Asks the user what they want to do."""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        commands = {
            "Log Period": LogPeriodCommand(db),
            "Plot Period": PlotPeriodStatsCommand(db),
            "Get Next Period Prediction": PredictNextPeriodCommand(db),
        }
        for command in commands.keys():
            markup.add(types.KeyboardButton(text=command))
        markup.add(types.KeyboardButton("Go Back"))  # add a Go Back button
        bot.send_message(message.chat.id, "Please select what you'd like to do:", reply_markup=markup)
        bot.register_next_step_handler(message, lambda msg: self.delegate_command(msg, bot, db))

    def delegate_command(self, message, bot, db):
        """Delegates the request to the appropriate period command."""
        if message.text == "Go Back":
            return self.execute(bot, db, message)  # show options again
        commands = {
            "Log Period": LogPeriodCommand(db),
            "Plot Period": PlotPeriodStatsCommand(db), # had forgotten to add this -> hopefully, now it will work
            "Get Next Period Prediction": PredictNextPeriodCommand(db),
        }
        command = commands.get(message.text)
        if command:
            command.execute(bot, db, message)
        else:
            bot.send_message(message.chat.id, "Invalid option. Please select a valid command.")
            self.execute(bot, db, message)