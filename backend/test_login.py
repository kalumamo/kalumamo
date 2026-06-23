#!/usr/bin/env python
import httpx
import json

# Test if server is running
try:
    client = httpx.Client(timeout=5.0)
    response = client.get('http://127.0.0.1:5000/health')
    print(f"Health check - Status: {response.status_code}\n")
except Exception as e:
    print(f"Server not running. Starting it...\n")
    exit(1)

# Test login
try:
    payload = {'email': 'admin@ahadubank.com', 'password': 'password123'}
    print(f"Sending login request for admin@ahadubank.com")
    
    response = client.post(
        'http://127.0.0.1:5000/api/auth/login',
        json=payload
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"SUCCESS!")
        print(f"  User: {data['full_name']} ({data['email']})")
        print(f"  Role: {data['role']}")
        print(f"  Token: {data['access_token'][:30]}...")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Login error: {e}")
