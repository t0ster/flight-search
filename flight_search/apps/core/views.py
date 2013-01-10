from django.views.generic import FormView

from flight_search.apps.core.utils import get_flights
from flight_search.apps.core.forms import FlightSearchForm


class GetFormMixin(object):
    """
    Mixin that enables form processing on GET request
    """
    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = {'initial': self.get_initial()}
        if self.request.GET:
            kwargs.update({
                'data': self.request.REQUEST,
            })
        return kwargs

    def get(self, request, *args, **kwargs):
        if self.request.GET:
            return self.post(request, *args, **kwargs)
        return super(GetFormMixin, self).get(request, *args, **kwargs)


class FlightSearchFormView(FormView):
    template_name = "index.haml"
    form_class = FlightSearchForm


class FlightSearchResultsView(GetFormMixin, FormView):
    template_name = "search_results.haml"
    form_class = FlightSearchForm

    def form_valid(self, form):
        return self.get_results(form)

    def get_results(self, form):
        results = get_flights(
                    origin=form.cleaned_data['origin'],
                    destination=form.cleaned_data['destination'],
                    departure_date=form.cleaned_data['departure_date'],
                    show_many=form.cleaned_data['show_many']
        )
        return self.render_to_response(self.get_context_data(results=results))
