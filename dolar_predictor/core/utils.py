import uuid, base64
from .models import *
from io import BytesIO
from matplotlib import pyplot
import datetime
import pandas as pd


import requests
from bs4 import BeautifulSoup


def scrap_now(url: str):
    """Scraps the given url and looks for compra and venta dolar prices.
    Example: '<div class="topic">Compra</div>\n<div class="value">$198.00</div>
    <div class="topic">Venta</div>\n<div class="value">$201.00</div>'
    :argument url
    :returns (venta_value, compra_value)
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    cotizaciones = soup.find_all('div', class_="tile cotizacion_value")
    precio_valores = []
    for cotizacion in cotizaciones:
        precios = cotizacion.find_all('div', class_="value")
        for i, precio in enumerate(precios):
            ind = precio.text.find('$')
            precio_valores.append(float(precio.text[ind+1:-1]))
    # print(precio_valores)
    venta_value = max(precio_valores)
    compra_value = min(precio_valores)
    return venta_value, compra_value


def get_graph():
    buffer = BytesIO()
    pyplot.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_chart(chart_type, data, precio_type, **kwargs):
    # PRECIO_TYPE_CHOICES = (
    #     ('#1', 'Venta'),
    #     ('#2', 'Compra'),
    #     ('#3', 'Ambos'),
    # )
    pyplot.switch_backend('AGG')
    fig = pyplot.figure(figsize=(10, 4))
    key = 'fecha'
    d = data
    date_time_index = pd.to_datetime(data['fecha'])

    if chart_type == '#1':
        print("Bar graph")
        if precio_type == '#1':
            pyplot.bar(d[key], d['venta'])
        elif precio_type == '#2':
            pyplot.bar(d[key], d['compra'])
    elif chart_type == '#2':
        print("Line graph")
        if precio_type == '#1':
            pyplot.plot(date_time_index, d['venta'], color='gray', marker='o', linestyle='dashed')
        elif precio_type == '#2':
            pyplot.plot(date_time_index, d['compra'], color='gray', marker='o', linestyle='dashed')
    else:
        print("Apparently...chart_type not identified")
    pyplot.tight_layout()
    pyplot.gcf().autofmt_xdate()
    chart = get_graph()
    return chart
