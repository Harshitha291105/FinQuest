from fastapi import FastAPI
from .services.plaid_client import create_sandbox_user, exchange_public_token, get_transactions

app = FastAPI()


@app.get("/")
def root():
    return {"message": "FinQuest API is running!"}


@app.get("/create_sandbox_user")
def create_user():
    public_token = create_sandbox_user()
    return {"public_token": public_token}


@app.post("/exchange_token/{public_token}")
def exchange_token(public_token: str):
    access_token = exchange_public_token(public_token)
    return {"access_token": access_token}


@app.get("/transactions")
def transactions():
    try:
        txns = get_transactions()
        return {"transactions": txns}
    except ValueError as e:
        return {"error": str(e)}
