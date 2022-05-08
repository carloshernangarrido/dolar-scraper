from scraper import scrap
import requests


if __name__ == '__main__':
    url = 'https://dolarhoy.com/cotizaciondolarblue'
    venta_value, compra_value = scrap(url)
    print(f'Compra: {compra_value}, Venta: {venta_value}')
