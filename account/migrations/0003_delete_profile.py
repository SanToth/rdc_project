# Generated by Django 4.2.6 on 2023-10-28 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_remove_profile_photo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
