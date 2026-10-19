from pymongo import MongoClient

# Connect Python to our local MongoDB server
client = MongoClient("mongodb://localhost:27017/")

# Select our project database
db = client["retail_store"]

# Create our first collection
products = db["products"]

# Insert one sample product
result = products.insert_one({
    "name": "Wireless Mouse",
    "sku": "ELEC001",
    "category": "Electronics",
    "price": 799,
    "stock": 25
})

print("Database setup successful!")
print("Inserted product ID:", result.inserted_id)

# Close the connection
client.close()
