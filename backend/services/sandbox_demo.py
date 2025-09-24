import os

from dotenv import load_dotenv
load_dotenv()

from datetime import datetime, timedelta
from plaid.api import plaid_api
from plaid.model.products import Products
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.country_code import CountryCode
from plaid.api_client import ApiClient
from plaid.configuration import Configuration
import pprint

from format_transactions import map_category  # your category mapping function

# Load environment variables
PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv("PLAID_SECRET")
PLAID_ENV = os.getenv("PLAID_ENV", "sandbox")

# Set base URL based on environment
if PLAID_ENV == "sandbox":
    base_url = "https://sandbox.plaid.com"
elif PLAID_ENV == "development":
    base_url = "https://development.plaid.com"
else:
    base_url = "https://production.plaid.com"

# Plaid configuration
configuration = Configuration(
    host=base_url,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
    }
)

client = plaid_api.PlaidApi(ApiClient(configuration))


def create_sandbox_user():
    """Create a sandbox user and get an access token"""
    request = SandboxPublicTokenCreateRequest(
        institution_id="ins_109508",  # Sandbox bank
        initial_products=[Products("transactions")],
        country_codes=[CountryCode('US')]
    )
    response = client.sandbox_public_token_create(request)
    public_token = response['public_token']

    exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
    exchange_response = client.item_public_token_exchange(exchange_request)
    access_token = exchange_response['access_token']

    print("📌 Public token:", public_token)
    print("🔑 Access token:", access_token)
    return access_token


def fetch_transactions(access_token):
    """Fetch and format transactions for the past 30 days"""
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")

    options = TransactionsGetRequestOptions(count=100, offset=0)
    request = TransactionsGetRequest(
        access_token=access_token,
        start_date=start_date,
        end_date=end_date,
        options=options
    )

    response = client.transactions_get(request)
    raw_transactions = response['transactions']

    formatted = []
    for tx in raw_transactions:
        formatted.append({
            "transaction_id": tx["transaction_id"],
            "amount": tx["amount"],
            "merchant_name": tx["name"],
            "category": [map_category(tx["name"])],
            "date": tx["date"]
        })
    return formatted


if __name__ == "__main__":
    access_token = create_sandbox_user()
    transactions = fetch_transactions(access_token)
    print("📄 Formatted transactions:")
    pprint.pprint(transactions)
