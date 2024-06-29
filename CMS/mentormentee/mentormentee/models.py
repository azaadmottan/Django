from django.db import models
from django.contrib.auth.models import User

class WebAdminProfile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name='web_admin_profile')
    emp_id = models.CharField(max_length=255, unique=True, db_index=True)
    phone = models.IntegerField()
    user_type = models.CharField(max_length=100, default='web_admin')
    dob = models.DateField(max_length=255, null=True, blank=True)
    address = models.TextField(max_length=455)
    profile_picture = models.ImageField(upload_to='webAdminProfilePicture/', blank=True, null=True)
    address = models.TextField(max_length=455)
    city = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} (web_admin) {self.emp_id} (Employee Id)"

class MentorProfile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    emp_id = models.CharField(max_length=255, unique=True, db_index=True)
    department = models.CharField(max_length=255)
    phone = models.IntegerField()
    user_type = models.CharField(max_length=100, default='mentor')
    profile_picture = models.ImageField(upload_to='mentorProfilePicture/', blank=True, null=True)
    dob = models.DateField(max_length=255, null=True, blank=True)
    address = models.TextField(max_length=455)
    city = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} (mentor) {self.emp_id} (Employee Id)"

class MenteeProfile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentee_profile')
    roll_no = models.IntegerField(unique=True)
    course = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    semester = models.CharField(max_length=255)
    user_type = models.CharField(max_length=255, default='mentee')
    mentor = models.ForeignKey(MentorProfile, on_delete=models.SET_NULL, null=True, blank=True)
    dob = models.DateField(max_length=255, null=True, blank=True)
    phone = models.IntegerField()
    father_name = models.CharField(max_length=255)
    father_phone = models.IntegerField()
    father_profession = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='menteeProfilePicture/', blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} (mentee) {self.roll_no} (Roll No)"

class MenteeQuery(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing/InProgress'),
        ('completed', 'Completed')
    ]
    mentee_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentee_name')
    mentor_name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='mentor_name')
    subject = models.CharField(max_length=355)
    description = models.TextField(max_length=1000)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.mentee_name} (mentee) | {self.mentor_name} (mentor) | {self.subject} (subject)"

class Notification(models.Model):
    USER_TYPE_NOTIFICATION = [
        ('public', 'Public'),
        ('web_admin', 'Web Admin'),
        ('mentor', 'Mentor'),
        ('mentee', 'Mentee')
    ]
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=2000)
    user_notification_type = models.CharField(max_length=255, choices=USER_TYPE_NOTIFICATION, default='public')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} | {self.user_notification_type}"
