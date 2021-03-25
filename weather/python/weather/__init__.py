import requests
from lily_ext import action, answer, conf, translate

def to_celsius(fahrenheit):
    return fahrenheit - 273.15

@action(name="weather")
class Weather:

    def __init__(self):
        self.api_key = conf("api_key")

    def trigger_action(self, context):
        curr_lang = "es"
        
        result = requests.get("https://api.openweathermap.org/data/2.5/weather", params={"q": context["city_name"], "appid": self.api_key, "lang": curr_lang}).json()
        context["weather_desc"] = result['weather'][0]['description']
        context["min_temp"] = round(to_celsius(result['main']['temp_min']))
        context["max_temp"] = round(to_celsius(result['main']['temp_max']))
    
        return answer(translate("weather_now_success", context), context)

        