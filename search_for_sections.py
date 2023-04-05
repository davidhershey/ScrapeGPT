from simplify import get_simplified_dom
from utils import split_text_into_chunks
from gpt_tools import chat_gpt_with_backoff
from dotenv import load_dotenv
load_dotenv()

from prompts import system_prompt, look_for_clues_prompt, compress_knowledge_base_prompt


def look_for_clues(chunk, url, idx, num_chunks, task):
    prompt = look_for_clues_prompt(url, task, idx, num_chunks, chunk)
    
    completion = chat_gpt_with_backoff(
      model="gpt-3.5-turbo",
      temperature=0.0,
      max_tokens=1000,
      messages=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": prompt}
      ]
    )
    return completion["choices"][0]["message"]["content"]


def compress_knowledge_base(kb, url, task):
    prompt = compress_knowledge_base_prompt(kb, url, task)
    completion = chat_gpt_with_backoff(
      model="gpt-4",
      temperature=0.0,
      max_tokens=1000,
      messages=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": prompt}
      ]
    )
    return completion["choices"][0]["message"]["content"]

def learn_from_html(url, task):
    simplified_dom = get_simplified_dom(url)
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

    