#!/usr/bin/env python
import httpx

# Get token
r = httpx.post('http://127.0.0.1:5000/api/auth/login', json={'email': 'admin@ahadubank.com', 'password': 'password123'})
print(f"Login status: {r.status_code}")
data = r.json()
print(f"Login response: {data}")

token = data.get('access_token')
if not token:
    print("No token received!")
    exit(1)

headers = {'Authorization': f'Bearer {token}'}

# Test the bulk predictions endpoint
print("\nTesting /api/ml/predictions/bulk?product_ids=1")
r = httpx.get('http://127.0.0.1:5000/api/ml/predictions/bulk?product_ids=1', headers=headers)
print(f'Status: {r.status_code}')
print(f'Response: {r.json() if r.status_code == 200 else r.text}')
