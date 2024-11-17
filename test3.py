import plotly.graph_objects as go
import csv
import datetime

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

    # Define the start date
    date_string = "2017-09-29"
    year, month, day = map(int, date_string.split('-'))
    start_date = datetime.date(year, month, day)

    months_of_study = [(datetime.date(int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2])) - start_date).days // 30 for date in sorted_dates]
    years_months_study = [f"{month // 12} years {month % 12} months" for month in months_of_study]

    # Create interactive plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=sorted_dates, y=sorted_counts, mode='lines+markers',
                             name='Word Counts',
                             text=[f"Date: {date}<br>Word Count: {count}" for date, count in zip(sorted_dates, sorted_counts)],
                             hoverinfo='text',
                             yaxis='y1'))

    # Adjusting the primary x-axis
    fig.update_xaxes(title_text="Date", tickvals=list(range(len(sorted_dates))), ticktext=sorted_dates, tickangle=45, tickfont=dict(size=10))

    # Adjusting the primary y-axis
    fig.update_yaxes(title_text="Word Count")

    # Adding a secondary x-axis for "Years Since 2017-09-29"
    fig.update_layout(
        xaxis2=dict(
            tickvals=list(range(len(sorted_dates))),
            ticktext=years_months_study,
            title_text="Years Since 2017-09-29",
            overlaying='x',
            side='top',
            tickfont=dict(size=10)
        )
    )

    # Adjusting the secondary y-axis
    max_y = max(sorted_counts) + 4000
    min_y = min(sorted_counts) + 4000
    fig.update_layout(
        yaxis2=dict(
            title="Higher by 4000",
            overlaying='y',
            side='right',
            range=[min_y, max_y],
            showgrid=False,
            tickvals=list(range(min_y, max_y, (max_y-min_y)//5)),
            ticktext=[str(val) for val in range(min_y, max_y, (max_y-min_y)//5)]
        )
    )

    fig.show()

# Don't forget to define CSV_FILENAME before calling the function
CSV_FILENAME = "/Users/samir/Documents/Programming/word_counts_by_date.csv"
plot_word_counts()
