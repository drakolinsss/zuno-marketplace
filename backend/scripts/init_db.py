from sqlalchemy.orm import Session
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.models import Base, Product, User
from config import engine, get_db
import logging

def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = next(get_db())
    
    # Create a sample seller
    sample_seller = User(
        username="demo_seller",
        email="seller@example.com",
        pgp_key="SAMPLE_PGP_KEY",
        seller_info="Experienced digital service provider",
        reputation_score=4.5
    )
    
    db.add(sample_seller)
    db.commit()
    db.refresh(sample_seller)
    
    # Create sample products
    sample_products = [
        {
            "name": "Premium VPN Service",
            "description": "Secure, high-speed VPN service with servers worldwide. Perfect for privacy-conscious users.",
            "price": 9.99,
            "category": "service",
            "stock": 999,
            "seller_id": sample_seller.id
        },
        {
            "name": "Secure Cloud Storage",
            "description": "End-to-end encrypted cloud storage solution with 1TB space.",
            "price": 19.99,
            "category": "service",
            "stock": 500,
            "seller_id": sample_seller.id
        },
        {
            "name": "Password Manager Pro",
            "description": "Advanced password management tool with secure sharing and team features.",
            "price": 4.99,
            "category": "software",
            "stock": 1000,
            "seller_id": sample_seller.id
        }
    ]
    
    for product_data in sample_products:
        product = Product(**product_data)
        db.add(product)
    
    db.commit()
    logging.info("Sample data initialized successfully")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_db()
