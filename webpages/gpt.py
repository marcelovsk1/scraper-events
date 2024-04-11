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
