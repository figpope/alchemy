import datetime
from mongoengine import *

class Session(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    sessionID = StringField(verbose_name="Session", required=True)
    users = ListField(ReferenceField('User'))
    start = StringField()
    end = StringField()
    documents = ListField(ReferenceField('Paper'))

class Keyword(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    session = ReferenceField(Session)
    indices = DictField(required=True)
    keyword = StringField(verbose_name="Keyword", required=True)
    documents = ListField(ReferenceField('Paper'))

class Concept(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    session = ReferenceField(Session)
    concept = StringField(verbose_name="Concept", required=True)
    documents = ListField(ReferenceField('Paper'))

class Paper(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    session = ReferenceField(Session)
    title = StringField(max_length=255, required=True)
    FPUrl = URLField(max_length=255, required=True)
    keywords = ListField(ReferenceField(Keyword))
    concepts = ListField(ReferenceField(Concept))

class User(Document):
    userID = StringField(required=True)
    accessToken = StringField()
    sessions = ListField(ReferenceField(Session))