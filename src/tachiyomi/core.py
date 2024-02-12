import gzip
from tachiyomi.model import Backup


class SourceNotFound(Exception):
    pass


class TachiyomiBackup(Backup):
    def __init__(self, filename: str):
        with gzip.open(filename, mode="rb") as bytes:
            self.data = Backup().create_from_bytes(bytes.read())

    def get_source_name(self, source_id: int) -> str:
        source = [s for s in self.data.sources if s.id == source_id]
        if len(source) != 1:
            raise SourceNotFound("source not found")
        return source[0].name
