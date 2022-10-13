# Generated by Django 4.0.3 on 2022-10-13 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metaData', '0008_othercompany_company_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='depth',
        ),
        migrations.RemoveField(
            model_name='item',
            name='numchild',
        ),
        migrations.RemoveField(
            model_name='item',
            name='path',
        ),
        migrations.AlterField(
            model_name='othercompany',
            name='company_sector',
            field=models.CharField(choices=[('manufacturing', 'Manufacturing'), ('restaurant', 'Restaurant business'), ('wholesale', 'Wholesale business'), ('retail', 'Retail business')], max_length=80, null=True),
        ),
    ]