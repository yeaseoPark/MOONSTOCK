# Generated by Django 4.0.3 on 2022-10-14 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metaData', '0004_alter_othercompany_company_sector'),
    ]

    operations = [
        migrations.AlterField(
            model_name='othercompany',
            name='company_sector',
            field=models.CharField(choices=[('manufacturing', 'Manufacturing'), ('restaurant', 'Restaurant business'), ('retail', 'Retail business'), ('wholesale', 'Wholesale business')], max_length=80, null=True),
        ),
    ]
