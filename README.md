# azure-blob-utils
Some functions used when working with azure blob storage

## Getting started

First, reading blobs into memory / writing memory objects to blobs:

```Python
credential = InteractiveBrowserCredential()
connector = AzureBlobStorageConnector('<account_url'>, '<conainer_name>', credential)

# read some file (for example: Parquet) into memory
with connector.open('path/to/blob.parquet', 'r') as stream:
    df = pd.read_parquet(stream)

# write some dataframe to file(for example: Parquet)
with connector.open('path/to/blob.parquet', 'w') as stream:
    df.to_parquet(stream)
```

## Note: Authentication
You can use several types of (Azure) credentials. In the example above, the `InteractiveBrowserCredential()` is used. There are several other types of credential classes that you can use as well. For more info, please check the [azure docs](https://docs.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python).

