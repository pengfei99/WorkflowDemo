from typing import Tuple

from src.storage.S3StorageEngine import S3StorageEngine


def get_local_input_file_path(remote_file_path: str, data_folder: str) -> Tuple[str, str]:
    file_name = S3StorageEngine.get_short_file_name(remote_file_path)
    return f"{data_folder}/{file_name}", file_name
