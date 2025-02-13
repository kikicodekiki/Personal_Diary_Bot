import http.client
import json

conn = http.client.HTTPSConnection("horoscope-astrology.p.rapidapi.com")
headers = {
    'x-rapidapi-key':"KEY",
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

    def __get_daily_horoscope_data(self):
        """Returns a dict containing the current date, time, horoscope and a lucky number."""
        if self.sign is None:
            raise ValueError(f"Invalid sign: {self.sign}")
        try:
            conn.request("GET", f"/horoscope?day=today&sunsign={self.sign}", headers=headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")
            return json.loads(data)
        except Exception as e:
            print(e)
            return None

    def get_horoscope(self) :
        """Returns only the horoscope string."""
        data = self.__get_daily_horoscope_data()
        if data is None:
            return "Couldn't retrieve horoscope data from Rapid API. But you will have a great day!"
        return data.get("horoscope", "Horoscope data not available.")

    def get_lucky_number(self):
        """Returns the lucky number as a string from the response."""
        data = self.__get_daily_horoscope_data()
        if data is None:
            return "Couldn't retrieve horoscope data from Rapid API. But you will have a great day!"
        return str(data.get("lucky_number", "Lucky number not available."))

    def __get_compatibility_data(self, second_sign):
        if second_sign is not None and second_sign not in self.signs:
            raise ValueError(f"Invalid sign: {second_sign}")
        try:
            conn.request("GET", f"/affinity?sign1={self.sign}&sign2={second_sign}", headers=headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")
            # parse the JSON response
            parsed_data = json.loads(data)
            # format the data, because response is a list of dictionaries
            formatted_text = "\n\n".join([entry["header"] + "\n" + entry["text"] for entry in parsed_data])
            return formatted_text
        except Exception as e:
            print(e)
            return None

    def get_compatibility(self, second_sign):
        """Returns the edited text that includes the degrees of the two signs and their alignment."""
        data = self.__get_compatibility_data(second_sign)
        if data is None:
            return "Couldn't retrieve compatibility data from Rapid API. But you should DUMP HIM!"
        return data

    def __get_numerology_data(self):
        """Returns the description based on the numerology life path number."""
        if self.numerology_number is None:
            raise ValueError(f"Invalid sign: {self.sign}")
        try:
            conn.request("GET", f"/numerology?n={self.numerology_number}", headers=headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")
            return json.loads(data)
        except Exception as e:
            print(e)
            return None

    def get_numerology(self):
        """Returns the numerology description from the response."""
        data = self.__get_numerology_data()
        if not data or "desc" not in data:
            return "Numerology data not available."
        return data["desc"]

