# Generated by Django 4.2.16 on 2025-04-17 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0081_schedule_branch_alter_schedule_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='specialization',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
