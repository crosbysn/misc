# Generated by Django 3.1 on 2021-11-01 22:44

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
                ('last_page_checked', models.CharField(default='0', max_length=4)),
                ('emptied', models.BooleanField(default=False)),
            ],
        ),
    ]