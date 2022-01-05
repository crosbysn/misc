# Generated by Django 4.0 on 2021-12-26 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='index_pages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index_code', models.CharField(default='NULL', max_length=15)),
                ('emptied', models.BooleanField(default=False)),
                ('checked_out', models.BooleanField(default=False)),
                ('next_page', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='skipped_company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('backend_string', models.CharField(max_length=40)),
                ('error_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]