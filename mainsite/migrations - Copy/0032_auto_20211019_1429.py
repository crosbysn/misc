# Generated by Django 3.1 on 2021-10-19 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0031_company_relation_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company_relation',
            old_name='parent_company',
            new_name='origin_company',
        ),
    ]