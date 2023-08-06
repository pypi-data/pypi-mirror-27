import os
import logging

import boto3
import botocore
from tempfile import NamedTemporaryFile

from urllib.parse import urlparse
from .local import LocalStore

logger = logging.getLogger(__name__)
logging.getLogger('boto3').setLevel(logging.ERROR)
logging.getLogger('botocore').setLevel(logging.ERROR)
logging.getLogger('s3transfer').setLevel(logging.ERROR)


class S3:
    @staticmethod
    def rm_leading_slash(s):
        if s[0] == '/':
            return s[1:]
        return s

    @staticmethod
    def write(name, mode, index, processor):
        parsed_name = urlparse(name)

        bucket_name = parsed_name.netloc
        key = S3.rm_leading_slash(parsed_name.path)
        logger.info(f'putting {key} to s3 ({bucket_name})')

        with NamedTemporaryFile(delete=False) as f:
            temp_file = f.name

        logger.debug(f'writing to tempfile {temp_file} before uploading')
        LocalStore.write(temp_file, 'replace', index, processor)

        s3 = boto3.resource('s3')
        s3.meta.client.upload_file(temp_file, bucket_name, key, ExtraArgs={'ContentType': "application/json"})


    @staticmethod
    def read(path):
        parsed_name = urlparse(path)

        bucket_name = parsed_name.netloc
        key = S3.rm_leading_slash(parsed_name.path)

        s3 = boto3.resource('s3')
        with NamedTemporaryFile(delete=False) as f:
            temp_file = f.name

        try:
            s3.Bucket(bucket_name).download_file(key, temp_file)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise

        obj = LocalStore.read(temp_file)
        os.remove(temp_file)
        return obj
