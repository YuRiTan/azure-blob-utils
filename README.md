# azure-blob-utils
Some commen functions used when working with azure blob storage. This package is intended to work alongside Azure's Python packages, providing some convenience functions.

## Requirements
- azure-identity
- azure-storage-blob

## Features
- **AzureBlobStorageConnector**: A connector class that allows you to `read`, `write` (or `overwrite`) files just like you would on your local machine using the Pythonic `open()` method.

## Getting started
In this example you can see how you can read/write parquet files from/to AzureBlobStorage.

```Python
connector = AzureBlobStorageConnector('<account_url'>, '<conainer_name>', '<optional_credential>')

# read some file (for example: Parquet) into memory
with connector.open('path/to/blob.parquet', 'r') as stream:
    df = pd.read_parquet(stream)

# write some dataframe to file(for example: Parquet)
with connector.open('path/to/blob.parquet', 'w') as stream:
    df.to_parquet(stream)
```

## Note: Authentication
You can use several types of (Azure) credentials. In the example above, if no credential is provided, the `DefaultAzureCredential` is used. There are several other types of credential classes that you can use as well. For more info, please check the [azure docs](https://docs.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python).

