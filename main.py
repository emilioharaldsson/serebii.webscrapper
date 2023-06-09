import json 
import requests
from bs4 import BeautifulSoup
import rich

POKEDEX_URL = "https://www.serebii.net/pokemon/nationalpokedex.shtml"

MOVE_URL = "https://bulbapedia.bulbagarden.net/wiki/List_of_moves#bulbapedia"

def has_pokemon(tr):
    td = tr.find('td', {'class': 'fooinfo', 'align': 'center'})
    return td is not None



def scrape_movedex(url):
    move_list = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    parent_table = soup.find('table', {'class' : 'sortable roundy'})
    target_table = parent_table.find('table', {'class' : 'sortable roundy'})
    for i, row in enumerate(target_table.find_all('tr')[1:]):
        columns = row.find_all('td')
        data = {
        'id': columns[0].text.strip(),
        'name': columns[1].text.strip(),
        'type': columns[2].text.strip(),
        'category': columns[3].text.strip(),
        'PP': columns[4].text.strip(),
        'power': columns[5].text.strip(),
        'accuracy': columns[6].text.strip(),
        'gen': columns[7].text.strip()
    }
        move_list.append(data)

    with open ("moves.json", "w", encoding='utf-8') as f:
        json.dump(move_list, f, indent = 4)

def filter_for_pokemon_name(td):
    a = td.find('a')
    return a and a.get('href') and a.get('href').startswith('/pokemon/')

def filter_for_pokemon_type(td):
    a= td.find('a')
    return a and a.get('href') and a.get('href').startswith('/pokemon/type/')
     
def filter_for_pokemon_nature(td):
    a = td.find('a')
    return a and a.get('href') and a.get('href').startswith('/abilitydex/')

def filter_for_pokemon_stats(td):
    return td.find('a') is None;

def get_pokemon_name(tr):
    a = []
    td_elements = tr.find_all('td')
    for td in td_elements:
        if filter_for_pokemon_name(td):
            a.append(td.find('a').text)
    return a

def get_pokemon_stats_from_row(tr):
    stats = []
    tds = tr.find_all('td')
    for td in tds:
        if filter_for_pokemon_stats(td):
            stats.append(td.text.strip())
    return stats

def get_pokemon_types(tr):
    types = []
    all_tds = tr.find_all('td')
    for td in all_tds:
        if filter_for_pokemon_type(td):
            all_anchords = td.find_all('a')
            for a in all_anchords:
                types.append(a['href'].split('/')[-1])
    return types

def get_pokemon_natures(tr):
    natures = []
    all_tds = tr.find_all('td')
    for td in all_tds:
        if filter_for_pokemon_nature(td):
            all_a = td.find_all('a')
            for a in all_a:
                natures.append(a.text)
    return natures
            

def scrape_pokedex(url):
    pokedex = []  
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    all_rows = soup.find_all('tr')
    pokemon_rows = [row for row in all_rows if has_pokemon(row)]
    for pokemon in pokemon_rows:
        stats = get_pokemon_stats_from_row(pokemon)
        pokemon_name = get_pokemon_name(pokemon)
        pokemon_types = get_pokemon_types(pokemon)
        pokemon_natures = get_pokemon_natures(pokemon)
        pokedex.append({
            "no_#": stats[0],
            "name": pokemon_name[2],
            "hp" : stats[1],
            "attack": stats[2],
            "defence": stats[3],
            "sp_attack": stats[4],
            "sp_defence": stats[5],
            "speed" : stats[6],
            "type": pokemon_types,
            "nature": pokemon_natures
        })
    with open ("pokedex.json", "w", encoding='utf-8') as f:
        json.dump(pokedex, f, indent = 4)
        


def run():
    scrape_movedex(MOVE_URL)
    scrape_pokedex(POKEDEX_URL)


if __name__ == "__main__":
    run()