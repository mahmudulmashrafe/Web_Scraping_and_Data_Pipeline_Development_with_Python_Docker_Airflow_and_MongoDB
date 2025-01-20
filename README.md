# Web Scraping using MongoDB, Python, and Apache Airflow Integration

This project demonstrates how to set up a data pipeline using MongoDB, Python, and Apache Airflow, all orchestrated with Docker Compose. The pipeline fetches real estate advertisements from [Finn.no](https://www.finn.no/realestate/newbuildings/search.html), processes the data, and stores it in a MongoDB database.

## Project Structure

. ├── dags/ 
  │├── src/ 
  │|└── search.py 
  │|└──scrape.py 
  │|└── process.py 
  │|└── check_existing.py 
  │|└── upload.py 
  │ └── finn_scraper_dag.py

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup and Installation

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
Build and Start the Services:

bash
Copy
docker-compose up --build
This command builds the Docker images and starts the services defined in docker-compose.yml.

Access Apache Airflow Web Interface:

Once the services are up, you can access the Apache Airflow web interface at http://localhost:8080. The default credentials are:

Username: legacy
Password: legacy
Configure MongoDB Connection in Airflow:

Navigate to the Airflow web interface.
Go to Admin > Connections.
Click on + to add a new connection with the following details:
Conn Id: mongo_default
Conn Type: MongoDB
Host: mongo
Schema: finn_data
Login: root
Password: root
Port: 27017
Run the DAG:

In the Airflow web interface, navigate to the DAGs tab.
Find the finn_scraper_dag and trigger it.
Docker Compose Configuration
The docker-compose.yml file defines the following services:

mongo: MongoDB service running on port 27017.
airflow: Apache Airflow services, including the web server, scheduler, and worker.
yaml
Copy
version: '3.8'

services:
  mongo:
    image: mongo:latest
    command: ["mongod", "--port", "27017"]
    ports:
      - "27017:27017"
    healthcheck:
      test: ["CMD", "mongo", "--eval", "db.adminCommand('ping')"]
      interval: 5s
      timeout: 40s
      retries: 5
    restart: always

  airflow:
    image: apache/airflow:2.7.2-python3.11
    environment:
      - AIRFLOW_UID=50000
      - AIRFLOW_GID=0
      - AIRFLOW_HOME=/opt/airflow
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=sqlite:////opt/airflow/airflow.db
      - AIRFLOW__CORE__LOAD_EXAMPLES=False
      - AIRFLOW__WEBSERVER__RBAC=True
      - AIRFLOW__WEBSERVER__AUTHENTICATE=True
      - AIRFLOW__WEBSERVER__AUTH_BACKENDS=airflow.contrib.auth.backends.password_auth
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    ports:
      - "8080:8080"
    depends_on:
      - mongo
    restart: always
Python Dependencies
The requirements.txt file includes the necessary Python packages:

requests
beautifulsoup4


DAG Details

The Airflow Directed Acyclic Graph (DAG) finn_scraper_dag consists of the following tasks:

Search New Ads: Fetches new real estate advertisements from Finn.no.
Scrape New Ads: Extracts detailed information from the fetched advertisements.
Process New Ads: Processes the scraped data for storage.
Check Existing Ads: Compares the processed data with existing records in MongoDB to avoid duplicates.
Upload New Ads: Inserts the new advertisements into the MongoDB database.
Accessing MongoDB
To access the MongoDB instance:

Connect via Mongo Shell:

bash

docker exec -it <container_id_or_name> mongo -u root -p root --authenticationDatabase admin
Connect via Python:

python

from pymongo import MongoClient

client = MongoClient('mongodb://root:root@localhost:27017/')
db = client['finn_data']
collection = db['real_estate']
Notes
Ensure that Docker and Docker Compose are installed and running on your machine.
The project uses the latest versions of MongoDB and Apache Airflow.
The default MongoDB username and password are both set to root.
The Airflow web interface is accessible at [http://localhost:808
