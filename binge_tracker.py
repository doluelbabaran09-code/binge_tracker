import random
import json
from abc import ABC, abstractmethod

PURPLE = '\033[95m'
CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

class WatchableItem(ABC):
    def __init__(self, title: str, total: int, watched: int = 0, status: str = "Plan to Watch", rating: str = "N/A"):
        self.title = title
        self.total = total
        self.watched = watched
        self.status = status
        self.rating = rating

    @abstractmethod
    def get_progress_string(self) -> str:
        """Abstract method: Must be implemented by all child classes."""
        pass

class Anime(WatchableItem):
    def __init__(self, title: str, total: int, watched: int = 0, status: str = "Plan to Watch", rating: str = "N/A"):
        # Explicit inheritance link via super()
        super().__init__(title, total, watched, status, rating)

    def get_progress_string(self) -> str:
        # Polymorphic behavior specific to Anime
        return f"{self.watched}/{self.total} Ep."


class KDrama(WatchableItem):
    def __init__(self, title: str, total: int, watched: int = 0, status: str = "Plan to Watch", rating: str = "N/A"):
        # Explicit inheritance link via super()
        super().__init__(title, total, watched, status, rating)

    def get_progress_string(self) -> str:
        # Polymorphic behavior specific to K-Drama
        return f"{self.watched}/{self.total} Ch."
    
class TrackerSystem:
    def __init__(self, filename="my_watchlist.json"):
        self.filename = filename
        self.__watchlist = []  # Private attribute (Encapsulation)
        self.load_data()

    def load_data(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                for item in data:
                    if "Anime" in item['title']:
                        self.__watchlist.append(Anime(item['title'], item['total'], item['watched'], item['status'], item.get('rating', 'N/A')))
                    else:
                        self.__watchlist.append(KDrama(item['title'], item['total'], item['watched'], item['status'], item.get('rating', 'N/A')))
        except FileNotFoundError:
            self.__watchlist = []

    def save_data(self):
        # Converts class instances to dictionary formats safely for JSON export
        raw_data = [obj.__dict__ for obj in self.__watchlist]
        with open(self.filename, 'w') as f:
            json.dump(raw_data, f, indent=4)

    def add_item(self, item: WatchableItem):
        self.__watchlist.append(item)
        self.save_data()
        print(f"{GREEN}Saved!{RESET}")

    def get_all_items(self):
        return self.__watchlist

    def update_progress(self, index: int, new_watched: int):