import requests
from bs4 import BeautifulSoup
import json


def _parse_element(element) -> str | None:
    if element is not None and hasattr(element, "text"):
        return element.text.strip()

    return None


def get_location(url: str) -> dict[str, str]:
    page = requests.get(url)
    page.raise_for_status()
    soup = BeautifulSoup(page.content, 'html.parser')

    # Парсинг названия локации
    loc_name = _parse_element(element=soup.find('h1'))

    # Парсинг адреса
    address = _parse_element(element=soup.find('div', class_='address'))

    # Парсинг координат
    latitude = _parse_element(element=soup.find('div', class_='latitude'))
    longitude = _parse_element(element=soup.find('div', class_='longitude'))

    # Парсинг телефонов
    phones = [
        _parse_element(phone)
        for phone in soup.find_all('div', class_='phones')
    ]

    # Парсинг времени работы
    working_hours = {}
    days = soup.find_all('div', class_='day')
    for day in days:
        day_name = _parse_element(element=day.find('span', class_='name'))
        day_hours = _parse_element(element=day.find('span', class_='hours'))
        working_hours[day_name] = day_hours

    # Объект с информацией о локации
    location_info = {
        'name': loc_name,
        'address': address,
        'latlon': [latitude, longitude],
        'phones': phones,
        'working_hours': working_hours
    }

    return location_info


def scrape_locations():
    websites = [
        'https://dentalia.com/',
        'https://omsk.yapdomik.ru/',
        'https://www.santaelena.com.co/'
    ]
    all_locations = [
        get_location(website) for website in websites
    ]

    # Сохранение информации в JSON-файл
    with open('locations.json', 'w', encoding="UTF-8") as file:
        json.dump(all_locations, file, indent=4)

    print('Информация о локациях успешно собрана и сохранена в файле locations.json')


scrape_locations()