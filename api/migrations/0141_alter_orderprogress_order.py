# Generated by Django 4.2.16 on 2025-06-03 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0140_remove_order_progress_status_orderprogress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderprogress',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_progress_status', to='api.order'),
        ),
    ]
