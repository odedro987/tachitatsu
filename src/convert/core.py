import kotatsu.helpers as kotatsu
from kotatsu.model import (
    Manga as KotatsuManga,
    FavoritesEntry,
    HistoryRecord,
)
from kotatsu.core import KotatsuBackup
from tachiyomi.model import Manga as TachiyomiManga
from tachiyomi.core import TachiyomiBackup
import json


def to_kotatsu_source(ty_source) -> str:
    if ty_source == "Mangakakalot":
        return "MANGAKAKALOTTV"
    if ty_source == "Comick":
        return "COMICK_FUN"
    return ty_source.upper()


def to_kotatsu_url(ty_source: str, ty_url: str) -> str:
    if ty_source == "MangaDex":
        return ty_url.replace("/manga/", "").replace("/title/", "")
    if ty_source == "Mangakakalot":
        return ty_url.replace("https://chapmanganato.to/", "/manga/")
    if ty_source == "Comick":
        return ty_url.replace("/comic/", "")
    return ty_url


def to_kotatsu_chapter_url(ty_source: str, ty_url: str) -> str:
    if ty_source == "MangaDex":
        return ty_url.replace("/chapter/", "")
    if ty_source == "Mangakakalot":
        return ty_url.replace("https://chapmanganato.to/", "/chapter/")
    if ty_source == "Comick":
        return ty_url.replace("/comic/", "")
    return ty_url


def to_kotatsu_public_url(ty_source: str, kt_url: str) -> str:
    if ty_source == "MangaDex":
        return "https://mangadex.org/title/" + kt_url
    if ty_source == "Mangakakalot":
        return "https://ww7.mangakakalot.tv" + kt_url
    if ty_source == "Comick":
        return "https://comick.cc/comic/" + kt_url
    return kt_url


def to_kotatsu_id(ty_source: str, ty_url: str) -> int:
    return kotatsu.get_kotatsu_id(
        to_kotatsu_source(ty_source) + to_kotatsu_url(ty_source, ty_url)
    )


def to_kotatsu_chapter_id(ty_source: str, ty_url: str) -> int:
    return kotatsu.get_kotatsu_id(
        to_kotatsu_source(ty_source) + to_kotatsu_chapter_url(ty_source, ty_url)
    )


def to_kotatsu_status(ty_status: int) -> str:
    if ty_status == 1:
        return "ONGOING"
    if ty_status == 2 or ty_status == 4:
        return "FINISHED"
    if ty_status == 5:
        return "ABANDONED"
    if ty_status == 6:
        return "PAUSED"
    return ""


def to_kotatsu_manga(ty_manga: TachiyomiManga, ty_source: str) -> KotatsuManga:
    kotatsu_url = to_kotatsu_url(ty_source, ty_manga.url)
    return KotatsuManga(
        to_kotatsu_id(ty_source, ty_manga.url),
        ty_manga.title,
        None,
        kotatsu_url,
        to_kotatsu_public_url(ty_source, kotatsu_url),
        -1.0,
        False,
        ty_manga.thumbnail,
        None,
        to_kotatsu_status(ty_manga.status),
        ty_manga.author,
        to_kotatsu_source(ty_source),
        [],
    )


def to_kotatsu_favorite(
    ty_manga: TachiyomiManga, kt_manga: KotatsuManga
) -> FavoritesEntry:
    return FavoritesEntry(
        kt_manga.id,
        1,
        0,
        ty_manga.date_added,
        0,
        kt_manga.__dict__,
    )


def to_kotatsu_history(
    ty_manga: TachiyomiManga, ty_source: str, kt_manga: KotatsuManga
) -> HistoryRecord:
    latest_chapter, newest_chapter = ty_manga.get_latest_and_newest_chapter()
    if latest_chapter == None:
        return None

    chapter_id = to_kotatsu_chapter_id(ty_source, latest_chapter.url)
    return HistoryRecord(
        kt_manga.id,
        ty_manga.date_added,
        ty_manga.date_added,
        chapter_id,
        latest_chapter.last_page,
        0,
        (
            latest_chapter.number / newest_chapter.number
            if newest_chapter.number > 0
            else 0
        ),
        kt_manga.__dict__,
    )


def to_kotatsu_backup(ty_backup: TachiyomiBackup) -> KotatsuBackup:
    favorites = []
    history = []
    total = len(ty_backup.data.mangaList)
    for i, manga in enumerate(ty_backup.data.mangaList):
        manga_src = ty_backup.sources[manga.source]
        kotatsu_manga = to_kotatsu_manga(manga, manga_src)
        favorites.append(to_kotatsu_favorite(manga, kotatsu_manga).__dict__)
        history_entry = to_kotatsu_history(manga, manga_src, kotatsu_manga)
        if history_entry != None:
            history.append(history_entry.__dict__)
        print("{:.2f}%".format(((i + 1) / total) * 100))
    return KotatsuBackup(favorites, history)
