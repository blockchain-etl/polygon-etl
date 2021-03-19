# Uploading to Docker Hub

```bash
MATICETL_VERSION=0.0.1
docker build -t matic-etl:${MATICETL_VERSION} -f Dockerfile .
docker tag matic-etl:${MATICETL_VERSION} blockchainetl/matic-etl:${MATICETL_VERSION}
docker push blockchainetl/matic-etl:${MATICETL_VERSION}

docker tag matic-etl:${MATICETL_VERSION} blockchainetl/matic-etl:latest
docker push blockchainetl/matic-etl:latest
```