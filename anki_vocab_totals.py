import json
import urllib.request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas
from IPython.display import HTML, display
import boto3
import datetime

import csv
import matplotlib.pyplot as plt

CSV_FILENAME = "/Users/samir/Documents/Programming/old dev/word_counts_by_date.csv"


def update_word_count(date, count):
    # Read existing data
    print("alert")
    print(date)
    print(count)
    existing_data = {}
    try:
        with open(CSV_FILENAME, "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                existing_data[row[0]] = int(row[1])
    except FileNotFoundError:
        pass  # It's okay if the file doesn't exist initially

    print(existing_data)
    # Update the word count for the given date
    # existing_data[date] = count
    current_datetime = datetime.datetime.now()
    formatted_date = current_datetime.strftime("%Y-%m-%d")
    print(formatted_date[0:7])
    substring = formatted_date[0:7]
    matching_keys = [key for key in existing_data if substring in key]
    print(matching_keys)
    for i in matching_keys:
        del existing_data[i]
    print(existing_data)
    existing_data[formatted_date] = count
    print(existing_data)
    # Write back to CSV
    with open(CSV_FILENAME, "w") as csvfile:
        writer = csv.writer(csvfile)
        for date, count in existing_data.items():
            writer.writerow([date, count])


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
    """ print(sorted_dates)
    print(sorted_counts) """
    # Plot
    plt.plot(sorted_dates, sorted_counts, marker="o", linestyle="-")
    # higher_counts = [count + 4000 for count in sorted_counts]
    # plt.plot(sorted_dates, higher_counts, marker='x', linestyle='--', color='red', label='Higher by 4000')

    fig, ax1 = plt.subplots()

    ax1.plot(
        sorted_dates, sorted_counts, marker="o", linestyle="-", label="Original Data"
    )
    ax1.set_ylabel("Word Count", color="blue")
    ax1.tick_params("y", colors="blue")

    # Create a second y-axis
    ax2 = ax1.twinx()
    ax2.set_ylim(ax1.get_ylim()[0] + 4000, ax1.get_ylim()[1] + 4000)
    # ax2.set_ylabel('', color='red')
    ax2.tick_params("y", colors="red")

    # plt.xticks(rotation=90)  # Rotate date labels for better readability
    nth_label = 2  # Adjust this based on the number of data points you have
    ax1.set_xticks(sorted_dates[::nth_label])
    ax1.set_xticklabels(sorted_dates[::nth_label], rotation=45)

    # Define the start date

    date_string = "2017-09-29"
    year, month, day = map(int, date_string.split("-"))
    start_date = datetime.date(year, month, day)

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

    # 2. Create a secondary x-axis
    ax2 = ax1.twiny()

    # 3. Set the limits for the secondary x-axis
    ax2.set_xlim(ax1.get_xlim())

    # Use the tick positions of ax1 for ax2
    ax2_ticks = ax1.get_xticks()

    # If the number of ticks is more than your years_of_study, you can slice it.
    # This ensures that the number of tick positions matches the number of labels.
    if len(ax2_ticks) > len(years_months_study):
        ax2_ticks = ax2_ticks[: len(years_months_study)]

    ax2.set_xticks(ax2_ticks)
    ax2.set_xticklabels(
        years_months_study[::nth_label]
    )  # Ensure matching number of labels

    # 4. Label the secondary x-axis
    ax2.set_xlabel("Years Since 2017-09-29")
    # plt.xlabel('Date')
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Word Count")
    # plt.ylabel('Word Count')
    plt.title("Japanese Word Count by Date")
    plt.tight_layout()  # Adjust layout to ensure everything fits
    # plt.show()
    plt.savefig("/Users/samir/Documents/Programming/old dev/graph.png", format="png")


def plot_word_counts_to_2023():
    plt.clf()
    # Read word counts from CSV
    word_counts_by_date = {}
    with open(
        "/Users/samir/Documents/Programming/old dev/word_counts_to_2023.csv", "r"
    ) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            word_counts_by_date[row[0]] = int(row[1])

    # Sort dates
    sorted_dates = sorted(word_counts_by_date.keys())
    sorted_counts = [word_counts_by_date[date] for date in sorted_dates]
    """ print(sorted_dates)
    print(sorted_counts) """
    # Plot
    plt.plot(sorted_dates, sorted_counts, marker="o", linestyle="-")
    # higher_counts = [count + 4000 for count in sorted_counts]
    # plt.plot(sorted_dates, higher_counts, marker='x', linestyle='--', color='red', label='Higher by 4000')

    fig, ax1 = plt.subplots()

    ax1.plot(
        sorted_dates, sorted_counts, marker="o", linestyle="-", label="Original Data"
    )
    ax1.set_ylabel("Word Count", color="blue")
    ax1.tick_params("y", colors="blue")

    # Create a second y-axis
    ax2 = ax1.twinx()
    ax2.set_ylim(ax1.get_ylim()[0] + 4000, ax1.get_ylim()[1] + 4000)
    # ax2.set_ylabel('', color='red')
    ax2.tick_params("y", colors="red")

    # plt.xticks(rotation=90)  # Rotate date labels for better readability
    nth_label = 1  # Adjust this based on the number of data points you have
    ax1.set_xticks(sorted_dates[::nth_label])
    ax1.set_xticklabels(sorted_dates[::nth_label], rotation=45)

    # Define the start date

    date_string = "2017-09-29"
    year, month, day = map(int, date_string.split("-"))
    start_date = datetime.date(year, month, day)

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

    # 2. Create a secondary x-axis
    ax2 = ax1.twiny()

    # 3. Set the limits for the secondary x-axis
    ax2.set_xlim(ax1.get_xlim())

    # Use the tick positions of ax1 for ax2
    ax2_ticks = ax1.get_xticks()

    # If the number of ticks is more than your years_of_study, you can slice it.
    # This ensures that the number of tick positions matches the number of labels.
    if len(ax2_ticks) > len(years_months_study):
        ax2_ticks = ax2_ticks[: len(years_months_study)]

    ax2.set_xticks(ax2_ticks)
    ax2.set_xticklabels(
        years_months_study[: len(ax2_ticks)]
    )  # Ensure matching number of labels

    # 4. Label the secondary x-axis
    ax2.set_xlabel("Years Since 2017-09-29")
    # plt.xlabel('Date')
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Word Count")
    # plt.ylabel('Word Count')
    plt.title("Word Count by Date")
    plt.tight_layout()  # Adjust layout to ensure everything fits
    # plt.show()
    plt.savefig("/Users/samir/Documents/Programming/old dev/graph2.png", format="png")


def delete_word_count(target_date):
    # Read existing data
    existing_data = {}
    try:
        with open(CSV_FILENAME, "r") as csvfile:
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
    with open(CSV_FILENAME, "w") as csvfile:
        writer = csv.writer(csvfile)
        for date, count in existing_data.items():
            writer.writerow([date, count])

    print(f"Deleted word count for date {target_date}")


""" update_word_count("2023-10-05", 13077)
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
 """


# Replace YOUR_AWS_REGION, YOUR_AWS_ACCESS_KEY_ID, and YOUR_AWS_SECRET_ACCESS_KEY with your own values
client = boto3.client(
    "ses",
    region_name="eu-north-1",
    aws_access_key_id="",
    aws_secret_access_key="",
)


def request(action, **params):
    return {"action": action, "params": params, "version": 6}


def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode("utf-8")
    response = json.load(
        urllib.request.urlopen(
            urllib.request.Request("http://localhost:8765", requestJson)
        )
    )
    if len(response) != 2:
        raise Exception("response has an unexpected number of fields")
    if "error" not in response:
        raise Exception("response is missing required error field")
    if "result" not in response:
        raise Exception("response is missing required result field")
    if response["error"] is not None:
        raise Exception(response["error"])
    return response["result"]


# result = invoke("deckNames")
# result = len(invoke("findCards", query='"deck:0 Programming::0 CP Past Problem Tricks" is:due'))
p1 = len(
    invoke("findCards", query='"deck:0 Portuguese > English – Phrase Book _sorted"')
)
p2 = len(
    invoke(
        "findCards",
        query='"deck:0 Portuguese > English – Phrase Book _sorted" is:suspended',
    )
)
p3 = len(
    invoke(
        "findCards",
        query='"deck:0 Portuguese > English – Phrase Book _sorted" -is:suspended is:new',
    )
)
r1 = len(invoke("findCards", query='"deck:0 日本語"'))
r2 = len(invoke("findCards", query='"deck:0 日本語" is:suspended'))
r3 = len(invoke("findCards", query='"deck:0 日本語" -is:suspended is:new'))
# result = invoke("getDeckStats", decks=["2 Portuguese > English – Phrase Book _sorted"])

print("number of known 日本語 cards: {}".format(r1 - r2 - r3))
print("number of known portuguese cards: {}".format(p1 - p2 - p3))

current_date = datetime.date.today()

update_word_count(current_date.strftime("%Y-%m-%d"), r1 - r2 - r3)
plot_word_counts()
plot_word_counts_to_2023()

# Read the existing Markdown file
file_path = "/Users/samir/Desktop/GithubReadme/isym444/README.md"
with open(file_path, "r") as file:
    lines = file.readlines()

# Update the line with the new count

for i, line in enumerate(lines):
    if "**Japanese words:**" in line:
        lines[i] = f"**Japanese words:** {r1-r2-r3+4000}\n"
        print(f"found japanese! {r1-r2-r3+4000}")
        break
for i, line in enumerate(lines):
    if "**Portuguese words:**" in line:
        lines[i] = f"**Portuguese words:** {p1 - p2 - p3}\n"
        print("found portuguese!")
        break
with open(file_path, "w") as file:
    file.writelines(lines)
print("Updated the Markdown file with the new atcoder stats.")

import shutil
import os

# File paths
readme_path = "/Users/samir/Desktop/GithubReadme/isym444/README.md"
graph_source_path = "/Users/samir/Documents/Programming/graph.png"
graph_destination_path = "/Users/samir/Desktop/GithubReadme/isym444/graph.png"

# Copy the graph image to the README.md directory
shutil.copy(graph_source_path, graph_destination_path)

# Read the file contents
with open(readme_path, "r") as file:
    lines = file.readlines()


# Append the graph image at the bottom
graph_filename = os.path.basename(graph_destination_path)
# lines.append(f"\n![Graph Image]({graph_filename})\n")

# Write the modified contents back to the file
with open(readme_path, "w") as file:
    file.writelines(lines)


subject = f"日本語: {r1 - r2 - r3} ({r1-r2-r3+4000})" + " portuguese: {}".format(
    p1 - p2 - p3
)
body = f"日本語: {r1 - r2 - r3} ({r1-r2-r3+4000})" + " portuguese: {}".format(
    p1 - p2 - p3
)
sender = "samir.yep@gmail.com"
recipient = "samir.yep@gmail.com"

message = {
    "Subject": {"Data": subject},
    "Body": {"Text": {"Data": body}},
    "Source": sender,
    "Destination": {"ToAddresses": [recipient]},
    "Message": {"Body": {"Text": {"Data": body}}, "Subject": {"Data": subject}},
}

# response = client.send_email(Source=message["Source"], Destination=message["Destination"], Message=message["Message"])


import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def send_email_with_attachment(
    subject, body, sender, recipient, attachment_filename, attachment_filename2
):
    # Create a MIMEText object to represent the email
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject

    # Add the plain text body to the email
    msg.attach(MIMEText(body, "plain"))

    # Attach the PNG
    with open(attachment_filename, "rb") as f:
        attach = MIMEBase("application", "octet-stream")
        attach.set_payload(f.read())
        encoders.encode_base64(attach)
        attach.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(attachment_filename)}",
        )
        msg.attach(attach)

    # Second attachment
    with open(attachment_filename2, "rb") as f:
        attach2 = MIMEBase("application", "octet-stream")
        attach2.set_payload(f.read())
        encoders.encode_base64(attach2)
        attach2.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(attachment_filename2)}",
        )
        msg.attach(attach2)
    # Send the email
    response = client.send_raw_email(
        Source=sender,
        Destinations=[recipient],
        RawMessage={
            "Data": msg.as_string(),
        },
    )
    return response


# Call the function
attachment_filename = "/Users/samir/Documents/Programming/graph.png"
attachment_filename2 = "/Users/samir/Documents/Programming/graph2.png"

# send_email_with_attachment(
#     subject, body, sender, recipient, attachment_filename, attachment_filename2
# )
