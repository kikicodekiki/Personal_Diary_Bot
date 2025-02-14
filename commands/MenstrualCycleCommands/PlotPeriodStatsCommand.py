import numpy as np
import matplotlib.pyplot as plt # thank God for numerical methods ;)
from commands.MenstrualCycleCommands.PeriodCommand import PeriodCommand
from telebot import types
import os

class PlotPeriodStatsCommand(PeriodCommand):
    """Command that aims at plotting the data, retrieved from the database."""
    def execute(self, bot, db, message):
        user_id = message.chat.id
        cycle_lengths = db.get_period_history_for_user(user_id)
        if not cycle_lengths or len(cycle_lengths) < 2:
            bot.send_message(user_id, 'Not enough data found for this user.')
            return self.return_to_main_menu(bot, message)
        self.plot_period_stats(bot, user_id, cycle_lengths, message)

    def plot_period_stats(self, bot, user_id, cycle_lengths, message):
        """Plots that represent the user's period lengths."""
        # x_axis = list(range(1, len(cycle_lengths) + 1))
        avg_cycle = np.mean(cycle_lengths)
        standard_dev = np.std(cycle_lengths)
        plt.plot(cycle_lengths, marker='o', linestyle='-', color='r', label="Cycle Lengths")
        plt.axhline(y=avg_cycle, color='b', linestyle='--', label=f"Avg Cycle ({avg_cycle:.2f} days)")
        plt.fill_between(range(len(cycle_lengths)), avg_cycle - standard_dev, avg_cycle + standard_dev, color='b', alpha=0.2,
                         label="Std Dev")
        plt.xlabel("Cycle Count")
        plt.ylabel("Cycle Length (days)")
        plt.title("Menstrual Cycle Length Over Time")
        plt.legend()
        plt.grid(True)
        # save the image
        image_path = os.path.join(os.getcwd(), "period_stats.png")
        plt.savefig(image_path)
        plt.close() # prevent memory leaks
        # send image to user
        with open(image_path, "rb") as image_file:
            bot.send_photo(user_id, photo=image_file, caption="Here is your period chart")
        self.return_to_main_menu(bot, message)

    def return_to_main_menu(self, bot, message):
        """Returns the user to the Menstrual Cycle Stats menu instead of the main menu."""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        markup.add(types.KeyboardButton(text="Log Period"))
        markup.add(types.KeyboardButton(text="Go Back"))
        bot.send_message(message.chat.id, "What would you like to do next?", reply_markup=markup)




