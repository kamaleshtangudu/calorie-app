# Generated by Django 3.1.13 on 2021-12-07 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='daily_price_threshold',
            new_name='monthly_price_threshold',
        ),
    ]
