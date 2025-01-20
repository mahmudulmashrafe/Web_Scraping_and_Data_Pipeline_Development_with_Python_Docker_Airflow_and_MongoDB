# Web Scraping and Data Pipeline Development

This repository contains a web scraping and data pipeline project built using **Python**, **Docker**, **Apache Airflow**, and **MongoDB**. The pipeline scrapes real estate data from the [finn.no](https://www.finn.no/realestate/newbuildings/search.html) website, processes it, and stores it in a MongoDB database.

## Objective

The primary goal is to demonstrate the integration of web scraping, data processing, and data storage, all orchestrated via an Airflow pipeline. This project also ensures reusability and modularity of the codebase.

---

## Features

1. **Web Scraping**:
   - Extracts daily new building advertisements from the `finn.no` website.
   - Fetches essential details such as:
     - Heading and Sub-Heading.
     - Key information (Nøkkelinfo) and Matrikkelinformasjon as key-value pairs.
     - Facilities in a structured format: `{ 'facilities': ['Heis', 'Hage', 'Sentralt', ...] }`.
     - FinnCode and Date.

2. **Data Processing**:
   - Each advertisement is stored as a document in MongoDB with the `FinnCode` as `_id`.
   - Duplicate records are checked and skipped to ensure data integrity.

3. **Data Pipeline with Airflow**:
   - The pipeline is defined using an **Airflow DAG**:
     - **Tasks**:
       1. Search new ads.
       2. Scrape new ads.
       3. Process new ads.
       4. Check existing ads.
       5. Upload new ads.
     - Scheduled to run daily at **2:30 PM**.

4. **Dockerized Environment**:
   - The project includes a Dockerized Airflow setup to simplify deployment and scaling.

---

## Project Structure
. ├── dags/ │├── src/ │|└── search.py │|└──scrape.py │|└── process.py │|└── check_existing.py │|└── upload.py │ └── finn_scraper_dag.py


- **dags/FinnScrapper**: Contains the Airflow DAG and associated scripts.
- **docker-compose.yml**: Docker configuration for Airflow and MongoDB.
- **.env**: Environment variables for sensitive data (e.g., database connection string).

---

## Prerequisites

1. **Python 3.8+**
2. **Docker & Docker Compose**
3. **MongoDB** (Local or Cloud-hosted)
4. **Apache Airflow**

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/web-scraping-data-pipeline.git
   cd web-scraping-data-pipeline


## Setup and Installation

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>

   
Build and Start the Services:

docker compose up
This command builds the Docker images and starts the services defined in docker-compose.yml.

Access Apache Airflow Web Interface:

Once the services are up, you can access the Apache Airflow web interface at http://localhost:2423. The default credentials are:
Username: legacy
Password: legacy

## Usage
Place the FinnScrapper folder inside the Airflow dags/ directory.
Verify that the DAG finn_scrapper_dag is visible in the Airflow UI.
Enable the DAG to schedule daily runs.

## Resources
BeautifulSoup Documentation
MongoDB Official Site
Apache Airflow Documentation

## Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request.
