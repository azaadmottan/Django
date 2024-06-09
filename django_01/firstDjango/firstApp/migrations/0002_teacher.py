# Generated by Django 5.0.6 on 2024-06-03 05:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_name', models.CharField(max_length=255)),
                ('teacher_email', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2024, 6, 3, 5, 59, 21, 646022, tzinfo=datetime.timezone.utc))),
                ('teacher_subject', models.ManyToManyField(to='firstApp.subject')),
            ],
        ),
    ]