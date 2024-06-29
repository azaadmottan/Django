# Generated by Django 5.0.6 on 2024-06-29 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentormentee', '0015_webadminprofile_city_webadminprofile_dob_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('description', models.TextField(max_length=2000)),
                ('user_type_notification', models.CharField(choices=[('public', 'Public'), ('web_admin', 'Web Admin'), ('mentor', 'Mentor'), ('mentee', 'Mentee')], default='public', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]