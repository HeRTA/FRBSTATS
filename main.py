from pymongo import MongoClient
import csv
import json
#Mongo Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["frbstats"]
collection = db["catalogue"]
#drop all data 
collection.drop()

with open('catalogue.json', 'r') as myfile:
    data=myfile.read()
    obj = json.loads(data)
    for obs in obj:
        collection.insert_one(obs)
