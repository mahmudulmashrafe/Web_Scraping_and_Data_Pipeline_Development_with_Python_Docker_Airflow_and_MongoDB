from pymongo import MongoClient

def upload_new_ads(filtered_ad_data):   
    with MongoClient('mongo', 27017) as client:
        db = client["finn_data"]
        collection = db["data"]
        if len(filtered_ad_data) > 0:
            collection.insert_many(filtered_ad_data)

            
