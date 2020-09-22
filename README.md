# azure-blob-utils
Some functions used when working with azure blob storage

## Getting started

First, reading blobs into memory / writing memory objects to blobs:

```Python
connector = AzureBlobStorageConnector('<account_url'>, '<conainer_name>')

# read some file (for example: Parquet) into memory
with connector.open('path/to/blob.file', 'r') as stream:
    df = pd.read_parquet(stream)

# write some dataframe to file(for example: Parquet)
with connector.open('path/to/blob.file', 'w') as stream:
    df.to_parquet(stream)
```

NOTE: Authentication is done via Azure's `InteractiveBrowserCredential`.

