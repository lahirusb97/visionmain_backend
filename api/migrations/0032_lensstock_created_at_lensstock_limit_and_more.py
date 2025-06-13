# Generated by Django 4.2.16 on 2025-01-11 14:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_alter_appointment_channel_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='lensstock',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lensstock',
            name='limit',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='lensstock',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
