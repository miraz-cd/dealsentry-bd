import requests
from bs4 import BeautifulSoup
import json
import re
from typing import List, Dict
from app.scrapers.base import BaseScraper

class DarazScraper(BaseScraper):
    BASE_URL = "https://www.daraz.com.bd"

    def search(self, query: str, category: str = None) -> List[Dict]:
        url = f"{self.BASE_URL}/catalog/"
        params = {"q": query}
        if category:
            params["category"] = category

        try:
            response = requests.get(url, headers=self.get_headers(), params=params, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')

            # Try to find script with page data
            scripts = soup.find_all('script')
            listings = []

            for script in scripts:
                text = script.string or ""
                if 'window.pageData' in text or '"itemId"' in text:
                    try:
                        # Extract JSON data
                        match = re.search(r'window\.pageData\s*=\s*({.*?});', text, re.DOTALL)
                        if match:
                            data = json.loads(match.group(1))
                            items = data.get('mods', {}).get('listItems', [])
                            for item in items:
                                listings.append(self.parse_listing(item))
                    except Exception:
                        continue

            # Fallback: parse HTML directly
            if not listings:
                products = soup.select('[data-tracking="product-card"]')
                for product in products:
                    listings.append(self._parse_html_product(product))

            self.sleep()
            return listings

        except Exception as e:
            print(f"Daraz scrape error: {e}")
            return []

    def parse_listing(self, raw_data: Dict) -> Dict:
        price_str = str(raw_data.get('price', '0')).replace(',', '').replace('৳', '')
        original_price_str = str(raw_data.get('originalPrice', '0')).replace(',', '').replace('৳', '')

        try:
            price = float(price_str) if price_str else 0
            original_price = float(original_price_str) if original_price_str else price
        except ValueError:
            price = 0
            original_price = 0

        return {
            "platform": "daraz",
            "seller_name": raw_data.get('sellerName', 'Unknown'),
            "seller_rating": float(raw_data.get('sellerRate', 0)) or None,
            "seller_reviews": int(raw_data.get('sellerReview', 0)) or 0,
            "seller_verified": raw_data.get('sellerBadge', '') == 'Mall',
            "price": price,
            "original_price": original_price if original_price > price else None,
            "url": raw_data.get('productUrl', ''),
            "warranty": "official" if raw_data.get('brandName') in ['Samsung', 'Apple', 'Xiaomi'] else "shop",
            "return_policy": True,
            "stock_status": "in_stock" if raw_data.get('inStock', True) else "out_of_stock",
        }

    def _parse_html_product(self, product) -> Dict:
        name_elem = product.select_one('.name')
        price_elem = product.select_one('.price')
        orig_price_elem = product.select_one('.price-original')

        price_text = price_elem.text.strip() if price_elem else "0"
        price = float(re.sub(r'[^0-9.]', '', price_text)) if price_text else 0

        orig_text = orig_price_elem.text.strip() if orig_price_elem else ""
        original_price = float(re.sub(r'[^0-9.]', '', orig_text)) if orig_text else None

        return {
            "platform": "daraz",
            "seller_name": "Daraz Seller",
            "seller_rating": None,
            "seller_reviews": 0,
            "seller_verified": False,
            "price": price,
            "original_price": original_price,
            "url": "",
            "warranty": "shop",
            "return_policy": True,
            "stock_status": "in_stock",
        }
