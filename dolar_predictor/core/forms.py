from django import forms

CHART_CHOICES = (
    ('#1', 'Bar Graph'),
    ('#2', 'Line Graph')
)
PRECIO_TYPE_CHOICES = (
    ('#1', 'Venta'),
    ('#2', 'Compra'),
    ('#3', 'Ambos'),
)


class PreciosSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='desde')
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='hasta')
    chart_type = forms.ChoiceField(choices=CHART_CHOICES, label='tipo de gráfico')
    precio_type = forms.ChoiceField(choices=PRECIO_TYPE_CHOICES)
