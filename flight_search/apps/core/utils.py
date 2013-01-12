from django.core.cache import cache

from flight_search.apps.core.gds import get_flights as gds_get_flights


CACHE_TIME = 10 * 60


def make_cache_key(origin, destination, departure_date, show_many):
    return 'gds:%s:%s:%s:%s' % (origin, destination, departure_date, show_many)


def get_flights(origin, destination, departure_date, show_many):
    """
    Wrapper around `gds.get_flights` which splits requests, converts results
    to list of dicts and caches gds response
    """
    results_from_cache = cache.get(make_cache_key(origin, destination, departure_date, show_many))
    if results_from_cache is not None:
        return results_from_cache
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

    cache.set(make_cache_key(origin, destination, departure_date, show_many),
              new_results, timeout=CACHE_TIME)

    return new_results
