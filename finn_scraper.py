# import re
# import json
# import requests
# from bs4 import BeautifulSoup
# from pymongo import MongoClient


# def search_new_ads():
#     """Fetch advertisement links from finn.no."""
#     url = "https://www.finn.no/realestate/newbuildings/search.html"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")

#     script_tag = soup.find('script', string=re.compile(r'window\.__remixContext'))
#     if not script_tag:
#         print("Failed to fetch data.")
#         return []

#     script_content = script_tag.string
#     match = re.search(r'window\.__remixContext\s*=\s*({.*});', script_content, re.DOTALL)
#     if not match:
#         print("No match found for advertisement data.")
#         return []

#     json_text = match.group(1)
#     data = json.loads(json_text)
#     main_data = data['state']['loaderData']['routes/realestate+/_search+/$subvertical.search[.html]']
#     return main_data["results"]['docs']


# def scrape_new_ads(ad_data):
#     """Scrape details of each advertisement."""
#     ad_urls = [data["canonical_url"] for data in ad_data]
#     scraped_ad_data = []

#     for url in ad_urls:
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, 'html.parser')

#         heading = soup.find("section", {"aria-label": "Tittel"}).find("h1").text.strip()
#         subheading_tag = soup.find("section", {"aria-label": "Tittel"}).find("h2")
#         subheading = subheading_tag.text.strip() if subheading_tag else None

#         key_info_section = soup.find("section", {"aria-labelledby": "keyinfo-heading"})
#         key_info_dict = {dt.text.strip(): dt.find_next_sibling("dd").text.strip()
#                          for dt in key_info_section.find_all("dt")} if key_info_section else {}

#         cadastre_section = key_info_section.find("section", {"aria-labelledby": "cadastreinfo-part"}) if key_info_section else None
#         cadastre_info_dict = {}
#         if cadastre_section:
#             for div in cadastre_section.find_all("div"):
#                 key, value = div.text.strip().split(":", 1)
#                 cadastre_info_dict[key.strip()] = value.strip()

#         finn_info_section = soup.find("section", {"aria-labelledby": "ad-info-heading"})
#         finn_info_dict = {}
#         if finn_info_section:
#             table = finn_info_section.find('table')
#             if table:
#                 for row in table.find_all('tr')[:2]:
#                     key = row.find('th').text.strip()
#                     value = row.find('td').text.strip()
#                     finn_info_dict[key] = value

#         # Extract FINN-kode from URL if not found in the parsed data
#         finn_code = key_info_dict.get("FINN-kode")
#         if not finn_code:
#             match = re.search(r'finnkode=(\d+)', url)
#             finn_code = match.group(1) if match else None

#         if not finn_code:
#             print(f"Warning: FINN-kode not found for URL: {url}")
#             continue  # Skip ads without a FINN-kode

#         scraped_ad_data.append({
#             '_id': finn_code,  # Use FINN-kode as the unique identifier
#             'heading': heading,
#             'subheading': subheading,
#             'key_info_1': key_info_dict,
#             'key_info_2': cadastre_info_dict,
#             'finn_info': finn_info_dict
#         })

#     return scraped_ad_data


# def check_existing_ads(processed_ad_data):
#     """Remove duplicates by comparing with existing MongoDB entries."""
#     new_finn_ids = [data["_id"] for data in processed_ad_data]

#     with MongoClient('localhost', 27017) as client:
#         db = client["finn_data"]
#         collection = db["real-estate"]
#         existing_finn_ids = [doc["_id"] for doc in collection.find({}, {'_id': True})]

#     duplicates = set(new_finn_ids).intersection(existing_finn_ids)
#     filtered_ad_data = [data for data in processed_ad_data if data["_id"] not in duplicates]
#     return filtered_ad_data


# def upload_new_ads(filtered_ad_data):
#     """Upload the filtered advertisements to MongoDB."""
#     with MongoClient('localhost', 27017) as client:
#         db = client["finn_data"]
#         collection = db["real-estate"]
#         if filtered_ad_data:
#             collection.insert_many(filtered_ad_data)
#             print(f"Uploaded {len(filtered_ad_data)} new ads to MongoDB.")
#         else:
#             print("No new ads to upload.")


# def main():
#     """Main script logic."""
#     print("Searching for new ads...")
#     search_results = search_new_ads()

#     if not search_results:
#         print("No new ads found.")
#         return

#     print("Scraping ad details...")
#     scraped_data = scrape_new_ads(search_results)

#     print("Checking for duplicates...")
#     filtered_data = check_existing_ads(scraped_data)

#     print("Uploading new ads to MongoDB...")
#     upload_new_ads(filtered_data)


# if __name__ == "__main__":
#     main()
