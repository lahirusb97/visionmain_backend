# Generated by Django 4.2.16 on 2025-02-05 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_framestock_limit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_type', models.CharField(choices=[('factory', 'Factory Invoice'), ('manual', 'Manual Invoice')], max_length=10)),
                ('daily_invoice_no', models.IntegerField(blank=True, null=True)),
                ('invoice_date', models.DateTimeField(auto_now_add=True)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='api.order')),
            ],
            options={
                'unique_together': {('invoice_date', 'daily_invoice_no')},
            },
        ),
    ]
