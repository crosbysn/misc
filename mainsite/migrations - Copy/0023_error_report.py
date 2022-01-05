# Generated by Django 3.1 on 2021-10-18 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0022_auto_20211012_1826'),
    ]

    operations = [
        migrations.CreateModel(
            name='error_report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_type', models.CharField(max_length=200)),
                ('model_inst', models.CharField(max_length=200)),
                ('date', models.DateField(auto_now_add=True)),
                ('text', models.TextField(default='NULL', max_length=5000)),
            ],
        ),
    ]