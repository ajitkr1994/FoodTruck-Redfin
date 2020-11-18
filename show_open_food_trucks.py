#!/usr/bin/env python

# Make sure to install requests before running:
# > pip install requests
# Documentation for the requests library can be found here: http://docs.python-requests.org/en/master/

import requests
from query_builder import QueryBuilder

# APP_TOKEN from the website.
APP_TOKEN = '5ziBX1z9hQeV73djUjc3Rq9gf'

def print_results(data, fields, first_time):
    """ 
    Print the results on the console.
    """
    open_trucks = []

    for row in data:
        open_truck = []

        for field in fields:
            open_truck.append(row[field])

        open_trucks.append(open_truck)

    if first_time:
        print("\t".join([field for field in fields]))
    else:
        pass

    for truck in open_trucks:
        print("\t".join([truck[i] for i in range(len(truck))]))

def handle_requests(base_url, query_builder, fields, n_results):
    """
    Processes the requests one by one and continues to do so until the user inputs the 'y' character.
    Calls the print_results function which prints the output data.
    """

    first_request = True

    # Continue requesting data until break
    while True:
        final_url = base_url + query_builder.query()

        header={'X-App-Token': APP_TOKEN}

        response = requests.get(final_url, headers = header)

        # 200 = Success
        if response.status_code == 200:
            data = response.json()

            # Print the results. For the first request, we also print the header, and skip header for other requests.
            print_results(data, fields, first_time = first_request)

            # Break when we reach end of data.
            if len(data) < n_results:
                print("End of results. Breaking.")
                break

            first_request = False

            user_input = input("See more results? (y/n): ").lower()

            # If the user input is 'y' or 'yes', then we continue requesting data from the API.
            if user_input == "y":
                pass
            else:
                print("Not printing more results. Breaking.")
                break

        else:
            # Handling unsuccessful request.
            print("Request unsuccessful with status =", response.text)
            break


if __name__ == "__main__":

    base_url = "http://data.sfgov.org/resource/bbb8-hzi6.json"
    fields = ["applicant", "location"]
    n_results = 10
    order_by = "applicant"
    ascending = True

    query_builder = QueryBuilder(base_url, fields, n_results, order_by, ascending)

    handle_requests(base_url, query_builder, fields, n_results)
