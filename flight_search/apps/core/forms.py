from datetime import date, timedelta

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions


AIRPORTS = ('SFO', 'LAX', 'NYC')


class FormStyleMixin(object):
    """
    Mixin for form styling, we are using twitter bootstrap
    (http://twitter.github.com/bootstrap/)
    """
    def __init__(self, *args, **kwargs):
        super(FormStyleMixin, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.layout.append(
            FormActions(
                Submit('search', 'Search', css_class='btn-primary'),
            )
        )


class DateInput(forms.DateInput):
    """
    Custom html5 DateInput widget <input type='date'>
    """
    input_type = 'date'


class FlightSearchForm(FormStyleMixin, forms.Form):
    ORIGINS_DESTINATIONS = tuple((a,) * 2 for a in AIRPORTS)

    origin = forms.ChoiceField(choices=ORIGINS_DESTINATIONS)
    destination = forms.ChoiceField(choices=ORIGINS_DESTINATIONS)
    departure_date = forms.DateField(initial=(date.today() + timedelta(1)),
                                     widget=DateInput(format='%m/%d/%Y'))
    show_many = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(FlightSearchForm, self).__init__(*args, **kwargs)
        self.helper.form_method = 'get'

    def clean_departure_date(self):
        departure_date = self.cleaned_data['departure_date']
        if departure_date < date.today():
            raise forms.ValidationError("Departure date can not be in the past")
        return departure_date

    def clean(self):
        cleaned_data = super(FlightSearchForm, self).clean()
        origin = cleaned_data.get("origin")
        destination = cleaned_data.get("destination")
        if origin and origin == destination:
            raise forms.ValidationError("Origin and destination can not be the same")
        return cleaned_data
