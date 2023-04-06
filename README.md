# Web Scraper Builder with GPT-4

This project is a web scraper builder that uses GPT-4 to automatically generate Python scripts for scraping websites based on user input. The app is built using Streamlit and allows users to input a URL and describe the data they want to scrape. The app then generates a Python script using GPT-4, which can be edited and debugged within the app.

## Features

- Automatically generate custom Python web scrapers using GPT-4
- Automatically debug your scraper

## Installation

1. Clone the repository:

```
git clone https://github.com/davidhershey/ScrapeGPT
```

2. Change to the project directory:

```
cd ScrapeGPT
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

4. Set the `OPENAI_API_KEY` environment variable to your OpenAI API key. You can also use a `.env` file, which should look like this:
```
OPENAI_API_KEY="YOUR_KEY"
```

5. [optionally set up [Promptlayer](https://promptlayer.com/home)] Set the `PROMPTLAYER_API_KEY` environment variable to your PROMPTLAYER_API_KEY API key. You can also use a `.env` file, which should look like this:
```
PROMPTLAYER_API_KEY="YOUR_KEY"
```

6. Run the Streamlit app:

```
streamlit run app.py
```

7. Open the app in your browser using the URL provided in the terminal.

## Usage

1. Enter a sample URL in the "Sample URL" field.
2. Describe the data you want to scrape in the "Describe what you want to scrape from this page" field.
3. Click the "Get Started!" button to generate a function name for your scraper.
4. Optionally, edit the function name in the "Name of the function to generate" field.
5. Click the "Build a scraper!" button to generate the scraper code.
6. Edit the generated code if necessary.
7. Use the "Automatic Debugger" section to iteratively debug the code. You can choose how many debugging rounds the model should do, and which model should be used.
8. Once the code is working, the final scraper code will be displayed in the "Final Code" section.

## Examples
There are a few examples of successful runs in the [successes folder](successes/)

## Limitations

* All of the web scrapers have a dependency on code that is used to annotate and simplify the HTML. That code is in `simplify.py`, and needs to be available to your scraper code. (The simplificaiton happens to reduce the number of tokens sent to GPT-4).
* Right now can write scrapers for a single page

## TODO

* Generate unit tests by looking at the simplified dom which should provide better auto-debugging

## Ackowledgements

* I relied heavily on [TaxyAI's browser-extension](https://github.com/TaxyAI/browser-extension) for the HTML simplification logic. I translated their logic from typescript to Python using GPT-4 to save some time :)
* [Promptlayer](https://promptlayer.com/home) made my life a lot easier when debugging the long chains of prompts used in this project

