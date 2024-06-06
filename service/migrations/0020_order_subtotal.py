# Generated by Django 5.0.4 on 2024-05-29 18:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("service", "0019_order_accepted"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="subtotal",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
