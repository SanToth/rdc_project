# Generated by Django 4.2.6 on 2023-10-21 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_remove_cell_site_controller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alarm',
            name='site_controller',
        ),
    ]
