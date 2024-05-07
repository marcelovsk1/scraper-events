import json
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from fuzzywuzzy import fuzz
from selenium.webdriver.chrome.options import Options
import geopy
from geopy.geocoders import Nominatim
from unidecode import unidecode
import datetime
import openai
import re



def generate_tags(title, description):
    predefined_tags = [
        {"id": "005a4420-88c3-11ee-ab49-69be32c19a11", "name": "Startup", "emoji": "🚀", "tagCategory": "Education"},
        {"id": "00fb7c50-3c47-11ee-bb59-7f5156da6f07", "name": "Reggae", "emoji": " 💚", "tagCategory": "Musique"},
        {"id": "00fe8220-3d0e-11ee-a0b5-a3a6fbdfc7e4", "name": "Squash", "emoji": "🏸", "tagCategory": "Sports"},
        {"id": "0159ac60-3d0c-11ee-a0b5-a3a6fbdfc7e4", "name": "Aquatics", "emoji": "🏊‍♂️", "tagCategory": "Sports"},
        {"id": "01785870-4ce5-11ee-931a-073fc9abbdfa", "name": "Karaoke", "emoji": "🎤", "tagCategory": "Leisure"},
        {"id": "06759f60-5c8d-11ee-8ae0-fb963ffbedc0", "name": "Holiday", "emoji": "🌞", "tagCategory": "Musique"},
        {"id": "0693e050-5c8e-11ee-8ae0-fb963ffbedc0", "name": "Roller Derby", "emoji": "🛼", "tagCategory": "Sports"},
        {"id": "099b2b90-4ce5-11ee-931a-073fc9abbdfa", "name": "Singing", "emoji": "🎤", "tagCategory": "Leisure"},
        {"id": "09dddaa0-573d-11ee-8b78-9b77053f08ef", "name": "Chess", "emoji": "♟", "tagCategory": "Leisure"},
        {"id": "0a3f4540-3c46-11ee-bb59-7f5156da6f07", "name": "Blues", "emoji": " 🎵", "tagCategory": "Musique"},
        {"id": "0ad207f0-3d0d-11ee-a0b5-a3a6fbdfc7e4", "name": "Golf", "emoji": "⛳", "tagCategory": "Sports"},
        {"id": "0b379d00-3d0c-11ee-a0b5-a3a6fbdfc7e4", "name": "Athletic Races", "emoji": "🏅", "tagCategory": "Sports"},
        {"id": "0cafac20-3d0e-11ee-a0b5-a3a6fbdfc7e4", "name": "Surfing", "emoji": "🏄‍♀️", "tagCategory": "Sports"},
        {"id": "0dc9b310-45df-11ee-837b-e184466a9b82", "name": "Book", "emoji": "📖", "tagCategory": "Leisure"},
        {"id": "108f37a0-3d0b-11ee-a0b5-a3a6fbdfc7e4", "name": "Fashion", "emoji": "🥻", "tagCategory": "Leisure"},
        {"id": "11164b60-4381-11ee-b8b1-a1b868b635cd", "name": "Punk", "emoji": "👩‍🎤", "tagCategory": "Musique"},
        {"id": "133a3370-3c47-11ee-bb59-7f5156da6f07", "name": "Religious", "emoji": "✝", "tagCategory": "Musique"},
        {"id": "1453a7c0-3d0d-11ee-a0b5-a3a6fbdfc7e4", "name": "Gymnastics", "emoji": "🤸‍♀️", "tagCategory": "Sports"},
        {"id": "15de0a70-45e3-11ee-837b-e184466a9b82", "name": "Hiking", "emoji": "🏃‍♂️", "tagCategory": "Sports"},
        {"id": "1859e020-6ec5-11ee-839e-4b70ecb92583", "name": "Cycling", "emoji": "🚴‍♂️", "tagCategory": "Sports"},
        {"id": "18f44470-6ec6-11ee-839e-4b70ecb92583", "name": "Fencing", "emoji": "🤺", "tagCategory": "Sports"},
        {"id": "19783bb0-45e3-11ee-837b-e184466a9b82", "name": "Yoga", "emoji": "🧘‍♂️", "tagCategory": "Sports"},
        {"id": "1b7e1210-3d0b-11ee-a0b5-a3a6fbdfc7e4", "name": "Photography", "emoji": "📸", "tagCategory": "Leisure"},
        {"id": "1cbfc5a0-3c46-11ee-bb59-7f5156da6f07", "name": "Jazz", "emoji": " 🎵", "tagCategory": "Musique"},
        {"id": "1d344290-3c46-11ee-bb59-7f5156da6f07", "name": "Pop", "emoji": "🎶", "tagCategory": "Musique"},
        {"id": "1d809850-3c47-11ee-bb59-7f5156da6f07", "name": "R&B", "emoji": " 🎶", "tagCategory": "Musique"},
        {"id": "1de59e30-3c47-11ee-bb59-7f5156da6f07", "name": "Rock", "emoji": "🎸", "tagCategory": "Musique"},
        {"id": "1e2c0d80-3c47-11ee-bb59-7f5156da6f07", "name": "Soul", "emoji": "🎶", "tagCategory": "Musique"},
        {"id": "1ec41b90-3c46-11ee-bb59-7f5156da6f07", "name": "Classical", "emoji": " 🎶", "tagCategory": "Musique"},
        {"id": "1f39ec90-3d0c-11ee-a0b5-a3a6fbdfc7e4", "name": "Baseball", "emoji": "⚾", "tagCategory": "Sports"},
        {"id": "201cbff0-3c47-11ee-bb59-7f5156da6f07", "name": "Country", "emoji": "🤠", "tagCategory": "Musique"},
        {"id": "21882c20-3c46-11ee-bb59-7f5156da6f07", "name": "Folk", "emoji": "🎻", "tagCategory": "Musique"},
        {"id": "2211e6d0-3c46-11ee-bb59-7f5156da6f07", "name": "Hip-Hop", "emoji": "🎤", "tagCategory": "Musique"},
        {"id": "226300e0-3d0b-11ee-a0b5-a3a6fbdfc7e4", "name": "Dance", "emoji": "💃", "tagCategory": "Leisure"},
        {"id": "2307f3e0-3c47-11ee-bb59-7f5156da6f07", "name": "Indie", "emoji": " 🎶", "tagCategory": "Musique"},
        {"id": "2401c100-3c46-11ee-bb59-7f5156da6f07", "name": "Metal", "emoji": "🤘", "tagCategory": "Musique"},
        {"id": "244cfde0-3c47-11ee-bb59-7f5156da6f07", "name": "Punk Rock", "emoji": "👩‍🎤", "tagCategory": "Musique"},
        {"id": "24883e40-3c46-11ee-bb59-7f5156da6f07", "name": "Reggaeton", "emoji": "🎵", "tagCategory": "Musique"},
        {"id": "24d07ab0-3d0d-11ee-a0b5-a3a6fbdfc7e4", "name": "Tennis", "emoji": "🎾", "tagCategory": "Sports"},
        {"id": "253b9e90-3d0d-11ee-a0b5-a3a6fbdfc7e4", "name": "Basketball", "emoji": "🏀", "tagCategory": "Sports"},
        {"id": "2602b960-3c47-11ee-bb59-7f5156da6f07", "name": "Gospel", "emoji": "🎶", "tagCategory": "Musique"},
        {"id": "263997d0-3c46-11ee-bb59-7f5156da6f07", "name": "Jazz", "emoji": " 🎶", "tagCategory": "Musique"},
        {"id": "274d8200-3c46-11ee-bb59-7f5156da6f07", "name": "Rap", "emoji": "🎤", "tagCategory": "Musique"},
        {"id": "27a4a0f0-3c47-11ee-bb59-7f5156da6f07", "name": "Rock and Roll", "emoji": "🎸", "tagCategory": "Musique"},
        {"id": "27fb1d20-3c47-11ee-bb59-7f5156da6f07", "name": "Ska", "emoji": "🎺", "tagCategory": "Musique"},
        {"id": "28ab7800-3c46-11ee-bb59-7f5156da6f07", "name": "Soul", "emoji": "🎶", "tagCategory": "Musique"},
        {"id": "290a1bb0-3c47-11ee-bb59-7f5156da6f07", "name": "Techno", "emoji": "🎧", "tagCategory": "Musique"},
        {"id": "2995c8b0-3c46-11ee-bb59-7f5156da6f07", "name": "World Music", "emoji": "🌍", "tagCategory": "Musique"}
    ]

    prompt = (
        f"You are a meticulous selector, trained on identifying relevant tags for events.\n" +
        f"Your task is to select, only from the list below, at most 5 tags that are very relevant for the event \"{title}\" (description: \"{description}\").\n" +
        f"Here are the exhaustive list of tags to select from:\n" +
        ''.join([f"{index+1}. {tag['name']} ({tag['tagCategory']})\n" for index, tag in enumerate(predefined_tags)]) +
        f"Only output the selected tags from this list, separated by comma.\n" +
        f"Do not output any other tag.\n" +
        f"If there is no relevant tag in the list, output 'NO TAG'."
    )
    print(prompt)

    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        temperature=0,
        messages=[
            {"role": "system", "content": prompt}
        ]
    )

    response = completion.choices[0].message.content

    print('response', response)

    relevant_tags = []

    for predefined_tag in predefined_tags:
        if (predefined_tag["name"] in response):
            relevant_tags.append(predefined_tag)

    print(relevant_tags)

    return relevant_tags

