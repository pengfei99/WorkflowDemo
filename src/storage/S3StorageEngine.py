import os
import re
from typing import Optional

import boto3
from botocore.config import Config
from boto3 import exceptions
import logging
from botocore.exceptions import ClientError

from src.storage.ProgressPercentage import ProgressPercentage
from src.storage.StorageEngineInterface import StorageEngineInterface

log = logging.getLogger(__name__)


class S3StorageEngine(StorageEngineInterface):

    def __init__(self, endpoint: str, access_key: str, secret_key: str, session_token: str, region_name='us-east-1'):
        self.storage_engine_type = "s3"
        if session_token:
            self.s3_client = boto3.client('s3', endpoint_url=endpoint, aws_access_key_id=access_key,
                                          aws_secret_access_key=secret_key,
                                          aws_session_token=session_token,
                                          config=Config(signature_version='s3v4'),
                                          region_name=region_name)
        else:
            self.s3_client = boto3.client('s3', endpoint_url=endpoint, aws_access_key_id=access_key,
                                          aws_secret_access_key=secret_key,
                                          config=Config(signature_version='s3v4'),
                                          region_name=region_name)

    def upload_data(self, source_path: str, destination_path: str) -> bool:
        """

        :param source_path: The local data path include parent dir and file name
        :param destination_path: is the full s3 remote path that includes bucket_name and s3 object name. e.g.
                s3://pengfei/tmp/tmp_bkp.sql
        :return: return true if upload complete, return false if failed
        """
        try:
            bucket_name, object_name = self.parse_path(destination_path)
            return self.upload_file_to_s3(bucket_name, object_name, source_path, delete_origin=True)
        except ValueError as e:
            log.error(e)
            return False

    def download_data(self, source_path: str, destination_path: str) -> bool:
        try:
            bucket_name, bucket_key = self.parse_path(source_path)
            return self.download_file_from_s3(bucket_name, bucket_key, destination_path)
        except ValueError as e:
            log.error(e)
            return False

    def list_dir(self, source_path: str) -> Optional[list]:

        bucket_name, bucket_key = self.parse_path(source_path)
        try:
            s3_objects = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=bucket_key)
            content_list = [s3_content['Key'] for s3_content in s3_objects['Contents']]
        except exceptions as e:
            log.exception(f"can't list content for the giving path {source_path}. {e}")
            return None
        return content_list

    def get_storage_engine_type(self) -> str:
        return self.storage_engine_type

    def get_short_file_name(self, file_name: str):
        return file_name.split("/")[-1]

    @staticmethod
    def parse_path(path: str):
        # note the path must have the format protocol://{bucket_name}/{bucket_key}
        # for example s3a://user-pengfei/tmp/sparkcv/input is a valid path for S3StorageEngine
        s3_path_pattern = "^s3[a-z]?://([^/]+)/(.*?([^/]+)/?)$"
        if re.match(s3_path_pattern, path):
            short_path = path.split("//")[-1]
            index = short_path.index("/")
            bucket_name = short_path[0:index]
            bucket_key = short_path[index + 1:]
            return bucket_name, bucket_key
        else:
            log.error("The given s3 path is not a validate path")
            raise ValueError

    @staticmethod
    def build_s3_object_key(source_file_path: str, bucket_key: str):
        # build n s3 object key based on the given source file path and bucket key
        source_file_name = os.path.basename(source_file_path)
        return f"{bucket_key}/{source_file_name}"

    def write_byte_to_s3(self, bucket_name: str, bucket_key: str, data):
        """
        It writes input data in byte to a s3 bucket with given bucket name and key

        :param bucket_name: The name of the bucket that you want to write
        :param bucket_key: The destination path of the data relative to the bucket name
        :param data: The data in byte that you want to write to s3
        :return: None
        """
        # # set the path of where you want to put the object
        # s3_object = self.s3_client.Object(bucket_name, bucket_key)
        # # set the content which you want to write
        # s3_object.put(Body=data)
        self.s3_client.put_object(Bucket=bucket_name, Key=bucket_key, Body=data)

    def upload_file_to_s3(self, bucket_name: str, object_name: str, source_file_path, delete_origin=False) -> bool:
        """
        Upload a file to an AWS S3 bucket. It will extract the origin file name from the source path, and concat it
        with the given bucket to form the final s3 object name.

        :param bucket_name: The name of the bucket that you want to write
        :param object_name: The full path of the data relative to the bucket name.
        :param source_file_path: indicates the source file path, all files under the path will be uploaded to s3
        :param delete_origin: default value is False. If set to True, after upload, the source file will be deleted.
        :return: None
        """
        try:
            self.s3_client.upload_file(source_file_path, bucket_name, object_name,
                                       Callback=ProgressPercentage(source_file_path))
        except ClientError as e:
            log.error(e)
            return False
        if delete_origin:
            os.remove(source_file_path)
        return True

    def upload_file_to_s3_with_origin_file_name(self, bucket_name: str, bucket_key: str, source_file_path,
                                                delete_origin=False) -> bool:
        """
        Upload a file to an AWS S3 bucket. It will extract the origin file name from the source path, and concat it
        with the given bucket to form the final s3 object name.

        :param bucket_name: The name of the bucket that you want to write
        :param bucket_key: The destination path of the data relative to the bucket name. It's the parent dir of
                           the uploaded file
        :param source_file_path: indicates the source file path, all files under the path will be uploaded to s3
        :param delete_origin: default value is False. If set to True, after upload, the source file will be deleted.
        :return: None
        """
        s3_object_name = self.build_s3_object_key(source_file_path, bucket_key)
        try:
            self.s3_client.upload_file(source_file_path, bucket_name, s3_object_name,
                                       Callback=ProgressPercentage(source_file_path))
        except ClientError as e:
            log.error(e)
            return False
        if delete_origin:
            os.remove(source_file_path)
        return True

    def download_file_from_s3(self, bucket_name: str, bucket_key: str, dest_path) -> bool:
        """
        Download a file to an AWS S3 bucket.

        :param bucket_name: The name of the bucket that you want to write
        :param bucket_key: The destination path of the data relative to the bucket name
        :param dest_path: indicates the destination file path.
        :return: None
        """
        try:
            self.s3_client.download_file(bucket_name, bucket_key, dest_path)
        except Exception as e:
            log.exception(e)
            return False
        return True

# The difference between upload-file and put_object in boto3
#
# The upload_file method is handled by the S3 Transfer Manager, this means that it will automatically handle
# multipart uploads behind the scenes for you, if necessary.
#
# The put_object method maps directly to the low-level S3 API request. It does not handle multipart uploads for you.
# It will attempt to send the entire body in one request.

# The difference between s3:// and (s3n/s3a):// is that s3 is a block-based overlay on top of Amazon S3,
# while s3n/s3a are not (they are object-based).
#
# The difference between s3n and s3a is that s3n supports objects up to 5GB in size, while s3a supports objects up
# to 5TB and has higher performance (both are because it uses multi-part upload). s3a is the successor to s3n.
