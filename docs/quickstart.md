# Quickstart

Install Polygon ETL:

```bash
pip3 install polygon-etl
```

Export blocks and transactions:

```bash
> polygonetl export_blocks_and_transactions --start-block 0 --end-block 500000 \
--provider-uri https://mainnet.infura.io/v3/7aef3f0cd1f64408b163814b22cc643c --blocks-output blocks.csv --transactions-output transactions.csv
```

Export ERC20 and ERC721 transfers:

```bash
> polygonetl export_token_transfers --start-block 0 --end-block 500000 \
--provider-uri file://$HOME/Library/Ethereum/geth.ipc --output token_transfers.csv
```

Export traces:

```bash
> polygonetl export_traces --start-block 0 --end-block 500000 \
--provider-uri file://$HOME/Library/Ethereum/parity.ipc --output traces.csv
```

Stream blocks, transactions, logs, token_transfers continually to console:

```bash
> pip3 install polygon-etl[streaming]
> polygonetl stream --start-block 500000 -e block,transaction,log,token_transfer --log-file log.txt
```

Find all commands [here](commands.md).

---

To run the latest version of Ethereum ETL, check out the repo and call

```bash
> pip3 install -e .
> python3 polygonetl.py
```
