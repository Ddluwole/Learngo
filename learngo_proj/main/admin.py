from django.contrib import admin
from .models import Teacher, CourseCategory, Student, Course, Chapter

# Register your models here.
admin.site.register(Teacher)
admin.site.register(CourseCategory)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Chapter)