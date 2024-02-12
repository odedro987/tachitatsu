import gzip
from dataclasses import dataclass
from tachiyomi.model import Backup


@dataclass
class TachiyomiBackup:
    filename: str

    def __gunzip(self):
        with gzip.open(self.filename, mode="rb") as bytes:
            return bytes.read()

    def read(self):
        return Backup().create_from_bytes(self.__gunzip())
