from urllib import urlencode
from datetime import date

from django.test import TestCase


class TestHomePage(TestCase):
    def test_valid_request(self):
        response = self.client.get('/?' + urlencode({
            'origin': 'SFO',
            'destination': 'LAX',
            'departure_date': date.today().strftime('%m/%d/%Y'),
        }))
        self.failUnlessEqual(response.status_code, 302)

    def test_invalid_request(self):
        response = self.client.get('/?' + urlencode({
            'origin': 'SFO',
            'departure_date': date.today().strftime('%m/%d/%Y'),
        }))
        self.failUnlessEqual(response.status_code, 200)


class TestSearchPage(TestCase):
    def test_valid_request(self):
        response = self.client.get('/search/?' + urlencode({
            'origin': 'SFO',
            'destination': 'LAX',
            'departure_date': date.today().strftime('%m/%d/%Y'),
            }),
        HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertContains(response, "Search Results")

    def test_invalid_request(self):
        response = self.client.get('/search/?' + urlencode({
            'origin': 'SFO',
            'departure_date': date.today().strftime('%m/%d/%Y'),
            }),
        HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertContains(response, "window.location =")
