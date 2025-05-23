#!/bin/bash

# Configuration
REALM=secure-realm
CLIENT_ID=flask-client
CLIENT_SECRET=YOUR_CLIENT_SECRET   # <-- Replace this!
USERNAME=newuser
PASSWORD=newpassword
KEYCLOAK_URL=http://localhost:8080
API_URL=http://localhost:5000

echo "==== 1. Test /public ===="
curl -s "$API_URL/public"
echo -e "\n"

echo "==== 2. Test /protected without token ===="
curl -s "$API_URL/protected"
echo -e "\n"

echo "==== 3. Requesting token ===="
RESPONSE=$(curl -s -X POST "$KEYCLOAK_URL/realms/$REALM/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET" \
  -d "username=$USERNAME" \
  -d "password=$PASSWORD" \
  -d "scope=openid")

# Print full token response
echo "$RESPONSE"

# Extract token manually
ACCESS_TOKEN=$(echo "$RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d':' -f2 | tr -d '"')

if [ -z "$ACCESS_TOKEN" ]; then
  echo "❌ Failed to extract access token."
  exit 1
fi

echo -e "\n✅ Access token extracted."

echo "==== 4. Test /protected with token ===="
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" "$API_URL/protected"
echo -e "\n"
