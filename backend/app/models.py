from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    brand = Column(String(100), nullable=True)
    model = Column(String(100), nullable=True)
    image_url = Column(String(500), nullable=True)
    msrp = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    listings = relationship("Listing", back_populates="product", cascade="all, delete-orphan")
    price_history = relationship("PriceHistory", back_populates="product", cascade="all, delete-orphan")

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    platform = Column(String(50), nullable=False, index=True)
    seller_name = Column(String(200), nullable=False)
    seller_rating = Column(Float, nullable=True)
    seller_reviews = Column(Integer, default=0)
    seller_verified = Column(Boolean, default=False)
    price = Column(Float, nullable=False)
    original_price = Column(Float, nullable=True)
    url = Column(String(500), nullable=False)
    warranty = Column(String(50), default="none")  # none, shop, official
    return_policy = Column(Boolean, default=False)
    stock_status = Column(String(50), default="unknown")
    scraped_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="listings")

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    platform = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="price_history")
