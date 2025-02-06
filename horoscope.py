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
    days = ['yesterday', 'today', 'tomorrow']  # the only valid days for using the API

    def __tryToGetData(self, parameters):
        try:
            r = requests.get(Horoscope.horoscope_url, params=parameters)
            if r.status_code == 200:
                data = r.json()
                return data
            else:
                """raise exception for not managing to get the results from the api"""
                pass
        except Exception as e:
            pass

    def __init__(self, sign, day = 'today', timezone = 'None'):
        self.sign = str(sign).lower()
        self.day = str(day).lower()
        if sign not in self.signs:
            """raise invalid sign error"""
            pass
        if day not in self.days:
            """raise invalid day error"""
            pass
        parameters = (('sign', self.sign), ('day', self.day), ('timezone', timezone))
        data = self.__tryToGetData(parameters)
        self.description = data['description']
        self.compatability = data['compatability']
        self.date_range = parse_date_range(data['date_range'])
        self.mood = data['mood']
        self.color = data['color']
        self.curr_date = parse_date(data['current_date'])
        self.lucky_time = parse_time(data['lucky_time'])

