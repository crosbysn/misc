# Generated by Django 4.0 on 2022-01-01 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0007_alter_company_relation_company_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='company_relation',
            name='raw_to_fields_attempted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='company_relation',
            name='raw_to_fields_successful',
            field=models.BooleanField(default=False),
        ),
    ]
