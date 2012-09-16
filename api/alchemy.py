import os, json, datetime
from flask import Flask, request, abort, jsonify
from mongoengine import *
from docParse import processDocuments, link2text
from association import randomWalk
from operator import itemgetter
from random import randint
from hashlib import md5
from models import *

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
    try:
      User.objects.get(userID__exact=request.form['userID'])
      return 'success'
    except:
      User(userID = request.form['userID'],
        accessToken = request.form['accessToken']).save()
      return 'success'
  abort(500)

@app.route('/getDocument', methods=["POST"])
def getDocument():
  if not 'keyword' in request.form:
    abort(400)
  else:
    keyword = Keyword.objects.get(keyword__iexact=request.form['keyword'])
    next = keyword.documents[randint(0,len(keyword.documents)-1)]
    text = link2text(next.FPUrl)
    keywords = []
    for keyword in next.keywords:
      for index in keyword.indices.get(next.title):
        keywords.append({'length': len(keyword.keyword), 'position': index})
    locations = sorted(keywords, key=itemgetter('position'))
    return jsonify({'locations':locations, 'text':text})
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
    return jsonify(status=session.status)

@app.route('/getGoals', methods=["POST"])
def getGoals():
  if not 'sessionID' in request.form:
    abort(400)
  else:
    session = Session.objects.get(sessionID__exact=request.form['sessionID'])
    goalDocs = randomwalk(app.config["MONGODB_DB"], session.sessionID, 5)
    start = goalDocs['start'].concepts[randint(0,len(goalDocs['start'].concepts)-1)]
    end = goalDocs['end'].concepts[randint(0,len(goalDocs['end'].concepts)-1)]
    return jsonify({'goals': {'start': start, 'end': end}, 'document': link2text(goalDocs['start'].FPUrl)})

@app.route('/createSession', methods=['POST'])
def createSession():
  if not 'userID' in request.form:
    abort(400)
  else:
    sessionID = md5(str(datetime.datetime.now())).hexdigest()
    session = Session(sessionID=sessionID, users=[User.objects.get(userID__exact=request.form['userID'])])
    session.save()
    return jsonify(sessionID=sessionID)

@app.route('/updateStats', methods=["POST"])
def updateStats():
  pass

@app.route('/addDocument', methods=["POST"])
def addDocument():
  app.logger.debug(str(request.form))
  if not 'files' in request.form:
    abort(400)
  documents = json.loads(request.form['files'])
  session = Session.objects.get(sessionID__exact=request.form['sessionID'])
  for document in documents:
    metadata = processDocuments(document['url'])
    filename = os.path.splitext(document['data']['filename'])[0]
    session.status = "Processing"
    doc = Paper(
      title = filename,
      FPUrl = document['url'],
      session = session)
    doc.save()
    session.documents.append(doc)
    session.save()
    for keyword in metadata[0]['keywords']:
      try:
        key = Keyword.objects.get(keyword__iexact=keyword['text'])
        key.indices.append({filename: keyword['position']})
        key.documents.append(doc)
      except:
        key = Keyword(
          indices = {filename: keyword['position']},
          keyword = keyword['text'],
          documents = [doc],
          session = session)
      key.save()
      doc.keywords.append(key)
    for concept in metadata[0]['concepts']:
      try:
        con = Concept.objects.get(concept__iexact=concept['text'])
        con.documents.append(doc)
      except:
          con = Concept(
            concept = concept['text'],
            documents = [doc],
            session = session)
      con.save()
      doc.concepts.append(con)
    doc.save()
  session.status = "Ready"
  session.save()
  return "success"

@app.route('/static/<path:file_path>')
def static_fetch(file_path):
  return app.send_static_file(str(file_path))

if __name__ == '__main__':
  # Bind to PORT if defined, otherwise default to 5000.
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)