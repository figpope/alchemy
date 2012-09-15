import datetime
from flask import url_for
from alchemy import db

class Document(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    FPUrl = db.URLField(max_length=255, required=True)
    keywords = db.ListField(db.EmbeddedDocumentField('Keyword'))
    concepts = db.ListField(db.EmbeddedDocumentField('Concept'))

    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at']
    }

class Keyword(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    index = db.IntField(required=True)
    keyword = db.StringField(verbose_name="Keyword", required=True)

class Concept(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    concept = db.StringField(verbose_name="Keyword", required=True)