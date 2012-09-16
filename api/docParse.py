import AlchemyAPI, requests, unicodedata, subprocess, os
from xmldict import xml_to_dict
from pyPdf import PdfFileReader
from StringIO import StringIO
from docx import *

alchemyObj = AlchemyAPI.AlchemyAPI()
alchemyObj.loadAPIKey("nlpKey.txt")

def pdf2string(file):
	text = ""
	pdf = PdfFileReader(StringIO(file))
	for i in range(0, pdf.getNumPages()):
		text += pdf.getPage(i).extractText() + " \n"
	text = u" ".join(text.replace(u"\xa0", u" ").strip().split())
	return text

def docx2string(file):
    document = opendocx(StringIO(file))       
    text = getdocumenttext(document)    
    unicodeText = ""
    for paratext in text:
        unicodeText += (paratext.encode("utf-8"))
    return unicodeText

def doc2string(doc):
	f = file("temp", 'w')
	f.write(doc)
	f.close()
	text = subprocess.check_output(["catdoc", "temp"])
	os.remove("temp")
	return text

def link2text(link):
	req = requests.get(link)
	fileType = req.headers['content-type']
	if fileType == 'application/pdf':
		text = pdf2string(req.content)
	elif fileType == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
		text = docx2string(req.content)
	elif fileType == 'application/msword':
		text = doc2string(req.content)
	else:
		text = req.text
	return text

def processDocuments(docs):
	processed = []
	if isinstance(docs, list):
		for doc in docs:
			text = link2text(doc)
			keywords = getKeywords(text)
			concepts = getConcepts(text)
			keywords = locateKeywords(text, keywords)
			processed.append({'keywords': keywords, 'concepts': concepts})
	else:
		text = link2text(docs)
		keywords = getKeywords(text)
		concepts = getConcepts(text)
		keywords = locateKeywords(text, keywords)
		processed.append({'keywords': keywords, 'concepts': concepts})
	return processed

def locateKeywords(text, keywords):
	if isinstance(text, unicode):
		text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
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

def getKeywords(text):
	# Set params for keyword search
	params = AlchemyAPI.AlchemyAPI_KeywordParams()
	params.setMaxRetrieve(30)
	params.setKeywordExtractMode('strict')

	if isinstance(text, unicode):
		text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
	result = xml_to_dict(alchemyObj.TextGetRankedKeywords(text, params))
	try:
		keywords = result['results']['keywords']['keyword']
	except:
		keywords = None
	return keywords

def getConcepts(text):
	# Set params for keyword search
	params = AlchemyAPI.AlchemyAPI_ConceptParams()
	params.setMaxRetrieve(30)

	if isinstance(text, unicode):
		text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
	result = xml_to_dict(alchemyObj.TextGetRankedConcepts(text, params))
	keywords = result['results']['concepts']['concept']
	temp = []
	for result in keywords:
		temp.append({'relevance': result['relevance'], 'text': result['text']})
	keywords = temp
	return keywords