import pymongo
client = pymongo.MongoClient(host='127.0.0.1')
db=client.BiliBili
collections=db.person
db_list = client.list_database_names()
print(db_list)