# Generated by Django 2.0.1 on 2018-01-12 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameshop', '0002_auto_20180112_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
