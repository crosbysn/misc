# Generated by Django 3.1 on 2021-10-18 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0024_error_report_error_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company_relation',
            name='registered_cap',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='company_relation',
            name='shouldcapi',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=18, null=True),
        ),
    ]