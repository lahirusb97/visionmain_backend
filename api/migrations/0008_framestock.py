# Generated by Django 4.2.16 on 2024-12-21 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_frame'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrameStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(default=0)),
                ('initial_count', models.IntegerField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='api.frame')),
            ],
        ),
    ]
