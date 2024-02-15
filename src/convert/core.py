SOURCES_MAP = {"MangaDex": "MANGADEX", "Mangakakalot": "MANGAKAKALOTTV"}


def to_kotatsu_url(source: str, tachiyomi_url: str) -> str:
    if source == "MangaDex":
        return tachiyomi_url.replace("/manga/", "")
    if source == "Mangakakalot":
        return tachiyomi_url.replace("https://chapmanganato.to/", "/manga/")


def to_kotatsu_status(tachiyomi_status: int) -> str:
    if tachiyomi_status == 1:
        return "ONGOING"
    if tachiyomi_status == 2 or tachiyomi_status == 4:
        return "FINISHED"
    if tachiyomi_status == 5:
        return "ABANDONED"
    if tachiyomi_status == 6:
        return "PAUSED"
    return ""
