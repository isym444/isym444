import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# API URL
url = "https://themecpapi.isym.uk/scrape_contest_history"
response = requests.get(url)
data = response.json()["data"]

# Define column names
columns = [
    "ID", "Date", "Topic", "Level", "R1", "R2", "R3", "R4",
    "T1", "T2", "T3", "T4", "Perf", "Rating", "Δ"
]

# Convert data to DataFrame
new_data = pd.DataFrame(data, columns=columns)

# Convert columns to appropriate data types
new_data['ID'] = new_data['ID'].astype(int)
new_data['Date'] = pd.to_datetime(new_data['Date'])
new_data['Perf'] = new_data['Perf'].str.replace('~', '').astype(float)

# Load existing data if present
csv_file = "contest_history.csv"
try:
    existing_data = pd.read_csv(csv_file)
    existing_data['Date'] = pd.to_datetime(existing_data['Date'])
except FileNotFoundError:
    existing_data = pd.DataFrame()

# Concatenate and remove duplicates based on 'ID'
combined_data = pd.concat([existing_data, new_data]).drop_duplicates(subset=['ID'])

# Save combined data
combined_data.to_csv(csv_file, index=False)

# Sort data by ID for plotting
combined_data = combined_data.sort_values(by='ID')

# Plotting the data and saving to file
plt.figure(figsize=(10, 6))
plt.plot(combined_data['Date'], combined_data['Perf'], marker='o')
plt.xlabel('Date')
plt.ylabel('Performance')
plt.title('ThemeCP Codeforces Virtual Contests Performance Over Time')
plt.grid(True)

# Save the plot to an image file
plt.savefig("contest_performance.png")

print("Plot saved as 'contest_performance.png'.")
