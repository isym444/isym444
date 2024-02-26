import requests
import json
from datetime import datetime
import os

# API endpoint
url = "https://kenkoooo.com/atcoder/atcoder-api/v3/user/ac_rank?user=isym444"
url2 = "https://atcoder.jp/users/isym444/history/json"

# Send a request to the API
response = requests.get(url)
if response.status_code == 200:
    json_data = response.json()
    count = json_data.get("count", "N/A")  # Extracts only the 'count' value
else:
    print("Failed to retrieve data: Status code", response.status_code)
    exit()

response2 = requests.get(url2)
if response2.status_code == 200:
    json_data = response2.json()
    rating = json_data[-1]['NewRating'] # Extracts only the 'rating' value
else:
    print("Failed to retrieve data: Status code", response2.status_code)
    exit()

def get_codeforces_rating():
    url = "https://codeforces.com/api/user.info"
    params = {
        'handles': "isym444"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] == "OK":
        user_info = data["result"][0]
        return user_info.get("rating")
    else:
        return "Error: " + data.get("comment", "Unknown Error")

# Example usage
cfrating = get_codeforces_rating()

# Read the existing Markdown file
file_path = "/Users/samir/Desktop/GithubReadme/isym444/README.md"
with open(file_path, "r") as file:
    lines = file.readlines()

# Update the line with the new count
updated = False
updated2 = False
updated3 = False
for i, line in enumerate(lines):
    if "**AtCoder Problems Solved:**" in line:
        lines[i] = f"**AtCoder Problems Solved:** {count}\n"
        updated = True
        break

for i, line in enumerate(lines):
    if "**AtCoder Rating:**" in line:
        lines[i] = f"**AtCoder Rating:** {rating}\n"
        updated2 = True
        break

for i, line in enumerate(lines):
    if "**Codeforces Rating:**" in line:
        lines[i] = f"**Codeforces Rating:** {cfrating}\n"
        updated3 = True
        break

# Write the updated content back to the file
if updated and updated2 and updated3:
    with open(file_path, "w") as file:
        file.writelines(lines)
    print("Updated the Markdown file with the new atcoder stats.")
else:
    print("The specified line was not found in the file.")


"""  """
"""  """

import pandas as pd
from datetime import datetime

# Function to update or add a new row in the CSV
def update_csv(file_path, x_value):
    # Check if the file exists and has content
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        data = pd.read_csv(file_path)
    else:
        # Initialize an empty DataFrame with the necessary columns
        data = pd.DataFrame(columns=['Date', 'Value'])

    today = datetime.now().strftime('%Y-%m-%d')
    
    if today in data['Date'].values:
        data.loc[data['Date'] == today, 'Value'] = x_value
    else:
        new_row = pd.DataFrame({'Date': [today], 'Value': [x_value]})
        data = pd.concat([data, new_row], ignore_index=True)

    data.to_csv(file_path, index=False)

# Example usage
x = count
csv_file_path = '/Users/samir/Desktop/GithubReadme/isym444/your_file.csv'
update_csv(csv_file_path, x)