
from pymongo import MongoClient
from datetime import datetime, timezone
from uuid import uuid4

client = MongoClient(
    "mongodb://localhost:27017/",
    serverSelectionTimeoutMS=5000
)

db = client["retail_store"]
products = db["products"]
sales = db["sales"]


def make_sale():
    print("\n===== CREATE A SALE =====")

    sku = input("Enter product SKU: ").strip().upper()

    try:
        quantity = int(input("Enter quantity to sell: "))

        if quantity <= 0:
            print("Quantity must be greater than zero.")
            return

    except ValueError:
        print("Please enter a valid whole-number quantity.")
        return

    product = products.find_one({"sku": sku})

    if product is None:
        print("Product not found.")
        return

    if product["stock"] < quantity:
        print("Insufficient stock!")
        print("Available stock:", product["stock"])
        return
    
    unit_price = product["price"]
    total = unit_price * quantity

    print("\nSale summary")
    print("Product:", product["name"])
    print("Quantity:", quantity)
    print("Price per item: ₹", unit_price)
    print("Total: ₹", total)

    confirm = input("Confirm sale? Type YES: ")

    if confirm != "YES":
        print("Sale cancelled.")
        return
    
    stock_result = products.update_one(
        {
            "sku": sku,
            "stock": {"$gte": quantity}
        },
        {
            "$inc": {"stock": -quantity}
        }
    )

    if stock_result.modified_count != 1:
        print("Sale failed: stock is no longer sufficient.")
        return
    
    sale = {
        "sale_id": str(uuid4()),
        "items": [
            {
                "sku": sku,
                "name": product["name"],
                "quantity": quantity,
                "unit_price": unit_price
            }
        ],
        "total": total,
        "sale_date": datetime.now(timezone.utc)
    }

    try:
        sales.insert_one(sale)

        print("\nSale completed successfully!")
        print("Sale ID:", sale["sale_id"])
        print("Total amount: ₹", total)

        updated_product = products.find_one({"sku": sku})
        print("Remaining stock:", updated_product["stock"])

    except Exception as error:
        try:
            products.update_one(
                {"sku": sku},
                {"$inc": {"stock": quantity}}
            )
            print("Sale record failed. Stock was restored.")
        except Exception:
            print("WARNING: Stock restoration failed.")
            print("Please check the product stock manually.")

        print("Database error:", error)


def view_sales():
    print("\n===== SALES HISTORY =====")

    found = False

    for sale in sales.find().sort("sale_date", -1):
        found = True
        print("\nSale ID:", sale["sale_id"])
        print("Date:", sale["sale_date"])

        for item in sale["items"]:
            print(
                item["name"],
                "| Quantity:", item["quantity"],
                "| Unit price: ₹", item["unit_price"]
            )

        print("Total: ₹", sale["total"])

    if not found:
        print("No sales recorded yet.")


def main():
    try:
        client.admin.command("ping")
        print("Connected to Retail Store Database!")

        while True:
            print("\n===== SALES MANAGEMENT =====")
            print("1. Create Sale")
            print("2. View Sales History")
            print("3. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                make_sale()
            elif choice == "2":
                view_sales()
            elif choice == "3":
                break
            else:
                print("Invalid choice.")

    except Exception as error:
        print("Database error:", error)

    finally:
        client.close()


if __name__ == "__main__":
    main()
