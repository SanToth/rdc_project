# Generated by Django 4.2.6 on 2023-10-21 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_alarm_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarm',
            name='priority',
            field=models.CharField(choices=[('CR', 'Critical'), ('MJ', 'Major'), ('MN', 'Minor')], default='MJ', max_length=2),
        ),
    ]