import os
import json
from datetime import datetime, timedelta
from backend.services.plaid_server import (
    create_link_token,
    exchange_public_token,
    get_transactions,
    client  # existing Plaid client
)
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.products import Products

# 1. Test Link Token Creation
link_token_response = create_link_token()
print("Link Token Response:")
print(json.dumps(link_token_response, indent=2))

# 2. Create a sandbox public_token
sandbox_request = SandboxPublicTokenCreateRequest(
    institution_id="ins_109508",  # First Platypus Bank (sandbox)
    initial_products=[Products("transactions")],
)
sandbox_response = client.sandbox_public_token_create(sandbox_request)
sandbox_public_token = sandbox_response["public_token"]
print("\nSandbox Public Token:")
print(sandbox_public_token)

# 3. Exchange public_token for access_token
exchange_response = exchange_public_token(sandbox_public_token)
print("\nExchange Public Token Response:")
print(json.dumps(exchange_response, indent=2))

# 4. Fetch transactions and format
def get_transactions_formatted():
    raw_response = get_transactions()

    if "error" in raw_response:
        return {"error": raw_response["error"]}

    transactions = raw_response.get("transactions", [])
    formatted_transactions = []

    for t in transactions:
        formatted_transactions.append({
            "transaction_id": t.get("transaction_id"),
            "account_id": t.get("account_id"),
            "amount": t.get("amount"),
            "merchant_name": t.get("merchant_name") or t.get("name"),
            "category": t.get("category") or [],
            "date": str(t.get("date")),
        })

    return {"transactions": formatted_transactions}

transactions_json = get_transactions_formatted()
print("\nFormatted Transactions:")
print(json.dumps(transactions_json, indent=2))
