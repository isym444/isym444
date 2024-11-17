import json
import urllib.request
import datetime
import time
import csv

CSV_FILENAME = "/Users/samir/Documents/Programming/Portuguese_word_counts_temp.csv"

def request(action, **params):
    return {"action": action, "params": params, "version": 6}

def invoke(action, **params):
    request_json = json.dumps(request(action, **params)).encode("utf-8")
    response = json.load(
        urllib.request.urlopen(
            urllib.request.Request("http://localhost:8765", request_json)
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

def get_all_note_creation_dates(deck_name):
    query = f'"deck:{deck_name}"'
    cards = invoke("findCards", query=query)
    card_info = invoke("cardsInfo", cards=cards)
    note_ids = list(set(card['note'] for card in card_info))
    notes_info = invoke("notesInfo", notes=note_ids)

    # Extract creation dates, handling cases where 'Created' may be missing
    note_dates = []
    for note in notes_info:
        if 'Created' in note:
            note_dates.append(datetime.datetime.fromtimestamp(note['Created'] / 1000.0))
        else:
            print(f"Warning: 'Created' key missing for note: {note}")
    return note_dates

def generate_monthly_counts(deck_name, start_date, end_date):
    note_dates = get_all_note_creation_dates(deck_name)
    note_dates.sort()
    
    current_date = start_date
    monthly_counts = {}
    
    while current_date <= end_date:
        month_end = current_date.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
        month_end = month_end - datetime.timedelta(days=month_end.day)
        
        count = sum(1 for date in note_dates if date <= month_end)
        monthly_counts[current_date.strftime("%Y-%m")] = count
        
        current_date = month_end + datetime.timedelta(days=1)
    
    return monthly_counts

def save_to_csv(data, filename):
    with open(filename, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Month", "Count"])
        for month, count in data.items():
            writer.writerow([month, count])

deck_name = "0 Portuguese > English – Phrase Book _sorted"
start_date = datetime.date(2017, 9, 29)  # Change this to your start date
end_date = datetime.date.today()

monthly_counts = generate_monthly_counts(deck_name, start_date, end_date)
save_to_csv(monthly_counts, CSV_FILENAME)