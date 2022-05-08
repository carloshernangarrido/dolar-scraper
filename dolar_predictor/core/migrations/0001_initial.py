# Generated by Django 4.0.4 on 2022-05-07 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Precios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('precio de compra', models.DecimalField(decimal_places=2, max_digits=10)),
                ('precio de venta', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
