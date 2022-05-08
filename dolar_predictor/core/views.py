import pandas
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib import messages
from .forms import PreciosSearchForm
from .models import *
# Create your views here.
from .utils import get_chart


def precios(request):
    sales_df = None
    chart = None
    no_data = None
    search_form = PreciosSearchForm(request.POST or None)

    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        precio_type = request.POST.get('precio_type')
        print(date_from, date_to, chart_type, precio_type)
        precios_qs = Precios.objects.filter(created__date__lte=date_to, created__date__gte=date_from)

        if len(precios_qs) > 0:
            precios_df = pandas.DataFrame(precios_qs.values())
            print(precios_df)
            precios_df['date_time'] = precios_df['date_time'].apply(lambda x: x.strftime('%Y%m%d %H:%M:%S'))
            precios_df.rename({'compra_value': 'compra', 'venta_value': 'venta'}, axis=1,
                              inplace=True)
            chart = get_chart(chart_type, precios_df, precio_type)
            precios_df_html = precios_df.to_html()

        else:
            messages.warning(request, "Todavía no hay datos...")

    context = {
        'search_form': search_form,
        'precios_df': precios_df_html,
        'chart': chart,
    }
    return render(request, 'precios.html', context)
