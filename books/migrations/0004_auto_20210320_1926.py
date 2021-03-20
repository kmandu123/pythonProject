# Generated by Django 3.1.6 on 2021-03-20 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_log_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='addr',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='주소'),
        ),
        migrations.AddField(
            model_name='log',
            name='city',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='city'),
        ),
        migrations.AddField(
            model_name='log',
            name='lat',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='위도'),
        ),
        migrations.AddField(
            model_name='log',
            name='long',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='경도'),
        ),
        migrations.AddField(
            model_name='log',
            name='state',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='state'),
        ),
    ]
