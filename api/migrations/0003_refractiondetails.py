# Generated by Django 4.2.16 on 2024-12-17 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_refraction'),
    ]

    operations = [
        migrations.CreateModel(
            name='RefractionDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hb_rx_right', models.CharField(blank=True, max_length=10, null=True)),
                ('hb_rx_left', models.CharField(blank=True, max_length=10, null=True)),
                ('auto_ref', models.CharField(blank=True, max_length=20, null=True)),
                ('ntc', models.CharField(blank=True, max_length=10, null=True)),
                ('va_without_glass', models.CharField(blank=True, max_length=10, null=True)),
                ('va_without_ph', models.CharField(blank=True, max_length=10, null=True)),
                ('va_with_glass', models.CharField(blank=True, max_length=10, null=True)),
                ('right_eye_dist_sph', models.CharField(blank=True, max_length=10, null=True)),
                ('right_eye_dist_cyl', models.CharField(blank=True, max_length=10, null=True)),
                ('right_eye_dist_axis', models.CharField(blank=True, max_length=10, null=True)),
                ('right_eye_near_sph', models.CharField(blank=True, max_length=10, null=True)),
                ('left_eye_dist_sph', models.CharField(blank=True, max_length=10, null=True)),
                ('left_eye_dist_cyl', models.CharField(blank=True, max_length=10, null=True)),
                ('left_eye_dist_axis', models.CharField(blank=True, max_length=10, null=True)),
                ('left_eye_near_sph', models.CharField(blank=True, max_length=10, null=True)),
                ('remark', models.CharField(blank=True, max_length=20, null=True)),
                ('refraction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='api.refraction')),
            ],
        ),
    ]
