# Generated by Django 4.1 on 2023-05-30 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dataspace", "0009_alter_cfp2017_ratediv_hard_soft_max_mhz_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cfp2017_ratediv_hard_soft",
            name="Peak_Pointers",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="cfp2017_speeddiv_hard_soft",
            name="Peak_Pointers",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="cint2017_ratediv_hard_soft",
            name="Peak_Pointers",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="cint2017_speeddiv_hard_soft",
            name="Peak_Pointers",
            field=models.IntegerField(),
        ),
    ]
