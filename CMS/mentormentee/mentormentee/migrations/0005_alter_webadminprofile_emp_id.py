# Generated by Django 5.0.6 on 2024-06-11 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentormentee', '0004_webadminprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webadminprofile',
            name='emp_id',
            field=models.CharField(db_index=True, max_length=255, unique=True),
        ),
    ]
