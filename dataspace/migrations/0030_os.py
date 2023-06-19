# Generated by Django 4.1 on 2023-06-04 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dataspace", "0029_specrate2017_speeddiv_int_score_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="OS",
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
                ("OS_name", models.CharField(max_length=128)),
                ("OS_value", models.IntegerField()),
            ],
        ),
    ]
