# Generated by Django 4.1 on 2023-05-31 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("dataspace", "0027_specrate2017_ratediv_int_score_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="SPECrate2017_speeddiv_fp_score",
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
                ("p_id", models.IntegerField()),
                ("test_sponsor", models.CharField(max_length=128)),
                ("System_Name", models.CharField(max_length=128)),
                ("SPECrate2017_fp_base", models.FloatField()),
                ("SPECrate2017_fp_peak", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="CFP2017_speeddiv_result",
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
                ("p_id", models.IntegerField()),
                ("test_sponsor", models.CharField(max_length=128)),
                ("System_Name", models.CharField(max_length=128)),
                ("turn", models.IntegerField()),
                ("basecol_time", models.FloatField()),
                ("peakcol_time", models.FloatField()),
                ("basecol_ratio", models.FloatField()),
                ("peakcol_ratio", models.FloatField()),
                ("basecol_threads", models.FloatField()),
                ("peakcol_threads", models.FloatField()),
                (
                    "benchmark",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dataspace.benchmark",
                    ),
                ),
            ],
        ),
    ]
