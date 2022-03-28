import abc
from typing import Optional


class StorageEngineInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'upload_data') and
                callable(subclass.upload_data) and
                hasattr(subclass, 'download_data') and
                callable(subclass.download_data) and
                hasattr(subclass, 'list_dir') and
                callable(subclass.list_dir) and
                hasattr(subclass, 'get_storage_engine_type') and
                callable(subclass.get_storage_engine_type) and
                hasattr(subclass, 'get_short_file_name') and
                callable(subclass.get_short_file_name)
                or
                NotImplemented)

    @abc.abstractmethod
    def upload_data(self, source_path: str, destination_path: str) -> bool:
        """upload data from local storage to remote storage

        :param source_path: The path of source file
        :param destination_path: The path and name of the destination of the file after upload.
                       e.g s3a://pengfei/tmp/toto.txt is valid. s3a://pengfei/tmp is not. The uploaded file will be
                       renamed to tmp by using s3a://pengfei/tmp

        :return: true if upload succeed, false if failed
        """
        raise NotImplementedError

    @abc.abstractmethod
    def download_data(self, source_path: str, destination_path: str) -> bool:
        """download data from remote storage to local

        :param source_path: The path of source file
        :param destination_path: The path of the destination of the file after download
        :return: true if upload succeed, false if failed
        """
        raise NotImplementedError

    @abc.abstractmethod
    def list_dir(self, source_path: str) -> Optional[list]:
        """list the content of a directory

        :param source_path: The path for finding available backup
        :return: a list of available backup
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_storage_engine_type(self) -> str:
        """return the type of storage engine

        :return: the type of the storage engine, e.g. s3, local
        """
        raise NotImplementedError

    # move this method from DbRestoreBot to StorageEngine, because each storage has different definition for
    # file_name. In linux fs, the file_name of /tmp/sql_backup/2022-01-11_test_pg_bck.sql is 2022-01-11_test_pg_bck.sql
    # For s3, the file name (object key) of s3://pengfei/tmp/sql_backup/2022-01-11_test_pg_bck.sql is
    # tmp/sql_backup/2022-01-11_test_pg_bck.sql.
    # So we need to have one specific implementation for each StorageEngine
    @abc.abstractmethod
    def get_short_file_name(self, file_name: str):
        """
         This function extract the short file name from the s3 object key
        :param file_name: the raw file name for the storage engine
        :return:
        """

        raise NotImplementedError
