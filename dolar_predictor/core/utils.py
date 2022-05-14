import uuid, base64

import numpy as np

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


def polynomial(data, degree):
    data = reduce(data)
    if len(data) < 4:
        return data
    if 'fecha y hora' in data:
        date_time_index = pd.to_datetime(data['fecha y hora'], format='%d/%m/%Y %H:%M:%S')
    elif 'fecha' in data:
        date_time_index = pd.to_datetime(data['fecha'], format='%d/%m/%Y')
    else:
        return None
    t = np.array([pd.Timestamp(_).value for _ in date_time_index]).reshape((-1, 1))
    c = data['compra'].values.astype('float').reshape((-1, 1))
    v = data['venta'].values.astype('float').reshape((-1, 1))
    tcv = np.hstack((t, c, v))
    poly_c = np.polyfit(t.flatten(), c, deg=degree)
    poly_v = np.polyfit(t.flatten(), v, deg=degree)
    date_time_num = date_time_index.values.astype(float)
    # delta = date_time_num[-1] - date_time_num[0]
    step = date_time_num[-1] - date_time_num[-2]
    horizon = 15
    t_ext = np.linspace(date_time_num[-1]+step, date_time_num[-1]+horizon*step, horizon)
    c_ext = np.polyval(poly_c, t_ext)
    v_ext = np.polyval(poly_v, t_ext)
    tcv_ext = np.hstack((t_ext.reshape((-1, 1)), c_ext.reshape((-1, 1)), v_ext.reshape((-1, 1))))
    data_ext = pd.DataFrame(tcv_ext, columns=['t', 'compra', 'venta'])
    data_ext['fecha'] = data_ext['t'].\
        apply(lambda x: datetime.datetime.strftime(pd.to_datetime(x), '%d/%m/%Y'))
    # print(data)
    # print(data_ext)
    return data_ext


def get_chart(data, precio_type, degree):
    # PRECIO_TYPE_CHOICES = (
    #     ('#1', 'Venta'),
    #     ('#2', 'Compra'),
    #     ('#3', 'Ambos'),
    # )

    if 'fecha y hora' in data:
        date_time_index = pd.to_datetime(data['fecha y hora'], format='%d/%m/%Y %H:%M:%S')
    elif 'fecha' in data:
        date_time_index = pd.to_datetime(data['fecha'], format='%d/%m/%Y')
    else:
        return None

    pyplot.switch_backend('AGG')
    pyplot.figure(figsize=(10, 5))
    # Taylor polynomial
    data_ext = polynomial(data, degree)
    date_time_index_ext = pd.to_datetime(data_ext['fecha'], format='%d/%m/%Y')

    if precio_type == '#1':
        pyplot.plot(date_time_index, data['venta'], color='blue', marker='x', linestyle='dashed', label='venta')
        pyplot.plot(date_time_index_ext, data_ext['venta'], color='blue', marker='', linestyle='-', label='predicción')
    elif precio_type == '#2':
        pyplot.plot(date_time_index, data['compra'], color='red', marker='o', linestyle='dashed', label='compra')
        pyplot.plot(date_time_index_ext, data_ext['compra'], color='red', marker='', linestyle='-', label='predicción')
    else:
        pyplot.plot(date_time_index, data['venta'], color='blue', marker='x', linestyle='dashed', label='venta')
        pyplot.plot(date_time_index, data['compra'], color='red', marker='o', linestyle='dashed', label='compra')
        pyplot.plot(date_time_index_ext, data_ext['venta'], color='blue', marker='', linestyle='-', label='predicción')
        pyplot.plot(date_time_index_ext, data_ext['compra'], color='red', marker='', linestyle='-', label='predicción')
    pyplot.legend()
    pyplot.tight_layout()
    pyplot.gcf().autofmt_xdate()
    chart = get_graph()
    return chart


def reduce(d):
    d_copy = d.copy()
    d_copy.insert(loc=0, column='fecha', value=d['fecha y hora'].str[0:10])
    d_copy = d_copy.drop(['fecha y hora'], axis=1)
    d_copy.drop_duplicates(subset='fecha', keep='first', inplace=True, ignore_index=False)
    return d_copy
