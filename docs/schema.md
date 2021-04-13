# Schema

## blocks.csv

| Column            | Type       |
| ----------------- | ---------- |
| number            | bigint     |
| hash              | hex_string |
| parent_hash       | hex_string |
| nonce             | hex_string |
| sha3_uncles       | hex_string |
| logs_bloom        | hex_string |
| transactions_root | hex_string |
| state_root        | hex_string |
| receipts_root     | hex_string |
| miner             | address    |
| difficulty        | numeric    |
| total_difficulty  | numeric    |
| size              | bigint     |
| extra_data        | hex_string |
| gas_limit         | bigint     |
| gas_used          | bigint     |
| timestamp         | bigint     |
| transaction_count | bigint     |

---

## transactions.csv

| Column            | Type       |
| ----------------- | ---------- |
| hash              | hex_string |
| nonce             | bigint     |
| block_hash        | hex_string |
| block_number      | bigint     |
| transaction_index | bigint     |
| from_address      | address    |
| to_address        | address    |
| value             | numeric    |
| gas               | bigint     |
| gas_price         | bigint     |
| input             | hex_string |
| block_timestamp   | bigint     |

---

## token_transfers.csv

| Column           | Type       |
| ---------------- | ---------- |
| token_address    | address    |
| from_address     | address    |
| to_address       | address    |
| value            | numeric    |
| transaction_hash | hex_string |
| log_index        | bigint     |
| block_number     | bigint     |

---

## receipts.csv

| Column              | Type       |
| ------------------- | ---------- |
| transaction_hash    | hex_string |
| transaction_index   | bigint     |
| block_hash          | hex_string |
| block_number        | bigint     |
| cumulative_gas_used | bigint     |
| gas_used            | bigint     |
| contract_address    | address    |
| root                | hex_string |
| status              | bigint     |

---

## logs.csv

| Column            | Type       |
| ----------------- | ---------- |
| log_index         | bigint     |
| transaction_hash  | hex_string |
| transaction_index | bigint     |
| block_hash        | hex_string |
| block_number      | bigint     |
| address           | address    |
| data              | hex_string |
| topics            | string     |

---

- Might need to add `removed` to logs, which tells us if it was removed due to a chain re-org
