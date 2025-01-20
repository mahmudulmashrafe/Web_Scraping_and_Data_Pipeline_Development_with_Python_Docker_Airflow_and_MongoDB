import re 
import json
import requests
from bs4 import BeautifulSoup

def search_new_ads():

    url = "https://www.finn.no/realestate/newbuildings/search.html"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    script_tag = soup.find('script', string=re.compile(r'window\.__remixContext'))

    if script_tag:
        script_content = script_tag.string

        match = re.search(r'window\.__remixContext\s*=\s*({.*});', script_content, re.DOTALL)

        if match:
            json_text = match.group(1)

            data = json.loads(json_text)
            main_data = data['state']['loaderData']['routes/realestate+/_search+/$subvertical.search[.html]']
            search_results = main_data["results"]['docs']

    return search_results