import requests
import json
from typing import Dict, List, Optional
import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

class AnkiConnectAPI:
    """A class to interact with AnkiConnect API for fetching deck statistics."""
    
    def __init__(self, url: str = "http://localhost:8765"):
        """
        Initialize the AnkiConnect API client.
        
        Args:
            url: The URL where AnkiConnect is running (default: http://localhost:8765)
        """
        self.url = url
    
    def _request(self, action: str, params: Optional[Dict] = None) -> Dict:
        """
        Send a request to AnkiConnect API.
        
        Args:
            action: The AnkiConnect action to perform
            params: Parameters for the action
            
        Returns:
            The response from AnkiConnect
            
        Raises:
            Exception: If the request fails or AnkiConnect returns an error
        """
        if params is None:
            params = {}
            
        payload = {
            "action": action,
            "version": 6,
            "params": params
        }
        
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            if result.get("error"):
                raise Exception(f"AnkiConnect error: {result['error']}")
                
            return result.get("result")
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to connect to AnkiConnect: {e}")
    
    def get_deck_names(self) -> List[str]:
        """Get all available deck names."""
        return self._request("deckNames")
    
    def get_deck_stats(self, deck_name: str) -> Dict:
        """
        Get detailed statistics for a specific deck.
        
        Args:
            deck_name: Name of the deck to get stats for
            
        Returns:
            Dictionary containing deck statistics
        """
        return self._request("getStats", {"decks": [deck_name]})
    
    def find_cards(self, query: str) -> List[int]:
        """
        Find card IDs matching a query.
        
        Args:
            query: Anki search query
            
        Returns:
            List of card IDs
        """
        return self._request("findCards", {"query": query})
    
    def get_cards_info(self, card_ids: List[int]) -> List[Dict]:
        """
        Get detailed information about specific cards.
        
        Args:
            card_ids: List of card IDs
            
        Returns:
            List of card information dictionaries
        """
        return self._request("cardsInfo", {"cards": card_ids})
    
    def get_deck_stats_direct(self, deck_name: str) -> Dict[str, int]:
        """
        Get deck statistics directly from AnkiConnect without iterating through cards.
        
        Args:
            deck_name: Name of the deck
            
        Returns:
            Dictionary with card counts by state
        """
        try:
            # Method 1: Try using getStats (if available)
            stats = self._request("getStats", {"decks": [deck_name]})
            if stats:
                # Parse the stats response - structure may vary
                print(f"Raw stats response: {stats}")
                return self._parse_anki_stats(stats)
        except:
            pass
        
        try:
            # Method 2: Use search queries for direct counts
            deck_query = f'deck:"{deck_name}"'
            
            # Count cards by state using search queries
            new_count = len(self.find_cards(f"{deck_query} is:new"))
            learning_count = len(self.find_cards(f"{deck_query} is:learn"))
            young_count = len(self.find_cards(f"{deck_query} is:review prop:ivl<21"))
            mature_count = len(self.find_cards(f"{deck_query} is:review prop:ivl>=21"))
            suspended_count = len(self.find_cards(f"{deck_query} is:suspended"))
            
            return {
                "new": new_count,
                "learning": learning_count,
                "young": young_count,
                "mature": mature_count,
                "suspended": suspended_count,
                "total": new_count + learning_count + young_count + mature_count
            }
        except Exception as e:
            print(f"Error getting direct stats: {e}")
            # Fallback to the original method
            return self.get_card_counts_by_state(deck_name)
    
    def _parse_anki_stats(self, stats_response) -> Dict[str, int]:
        """
        Parse the response from AnkiConnect getStats.
        
        Args:
            stats_response: Raw response from getStats
            
        Returns:
            Parsed statistics dictionary
        """
        # This will need to be adjusted based on the actual structure
        # of the getStats response
        return stats_response
    
    def get_card_counts_by_state(self, deck_name: str) -> Dict[str, int]:
        """
        Get the count of cards by their learning state in a deck.
        
        Args:
            deck_name: Name of the deck
            
        Returns:
            Dictionary with 'mature', 'young', 'learning', 'relearning', and 'total' counts
        """
        # Find all cards in the deck
        deck_query = f'deck:"{deck_name}"'
        all_card_ids = self.find_cards(deck_query)
        
        if not all_card_ids:
            return {"mature": 0, "young": 0, "learning": 0, "relearning": 0, "total": 0}
        
        # Get card information
        cards_info = self.get_cards_info(all_card_ids)
        
        mature_count = 0
        young_count = 0
        learning_count = 0
        relearning_count = 0
        
        # Debug counters
        debug_info = {
            "suspended_review_cards": 0,
            "review_cards_21_plus": 0,
            "review_cards_under_21": 0,
            "mature_intervals": []
        }
        
        for card in cards_info:
            # Card type: 0=new, 1=learning, 2=review, 3=relearning
            card_type = card.get("type", 0)
            interval = card.get("interval", 0)
            queue = card.get("queue", 0)  # -1=suspended, 0=new, 1=learning, 2=review, 3=day learning
            
            # Skip suspended cards for all types
            if queue == -1:
                if card_type == 2:
                    debug_info["suspended_review_cards"] += 1
                continue
            
            if card_type == 1:  # Learning cards (excluding suspended)
                learning_count += 1
            elif card_type == 2:  # Review cards (excluding suspended)
                # Mature cards are review cards with interval >= 21 days (excluding suspended)
                if interval >= 21:
                    mature_count += 1
                    debug_info["review_cards_21_plus"] += 1
                    # Sample some intervals for debugging
                    if len(debug_info["mature_intervals"]) < 10:
                        debug_info["mature_intervals"].append(interval)
                else:
                    # Young cards are review cards with interval < 21 days (excluding suspended)
                    young_count += 1
                    debug_info["review_cards_under_21"] += 1
            elif card_type == 3:  # Relearning cards (excluding suspended)
                relearning_count += 1
        
        result = {
            "mature": mature_count,
            "young": young_count,
            "learning": learning_count,
            "relearning": relearning_count,
            "total": mature_count + young_count + learning_count + relearning_count,
            "debug": debug_info
        }
        
        return result
    
    def get_all_deck_stats(self) -> Dict[str, Dict[str, int]]:
        """
        Get card counts by state for all decks.
        
        Returns:
            Dictionary mapping deck names to their statistics
        """
        deck_names = self.get_deck_names()
        all_stats = {}
        
        for deck_name in deck_names:
            try:
                stats = self.get_card_counts_by_state(deck_name)
                all_stats[deck_name] = stats
            except Exception as e:
                print(f"Error getting stats for deck '{deck_name}': {e}")
                all_stats[deck_name] = {"mature": 0, "young": 0, "learning": 0, "relearning": 0, "total": 0}
        
        return all_stats


