#!/usr/bin/env python
"""
System Verification Script
Checks that all components are working correctly before testing
"""

import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:8000"
API_KEY = "test_token_super_admin"  # Adjust if needed

def check_backend():
    """Check if backend is running and responsive"""
    try:
        resp = requests.get(f"{BASE_URL}/api/v1/products", timeout=5)
        print(f"✓ Backend is running (HTTP {resp.status_code})")
        return True
    except Exception as e:
        print(f"✗ Backend not responding: {e}")
        return False

def get_auth_token():
    """Try to get auth token"""
    try:
        # Try login with default user
        resp = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            json={"username": "admin@ahadubank.com", "password": "password"}
        )
        if resp.status_code == 200:
            data = resp.json()
            token = data.get("access_token")
            print(f"✓ Got authentication token")
            return token
        else:
            print(f"✗ Auth failed: {resp.status_code}")
            return None
    except Exception as e:
        print(f"✗ Auth error: {e}")
        return None

def check_database(token):
    """Check database connection"""
    try:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        resp = requests.get(f"{BASE_URL}/api/v1/products", headers=headers, timeout=5)
        if resp.status_code == 200:
            products = resp.json()
            print(f"✓ Database connected, found {len(products)} products")
            return True
        else:
            print(f"✗ Database check failed: {resp.status_code}")
            return False
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

def check_features(token):
    """Check processed features"""
    try:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        resp = requests.get(f"{BASE_URL}/api/v1/data/features", headers=headers, timeout=5)
        if resp.status_code == 200:
            features = resp.json()
            print(f"✓ ProcessedFeatures table has {len(features)} records")
            return True
        else:
            print(f"✗ Features check failed: {resp.status_code}")
            return False
    except Exception as e:
        print(f"✗ Features error: {e}")
        return False

def check_scores(token):
    """Check scores"""
    try:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        resp = requests.get(f"{BASE_URL}/api/v1/scores", headers=headers, timeout=5)
        if resp.status_code == 200:
            scores = resp.json()
            print(f"✓ Score table has {len(scores)} records")
            return True
        else:
            print(f"✗ Scores check failed: {resp.status_code}")
            return False
    except Exception as e:
        print(f"✗ Scores error: {e}")
        return False

def main():
    print("=" * 60)
    print("AHADU PULSE - System Verification")
    print("=" * 60)
    print(f"Time: {datetime.now().isoformat()}")
    print()
    
    print("1. Checking backend...")
    if not check_backend():
        print("\n✗ Backend is not running!")
        sys.exit(1)
    
    print("\n2. Getting authentication token...")
    token = get_auth_token()
    if not token:
        print("\n⚠ Warning: Could not get auth token, some checks may fail")
    
    print("\n3. Checking database...")
    check_database(token)
    
    print("\n4. Checking processed features...")
    check_features(token)
    
    print("\n5. Checking scores...")
    check_scores(token)
    
    print("\n" + "=" * 60)
    print("✓ System verification complete!")
    print("=" * 60)
    print("\nREADY FOR TESTING")
    print("Next steps:")
    print("  1. Go to http://localhost:3000/dashboard/settings")
    print("  2. Upload DATASET_1_INITIAL.xlsx")
    print("  3. Upload DATASET_2_WEEK2.xlsx")
    print("  4. Upload DATASET_3_WEEK3.xlsx")
    print("  5. Upload DATASET_4_WEEK4.xlsx")
    print("\nVerify that scores change with each upload!")

if __name__ == "__main__":
    main()
