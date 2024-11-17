import csv
import matplotlib.pyplot as plt

CSV_FILENAME = 'word_counts_by_date.csv'

def update_word_count(date, count):
    # Read existing data
    existing_data = {}
    try:
        with open(CSV_FILENAME, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                existing_data[row[0]] = int(row[1])
    except FileNotFoundError:
        pass  # It's okay if the file doesn't exist initially

    # Update the word count for the given date
    existing_data[date] = count

    # Write back to CSV
    with open(CSV_FILENAME, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for date, count in existing_data.items():
            writer.writerow([date, count])

def plot_word_counts():
    # Read word counts from CSV
    word_counts_by_date = {}
    with open(CSV_FILENAME, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            word_counts_by_date[row[0]] = int(row[1])

    # Sort dates
    sorted_dates = sorted(word_counts_by_date.keys())
    sorted_counts = [word_counts_by_date[date] for date in sorted_dates]

    # Plot
    plt.plot(sorted_dates, sorted_counts, marker='o', linestyle='-')
    plt.xticks(rotation=45)  # Rotate date labels for better readability
    plt.xlabel('Date')
    plt.ylabel('Word Count')
    plt.title('Word Count by Date')
    plt.tight_layout()  # Adjust layout to ensure everything fits
    #plt.show()
    plt.savefig("graph.png", format='png')

def delete_word_count(target_date):
    # Read existing data
    existing_data = {}
    try:
        with open(CSV_FILENAME, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                existing_data[row[0]] = int(row[1])
    except FileNotFoundError:
        print("Error: File not found!")
        return

    # Check if the date exists
    if target_date not in existing_data:
        print(f"No data found for date {target_date}")
        return
    
    # Delete the word count for the given date
    del existing_data[target_date]

    # Write back to CSV
    with open(CSV_FILENAME, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for date, count in existing_data.items():
            writer.writerow([date, count])

    print(f"Deleted word count for date {target_date}")

#update_word_count("2023-10-05", 13077)
delete_word_count("2023-10-05")
update_word_count("2023-10-04", 13057)
update_word_count("2023-09-26", 12988)
update_word_count("2023-08-20", 12680)
update_word_count("2023-07-31", 12576)
update_word_count("2023-07-01", 12496)
#update_word_count("2023-07-04", 12437)
#delete_word_count("2023-07-04")
update_word_count("2023-06-07", 12441)
update_word_count("2023-05-04", 12372)
update_word_count("2023-04-11", 12272)

plot_word_counts()
