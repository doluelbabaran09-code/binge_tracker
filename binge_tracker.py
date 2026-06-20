import random
import json
from abc import ABC, abstractmethod

# UI Colors for the CLI
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
        if 0 <= index < len(self.__watchlist):
            selected = self.__watchlist[index]
            
            # Data Validation Guardrail (Encapsulation benefit)
            if new_watched > selected.total:
                print(f"{RED}Error: Watched episodes cannot exceed total episodes ({selected.total}).{RESET}")
                return
                
            selected.watched = new_watched
            if selected.watched >= selected.total:
                selected.status = "Completed"
                print(f"{GREEN}🎉 Show Finished!{RESET}")
                review = input(f"Rate {selected.title} (1-10): ")
                selected.rating = review
            else:
                selected.status = "Watching"
                print(f"{GREEN}Updated.{RESET}")
            
            self.save_data()
        else:
            print(f"{RED}Invalid selection.{RESET}")

def main():
    system = TrackerSystem()
    
    recommendation_pool = [
        "Attack on Titan (Anime)", "Demon Slayer (Anime)", "Squid Game (K-Drama)", 
        "Solo Leveling (Anime)", "Goblin (K-Drama)", "One Piece (Anime)", 
        "All of Us Are Dead (K-Drama)", "Moving (K-Drama)", "Death Note (Anime)", 
        "The Glory (K-Drama)", "Lovely Runner (K-Drama)", "Mr Plankton (K-Drama)"
    ]

    while True:
        print(f"{PURPLE}{BOLD}═══════════════════════════════════     B I N G E   T R A C K E R   ════════════════════════════════════════ {RESET}")
        print(f"{BOLD}1. Add Show")
        print("2. Update Progress")
        print("3. View Watchlist")
        print("4. Recommendation")
        print(f"5. Exit{RESET}")
        
        choice = input(f"\n{CYAN}Choice > {RESET}")

        if choice == '1':
            print(f"\n{PURPLE}--- ADD SHOW ---{RESET}")
            title = input("Title: ")
            total = int(input("Total Episodes/Chapters: "))
            
            print("Type: [1] Anime  [2] K-Drama")
            type_choice = input("Select Type: ")
            
            if type_choice == '1':
                if "Anime" not in title: title += " (Anime)"
                new_item = Anime(title, total)
            else:
                if "K-Drama" not in title: title += " (K-Drama)"
                new_item = KDrama(title, total)
                
            system.add_item(new_item)
            input("Press Enter...")

        elif choice == '2':
            print(f"\n{PURPLE}--- UPDATE ---{RESET}")
            watchlist = system.get_all_items()
            
            for idx, show in enumerate(watchlist, 1):
                # Polymorphism execution context at runtime
                print(f"[{idx}] {show.title} ({show.get_progress_string()})")
                
            try:
                selection = int(input("\nSelect Number: ")) - 1
                new_watched = int(input("Episodes/Chapters watched: "))
                system.update_progress(selection, new_watched)
            except ValueError:
                print(f"{RED}Please enter valid numbers.{RESET}")
                
            input("Press Enter...")

        elif choice == '3':
            print(f"\n{PURPLE}--- MY LIST ---{RESET}")
            print(f"{'TITLE':<30} | {'PROGRESS':<12} | {'RATING':<8} | {'STATUS'}")
            print("-" * 75)
            
            for show in system.get_all_items():
                print(f"{BOLD}{show.title:<30}{RESET} | {show.get_progress_string():<12} | {show.rating:<8} | {show.status}")
            input("\nPress Enter...")

        elif choice == '4':
            print(f"\n{PURPLE}--- RECOMMENDATION ---{RESET}")
            pick = random.choice(recommendation_pool)
            print(f"Watch this: {GREEN}{BOLD}{pick}{RESET}")
            input("\nPress Enter...")

        elif choice == '5':
            print(f"{RED}Bye! Data saved.{RESET}")
            break

if __name__ == '__main__':
    main()