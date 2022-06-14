# Expected context is repository root
# This makes cli folder is accessible for copy and install
# docker build -f . -t polygon-etl-airflow-tests ..

FROM python:3.6.10

WORKDIR /airflow

COPY requirements_test.txt requirements_test.txt
COPY airflow/requirements_local.txt requirements_local.txt
COPY airflow/requirements.txt requirements.txt

RUN pip install \
    --upgrade pip \
    -r requirements_test.txt \
    -r requirements_local.txt

COPY cli ../cli
RUN pip install \
    -e ../cli \
    -r requirements.txt

COPY airflow/tests tests
COPY airflow/dags dags
ENTRYPOINT pytest -vv
