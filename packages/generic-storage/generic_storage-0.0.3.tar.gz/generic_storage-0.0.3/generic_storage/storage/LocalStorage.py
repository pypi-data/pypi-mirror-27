from .StorageStrategy import StorageStrategy

class LocalStorage(StorageStrategy):
    def _read(self, path):
        content = None
        with open(path, 'r') as src:
            content = src.read()
        return content

    def _read_as_chunk(self, path, chunk_size):
        with open(path, 'rb') as src:
            while True:
                chunk = src.read(chunk_size)
                if chunk:
                    yield chunk
                else:
                    break
