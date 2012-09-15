import AlchemyAPI, requests, unicodedata
from xmldict import xml_to_dict

alchemyObj = AlchemyAPI.AlchemyAPI()
alchemyObj.loadAPIKey("nlpKey.txt")

def processDocuments(docs):
	processed = []
	if isinstance(docs, list):
		for doc in docs:
			keywords = getKeywords(doc)
			concepts = getConcepts(doc)
			keywords = locateKeywords(doc, keywords)
			processed.append({'keywords': keywords, 'concepts': concepts})
	else:
		keywords = getKeywords(docs)
		concepts = getConcepts(docs)
		keywords = locateKeywords(docs, keywords)
		processed.append({'keywords': keywords, 'concepts': concepts})
	return processed

def locateKeywords(file, keywords):
	text = requests.get(file).text
	if isinstance(text, unicode):
		text = unicodedata.normalize('NFKD', requests.get(file).text).encode('ascii', 'ignore')
	end = len(text)
	for keyword in keywords:
		indices = []
		start = 0
		while start < end:
			try:
				start = indices[len(indices)-1] + 1
			except:
				pass
			pos = text.find(keyword['text'], start)
			if not pos == -1:
				indices.append(pos)
			else:
				start = end
		keyword['position'] = indices
	return keywords

def getKeywords(file):
	# Set params for keyword search
	params = AlchemyAPI.AlchemyAPI_KeywordParams()
	params.setMaxRetrieve(30)
	params.setKeywordExtractMode('strict')

	text = requests.get(file).text
	if isinstance(text, unicode):
		text = unicodedata.normalize('NFKD', requests.get(file).text).encode('ascii', 'ignore')
	result = xml_to_dict(alchemyObj.TextGetRankedKeywords(text, params))
	keywords = result['results']['keywords']['keyword']
	return keywords

def getConcepts(file):
	# Set params for keyword search
	params = AlchemyAPI.AlchemyAPI_ConceptParams()
	params.setMaxRetrieve(30)

	text = requests.get(file).text
	if isinstance(text, unicode):
		text = unicodedata.normalize('NFKD', requests.get(file).text).encode('ascii', 'ignore')
	result = xml_to_dict(alchemyObj.TextGetRankedConcepts(text, params))
	keywords = result['results']['concepts']['concept']
	temp = []
	for result in keywords:
		temp.append({'relevance': result['relevance'], 'text': result['text']})
	keywords = temp
	return keywords