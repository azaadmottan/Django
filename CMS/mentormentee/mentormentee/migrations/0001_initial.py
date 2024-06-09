# Generated by Django 5.0.6 on 2024-06-08 14:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MentorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.CharField(db_index=True, max_length=255, unique=True)),
                ('department', models.CharField(max_length=255)),
                ('phone', models.IntegerField()),
                ('address', models.TextField(max_length=455)),
                ('user_type', models.CharField(default='mentor', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentor_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]