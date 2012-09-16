from flask import Flask, request, abort
from mongoengine import *
from docParse import processDocuments
from models import *
import os, json

app = Flask(__name__)
app.config["MONGODB_DB"] = "alchemy"
app.config["SECRET_KEY"] = "(e%\+ydg$mtd&4wvzfmg-a*b@tfyz*1tn2ak(k+-&4q9=#&qpdq"

db = connect(app.config["MONGODB_DB"])

@app.route('/')
def index():
  return app.send_static_file('test.html')

@app.route('/login', methods=["POST"])
def login():
  app.logger.debug(str(request.form))
  if 'accessToken' in request.form and 'userID' in request.form:
      userID = request.form['userID']
      accessToken = request.form['accessToken']
      return 'success'
  abort(500)

@app.route('/getDocument', methods=["POST"])
def getDocument():
  pass

@app.route('/getSessions', methods=["POST"])
def getSessions():
  if not 'userID' in request.form:
    abort(400)
  else:
    user = Users.objects.get(userID__exact=request.form['userID'])
    sess = []
    for sessions in user.sessions:
      sess.append(sessions.sessionID)
    return sess

@app.route('/getStatus', methods=["POST"])
def getStatus():
  if not 'sessionID' in request.form:
    abort(400)
  else:
    session = Session.objects.get(sessionID__exact=request.form['sessionID'])
    return session.status

@app.route('/getGoals', methods=["POST"])
def getGoals():
  if not 'sessionID' in request.form:
    abort(400)
  else:
    session = Session.objects.get(sessionID__exact=request.form['sessionID'])


@app.route('/updateStats', methods=["POST"])
def updateStats():
  pass

@app.route('/addDocument', methods=["POST"])
def addDocument():
  app.logger.debug(str(request.form))
  if not 'files' in request.form:
    abort(400)
  documents = json.loads(request.form['files'])
  for document in documents:
    metadata = processDocuments(document['url'])
    filename = os.path.splitext(document['data']['filename'])[0]
    doc = Paper(
      title = filename,
      FPUrl = document['url'])
    doc.save()
    for keyword in metadata[0]['keywords']:
      try:
        key = Keyword.objects.get(keyword__iexact=keyword['text'])
        key.indices.append({filename: keyword['position']})
        key.documents.append(doc)
      except:
        key = Keyword(
          indices = {filename: keyword['position']},
          keyword = keyword['text'],
          documents = [doc])
      key.save()
      doc.keywords.append(key)
    for concept in metadata[0]['concepts']:
      try:
        con = Concept.objects.get(concept__iexact=concept['text'])
        con.documents.append(doc)
      except:
          con = Concept(
            concept = concept['text'],
            documents = [doc])
      con.save()
      doc.concepts.append(con)
    doc.save()
  return "success"

@app.route('/static/<path:file_path>')
def static_fetch(file_path):
  return app.send_static_file(str(file_path))

if __name__ == '__main__':
  # Bind to PORT if defined, otherwise default to 5000.
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)