from django.views.generic import FormView
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

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


class FlightSearchFormView(GetFormMixin, FormView):
    """
    View that displays flight search form, if form is valid redirects
    to `FlightSearchResultsView` or displays errors
    """
    template_name = "index.haml"
    form_class = FlightSearchForm

    def form_valid(self, form):
        return redirect("%s?%s" % (reverse('search_results'), self.request.GET.urlencode()))


class FlightSearchResultsView(GetFormMixin, FormView):
    """
    View that displays flight search results.

    If normal request just renders "search_results.haml" template,
    if ajax request gets results and renders "_search_results.haml" with these results.

    If invalid request redirects to `FlightSearchFormView` via javascipt,
    see "_search_results.haml" template for details.
    """
    form_class = FlightSearchForm

    def get_template_names(self):
        if not self.request.is_ajax():
            template_name = "search_results.haml"
        else:
            template_name = "_search_results.haml"
        return [template_name]

    def get(self, request, *args, **kwargs):
        # if empty query string going back to search form
        if not self.request.GET:
            return redirect('home')
        # Request is not ajax so just rendering template which contains
        # "Loading ..." text
        if not self.request.is_ajax():
            return self.render_to_response(self.get_context_data())
        return super(FlightSearchResultsView, self).get(request, *args, **kwargs)

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
