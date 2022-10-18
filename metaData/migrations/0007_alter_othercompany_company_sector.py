# Generated by Django 4.0.3 on 2022-10-14 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metaData', '0006_alter_item_registration_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='othercompany',
            name='company_sector',
            field=models.CharField(choices=[('restaurant', 'Restaurant business'), ('retail', 'Retail business'), ('wholesale', 'Wholesale business'), ('manufacturing', 'Manufacturing')], max_length=80, null=True),
        ),
    ]