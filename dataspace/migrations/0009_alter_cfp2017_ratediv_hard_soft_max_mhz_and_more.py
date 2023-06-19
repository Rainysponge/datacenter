# Generated by Django 4.1 on 2023-05-30 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "dataspace",
            "0008_cfp2017_ratediv_hard_soft_cfp2017_speeddiv_hard_soft_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="cfp2017_ratediv_hard_soft",
            name="Max_MHz",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="cfp2017_ratediv_hard_soft",
            name="Nominal",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="cfp2017_speeddiv_hard_soft",
            name="Max_MHz",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="cfp2017_speeddiv_hard_soft",
            name="Nominal",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="cint2017_ratediv_hard_soft",
            name="Max_MHz",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="cint2017_ratediv_hard_soft",
            name="Nominal",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="cint2017_speeddiv_hard_soft",
            name="Max_MHz",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="cint2017_speeddiv_hard_soft",
            name="Nominal",
            field=models.IntegerField(),
        ),
    ]
