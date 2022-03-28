import os
import sys

from src.log.LogManager import LogManager
from src.storage.S3StorageEngine import S3StorageEngine

my_logger = LogManager(__name__).get_logger()
my_logger.debug("Init ingest_source_data")


def main():
    if len(sys.argv) != 3:
        my_logger.error(
            'Number of arguments that you give is wrong, please enter the path of the file which you want to analyze.')
    else:
        remote_file_path = sys.argv[1]
        data_folder = sys.argv[2]
    endpoint = "https://" + os.getenv("AWS_S3_ENDPOINT")
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    session_token = os.getenv("AWS_SESSION_TOKEN")
    storage_engine = S3StorageEngine(endpoint, access_key, secret_key, session_token)
    file_name = storage_engine.get_short_file_name(remote_file_path)
    dest_file_path = f"{data_folder}/{file_name}"
    if storage_engine.download_data(remote_file_path, dest_file_path):
        my_logger.info(f"Downloading data from {remote_file_path} to {dest_file_path}")
    else:
        my_logger.error(f"fail to download data from {remote_file_path}")


if __name__ == "__main__":
    main()
