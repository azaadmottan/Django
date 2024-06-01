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
    
# Foreign key constraints (One to Many relations)

class Author(models.Model):
    authorName = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.authorName} (Author)"

class Book(models.Model):
    bookAuthor = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    bookTitle = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.bookTitle} (Book)"

# Many to Many relationship

class Student(models.Model):
    studentName = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.studentName} (Student)"
    
class Course(models.Model):
    courseName = models.CharField(max_length=255)
    students = models.ManyToManyField(Student, related_name="students")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.courseName} (Course)"

# One to One relationship

class Teacher(models.Model):
    teacherName = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.teacherName} (Teacher)"

class Subject(models.Model):
    subjectName = models.CharField(max_length=255)
    teachers = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.subjectName} (Subject)"

class Profile(models.Model):
    studentName = models.CharField(max_length=255)
    studentAge = models.IntegerField()
    studentClass = models.CharField(max_length=255)
    studentSubject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.studentName} (Profile)"