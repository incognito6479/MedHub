# Generated by Django 4.0.1 on 2022-01-28 22:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medhub', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='responder',
            name='poll',
        ),
    ]
