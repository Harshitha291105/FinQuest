import json
from pathlib import Path
from datetime import datetime
from plaid.api import plaid_api
from plaid.model.products import Products
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.configuration import Configuration
from plaid.api_client import ApiClient
from plaid.configuration import Environment


import os
from dotenv import load_dotenv
from plaid.configuration import Configuration, Environment

load_dotenv()  # loads variables from .env

PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv("PLAID_SECRET")
PLAID_ENV = os.getenv("PLAID_ENV", "sandbox")

environment = Environment.Sandbox if PLAID_ENV == "sandbox" else Environment.Production

configuration = Configuration(
    host=environment,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
    }
)

api_client = ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

ACCESS_TOKEN_FILE = Path(__file__).parent / "access_token.json"


from plaid.model.products import Products
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest

def create_sandbox_user():
    request = SandboxPublicTokenCreateRequest(
        institution_id="ins_109508",  # example sandbox institution
        initial_products=[Products("transactions")]  # <- fix here
    )
    response = client.sandbox_public_token_create(request)
    return response['public_token']




def exchange_public_token(public_token: str) -> str:
    """Exchange public token for access token and store it."""
    request = ItemPublicTokenExchangeRequest(public_token=public_token)
    response = client.item_public_token_exchange(request)
    access_token = response['access_token']

    with open(ACCESS_TOKEN_FILE, "w") as f:
        json.dump({"access_token": access_token}, f)
    
    return access_token


def get_access_token() -> str:
    """Retrieve access token from file."""
    if not ACCESS_TOKEN_FILE.exists():
        raise ValueError("No access token found. Exchange a public_token first.")
    with open(ACCESS_TOKEN_FILE) as f:
        return json.load(f)['access_token']


def get_transactions(start_date: str = None, end_date: str = None):
    """Fetch transactions from Plaid sandbox."""
    access_token = get_access_token()

    if not start_date:
        start_date = (datetime.today().replace(day=1)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.today().strftime("%Y-%m-%d")
    
    request = TransactionsGetRequest(
        access_token=access_token,
        start_date=start_date,
        end_date=end_date,
        options=TransactionsGetRequestOptions()
    )
    response = client.transactions_get(request)
    return response['transactions']
