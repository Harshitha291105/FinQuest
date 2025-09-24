# backend/api.py
from fastapi import FastAPI
from backend.services.format_transactions import get_formatted_transactions

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to FinQuest API 🚀"}

@app.get("/transactions")
def read_transactions():
    """Return all formatted transactions"""
    return {"transactions": get_formatted_transactions()}
