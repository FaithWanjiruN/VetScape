# Generated by Django 5.1.2 on 2024-12-02 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VetApp', '0003_clinic_latitude_clinic_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinic',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='clinic_images/'),
        ),
    ]
