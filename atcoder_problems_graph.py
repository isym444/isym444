import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime, timedelta
import os
import glob

# Read data from CSV
data = pd.read_csv('/Users/samir/Desktop/GithubReadme/isym444/your_file.csv', parse_dates=['Date'])

# Plotting
plt.style.use('dark_background')
plt.figure(figsize=(10, 6))
plt.plot(data['Date'], data['Value'], marker='o', linestyle='-', color='#58a6ff')  # Plot with markers at each point

# Formatting the plot
plt.xlabel('Date', color='white')
plt.ylabel('Number of Problems Solved', color='white')
plt.title('AtCoder Problems Solved Over Time', color='white')
plt.grid(True, color='#343a40')  # Use a dark grid color

# Format date on x-axis to DD/MM/YY
date_format = DateFormatter("%d/%m/%y")
plt.gca().xaxis.set_major_formatter(date_format)
plt.gca().tick_params(colors='white')  # Set the color of ticks to white

# Rotate date labels for better readability
plt.xticks(rotation=45)


# Specify the directory path where your files are located
directory_path = '/Users/samir/Desktop/GithubReadme/isym444'

# Construct the pattern to match files starting with 'problems_solved_over_time'
pattern = os.path.join(directory_path, 'problems_solved_over_time*.png')

# Use glob to find all files matching the pattern
matching_files = glob.glob(pattern)

for file_path in matching_files:
    try:
        os.remove(file_path)
        print(f"Deleted {file_path}")
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")

# Save the figure
#plt.savefig(f'/Users/samir/Desktop/GithubReadme/isym444/problems_solved_over_time{datetime.now().strftime("%d%m%Y")}.png', transparent=True)
temp = datetime.now().strftime("%d%m%Y")
temp2 = (datetime.now()-timedelta(days=1)).strftime("%d%m%Y")
# os.remove(f'/Users/samir/Desktop/GithubReadme/isym444/problems_solved_over_time{temp2}.png')
plt.savefig(f'/Users/samir/Desktop/GithubReadme/isym444/problems_solved_over_time{temp}.png', transparent=True)
file_path = "/Users/samir/Desktop/GithubReadme/isym444/README.md"

with open(file_path, "r") as file:
    lines = file.readlines()
for i, line in enumerate(lines):
    if '![AtCoder Progression](problems_solved_over_time' in line:
        print("found line")
        temp = datetime.now().strftime("%d%m%Y")
        print(temp)
        lines[i] = f'![AtCoder Progression](problems_solved_over_time{temp}.png "AtCoder Progression")'
        updated = True
        with open(file_path, "w") as file:
            file.writelines(lines)
            print("Updated the Markdown file with the new atcoder stats.")


# Close the plot
plt.close()
