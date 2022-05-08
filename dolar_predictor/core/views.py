# from django.shortcuts import render
# import pandas
from django.shortcuts import render
from django.views.generic import ListView
from .forms import PreciosSearchForm


def precios(request):
    search_form = PreciosSearchForm(request.POST or None)
    context = {
        'search_form': search_form,
    }
    return render(request, 'precios.html',  context)
