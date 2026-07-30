import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict
from app.scrapers.base import BaseScraper

class ChaldalScraper(BaseScraper):
    BASE_URL = "https://chaldal.com"

    def search(self, query: str, category: str = None) -> List[Dict]:
        url = f"{self.BASE_URL}/search/{query.replace(' ', '%20')}"

        try:
            response = requests.get(url, headers=self.get_headers(), timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')

            listings = []
            products = soup.select('.product')

            for product in products:
                listings.append(self._parse_html_product(product))

            self.sleep()
            return listings

        except Exception as e:
            print(f"Chaldal scrape error: {e}")
            return []

    def _parse_html_product(self, product) -> Dict:
        price_elem = product.select_one('.price')
        name_elem = product.select_one('.name')

        price_text = price_elem.text.strip() if price_elem else "0"
        price = float(re.sub(r'[^0-9.]', '', price_text)) if price_text else 0

        return {
            "platform": "chaldal",
            "seller_name": "Chaldal",
            "seller_rating": 4.0,
            "seller_reviews": 200,
            "seller_verified": True,
            "price": price,
            "original_price": None,
            "url": "",
            "warranty": "shop",
            "return_policy": True,
            "stock_status": "in_stock",
        }

    def parse_listing(self, raw_data: Dict) -> Dict:
        return raw_data
