import json
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from geopy.geocoders import Nominatim
import re
from datetime import datetime
import openai

client = openai.OpenAI(api_key='sk-proj-9u5cdlccA0ZcAuhepyhGT3BlbkFJb8GBvlHY8d6DvxuElr6F') # to do: move it into .env variables

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


def scroll_to_bottom(driver, max_scroll=1):
    for _ in range(max_scroll):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)


def scroll_to_bottom(driver, max_scroll=1):
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
        start_month_num = datetime.strptime(start_month, '%B').month

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
    geolocator = Nominatim(user_agent="event_scraper", timeout=30)  # Aumentando o tempo limite para 10 segundos
    location = geolocator.geocode(location)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def open_google_maps(latitude, longitude):
    google_maps_url = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
    return google_maps_url

def get_location_details(latitude, longitude):

    try:
        geolocator = Nominatim(user_agent="event_scraper")
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        if location:
            address = location.address
            city = location.raw.get('address', {}).get('city')
            country_code = location.raw.get('address', {}).get('country_code')

            # Ajuste para Montreal e ca apenas se ambos forem None
            if city is None and country_code is None:
                city = 'Montreal'
                country_code = 'ca'
            elif city and city.lower() == 'montreal':
                city = 'Montreal'
                country_code = 'ca'

            return address, city, country_code
        else:
            return None, None, None
    except Exception as e:
        print(f"An error occurred while fetching location details: {e}")
        return None, None, None

def scrape_facebook_events(driver, url, selectors, max_scroll=30):
    global event_id_counter  # Referencing the global variable

    driver.get(url)
    driver.implicitly_wait(20)

    all_events = []
    unique_event_titles = set()

    # Scroll down to load more events
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
            event_title = event_title_elem.text.strip()
            if any(event_title == existing_title for existing_title in unique_event_titles):
                continue
        else:
            continue

        description = event_page.find('div', class_='xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs').text.strip() if event_page.find('div', class_='xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs') else None

        location_div = event_page.find('div', class_='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f')
        location_span = event_page.find('span', class_='xt0psk2')
        location_text = location_div.text.strip() if location_div else (location_span.text.strip() if location_span else None)

        latitude, longitude = get_coordinates(location_text)
        google_maps_url = open_google_maps(latitude, longitude)
        event_id_counter = 0

        address_span = event_page.find('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x1f6kntn xvq8zen xo1l8bm xi81zsa x1yc453h')
        address = address_span.text.strip() if address_span else None

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
        print("Date text:", date_text)  # Add this line for debugging

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
            'Title': event_title,
            'Description': description,
            'Date': format_date(date_text),  # Corrected to pass the original date
            **location_details,
            'ImageURL': event_page.find('img', class_='xz74otr x1ey2m1c x9f619 xds687c x5yr21d x10l6tqk x17qophe x13vifvy xh8yej3')['src'] if event_page.find('img', class_='xz74otr x1ey2m1c x9f619 xds687c x5yr21d x10l6tqk x17qophe x13vifvy xh8yej3') else None,
            'Organizer': event_page.find('span', class_='xt0psk2').text.strip() if event_page.find('span', class_='xt0psk2') else None,
            'Organizer_IMG': event_page.find('img', class_='xz74otr')['src'] if event_page.find('img', class_='xz74otr') else None,
            'EventUrl': event_url,
            'StartTime': start_time,
            'EndTime': end_time,
        }

        # Call generate_tags function here passing event title and description
        event_tags = generate_tags(event_title, description)
        event_info['Tags'] = event_tags

        all_events.append(event_info)
        unique_event_titles.add(event_title)

        driver.back()

    return all_events if all_events else None

if __name__ == "__main__":
    sources = [
        {
            'name': 'Facebook',
            'url': 'https://www.facebook.com/events/explore/montreal-quebec/102184499823699/',
            'selectors': {
                'event': {'tag': 'div', 'class': 'x1qjc9v5 x9f619 x78zum5 xdt5ytf x5yr21d x6ikm8r x10wlt62 xexx8yu x10ogl3i xg8j3zb x1k2j06m xlyipyv xh8yej3'}
            }
        }
    ]

    driver = webdriver.Chrome()

    all_events = []
    for source in sources:
        print(f"Scraping events from: {source['name']}")
        if source['name'] == 'Facebook':
            events = scrape_facebook_events(driver, source['url'], source['selectors'])  # Corrected incomplete statement
            if events is not None:
                for event in events:
                    if 'Div' in event['Location']:
                        event['Location']['Div'] = str(event['Location']['Div'])
                    if 'Span' in event['Location']:
                        event['Location']['Span'] = str(event['Location']['Span'])

                all_events.extend(events)
            else:
                print("No events found.")

    # Save events to JSON file
    with open('facebook.json', 'w') as f:
        json.dump(all_events, f, indent=4)

    driver.quit()
