import requests
import json


def get_data(country, month=None):
    api_key = '7cb48bea-52bb-4275-82ed-83d6334a7fcb'
    url = 'https://holidayapi.com/v1/holidays'
    params = {
        'key': api_key,
        'country': country,
        'year': 2024,
        'language': 'en'
    }
    if month is not None:
        params['month'] = month
    response = requests.get(url, params=params)
    return json.loads(response.text)


months = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}


print('Данная программа показывает праздники в разных странах за 2024 год')
# country_code = 'NL'
country_code = input('Введите код (##) страны: ')
print('Желаете вывести праздники за отдельный месяц или за весь год?')
for_month = int(input('1 - за месяц, 2 - за год: '))
data = None
if for_month == 1:
    month = input('Введите название месяца (латиницей): ')
    if month not in months:
        print('Направильный месяц!')
        quit()
    data = get_data(country_code, months[month])
elif for_month == 2:
    data = get_data(country_code)
else:
    print('Неправильный ввод')
    quit()
if 'error' in data:
    print(data['error'])
    quit()
print(f'{'Дата':<15} Праздник')
for holiday in data.get('holidays', []):
    print(f'{holiday['date']:<15} {holiday['name']}')
