import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

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

# Save the figure
plt.savefig('problems_solved_over_time.png', transparent=True)

# Close the plot
plt.close()
