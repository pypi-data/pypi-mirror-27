from urllib.parse import urlparse
import logging
from .local import LocalStore
from .s3 import S3

logger = logging.getLogger(__name__)


class Store:
    @staticmethod
    def write(name, mode, index, processor):
        """
        :param name: name/path of the file
        :param mode:
        :param index:
        :param processor:
        :return:
        """
        scheme = urlparse(name).scheme

        if not scheme or scheme == "file":
            LocalStore.write(name, mode, index, processor)

        elif scheme == "s3":
            S3.write(name, mode, index, processor)

        else:
            logger.error(f'unknown scheme: {scheme}')

    @staticmethod
    def read(path):
        scheme = urlparse(path).scheme

        if not scheme or scheme == "file":
            return LocalStore.read(path)

        elif scheme == "s3":
            return S3.read(path)

        else:
            logger.error(f'unknown scheme: {scheme}')
