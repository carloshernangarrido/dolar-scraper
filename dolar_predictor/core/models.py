from django.db import models

# Create your models here.
from django.utils import timezone
# from core.utils import generate_code


# Customer class to keep track of name and image
class Precios(models.Model):
    date_time = models.DateTimeField(name='fecha')
    compra_value = models.DecimalField(max_digits=10, decimal_places=2, name='precio_de_compra')
    venta_value = models.DecimalField(max_digits=10, decimal_places=2, name='precio_de_venta')

    def __str__(self):
        return f'{self.fecha}, venta: ${self.precio_de_venta}, compra: ${self.precio_de_compra}'

    def save(self, *args, **kwargs):
        if self.fecha is None:
            self.fecha = timezone.now()
        return super().save(*args, **kwargs)