# Exemplo de uso:
title = "Psy Crisis IV: JUNGLE"
description = "With immense joy and excitement, Wizard Tribe in collaboration with AlpaKa MuziK/Productions present..."

tags = generate_tags(title, description)
print("Tags relacionadas encontradas:", tags)

def calculate_similarity(str1, str2):
    return fuzz.token_sort_ratio(str1, str2)

def scroll_to_bottom(driver, max_scroll=2):
    for _ in range(max_scroll):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

def format_date(date_str):
    print("Original date string:", date_str)

    # Verificar se a string da data está vazia
    if not date_str:
        print("Erro: String de data vazia.")
        return None

    # Usar expressões regulares para extrair os componentes da data
    match = re.match(r"(\w+), (\w+ \d{1,2}, \d{4}) AT (\d{1,2}:\d{2}\s*(?:AM|PM)) – (\d{1,2}:\d{2}\s*(?:AM|PM))", date_str)
    if match:
        day_of_week, date, start_time, end_time = match.groups()

        # Extrair o nome abreviado do mês
        start_month = date.split()[0]

        # Converter o nome do mês para seu equivalente numérico
        start_month_num = datetime.datetime.strptime(start_month, '%B').month

        # Extrair o dia do mês e o ano
        start_day, year = re.search(r"(\d{1,2}), (\d{4})", date).groups()

        # Formatando a data de início com dia, mês e ano
        formatted_start_date = f"{start_day}/{start_month_num:02d}/{year}"
        print("Formatted start date:", formatted_start_date)

        return formatted_start_date
    else:
        print("Erro: Formato de data inválido.")
        return None

