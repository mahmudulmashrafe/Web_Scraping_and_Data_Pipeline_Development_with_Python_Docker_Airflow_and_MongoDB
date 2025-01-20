import json
from pymongo import MongoClient

def check_existing_ads(processed_ad_data):
    
    new_finn_id = [data["_id"] for data in processed_ad_data]

    with MongoClient('mongo', 27017) as client:
        db = client["finn_data"]
        collection = db["data"]
        existing_finn_id = [doc["_id"] for doc in collection.find({},{'_id':True})]

    duplicates = set(new_finn_id).intersection(existing_finn_id)

    filtered_ad_data = [data for data in processed_ad_data if data["_id"] not in duplicates]
    
    return filtered_ad_data