# Generated by Django 4.2.3 on 2023-07-29 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='formData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formId', models.CharField(max_length=250)),
                ('name', models.CharField(max_length=250)),
                ('createdAt', models.DateTimeField()),
                ('updatedAt', models.DateTimeField()),
            ],
        ),
    ]
