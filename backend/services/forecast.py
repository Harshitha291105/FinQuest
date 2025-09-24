import json
from datetime import datetime
from . import recommendations  # relative import
from .format_transactions import get_formatted_transactions

<<<<<<< HEAD
def get_forecast_and_recommendations(transactions_file="data/mock_transactions.json",
                                     budgets_file="data/mock_budgets.json"):
    # 1. Load transactions and budgets
    with open(transactions_file) as f:
        transactions = json.load(f)["transactions"]
=======
def get_forecast_and_recommendations(budgets_file="data/mock_budgets.json"):
    # ------------------------------
    # 1. Load transactions and budgets
    # ------------------------------
    # Use formatted transactions from format_transactions service
    transactions = get_formatted_transactions()
>>>>>>> f91c72672ce134e20e9341193bd160f07981f864

    with open(budgets_file) as f:
        budgets = json.load(f)["budgets"]

    # 2. Aggregate spending by category
    spending = {}
    for tx in transactions:
        category = tx["category"][0]  # top-level category
        amount = tx["amount"]
        spending[category] = spending.get(category, 0) + amount

    # 3. Forecasting
    today = datetime.today()
    days_in_month = 30  # approximate
    days_elapsed = today.day

    projection = {}
    for cat, spent in spending.items():
        projected = (spent / days_elapsed) * days_in_month  # linear extrapolation
        budget = budgets.get(cat, 0)
        projection[cat] = {
            "spent_so_far": round(spent, 2),
            "budget": budget,
            "projected_end_of_month": round(projected, 2),
            "status": "on track" if projected <= budget else "over budget"
        }

    # 4. Generate recommendations
    recommendation_list = recommendations.generate_recommendations(projection)

    # 5. Return results (instead of writing to disk)
    return {
        "forecast": projection,
        "recommendations": recommendation_list
    }
