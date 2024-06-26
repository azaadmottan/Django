from django.contrib import admin
from .models import WebAdminProfile, MentorProfile, MenteeProfile, MenteeQuery

# Register your models here.

class WebAdminProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'emp_id', 'user_type', 'created_at', 'updated_at')

class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'emp_id', 'department', 'user_type', 'created_at', 'updated_at')

class MenteeProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'roll_no', 'course', 'branch', 'user_type', 'created_at', 'updated_at')

class MenteeQueryAdmin(admin.ModelAdmin):
    list_display = ('mentee_name', 'mentor_name', 'subject', 'created_at', 'updated_at')

admin.site.register(WebAdminProfile, WebAdminProfileAdmin)
admin.site.register(MentorProfile, MentorProfileAdmin)
admin.site.register(MenteeProfile, MenteeProfileAdmin)
admin.site.register(MenteeQuery, MenteeQueryAdmin)