#!/usr/bin/env python
from app.core.database import SessionLocal
from app.models.user import User
from app.models.audit_log import AuditLog
from app.core.security import hash_password, verify_password
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Just clear and recreate users without touching database structure
db = SessionLocal()

try:
    # Delete audit logs first (they reference users)
    db.query(AuditLog).delete()
    db.commit()
    logger.info("Cleared audit logs")
    
    # Delete existing users
    db.query(User).delete()
    db.commit()
    logger.info("Cleared old users")
    
    # Create fresh users with proper password hashing
    users_data = [
        ('Abebe Girma', 'admin@ahadubank.com', 'password123', 'super_admin'),
        ('Tigist Alemu', 'exec@ahadubank.com', 'password123', 'executive_management'),
        ('Dawit Bekele', 'pm@ahadubank.com', 'password123', 'product_manager'),
    ]

    logger.info("Creating users...")
    for full_name, email, password, role in users_data:
        hashed = hash_password(password)
        logger.info(f"  {email}: hash_len={len(hashed)}")
        user = User(
            full_name=full_name,
            email=email,
            hashed_password=hashed,
            role=role,
            is_active=True,
        )
        db.add(user)

    db.commit()
    logger.info(f"Created {len(users_data)} users")

    # Verify password works
    logger.info("Verifying password works...")
    user = db.query(User).filter(User.email == 'admin@ahadubank.com').first()
    if user:
        result = verify_password('password123', user.hashed_password)
        logger.info(f"Password verification for admin@ahadubank.com: {result}")
        if result:
            logger.info("SUCCESS - Passwords are working correctly!")
        else:
            logger.error("FAILED - Password verification failed")
    else:
        logger.error("User not found")

    db.close()
    logger.info("Done")
except Exception as e:
    logger.error(f"Error: {e}", exc_info=True)
    db.close()
