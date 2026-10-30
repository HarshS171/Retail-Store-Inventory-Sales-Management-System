
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient(
    "mongodb://localhost:27017/",
    serverSelectionTimeoutMS=5000
)

db = client["retail_store"]
products = db["products"]

products.create_index("sku", unique=True)


def add_product():
    print("\n--- Add Product ---")

    name = input("Product name: ").strip()
    sku = input("Product SKU: ").strip().upper()
    category = input("Category: ").strip()

    if not name or not sku or not category:
        print("Name, SKU, and category cannot be empty.")
        return

    try:
        price = float(input("Price: "))
        stock = int(input("Stock quantity: "))

        if price <= 0 or stock < 0:
            print("Price must be positive and stock cannot be negative.")
            return

        product = {
            "name": name,
            "sku": sku,
            "category": category,
            "price": price,
            "stock": stock
        }

        products.insert_one(product)
        print("Product added successfully!")

    except ValueError:
        print("Invalid input. Enter a number for price and stock.")

    except DuplicateKeyError:
        print("This SKU already exists. Use a unique SKU.")


def view_products():
    print("\n--- Product Inventory ---")

    found = False

    for product in products.find().sort("name", 1):
        found = True
        print(
            f"Name: {product['name']} | "
            f"SKU: {product['sku']} | "
            f"Category: {product['category']} | "
            f"Price: ₹{product['price']} | "
            f"Stock: {product['stock']}"
        )

    if not found:
        print("No products found.")


def update_product():
    print("\n--- Update Product ---")

    sku = input("Enter the SKU to update: ").strip().upper()

    product = products.find_one({"sku": sku})

    if product is None:
        print("Product not found.")
        return

    print("Leave a field blank to keep its current value.")

    price_input = input(
        f"New price (current ₹{product['price']}): "
    ).strip()

    stock_input = input(
        f"New stock (current {product['stock']}): "
    ).strip()

    changes = {}

    try:
        if price_input:
            new_price = float(price_input)

            if new_price <= 0:
                print("Price must be positive.")
                return

            changes["price"] = new_price

        if stock_input:
            new_stock = int(stock_input)

            if new_stock < 0:
                print("Stock cannot be negative.")
                return

            changes["stock"] = new_stock

        if not changes:
            print("No changes entered.")
            return

        products.update_one(
            {"sku": sku},
            {"$set": changes}
        )

        print("Product updated successfully!")

    except ValueError:
        print("Invalid input. Enter valid numeric values.")


def delete_product():
    print("\n--- Delete Product ---")

    sku = input("Enter the SKU to delete: ").strip().upper()

    product = products.find_one({"sku": sku})

    if product is None:
        print("Product not found.")
        return

    print(f"Product: {product['name']}")

    confirm = input("Are you sure? Type YES to delete: ")

    if confirm == "YES":
        products.delete_one({"sku": sku})
        print("Product deleted successfully!")
    else:
        print("Deletion cancelled.")


def main():
    try:
        client.admin.command("ping")
        print("Connected to Retail Store Database!")

        while True:
            print("\n===== RETAIL STORE MANAGEMENT =====")
            print("1. Add Product")
            print("2. View Products")
            print("3. Update Product")
            print("4. Delete Product")
            print("5. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                add_product()
            elif choice == "2":
                view_products()
            elif choice == "3":
                update_product()
            elif choice == "4":
                delete_product()
            elif choice == "5":
                print("Thank you for using the system!")
                break
            else:
                print("Invalid choice. Enter 1 to 5.")

    except Exception as error:
        print("A database error occurred:", error)

    finally:
        client.close()


if __name__ == "__main__":
    main()
