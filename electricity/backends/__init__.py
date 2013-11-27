import abc


class BaseCDN(object):
    base_path = ''
    build_path = ''
    bucket_name = ''
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create_bucket(self, name):
        """
        Create the bucket in the CDN
        """
        return

    @abc.abstractmethod
    def delete_bucket(self, name):
        """
        Remove the bucket in the CDN
        """
        return

    @abc.abstractmethod
    def upload(self, filename, file_path):
        """
        Upload a file to the CDN
        """
        return

    @abc.abstractmethod
    def sync(self):
        """
        Push new assets to the CDN
        """
        return

    @abc.abstractmethod
    def flush(self):
        """
        Remove all assets from the CDN
        """
        return

    @abc.abstractmethod
    def put(self):
        """
        Push all assets to the CDN
        """
        return

    @abc.abstractmethod
    def download(self, download_path):
        """
        Download all assets from the CDN
        """
        return
