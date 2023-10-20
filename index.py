from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GODADDY_URL = os.environ.get('GODADDY_API_URL', 'https://api.ote-godaddy.com')
AUTHORIZATION_HEADER = os.environ.get('GODADDY_AUTH_HEADER')

@app.route('/check-domain', methods=['POST'])
def check_domain():
    data = request.json
    headers = {
        'Content-Type': 'application/json',
        'Authorization': AUTHORIZATION_HEADER
    }

    response = requests.post(GODADDY_URL + "/v1/domains/available?checkType=FAST", headers=headers, json=data)

    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(port=5000)
