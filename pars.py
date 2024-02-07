import requests
from bs4 import BeautifulSoup
import json

# url_1 = 'https://dentalia.com/'
# url_2 = 'https://omsk.yapdomik.ru/'
# url_3 = 'https://www.santaelena.com.co/'


def get_location(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Парсинг названия локации
    loc_name = soup.find('h1')
    if loc_name is not None:
        loc_name = loc_name.text.strip()
    else:
        loc_name = 'Название не найдено'

    # Парсинг координат
    coordinator = soup.find('div', class_='coordinator')
    if coordinator is not None:
        coordinator = coordinator.text.strip()
    else:
        coordinator = 'Локация не найдена'

    # Парсинг телефонов
    phones = []
    phone_elements = soup.find_all('div', class_='phone')
    for phone_element in phone_elements:
        phones.append(phone_element.text.strip())

    # Парсинг времени работы
    working_hours = {}
    days = soup.find_all('div', class_='day')
    for day in days:
        day_name = day.find('span', class_='name').text.strip()
        day_hours = day.find('span', class_='hours').text.strip()
        working_hours[day_name] = day_hours

    # Объект с информацией о локации
    location_info = {
        'Название локации': loc_name,
        'Координаты': coordinator,
        'Телефоны': phones,
        'Время работы': working_hours
    }

    return location_info


def scrape_locations():
    websites = [
        'https://dentalia.com/',
        'https://omsk.yapdomik.ru/',
        'https://www.santaelena.com.co/'
    ]

    all_locations = []

    for website in websites:
        location_info = get_location(website)
        all_locations.append(location_info)

    # Сохранение информации в JSON-файл
    with open('locations.json', 'w') as file:
        json.dump(all_locations, file, indent=4)

    print('Информация о локациях успешно собрана и сохранена в файле locations.json')


scrape_locations()
