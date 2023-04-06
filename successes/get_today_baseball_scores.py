# url: https://www.baseball-reference.com/boxes/
# task: A list of the scores of every baseball game that happened today

from bs4 import BeautifulSoup
from simplify import fetch_and_simplify_dom

def get_today_baseball_scores(url):
    simplified_html = fetch_and_simplify_dom(url)
    soup = BeautifulSoup(simplified_html, 'html.parser')

    game_summaries_div = soup.find('div', class_='game_summaries')
    game_divs = game_summaries_div.find_all('div', class_='game_summary nohover')

    scores = []

    for game_div in game_divs:
        teams_table = game_div.find('table', class_='teams')
        winner_row = teams_table.find('tr', class_='winner')
        loser_row = teams_table.find('tr', class_='loser')

        winner_team = winner_row.find('a').text.strip()
        winner_score = winner_row.find('td', class_='right').text.strip()

        loser_team = loser_row.find('a').text.strip()
        loser_score = loser_row.find('td', class_='right').text.strip()

        scores.append((winner_team, winner_score, loser_team, loser_score))

    return scores

url = 'https://www.baseball-reference.com/boxes/'
today_scores = get_today_baseball_scores(url)
print(today_scores)
