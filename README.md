# FinnScrapper: Real Estate Ad Pipeline

This project implements an Airflow DAG to automate the process of scraping and uploading new real estate ads from Finn.no. It leverages Docker for containerized execution.

**Key Features:**

* **Automated Scraping:** Periodically searches Finn.no for new ads based on your defined criteria.
* **Data Processing:** Cleans and filters scraped data to prepare it for upload.
* **Existing Ad Check:** Optionally checks for existing ads to avoid duplicates (implementation provided in `FinnScrapper.src.check_existing_ads.py`).
* **Dockerized Execution:** Ensures consistent environment and dependencies across deployments.
* **XCom for Data Exchange:** Facilitates communication between tasks within the Airflow DAG.

**Requirements:**

* Apache Airflow
* Docker
* Python 3.x 

**Installation:**

1.  **Set up and Docker:**
      - Install and configure Docker: Docker Documentation

2.  **Clone this repository:**

    bash
      ```
      git clone [https://github.com/HIMU-0010/Real-estate_ad_scraping_project_using_Docker_AirFlow.git]
      ```

**Configuration:**

1.  **Airflow DAG:**

      - Update the Airflow DAG definition (`finn_scrapper_dag.py`) with your specific requirements, such as:
          - `schedule_interval`: How often to run the DAG.
          - Finn.no search criteria (implementation in `FinnScrapper.src.search_new_ads`).
          - Data processing logic (implementation in `FinnScrapper.src.process_new_ads`).
          - Existing ad check configuration (optional, implementation in `FinnScrapper.src.check_existing_ads`).
          - Upload destination and credentials (implementation in `FinnScrapper.src.upload_new_ads`).

2.  **Dockerfile (Optional):**

      - `Dockerfile` specifies the Airflow environment and dependencies.

**Usage:**

1.  **Start project:**

    bash
     ```
      docker compose up 
      ```

2.  **Access Airflow webserver:**

      - Goto http://localhost:2423/
      - And use "legacy" as username and password
      - run the dag and wait for scheduled interval to access the data

**Contributing:**

You are welcome to make contributions to this project! Please feel free to create pull requests to improve the code, documentation, or add new features.
