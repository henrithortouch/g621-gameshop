# Generated by Django 2.0.1 on 2018-01-23 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gameshop', '0009_auto_20180123_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gameshop.Developer'),
        ),
    ]