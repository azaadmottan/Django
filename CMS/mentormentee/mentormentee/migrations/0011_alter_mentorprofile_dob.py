# Generated by Django 5.0.6 on 2024-06-25 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentormentee', '0010_mentorprofile_city_mentorprofile_dob_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentorprofile',
            name='dob',
            field=models.DateField(blank=True, max_length=255, null=True),
        ),
    ]
