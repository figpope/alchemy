import requests
from mongoengine import *
from models import *

BASE_URL = "http://conceptnet5.media.mit.edu/data/5.1/"
ASSOC = "assoc"
SEARCH = "search"
REGION = "/c/en/"

def getAssociation(one, two):
	oneInfo = requests.get(BASE_URL + SEARCH + "?text=" + one)
	twoInfo = requests.get(BASE_URL + SEARCH + "?text=" + one)
	association = requests.get(BASE_URL + ASSOC + REGION + one +
		"?filter=" + REGION + two + "&limit=1")

def randomWalk(database, session, steps):
	connect(database)
	session = Session.objects.get(sessionID__exact=session)
	