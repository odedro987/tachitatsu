import re
import time
from typing import Tuple, List, Any

import kotatsu.helpers as kotatsu
from kotatsu.model import (
    Manga as KotatsuManga,
    FavoritesEntry,
    HistoryRecord,
    Category as KotatsuCategory
)
from kotatsu.core import KotatsuBackup
from tachiyomi.model import (
    Manga as TachiyomiManga,
    Category as TachiyomiCategory
)
from tachiyomi.core import TachiyomiBackup
import json


def to_kotatsu_source(ty_source) -> str | None:
    if ty_source == "Mangakakalot":
        return "MANGAKAKALOTTV"
    if ty_source == "Comick":
        return "COMICK_FUN"
    if ty_source == "Hitomi":
        return "HITOMILA"
    if ty_source == "E-Hentai":
        return "EXHENTAI"
    if ty_source == "NHentai":
        return "NHENTAI"
    return None


def to_kotatsu_url(ty_source: str, ty_url: str) -> str | None:
    if ty_source == "MangaDex":
        return ty_url.replace("/manga/", "").replace("/title/", "")
    if ty_source == "Mangakakalot":
        return ty_url.replace("https://chapmanganato.to/", "/manga/")
    if ty_source == "Comick":
        return ty_url.replace("/comic/", "")
    if ty_source == "Hitomi":
        return ty_url[-12:-5]
    if ty_source == "E-Hentai":
        return ty_url[:22]
    if ty_source == "NHentai":
        return ty_url
    return None


def to_kotatsu_chapter_url(ty_source: str, ty_url: str) -> str | None:
    if ty_source == "MangaDex":
        return ty_url.replace("/chapter/", "")
    if ty_source == "Mangakakalot":
        return ty_url.replace("https://chapmanganato.to/", "/chapter/")
    if ty_source == "Comick":
        return ty_url.replace("/comic/", "")
    if ty_source == "Hitomi":
        return ty_url[-12:-5]
    if ty_source == "E-Hentai":
        return ty_url[:22]
    if ty_source == "NHentai":
        return ty_url
    return None


def to_kotatsu_public_url(ty_source: str, kt_url: str) -> str | None:
    if ty_source == "MangaDex":
        return "https://mangadex.org/title/" + kt_url
    if ty_source == "Mangakakalot":
        return "https://ww7.mangakakalot.tv" + kt_url
    if ty_source == "Comick":
        return "https://comick.cc/comic/" + kt_url
    if ty_source == "Hitomi":
        return "https://hitomi.la/g/" + kt_url
    if ty_source == "NHentai":
        return "https://nhentai.net" + kt_url
    return None


def to_kotatsu_id(kotatsu_source: str, kotatsu_url: str) -> int:
    return kotatsu.get_kotatsu_id(kotatsu_source + kotatsu_url)


def to_kotatsu_chapter_id(kotatsu_source: str, kotatsu_chapter_url: str) -> int:
    return kotatsu.get_kotatsu_id(kotatsu_source + kotatsu_chapter_url)


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


def to_kotatsu_manga(ty_manga: TachiyomiManga, ty_source: str) -> KotatsuManga | None:
    kotatsu_source = to_kotatsu_source(ty_source)
    kotatsu_url = to_kotatsu_url(ty_source, ty_manga.url)
    if kotatsu_url is None or kotatsu_source is None:
        return None
    return KotatsuManga(
        to_kotatsu_id(kotatsu_source, kotatsu_url),
        ty_manga.title,
        None,
        kotatsu_url,
        to_kotatsu_public_url(ty_source, kotatsu_url),
        -1.0,
        False,
        ty_manga.thumbnail,
        None,
        to_kotatsu_status(ty_manga.status),
        ty_manga.author or ty_manga.artist,
        kotatsu_source,
        # list(ty_manga.genres),
    )


def to_kotatsu_favorite(
    ty_manga: TachiyomiManga, category: int, kt_manga: KotatsuManga
) -> FavoritesEntry:
    return FavoritesEntry(
        kt_manga.id,
        category,
        0,
        ty_manga.date_added,
        0,
        kt_manga.__dict__,
    )


def to_kotatsu_history(
    ty_manga: TachiyomiManga, ty_source: str, kt_manga: KotatsuManga
) -> HistoryRecord | None:
    latest_chapter, newest_chapter = ty_manga.get_latest_and_newest_chapter()
    if latest_chapter is None:
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


def to_kotatsu_backup(ty_backup: TachiyomiBackup) -> tuple[KotatsuBackup, list[Any]]:
    now = int(time.time() * 1000)
    favorites = []
    history = []
    total = len(ty_backup.data.mangaList)
    failed = []
    for i, manga in enumerate(ty_backup.data.mangaList):
        manga_src = ty_backup.sources[manga.source]
        kotatsu_manga = to_kotatsu_manga(manga, manga_src)
        if kotatsu_manga is None:
            manga_dict = manga.to_dict()
            manga_dict["source_name"] = manga_src
            failed.append(manga_dict)
            continue
        for j in manga.categories:
            favorites.append(to_kotatsu_favorite(manga, j, kotatsu_manga).__dict__)
        history_entry = to_kotatsu_history(manga, manga_src, kotatsu_manga)
        if history_entry is not None:
            history.append(history_entry.__dict__)
        print("{:.2f}%".format(((i + 1) / total) * 100))
    category = [KotatsuCategory(c.order, now, c.order, c.name, "NEWEST", True, True).__dict__
                for c in ty_backup.data.category]
    return KotatsuBackup(favorites, history, category), failed
