from django.contrib import admin
from .models import UserPost, Author, Book, Student, Course, Teacher, Subject, Profile

# Register your models here.

class BookInline(admin.TabularInline):
    model = Book
    extra = 2
    fields = ['bookTitle', 'bookAuthor']

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('authorName', 'created_at')
    inlines = [BookInline]

class BookAdmin(admin.ModelAdmin):
    list_display = ('bookTitle', 'bookAuthor')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('studentName', 'created_at')
    search_fields = ('studentName', 'created_at')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('courseName', 'created_at')
    filter_horizontal = ('students', )
    search_fields = ('courseName', 'created_at')

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacherName', 'created_at')
    search_fields = ('teacherName', 'created_at')

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subjectName', 'created_at')
    search_fields = ('subjectName', 'created_at')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('studentName', 'studentClass', 'created_at')
    search_fields = ('studentName', 'created_at')
    list_filter = ('studentName', 'created_at')

admin.site.register(UserPost)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Profile, ProfileAdmin)