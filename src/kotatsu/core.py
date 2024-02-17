from dataclasses import dataclass
from kotatsu.model import FavoritesEntry, HistoryRecord
import json
import zipfile
import os
from datetime import datetime


@dataclass
class KotatsuBackup:
    favorites: list[FavoritesEntry]
    history: list[HistoryRecord]

    def create_backup(self):
        os.makedirs("output")

        with open("output/favourites", encoding="utf-8", mode="w") as f:
            f.write(json.dumps(self.favorites))

        with open("output/history", encoding="utf-8", mode="w") as f:
            f.write(json.dumps(self.history))

        today = datetime.now().strftime("%d%m%Y")
        with zipfile.ZipFile(f"output/tachiyomi_to_kotatsu_{today}.bk", "a") as file:
            file.write("output/favourites", "favourites")
            file.write("output/history", "history")

        if os.path.exists("output/favourites"):
            os.remove("output/favourites")

        if os.path.exists("output/history"):
            os.remove("output/history")
