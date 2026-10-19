
from pymongo import MongoClient

# Connect to the local MongoDB server
client = MongoClient(
    "mongodb://localhost:27017/",
    serverSelectionTimeoutMS=5000
)

try:
    # Check whether the MongoDB server is responding
    client.admin.command("ping")
    print("MongoDB connection successful!")

except Exception as error:
    print("MongoDB connection failed.")
    print("Error:", error)

finally:
    # Close the connection when the script finishes
    client.close()
