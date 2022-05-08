import requests


def scrap(url: str):
    """Scraps the given url and looks for compra and venta dolar prices.
    Example: '<div class="topic">Compra</div>\n<div class="value">$198.00</div>
    <div class="topic">Venta</div>\n<div class="value">$201.00</div>'
    :argument url
    :returns (venta_value, compra_value)
    """
    page = requests.get(url)
    # print(page.text)
    ind_compra = page.text.find('<div class="topic">Compra</div>')
    ind_venta = page.text.find('<div class="topic">Venta</div>')

    if ind_compra != -1:
        try:
            compra_value = float(page.text[ind_compra + 51:ind_compra + 57])
        except ValueError:
            compra_value = 0.0
    else:
        compra_value = 0.0

    if ind_venta != -1:
        try:
            venta_value = float(page.text[ind_venta + 50:ind_venta + 56])
        except ValueError:
            venta_value = 0.0
    else:
        venta_value = 0.0
    return venta_value, compra_value
