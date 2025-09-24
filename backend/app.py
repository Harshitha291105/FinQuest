from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
from services.forecast import get_forecast_and_recommendations
from services.format_transactions import get_formatted_transactions
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
def get_transactions():
    """
    API endpoint that returns formatted transactions
    """
    try:
        transactions = get_formatted_transactions()
        return {"transactions": transactions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get transactions: {str(e)}")

@app.get("/health")
def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
