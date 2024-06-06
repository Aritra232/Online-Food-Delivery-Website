# Generated by Django 5.0.4 on 2024-04-20 05:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("service", "0004_restaurant"),
    ]

    operations = [
        migrations.CreateModel(
            name="FoodItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("picture", models.ImageField(upload_to="food_items/")),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("ingredients", models.TextField()),
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="service.restaurant",
                    ),
                ),
            ],
        ),
    ]
