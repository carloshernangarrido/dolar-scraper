from scraper import scrap_now


if __name__ == '__main__':
    url = 'https://dolarhoy.com/cotizaciondolarblue'
    venta_value, compra_value = scrap_now(url)
    print(f'Compra: {compra_value}, Venta: {venta_value}')
