# Generated by Django 4.0 on 2021-12-30 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0004_company_relation_original_response'),
    ]

    operations = [
        migrations.AddField(
            model_name='company_relation',
            name='index_page_source',
            field=models.CharField(default='CREATED FROM RECORD WITHOUT INDEX RECORDED.', max_length=50),
        ),
    ]
