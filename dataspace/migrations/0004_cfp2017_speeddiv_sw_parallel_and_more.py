# Generated by Django 4.1 on 2023-05-30 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dataspace", "0003_cfp2017_ratediv_ps_cfp2017_speeddiv_ps_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="cfp2017_speeddiv",
            name="sw_parallel",
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="cint2017_speeddiv",
            name="sw_parallel",
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
