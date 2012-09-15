from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGO_DB"] = "alchemy"
app.config["SECRET_KEY"] = "(e%\+ydg$mtd&4wvzfmg-a*b@tfyz*1tn2ak(k+-&4q9=#&qpdq"

db = MongoEngine(app)

if __name__ == '__main__':
	app.run()