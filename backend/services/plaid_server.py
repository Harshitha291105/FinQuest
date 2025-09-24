import os
from datetime import datetime, timedelta, date
from dotenv import load_dotenv
from plaid.api import plaid_api
from plaid import Configuration, ApiClient
from plaid.configuration import Environment
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.country_code import CountryCode
from plaid.model.products import Products
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

# Load environment variables
load_dotenv()

PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv("PLAID_SECRET")
PLAID_ENV = os.getenv("PLAID_ENV", "sandbox")

# Map environment names
env_mapping = {
    "sandbox": Environment.Sandbox,
    "development": Environment.Sandbox,   # Development = Sandbox
    "production": Environment.Production,
}

# Configure Plaid client
configuration = Configuration(
    host=env_mapping[PLAID_ENV],
    api_key={
        "clientId": PLAID_CLIENT_ID,
        "secret": PLAID_SECRET,
    },
)
api_client = ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)


# Step 1: Create link token
def create_link_token():
    try:
        request = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(client_user_id="user-id-123"),
            client_name="FinQuest",
            products=[Products("transactions")],
            country_codes=[CountryCode("US")],
            language="en",
        )
        response = client.link_token_create(request)
        return response.to_dict()
    except Exception as e:
        return {"error": str(e)}


# Step 2: Exchange public token for access token
def exchange_public_token(public_token):
    try:
        request = ItemPublicTokenExchangeRequest(public_token=public_token)
        response = client.item_public_token_exchange(request)
        data = response.to_dict()

        # Save access token locally for demo
        os.makedirs("data", exist_ok=True)
        with open("data/access_token.txt", "w") as f:
            f.write(data["access_token"])

        return data
    except Exception as e:
        return {"error": str(e)}


# Step 3: Fetch transactions
def get_transactions():
    try:
        with open("data/access_token.txt") as f:
            access_token = f.read().strip()

        start_date = (datetime.now() - timedelta(days=30)).date()
        end_date = datetime.now().date()

        request = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date,
        )
        response = client.transactions_get(request)
        return response.to_dict()
    except FileNotFoundError:
        return {"error": "No access_token found. Please exchange a public_token first."}
    except Exception as e:
        return {"error": str(e)}