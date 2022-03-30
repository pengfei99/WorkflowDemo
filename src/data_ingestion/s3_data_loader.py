import os
import sys

from src.log.LogManager import LogManager
from src.storage.S3StorageEngine import S3StorageEngine

my_logger = LogManager(__name__, enable_file_handler=True, log_file_path=os.getenv("LOG_PATH")).get_logger()
my_logger.debug("Init s3_data_loader")


def main():
    if len(sys.argv) != 4:
        my_logger.error(
            'Number of arguments that you give is wrong, please enter the path of the file which you want to analyze.')
        sys.exit(1)
    else:
        data_folder = sys.argv[1]
        source_file_name = sys.argv[2]
        destination_folder = sys.argv[3]

    endpoint = "https://" + os.getenv("AWS_S3_ENDPOINT")
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    session_token = os.getenv("AWS_SESSION_TOKEN")
    storage_engine = S3StorageEngine(endpoint, access_key, secret_key, session_token)
    source_file_path = f"{data_folder}/{source_file_name}"
    destination_file_path = f"{destination_folder}/{source_file_name}"
    if storage_engine.upload_data(source_file_path, destination_file_path):
        my_logger.info(f"Data {source_file_path} has been uploaded to {destination_file_path}")
    else:
        my_logger.error(f"Fail to upload data {source_file_path} to {destination_file_path}")


if __name__ == "__main__":
    main()
