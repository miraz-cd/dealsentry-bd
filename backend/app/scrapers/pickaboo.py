import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict
from app.scrapers.base import BaseScraper

class PickabooScraper(BaseScraper):
    BASE_URL = "https://www.pickaboo.com"

    def search(self, query: str, category: str = None) -> List[Dict]:
        url = f"{self.BASE_URL}/search"
        params = {"q": query}

        try:
            response = requests.get(url, headers=self.get_headers(), params=params, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')

            listings = []
            products = soup.select('.product-item-info')

            for product in products:
                listings.append(self._parse_html_product(product))

            self.sleep()
            return listings

        except Exception as e:
            print(f"Pickaboo scrape error: {e}")
            return []

    def _parse_html_product(self, product) -> Dict:
        price_elem = product.select_one('.price')
        orig_price_elem = product.select_one('.old-price .price')
        seller_elem = product.select_one('.seller-name')

        price_text = price_elem.text.strip() if price_elem else "0"
        price = float(re.sub(r'[^0-9.]', '', price_text)) if price_text else 0

        orig_text = orig_price_elem.text.strip() if orig_price_elem else ""
        original_price = float(re.sub(r'[^0-9.]', '', orig_text)) if orig_text else None

        return {
            "platform": "pickaboo",
            "seller_name": seller_elem.text.strip() if seller_elem else "Pickaboo",
            "seller_rating": 4.2,
            "seller_reviews": 500,
            "seller_verified": True,
            "price": price,
            "original_price": original_price,
            "url": "",
            "warranty": "official",
            "return_policy": True,
            "stock_status": "in_stock",
        }

    def parse_listing(self, raw_data: Dict) -> Dict:
        return raw_data
