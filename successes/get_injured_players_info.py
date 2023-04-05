# url: https://www.espn.com/nba/injuries
# task: A list of every injured player on every team. Include their name, team, position, status, and the comment field

from bs4 import BeautifulSoup
from simplify import get_simplified_dom

def get_injured_players_info(url):
    simplified_html = get_simplified_dom(url)
    soup = BeautifulSoup(simplified_html, 'html.parser')

    wrapper = soup.find('div', class_='Wrapper Card__Content')
    injury_tables = wrapper.find_all('div', class_='ResponsiveTable Table__league-injuries')

    injured_players = []

    for table in injury_tables:
        team_name = table.find('span', class_='injuries__teamName').text.strip()
        player_table = table.find('table', class_='Table')
        player_rows = player_table.tbody.find_all('tr')

        for row in player_rows:
            player_name = row.find('td', class_='col-name Table__TD').a.text.strip()
            position = row.find('td', class_='col-pos Table__TD').text.strip()
            date_of_injury = row.find('td', class_='col-date Table__TD').text.strip()
            status = row.find('td', class_='col-stat Table__TD').span.text.strip()

            comment_td = row.find('td', class_='col-desc Table__TD')
            comment = comment_td.text.strip() if comment_td else ''

            injured_players.append({
                'name': player_name,
                'team': team_name,
                'position': position,
                'date_of_injury': date_of_injury,
                'status': status,
                'comment': comment
            })

    return injured_players

url = 'https://www.espn.com/nba/injuries'
injured_players = get_injured_players_info(url)

for player in injured_players:
    print(player)
