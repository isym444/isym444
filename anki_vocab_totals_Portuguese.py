import matplotlib.pyplot as plt
import datetime
import csv

CSV_FILENAME = "/Users/samir/Documents/Programming/old dev/Portuguese_word_counts_by_date.csv"


def plot_word_counts():
    plt.clf()
    # Read word counts from CSV
    word_counts_by_date = {}
    with open(CSV_FILENAME, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            word_counts_by_date[row[0]] = int(row[1])

    # Sort dates
    sorted_dates = sorted(word_counts_by_date.keys())
    sorted_counts = [word_counts_by_date[date] for date in sorted_dates]

    fig, ax1 = plt.subplots()

    #-----------------------------------------
    ax1.plot(
        sorted_dates, sorted_counts, marker="o", linestyle="-", label="Original Data"
    )
    ax1.set_ylabel("Word Count", color="blue")
    ax1.tick_params("y", colors="blue")

    # Create a second y-axis
    # ax2 = ax1.twinx()
    # ax2.set_ylim(ax1.get_ylim()[0] + 4000, ax1.get_ylim()[1] + 4000)
    # ax2.tick_params("y", colors="red")

    nth_label = 2  # Adjust this based on the number of data points you have
    ax1.set_xticks(sorted_dates[::nth_label])
    ax1.set_xticklabels(
        sorted_dates[::nth_label], rotation=45, fontsize=8
    )  # Adjust fontsize
    #--------------------------------------------
    # Define the start date
    date_string = "2022-09-14"
    year, month, day = map(int, date_string.split("-"))
    start_date = datetime.date(year, month, day)

    # Calculate months and years from the start date
    print(sorted_dates)
    print(sorted_dates[::nth_label])
    print(len(sorted_dates[::nth_label]))
    months_of_study = [
        (
            datetime.date(
                int(date.split("-")[0]),
                int(date.split("-")[1]),
                int(date.split("-")[2]),
            )
            - start_date
        ).days
        // 30
        for date in sorted_dates
    ]
    years_months_study = [
        f"{month // 12} years\n{month % 12} months" for month in months_of_study
    ]
    print(years_months_study)
    print(len(years_months_study))

    # Ensure the number of secondary x-axis labels matches the number of primary x-axis labels
    secondary_labels = years_months_study[::nth_label]
    
    #----------------------------------
    # Create a secondary x-axis
    ax3 = ax1.twiny()

    # Set the limits for the secondary x-axis
    ax3.set_xlim(ax1.get_xlim())

    # Use the tick positions of ax1 for ax3
    ax3.set_xticks(ax1.get_xticks())
    ax3.set_xticklabels(
        secondary_labels, fontsize=8, rotation=45
    )  # Adjust fontsize and angle

    #----------------------------------
    # Label the secondary x-axis
    ax3.set_xlabel("Years Since 2022-09-14")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Word Count")
    plt.title("Portuguese Word Count by Date")
    plt.tight_layout()  # Adjust layout to ensure everything fits
    plt.savefig("/Users/samir/Documents/Programming/old dev/graph_PT.png", format="png")


plot_word_counts()


import shutil
import os

# File paths
readme_path = "/Users/samir/Desktop/GithubReadme/isym444/README.md"
graph_source_path = "/Users/samir/Documents/Programming/old dev/graph_PT.png"
graph_destination_path = "/Users/samir/Desktop/GithubReadme/isym444/graph_PT.png"

# Copy the graph image to the README.md directory
shutil.copy(graph_source_path, graph_destination_path)

# # Read the file contents
# with open(readme_path, "r") as file:
#     lines = file.readlines()


# # Append the graph image at the bottom
# graph_filename = os.path.basename(graph_destination_path)
# # lines.append(f"\n![Graph Image]({graph_filename})\n")

# # Write the modified contents back to the file
# with open(readme_path, "w") as file:
#     file.writelines(lines)

# import json
# import urllib.request
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import pandas
# from IPython.display import HTML, display
# import boto3
# import datetime

# import csv
# import matplotlib.pyplot as plt

# CSV_FILENAME = "/Users/samir/Documents/Programming/Portuguese_word_counts_by_date.csv"

# def update_word_count(date, count):
#     # Read existing data
#     print("alert")
#     print(date)
#     print(count)
#     existing_data = {}
#     try:
#         with open(CSV_FILENAME, "r") as csvfile:
#             reader = csv.reader(csvfile)
#             for row in reader:
#                 existing_data[row[0]] = int(row[1])
#     except FileNotFoundError:
#         pass  # It's okay if the file doesn't exist initially

#     print(existing_data)
#     # Update the word count for the given date
#     # existing_data[date] = count
#     current_datetime = datetime.datetime.now()
#     formatted_date = current_datetime.strftime("%Y-%m-%d")
#     print(formatted_date[0:7])
#     substring = formatted_date[0:7]
#     matching_keys = [key for key in existing_data if substring in key]
#     print(matching_keys)
#     for i in matching_keys:
#         del existing_data[i]
#     print(existing_data)
#     existing_data[formatted_date] = count
#     print(existing_data)
#     # Write back to CSV
#     with open(CSV_FILENAME, "w") as csvfile:
#         writer = csv.writer(csvfile)
#         for date, count in existing_data.items():
#             writer.writerow([date, count])


# def request(action, **params):
#     return {"action": action, "params": params, "version": 6}

# def invoke(action, **params):
#     requestJson = json.dumps(request(action, **params)).encode("utf-8")
#     response = json.load(
#         urllib.request.urlopen(
#             urllib.request.Request("http://localhost:8765", requestJson)
#         )
#     )
#     if len(response) != 2:
#         raise Exception("response has an unexpected number of fields")
#     if "error" not in response:
#         raise Exception("response is missing required error field")
#     if "result" not in response:
#         raise Exception("response is missing required result field")
#     if response["error"] is not None:
#         raise Exception(response["error"])
#     return response["result"]


# def plot_word_counts():
#     plt.clf()
#     # Read word counts from CSV
#     word_counts_by_date = {}
#     with open(CSV_FILENAME, "r") as csvfile:
#         reader = csv.reader(csvfile)
#         for row in reader:
#             word_counts_by_date[row[0]] = int(row[1])

#     # Sort dates
#     sorted_dates = sorted(word_counts_by_date.keys())
#     sorted_counts = [word_counts_by_date[date] for date in sorted_dates]
#     """ print(sorted_dates)
#     print(sorted_counts) """
#     # Plot
#     plt.plot(sorted_dates, sorted_counts, marker="o", linestyle="-")
#     # higher_counts = [count + 4000 for count in sorted_counts]
#     # plt.plot(sorted_dates, higher_counts, marker='x', linestyle='--', color='red', label='Higher by 4000')

#     fig, ax1 = plt.subplots()

#     ax1.plot(
#         sorted_dates, sorted_counts, marker="o", linestyle="-", label="Original Data"
#     )
#     ax1.set_ylabel("Word Count", color="blue")
#     ax1.tick_params("y", colors="blue")

#     # Create a second y-axis
#     ax2 = ax1.twinx()
#     ax2.set_ylim(ax1.get_ylim()[0] + 4000, ax1.get_ylim()[1] + 4000)
#     # ax2.set_ylabel('', color='red')
#     ax2.tick_params("y", colors="red")

#     # plt.xticks(rotation=90)  # Rotate date labels for better readability
#     nth_label = 2  # Adjust this based on the number of data points you have
#     ax1.set_xticks(sorted_dates[::nth_label])
#     ax1.set_xticklabels(sorted_dates[::nth_label], rotation=45)

#     # Define the start date

#     date_string = "2022-09-14"
#     year, month, day = map(int, date_string.split("-"))
#     start_date = datetime.date(year, month, day)

#     months_of_study = [
#         (
#             datetime.date(
#                 int(date.split("-")[0]),
#                 int(date.split("-")[1]),
#                 int(date.split("-")[2]),
#             )
#             - start_date
#         ).days
#         // 30
#         for date in sorted_dates
#     ]
#     years_months_study = [
#         f"{month // 12} years\n{month % 12} months" for month in months_of_study
#     ]

#     # 2. Create a secondary x-axis
#     ax2 = ax1.twiny()

#     # 3. Set the limits for the secondary x-axis
#     ax2.set_xlim(ax1.get_xlim())

#     # Use the tick positions of ax1 for ax2
#     ax2_ticks = ax1.get_xticks()

#     # If the number of ticks is more than your years_of_study, you can slice it.
#     # This ensures that the number of tick positions matches the number of labels.
#     if len(ax2_ticks) > len(years_months_study):
#         ax2_ticks = ax2_ticks[: len(years_months_study)]

#     ax2.set_xticks(ax2_ticks)
#     ax2.set_xticklabels(
#         years_months_study[: len(ax2_ticks)]
#     )  # Ensure matching number of labels

#     # 4. Label the secondary x-axis
#     ax2.set_xlabel("Years Since 2022-09-14")
#     # plt.xlabel('Date')
#     ax1.set_xlabel("Date")
#     ax1.set_ylabel("Word Count")
#     # plt.ylabel('Word Count')
#     plt.title("Portuguese Word Count by Date")
#     plt.tight_layout()  # Adjust layout to ensure everything fits
#     # plt.show()
#     plt.savefig("/Users/samir/Documents/Programming/graph_PT.png", format="png")


# p1 = len(
#     invoke("findCards", query='"deck:0 Portuguese > English – Phrase Book _sorted"')
# )
# p2 = len(
#     invoke(
#         "findCards",
#         query='"deck:0 Portuguese > English – Phrase Book _sorted" is:suspended',
#     )
# )
# p3 = len(
#     invoke(
#         "findCards",
#         query='"deck:0 Portuguese > English – Phrase Book _sorted" -is:suspended is:new',
#     )
# )

# print("number of known portuguese cards: {}".format(p1 - p2 - p3))

# current_date = datetime.date.today()

# update_word_count(current_date.strftime("%Y-%m-%d"), p1 - p2 - p3)

# plot_word_counts()
