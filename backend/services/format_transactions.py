# backend/services/format_transactions.py
import json
import os
from fastapi import HTTPException

# Point to your transactions.json file inside backend/data/
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # points to /backend
TRANSACTIONS_FILE = os.path.join(BASE_DIR, "data", "mock_transactions.json")
print(f"📂 Using transactions file: {TRANSACTIONS_FILE}")

# Custom category mapping (merchant-based)
CATEGORY_MAPPING = {
    "food": ["McDonald's", "Starbucks", "KFC", "Zomato"],
    "transport": ["Uber", "Lyft", "ADNOC Fuel"],
    "shopping": ["Amazon", "Walmart", "Target", "Carrefour"],
    "entertainment": ["Netflix", "Spotify", "Cinema"],
    "bills": ["AT&T", "Verizon", "Electricity", "Water"],
    "travel": ["United Airlines", "Delta", "Airbnb", "Emirates Airlines"],
}


def load_transactions(file_path: str):
    """Load transactions from JSON file"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Transactions file not found: {file_path}")
    with open(file_path, "r") as f:
        return json.load(f).get("transactions", [])


def map_category(merchant_name: str, plaid_categories: list = None):
    """Map merchant or Plaid categories to custom categories"""
    if not merchant_name and not plaid_categories:
        return "other"

    # Case-insensitive match for merchant names
    if merchant_name:
        merchant_name = merchant_name.lower()
        for cat, merchants in CATEGORY_MAPPING.items():
            if any(merchant_name == m.lower() for m in merchants):
                return cat

    # Fallback: map Plaid's category field
    if plaid_categories:
        for plaid_cat in plaid_categories:
            plaid_cat = plaid_cat.lower()
            if "food" in plaid_cat:
                return "food"
            if "transport" in plaid_cat:
                return "transport"
            if "shop" in plaid_cat:
                return "shopping"
            if "entertain" in plaid_cat:
                return "entertainment"
            if "bill" in plaid_cat or "utility" in plaid_cat:
                return "bills"
            if "travel" in plaid_cat:
                return "travel"

    return "other"


def get_formatted_transactions():
    """Load and format transactions for API or script"""
    try:
        raw_transactions = load_transactions(TRANSACTIONS_FILE)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    formatted = []
    for tx in raw_transactions:
        formatted.append({
            "transaction_id": tx.get("transaction_id"),
            "account_id": tx.get("account_id"),
            "amount": tx.get("amount"),
            "merchant_name": tx.get("merchant_name") or "Unknown",
            "category": [map_category(
                tx.get("merchant_name"),
                tx.get("category")
            )],
            "date": tx.get("date"),
        })
    return formatted


if __name__ == "__main__":
    # Only runs when called directly (not via API)
    data = {"transactions": get_formatted_transactions()}
    print(json.dumps(data, indent=2))
