from abc import ABC, abstractmethod
import os
import tempfile


class StorageStrategy(ABC):

    def __init__(self):
        self._cache = {}

    def read(self, path):
        if path not in self._cache:
            content = self._read(path)
            self._cache[path] = content
        return self._cache[path]

    def download(self, src_path):
        local_destination = "{}/{}".format(
            tempfile.gettempdir(),
            os.path.basename(src_path)
        )
        with open(local_destination, 'w') as dest:
            redshift_cert = self._read(src_path)
            dest.write(redshift_cert)
        return local_destination

    @abstractmethod
    def _read(self, path):
        pass
