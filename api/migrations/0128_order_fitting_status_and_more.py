# Generated by Django 4.2.16 on 2025-05-24 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0127_merge_20250524_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='fitting_status',
            field=models.CharField(choices=[('fitting_ok', 'Pending'), ('not_fitting', 'Not Fitting'), ('damage', 'Damage')], default='not_fitting', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='fitting_status_updated_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
