# Generated by Django 4.0.3 on 2022-10-12 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0009_alter_user_company_sector'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='company_sector',
            field=models.CharField(choices=[('wholesale', 'Wholesale business'), ('restaurant', 'Restaurant business'), ('retail', 'Retail business'), ('manufacturing', 'Manufacturing')], max_length=80),
        ),
    ]
