import datetime
from mongoengine import *

class Keyword(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    indices = DictField(required=True)
    keyword = StringField(verbose_name="Keyword", required=True)
    documents = ListField(ReferenceField(Document))

class Concept(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    concept = StringField(verbose_name="Keyword", required=True)
    documents = ListField(ReferenceField(Document))

class Document(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    title = StringField(max_length=255, required=True)
    FPUrl = URLField(max_length=255, required=True)
    keywords = ListField(ReferenceField(Keyword))
    concepts = ListField(ReferenceField(Concept))

class User(Document):
    userID = StringField(required=True)
    accessToken = StringField()