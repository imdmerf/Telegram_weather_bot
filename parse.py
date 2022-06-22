import requests
key = "" # enter your apikey from openweathermap
url = "https://api.openweathermap.org/data/2.5/"

def weater_now(q: str="", appid: str = key, units: str = "metric", lang: str="ru") -> dict:
    weater_data = requests.get(url + "weather", params=locals()).json()
    city_name = weater_data['name']
    main = weater_data['main']
    temp = round(main['temp'])
    weather = weater_data['weather']
    for i in range(len(weather)):
        description = weather[i]['description']
        print(description)

    return city_name, temp, description