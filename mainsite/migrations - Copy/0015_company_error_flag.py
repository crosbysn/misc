# Generated by Django 3.1 on 2021-09-28 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0014_auto_20210921_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='error_flag',
            field=models.BooleanField(default=False),
        ),
    ]
