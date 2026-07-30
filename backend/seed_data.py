from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Product, Listing
import random

engine = create_engine("sqlite:///./dealsentry.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Sample products
products_data = [
    {"name": "Samsung Galaxy A14 6GB/128GB", "category": "Mobile Phones", "brand": "Samsung", "model": "A14", "msrp": 18999},
    {"name": "Xiaomi Redmi Note 12 8GB/128GB", "category": "Mobile Phones", "brand": "Xiaomi", "model": "Note 12", "msrp": 22999},
    {"name": "Walton Primo RX8 Mini", "category": "Mobile Phones", "brand": "Walton", "model": "Primo RX8", "msrp": 12999},
    {"name": "Symphony Z70", "category": "Mobile Phones", "brand": "Symphony", "model": "Z70", "msrp": 11999},
    {"name": "Apple iPhone 15 128GB", "category": "Mobile Phones", "brand": "Apple", "model": "iPhone 15", "msrp": 129999},
    {"name": "Samsung 1.5 Ton Inverter AC", "category": "Home Appliances", "brand": "Samsung", "model": "AR18", "msrp": 72000},
    {"name": "Walton WSI-INVERNA-18A", "category": "Home Appliances", "brand": "Walton", "model": "WSI-18A", "msrp": 58000},
    {"name": "Marcel 1.5 Ton Split AC", "category": "Home Appliances", "brand": "Marcel", "model": "MCS-18", "msrp": 52000},
    {"name": "Sony WH-1000XM5 Headphones", "category": "Electronics", "brand": "Sony", "model": "WH-1000XM5", "msrp": 35000},
    {"name": "JBL Tune 760NC", "category": "Electronics", "brand": "JBL", "model": "Tune 760NC", "msrp": 8500},
    {"name": "HP 15s-fq5009TU Laptop", "category": "Laptops & Accessories", "brand": "HP", "model": "15s-fq5009TU", "msrp": 52000},
    {"name": "Dell Inspiron 15 3520", "category": "Laptops & Accessories", "brand": "Dell", "model": "Inspiron 3520", "msrp": 58000},
    {"name": "Asus VivoBook 15", "category": "Laptops & Accessories", "brand": "Asus", "model": "VivoBook 15", "msrp": 62000},
    {"name": "Anker PowerCore 20000mAh", "category": "Gadgets", "brand": "Anker", "model": "PowerCore 20000", "msrp": 3200},
    {"name": "Xiaomi 20000mAh Power Bank", "category": "Gadgets", "brand": "Xiaomi", "model": "Mi Power Bank 3", "msrp": 2499},
    {"name": "Samsung 43" Crystal UHD 4K TV", "category": "Home Appliances", "brand": "Samsung", "model": "UA43CU7000", "msrp": 45000},
    {"name": "Walton 43" Smart Android TV", "category": "Home Appliances", "brand": "Walton", "model": "W43D2GS", "msrp": 32000},
    {"name": "Logitech MX Master 3S", "category": "Laptops & Accessories", "brand": "Logitech", "model": "MX Master 3S", "msrp": 12500},
    {"name": "Samsung Galaxy Buds2 Pro", "category": "Electronics", "brand": "Samsung", "model": "Buds2 Pro", "msrp": 22000},
    {"name": "Realme C53 6GB/128GB", "category": "Mobile Phones", "brand": "Realme", "model": "C53", "msrp": 14999},
]

products = []
for p in products_data:
    product = Product(**p)
    db.add(product)
    products.append(product)

db.commit()

# Generate listings for each product across platforms
platforms = [
    {"platform": "daraz", "verified_rate": 0.7, "review_base": 200, "rating_base": 4.2, "return_policy": True},
    {"platform": "pickaboo", "verified_rate": 0.9, "review_base": 150, "rating_base": 4.0, "return_policy": True},
    {"platform": "chaldal", "verified_rate": 0.8, "review_base": 80, "rating_base": 3.8, "return_policy": True},
    {"platform": "ajkerdeal", "verified_rate": 0.3, "review_base": 20, "rating_base": 3.2, "return_policy": False},
]

warranty_types = ["none", "shop", "official"]
seller_prefixes = {
    "daraz": ["Daraz Mall", "BD Electronics", "Gadget Zone", "Tech Hub BD"],
    "pickaboo": ["Pickaboo Official", "Electro Mart", "Digital Bangladesh"],
    "chaldal": ["Chaldal", "Daily Needs BD"],
    "ajkerdeal": ["AjkerDeal Seller", "Budget Shop", "Local Trader"],
}

for product in products:
    num_listings = random.randint(2, 4)
    selected_platforms = random.sample(platforms, min(num_listings, len(platforms)))

    for plat in selected_platforms:
        # Price variation: -20% to +15% from MSRP
        variation = random.uniform(0.8, 1.15)
        price = round(product.msrp * variation, 2)

        # Some listings have original price (discount)
        has_discount = random.random() > 0.5
        original_price = round(price * random.uniform(1.1, 1.4), 2) if has_discount else None

        verified = random.random() < plat["verified_rate"]
        reviews = max(0, int(plat["review_base"] * random.uniform(0.1, 2.0)))
        rating = round(min(5.0, max(1.0, plat["rating_base"] + random.uniform(-0.8, 0.8))), 1)

        # Warranty based on platform and verification
        if plat["platform"] == "daraz" and verified:
            warranty = random.choice(["official", "shop"])
        elif plat["platform"] == "pickaboo":
            warranty = random.choice(["official", "shop"])
        else:
            warranty = random.choice(["shop", "none"])

        seller = random.choice(seller_prefixes[plat["platform"]])

        listing = Listing(
            product_id=product.id,
            platform=plat["platform"],
            seller_name=seller,
            seller_rating=rating,
            seller_reviews=reviews,
            seller_verified=verified,
            price=price,
            original_price=original_price,
            url=f"https://{plat['platform']}.com.bd/product/{product.id}",
            warranty=warranty,
            return_policy=plat["return_policy"],
            stock_status=random.choice(["in_stock", "in_stock", "in_stock", "low_stock"]),
        )
        db.add(listing)

db.commit()
db.close()

print("Seed data inserted successfully!")
print(f"Products: {len(products_data)}")
print(f"Listings: generated across {len(platforms)} platforms")
