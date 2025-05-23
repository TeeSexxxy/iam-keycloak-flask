import os
from flask import Flask, request, jsonify
from jose import jwt
import requests

app = Flask(__name__)

#OAuth 2.0 / Keycloak configuration
#KEYCLOAK_URL = 'http://localhost:8080/realms/secure-realm'
KEYCLOAK_URL = 'http://keycloak:8080/realms/secure-realm'
KEYCLOAK_CLIENT_ID = "testuser"
KEYCLOAK_SERVER_URL = os.environ.get("KEYCLOAK_SERVER_URL", "http://localhost:8080")

#KEYCLOAK_CLIENT_ID = os.environ.get("KEYCLOAK_CLIENT_ID", "your-client-id")
#KEYCLOAK_SERVER_URL = os.environ.get("KEYCLOAK_SERVER_URL", "http://localhost:8080")
JWKS_URL = f'{KEYCLOAK_URL}/protocol/openid-connect/certs'

import time
import requests

JWKS_URL = "http://keycloak:8080/realms/secure-realm/protocol/openid-connect/certs"

for _ in range(10):
    try:
        response = requests.get(JWKS_URL)
        if response.status_code == 200:
            jwks = response.json()
            break
    except requests.exceptions.ConnectionError:
        print("Keycloak not ready, retrying...")
    time.sleep(3)
else:
    raise Exception("Keycloak not available after retries")





# Get public keys for token verification
jwks = requests.get(JWKS_URL).json()

def get_public_key(token):
    unverified_header = jwt.get_unverified_header(token)
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            return jwt.algorithms.RSAAlgorithm.from_jwk(key)
    return None

def token_required(f):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return jsonify({"error": "Missing Authorization header"}), 401

        try:
            token = auth_header.split()[1]
            public_key = get_public_key(token)
            decoded = jwt.decode(token, public_key, algorithms=['RS256'], audience='flask-client')
            request.user = decoded
        except Exception as e:
            return jsonify({"error": str(e)}), 401

        return f(*args, **kwargs)
    return wrapper

@app.route('/public')
def public():
    return jsonify(message="This is a public endpoint")

@app.route('/protected')
@token_required
def protected():
    return jsonify(message=f"Welcome, {request.user.get('preferred_username')}!")

@app.route("/health")
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
