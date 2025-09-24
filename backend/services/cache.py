import os
import json
import time
from backend.services.plaid_server import get_transactions  # adjust to your actual Plaid fetch function

CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "transactions_cache.json")
CACHE_TTL = 300  # 5 minutes (can change)

def load_cache():
    """Return cached transactions if still valid, else None."""
    if os.path.exists(CACHE_FILE):
        age = time.time() - os.path.getmtime(CACHE_FILE)
        if age < CACHE_TTL:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
    return None

def save_cache(data):
    """Save fresh transactions to JSON file."""
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_cached_transactions():
    """Check cache first, else fetch from Plaid, save, return."""
    cached = load_cache()
    if cached:
        return cached

    # If no valid cache, fetch from Plaid
    fresh_data = get_transactions()
    save_cache(fresh_data)
    return fresh_data