def get_coordinates(location):
    if location is None:
        # print("Location is None!")
        return None, None

    location = str(location)

    print("Location before unidecode:", location)
    location = unidecode(location)
    print("Location after unidecode:", location)

    geolocator = Nominatim(user_agent="event_scraper")
    retries = 3
    delay = 2

    for _ in range(retries):
        try:
            location = geolocator.geocode(location, addressdetails=True)
            if location:
                latitude = location.latitude
                longitude = location.longitude
                return latitude, longitude
            else:
                return None, None
        except geopy.exc.GeocoderUnavailable as e:
            time.sleep(delay)

    return None, None

def open_google_maps(latitude, longitude):
    google_maps_url = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
    return google_maps_url

def get_location_details(latitude, longitude):
    geolocator = Nominatim(user_agent="event_scraper")
    retries = 3
    delay = 2

    for _ in range(retries):
        try:
            location = geolocator.reverse((latitude, longitude), language='en', addressdetails=True)
            if location:
                address = location.raw['address']
                city = address.get('city', None)
                country_code = address.get('country_code', None)
                return address, city, country_code
            else:
                return None, None, None
        except geopy.exc.GeocoderUnavailable as e:
            time.sleep(delay)

    return None, None, None

#### FACEBOOK ####
def scrape_facebook_events(driver, url, selectors, max_scroll=30):
    global event_id_counter

    driver.get(url)
    driver.implicitly_wait(20)

    all_events = []
    unique_event_titles = set()

    scroll_to_bottom(driver, max_scroll)

    page_content = driver.page_source
    webpage = BeautifulSoup(page_content, 'html.parser')
    events = webpage.find_all(selectors['event']['tag'], class_=selectors['event'].get('class'))

    for event in events:
        event_link = event.find('a', href=True)
        if not event_link:
            continue

        event_url = 'https://www.facebook.com' + event_link['href'] if event_link['href'].startswith('/') else event_link['href']

        driver.get(event_url)
        time.sleep(1)

        event_page_content = driver.page_source
        event_page = BeautifulSoup(event_page_content, 'html.parser')

        event_title_elem = event_page.find('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6')
        if event_title_elem:
            title = event_title_elem.text.strip()
            if any(calculate_similarity(title, existing_title) >= 90 for existing_title in unique_event_titles):
                continue
        else:
            continue

        description = event_page.find('div', class_='xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs').text.strip() if event_page.find('div', class_='xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs') else None

        location_div = event_page.find('div', class_='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f')
        location_span = event_page.find('span', class_='xt0psk2')
        location_text = location_div.text.strip() if location_div else (location_span.text.strip() if location_span else None)

        if location_text:
            latitude, longitude = get_coordinates(location_text)
        else:
            latitude, longitude = None, None

        google_maps_url = open_google_maps(latitude, longitude)

        address_span = event_page.find('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x1f6kntn xvq8zen xo1l8bm xi81zsa x1yc453h')
        address = address_span.text.strip() if address_span else None

        tags = generate_tags(title, description)

        location_details = {
            'Location': {
                'Location': location_text,
                'Address': address,
                'Latitude': latitude,
                'Longitude': longitude,
                'GoogleMaps_URL': google_maps_url,
                'City': None,
                'CountryCode': None
            }
        }

        address, city, country_code = get_location_details(latitude, longitude)

        location_details['Location']['Address'] = address
        location_details['Location']['City'] = city
        location_details['Location']['CountryCode'] = country_code

        if city is None and country_code is None:
            location_details['Location']['City'] = 'Montreal'
            location_details['Location']['CountryCode'] = 'ca'

        date_text = event_page.find('div', class_='x1e56ztr x1xmf6yo').text.strip() if event_page.find('div', class_='x1e56ztr x1xmf6yo') else None

        # StartTime and EndTime with regex
        if date_text:
            match = re.search(r'(\d{1,2}:\d{2}\s?[AP]M)\s?–\s?(\d{1,2}:\d{2}\s?[AP]M)', date_text)
            if match:
                start_time, end_time = match.groups()
            else:
                if "at" in date_text.lower():
                    start_time = re.search(r'(\d{1,2}:\d{2}\s?[AP]M)', date_text).group(1)
                    end_time = None
                else:
                    start_time, end_time = None, None
        else:
            start_time, end_time = None, None

        event_info = {
            'Title': title,
            'Description': description,
            'Date': format_date(date_text),  # Aqui está a chamada corrigida da função format_date
            **location_details,
            'ImageURL': event_page.find('img', class_='xz74otr x1ey2m1c x9f619 xds687c x5yr21d x10l6tqk x17qophe x13vifvy xh8yej3')['src'] if event_page.find('img', class_='xz74otr x1ey2m1c x9f619 xds687c x5yr21d x10l6tqk x17qophe x13vifvy xh8yej3') else None,
            'Organizer': event_page.find('span', class_='xt0psk2').text.strip() if event_page.find('span', class_='xt0psk2') else None,
            'Organizer_IMG': event_page.find('img', class_='xz74otr')['src'] if event_page.find('img', class_='xz74otr') else None,
            'EventUrl': event_url,
            'StartTime': start_time,
            'EndTime': end_time,
            'Tags': tags,
        }

        all_events.append(event_info)
        unique_event_titles.add(title)

        driver.back()

    return all_events if all_events else None

