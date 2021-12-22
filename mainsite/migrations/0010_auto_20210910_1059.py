# Generated by Django 3.1 on 2021-09-10 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0009_remove_company_法定代表人'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='法定代表人',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='legal_rep', to='mainsite.individual'),
        ),
        migrations.AddField(
            model_name='company',
            name='经营者',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='operator', to='mainsite.individual'),
        ),
    ]