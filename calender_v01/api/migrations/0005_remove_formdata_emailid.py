# Generated by Django 4.2.3 on 2023-07-30 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_formdata_emailid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formdata',
            name='emailId',
        ),
    ]