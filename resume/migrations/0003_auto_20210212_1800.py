# Generated by Django 3.1.6 on 2021-02-12 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0002_auto_20210212_1720'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='education',
            options={'managed': True, 'permissions': [('private_closed', 'Private closed'), ('private_open', 'Private open'), ('public_closed', 'Public closed'), ('public_open', 'Public open')]},
        ),
    ]