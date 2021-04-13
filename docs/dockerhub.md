# Uploading to Docker Hub

```bash
POLYGONETL_VERSION=0.0.1
docker build -t polygon-etl:${POLYGONETL_VERSION} -f Dockerfile .
docker tag polygon-etl:${POLYGONETL_VERSION} blockchainetl/polygon-etl:${POLYGONETL_VERSION}
docker push blockchainetl/polygon-etl:${POLYGONETL_VERSION}

docker tag polygon-etl:${POLYGONETL_VERSION} blockchainetl/polygon-etl:latest
docker push blockchainetl/polygon-etl:latest
```
