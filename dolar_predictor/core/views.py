import pandas
import pytz
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib import messages
from .forms import PreciosSearchForm
from .models import *
from .utils import get_chart, scrap_now
from django.conf import settings
import datetime
from decimal import Decimal


def precios(request):
    precios_df = None
    chart = None
    no_data = None
    search_form = PreciosSearchForm(request.POST or None)

    if request.method == 'POST':
        tz = pytz.timezone(settings.TIME_ZONE)
        str_from = request.POST.get('date_from')
        naive_from = datetime.datetime.strptime(str_from, '%Y-%m-%d')
        date_from = tz.localize(naive_from, is_dst=None).astimezone(pytz.utc)
        str_to = request.POST.get('date_to')
        naive_to = datetime.datetime.strptime(str_to, '%Y-%m-%d')
        date_to = tz.localize(naive_to, is_dst=None).astimezone(pytz.utc)
        chart_type = request.POST.get('chart_type')
        precio_type = request.POST.get('precio_type')
        print(date_from, date_to, chart_type, precio_type)
        precios_qs = Precios.objects.filter(fecha__lte=date_to, fecha__gte=date_from)

        if len(precios_qs) > 0:
            precios_df = pandas.DataFrame(precios_qs.values())
            print(precios_df)
            precios_df['date_time'] = precios_df['date_time'].apply(lambda x: x.strftime('%Y%m%d %H:%M:%S'))
            precios_df.rename({'compra_value': 'compra', 'venta_value': 'venta'}, axis=1,
                              inplace=True)
            chart = get_chart(chart_type, precios_df, precio_type)
            precios_df = precios_df.to_html()
        else:
            messages.warning(request, "Todavía no hay datos...")

    context = {
        'search_form': search_form,
        'precios_df': precios_df,
        'chart': chart,
    }
    return render(request, 'precios.html', context)


def scrap(request):
    messages.warning(request, 'scrap!')
    url = 'https://dolarhoy.com/cotizaciondolarblue'
    venta_value, compra_value = scrap_now(url)
    print(f'Compra: {compra_value}, Venta: {venta_value}')
    precio = Precios(fecha=timezone.now(),
                     precio_de_venta=Decimal.from_float(venta_value),
                     precio_de_compra=Decimal.from_float(compra_value))
    precio.save()
    return precios(request)
