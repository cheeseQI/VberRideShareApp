# Generated by Django 4.1.6 on 2023-02-05 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vber', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_name',
            field=models.CharField(max_length=20),
        ),
    ]