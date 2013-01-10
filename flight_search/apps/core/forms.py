from datetime import date, timedelta

from django import forms


AIRPORTS = ('SFO', 'LAX', 'NYC')


class FlightSearchForm(forms.Form):
    ORIGINS_DESTINATIONS = tuple((a,) * 2 for a in AIRPORTS)

    origin = forms.ChoiceField(choices=ORIGINS_DESTINATIONS)
    destination = forms.ChoiceField(choices=ORIGINS_DESTINATIONS)
    departure_date = forms.DateField(initial=(date.today() + timedelta(1)),
                                     widget=forms.DateInput(format='%m/%Y/%d'))
    show_many = forms.BooleanField(required=False)
