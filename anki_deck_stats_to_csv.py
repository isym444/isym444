import sqlite3
import os
import json  # Import the json module

# Define the deck name you're interested in
target_deck_name = "Your Deck Name Here"  # Replace with the name of the deck you want to query

# Connect to the database
home_dir = os.path.expanduser('~')
db_path = f"{home_dir}/Library/Application Support/Anki2/User 1/collection.anki2"
con = sqlite3.connect(db_path)
c = con.cursor()

# Get the deck ID using the deck name
c.execute("SELECT decks FROM col")
decks_json = c.fetchone()[0]
print(decks_json)

decks_dict = json.loads(decks_json)  # Use json.loads() to parse the JSON string
deck_id = None
for deck in decks_dict.values():
    if deck['name'] == target_deck_name:
        deck_id = deck['id']
        break

if deck_id is None:
    print(f"No deck found with the name: {target_deck_name}")
    exit()

# Count the number of cards in the deck using the deck ID
c.execute("SELECT COUNT(*) FROM cards WHERE did=?", (deck_id,))
num_cards = c.fetchone()[0]

print(f"The deck '{target_deck_name}' has {num_cards} cards.")

con.close()
