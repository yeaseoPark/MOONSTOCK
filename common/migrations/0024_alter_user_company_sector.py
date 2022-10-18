# Generated by Django 4.0.3 on 2022-10-14 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0023_alter_user_company_sector'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='company_sector',
            field=models.CharField(choices=[('manufacturing', 'Manufacturing'), ('wholesale', 'Wholesale business'), ('restaurant', 'Restaurant business'), ('retail', 'Retail business')], max_length=80),
        ),
    ]
