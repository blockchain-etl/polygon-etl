# Expected context is repository root
# This makes cli folder is accessible for copy and install
# docker build -f ./Dockerfile -t polygon-etl-tests ..

FROM python:3.8.12

WORKDIR /app

RUN pip install --upgrade pip

COPY pytest.ini requirements_test.txt airflow/requirements* .

RUN pip install \
    -r requirements_test.txt \
    -r requirements_local.txt

COPY cli cli
RUN pip install \
    -e cli \
    -r requirements_airflow.txt

COPY airflow airflow
ENTRYPOINT pytest -vv
