def system_prompt():
    return "You are ScrapeGPT, a helpful assistant that helps write python scripts to scrape websites."


def extract_fn_name_prompt(url, instructions):
    return f"""Your goal is to write a python function to scrape a website for some information.
    
Website: {url}
What to scrape: {instructions}

What should we name our function? Respond with only the function name."""


def look_for_clues_prompt(url, task, idx, num_chunks, chunk):
    return f"""Our goal is to scrape {url}, and we want to scrape {task}.

Before we write any code, we're going to loop through the website one part at a time to figure out where we can find the relevant information on the page.

Part {idx} of {num_chunks}:
```
{chunk}
```

If any of the information we are trying to scrape is in this part, succinctly summarize the structure of the page in a way that would be helpful when we write the scraper. Include information about the tags so that we can scrape them effectively.

For each piece of relevant and new information, include a condensed snippet of HTML that shows the relevant information we need for our scraper.

If there is no relevant information, simply respond 'No new information'."""


def compress_knowledge_base_prompt(kb, url, task):
    notes = "\n".join(kb)
    return f"""Our goal is to scrape {url}, and we want to scrape {task}.

I just finished going through the html, and took some notes about where to find the relevant information. Here are my notes:
```
{notes}
```

Summarize my notes into a shorter description of how to scrape the relevant information from the website. The notes are chronological and don't have perfect context, so you may want to ignore some of the notes if you think they may be misleading."""


def write_scraper_prompt(url, task, function_name, instructions):
    return f"""Let's write a web scraping script together in Python. Our goal is to scrape {url}, and we want to scrape {task}

Here are some notes I took about how I think we can solve this problem:
```
{instructions}
```

Write a python script to complete this scraping task. Write a function called `{function_name}`. Make sure to strip any excess whitespace. I have a helper function that downloads and simplifies the HTML of a page that you should use, which should look like this:
```
from simplify import fetch_and_simplify_dom

simplified_html = fetch_and_simplify_dom(url)
```
"""


def debug_error_prompt(function_name, stdout, stderr):
    return f"""When I ran the scraper, I got an error with this output:
```
STDOUT
------
{stdout}

STDERR
------
{stderr}
```
Can you fix it and return the whole fixed script?"""
