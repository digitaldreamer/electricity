import os
import sys
import boto

from dateutil import tz
from datetime import datetime
from boto.exception import NoAuthHandlerFound, S3ResponseError
from boto.s3.cors import CORSConfiguration
from boto.s3.key import Key
from electricity.backends import BaseCDN


class AmazonCDN(BaseCDN):
    base_path = ''
    bucket_name = ''
    _cdn = None
    _bucket = None

    def __init__(self, base_path, bucket_name):
        self.base_path = base_path
        self.bucket_name = bucket_name

        # initialize the bucket
        try:
            self._cdn = boto.connect_s3()
        except NoAuthHandlerFound:
            return
        else:
            self._bucket = AmazonCDN.get_or_create_bucket(self._cdn, bucket_name)

    @classmethod
    def get_or_create_bucket(cls, cdn, name):
        """
        Get or create bucket from the CDN
        """
        bucket = cls.get_bucket(cdn, name)

        if not bucket:
            bucket = cls.create_bucket(cdn, name)

        return bucket

    @classmethod
    def get_bucket(cls, cdn, name):
        """
        Get a bucket from the CDN
        """
        try:
            bucket = cdn.get_bucket(name)
        except S3ResponseError:
            bucket = None

        return bucket

    @classmethod
    def create_bucket(cls, cdn, name):
        """
        Create the bucket in the CDN
        """
        try:
            bucket = cdn.create_bucket(name)
        except S3ResponseError:
            bucket = None
        else:
            # set permisssions
            cors_config = CORSConfiguration()
            cors_config.add_rule('GET', '*')

            bucket.set_cors(cors_config)
            bucket.set_acl('public-read')

        return bucket

    @classmethod
    def delete_bucket(cls, cdn, name):
        """
        Remove the bucket in the CDN
        """
        try:
            cdn.delete_bucket(name)
        except S3ResponseError:
            return False

        return True

    def _get_key(self, key):
        """
        Get key from CDN
        """
        return self._bucket.get_key(key)

    def sync(self):
        """
        Push new assets to CDN
        """
        for root, dirs, files in os.walk(self.base_path):
            relative_path = root.replace(self.base_path, '')

            for filename in files:
                file_path = os.path.join(root, filename)
                filename = os.path.relpath(file_path, self.base_path)

                # check for changes
                original_key = self._get_key(filename)

                if original_key:
                    # TODO: figure out how to use timestamps better
                    utc_zone = tz.tzutc()
                    local_zone = tz.tzlocal()
                    original_last_modified = boto.utils.parse_ts(original_key.last_modified)
                    last_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                    last_modified = last_modified.replace(tzinfo=local_zone)

                    # for now use the MD5 to check for changes on the file
                    if original_key.etag.strip('"') != original_key.compute_md5(open(file_path))[0]:
                        self.upload(filename, file_path)

                elif filename.find('DS_Store') == -1:
                    self.upload(filename, file_path)

    def upload(self, filename, file_path):
        """
        Upload a file to the CDN
        """
        key = Key(self._bucket)
        key.key = filename
        key.set_contents_from_filename(file_path)
        self._bucket.set_acl('public-read', key.key)

    def flush(self):
        """
        Remove all assets from CDN
        """
        for key in self._bucket.list():
            self._bucket.delete_key(key.key)

    def put(self):
        """
        Push all files to the CDN
        """
        for root, dirs, files in os.walk(self.base_path):
            relative_path = root.replace(self.base_path, '')

            for filename in files:
                file_path = os.path.join(root, filename)
                filename = os.path.relpath(file_path, self.base_path)
                self.upload(filename, file_path)

    def download(self, download_path):
        return
