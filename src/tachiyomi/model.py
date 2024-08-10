from protobuf3.message import Message
from protobuf3.fields import (
    MessageField,
    Int32Field,
    FloatField,
    Int64Field,
    StringField,
    BoolField,
)


class Source(Message):
    name = StringField(field_number=1)
    id = Int64Field(field_number=2)


class Chapter(Message):
    url = StringField(field_number=1)
    name = StringField(field_number=2)
    scanlator = StringField(field_number=3)
    read = BoolField(field_number=4)
    bookmark = BoolField(field_number=5, optional=True)
    last_page = Int32Field(field_number=6)
    fetch_date = Int32Field(field_number=7)
    upload_date = Int32Field(field_number=8)
    volume = FloatField(field_number=9)
    number = Int32Field(field_number=10)
    last_modified_at = Int64Field(field_number=11)

    def to_dict(self):
        return {"url": self.url, "name": self.name, "scanlator": self.scanlator, "read": self.read,
                "bookmark": self.bookmark, "last_page": self.last_page, "upload_date": self.fetch_date,
                "update_date": self.upload_date, "volume": self.volume, "number": self.number,
                "last_modified_at": self.last_modified_at}


class Manga(Message):
    source = Int64Field(field_number=1)
    url = StringField(field_number=2)
    title = StringField(field_number=3)
    artist = StringField(field_number=4, optional=True)
    author = StringField(field_number=5, optional=True)
    description = StringField(field_number=6, optional=True)
    genres = StringField(field_number=7, repeated=True)
    status = Int32Field(field_number=8)
    thumbnail = StringField(field_number=9, optional=True)
    date_added = Int64Field(field_number=13)
    viewer = Int32Field(field_number=14)
    chapters = MessageField(Chapter, field_number=16, repeated=True)
    categories = Int32Field(field_number=17, repeated=True)
    favorite = BoolField(field_number=100)
    last_modified_at = Int64Field(field_number=106)
    favorite_modified_at = Int64Field(field_number=107)

    def get_latest_and_newest_chapter(self):
        latest = None
        newest = None
        for chapter in self.chapters:
            if chapter.number > len(self.chapters):
                continue
            if chapter.read and (latest is None or latest.number < chapter.number):
                latest = chapter
            if newest is None or newest.number < chapter.number:
                newest = chapter
        return latest, newest

    def to_dict(self):
        return {"source": self.source, "url": self.url, "title": self.title, "artist": self.artist,
                "author": self.author, "description": self.description, "genres": list(self.genres),
                "status": self.status, "thumbnail": self.thumbnail, "date_added": self.date_added,
                "viewer": self.viewer, "chapters": [c.to_dict() for c in self.chapters],
                "categories": list(self.categories), "favorite": self.favorite,
                "last_modified_at": self.last_modified_at, "favorite_modified_at": self.favorite_modified_at}

    def print(self):
        print(
            f"Title: {self.title}\nURL: {self.url}\nAuthor and artist: {self.author}; {self.artist}\nDescription: {self.description}\nChapter read: {len([c for c in self.chapters if c.read])}/{len(self.chapters)}\n"
        )


class Category(Message):
    name = StringField(field_number=1)
    order = Int64Field(field_number=2)
    flags = Int64Field(field_number=100)


class Backup(Message):
    mangaList = MessageField(message_cls=Manga, field_number=1, repeated=True)
    category = MessageField(message_cls=Category, field_number=2, repeated=True)
    sources = MessageField(message_cls=Source, field_number=101, repeated=True)
