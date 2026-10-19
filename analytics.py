
from pymongo import MongoClient, DESCENDING, ASCENDING

client = MongoClient(
    "mongodb://localhost:27017/",
    serverSelectionTimeoutMS=5000
)

db = client["retail_store"]
products = db["products"]
sales = db["sales"]


def revenue_report():
    print("\n===== REVENUE REPORT =====")

    pipeline = [
        {
            "$group": {
                "_id": None,
                "total_revenue": {"$sum": "$total"},
                "total_sales": {"$sum": 1},
                "average_sale": {"$avg": "$total"}
            }
        }
    ]

    results = list(sales.aggregate(pipeline))

    if not results:
        print("No sales recorded yet.")
        return

    report = results[0]

    print(f"Total revenue: ₹{report['total_revenue']:.2f}")
    print(f"Number of sales: {report['total_sales']}")
    print(f"Average sale value: ₹{report['average_sale']:.2f}")


def best_selling_products():
    print("\n===== BEST-SELLING PRODUCTS =====")

    pipeline = [
        {"$unwind": "$items"},
        {
            "$group": {
                "_id": "$items.sku",
                "product_name": {"$first": "$items.name"},
                "units_sold": {"$sum": "$items.quantity"},
                "revenue": {
                    "$sum": {
                        "$multiply": [
                            "$items.quantity",
                            "$items.unit_price"
                        ]
                    }
                }
            }
        },
        {"$sort": {"units_sold": DESCENDING}},
        {"$limit": 10}
    ]

    results = list(sales.aggregate(pipeline))

    if not results:
        print("No sales recorded yet.")
        return

    for item in results:
        print(
            f"{item['product_name']} | "
            f"SKU: {item['_id']} | "
            f"Units sold: {item['units_sold']} | "
            f"Revenue: ₹{item['revenue']:.2f}"
        )


def category_sales_report():
    print("\n===== CATEGORY-WISE SALES =====")

    pipeline = [
        {"$unwind": "$items"},
        {
            "$lookup": {
                "from": "products",
                "localField": "items.sku",
                "foreignField": "sku",
                "as": "product_info"
            }
        },
        {
            "$group": {
                "_id": {
                    "$ifNull": [
                        {"$arrayElemAt": [
                            "$product_info.category", 0
                        ]},
                        "Unknown / Product unavailable"
                    ]
                },
                "units_sold": {"$sum": "$items.quantity"},
                "revenue": {
                    "$sum": {
                        "$multiply": [
                            "$items.quantity",
                            "$items.unit_price"
                        ]
                    }
                }
            }
        },
        {"$sort": {"revenue": DESCENDING}}
    ]

    results = list(sales.aggregate(pipeline))

    if not results:
        print("No sales recorded yet.")
        return

    for item in results:
        print(
            f"Category: {item['_id']} | "
            f"Units sold: {item['units_sold']} | "
            f"Revenue: ₹{item['revenue']:.2f}"
        )


def low_stock_report():
    print("\n===== LOW-STOCK ALERT =====")

    threshold = 5

    results = list(
        products.find(
            {"stock": {"$lte": threshold}}
        ).sort("stock", ASCENDING)
    )

    if not results:
        print("No low-stock products.")
        return

    for product in results:
        print(
            f"{product['name']} | "
            f"SKU: {product['sku']} | "
            f"Remaining stock: {product['stock']}"
        )


def main():
    try:
        client.admin.command("ping")
        print("Connected to Retail Store Database!")

        while True:
            print("\n===== BUSINESS ANALYTICS =====")
            print("1. Revenue Report")
            print("2. Best-Selling Products")
            print("3. Category-Wise Sales")
            print("4. Low-Stock Alert")
            print("5. Exit")

            choice = input("Choose a report: ").strip()

            if choice == "1":
                revenue_report()
            elif choice == "2":
                best_selling_products()
            elif choice == "3":
                category_sales_report()
            elif choice == "4":
                low_stock_report()
            elif choice == "5":
                break
            else:
                print("Invalid choice.")

    except Exception as error:
        print("Database error:", error)

    finally:
        client.close()


if __name__ == "__main__":
    main()
