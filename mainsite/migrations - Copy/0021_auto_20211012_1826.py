# Generated by Django 3.1 on 2021-10-12 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0020_relation_tag_sub_original_response'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company_relation',
            name='shouldcapi',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
