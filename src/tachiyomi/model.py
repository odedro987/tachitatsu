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
    number = FloatField(field_number=9)


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
    chapters = MessageField(Chapter, field_number=16, repeated=True)
    categories = Int32Field(field_number=17, repeated=True)
    favorite = BoolField(field_number=100)

    def get_latest_and_newest_chapter(self):
        latest = None
        newest = None
        for chapter in self.chapters:
            if chapter.number > len(self.chapters):
                continue
            if chapter.read and (latest == None or latest.number < chapter.number):
                latest = chapter
            if newest == None or newest.number < chapter.number:
                newest = chapter
        return latest, newest

    def print(self):
        print(
            f"Title: {self.title}\nURL: {self.url}\nAuthor and artist: {self.author}; {self.artist}\nDescription: {self.description}\nChapter read: {len([c for c in self.chapters if c.read])}/{len(self.chapters)}\n"
        )


class Backup(Message):
    mangaList = MessageField(message_cls=Manga, field_number=1, repeated=True)
    sources = MessageField(message_cls=Source, field_number=101, repeated=True)
