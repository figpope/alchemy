import datetime
from mongoengine import *

class Session(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    sessionID = StringField(verbose_name="Session", required=True, unique=True)
    users = ListField(ReferenceField('User'), required=True)
    start = StringField()
    current = ReferenceField('Paper')
    end = StringField()
    status = StringField(default="Opened", required=True)
    documents = ListField(ReferenceField('Paper'))

class Keyword(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    session = ReferenceField(Session, required=True)
    indices = DictField(required=True)
    keyword = StringField(verbose_name="Keyword", required=True, unique=True)
    documents = ListField(ReferenceField('Paper'))

class Concept(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    session = ReferenceField(Session, required=True)
    concept = StringField(verbose_name="Concept", required=True, unique=True)
    documents = ListField(ReferenceField('Paper'))

class Paper(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    session = ReferenceField(Session, required=True)
    title = StringField(max_length=255, required=True)
    FPUrl = URLField(max_length=255, required=True)
    keywords = ListField(ReferenceField(Keyword))
    concepts = ListField(ReferenceField(Concept))

class User(Document):
    userID = StringField(required=True, unique=True)
    accessToken = StringField()
    sessions = ListField(ReferenceField(Session))