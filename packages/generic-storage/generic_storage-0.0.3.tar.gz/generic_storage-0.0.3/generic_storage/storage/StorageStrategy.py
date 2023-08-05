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
        with open(local_destination, 'wb') as dest:
            for chunk in self._read_as_chunk(src_path, 8192):
                dest.write(chunk)
        return local_destination

    @abstractmethod
    def _read(self, path):
        pass

    @abstractmethod
    def _read_as_chunk(self, path, chunk_size):
        pass
