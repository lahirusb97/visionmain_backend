# Generated by Django 4.2.16 on 2025-06-02 16:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0136_order_is_refund_order_refund_note_order_refunded_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='MntOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mnt_number', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mnt_orders_admin', to=settings.AUTH_USER_MODEL)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mnt_orders_branch', to='api.branch')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mnt_orders', to='api.order')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mnt_orders_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
                'unique_together': {('order', 'mnt_number', 'branch')},
            },
        ),
    ]
