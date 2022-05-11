import pandas
import pytz
from django.shortcuts import render, redirect
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
        precios_qs = Precios.objects.filter(fecha__date__lte=date_to, fecha__date__gte=date_from)

        if len(precios_qs) > 0:
            precios_df = pandas.DataFrame(precios_qs.values())
            precios_df['fecha'] = precios_df['fecha'].\
                apply(lambda x: timezone.localtime(x, 'America/Argentina/Buenos_Aires'))
            precios_df['fecha'] = precios_df['fecha'].apply(lambda x: x.strftime('%d/%m/%Y %H:%M:%S'))
            precios_df.rename({'fecha': 'fecha y hora', 'precio_de_compra': 'compra', 'precio_de_venta': 'venta'},
                              axis=1, inplace=True)
            chart = get_chart(chart_type, precios_df, precio_type)
            precios_df = precios_df.to_html(index=False, justify='left', col_space=200).\
                replace('<td>', '<td align="left">')
        else:
            messages.warning(request, "Todavía no hay datos...")

    context = {
        'search_form': search_form,
        'precios_df': precios_df,
        'chart': chart,
    }
    return render(request, 'precios.html', context)


def scrap(request):
    url = 'https://dolarhoy.com/cotizaciondolarblue'
    venta_value, compra_value = scrap_now(url)
    # print(f'Compra: {compra_value}, Venta: {venta_value}')
    precio = Precios(fecha=timezone.now(),
                     precio_de_venta=Decimal.from_float(venta_value),
                     precio_de_compra=Decimal.from_float(compra_value))
    precio.save()
    return redirect('precios')