#### EVENTBRITE ####
def extract_start_end_time(date_str):
    if date_str is None:
        return None, None

    # If "-" is not present in the string, it means it is just a start time
    if "-" not in date_str:
        start_time_match = re.search(r'(\d{1,2}:\d{2}\s*(?:AM|PM)?)', date_str)
        if start_time_match:
            start_time = start_time_match.group(1)
            return start_time.strip(), None
        else:
            return None, None

    # For events that start and end on different days
    day_match = re.search(r'(\w+, \w+ \d{1,2}, \d{4} \d{1,2}:\d{2} (?:AM|PM))\s*-\s*(\w+, \w+ \d{1,2}, \d{4} \d{1,2}:\d{2} (?:AM|PM))', date_str)
    if day_match:
        start_time = day_match.group(1)
        end_time = day_match.group(2)
        return start_time.strip(), end_time.strip()

    date_str = re.sub(r'\b(?:lun(?:di)?|mon(?:day)?)\b', 'Monday', date_str, flags=re.IGNORECASE)
    date_str = re.sub(r'\b(?:mar(?:di)?|tue(?:sday)?)\b', 'Tuesday', date_str, flags=re.IGNORECASE)
    date_str = re.sub(r'\b(?:mer(?:credi)?|wed(?:nesday)?)\b', 'Wednesday', date_str, flags=re.IGNORECASE)
    date_str = re.sub(r'\b(?:jeu(?:di)?|thu(?:rsday)?)\b', 'Thursday', date_str, flags=re.IGNORECASE)
    date_str = re.sub(r'\b(?:ven(?:dredi)?|fri(?:day)?)\b', 'Friday', date_str, flags=re.IGNORECASE)
    date_str = re.sub(r'\b(?:sam(?:edi)?|sat(?:urday)?)\b', 'Saturday', date_str, flags=re.IGNORECASE)
    date_str = re.sub(r'\b(?:dim(?:anche)?|sun(?:day)?)\b', 'Sunday', date_str, flags=re.IGNORECASE)

    # Pattern for start and end time in the same day
    same_day_match = re.search(r'(\w+, \w+ \d{1,2}, \d{4} \d{1,2}:\d{2} (?:AM|PM))\s*-\s*(\d{1,2}:\d{2} (?:AM|PM))', date_str)
    if same_day_match:
        start_time = same_day_match.group(1)
        end_time = same_day_match.group(2)
        return start_time.strip(), end_time.strip()

    # AM/PM Format
    am_pm_match = re.search(r'(\d{1,2}:\d{2}\s*(?:AM|PM))\s*-\s*(\d{1,2}:\d{2}\s*(?:AM|PM))', date_str)
    if am_pm_match:
        start_time, end_time = am_pm_match.groups()
        return start_time.strip(), end_time.strip()

    # 24hrs Format
    hrs_24_match = re.search(r'(\d{1,2}:\d{2})\s*-\s*(\d{1,2}:\d{2})', date_str)
    if hrs_24_match:
        start_time, end_time = hrs_24_match.groups()
        return start_time.strip(), end_time.strip()

    # Handle times like "9pm" and "11pm"
    pm_match = re.search(r'(\d{1,2})pm', date_str, flags=re.IGNORECASE)
    if pm_match:
        start_hour = int(pm_match.group(1))
        if start_hour < 12:
            start_hour += 12
        start_time = f"{start_hour:02}:00"

        # Assume the event ends after the start time
        end_hour = start_hour + 2  # Adding 2 hours as a default duration
        if end_hour >= 24:
            end_hour -= 12
        end_time = f"{end_hour:02}:00"

        return start_time.strip(), end_time

    # Handle times like "9am" and "11am"
    am_match = re.search(r'(\d{1,2})am', date_str, flags=re.IGNORECASE)
    if am_match:
        start_hour = int(am_match.group(1))
        if start_hour == 12:
            start_hour = 0
        start_time = f"{start_hour:02}:00"

        # Assume the event ends after the start time
        end_hour = start_hour + 2  # Adding 2 hours as a default duration
        if end_hour >= 12:
            end_hour -= 12
        end_time = f"{end_hour:02}:00"

        return start_time.strip(), end_time

    return None, None

