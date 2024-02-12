from protobuf3.message import Message
from protobuf3.fields import (
    MessageField,
    Int32Field,
    Int64Field,
    StringField,
    BoolField,
)


class Source(Message):
    name = StringField(field_number=1)
    id = Int64Field(field_number=2)


class Category(Message):
    name = StringField(field_number=1)
    order = Int32Field(field_number=2)
    flags = Int32Field(field_number=3)


class Chapter(Message):
    url = StringField(field_number=1)
    name = StringField(field_number=2)
    scanlator = StringField(field_number=3)
    read = BoolField(field_number=4)
    bookmark = BoolField(field_number=5)
    lastPage = Int32Field(field_number=6)
    pagesLeft = Int32Field(field_number=800)


class Manga(Message):
    source = Int64Field(field_number=1)
    url = StringField(field_number=2)
    title = StringField(field_number=3)
    artist = StringField(field_number=4)
    author = StringField(field_number=5)
    description = StringField(field_number=6)
    genres = StringField(field_number=7, repeated=True)
    chapters = MessageField(Chapter, field_number=16, repeated=True)
    categories = Int32Field(field_number=17, repeated=True)
    favorite = BoolField(field_number=100)

    def print(self):
        print(
            f"Title: {self.title}\nURL: {self.url}\nAuthor and artist: {self.author}; {self.artist}\nDescription: {self.description}\nChapter read: {len([c for c in self.chapters if c.read])}/{len(self.chapters)}\n"
        )


class Backup(Message):
    mangaList = MessageField(message_cls=Manga, field_number=1, repeated=True)
    categories = MessageField(message_cls=Category, field_number=2, repeated=True)
    sources = MessageField(message_cls=Source, field_number=101, repeated=True)
