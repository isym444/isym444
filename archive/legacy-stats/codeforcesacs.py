import requests


def get_accepted_problems_count(user_handle):
    url = f"https://codeforces.com/api/user.status?handle={user_handle}"
    response = requests.get(url)
    data = response.json()

    if data["status"] != "OK":
        return "Failed to retrieve data"

    accepted_problems = (
        set()
    )  # Use a set to avoid counting the same problem multiple times
    for submission in data["result"]:
        if submission["verdict"] == "OK":
            problem_id = (
                submission["problem"]["contestId"],
                submission["problem"]["index"],
            )
            accepted_problems.add(problem_id)

    return len(accepted_problems)


import requests
from datetime import datetime


def get_accepted_problems_count2024(user_handle):
    # Define the start of January 2024 in UNIX timestamp
    start_of_january_2024 = int(datetime(2024, 1, 1).timestamp())

    url = f"https://codeforces.com/api/user.status?handle={user_handle}"
    response = requests.get(url)
    data = response.json()

    if data["status"] != "OK":
        return "Failed to retrieve data"

    accepted_problems = set()
    for submission in data["result"]:
        submission_time = submission["creationTimeSeconds"]
        # Check if the submission is "Accepted" and after the start of January 2024
        if submission["verdict"] == "OK" and submission_time >= start_of_january_2024:
            problem_id = (
                submission["problem"]["contestId"],
                submission["problem"]["index"],
            )
            accepted_problems.add(problem_id)

    return len(accepted_problems)


# Example usage
user_handle = "isym444"
print(get_accepted_problems_count(user_handle))

# Example usage
user_handle = "isym444"
print(get_accepted_problems_count2024(user_handle))
