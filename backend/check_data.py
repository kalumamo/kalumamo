#!/usr/bin/env python
import httpx
import json

client = httpx.Client()

# Get auth token first
print("Getting auth token...")
r = client.post('http://127.0.0.1:5000/api/auth/login', json={'email': 'admin@ahadubank.com', 'password': 'password123'})
token = r.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}
print(f"✓ Token obtained\n")

# Test products endpoint
print("=== PRODUCTS ===")
r = client.get('http://127.0.0.1:5000/api/products', headers=headers)
print(f"Status: {r.status_code}")
products = r.json()
print(f"Products count: {len(products)}")
if products:
    print(f"First product: {products[0].get('name')}")
else:
    print("No products found")

# Test scores endpoint
print("\n=== SCORES ===")
r = client.get('http://127.0.0.1:5000/api/scores', headers=headers)
print(f"Status: {r.status_code}")
scores = r.json()
print(f"Scores count: {len(scores)}")

# Test alerts endpoint
print("\n=== ALERTS ===")
r = client.get('http://127.0.0.1:5000/api/alerts', headers=headers)
print(f"Status: {r.status_code}")
alerts = r.json()
print(f"Alerts count: {len(alerts)}")

# Test rankings endpoint
print("\n=== RANKINGS ===")
r = client.get('http://127.0.0.1:5000/api/rankings', headers=headers)
print(f"Status: {r.status_code}")
rankings = r.json()
print(f"Rankings count: {len(rankings)}")

# Check database directly
print("\n=== DATABASE CHECK ===")
from app.core.database import SessionLocal
from app.models.product import Product
from app.models.ml_models import Score
from app.models.alerts import Alert

db = SessionLocal()
product_count = db.query(Product).count()
score_count = db.query(Score).count()
alert_count = db.query(Alert).count()

print(f"Products in DB: {product_count}")
print(f"Scores in DB: {score_count}")
print(f"Alerts in DB: {alert_count}")

db.close()
