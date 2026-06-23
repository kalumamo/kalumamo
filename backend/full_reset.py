#!/usr/bin/env python
"""Complete database reset - drop all tables and recreate with fresh data"""
from app.core.database import Base, engine, SessionLocal
from app.models.user import User
from app.models.audit_log import AuditLog
from app.core.security import hash_password, verify_password
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Drop ALL tables completely
    logger.info("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)

    # Recreate all tables from scratch
    logger.info("Creating all tables...")
    Base.metadata.create_all(bind=engine)

    # Create fresh users
    db = SessionLocal()
    users_data = [
        ('Abebe Girma', 'admin@ahadubank.com', 'Admin@123', 'super_admin'),
        ('Tigist Alemu', 'exec@ahadubank.com', 'Exec@123', 'executive_management'),
        ('Dawit Bekele', 'pm@ahadubank.com', 'PM@12345', 'product_manager'),
    ]

    logger.info("Creating users...")
    for full_name, email, password, role in users_data:
        hashed = hash_password(password)
        logger.info(f"  {email}: hash={hashed[:20]}... (len={len(hashed)})")
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

    # Verify each user
    logger.info("\nVerifying passwords...")
    for full_name, email, password, role in users_data:
        user = db.query(User).filter(User.email == email).first()
        result = verify_password(password, user.hashed_password)
        logger.info(f"  {email}: {result}")
        if not result:
            logger.error(f"    ERROR: Password verification failed for {email}!")

    db.close()
    logger.info("\n✓ Complete clean database setup finished!")
    
except Exception as e:
    logger.error(f"Error: {e}", exc_info=True)
