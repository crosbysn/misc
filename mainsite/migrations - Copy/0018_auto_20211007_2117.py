# Generated by Django 3.1 on 2021-10-08 01:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0017_auto_20211007_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='company_relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation_type', models.CharField(max_length=200)),
                ('econ_kind', models.CharField(default='NULL', help_text='Value listed in QCC API response, carried over for data completeness.', max_length=200)),
                ('percent', models.DecimalField(decimal_places=3, default=0, max_digits=5)),
                ('percent_total', models.DecimalField(decimal_places=3, default=0, help_text='Value listed in QCC API response, carried over for data completeness.', max_digits=5)),
                ('org', models.IntegerField(default=0, help_text='Value listed in QCC API response, carried over for data completeness.')),
                ('shouldcapi', models.IntegerField(default='NULL')),
                ('stockrightnum', models.CharField(default='NULL', help_text='Value listed in QCC API response, carried over for data completeness.', max_length=200)),
                ('detailcount', models.IntegerField(default=0, help_text='Value listed in QCC API response, carried over for data completeness.')),
                ('shortstatus', models.CharField(default='在业', help_text='Value listed in QCC API response, carried over for data completeness.', max_length=200)),
                ('stocktype', models.CharField(default='NULL', help_text='Value listed in QCC API response, carried over for data completeness.', max_length=200)),
                ('investtype', models.CharField(default='NULL', help_text='Value listed in QCC API response, carried over for data completeness.', max_length=200)),
                ('registered_cap', models.IntegerField(default='NULL')),
                ('detaillist', models.CharField(default='NULL', help_text='Value listed in QCC API response, carried over for data completeness.', max_length=200)),
                ('child_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Child', to='mainsite.company')),
                ('parent_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Parent', to='mainsite.company')),
                ('tags', models.ManyToManyField(to='mainsite.relation_tag_sub')),
            ],
        ),
        migrations.DeleteModel(
            name='equity_relation',
        ),
    ]
