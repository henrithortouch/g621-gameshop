# Generated by Django 2.0.1 on 2018-02-16 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameshop', '0005_remove_profile_money'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game_state',
            name='submitted_score',
            field=models.FloatField(default=0),
        ),
    ]
