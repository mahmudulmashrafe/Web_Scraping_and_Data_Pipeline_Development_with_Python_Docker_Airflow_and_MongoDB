from airflow.decorators import dag, task
from datetime import datetime
from FinnScrapper.src.search import search_new_ads
from FinnScrapper.src.scrape import scrape_new_ads
from FinnScrapper.src.process import process_new_ads
from FinnScrapper.src.check_existing import check_existing_ads
from FinnScrapper.src.upload import upload_new_ads


@dag(
        dag_id = "finn_scrapper_dag",
        schedule_interval = "30 2 * * *",
        start_date = datetime(2022, 1, 1), 
        catchup = False,
        tags = ["finn.no", "real-estate"]
    )
def finn_scrapper_dag():

    @task(task_id="search_new_ads")
    def search_new_ads_task(task_instance):
        search_results = search_new_ads()
        task_instance.xcom_push(key="search_results", value=search_results)
        return search_results

    @task(task_id="scrape_new_ads")
    def scrape_new_ads_task(task_instance):
        search_results = task_instance.xcom_pull(task_ids="search_new_ads")
        scraped_ad_data = scrape_new_ads(search_results)
        task_instance.xcom_push(key="scraped_data", value=scraped_ad_data)
        return scraped_ad_data
    
    @task(task_id="process_new_ads")
    def process_new_ads_task(task_instance):
        scraped_ad_data = task_instance.xcom_pull(task_ids="scrape_new_ads")
        processed_ad_data = process_new_ads(scraped_ad_data)
        task_instance.xcom_push(key="processed_ad_data", value=processed_ad_data)
        return processed_ad_data

    @task(task_id="check_existing_ads")
    def check_existing_ads_task(task_instance):
        processed_ad_data = task_instance.xcom_pull(task_ids="process_new_ads")
        filtered_ad_data = check_existing_ads(processed_ad_data)
        task_instance.xcom_push(key="filtered_ad_data", value=filtered_ad_data)
        return filtered_ad_data

    @task(task_id="upload_new_ads")
    def upload_new_ads_task(task_instance):
        filtered_ad_data = task_instance.xcom_pull(task_ids="check_existing_ads")
        upload_new_ads(filtered_ad_data)

    search_ads = search_new_ads_task()
    scrape_ads = scrape_new_ads_task()
    process_ads = process_new_ads_task()
    existing_ads = check_existing_ads_task()
    upload_ads = upload_new_ads_task()

    search_ads >> scrape_ads >> process_ads >> existing_ads >> upload_ads

dag = finn_scrapper_dag()