# Generated by Django 4.2.16 on 2025-02-10 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_patient_refraction'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='brand_type',
            field=models.CharField(choices=[('frame', 'Frame Brand'), ('lens', 'Lens Brand'), ('both', 'Both Frame & Lens')], default='both', max_length=10),
        ),
    ]
