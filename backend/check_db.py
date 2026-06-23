from app.core.database import SessionLocal
from app.models.user import User

db = SessionLocal()
user = db.query(User).filter(User.email == 'admin@ahadubank.com').first()
if user:
    print(f"User found: {user.full_name}")
    print(f"Hash: {user.hashed_password}")
    print(f"Hash length: {len(user.hashed_password)}")
else:
    print("User not found")
db.close()
