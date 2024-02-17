import kotatsu.helpers as kotatsu
import tachiyomi.helpers as tachi
from kotatsu.model import (
    Manga as KotatsuManga,
    FavoritesEntry,
    HistoryRecord,
)
from kotatsu.core import KotatsuBackup
from tachiyomi.model import Manga as TachiyomiManga
from tachiyomi.core import TachiyomiBackup
import json

SOURCES_MAP = {"MangaDex": "MANGADEX", "Mangakakalot": "MANGAKAKALOTTV"}


def to_kotatsu_url(ty_source: str, ty_url: str) -> str:
    if ty_source == "MangaDex":
        return ty_url.replace("/manga/", "").replace("/title/", "")
    if ty_source == "Mangakakalot":
        return ty_url.replace("https://chapmanganato.to/", "/manga/")
    return ty_url


def to_kotatsu_chapter_url(ty_source: str, ty_url: str) -> str:
    if ty_source == "MangaDex":
        return ty_url.replace("/chapter/", "")
    if ty_source == "Mangakakalot":
        return ty_url.replace("https://chapmanganato.to/", "/chapter/")
    return ty_url


def to_kotatsu_public_url(ty_source: str, ty_url: str) -> str:
    if ty_source == "MangaDex":
        return "https://mangadex.org/title/" + ty_url
    if ty_source == "Mangakakalot":
        return "https://ww7.mangakakalot.tv" + ty_url
    return ty_url


def to_kotatsu_id(ty_source: str, ty_url: str) -> int:
    return kotatsu.get_kotatsu_id(
        SOURCES_MAP[ty_source] + to_kotatsu_url(ty_source, ty_url)
    )


def to_kotatsu_chapter_id(ty_source: str, ty_url: str) -> int:
    return kotatsu.get_kotatsu_id(
        SOURCES_MAP[ty_source] + to_kotatsu_chapter_url(ty_source, ty_url)
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


def to_kotatsu_manga(ty_manga: TachiyomiManga) -> KotatsuManga:
    ty_src = tachi.get_source_name(ty_manga.source)
    kotatsu_url = to_kotatsu_url(ty_src, ty_manga.url)
    return KotatsuManga(
        to_kotatsu_id(ty_src, ty_manga.url),
        ty_manga.title,
        None,
        kotatsu_url,
        to_kotatsu_public_url(ty_src, kotatsu_url),
        -1.0,
        False,
        ty_manga.thumbnail,
        None,
        to_kotatsu_status(ty_manga.status),
        ty_manga.author,
        SOURCES_MAP[ty_src],
        [],
    )


def to_kotatsu_favorite(
    ty_manga: TachiyomiManga, kt_manga: KotatsuManga
) -> FavoritesEntry:
    ty_src = tachi.get_source_name(ty_manga.source)
    return FavoritesEntry(
        kt_manga.id,
        1,
        0,
        ty_manga.date_added,
        0,
        kt_manga.__dict__,
    )


def to_kotatsu_history(
    ty_manga: TachiyomiManga, kt_manga: KotatsuManga
) -> HistoryRecord:
    ty_src = tachi.get_source_name(ty_manga.source)
    latest_chapter, newest_chapter = ty_manga.get_latest_and_newest_chapter()
    chapter_id = (
        to_kotatsu_chapter_id(ty_src, latest_chapter.url)
        if latest_chapter != None
        else 0
    )
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
    for manga in ty_backup.data.mangaList:
        kotatsu_manga = to_kotatsu_manga(manga)
        favorites.append(to_kotatsu_favorite(manga, kotatsu_manga).__dict__)
        history.append(to_kotatsu_history(manga, kotatsu_manga).__dict__)
    return KotatsuBackup(favorites, history)
