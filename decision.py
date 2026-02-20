from weather import get_rain_probability

def irrigation_decision(soil_moisture):
    rain_probability = get_rain_probability()

    if soil_moisture < 40 and rain_probability < 50:
        return "WATER"
    return "WAIT"