# Generated by Django 4.2.16 on 2025-02-01 05:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_remove_orderitem_remark_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='sales_staff_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='refractiondetails',
            name='refraction',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='refraction_details', to='api.refraction'),
        ),
    ]
