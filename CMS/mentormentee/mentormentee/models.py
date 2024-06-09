from django.db import models
from django.contrib.auth.models import User

class MentorProfile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    emp_id = models.CharField(max_length=255, unique=True, db_index=True)
    department = models.CharField(max_length=255)
    phone = models.IntegerField()
    address = models.TextField(max_length=455)
    user_type = models.CharField(max_length=100, default='mentor')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} (mentor) {self.emp_id} (Employee Id)"