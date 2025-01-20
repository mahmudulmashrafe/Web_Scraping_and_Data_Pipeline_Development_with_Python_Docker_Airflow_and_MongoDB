from pymongo import MongoClient

def process_new_ads(processed_ad_data):
    """Remove duplicates by comparing with existing MongoDB entries."""
    new_finn_ids = [data["_id"] for data in processed_ad_data]

    with MongoClient('mongo', 27017) as client:
        db = client["finn_data"]
        collection = db["data"]
        existing_finn_ids = [doc["_id"] for doc in collection.find({}, {'_id': True})]

    duplicates = set(new_finn_ids).intersection(existing_finn_ids)
    filtered_ad_data = [data for data in processed_ad_data if data["_id"] not in duplicates]
    return filtered_ad_data
