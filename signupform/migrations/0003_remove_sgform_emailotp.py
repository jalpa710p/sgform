# Generated by Django 4.2.6 on 2024-02-22 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signupform', '0002_sgform_emailotp_sgform_photp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sgform',
            name='emailotp',
        ),
    ]
