# Generated by Django 4.0.3 on 2022-10-14 00:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('registration_date', models.DateField(default=django.utils.timezone.now)),
                ('is_endItem', models.BooleanField(default=True)),
                ('price', models.IntegerField(default=0)),
                ('note', models.TextField(blank=True, null=True)),
                ('required', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OtherCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=200)),
                ('company_sector', models.CharField(choices=[('wholesale', 'Wholesale business'), ('retail', 'Retail business'), ('manufacturing', 'Manufacturing'), ('restaurant', 'Restaurant business')], max_length=80, null=True)),
                ('company_phoneNum', models.CharField(blank=True, max_length=200, null=True)),
                ('company_address', models.CharField(blank=True, max_length=300, null=True)),
                ('company_email', models.CharField(blank=True, max_length=300, null=True)),
                ('is_vendor', models.BooleanField()),
                ('is_customer', models.BooleanField()),
                ('note', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='myCompany', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('required', models.IntegerField(blank=True, default=0, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metaData.item')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
