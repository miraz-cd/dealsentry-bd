from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Product, Listing, PriceHistory
from app.schemas import DealResponse, StatsResponse, ListingResponse, ProductResponse
from app.risk_engine import RiskEngine
from app.scrapers.daraz import DarazScraper
from app.scrapers.pickaboo import PickabooScraper
from app.scrapers.chaldal import ChaldalScraper
from sqlalchemy import func

router = APIRouter(prefix="/api", tags=["deals"])

@router.get("/deals", response_model=List[DealResponse])
def get_deals(
    category: Optional[str] = Query(None),
    platform: Optional[str] = Query(None),
    sort: Optional[str] = Query("best_value"),  # lowest_price, best_value, lowest_risk, biggest_savings
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    if category:
        query = query.filter(Product.category.ilike(f"%{category}%"))
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    products = query.all()
    results = []

    for product in products:
        listings_query = db.query(Listing).filter(Listing.product_id == product.id)
        if platform:
            listings_query = listings_query.filter(Listing.platform == platform)
        listings = listings_query.all()

        if not listings:
            continue

        listing_responses = [ListingResponse.model_validate(l) for l in listings]
        best_price = min(l.price for l in listings)
        average_price = sum(l.price for l in listings) / len(listings)
        price_spread = max(l.price for l in listings) - best_price

        # Analyze each listing and pick the best one for the card
        best_listing = min(listings, key=lambda x: x.price)
        best_listing_resp = ListingResponse.model_validate(best_listing)
        risk = RiskEngine.analyze_deal(best_listing_resp, listing_responses, product.msrp)

        results.append({
            "product": ProductResponse.model_validate(product),
            "listings": listing_responses,
            "risk_analysis": risk,
            "best_price": best_price,
            "average_price": round(average_price, 2),
            "price_spread": round(price_spread, 2),
            "platform_count": len(set(l.platform for l in listings)),
        })

    # Sorting
    if sort == "lowest_price":
        results.sort(key=lambda x: x["best_price"])
    elif sort == "lowest_risk":
        results.sort(key=lambda x: x["risk_analysis"]["score"])
    elif sort == "biggest_savings":
        results.sort(key=lambda x: x["risk_analysis"]["savings_bdt"], reverse=True)
    else:  # best_value
        results.sort(key=lambda x: (x["risk_analysis"]["score"], -x["risk_analysis"]["savings_bdt"]))

    return results

@router.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    total_products = db.query(Product).count()
    total_listings = db.query(Listing).count()

    # Calculate average risk (simplified)
    all_listings = db.query(Listing).all()
    avg_risk = 35.0  # placeholder

    # Best deals = products with savings > 1000
    best_deals = db.query(Listing).filter(Listing.original_price != None).count()

    # Platform breakdown
    platform_counts = db.query(Listing.platform, func.count(Listing.id)).group_by(Listing.platform).all()
    platform_breakdown = {p: c for p, c in platform_counts}

    return {
        "items_scanned": total_listings,
        "best_deals_found": best_deals,
        "average_risk": round(avg_risk, 1),
        "total_potential_savings": 0.0,
        "platform_breakdown": platform_breakdown,
    }

@router.post("/scrape")
def trigger_scrape(query: str, platforms: List[str] = Query(["daraz"]), db: Session = Depends(get_db)):
    scrapers = {
        "daraz": DarazScraper(),
        "pickaboo": PickabooScraper(),
        "chaldal": ChaldalScraper(),
    }

    results = []
    for platform in platforms:
        if platform in scrapers:
            try:
                data = scrapers[platform].search(query)
                results.append({"platform": platform, "count": len(data)})
            except Exception as e:
                results.append({"platform": platform, "error": str(e)})

    return {"status": "completed", "results": results}

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Product.category).distinct().all()
    return [c[0] for c in categories]
