#!/usr/bin/env python
"""Test data upload functionality."""

import requests
import io
import csv
from datetime import date

# Login
print("="*80)
print("TESTING DATA UPLOAD FUNCTIONALITY")
print("="*80)

print("\n1. Logging in...")
login_response = requests.post(
    "http://localhost:8000/api/auth/login",
    json={
        "email": "admin@ahadubank.com",
        "password": "Admin@123"
    }
)

if login_response.status_code != 200:
    print(f"❌ Login failed: {login_response.status_code}")
    print(login_response.text)
    exit(1)

token = login_response.json()["access_token"]
print(f"✅ Login successful, token: {token[:20]}...")

# Create test CSV
print("\n2. Creating test CSV data...")
csv_data = """product_code,period_date,total_users,active_users,new_users,churned_users,total_transactions,successful_transactions,failed_transactions,transaction_volume,total_revenue,fee_revenue,uptime_percentage,downtime_hours,avg_response_time_ms,api_error_rate,total_complaints,resolved_complaints,csat_score,fraud_event_count,security_incident_count
MOBILE_01,2026-07-31,850000,561000,8500,5100,2500000,2375000,125000,6200000000,40000000,2400000,98.5,36,350,1.5,150,132,4.2,5,0
CARD_01,2026-07-31,650000,442000,6500,3250,1800000,1742400,57600,7000000000,60000000,3000000,98.3,48,400,1.8,100,94,4.0,4,0
"""

print("✅ CSV content created")

# Upload file
print("\n3. Uploading CSV file...")
files = {
    'file': ('test_data.csv', io.BytesIO(csv_data.encode()), 'text/csv')
}
headers = {
    'Authorization': f'Bearer {token}'
}

upload_response = requests.post(
    "http://localhost:8000/api/data/upload",
    headers=headers,
    files=files
)

print(f"Upload Response Status: {upload_response.status_code}")
print(f"Response Body:")

if upload_response.status_code == 200:
    response_data = upload_response.json()
    print(f"✅ UPLOAD SUCCESSFUL!")
    print(f"   Status: {response_data.get('status')}")
    print(f"   Rows imported: {response_data.get('rows_imported')}")
    print(f"   Rows failed: {response_data.get('rows_failed')}")
    print(f"   Features computed: {response_data.get('features_computed')}")
    print(f"   Products scored: {response_data.get('products_scored')}")
    print(f"\n   Message: {response_data.get('message')}")
    
    if response_data.get('products_scored'):
        print(f"\n   Scored products:")
        for product in response_data.get('products_scored', []):
            print(f"     - Product {product['product_id']}: Score {product['score']} ({product['tier']})")
else:
    print(f"❌ UPLOAD FAILED!")
    print(f"   Error: {upload_response.text}")

print("\n" + "="*80)
print("TEST COMPLETE")
print("="*80)
