# Uploading to Docker Hub

```bash
POLYGONETL_VERSION=0.0.1
docker build -t matic-etl:${POLYGONETL_VERSION} -f Dockerfile .
docker tag matic-etl:${POLYGONETL_VERSION} blockchainetl/matic-etl:${POLYGONETL_VERSION}
docker push blockchainetl/matic-etl:${POLYGONETL_VERSION}

docker tag matic-etl:${POLYGONETL_VERSION} blockchainetl/matic-etl:latest
docker push blockchainetl/matic-etl:latest
```
