import gzip
from tachiyomi.model import Backup


class SourceNotFound(Exception):
    pass


class TachiyomiBackup:
    def __init__(self, filename: str):
        with gzip.open(filename, mode="rb") as bytes:
            self.data = Backup().create_from_bytes(bytes.read())
        self.sources = {item.id: item.name for item in self.data.sources}
