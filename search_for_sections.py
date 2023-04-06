from simplify import fetch_and_simplify_dom
from utils import split_text_into_chunks
from gpt_tools import chat_gpt_with_backoff
from dotenv import load_dotenv
load_dotenv()

from gpt_tools import look_for_clues, compress_knowledge_base



def learn_from_html(url, task):
    simplified_dom = fetch_and_simplify_dom(url)
    chunks = split_text_into_chunks(simplified_dom)
    knowledge_base = []
    for i, chunk in enumerate(chunks):
        print(f'{i}/{len(chunks)}')
        new_knowledge = look_for_clues(chunk, url, i, len(chunks), task)
        if new_knowledge != "No new information.":
            knowledge_base.append(new_knowledge)
    return knowledge_base


def get_scraping_instructions(url, task):
    kb = learn_from_html(url, task)
    summarized = compress_knowledge_base(kb, url, task)
    return summarized

if __name__ == "__main__":
    # Usage example
    url = 'https://www.espn.com/nba/injuries'
    task = "a list of every injured player on every team. Include their name, team, position, status, and the comment field."
    print(get_scraping_instructions(url, task))

    