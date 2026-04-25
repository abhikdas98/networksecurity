
from urllib.parse import quote_plus
from pymongo.mongo_client import MongoClient

Username = quote_plus("abhik_das98")
Password = quote_plus("Ironman@103D")

uri = f"mongodb+srv://{Username}:{Password}@cluster0.ksnkq2u.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
