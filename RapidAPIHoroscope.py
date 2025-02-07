import http.client
import json

conn = http.client.HTTPSConnection("horoscope-astrology.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "KEY",
    'x-rapidapi-host': "horoscope-astrology.p.rapidapi.com"
}

class RapidAPIHoroscope:
    """Wrapper class for the Rapid Horoscope API."""
    signs = [
        'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra',
        'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'
    ]
    numerology_life_paths = [i for i in range(1, 10)] # life paths are 1 through 9

    def __init__ (self, numerology_number=None, sign=None):
        """Initialize the data given by the user and then implement the data as wished."""
        self.sign = str(sign).lower() if sign is not None else None
        if self.sign is not None and self.sign not in self.signs:
            raise ValueError(f"Invalid sign: {self.sign}")
        self.numerology_number = int(numerology_number) if numerology_number is not None else None
        if self.numerology_number is not None and self.numerology_number not in self.numerology_life_paths:
            raise ValueError(f"Invalid life path: {self.numerology_number}")

    def get_daily_horoscope_data(self):
        """Returns a dict containing the current date, time, horoscope and a lucky number."""
        try:
            conn.request("GET", f"/horoscope?day=today&sunsign={self.sign}", headers=headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")
            return json.loads(data)
        except Exception as e:
            print(e)
            return None

    def get_horoscope_str(self) :
        """Returns only the horoscope string."""
        data = self.get_daily_horoscope_data()
        if data is None:
            return "Couldn't retrieve horoscope data from Rapid API. But you will have a great day!"
        return data.get("horoscope", "Horoscope data not available.")

    def get_lucky_number(self):
        """Returns the lucky number from the response."""
        data = self.get_daily_horoscope_data()
        if data is None:
            return "Couldn't retrieve horoscope data from Rapid API. But you will have a great day!"
        return data.get("lucky_number", "Lucky number not available.")

    def get_compatability_data(self, second_sign):
        if second_sign is not None and second_sign not in self.signs:
            raise ValueError(f"Invalid sign: {second_sign}")



horoscope = RapidAPIHoroscope(sign = 'virgo')
print(horoscope.get_horoscope_str())