# Generated by Django 2.0.1 on 2018-02-16 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameshop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genre',
            name='id',
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]