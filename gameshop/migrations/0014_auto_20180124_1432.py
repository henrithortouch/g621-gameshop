# Generated by Django 2.0.1 on 2018-01-24 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameshop', '0013_auto_20180124_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='bought',
            field=models.ManyToManyField(blank=True, to='gameshop.Profile'),
        ),
    ]