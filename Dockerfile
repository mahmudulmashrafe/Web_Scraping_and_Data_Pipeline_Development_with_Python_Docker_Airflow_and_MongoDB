ARG AIRFLOW_VERSION="slim-latest"
ARG PYTHON_VERSION="3.10"
FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION}

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends\
    vim gcc libpq-dev python3-dev libcurl4-openssl-dev libssl-dev\
    build-essential wget\
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list
RUN apt-get -y update && apt-get install -y apt-transport-https
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

USER airflow
RUN python -m pip install --upgrade pip
RUN pip install setuptools==57.5.0
RUN pip install psycopg2
RUN mkdir -p ${AIRFLOW_HOME}/logs

ARG PY_VERSION="3.10"
RUN echo ${PYTHON_VERSION}

ARG CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PY_VERSION}.txt"
RUN pip install --no-cache-dir "apache-airflow[async,celery,redis,amazon,mongo,ssh]==${AIRFLOW_VERSION}" \
    --constraint ${CONSTRAINT_URL}

RUN pip install --no-cache-dir -r requirements.txt
CMD ["airflow", "db", "upgrade"]
