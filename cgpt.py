# Import requests and BeautifulSoup libraries
import requests
from bs4 import BeautifulSoup

# Define the website url
url = "https://www.bbc.com/news"

# Send a GET request to the website and store the response
response = requests.get(url)

# Check if the response status code is 200 (OK)
if response.status_code == 200:
    # Parse the response content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the elements with the class name "gs-c-promo-heading__title"
    titles = soup.find_all(class_="gs-c-promo-heading__title")

    # Loop through the titles and print the text content
    for title in titles:
        print(title.text)
        print("\n")
else:
    # Print an error message if the response status code is not 200
    print("Error: Unable to access the website")
