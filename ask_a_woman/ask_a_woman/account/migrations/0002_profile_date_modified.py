# Generated by Django 5.1.2 on 2024-11-05 20:03

import ask_a_woman.account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, verbose_name=ask_a_woman.account.models.AppUser),
        ),
    ]
