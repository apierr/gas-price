# gas-price


### get pending txs

1. get pending transactions, price oracles, network stats and pools stats

```sh
python extract.py
```

2. load pending transactions in a DB

```sh
python load.py
```

3.  get **block_id** and **gas_used** from confirmed transactions

```sh
python extract_block.py
```
