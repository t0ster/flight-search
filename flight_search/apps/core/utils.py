from datetime import date

from flight_search.apps.core.gds import get_flights as gds_get_flights


def get_flights(origin, destination, departure_date, show_many):
    number_of_results = 15 if show_many else 10
    number_of_results_per_request = 5
    number_of_queries = (number_of_results / number_of_results_per_request)

    results = []
    results.extend(gds_get_flights(origin, destination, departure_date,
                   number_of_results=number_of_results_per_request))

    for i in range(number_of_queries - 1):
        results.extend(gds_get_flights(
            origin, destination, departure_date,
            get_more=True,
            number_of_results=(number_of_results_per_request * (i + 1 + 1)),
            number_of_results_skipped=(number_of_results_per_request * (i + 1))
        ))

    new_results = []
    for result in results:
        airline, flight_number, origin_destination, departure_time, arrival_time = result
        new_results.append({
            'airline': airline,
            'flight_number': flight_number,
            'origin_destination': origin_destination,
            'departure_time': departure_time,
            'arrival_time': arrival_time
        })

    return new_results
