# Generated by Django 4.0 on 2021-12-30 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0003_company_relation_tags_raw'),
    ]

    operations = [
        migrations.AddField(
            model_name='company_relation',
            name='original_response',
            field=models.CharField(default='NULL', max_length=5000),
            preserve_default=False,
        ),
    ]