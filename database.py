from pymongo import MongoClient


# database connection
client = MongoClient()
database = client["data_pusher"]

account = database["account"]
destinations = database["destinations"]




