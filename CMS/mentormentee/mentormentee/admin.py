from django.contrib import admin
from .models import MentorProfile

# Register your models here.

class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'emp_id', 'department', 'user_type')

admin.site.register(MentorProfile, MentorProfileAdmin)