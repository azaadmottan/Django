# Generated by Django 5.0.6 on 2024-06-08 15:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentormentee', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentorprofile',
            name='username',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mentor_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
