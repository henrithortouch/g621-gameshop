# Generated by Django 2.0.1 on 2018-02-16 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameshop', '0004_auto_20180216_1526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='money',
        ),
    ]
