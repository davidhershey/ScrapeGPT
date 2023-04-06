# url: https://boardgamegeek.com/hotness
# task: A ranked list of the 50 hottest board games and a link to their page on bgg
import requests
from bs4 import BeautifulSoup
from simplify import fetch_and_simplify_dom

def get_hot_board_games(url):
    simplified_html = fetch_and_simplify_dom(url)
    soup = BeautifulSoup(simplified_html, 'html.parser')
    
    hot_games = []
    
    for li in soup.find_all('li', class_='numbered-game-list__item'):
        rank = li.find('h2', class_='numbered-game-list__position').text.strip()
        game_link = li.find('a', class_='stretched-link link-text-color')
        name = game_link.text.strip()
        link = game_link['href']
        release_year = li.find('span', class_='post-meta__item').text.strip()
        description = li.find('p', class_='tw-mt-1 tw-mb-0 tw-text-xs tw-line-clamp-3 md:tw-text-sm').text.strip()
        
        hot_games.append({
            'rank': rank.strip(),
            'name': name.strip(),
            'link': link.strip(),
            'release_year': release_year.strip(),
            'description': description.strip()
        })
    
    return hot_games

if __name__ == '__main__':
    url = 'https://boardgamegeek.com/hotness'
    hot_board_games = get_hot_board_games(url)
    for game in hot_board_games:
        # print(game['rank'])
        print(f"{game['rank'][0]}. {game['name']} ({game['release_year']}) - {game['link']}")
        print(f"Description: {game['description']}\n")
    print(len(hot_board_games))
