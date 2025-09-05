import requests
import json


def get_weather(city_name):
    api_key = 'b944bd10e88a979cf193682d789b7606'
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric",
        "lang": "en"
    }
    response = requests.get(url, params=params)
    data = json.loads(response.text)
    return data['weather'][0]['main'], data['main']['temp'], data['main']['pressure'], data['main']['humidity']


# city = input('Напишите название города: ')
city = 'Rome'
w, t, p, h = get_weather(city)
print('Город: ', city)
print(
    f'Погода: {w}\nТемпература воздуха {t} гр. Ц.\nДавление: {p} ГПа\nВлажность: {h}%')
