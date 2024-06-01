from django.db import models

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