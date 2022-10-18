# Generated by Django 4.0.3 on 2022-10-18 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0027_alter_user_company_sector'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='company_sector',
            field=models.CharField(choices=[('retail', 'Retail business'), ('restaurant', 'Restaurant business'), ('manufacturing', 'Manufacturing'), ('wholesale', 'Wholesale business')], max_length=80),
        ),
    ]
