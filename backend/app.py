from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
from services.forecast import get_forecast_and_recommendations
from services.format_transactions import get_formatted_transactions
from services.plaid_server import create_link_token, exchange_public_token, get_transactions as get_plaid_transactions
import json
import os

app = FastAPI(title="FinQuest API", version="1.0.0")

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Budget data model
class BudgetData(BaseModel):
    food: float
    travel: float
    shopping: float
    entertainment: float
    bills: float
    transport: float

@app.get("/forecast")
def get_forecast():
    """
    API endpoint that returns forecast and recommendations
    Returns JSON with 2 keys: forecast and reccs
    """
    try:
        result = get_forecast_and_recommendations()
        return {
            "forecast": result["forecast"],
            "reccs": result["recommendations"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate forecast: {str(e)}")

@app.post("/budget")
def save_budget(budget: BudgetData):
    """
    API endpoint to save user budget data
    """
    try:
        budget_data = budget.dict()
        
        # Save to mock_budgets.json file
        budget_file_path = "data/mock_budgets.json"
        
        # Create the budget structure expected by forecast service
        budget_structure = {
            "budgets": {}
        }
        
        # Map frontend categories to backend format
        category_mapping = {
            "food": "Food",
            "travel": "Transportation", 
            "shopping": "Shopping",
            "entertainment": "Entertainment",
            "bills": "Housing",  # Bills maps to Housing
            "transport": "Transportation"
        }
        
        # Convert frontend data to backend format
        for category, amount in budget_data.items():
            backend_category = category_mapping.get(category, category.capitalize())
            budget_structure["budgets"][backend_category] = float(amount)
        
        # Write to file
        with open(budget_file_path, 'w') as f:
            json.dump(budget_structure, f, indent=2)
        
        return {
            "message": "Budget saved successfully",
            "budgets": budget_structure["budgets"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save budget: {str(e)}")

@app.get("/budget")
def get_budget():
    """
    API endpoint to get current budget data
    """
    try:
        budget_file_path = "data/mock_budgets.json"
        
        if os.path.exists(budget_file_path):
            with open(budget_file_path, 'r') as f:
                budget_data = json.load(f)
            return budget_data["budgets"]
        else:
            # Return default budget if no file exists
            return {
                "Food": 0,
                "Transportation": 0,
                "Shopping": 0,
                "Entertainment": 0,
                "Housing": 0
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get budget: {str(e)}")

@app.get("/transactions")
def get_transactions(use_plaid: bool = True):
    """
    API endpoint that returns formatted transactions - can toggle between Plaid and mock data
    """
    try:
        transactions = get_formatted_transactions(use_plaid=use_plaid)
        return {"transactions": transactions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get transactions: {str(e)}")

@app.get("/health")
def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy"}

# Plaid Integration Endpoints
@app.get("/plaid/link-token")
def create_plaid_link_token():
    """Create Plaid Link token for frontend integration"""
    try:
        result = create_link_token()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create link token: {str(e)}")

@app.post("/plaid/exchange-token")
def exchange_plaid_token(public_token: dict):
    """Exchange public token for access token"""
    try:
        result = exchange_public_token(public_token.get("public_token"))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to exchange token: {str(e)}")

@app.get("/plaid/transactions")
def get_plaid_transaction_data():
    """Get real transactions from Plaid"""
    try:
        result = get_plaid_transactions()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get Plaid transactions: {str(e)}")

@app.post("/plaid/sync-transactions")
def sync_plaid_to_local():
    """Sync Plaid transactions to local mock_transactions.json file"""
    try:
        # Get transactions from Plaid
        plaid_data = get_plaid_transactions()
        
        if "error" in plaid_data:
            raise HTTPException(status_code=400, detail=plaid_data["error"])
        
        # Transform Plaid data to our format
        transactions = []
        for tx in plaid_data.get("transactions", []):
            formatted_tx = {
                "transaction_id": tx.get("transaction_id"),
                "account_id": tx.get("account_id"),
                "amount": abs(tx.get("amount", 0)),  # Make positive for spending
                "merchant_name": tx.get("merchant_name") or tx.get("name", "Unknown"),
                "category": tx.get("category", ["Other"]),
                "date": tx.get("date")
            }
            transactions.append(formatted_tx)
        
        # Save to mock_transactions.json
        transactions_data = {"transactions": transactions}
        with open("data/mock_transactions.json", "w") as f:
            json.dump(transactions_data, f, indent=2)
        
        return {
            "message": f"Successfully synced {len(transactions)} transactions from Plaid",
            "transactions_count": len(transactions)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to sync Plaid transactions: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
