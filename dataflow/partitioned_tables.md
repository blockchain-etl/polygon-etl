# Partitioned Tables

Generate all partitioned table prefixes:

```python
hex_chars = '0123456789abcdef'

f = open('out.txt', 'w')

f.write(f'empty\n')

for hex_char1 in hex_chars:
    for hex_char2 in hex_chars:
        for hex_char3 in hex_chars:
            f.write(f'0x{hex_char1}{hex_char2}{hex_char3}\n')
```

For each of the rows in `out.txt` run these commands in BigQuery (
make sure to replace `<project>` with your project and `$1` with a row from `out.txt`):

```sql
CREATE TABLE IF NOT EXISTS `<project>.crypto_polygon_partitioned.logs_by_topic_$1`
(
log_index INT64,
transaction_hash STRING,
transaction_index INT64,
address STRING,
data STRING,
topics ARRAY<STRING>,
block_timestamp TIMESTAMP,
block_number INT64,
block_hash STRING
)
PARTITION BY TIMESTAMP_TRUNC(block_timestamp, HOUR)
OPTIONS(partition_expiration_days=7);

CREATE TABLE IF NOT EXISTS `<project>.crypto_polygon_partitioned.traces_by_input_$1`
(
transaction_hash STRING,
transaction_index INT64,
from_address STRING,
to_address STRING,
value NUMERIC,
input STRING,
output STRING,
trace_type STRING,
call_type STRING,
reward_type STRING,
gas INT64,
gas_used INT64,
subtraces INT64,
trace_address STRING,
error STRING,
status INT64,
block_timestamp TIMESTAMP,
block_number INT64,
block_hash STRING,
trace_id STRING,
)
PARTITION BY TIMESTAMP_TRUNC(block_timestamp, HOUR)
OPTIONS(partition_expiration_days=7);
```

Verify the number of tables (should be 8194):

```sql
SELECT *
FROM `<project>.crypto_polygon_partitioned.__TABLES__`
```
