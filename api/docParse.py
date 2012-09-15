import AlchemyAPI
from xmldict import xml_to_dict

alchemyObj = AlchemyAPI.AlchemyAPI()
alchemyObj.loadAPIKey("nlpKey.txt")

def processDocuments(docs):
	processed = []
	if isinstance(test, list):
		for doc in docs:
			keywords = getKeywords(doc)
			concepts = getConcepts(doc)
			keywords = locateKeywords(doc, keywords)
			processed.append({'keywords': keywords, 'concepts': concepts})
	else:
		keywords = getKeywords(doc)
		concepts = getConcepts(doc)
		keywords = locateKeywords(doc, keywords)
		processed.append({'keywords': keywords, 'concepts': concepts})
	return processed

def locateKeywords(file, keywords):
	text = open(file, 'r').read()
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

	file = open(file, 'r')
	result = xml_to_dict(alchemyObj.TextGetRankedKeywords(file.read(), params))
	keywords = result['results']['keywords']['keyword']
	return keywords

def getConcepts(file):
	# Set params for keyword search
	params = AlchemyAPI.AlchemyAPI_ConceptParams()
	params.setMaxRetrieve(30)

	file = open(file, 'r')
	result = xml_to_dict(alchemyObj.TextGetRankedConcepts(file.read(), params))
	keywords = result['results']['concepts']['concept']
	temp = []
	for result in keywords:
		temp.append({'relevance': result['relevance'], 'text': result['text']})
	keywords = temp
	return keywords