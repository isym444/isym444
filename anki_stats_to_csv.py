import csv
import os
import sqlite3

# Get user's home directory
home_dir = os.path.expanduser('~')
# db_path = f"{home_dir}/Library/Application Support/Anki2/User 1/collection.anki2"
db_path = "/Users/samir/Library/Application Support/Anki2/User 1/collection.anki2"
con = sqlite3.connect(db_path)
c = con.cursor()

# Corrected the indentation for the query string
query = """
SELECT *
FROM col
"""

result = c.execute(query).fetchall()
print(result)

# Get column names from cursor description
column_names = [description[0] for description in c.description]

# Define path to save CSV file (you can modify this path as needed)
csv_file_path = os.path.join(home_dir, "result.csv")

# Save result to a CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(column_names)  # write header
    writer.writerows(result)

print(f"Result saved to {csv_file_path}")