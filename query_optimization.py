
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["retail_store"]
products = db["products"]


def show_explain(title, query):
    print(f"\n===== {title} =====")

    explanation = products.find(query).explain()
    stats = explanation.get("executionStats", {})
    plan = explanation.get("queryPlanner", {}).get(
        "winningPlan", {}
    )

    print("Winning plan:", plan)
    print("Documents returned:", stats.get("nReturned"))
    print("Documents examined:", stats.get("totalDocsExamined"))
    print("Index keys examined:", stats.get("totalKeysExamined"))
    print("Execution time (ms):", stats.get("executionTimeMillis"))


try:
    client.admin.command("ping")

    show_explain(
        "SKU SEARCH",
        {"sku": "ELEC001"}
    )

    show_explain(
        "CATEGORY SEARCH",
        {"category": "Electronics"}
    )

    show_explain(
        "CATEGORY AND PRICE SEARCH",
        {
            "category": "Electronics",
            "price": {"$lte": 1000}
        }
    )

finally:
    client.close()
