import unittest
from utils.RapidAPIHoroscope import RapidAPIHoroscope
from unittest.mock import patch, MagicMock

class TestRapidAPI(unittest.TestCase):
    # List of valid signs
    signs = [
        'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra',
        'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'
    ]
    # List of non - valid signs
    non_signs = [
        'ophiuchus', 'snake', 'monkey'
    ]
    # List of valid life path number
    life_paths = [
        i for i in range(1, 10)
    ]
    # List of non - valid life path numbers
    non_life_paths = [
        19, 69, 14
    ]

    def setUp(self):
        """Setup a valid instance of the class before each test."""
        try:
            self.check = RapidAPIHoroscope(sign='virgo', numerology_number=2)
        except Exception as e:
            print("setUp method failed: ", e)

    def test_data_type(self):
        """Make sure that the data types are correct."""
        self.assertTrue(type(self.check.sign) is str)
        self.assertTrue(type(self.check.numerology_number) is int)

    def test_invalid_sign(self):
        """Make sure that a ValueError is raised for a sign that is not valid."""
        for sign in self.non_signs:
            with self.assertRaises(ValueError):
                RapidAPIHoroscope(sign=sign)

    def test_invalid_numerology_number(self):
        """Make sure that a ValueError is raised for a numerology number that is not valid."""
        for num in self.non_life_paths:
            with self.assertRaises(ValueError):
                RapidAPIHoroscope(numerology_number=num)

    # mock to prevent actual API calls during testing
    @patch("http.client.HTTPSConnection")
    def test_get_horoscope(self, mock_https):
        """simulating what the API would return"""
        mock_response = MagicMock()
        # mimic a JSON object => the test is passed if the result is BRAVO BE PHILIPS
        mock_response.read.return_value = b'{"horoscope": "BRAVO BE PHILIPS!"}'
        mock_https.return_value.getresponse.return_value = mock_response
        result = self.check.get_horoscope()
        self.assertEqual(result, "Horoscope data not available.")

    @patch("http.client.HTTPSConnection")
    def test_get_lucky_number(self, mock_https):
        """Mock API call to test the get_lucky_number method."""
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"lucky_number": 3}' # 3 like the grade I am getting!
        mock_https.return_value.getresponse.return_value = mock_response
        result = self.check.get_lucky_number()
        self.assertEqual(result, 3)

    @patch("http.client.HTTPSConnection")
    def test_get_compatability(self, mock_https):
        """Mock API call to test get_compatibility method."""
        mock_response = MagicMock()
        # valentine's day vibes
        mock_response.read.return_value = b'[{"header": "Awful Match!", "text": "DUMP HIM!"}]'
        mock_https.return_value.getresponse.return_value = mock_response
        result = self.check.get_compatability("leo")
        self.assertEqual(result, "Couldn't retrieve compatability data from Rapid API. But you should DUMP HIM!")

    @patch("http.client.HTTPSConnection")
    def test_get_numerology(self, mock_https):
        """Mock API call to test get_numerology method."""
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"desc": "Your life path is full of wisdom."}'
        mock_https.return_value.getresponse.return_value = mock_response
        result = self.check.get_numerology()
        self.assertEqual(result, "Your life path is full of wisdom.")

    if __name__ == "__main__":
        unittest.main()