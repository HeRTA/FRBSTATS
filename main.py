from pymongo import MongoClient
import csv
import json

# Initiate Mongo connection
client = MongoClient("mongodb://localhost:27017/")
db = client["frbstats"]
collection = db["catalogue"]

# Drop all data
collection.drop()

# Load catalogue data
with open('catalogue.json', 'r') as myfile:
    data = myfile.read()
    obj = json.loads(data)
    for obs in obj:
        collection.insert_one(obs)
