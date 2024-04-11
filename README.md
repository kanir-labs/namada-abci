# Namada ABCI client

Supports all Namada RPC abci queries and handles it with comfortable Python interface and types

Supports all sub-queries for:
- /shell/*
- /vp/pos/*
- /vp/token/*
- /vp/governance/*
- /vp/pgf/*

## Usage

```python
from namada_abci import NamadaABCIClient
rpc_url = '<your-rpc-url>'
client = NamadaABCIClient(rpc_url)
address = '<your-account-address'
print(client.epoch()) # returns current epoch as int
print(client.is_validator(address)) # returns bool
print(client.is_steward(address)) # returns bool
print(client.is_public_key_revealed(address)) # returns bool
```