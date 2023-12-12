from flask import Flask
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient

app = Flask(__name__) #instance of Flask

uri = "mongodb+srv://gayatriMotaparthi:LearnFlask123@cluster0.l8cnhl0.mongodb.net/test?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true"
#mongodb+srv://gayatriMotaparthi:LearnFlask123@cluster0.l8cnhl0.mongodb.net/?retryWrites=true&w=majority
client = MongoClient(uri)
db = client.db

app.secret_key = "hello"
app.config['MONGO_URI'] = uri
mongo = PyMongo(app)

from application import routes