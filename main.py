import json 
import requests
from bs4 import BeautifulSoup


POKEDEX_URL = "https://www.serebii.net/pokemon/nationalpokedex.shtml"

MOVE_URL = "https://bulbapedia.bulbagarden.net/wiki/List_of_moves#bulbapedia"

def filter_pokemon_rows(rows):
    f_rows = []
    for row in rows:
        if row.find('td', {'class' : 'fooinfo', 'align' : 'center'}):
            f_rows.append(row)


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

def scrape_pokedex(url):  
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    all_rows = soup.find_all('tr')
    pokemon_rows = filter_pokemon_rows(all_rows)



def run():
    pass


if __name__ == "__main__":
    run()