# Generated by Django 4.2.16 on 2025-04-05 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0079_merge_20250405_0506'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='api.branch'),
        ),
    ]
