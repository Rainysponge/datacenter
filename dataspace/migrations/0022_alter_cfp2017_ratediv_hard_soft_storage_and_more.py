# Generated by Django 4.1 on 2023-05-30 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dataspace", "0021_alter_cfp2017_ratediv_hard_soft_other_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cfp2017_ratediv_hard_soft",
            name="Storage",
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name="cfp2017_speeddiv_hard_soft",
            name="Storage",
            field=models.CharField(max_length=512),
        ),
        migrations.AlterField(
            model_name="cint2017_ratediv_hard_soft",
            name="Storage",
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name="cint2017_speeddiv_hard_soft",
            name="Storage",
            field=models.CharField(max_length=256),
        ),
    ]
