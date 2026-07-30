from abc import ABC, abstractmethod
from typing import List, Dict
import time
import random
from fake_useragent import UserAgent

class BaseScraper(ABC):
    def __init__(self, delay: int = 2):
        self.delay = delay
        self.ua = UserAgent()

    def get_headers(self):
        return {
            "User-Agent": self.ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

    def sleep(self):
        time.sleep(self.delay + random.uniform(0, 1))

    @abstractmethod
    def search(self, query: str, category: str = None) -> List[Dict]:
        pass

    @abstractmethod
    def parse_listing(self, raw_data: Dict) -> Dict:
        pass
