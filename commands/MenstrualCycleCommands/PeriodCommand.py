from utils.Database import Database

class PeriodCommand:
    """Parent class for the other period related commands."""
    def __init__(self, db: Database):
        self.db = db # keep an instance of the database

    def execute(self, bot, db, message):
        raise NotImplementedError("This command is not yet implemented.")

