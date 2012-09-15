from flask import Flask
from mongoengine import *
from docParse import processDocuments

app = Flask(__name__)
app.config["MONGODB_DB"] = "alchemy"
app.config["SECRET_KEY"] = "(e%\+ydg$mtd&4wvzfmg-a*b@tfyz*1tn2ak(k+-&4q9=#&qpdq"

db = connect(app.config["MONGODB_DB"])

@app.route('/')
def index():
  return app.send_static_file('index.html')

@app.route('/api/login', methods="POST")
def login():
	app.logger.debug(str(request.form))
	if 'authKey' in request.form and 'userID' in request.form:
	    userID = request.form['userID']
	    authKey = request.form['authKey']
	    return 'success'
	abort(400)

@app.route('/api/addDocument', methods="POST")
def addDocument():
	app.logger.debug(str(request.form))
	if not 'documents' in request.form:
		abort(400)
	for document in request.form['documents']:
		metadata = processDocuments(document['FPUrl'])
		doc = Document(
			title = request.form['filename'],
			FPUrl = request.form['FPUrl'])
		for keyword in metadata['keywords']:
			try:
				key = Keyword.objects(keyword__iexact=keyword['text'])
				key.indices.append()
			except:
				key = Keyword(
					indices = {request.form['filename']: keyword['position']},
					keyword = keyword['text'],
					documents = [doc])
			key.save()
			doc.keywords.append(key)
		for concept in metadata['concepts']:
			con = concept(
				concept = concept['text'],
				documents = [doc])
			con.save()
			doc.concepts.append(con)
		doc.save()
	return success

@app.route('/static/<path:file_path>')
def static_fetch(file_path):
  return app.send_static_file(str(file_path))

if __name__ == '__main__':
  # Bind to PORT if defined, otherwise default to 5000.
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)