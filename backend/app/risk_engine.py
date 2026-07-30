from typing import Optional, List
from dataclasses import dataclass
from app.schemas import ListingResponse

@dataclass
class RiskFactors:
    price_reality: int = 0
    seller_trust: int = 0
    return_policy: int = 0
    warranty: int = 0
    platform_safety: int = 0

class RiskEngine:
    @staticmethod
    def get_market_average(listings: List[ListingResponse]) -> float:
        if not listings:
            return 0.0
        return sum(l.price for l in listings) / len(listings)

    @classmethod
    def calculate_risk(cls, listing: ListingResponse, all_listings: List[ListingResponse]) -> dict:
        factors = RiskFactors()
        market_avg = cls.get_market_average(all_listings)

        # Price Reality (30%)
        if market_avg > 0:
            ratio = listing.price / market_avg
            if ratio < 0.5:
                factors.price_reality = 30
            elif ratio < 0.7:
                factors.price_reality = 20
            elif ratio < 0.85:
                factors.price_reality = 10

        # Seller Trust (25%)
        if listing.seller_reviews < 50:
            factors.seller_trust += 15
        if listing.seller_rating and listing.seller_rating < 3.5:
            factors.seller_trust += 10
        if not listing.seller_verified:
            factors.seller_trust += 10
        factors.seller_trust = min(factors.seller_trust, 25)

        # Return Policy (15%)
        if not listing.return_policy:
            factors.return_policy = 15

        # Warranty (15%)
        if listing.warranty == "none":
            factors.warranty = 15
        elif listing.warranty == "shop":
            factors.warranty = 8

        # Platform Safety (15%)
        platform = listing.platform.lower()
        if platform == "facebook" and not listing.seller_verified:
            factors.platform_safety = 15
        elif platform == "daraz" and listing.seller_verified:
            factors.platform_safety = -10
        elif platform in ["ajkerdeal", "facebook"]:
            factors.platform_safety = 10

        total_score = max(0, min(100, 
            factors.price_reality + factors.seller_trust + 
            factors.return_policy + factors.warranty + factors.platform_safety
        ))

        return {
            "score": total_score,
            "factors": {
                "price_reality": factors.price_reality,
                "seller_trust": factors.seller_trust,
                "return_policy": factors.return_policy,
                "warranty": factors.warranty,
                "platform_safety": factors.platform_safety,
            }
        }

    @staticmethod
    def get_risk_category(score: int) -> tuple:
        if score <= 20:
            return "LOW RISK", "green"
        elif score <= 45:
            return "MODERATE", "yellow"
        elif score <= 70:
            return "HIGH RISK", "orange"
        else:
            return "VERY HIGH", "red"

    @staticmethod
    def get_recommendation(score: int, savings_percent: float) -> tuple:
        if score <= 20 and savings_percent >= 15:
            return "STRONG BUY", "✅"
        elif score <= 35 and savings_percent >= 5:
            return "BUY", "✅"
        elif score <= 50:
            return "CAUTIOUS BUY", "⚠️"
        elif score <= 70:
            return "NOT RECOMMENDED", "❌"
        else:
            return "AVOID", "🚫"

    @classmethod
    def analyze_deal(cls, listing: ListingResponse, all_listings: List[ListingResponse], msrp: Optional[float] = None):
        risk = cls.calculate_risk(listing, all_listings)
        score = risk["score"]
        category, color = cls.get_risk_category(score)

        market_avg = cls.get_market_average(all_listings)
        reference_price = msrp or market_avg
        savings_bdt = max(0, reference_price - listing.price) if reference_price > listing.price else 0
        savings_percent = (savings_bdt / reference_price * 100) if reference_price > 0 else 0

        recommendation, icon = cls.get_recommendation(score, savings_percent)

        return {
            "score": score,
            "category": category,
            "color": color,
            "factors": risk["factors"],
            "recommendation": recommendation,
            "recommendation_icon": icon,
            "savings_bdt": round(savings_bdt, 2),
            "savings_percent": round(savings_percent, 1),
        }
