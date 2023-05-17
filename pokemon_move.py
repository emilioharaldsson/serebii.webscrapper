import json
import rich
import requests
from bs4 import BeautifulSoup


move_pokemon = []

with open ("pokedex_urls.json", 'r') as r:
    data = json.load(r)

def filter_for_move_name(td):
    a = td.find('a')
    return a and a.get('href').startswith('/attackdex')


def get_cells(pokemon):
    response = requests.get(pokemon['url'])
    soup = BeautifulSoup(response.content, "html.parser")
    all_tds = soup.find_all('td', {'class': 'fooinfo', 'rowspan': '2'})
    all_move_names = list(set([td.find('a').text for td in all_tds if filter_for_move_name(td)]))
    return all_move_names

if __name__ == "__main__":
    for pokemon in data:
        moves = get_cells(pokemon)
        move_pokemon.append({
            "name": pokemon['name'],
            "moves": moves
        })
    rich.print(move_pokemon)
    with open ("pokemon_move.json", "w", encoding='utf-8') as f:
        json.dump(move_pokemon, f, indent=4)