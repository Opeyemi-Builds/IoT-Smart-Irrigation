import requests

API_KEY = "9844356ce8cd199867dbb6e23e200a16"


def get_rain_probability(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    rain_probability = data["list"][0].get("pop", 0) * 100
    return rain_probability
