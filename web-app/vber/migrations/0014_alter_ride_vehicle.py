# Generated by Django 4.1.5 on 2023-02-03 01:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vber', '0013_alter_ride_sharer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='vehicle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vber.vehicle'),
        ),
    ]