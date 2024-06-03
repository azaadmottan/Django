from django.db import models
from django.utils import timezone

# Create your models here.

class UserPost (models.Model):
    MODIFIER = [
        ('PUB', 'PUBLIC'),
        ('PRI', 'PRIVATE'),
        ('PRO', 'PROTECTED'),
    ]
    username = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    accModifier = models.CharField(max_length=100, choices=MODIFIER)
    description = models.TextField(max_length=500, blank=True)
    postPic = models.ImageField(upload_to='postPictures/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

# Foreign key constraints (Many to One relations)
class Subject(models.Model):
    subject_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.subject_name} (Subject)"

# One to One relationship
class Student(models.Model):
    student_name = models.CharField(max_length=255)
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subjects' , null=True)
    student_email = models.EmailField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student_name} (Student)"

class Profile(models.Model):
    student_name = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="profile")
    student_age = models.IntegerField()
    student_class = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student_name} (Student Profile)"

# Many to Many relationship
class Teacher(models.Model):
    teacher_name = models.CharField(max_length=255)
    teacher_subject = models.ManyToManyField(Subject)
    teacher_email = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{self.teacher_name} (Teacher Name)"