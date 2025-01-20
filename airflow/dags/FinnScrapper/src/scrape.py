import re
from bs4 import BeautifulSoup
import requests

def scrape_new_ads(ad_data):
    """Scrape details of each advertisement."""
    ad_urls = [data["canonical_url"] for data in ad_data]
    scraped_ad_data = []

    for url in ad_urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        heading = soup.find("section", {"aria-label": "Tittel"}).find("h1").text.strip()
        subheading_tag = soup.find("section", {"aria-label": "Tittel"}).find("h2")
        subheading = subheading_tag.text.strip() if subheading_tag else None

        key_info_section = soup.find("section", {"aria-labelledby": "keyinfo-heading"})
        key_info_dict = {dt.text.strip(): dt.find_next_sibling("dd").text.strip()
                         for dt in key_info_section.find_all("dt")} if key_info_section else {}

        cadastre_section = key_info_section.find("section", {"aria-labelledby": "cadastreinfo-part"}) if key_info_section else None
        cadastre_info_dict = {}
        if cadastre_section:
            for div in cadastre_section.find_all("div"):
                key, value = div.text.strip().split(":", 1)
                cadastre_info_dict[key.strip()] = value.strip()

        finn_info_section = soup.find("section", {"aria-labelledby": "ad-info-heading"})
        finn_info_dict = {}
        if finn_info_section:
            table = finn_info_section.find('table')
            if table:
                for row in table.find_all('tr')[:2]:
                    key = row.find('th').text.strip()
                    value = row.find('td').text.strip()
                    finn_info_dict[key] = value

        finn_code = key_info_dict.get("FINN-kode")
        if not finn_code:
            match = re.search(r'finnkode=(\d+)', url)
            finn_code = match.group(1) if match else None

        if not finn_code:
            print(f"Warning: FINN-kode not found for URL: {url}")
            continue

        scraped_ad_data.append({
            '_id': finn_code,
            'heading': heading,
            'subheading': subheading,
            'key_info_1': key_info_dict,
            'key_info_2': cadastre_info_dict,
            'finn_info': finn_info_dict
        })

    return scraped_ad_data
