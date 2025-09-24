from flask import Flask, jsonify
from flask_cors import CORS
from services.forecast import get_forecast_and_recommendations

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

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
