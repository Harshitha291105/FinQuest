from flask import Flask, jsonify, request
from flask_cors import CORS
from services.forecast import get_forecast_and_recommendations
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

@app.route('/forecast', methods=['GET'])
def get_forecast():
    """
    API endpoint that returns forecast and recommendations
    Returns JSON with 2 keys: forecast and reccs
    """
    try:
        result = get_forecast_and_recommendations()
        return jsonify({
            "forecast": result["forecast"],
            "reccs": result["recommendations"]
        })
    except Exception as e:
        return jsonify({
            "error": f"Failed to generate forecast: {str(e)}"
        }), 500

@app.route('/budget', methods=['POST'])
def save_budget():
    """
    API endpoint to save user budget data
    Expects JSON with budget categories and amounts
    """
    try:
        budget_data = request.get_json()
        
        # Validate the data
        if not budget_data:
            return jsonify({"error": "No budget data provided"}), 400
        
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
        
        return jsonify({
            "message": "Budget saved successfully",
            "budgets": budget_structure["budgets"]
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to save budget: {str(e)}"
        }), 500

@app.route('/budget', methods=['GET'])
def get_budget():
    """
    API endpoint to get current budget data
    """
    try:
        budget_file_path = "data/mock_budgets.json"
        
        if os.path.exists(budget_file_path):
            with open(budget_file_path, 'r') as f:
                budget_data = json.load(f)
            return jsonify(budget_data["budgets"])
        else:
            # Return default budget if no file exists
            return jsonify({
                "Food": 0,
                "Transportation": 0,
                "Shopping": 0,
                "Entertainment": 0,
                "Housing": 0
            })
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get budget: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