def get_coordinates(location):
    if location is None:
        print("Location is None!")
        return None, None

    geolocator = Nominatim(user_agent="event_scraper")
    retries = 3
    delay = 2

    location = unidecode(location) if location else None

    for _ in range(retries):
        try:
            location = geolocator.geocode(location, addressdetails=True)
            if location:
                latitude = location.latitude
                longitude = location.longitude
                return latitude, longitude
            else:
                return None, None
        except geopy.exc.GeocoderUnavailable as e:
            time.sleep(delay)

    return None, None

def open_google_maps(latitude, longitude):
    google_maps_url = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
    return google_maps_url

def get_previous_page_image_url(driver):
    url = 'https://www.eventbrite.com/d/canada--montreal/all-events/?page=1'

    driver.get(url)

    if driver.page_source:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        img_tag = soup.find('img', class_='event-card-image')

        if img_tag:
            return img_tag['src']

    return None

def scrape_eventbrite_events(driver, url, selectors, max_pages=30):
    global event_id_counter

    driver.get(url)
    driver.implicitly_wait(20)

    all_events = []

    for _ in range(max_pages):
        try:
            page_content = driver.page_source
            webpage = BeautifulSoup(page_content, 'html.parser')
            events = webpage.find_all(selectors['event']['tag'], class_=selectors['event'].get('class'))

            for event in events:
                event_info = {}
                for key, selector in selectors.items():
                    if key != 'event':
                        element = event.find(selector['tag'], class_=selector.get('class'))
                        event_info[key] = element.text.strip() if element else None
                        if key == 'ImageURL':
                            img_element = event.find('img', class_='event-card__image')
                            event_info[key] = img_element['src'] if img_element and 'src' in img_element.attrs else None

                event_link = event.find('a', href=True)['href']
                driver.get(event_link)

                try:
                    event_page_content = driver.page_source
                    event_page = BeautifulSoup(event_page_content, 'html.parser')

                    title = event_page.find('h1', class_='event-title css-0').text.strip() if event_page.find('h1', class_='event-title css-0') else None
                    description = event_page.find('p', class_='summary').text.strip() if event_page.find('p', class_='summary') else None
                    price = event_page.find('div', class_='conversion-bar__panel-info').text.strip() if event_page.find('div', class_='conversion-bar__panel-info') else None
                    date = event_page.find('span', class_='date-info__full-datetime').text.strip() if event_page.find('span', class_='date-info__full-datetime') else None
                    location_element = event_page.find('p', class_='location-info__address-text')
                    location = location_element.text.strip() if location_element else None
                    ImageURL = get_previous_page_image_url(driver)
                    tags = generate_tags(title, description)

                    # Isolating the number from the price using regular expressions
                    price_number = None
                    if price:
                        price_matches = re.findall(r'\d+\.?\d*', price)
                        if price_matches:
                            price_number = float(price_matches[0])

                    latitude, longitude = get_coordinates(location)

                    organizer = event_page.find('a', class_='descriptive-organizer-info__name-link') if event_page.find('a', class_='descriptive-organizer-info__name-link') else None
                    image_url_organizer = event_page.find('svg', class_='eds-avatar__background eds-avatar__background--has-border')
                    if image_url_organizer:
                        image_tag = image_url_organizer.find('image')
                        if image_tag:
                            event_info['Image URL Organizer'] = image_tag.get('xlink:href')
                        else:
                            event_info['Image URL Organizer'] = None
                    else:
                        event_info['Image URL Organizer'] = None

                    event_info['Title'] = title
                    event_info['Description'] = description
                    event_info['Price'] = price_number
                    event_info['Date'] = date
                    event_info['StartTime'], event_info['EndTime'] = extract_start_end_time(date)
                    event_info['Location'] = location
                    event_info['ImageURL'] = ImageURL
                    event_info['Latitude'] = latitude
                    event_info['Longitude'] = longitude
                    event_info['Organizer'] = organizer.text.strip() if organizer else None
                    event_info['EventUrl'] = event_link
                    event_info['Tags'] = tags

                    if latitude is not None and longitude is not None:
                        map_url = open_google_maps(latitude, longitude)
                        event_info['GoogleMaps_URL'] = map_url

                    all_events.append(event_info)

                except Exception as e:
                    print("Error scraping event page:", e)

                finally:
                    driver.back()

            try:
                next_button = driver.find_element_by_link_text('Next')
                next_button.click()
            except Exception as e:
                print("Error clicking next button:", e)
                break

        except Exception as e:
            print("Error scraping events page:", e)
            break

    return all_events


