# Generated by Django 4.2.16 on 2025-02-25 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_brand_brand_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='lenscleaner',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
