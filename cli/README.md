# Polygon ETL CLI


Polygon ETL lets you convert blockchain data into convenient formats like CSVs and relational databases.


[Full documentation available here](http://polygon-etl.readthedocs.io/).

## Quickstart

Install Polygon ETL CLI:

```bash
pip3 install polygon-etl
```

Export blocks, actions and logs ([Schema](../docs/schema.md), [Reference](../docs/commands.md)):

```bash
> polygonetl export_blocks --start-block 1 --end-block 500000 \
--output-dir output --provider-uri grpcs://api.mainnet.polygon.one:443
```

---

Stream blocks, actions and logs to console ([Reference](../docs/commands.md#stream)):

```bash
> pip3 install polygon-etl[streaming]
> polygonetl stream --start-block 500000 -e block,action,log --log-file log.txt \
--provider-uri grpcs://api.mainnet.polygon.one:443
```

Find other commands [here](https://polygon-etl.readthedocs.io/en/latest/commands/).

For the latest version, check out the repo and call 
```bash
> pip3 install -e . 
> python3 polygonetl.py
```

## Useful Links

- [Schema](https://polygon-etl.readthedocs.io/en/latest/schema/)
- [Command Reference](https://polygon-etl.readthedocs.io/en/latest/commands/)
- [Documentation](https://polygon-etl.readthedocs.io/)

## Running Tests

```bash
> pip3 install -e .[dev,streaming]
> export POLYGONETL_PROVIDER_URI=grpcs://api.mainnet.polygon.one:443
> pytest -vv
```

### Running Tox Tests

```bash
> pip3 install tox
> tox
```

## Running in Docker

1. Install Docker https://docs.docker.com/install/

2. Build a docker image
        
        > docker build -t polygon-etl:latest .
        > docker image ls
        
3. Run a container out of the image

        > docker run -v $HOME/output:/polygon-etl/output polygon-etl:latest export_blocks -s 1 -e 5499999 -b 1000 -o out

4. Run streaming to console or Pub/Sub

        > docker build -t polygon-etl:latest -f Dockerfile .
        > echo "Stream to console"
        > docker run polygon-etl:latest stream --start-block 500000 --log-file log.txt
        > echo "Stream to Pub/Sub"
        > docker run -v /path_to_credentials_file/:/polygon-etl/ --env GOOGLE_APPLICATION_CREDENTIALS=/polygon-etl/credentials_file.json polygon-etl:latest stream --start-block 500000 --output projects/<your-project>/topics/mainnet

