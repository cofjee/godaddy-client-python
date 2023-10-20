
import logging
from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

GODADDY_URL = os.environ.get('GODADDY_API_URL', 'https://api.godaddy.com')
AUTHORIZATION_HEADER = os.environ.get('GODADDY_AUTH_HEADER')

@app.route('/check-domain', methods=['POST'])
def check_domain():
    data = request.json
    request_headers = data.get('headers', {})
    log_message = f"Received request to check domains: {data} | "

    headers = {
        'Content-Type': 'application/json',
        'Authorization': request_headers.get("Authorization", AUTHORIZATION_HEADER)
    }

    try:
        response = requests.post(GODADDY_URL + "/v1/domains/available?checkType=FAST", headers=headers, json=data)
        log_message += GODADDY_URL
        log_message += f"Received response from GoDaddy API: {response.json()}"
        logger.info(log_message)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        log_message += f"Error while calling GoDaddy API: {e}"
        logger.error(log_message)
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(port=5000)
