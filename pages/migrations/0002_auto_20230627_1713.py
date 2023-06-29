# Generated by Django 3.0.6 on 2023-06-27 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attributes',
            name='updated_by',
            field=models.CharField(default=False, max_length=255),
        ),
        migrations.AddField(
            model_name='attributevalues',
            name='updated_by',
            field=models.CharField(default=False, max_length=255),
        ),
        migrations.AddField(
            model_name='brands',
            name='updated_by',
            field=models.CharField(default=False, max_length=255),
        ),
        migrations.AddField(
            model_name='categories',
            name='updated_by',
            field=models.CharField(default=False, max_length=255),
        ),
        migrations.AddField(
            model_name='categoryfaq',
            name='updated_by',
            field=models.CharField(default=False, max_length=255),
        ),
        migrations.AddField(
            model_name='producttypeattributevalue',
            name='updated_by',
            field=models.CharField(default=False, max_length=255),
        ),
        migrations.AddField(
            model_name='producttypes',
            name='updated_by',
            field=models.CharField(default=False, max_length=255),
        ),
        migrations.AddField(
            model_name='shippingtype',
            name='updated_by',
            field=models.CharField(default=False, max_length=255),
        ),
    ]