def print_stats(selected_deck: str, stats: Dict[str, int]):
    print(f"\nDeck: {selected_deck}")
    print(f"Mature cards: {stats['mature']}")
    print(f"Young cards: {stats['young']}")
    print(f"Learning cards: {stats['learning']}")
    print(f"Relearning cards: {stats['relearning']}")
    print(f"Total cards: {stats['total']}")

def addToCsv(name_of_csv: str, total: int):
    import csv
    from datetime import datetime
    import os
    
    today = datetime.now().strftime('%Y-%m-%d')
    filename = name_of_csv
    
    # Check if file exists and read existing data
    existing_data = []
    updated = False
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            # print(list(reader))
            for row in reader:
                if len(row) >= 2 and row[0] == today:
                    # Replace today's entry
                    existing_data.append([today, str(total)])
                    updated = True
                else:
                    if(len(existing_data) > 0 and existing_data[-1][1] != row[1]):
                        existing_data.append(row)
                    elif(len(existing_data) == 0):
                        existing_data.append(row)
    
    # If today's date wasn't found, add new entry
    if ((not updated) and (existing_data[-1][1] != str(total))):
        existing_data.append([today, str(total)])
    
    # Write back all data
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(existing_data)


def update_graph_pt(words: int):
    """Update the Portuguese word count graph."""
    csv_file_path = 'pt_counts.csv'
    start_date = datetime(2024, 2, 5)  # Start date of learning Portuguese (based on CSV data)
    
    # Check if the file exists and has data
    if not os.path.exists(csv_file_path) or os.path.getsize(csv_file_path) == 0:
        print(f"CSV file {csv_file_path} not found or empty. Cannot create graph.")
        return
    
    # Read the CSV for plotting
    df = pd.read_csv(csv_file_path, parse_dates=['Date'])
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    df = df.dropna()
    
    if df.empty:
        print("No valid data found in CSV file. Cannot create graph.")
        return
    
    # Plotting
    fig, ax = plt.subplots(figsize=(12, 6))

    # Main plot (left y-axis)
    ax.plot(df["Date"], df["Value"], marker='o', linestyle='-', color='green', linewidth=2, markersize=8)
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('Word Count', fontsize=14, color='green')
    ax.tick_params(axis='y', labelcolor='green')

    # Manually setting ticks for alignment
    y_min, y_max = ax.get_ylim()
    y_step = max(1, int((y_max - y_min) / 10))  # Adaptive step size for Portuguese (smaller numbers)
    y_ticks = range(int(y_min), int(y_max) + y_step, y_step)
    ax.set_yticks(y_ticks)

    # Top x-axis for time since start
    def time_since_start(date):
        delta = date - start_date
        if delta.days < 30:
            return f"{delta.days} days"
        elif delta.days < 365:
            months = delta.days // 30
            return f"{months} months"
        else:
            years = delta.days // 365
            months = (delta.days % 365) // 30
            return f"{years} years {months} months"

    ax_top = ax.secondary_xaxis('top')
    ax_top.set_xlabel('Time Since starting to learn Portuguese', fontsize=14)
    
    # Select points: first, last, and last point per month for others
    selected_indices = []
    
    # Always include first point
    selected_indices.append(0)
    
    # Group by year-month and take the last point in each month
    df['YearMonth'] = df['Date'].dt.to_period('M')
    monthly_last = df.groupby('YearMonth').tail(1)
    
    # Get indices of monthly last points (excluding first and last overall)
    for idx in monthly_last.index:
        if idx != 0 and idx != len(df) - 1:
            selected_indices.append(idx)
    
    # Always include last point (if not already included)
    if len(df) - 1 not in selected_indices:
        selected_indices.append(len(df) - 1)
    
    # Sort indices and remove duplicates
    selected_indices = sorted(list(set(selected_indices)))
    
    # Filter out any indices that would create duplicate labels
    final_indices = [selected_indices[0]]  # Always include first
    seen_labels = {time_since_start(df["Date"].iloc[selected_indices[0]])}
    
    for idx in selected_indices[1:]:
        label = time_since_start(df["Date"].iloc[idx])
        if label not in seen_labels:
            final_indices.append(idx)
            seen_labels.add(label)
        elif idx == len(df) - 1:  # Always include last point even if duplicate label
            final_indices.append(idx)
    
    selected_dates = [df["Date"].iloc[i] for i in final_indices]
    selected_labels = [time_since_start(df["Date"].iloc[i]) for i in final_indices]
    
    ax_top.set_xticks(selected_dates)
    ax_top.set_xticklabels(selected_labels, rotation=45, ha='left')

    # Customize grid and layout
    ax.grid(visible=True, which='major', linestyle='--', linewidth=0.5)
    plt.title('Portuguese Word Count by Date', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot
    plt.savefig('graph_PT.png', dpi=300)
    print(f"Portuguese graph saved as graph_PT.png with {words} words.")

def update_graph(words: int):
    """Update the Japanese word count graph."""
    csv_file_path = 'nihongo_counts.csv'
    start_date = datetime(2017, 10, 1)  # Start date of learning Japanese
    
    # Check if the file exists and has data
    if not os.path.exists(csv_file_path) or os.path.getsize(csv_file_path) == 0:
        print(f"CSV file {csv_file_path} not found or empty. Cannot create graph.")
        return
    
    # Read the CSV for plotting
    df = pd.read_csv(csv_file_path, parse_dates=['Date'])
    df['Word Count'] = pd.to_numeric(df['Word Count'], errors='coerce')
    df = df.dropna()
    
    if df.empty:
        print("No valid data found in CSV file. Cannot create graph.")
        return
    
    # Plotting
    fig, ax = plt.subplots(figsize=(12, 6))

    # Main plot (left y-axis)
    ax.plot(df["Date"], df["Word Count"], marker='o', linestyle='-', color='royalblue', linewidth=2, markersize=8)
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('Word Count', fontsize=14, color='royalblue')
    ax.tick_params(axis='y', labelcolor='royalblue')

    # Manually setting ticks for alignment
    y_min, y_max = ax.get_ylim()
    y_ticks = range(int(y_min), int(y_max) + 100, 300)
    ax.set_yticks(y_ticks)

    # Top x-axis for years since start
    def years_since_start(date):
        delta = date - start_date
        years = delta.days // 365
        months = (delta.days % 365) // 30
        return f"{years} years {months} months"

    ax_top = ax.secondary_xaxis('top')
    ax_top.set_xlabel('Years Since starting to learn Japanese', fontsize=14)
    
    # Select points: first, last, and last point per month for others
    selected_indices = []
    
    # Always include first point
    selected_indices.append(0)
    
    # Group by year-month and take the last point in each month
    df['YearMonth'] = df['Date'].dt.to_period('M')
    monthly_last = df.groupby('YearMonth').tail(1)
    
    # Get indices of monthly last points (excluding first and last overall)
    for idx in monthly_last.index:
        if idx != 0 and idx != len(df) - 1:
            selected_indices.append(idx)
    
    # Always include last point (if not already included)
    if len(df) - 1 not in selected_indices:
        selected_indices.append(len(df) - 1)
    
    # Sort indices and remove duplicates
    selected_indices = sorted(list(set(selected_indices)))
    
    # Filter out any indices that would create duplicate labels
    final_indices = [selected_indices[0]]  # Always include first
    seen_labels = {years_since_start(df["Date"].iloc[selected_indices[0]])}
    
    for idx in selected_indices[1:]:
        label = years_since_start(df["Date"].iloc[idx])
        if label not in seen_labels:
            final_indices.append(idx)
            seen_labels.add(label)
        elif idx == len(df) - 1:  # Always include last point even if duplicate label
            final_indices.append(idx)
    
    selected_dates = [df["Date"].iloc[i] for i in final_indices]
    selected_labels = [years_since_start(df["Date"].iloc[i]) for i in final_indices]
    
    ax_top.set_xticks(selected_dates)
    ax_top.set_xticklabels(selected_labels, rotation=45, ha='left')

    # Right y-axis (4000 higher than the left y-axis)
    ax_right = ax.secondary_yaxis('right', functions=(lambda x: x + 4000, lambda x: x - 4000))
    ax_right.set_ylabel('Word Count (incl. pre-anki)', fontsize=14, color='red')
    ax_right.tick_params(axis='y', labelcolor='red')
    ax_right.set_yticks([tick + 4000 for tick in y_ticks])  # Align ticks properly

    # Customize grid and layout
    ax.grid(visible=True, which='major', linestyle='--', linewidth=0.5)
    plt.title('Japanese Word Count by Date', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot
    plt.savefig('graph.png', dpi=300)
    print(f"Japanese graph saved as graph.png with {words} words.")

def main():
    """Main function to demonstrate the AnkiConnect API usage."""
    # Initialize the API client
    anki = AnkiConnectAPI()
    
    try:
        # Test connection
        print("Testing connection to AnkiConnect...")
        deck_names = anki.get_deck_names()
        print(f"Successfully connected! Found {len(deck_names)} decks.\n")
        
        if not deck_names:
            print("No decks found in Anki.")
            return
        
        selected_deck = "0 日本語"
        stats_jp = anki.get_card_counts_by_state(selected_deck)

        print_stats(selected_deck, stats_jp)
        addToCsv("nihongo_counts.csv", stats_jp['total'])
        update_graph(stats_jp['total'])

        selected_deck = "0 Portuguese > English – Phrase Book _sorted"
        stats_pt = anki.get_card_counts_by_state(selected_deck)

        print_stats(selected_deck, stats_pt)
        addToCsv("pt_counts.csv", stats_pt['total'])
        update_graph_pt(stats_pt['total'])

    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure:")
        print("1. Anki is running")
        print("2. AnkiConnect add-on is installed and enabled")
        print("3. AnkiConnect is accessible at http://localhost:8765")

if __name__ == "__main__":
    main()