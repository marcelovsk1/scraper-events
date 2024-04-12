import openai
import json
import re

openai.api_key = ""

def generate_tags(event_title):
    prompt = (
        f"Generate tags related to the event \"{event_title}\". These tags should be one-word keywords that accurately represent the essence of the event. "
        "Keywords for the event:"
    )

    response = openai.Completion.create(
        engine="davinci-002",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None
    )

    tags = [line.strip() for line in response.choices[0].text.strip().split("\n") if line.strip()]
    return tags

def add_generic_tag(tags):
    if not tags:
        return ["Event"]
    return tags

def remove_tags_with_numbers(tags):
    return [tag for tag in tags if not re.search(r'\d', tag)]

if __name__ == '__main__':
    # Carregar o conteúdo do arquivo JSON
    with open('unique_events.json', 'r') as file:
        events_data = json.load(file)

    # Gerar tags para cada evento
    for event in events_data:
        event_title = event.get('Title')
        if event_title:
            tags = generate_tags(event_title)
            tags = add_generic_tag(tags)
            tags = remove_tags_with_numbers(tags)
            # Atualiza a lista de tags do evento
            event['Tags'] = tags

    # Salvar os dados atualizados de volta no arquivo JSON
    with open('unique_events_with_tags.json', 'w') as file:
        json.dump(events_data, file, indent=4)



########################

import openai
import requests

openai.api_key = "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"  # Sua chave de API do OpenAI
ticketmaster_api_key = "XXEn18ypu1or6412B7C4P6iP3EFO7Mfx"  # Sua chave de API da Ticketmaster

def get_ticketmaster_tags(api_key):
    url = "https://app.ticketmaster.com/discovery/v2/classifications/segments?apikey=" + api_key

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "segments" in data:
            tags = [segment["name"] for segment in data["segments"]]
            return tags
    return []

def generate_tags(title, description, ticketmaster_tags):
    # Concatenar as tags da Ticketmaster com o prompt para o GPT
    ticketmaster_tags_str = ", ".join(ticketmaster_tags)
    prompt = (
        f"Generate tags related to the event \"{title}\" and \"{description}\", "
        f"using Ticketmaster tags: {ticketmaster_tags_str}."
    )

    response = openai.Completion.create(
        engine="davinci-002",
        prompt=prompt,
        max_tokens=50,  # Defina o número máximo de tokens de acordo com suas necessidades
        n=1,
        stop=None
    )

    # Extrair as tags geradas pelo GPT e formatá-las corretamente
    generated_tags = response.choices[0].text.strip().split(",")
    formatted_generated_tags = [tag.strip() for tag in generated_tags]

    # Combinação das tags da Ticketmaster e as tags geradas pelo GPT
    combined_tags = ticketmaster_tags + formatted_generated_tags
    unique_tags = list(set(combined_tags))  # Remover tags duplicadas

    return unique_tags

###########################
