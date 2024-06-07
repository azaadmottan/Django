from django.contrib import admin
from .models import UserPost, Student, Profile, Subject, Teacher

# Register your models here.

class UserPostAdmin(admin.ModelAdmin):
    list_display = ('username', 'title', 'created_at')

class ProfileInline(admin.TabularInline):
    model = Profile
    extra = 1

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'subject_name', 'student_email', 'created_at')
    search_fields = ('student_name', 'created_at')
    inlines = [ProfileInline]

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'student_class', 'created_at')
    search_fields = ('student_name', 'student_class', 'created_at')

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'created_at')
    search_fields = ('subject_name', 'created_at')
    # inlines = [SubjectInline]

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_name', 'teacher_email', 'created_at')
    search_fields = ('teacher_name', 'created_at')
    filter_horizontal = ('teacher_subject', )

admin.site.register(UserPost, UserPostAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Teacher, TeacherAdmin)