def main():
    sources = [
        {
            'name': 'Facebook',
            'url': 'https://www.facebook.com/events/explore/montreal-quebec/102184499823699/',
            'selectors': {
                'event': {'tag': 'div', 'class': 'x1qjc9v5 x9f619 x78zum5 xdt5ytf x5yr21d x6ikm8r x10wlt62 xexx8yu x10ogl3i xg8j3zb x1k2j06m xlyipyv xh8yej3'}
            }
        },
        {
            'name': 'Eventbrite',
            'url': 'https://www.eventbrite.com/d/canada--montreal/all-events/',
            'selectors': {
                'event': {'tag': 'div', 'class': 'discover-search-desktop-card discover-search-desktop-card--hiddeable'},
                'Title': {'tag': 'h2', 'class': 'event-card__title'},
                'Description': {'tag': 'p', 'class': 'event-card__description'},
                'Date': {'tag': 'p', 'class': 'event-card__date'},
                'Location': {'tag': 'p', 'class': 'location-info__address-text'},
                'Price': {'tag': 'p', 'class': 'event-card__price'},
                'ImageURL': {'tag': 'img', 'class': 'event-card__image'},
                # 'Tags': {'tag': 'ul', 'class': 'event-card__tags'},
                'Organizer': {'tag': 'a', 'class': 'event-card__organizer'},
                'Organizer_IMG': {'tag': 'svg', 'class': 'eds-avatar__background eds-avatar__background--has-border'}
            }
        }
    ]

    chrome_options = Options()

    driver = webdriver.Chrome(options=chrome_options)

    all_events = []
    unique_event_titles = set()
    duplicate_events = []

    for source in sources:
        if source['name'] == 'Facebook':
            events = scrape_facebook_events(driver, source['url'], source['selectors'])
        elif source['name'] == 'Eventbrite':
            events = scrape_eventbrite_events(driver, source['url'], source['selectors'])
        else:
            print(f"Fonte não suportada: {source['name']}")
            continue

        if events:
            for event in events:
                event_title = event.get('Title')
                if event_title not in unique_event_titles:
                    unique_event_titles.add(event_title)
                    all_events.append(event)
                else:
                    duplicate_events.append(event)

    # JSON File for unique events
    with open('unique_events.json', 'w') as f:
        json.dump(all_events, f, indent=4)

    # JSON File for duplicate events
    with open('duplicate_events.json', 'w') as f:
        json.dump(duplicate_events, f, indent=4)

    driver.quit()

if __name__ == "__main__":
    main()
