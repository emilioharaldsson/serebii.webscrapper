import json
import rich
import requests
from bs4 import BeautifulSoup


move_pokemon = []

def filter_pokemon_cells(cell):
    a = cell.find('a')
    return a and a.get('href') and a.get('href').startswith('/pokedex-sv/') and not a.find('img')

def get_rows(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    all_cells = soup.find_all('td', {'class':'fooinfo', 'align':'center'})
    pokemon_cells = [td.find('a').text for td in all_cells if filter_pokemon_cells(td)]
    return list(set(pokemon_cells))

def run(data):
    for pokemon in data:
        url = pokemon['url']
        pokemon_list = get_rows(url)
        move_pokemon.append({
            "name" : pokemon["name"],
            "pokemon" : pokemon_list
        })
    
if __name__ == "__main__":
    with open("move_urls.json") as json_file:
        data = json.load(json_file)
    run(data)
    with open ("move_pokemon.json", "w", encoding='utf-8') as f:
        json.dump(move_pokemon, f, indent=4)