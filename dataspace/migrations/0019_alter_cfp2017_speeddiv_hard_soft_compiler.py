# Generated by Django 4.1 on 2023-05-30 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dataspace", "0018_alter_cfp2017_ratediv_hard_soft_compiler_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cfp2017_speeddiv_hard_soft",
            name="Compiler",
            field=models.CharField(max_length=256),
        ),
    ]
