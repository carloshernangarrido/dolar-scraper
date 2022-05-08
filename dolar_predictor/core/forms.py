from django import forms
from django.utils import timezone

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
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='desde',
                                initial=timezone.now().date())
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='hasta',
                                initial=timezone.now().date())
    chart_type = forms.ChoiceField(choices=CHART_CHOICES, label='tipo de gráfico')
    precio_type = forms.ChoiceField(choices=PRECIO_TYPE_CHOICES)
