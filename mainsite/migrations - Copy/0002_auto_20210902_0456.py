# Generated by Django 3.1 on 2021-09-02 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='parent_company',
            field=models.ManyToManyField(null=True, through='mainsite.ownership_through_class', to='mainsite.company'),
        ),
        migrations.AlterField(
            model_name='company',
            name='法定代表人',
            field=models.ManyToManyField(null=True, through='mainsite.operator_through_class', to='mainsite.individual'),
        ),
    ]
