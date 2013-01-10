import random
from datetime import datetime, date, time, timedelta
from time import sleep


AIRLINES = ('AA', 'UA', 'DL', 'US')


def get_flights(origin, destination, departure_date, number_of_results,
                get_more=False, number_of_results_skipped=None):
    if get_more:
        if number_of_results_skipped is None:
            raise ValueError('specify number_of_results_skipped')
        number_of_results = number_of_results - number_of_results_skipped

    results = []
    for _ in range(number_of_results):
        airline = random.choice(AIRLINES)
        flight_number = random.randint(1, 999999)
        origin_destination = "%s-%s" % (origin, destination)
        departure_time = datetime.combine(
            date.today(),
            time()) + timedelta(seconds=(random.randint(0, 24 * 60 * 60))
        )
        arrival_time = (
            departure_time +
            timedelta(seconds=(random.randint(0, 8 * 60 * 60)))
        )
        results.append((airline, flight_number, origin_destination, departure_time, arrival_time))

    sleep(7 if number_of_results > 5 else 2)

    return results
