# Generated by Django 4.1 on 2023-06-04 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dataspace", "0031_summary_results_company_summary_results_hz"),
    ]

    operations = [
        migrations.CreateModel(
            name="sponsor_system",
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
                ("sponsor", models.CharField(max_length=128)),
                ("System_name", models.CharField(max_length=128)),
            ],
        ),
    ]
