# Generated by Django 4.2.16 on 2025-03-29 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0073_merge_20250329_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='daily_invoice_no',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
