from flask import Flask
app = Flask(__name__)

@app.route("/v1/documents/")
def documents():
  return ''