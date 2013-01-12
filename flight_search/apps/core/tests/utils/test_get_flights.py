from datetime import date

from django.test import TestCase

from flight_search.apps.core.utils import get_flights


class TestGetFlights(TestCase):
    """
    Basic tests for `flight_search.apps.core.utils.get_flights`
    """
    def test(self):
        results = get_flights("SFO", "NYC", date.today(), show_many=False)
        self.assertEquals(len(results), 10)

    def test_show_many(self):
        results = get_flights("SFO", "NYC", date.today(), show_many=True)
        self.assertEquals(len(results), 15)
