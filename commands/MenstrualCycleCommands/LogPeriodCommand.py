from commands.MenstrualCycleCommands.PeriodCommand import PeriodCommand
from datetime import datetime


class LogPeriodCommand(PeriodCommand):
    """Command that handles the proper record of the user's menstrual cycle."""
    def execute(self, update, context):
        """Makes a connection with the database and logs in a new period entry."""
        user_id = update.message.chat_id
        if not context.args:
            update.message.reply_text("Please provide the start date (YYYY-MM-DD).")
            return
        try:
            start_date = datetime.strptime(context.args[0], "%Y-%m-%d").date()
            self.db.log_period(user_id, start_date)
            update.message.reply_text("Period logged in successfully.")
        except ValueError:
            update.message.reply_text("Please provide the start date (YYYY-MM-DD).")
