from typing import BinaryIO, Optional, Generator
from contextlib import contextmanager
from io import BytesIO

from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient, StorageStreamDownloader


DEFAULT_CREDENTIAL = DefaultAzureCredential(
    exclude_interactive_browser_credential=False
)


class AzureBlobStorageConnector:
    """Connector class that contains Azure's Container client, and works as an
    interface to read/write from/to files on AzureBlobStorage.
    """
    def __init__(self, 
                 account_url: str, 
                 container_name: str, 
                 credential: Optional[any] = None) -> None:
        """ Setting up the `AzureBlobStorageConnector` by initializing a 
        containerclient and credential.

        Parameters
        ----------
        account_url: str
            Account url used in the `azure.storage.blob.ContainerClient`.
        container_name: str
            Name of the container used in the 
            `azure.storage.blob.ContainerClient`.
        credential: Optional[any]
            Credential instance of some credential class provided by the 
            `azure.identity` package.
        """
        self.account_url = account_url
        self.container_name = container_name

        # Will use InteractiveBrowserCredential if all others fail
        self.credential = credential or DEFAULT_CREDENTIAL

        self.container_client = ContainerClient(self.account_url,
                                                self.container_name,
                                                credential=self.credential)

    def download_blob(self, blob_path: str, dest_path: str) -> None:
        """Downloads as blob from AzureBlobStorage to a file on your local
        filesystem.

        Parameters
        ----------
        blob_path: str
            Filepath (relative to container root) of the file you want to
            download.
        dest_path: str
            (local) path to the file you want to store it.
        """
        blob_client = self.container_client.get_blob_client(blob_path)
        with open(dest_path, "wb") as f:
            blob_client.download_blob().readinto(f)

    @contextmanager
    def download_stream(self, blob_path: str) -> BytesIO:
        """Downloads a blob as BytesIO stream. This stream can then be used
        to load a DataFrame directly into (pandas) memory, without storing
        locally first.

        Usage:
        with connector.download_stream('path/to/file.ext') as stream:
            df = pd.read_parquet(stream)

        This way the stream gets neatly created and closed afterwards.

        Parameters
        ----------
        blob_path: str
            filepath (relative to container root) from the file to download.

        Yields
        ------
        : BytesIO
            Stream which allows to load directly into memory.
        """
        stream = BytesIO()
        blob_client = self.container_client.get_blob_client(blob_path)
        blob_client.download_blob().readinto(stream)
        yield stream
        logger.debug('Closing stream...')
        stream.close()

    def upload_blob(self, 
                    source_path: str, 
                    blob_path: str, 
                    overwrite: bool = False) -> None:
        """Uploads a local file to Azure Blob Storage

        Parameters
        ----------
        source_path: str
            (local) path to the file you want to upload.
        blob_path: str
            Filepath (relative to container root) of the file to be created.
        """
        blob_client = self.container_client.get_blob_client(blob_path)
        with open(source_path, 'rb') as f:
            blob_client.upload_blob(f, 
                                    blob_type="BlockBlob", 
                                    overwrite=overwrite)

    @contextmanager
    def upload_stream(self, blob_path: str, overwrite: bool = False) -> BytesIO:
        """Opens a byte-stream to write to using a context manager. The stream
        will write to a file on Azure Blob Storage specified by the `blob_path`.

        Usage:
        with connector.upload_stream('path/to/file.ext') as stream:
            df.to_parquet(stream)

        This way the stream gets neatly created and closed afterwards.

        Parameters
        ----------
        blob_path: str
            Filepath (relative to conainer root) of the file to be created.
        overwrite: bool (optional)
            Wheter or not to overwrite an existing file. If set to False and
            the blob already exists, will raise a ResourceExistsError. 
            Defaults to False

        Yields
        ------
        : BytesIO
            Stream which allows to load directly into memory.
        """
        stream = BytesIO()
        yield stream
        stream.seek(0)  # set pointer back to start of stream

        blob_client = self.container_client.get_blob_client(blob_path)
        blob_client.upload_blob(stream, 
                                blob_type="BlockBlob", 
                                overwrite=overwrite)

        logger.debug(f'Uploaded stream to {blob_path}. Closing stream...')
        stream.close()

    @contextmanager
    def open(self, blob_path: str, mode: str) -> Generator[BytesIO, None, None]:
        """Create a Python-like `open()` interface for downloading and uploading
        files from and to AzureBlobStorage.

        Usage:
        with connector.open('path/to/file.ext', 'r') as stream:
            df = pd.read_parquet(stream)
        

        Parameters
        ----------
        blob_path: str
            Filepath (relative to container root) of the file to be created.
        mode: str
            Like Python's `open()` function, the mode you want to open the file.

            Character Meaning
            --------- ----------------------------------------------------------
            'r'       open for reading, or downloading the stream.
            'w'       open for writing, or uploading the stream.
            'o'       open for overwriting, or delete file, and upload stream.
        """
        if mode.lower() == 'r':
            with self.download_stream(blob_path) as s:
                yield s
        elif mode.lower() == 'w':
            with self.upload_stream(blob_path, overwrite=False) as s:
                yield s
        elif mode.lower() == 'o':
            with self.upload_stream(blob_path, overwrite=True) as s:
                yield s
        else:
            raise ValueError(f'Unknown mode: {mode}.')

