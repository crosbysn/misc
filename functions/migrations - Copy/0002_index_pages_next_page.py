# Generated by Django 3.1 on 2021-11-02 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='index_pages',
            name='next_page',
            field=models.IntegerField(default=0),
        ),
    ]
