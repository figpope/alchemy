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
	return association.json['similar'][0][1]

def closestMatch(database, sessionID, keyword):
	connect(database)
	session = Session.objects.get(sessionID__exact=session)
	pairs = []
	for document in session.documents:
		for key in document.concepts:
			pairs.append({key.text: getAssociation(key.text, keyword)})
	highest = pairs[0]
	for pair in pairs:
		if pair[1] > highest[1]:
			highest = pair
	return pair[0]

def evaluateKeywords(document):
	for keyword in document.keywords:
		keyword['concept'] = Concept.objects.get(concept__exact=closestMatch(keyword))
		keyword.save()

def randomWalk(database, sessionID, steps):
	connect(database)
	session = Session.objects.get(sessionID__exact=session)
	start = session.documents[randint(0,len(session.documents)-1)]
	beginning = start
	last = start
	for i in range(0, steps):
		start = start.keywords[randint(0,len(start.keywords)-1)]
		new = start.documents[randint(0,len(start.documents)-1)]
		while new == last:
			new = start.documents[randint(0,len(start.documents)-1)]
		last = start
		start = new
	return {'start': beginning, 'end': start}
