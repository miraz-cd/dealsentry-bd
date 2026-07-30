from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    category: str
    brand: Optional[str] = None
    model: Optional[str] = None
    image_url: Optional[str] = None
    msrp: Optional[float] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ListingBase(BaseModel):
    platform: str
    seller_name: str
    seller_rating: Optional[float] = None
    seller_reviews: int = 0
    seller_verified: bool = False
    price: float
    original_price: Optional[float] = None
    url: str
    warranty: str = "none"
    return_policy: bool = False
    stock_status: str = "unknown"

class ListingCreate(ListingBase):
    product_id: int

class ListingResponse(ListingBase):
    id: int
    product_id: int
    scraped_at: datetime

    class Config:
        from_attributes = True

class PriceHistoryBase(BaseModel):
    platform: str
    price: float
    date: datetime

class PriceHistoryCreate(PriceHistoryBase):
    product_id: int

class PriceHistoryResponse(PriceHistoryBase):
    id: int
    product_id: int

    class Config:
        from_attributes = True

class RiskAnalysis(BaseModel):
    score: int = Field(..., ge=0, le=100)
    category: str
    color: str
    factors: dict
    recommendation: str
    recommendation_icon: str
    savings_bdt: float
    savings_percent: float

class DealResponse(BaseModel):
    product: ProductResponse
    listings: List[ListingResponse]
    risk_analysis: RiskAnalysis
    best_price: float
    average_price: float
    price_spread: float
    platform_count: int

class StatsResponse(BaseModel):
    items_scanned: int
    best_deals_found: int
    average_risk: float
    total_potential_savings: float
    platform_breakdown: dict
