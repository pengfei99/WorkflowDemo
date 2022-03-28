import logging
import os
import shutil
from typing import Optional

from src.storage.StorageEngineInterface import StorageEngineInterface

log = logging.getLogger(__name__)


class LocalStorageEngine(StorageEngineInterface):
    def __init__(self):
        self.storage_engine_type = "local"

    def upload_data(self, source_path: str, destination_path: str) -> bool:
        return self.move_file(source_path, destination_path)

    def download_data(self, source_path: str, destination_path: str) -> bool:
        return self.move_file(source_path, destination_path)

    def list_dir(self, source_path: str) -> Optional[list]:
        try:
            backup_list = [f for f in os.listdir(source_path) if os.path.isfile(os.path.join(source_path, f))]
        except FileNotFoundError:
            log.error(f'Could not found {source_path} when searching for backups.'
                      f'Check your .config file settings')
            return None
        return backup_list

    def get_storage_engine_type(self) -> str:
        return self.storage_engine_type

    def get_short_file_name(self, file_name: str):
        return file_name

    @staticmethod
    def move_file(source_path: str, destination_path: str):
        if source_path == destination_path:
            return True
        else:
            try:
                shutil.copy(source_path, destination_path)
            except Exception as e:
                log.exception(e)
                return False
            return True
