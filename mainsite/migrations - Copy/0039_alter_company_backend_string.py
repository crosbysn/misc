# Generated by Django 3.2.9 on 2021-11-10 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0038_figure_relation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='backend_string',
            field=models.CharField(max_length=40),
        ),
    ]
