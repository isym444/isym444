import os
import requests
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Fetch data from the API
response = requests.get("http://10.134.112.24:8000/nihongo")
data = response.json()
vocab_count = data["known_cards"]

# CSV file path
csv_file_path = 'nihongo_counts.csv'
start_date = datetime(2017, 10, 1)  # Start date of learning Japanese

def update_readme(vocab_count):
    readme_file_path = 'README.md'
    new_count = vocab_count + 4000

    with open(readme_file_path, 'r') as file:
        lines = file.readlines()

    with open(readme_file_path, 'w') as file:
        for line in lines:
            if line.startswith('**Japanese words:**'):
                file.write(f'**Japanese words:** {new_count}\n')
            else:
                file.write(line)

def update_csv(file_path, vocab_count):
    today = datetime.now().strftime('%Y-%m-%d')

    # Check if the file exists and read it, else create an empty DataFrame
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        df = pd.read_csv(file_path, parse_dates=['Date'])
    else:
        df = pd.DataFrame(columns=['Date', 'Word Count'])

    # Ensure 'Date' column is datetime and 'Word Count' is numeric
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date
    df['Word Count'] = pd.to_numeric(df['Word Count'], errors='coerce')

    # Drop invalid rows
    df = df.dropna()

    # Update or append today's count
    if today in df['Date'].astype(str).values:
        df.loc[df['Date'].astype(str) == today, 'Word Count'] = vocab_count
    else:
        new_row = pd.DataFrame({'Date': [today], 'Word Count': [vocab_count]})
        df = pd.concat([df, new_row], ignore_index=True)

    # Save updated CSV with proper date format
    df['Date'] = df['Date'].astype(str)
    df.to_csv(file_path, index=False)

# Update the CSV with today's data
update_csv(csv_file_path, vocab_count)

update_readme(vocab_count)

# Read the CSV for plotting
df = pd.read_csv(csv_file_path, parse_dates=['Date'])
df['Word Count'] = pd.to_numeric(df['Word Count'], errors='coerce')
df = df.dropna()

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
ax_top.set_xlabel('Years Since 2017-10', fontsize=14)
ax_top.set_xticks(df["Date"])
ax_top.set_xticklabels([years_since_start(d) for d in df["Date"]], rotation=45, ha='left')

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
