import http.client

conn = http.client.HTTPSConnection("horoscope-astrology.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "<KEY>",
    'x-rapidapi-host': "horoscope-astrology.p.rapidapi.com"
}

conn.request("GET", "/horoscope?day=today&sunsign=virgo", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))