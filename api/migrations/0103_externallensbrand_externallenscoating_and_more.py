# Generated by Django 4.2.16 on 2025-05-01 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0102_order_is_frame_only'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalLensBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExternalLensCoating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveConstraint(
            model_name='externallens',
            name='unique_lens_combination',
        ),
        migrations.AddConstraint(
            model_name='externallens',
            constraint=models.UniqueConstraint(fields=('lens_type', 'coating', 'brand', 'branded'), name='unique_external_lens_combination'),
        ),
        migrations.AlterField(
            model_name='externallens',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='external_lenses', to='api.externallensbrand'),
        ),
        migrations.AlterField(
            model_name='externallens',
            name='coating',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='external_lenses', to='api.externallenscoating'),
        ),
    ]
