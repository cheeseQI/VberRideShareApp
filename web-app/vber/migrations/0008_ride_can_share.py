# Generated by Django 4.1.5 on 2023-02-01 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vber', '0007_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='can_share',
            field=models.BooleanField(default=False),
        ),
    ]
