#!/usr/bin/env python
import httpx
import json

client = httpx.Client()

# Test with different credential combinations
test_cases = [
    {'email': 'admin@ahadubank.com', 'password': 'password123'},
    {'email': 'admin@ahadubank.com', 'password': 'admin'},
    {'email': 'admin@ahadubank.com', 'password': 'Admin@123'},
]

for test in test_cases:
    print(f"\nTesting: {test['email']} / {test['password']}")
    r = httpx.post('http://127.0.0.1:5000/api/auth/login', json=test)
    print(f"Status: {r.status_code}")
    data = r.json()
    if r.status_code == 200:
        print(f"✓ SUCCESS - {data.get('full_name')}")
    else:
        print(f"✗ FAILED - {data.get('detail')}")

# Also show all users in database
print("\n\n=== DATABASE USERS ===")
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import verify_password

db = SessionLocal()
users = db.query(User).all()
print(f"Total users: {len(users)}")
for u in users:
    # Test if password123 works
    result = verify_password('password123', u.hashed_password)
    print(f"  {u.email}: hash_ok={result}, role={u.role}")
db.close()
