# Web scraping in a functional programming style with Python

This is the demonstration code for my related blog article. Read the
two-part blog article for more background on the project here: Part I (functional
programming) and Part II (explanation of this project).

The code runs web scraping on the two web pages specified in data/webpage.json.

If you want to try out the code, here is how to get started:

- Developed and tested with Python 3.11, MacOS/Unix
- clone the repo and go to the directory for post_3
- create a virtual environment: `python -m venv venv`
- activate the virtual environment: `source venv/bin/activate` (or equivalent command on Windows)
- install requirements: `pip install -r requirements.txt`
- Install the cli app from the setup.py: `pip install .`

Use the cli app to run a scraping process with the venv activated:
- `scraper_cli run-spiders data/webpage.json --max-days 60`

(requires the path to the json file with the data for the web pages to be scraped.
Optionally, you can indicate how many days back you want to search for documents;
default is 40 days)

Disclaimer: The two web sites indicated in data/webpage.json are only
illustrative examples. If you try out this project, be polite to these web
sites and respect best practices for web scraping. I tested the project before
publishing the blog post on 1 September 2023. But the web sites might change in the future.