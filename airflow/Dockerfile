# Expected context is repository root
# This makes cli folder is accessible for copy and install
# docker build -f . -t polygon-etl-airflow-tests ..

FROM python:3.6.10

WORKDIR /airflow

COPY airflow/requirements_local.txt requirements_local.txt
RUN pip install --upgrade pip && \
    pip install -r requirements_local.txt

COPY cli ../cli
RUN pip install -e ../cli

COPY airflow/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY airflow/dags dags
CMD cd dags && \
    python -m pytest -vv
