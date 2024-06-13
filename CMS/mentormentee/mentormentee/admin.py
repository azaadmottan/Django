from django.contrib import admin
from .models import WebAdminProfile, MentorProfile, MenteeProfile

# Register your models here.

class WebAdminProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'emp_id', 'user_type')

class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'emp_id', 'department', 'user_type')

class MenteeProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'roll_no', 'course', 'branch', 'user_type')

admin.site.register(WebAdminProfile, WebAdminProfileAdmin)
admin.site.register(MentorProfile, MentorProfileAdmin)
admin.site.register(MenteeProfile, MenteeProfileAdmin)