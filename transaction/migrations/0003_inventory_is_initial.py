# Generated by Django 4.0.3 on 2022-10-14 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_alter_inventory_referencedate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='is_initial',
            field=models.BooleanField(default=False),
        ),
    ]
