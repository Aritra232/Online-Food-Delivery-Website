# Generated by Django 5.0.4 on 2024-05-18 13:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("service", "0016_account_role_alter_account_gender"),
    ]

    operations = [
        migrations.CreateModel(
            name="FinalDelivery",
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
                ("accepted_time", models.DateTimeField(auto_now_add=True)),
                (
                    "delivery_man",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="service.deliveryman",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="service.order"
                    ),
                ),
            ],
        ),
    ]
