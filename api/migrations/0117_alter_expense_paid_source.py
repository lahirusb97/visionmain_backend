# Generated by Django 4.2.16 on 2025-05-11 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0116_alter_order_progress_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='paid_source',
            field=models.CharField(choices=[('safe', 'Safe'), ('cash', 'Cash'), ('bank', 'Bank')], max_length=20),
        ),
    ]
