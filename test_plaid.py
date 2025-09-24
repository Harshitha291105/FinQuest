from backend.services.plaid_server import (
    create_link_token,
    exchange_public_token,
    get_transactions,
)

from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.products import Products

from backend.services.plaid_server import client  # use existing Plaid client

# 1. Test Link Token Creation
link_token_response = create_link_token()
print("Link Token Response:")
print(link_token_response)

# 2. Create a sandbox public_token dynamically
sandbox_request = SandboxPublicTokenCreateRequest(
    institution_id="ins_109508",  # Chase (sandbox test institution)
    initial_products=[Products("transactions")],
)
sandbox_response = client.sandbox_public_token_create(sandbox_request)
sandbox_public_token = sandbox_response["public_token"]
print("\nSandbox Public Token:")
print(sandbox_public_token)

# 3. Exchange public_token for access_token
exchange_response = exchange_public_token(sandbox_public_token)
print("\nExchange Public Token Response:")
print(exchange_response)

# 4. Fetch transactions
transactions_response = get_transactions()
print("\nTransactions Response:")
print(transactions_response)
