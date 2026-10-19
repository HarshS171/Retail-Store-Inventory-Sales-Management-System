from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["retail_store"]

product_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "sku", "name", "category", "price", "stock"
        ],
        "properties": {
            "sku": {
                "bsonType": "string",
                "minLength": 1
            },
            "name": {
                "bsonType": "string",
                "minLength": 1
            },
            "category": {
                "bsonType": "string",
                "minLength": 1
            },
            "price": {
                "bsonType": "number",
                "minimum": 0.01
            },
            "stock": {
                "bsonType": "int",
                "minimum": 0
            }
        }
    }
}

sales_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["sale_id", "items", "total", "sale_date"],
        "properties": {
            "sale_id": {
                "bsonType": "string",
                "minLength": 1
            },
            "items": {
                "bsonType": "array",
                "minItems": 1,
                "items": {
                    "bsonType": "object",
                    "required": [
                        "sku", "name", "quantity", "unit_price"
                    ],
                    "properties": {
                        "sku": {"bsonType": "string"},
                        "name": {"bsonType": "string"},
                        "quantity": {
                            "bsonType": "int",
                            "minimum": 1
                        },
                        "unit_price": {
                            "bsonType": "number",
                            "minimum": 0
                        }
                    }
                }
            },
            "total": {
                "bsonType": "number",
                "minimum": 0
            },
            "sale_date": {
                "bsonType": "date"
            }
        }
    }
}

db.command({
    "collMod": "products",
    "validator": product_validator,
    "validationLevel": "strict",
    "validationAction": "error"
})

if "sales" not in db.list_collection_names():
    db.create_collection(
        "sales",
        validator=sales_validator
    )
else:
    db.command({
        "collMod": "sales",
        "validator": sales_validator,
        "validationLevel": "strict",
        "validationAction": "error"
    })

db.products.create_index("sku", unique=True)
db.sales.create_index("sale_id", unique=True)
db.sales.create_index("sale_date")
db.sales.create_index("items.sku")

print("Schema validation applied successfully!")
print("Indexes created successfully.")

client.close()
