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

def closestMatch(database, sessionID, keyword):
	connect(database)
	session = Session.objects.get(sessionID__exact=session)


def randomWalk(database, sessionID, steps):
	connect(database)
	session = Session.objects.get(sessionID__exact=session)
	for i in range(0, steps):
		session.documents(randomWalk)