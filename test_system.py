#!/usr/bin/env python
"""Test system endpoints to verify backend is working correctly."""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

print("\n" + "="*70)
print("AHADU PULSE SYSTEM CHECK")
print("="*70)

# 1. Health check
print("\n1. Health Check")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    if response.status_code == 200:
        print("   ✓ Backend is running on http://127.0.0.1:5000")
        print(f"   Response: {response.json()}")
    else:
        print(f"   ✗ Unexpected status: {response.status_code}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# 2. Login test
print("\n2. Login Test")
try:
    login_data = {
        "email": "admin@ahadubank.com",
        "password": "Admin@123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data, timeout=5)
    if response.status_code == 200:
        token_data = response.json()
        print(f"   ✓ Login successful")
        print(f"   User: {token_data.get('full_name')} ({token_data.get('role')})")
        print(f"   Email: {token_data.get('email')}")
        
        # Save token for further tests
        access_token = token_data.get("access_token")
        
        # 3. Get alerts
        print("\n3. Alerts Endpoint")
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(f"{BASE_URL}/api/alerts/?limit=3", headers=headers, timeout=5)
            if response.status_code == 200:
                alerts = response.json()
                print(f"   ✓ Alerts loaded: {len(alerts)} alerts retrieved")
                if alerts:
                    print(f"   Sample alert: {alerts[0].get('title')}")
            else:
                print(f"   ✗ Status {response.status_code}: {response.text}")
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        # 4. Get products
        print("\n4. Products Endpoint")
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(f"{BASE_URL}/api/products/?limit=3", headers=headers, timeout=5)
            if response.status_code == 200:
                products = response.json()
                print(f"   ✓ Products loaded: {len(products)} products retrieved")
                if products:
                    print(f"   Sample product: {products[0].get('name')}")
            else:
                print(f"   ✗ Status {response.status_code}: {response.text}")
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        # 5. Get recommendations
        print("\n5. Recommendations Endpoint")
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(f"{BASE_URL}/api/recommendations/?limit=3", headers=headers, timeout=5)
            if response.status_code == 200:
                recs = response.json()
                print(f"   ✓ Recommendations loaded: {len(recs)} recommendations retrieved")
                if recs:
                    print(f"   Sample recommendation: {recs[0].get('title')}")
            else:
                print(f"   ✗ Status {response.status_code}: {response.text}")
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        # 6. Get scores
        print("\n6. Scores Endpoint")
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(f"{BASE_URL}/api/scores/?limit=3", headers=headers, timeout=5)
            if response.status_code == 200:
                scores = response.json()
                print(f"   ✓ Scores loaded: {len(scores)} scores retrieved")
                if scores:
                    print(f"   Sample score: {scores[0].get('performance_score')}")
            else:
                print(f"   ✗ Status {response.status_code}: {response.text}")
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        # 7. Get predictions
        print("\n7. Predictions Endpoint")
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(f"{BASE_URL}/api/ml/predictions/?limit=3", headers=headers, timeout=5)
            if response.status_code == 200:
                predictions = response.json()
                print(f"   ✓ Predictions loaded: {len(predictions)} predictions retrieved")
                if predictions:
                    print(f"   Sample prediction: {predictions[0].get('predicted_score')}")
            else:
                print(f"   ✗ Status {response.status_code}: {response.text}")
        except Exception as e:
            print(f"   ✗ Error: {e}")
            
    else:
        print(f"   ✗ Login failed with status {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "="*70)
print("SYSTEM CHECK COMPLETE")
print("="*70 + "\n")
