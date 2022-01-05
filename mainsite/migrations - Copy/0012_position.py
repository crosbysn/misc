# Generated by Django 3.2.4 on 2021-09-13 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0011_auto_20210910_1637'),
    ]

    operations = [
        migrations.CreateModel(
            name='position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_title', models.CharField(choices=[('法定代表人', '法定代表人'), ('经营者', '经营者')], default='法定代表人', max_length=20)),
                ('position_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position_company', to='mainsite.company')),
                ('position_individual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position_individual', to='mainsite.individual')),
            ],
        ),
    ]