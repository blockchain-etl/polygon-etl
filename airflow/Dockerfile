FROM python:3.6.10

WORKDIR /airflow

COPY requirements_local.txt requirements_local.txt
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements_local.txt -r requirements.txt

COPY dags dags

CMD cd dags && \
    python -m pytest -vv
