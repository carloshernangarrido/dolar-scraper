from django import forms
from django.utils import timezone

CHART_CHOICES = (
    ('0', 'Constante'),
    ('1', 'Lineal'),
    ('2', 'Cuadrático'),
    ('3', 'Cúbico'),
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
    chart_type = forms.ChoiceField(choices=CHART_CHOICES, label='Grado del polinomio de Taylor')
    precio_type = forms.ChoiceField(choices=PRECIO_TYPE_CHOICES)
