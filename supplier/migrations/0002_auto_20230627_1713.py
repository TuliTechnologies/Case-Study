# Generated by Django 3.0.6 on 2023-06-27 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='updated_by',
            field=models.CharField(default=False, max_length=255),
        ),
        migrations.AddField(
            model_name='supplieraddress',
            name='updated_by',
            field=models.CharField(default=False, max_length=255),
        ),
    ]