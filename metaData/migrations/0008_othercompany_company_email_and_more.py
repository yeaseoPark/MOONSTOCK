# Generated by Django 4.0.3 on 2022-10-12 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metaData', '0007_othercompany_note_alter_othercompany_company_sector'),
    ]

    operations = [
        migrations.AddField(
            model_name='othercompany',
            name='company_email',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='othercompany',
            name='company_address',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='othercompany',
            name='company_phoneNum',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='othercompany',
            name='company_sector',
            field=models.CharField(choices=[('wholesale', 'Wholesale business'), ('retail', 'Retail business'), ('restaurant', 'Restaurant business'), ('manufacturing', 'Manufacturing')], max_length=80, null=True),
        ),
    ]