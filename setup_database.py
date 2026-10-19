from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["retail_store"]

products = db["products"]

result = products.insert_one({
    "name": "Wireless Mouse",
    "sku": "ELEC001",
    "category": "Electronics",
    "price": 799,
    "stock": 25
})

print("Database setup successful!")
print("Inserted product ID:", result.inserted_id)

client.close()
