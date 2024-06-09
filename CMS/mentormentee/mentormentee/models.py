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

class MenteeProfile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentee_profile')
    roll_no = models.IntegerField(unique=True)
    course = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    semester = models.CharField(max_length=255)
    mentor = models.ForeignKey(MentorProfile, on_delete=models.SET_NULL, null=True)
    phone = models.IntegerField()
    father_name = models.CharField(max_length=255)
    father_phone = models.IntegerField()
    father_profession = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='menteeProfilePicture/', blank=True)
    user_type = models.CharField(max_length=255, default='mentee')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} (mentee) {self.roll_no} (Roll No)"
