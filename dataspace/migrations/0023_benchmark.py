# Generated by Django 4.1 on 2023-05-31 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dataspace", "0022_alter_cfp2017_ratediv_hard_soft_storage_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Benchmark",
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
                ("benchmark_name", models.CharField(max_length=64)),
            ],
        ),
    ]
