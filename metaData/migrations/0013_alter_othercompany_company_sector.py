# Generated by Django 4.0.3 on 2022-10-13 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metaData', '0012_alter_othercompany_company_sector'),
    ]

    operations = [
        migrations.AlterField(
            model_name='othercompany',
            name='company_sector',
            field=models.CharField(choices=[('retail', 'Retail business'), ('restaurant', 'Restaurant business'), ('manufacturing', 'Manufacturing'), ('wholesale', 'Wholesale business')], max_length=80, null=True),
        ),
    ]
