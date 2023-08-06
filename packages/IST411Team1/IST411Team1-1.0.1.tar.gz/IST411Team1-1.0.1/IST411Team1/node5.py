"""Project:W10 - Project Diamond
Purpose Details: Loging all activities in the Project to MongoDB
Course: IST 411
Author: Arnold Adu-Darko
Date Developed: 11/24/2017
Last Date Changed:11/26/2017
Rev: 2.0"""


from pymongo import MongoClient
from pymongo import ASCENDING
import datetime

"""Connecting to MongoDB"""
client = MongoClient('localhost', 27017)
"""Creating and naming database"""
db = client.Team1_Logs
log_collection = db.log
log_collection.ensure_index([('Timestamp', ASCENDING)])

class Node5:
	def log(msg):
		inserted = False
		"""Log message to MongoDB"""
		entry = {}
		entry['Timestamp'] = datetime.datetime.utcnow()
		entry['msg'] = msg
		log_collection.insert_one(entry)
		print("Inserted log entry into Team 1's MongoDB")
		inserted = True

if __name__ == '__main__':
	main()
