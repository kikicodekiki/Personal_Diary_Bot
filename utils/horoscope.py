"""Wrapper class for a free API (aztro) that I found, which gives access to
        daily horoscopes, mood, compatabiliyu, ect."""
import requests
from parseDataForHoroscopes import *

class Horoscope:
    horoscope_url = 'https://aztro.sameerkumar.website'
    signs = [
        'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra',
        'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'
    ]
    days = ['yesterday', 'today', 'tomorrow']

    def __tryToGetData(self, parameters):
        try:
            r = requests.post(Horoscope.horoscope_url, params=parameters)  # API requires POST
            r.raise_for_status()  # Raise error for bad response
            return r.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching horoscope: {e}")  # Log the error
            return None

    def __init__(self, sign, day='today', timezone='None'):
        self.sign = str(sign).lower()
        self.day = str(day).lower()
        if self.sign not in self.signs:
            raise ValueError(f"Invalid sign: {self.sign}")
        if self.day not in self.days:
            raise ValueError(f"Invalid day: {self.day}")

        parameters = {'sign': self.sign, 'day': self.day, 'timezone': timezone}
        data = self.__tryToGetData(parameters)

        if not data:
            raise ValueError(f"Could not fetch horoscope data for sign '{self.sign}' and day '{self.day}'")

        self.description = data['description']
        self.compatability = data['compatibility']  # Fixed typo: 'compatability' -> 'compatibility'
        self.date_range = parse_date_range(data['date_range'])
        self.mood = data['mood']
        self.color = data['color']
        self.curr_date = parse_date(data['current_date'])
        self.lucky_time = parse_time(data['lucky_time'])

data = Horoscope('virgo', day='tomorrow')
print(data.description)
