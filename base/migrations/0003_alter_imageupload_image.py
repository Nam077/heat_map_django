# Generated by Django 4.1.7 on 2023-02-21 10:36

import base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageupload',
            name='image',
            field=models.ImageField(max_length=500, upload_to=base.models.upload_location),
        ),
    ]